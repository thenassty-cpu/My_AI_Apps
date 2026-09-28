// ==========================================
// BKK Flood Logger (24/7 Google Apps Script)
// ==========================================

const SHEET_NAME = "Data";

// 1. ฟังก์ชันหลักสำหรับดึงข้อมูลและบันทึกลงชีต (จะตั้งเวลาให้รันทุก 30 นาที)
function fetchBMAAndSave() {
  const url = 'https://weather.bangkok.go.th/water/';
  
  // ปลอมตัวเป็น Browser (Spoofing) เพื่อทะลุ Firewall กทม.
  const options = {
    'method' : 'get',
    'headers': {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
      'Accept': 'text/html',
      'Referer': 'https://weather.bangkok.go.th/'
    },
    'muteHttpExceptions': true
  };
  
  try {
    const response = UrlFetchApp.fetch(url, options);
    const html = response.getContentText();
    
    // ใช้ Regex ดึงข้อมูล
    const regex = /(WL\.PSC\.\d{2})\s*:\s*.*?\'([-\d\.]+)\'.*?\'([-\d\.]+)\'.*?\'(\d{2}\/\d{2}\/\d{4} \d{2}:\d{2})\'.*?(bg-success|bg-warning|bg-danger)/g;
    let match;
    let dataMap = {};
    let bmaTime = "";
    
    while ((match = regex.exec(html)) !== null) {
      let code = match[1];
      let levelIn = match[2];
      let levelOut = match[3];
      let timeStr = match[4];
      
      dataMap[code] = {
        in: levelIn,
        out: levelOut
      };
      if (code === "WL.PSC.01") {
        bmaTime = timeStr;
      }
    }
    
    // ถ้าดึงสำเร็จและมีข้อมูลหน้าบ้าน (PSC.01)
    if (dataMap["WL.PSC.01"]) {
      const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
      if (!sheet) return;
      
      // ดึงเวลาปัจจุบันของเซิร์ฟเวอร์
      const timestamp = Utilities.formatDate(new Date(), "Asia/Bangkok", "yyyy-MM-dd HH:mm:ss");
      
      // ลำดับคอลัมน์: เวลาเซิร์ฟเวอร์, เวลา กทม., หนองแขม(ใน), บางแค(ใน), หน้าบ้าน(ใน), หน้าบ้าน(นอก)
      const psc05 = dataMap["WL.PSC.05"] ? dataMap["WL.PSC.05"].in : "";
      const psc02 = dataMap["WL.PSC.02"] ? dataMap["WL.PSC.02"].in : "";
      const psc01_in = dataMap["WL.PSC.01"].in;
      const psc01_out = dataMap["WL.PSC.01"].out;
      
      // เช็กก่อนว่า เวลา กทม. ซ้ำกับแถวล่าสุดไหม (ถ้า กทม. ไม่อัปเดต เราจะไม่บันทึกซ้ำซ้อน)
      const lastRow = sheet.getLastRow();
      if (lastRow > 1) {
        const lastBmaTime = sheet.getRange(lastRow, 2).getValue();
        if (lastBmaTime == bmaTime) {
          Logger.log("กทม. ยังไม่อัปเดตข้อมูล (เวลาเดิม: " + bmaTime + ") ข้ามการบันทึก");
          return;
        }
      }
      
      sheet.appendRow([timestamp, bmaTime, psc05, psc02, psc01_in, psc01_out]);
      Logger.log("บันทึกข้อมูลเรียบร้อย: " + bmaTime);
    }
    
  } catch (e) {
    Logger.log("Error: " + e.toString());
  }
}

// 2. ฟังก์ชัน API สำหรับปล่อยข้อมูลให้ Python (หรือหน้าเว็บ) ดึงไปวาดกราฟ
function doGet(e) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
  const lastRow = sheet.getLastRow();
  
  // ถ้าไม่มีข้อมูล
  if (lastRow <= 1) {
    return ContentService.createTextOutput(JSON.stringify({status: "empty"}))
      .setMimeType(ContentService.MimeType.JSON);
  }
  
  // ดึงข้อมูล 48 แถวล่าสุด (ประมาณ 24 ชั่วโมง) ไปวาดกราฟ
  const numRows = Math.min(48, lastRow - 1);
  const startRow = lastRow - numRows + 1;
  const data = sheet.getRange(startRow, 1, numRows, 6).getValues();
  
  let result = [];
  for (let i = 0; i < data.length; i++) {
    result.push({
      timestamp: data[i][0],
      bma_time: data[i][1],
      psc05_in: data[i][2],
      psc02_in: data[i][3],
      psc01_in: data[i][4],
      psc01_out: data[i][5]
    });
  }
  
  return ContentService.createTextOutput(JSON.stringify(result))
    .setMimeType(ContentService.MimeType.JSON);
}
