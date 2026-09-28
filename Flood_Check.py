import urllib.request
import re
import json

print('กำลังดึงข้อมูลระดับน้ำจากเว็บ กทม. (อาจใช้เวลา 10-20 วินาที)...')

url = 'https://weather.bangkok.go.th/water/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}
req = urllib.request.Request(url, headers=headers)

try:
    res = urllib.request.urlopen(req, timeout=30)
    html = res.read().decode('utf-8')
    
    # พยายามดึงข้อมูลที่เกี่ยวกับ "ภาษีเจริญ"
    print('\n=== รายงานระดับน้ำ คลองภาษีเจริญ ===')
    
    # มองหาโครงสร้างตารางหรือสคริปต์ที่ซ่อนอยู่ (เว็บ กทม. มักจะมี id หรือ tag ระบุ)
    # เราจะใช้วิธีตัด string แบบง่ายๆ ก่อน
    matches = re.finditer(r'(.{0,50})ภาษีเจริญ(.{0,100})', html)
    
    found = False
    for m in matches:
        text = m.group(0).replace('\n', ' ').strip()
        # กรองเฉพาะบรรทัดที่น่าจะเป็นข้อมูลตัวเลข
        if re.search(r'\d+\.\d+', text):
            print('-', text)
            found = True
            
    if not found:
        print('ดึงข้อมูลสำเร็จ แต่ไม่พบตัวเลขระดับน้ำที่ชัดเจนในรูปแบบ Text (อาจอยู่ในรูปแบบแผนที่ Map)')
        
    print('\n[ช่องทางเช็กด้วยตัวเอง]')
    print('เข้าไปที่: https://weather.bangkok.go.th/water/')
    print('1. กดแท็บ "สถานีวัดระดับน้ำ"')
    print('2. ค้นหา "ภาษีเจริญ" เพื่อดูระดับน้ำจริงเทียบกับระดับตลิ่ง')

except Exception as e:
    print('เกิดข้อผิดพลาดในการดึงข้อมูล:', e)
