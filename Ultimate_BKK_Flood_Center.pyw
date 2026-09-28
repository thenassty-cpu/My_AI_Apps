import customtkinter as ctk
import urllib.request
import re
import threading
import time
import random
import json
import os
import datetime
import pandas as pd
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

mpl.rc('font', family='Kanit')
mpl.rcParams['axes.unicode_minus'] = False

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Ultimate BKK Flood Center V15 (3-in-1 Edition)")
root.geometry("1250x720")
root.resizable(False, False)

icon_path = "flood_icon.ico"
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

FONT_TITLE = ctk.CTkFont(family="Kanit", size=18, weight="bold")
FONT_BIG = ctk.CTkFont(family="Kanit", size=52, weight="bold")
FONT_MED = ctk.CTkFont(family="Kanit", size=36, weight="bold")
FONT_SUB = ctk.CTkFont(family="Kanit", size=15)
FONT_TREND = ctk.CTkFont(family="Kanit", size=16)
FONT_BTN = ctk.CTkFont(family="Kanit", size=16, weight="bold")
CARD_BG = "#22272e"
FONT_PEAK = ctk.CTkFont(family="Kanit", size=14)
FONT_TIDE = ctk.CTkFont(family="Kanit", size=15, weight="bold")

HISTORY_FILE = "flood_history_master.json"

def get_color_emoji(status_class):
    if "bg-success" in status_class: return "#2ecc71"
    if "bg-warning" in status_class: return "#f39c12"
    if "bg-danger" in status_class: return "#e74c3c"
    return "white"

class DashboardTab:
    def __init__(self, parent, title_home, title_g1, title_g2, title_graph, csv_file, coords, home_code, g1_code, g2_code):
        self.parent = parent
        self.csv_file = csv_file
        self.coords = coords
        self.home_code = home_code
        self.g1_code = g1_code
        self.g2_code = g2_code
        
        self.frame_left = ctk.CTkFrame(parent, fg_color="transparent", width=620)
        self.frame_left.pack(side="left", fill="y", expand=False)

        self.frame_right = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=10)
        self.frame_right.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        # Top
        frame_top = ctk.CTkFrame(self.frame_left, fg_color="transparent")
        frame_top.pack(fill="x", padx=10, pady=(10, 5))
        frame_neighbors = ctk.CTkFrame(frame_top, fg_color="transparent")
        frame_neighbors.pack(fill="x")

        # G1
        card_g1 = ctk.CTkFrame(frame_neighbors, fg_color=CARD_BG, corner_radius=10)
        card_g1.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkLabel(card_g1, text=title_g1, font=FONT_SUB, text_color="gray").pack(pady=(10,0))
        self.lbl_g1_val = ctk.CTkLabel(card_g1, text="-- ม.", font=FONT_MED)
        self.lbl_g1_val.pack()
        self.lbl_g1_trend = ctk.CTkLabel(card_g1, text="--", font=FONT_TREND, text_color="gray")
        self.lbl_g1_trend.pack(pady=(0,10))

        # G2
        card_g2 = ctk.CTkFrame(frame_neighbors, fg_color=CARD_BG, corner_radius=10)
        card_g2.pack(side="right", fill="x", expand=True, padx=(5, 0))
        ctk.CTkLabel(card_g2, text=title_g2, font=FONT_SUB, text_color="gray").pack(pady=(10,0))
        self.lbl_g2_val = ctk.CTkLabel(card_g2, text="-- ม.", font=FONT_MED)
        self.lbl_g2_val.pack()
        self.lbl_g2_trend = ctk.CTkLabel(card_g2, text="--", font=FONT_TREND, text_color="gray")
        self.lbl_g2_trend.pack(pady=(0,10))

        # Home
        card_home = ctk.CTkFrame(frame_top, fg_color=CARD_BG, corner_radius=10)
        card_home.pack(fill="x", pady=10)
        ctk.CTkLabel(card_home, text=title_home, font=FONT_TITLE, text_color="white").pack(pady=(15,0))
        self.lbl_home_val = ctk.CTkLabel(card_home, text="--", font=FONT_BIG)
        self.lbl_home_val.pack(pady=5)
        self.lbl_home_trend = ctk.CTkLabel(card_home, text="(รอโหลดข้อมูล...)", font=FONT_TREND, text_color="gray")
        self.lbl_home_trend.pack(pady=(0, 2))
        self.lbl_home_peak = ctk.CTkLabel(card_home, text="รอคำนวณสถิติ 24 ชม...", font=FONT_PEAK, text_color="gray")
        self.lbl_home_peak.pack(pady=(0, 10))

        # Bot
        frame_bot = ctk.CTkFrame(self.frame_left, fg_color="transparent")
        frame_bot.pack(fill="x", padx=10, pady=(0, 10))
        card_rain = ctk.CTkFrame(frame_bot, fg_color=CARD_BG, corner_radius=10)
        card_rain.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkLabel(card_rain, text="☁️ ฝน 24 ชม. (พิกัดบ้าน)", font=FONT_SUB, text_color="gray").pack(pady=(10,0))
        self.lbl_rain_val = ctk.CTkLabel(card_rain, text="-- %", font=FONT_MED, text_color="#3498db")
        self.lbl_rain_val.pack()
        self.lbl_rain_trend = ctk.CTkLabel(card_rain, text="ปริมาณสะสม: -- mm", font=FONT_TREND, text_color="gray")
        self.lbl_rain_trend.pack(pady=(0,10))

        card_info = ctk.CTkFrame(frame_bot, fg_color=CARD_BG, corner_radius=10)
        card_info.pack(side="right", fill="x", expand=True, padx=(5, 0))
        self.lbl_info_title = ctk.CTkLabel(card_info, text="💡 เทียบน้ำนอกประตู (แม่น้ำ)", font=FONT_SUB, text_color="gray")
        self.lbl_info_title.pack(pady=(10,0))
        self.lbl_info_val = ctk.CTkLabel(card_info, text="ติดตามใกล้ชิด", font=FONT_TITLE, text_color="#e67e22")
        self.lbl_info_val.pack(pady=5)
        
        # Tide
        frame_bot_2 = ctk.CTkFrame(self.frame_left, fg_color="transparent")
        frame_bot_2.pack(fill="x", padx=10, pady=(0, 10))
        card_tide = ctk.CTkFrame(frame_bot_2, fg_color=CARD_BG, corner_radius=10)
        card_tide.pack(fill="x", expand=True)
        ctk.CTkLabel(card_tide, text="🌊 ตารางน้ำขึ้น-น้ำลง (ท่าเรือกรุงเทพ / กองทัพเรือ)", font=FONT_SUB, text_color="gray").pack(pady=(5,0))
        
        # เพิ่มตัวแปรวันที่แบบ Dynamic เพื่อให้รู้ว่าข้อมูลของวันไหน
        today_str = datetime.datetime.now().strftime("%d/%m/%Y")
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        tomorrow_str = tomorrow.strftime("%d/%m/%Y")
        
        tide_text = f"🔴 สูงสุด ({today_str}): 18:43 น. (2.83ม.)  |  🟢 ต่ำสุด: 00:50 น. (1.35ม.)\n⚠️ น้ำหนุนอีกรอบ ({tomorrow_str}): 05:52 น. (2.38ม.)"
        self.lbl_tide = ctk.CTkLabel(card_tide, text=tide_text, font=FONT_TIDE, text_color="#f1c40f")
        self.lbl_tide.pack(pady=(5, 10))
        
        # Graph
        frame_gh = ctk.CTkFrame(self.frame_right, fg_color="transparent")
        frame_gh.pack(fill="x", padx=10, pady=10)
        lbl_graph_title = ctk.CTkLabel(frame_gh, text=title_graph, font=FONT_TITLE, text_color="white")
        lbl_graph_title.pack(side="left")
        
        self.zoom_val = 24
        
        def on_zoom_change(choice):
            if choice == "12 ชม.": self.zoom_val = 24
            elif choice == "24 ชม.": self.zoom_val = 48
            elif choice == "48 ชม.": self.zoom_val = 96
            self.update_graph()
            
        self.seg_zoom = ctk.CTkSegmentedButton(frame_gh, values=["12 ชม.", "24 ชม.", "48 ชม."], font=FONT_BTN, command=on_zoom_change)
        self.seg_zoom.set("12 ชม.")
        self.seg_zoom.pack(side="right")
        
        self.fig = Figure(figsize=(4, 4), dpi=100, facecolor=CARD_BG)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(CARD_BG)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_right)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def update_graph(self):
        if not os.path.exists(self.csv_file): return
        try:
            df = pd.read_csv(self.csv_file)
            df['time'] = pd.to_datetime(df['time'], format='mixed')
            df = df.tail(self.zoom_val)
            
            if not df.empty:
                max_val = df['home'].max()
                current_val = df['home'].iloc[-1]
                diff_cm = (max_val - current_val) * 100
                if diff_cm > 0:
                    self.lbl_home_peak.configure(text=f"📉 ลดจากจุดสูงสุด (24 ชม.): {diff_cm:.0f} ซม.", text_color="#2ecc71")
                elif diff_cm < 0:
                    self.lbl_home_peak.configure(text=f"📈 สูงกว่าสถิติเดิม: {abs(diff_cm):.0f} ซม.", text_color="#e74c3c")
                else:
                    self.lbl_home_peak.configure(text="⚠️ ระดับน้ำแตะจุดพีกสุดของวัน!", text_color="#f39c12")
            
            self.ax.clear()
            self.ax.plot(df['time'], df['home'], label="หน้าบ้าน/จุดหลัก", color="#e74c3c", marker="o", linewidth=2)
            self.ax.plot(df['time'], df['g1'], label="จุดสกัด/ต้นน้ำ", color="#f39c12", marker="x", linewidth=2)
            self.ax.set_facecolor(CARD_BG)
            self.ax.tick_params(colors='gray')
            for spine in self.ax.spines.values(): spine.set_color('gray')
            self.ax.spines['top'].set_color(CARD_BG)
            self.ax.spines['right'].set_color(CARD_BG)
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            self.ax.legend(facecolor=CARD_BG, labelcolor='white')
            self.fig.tight_layout()
            self.canvas.draw()
        except Exception as e: print('RAIN ERROR:', e)

    def append_csv(self, time_str, home_val, g1_val, g2_val=0.0):
        try:
            parts = time_str.split(" ")
            d_parts = parts[0].split("/")
            std_time = f"{int(d_parts[2])-543}-{d_parts[1]}-{d_parts[0]} {parts[1]}"
            new_row = pd.DataFrame({'time': [std_time], 'home': [float(home_val)], 'g1': [float(g1_val)], 'g2': [float(g2_val)]})
            if os.path.exists(self.csv_file):
                df = pd.read_csv(self.csv_file)
                if std_time not in df['time'].values:
                    new_row.to_csv(self.csv_file, mode='a', header=False, index=False)
            else:
                new_row.to_csv(self.csv_file, index=False)
            self.update_graph()
        except Exception as e: print('RAIN ERROR:', e)

    def update_ui(self, data, is_cache, diffs):
        def apply_ui(lbl_val, lbl_trend, code):
            if code in data:
                c = data[code]
                lbl_val.configure(text=f"{c['in']} ม.", text_color="gray" if c.get("offline") else get_color_emoji(c['status']))
                if c.get("offline"):
                    lbl_trend.configure(text="❌ กทม. ขัดข้อง", text_color="#e74c3c")
                else:
                    diff = diffs.get(code, 0)
                    if is_cache: lbl_trend.configure(text="(ข้อมูลเก่าใน Cache)", text_color="gray")
                    else: lbl_trend.configure(text=f"🔺 +{diff:.2f}" if diff>0 else f"🔽 {diff:.2f}" if diff<0 else "คงที่", text_color="gray")
        
        apply_ui(self.lbl_home_val, self.lbl_home_trend, self.home_code)
        apply_ui(self.lbl_g1_val, self.lbl_g1_trend, self.g1_code)
        apply_ui(self.lbl_g2_val, self.lbl_g2_trend, self.g2_code)
        
        # IN vs OUT Comparison for Home Gate
        if self.home_code in data:
            c = data[self.home_code]
            if c.get('offline'):
                self.lbl_info_val.configure(text="เซ็นเซอร์ขัดข้อง", text_color="#e74c3c")
            else:
                try:
                    val_in = float(c['in'])
                    val_out = float(c['out'])
                    diff = val_out - val_in
                    if diff > 0:
                        self.lbl_info_val.configure(text=f"น้ำนอกสูงกว่า {abs(diff):.2f} ม.", text_color="#e74c3c")
                    elif diff < 0:
                        self.lbl_info_val.configure(text=f"น้ำในสูงกว่า {abs(diff):.2f} ม.", text_color="#2ecc71")
                    else:
                        self.lbl_info_val.configure(text="น้ำใน/นอก เท่ากัน", text_color="#f39c12")
                except:
                    self.lbl_info_val.configure(text="ไม่มีค่าน้ำนอกประตู", text_color="gray")
        
        if self.home_code in data and self.g1_code in data:
            g2_val = data[self.g2_code]["in"] if self.g2_code and self.g2_code in data and not data[self.g2_code].get("offline") else 0.0
            self.append_csv(data["timestamp"], data[self.home_code]["in"], data[self.g1_code]["in"], g2_val)

# Setup Tabs
tabview = ctk.CTkTabview(root, width=1080, height=650)
tabview._segmented_button.configure(font=FONT_BTN)
tabview.pack(padx=10, pady=(0, 10), fill="both", expand=True)

t1 = tabview.add("🏠 ภาษีเจริญ (พี่ต้น)")
t2 = tabview.add("🏭 คลองสอง (เสี่ยโด่ง)")
t3 = tabview.add("🏡 พระยาสุเรนทร์ (บอล)")

tab_ton = DashboardTab(t1, "🏠 คลองภาษีเจริญ (หน้าบ้านพี่ต้น)", "ต้นน้ำ (หนองแขม)", "กลางน้ำ (บางแค)", "📈 กราฟความเสี่ยงน้ำท่วม (ภาษีเจริญ)", "flood_data_ton.csv", (13.737, 100.456), "WL.PSC.01", "WL.PSC.05", "WL.PSC.02")
tab_dong = DashboardTab(t2, "🏭 คลองสองสายใต้ (โกดังเสี่ยโด่ง)", "กำแพง กทม. (คลองหกวา)", "ปลายทางหลัก (แสนแสบ)", "📈 กราฟความเสี่ยงน้ำท่วม (คลอง 2)", "flood_data_dong.csv", (13.9569, 100.6520), "WL.SST.01", "WL.KHW.01", "WL.SSB.09")
tab_ball = DashboardTab(t3, "🏡 พระยาสุเรนทร์ (บ้านคุณบอล)", "ต้นน้ำ (พระยาสุเรนทร์)", "ปลายทางระบายน้ำ (แสนแสบ)", "📈 กราฟความเสี่ยงน้ำท่วม (ตะวันออก)", "flood_data_ball.csv", (13.862383, 100.695103), "WL.SWA.01", "WL.PSR.01", "WL.SSB.09")
tabview.add("🏡 สายไหม 85 (ปอกะดั่น)")
t4 = tabview.tab("🏡 สายไหม 85 (ปอกะดั่น)")
tab_por = DashboardTab(t4, "🏡 สายไหม 85 (บ้านปอกะดั่น)", "ต้นน้ำ (หกวา)", "ปลายทาง (พระยาสุเรนทร์)", "📈 กราฟความเสี่ยงน้ำท่วม (สายไหม)", "flood_data_por.csv", (13.927, 100.688), "WL.KHW.01", "WL.SST.01", "WL.PSR.01")


frame_footer = ctk.CTkFrame(root, fg_color="transparent", height=40)
frame_footer.pack_propagate(False)
frame_footer.pack(fill="x", padx=15, pady=(0,10))
lbl_status = ctk.CTkLabel(frame_footer, text="กำลังเตรียมข้อมูล...", font=FONT_SUB, text_color="gray")
lbl_status.pack(side="left", padx=10)

current_font = "Kanit"
def toggle_font():
    global current_font
    current_font = "Tahoma" if current_font == "Kanit" else "Kanit"
    
    # Update CTkFonts
    FONT_TITLE.configure(family=current_font)
    FONT_BIG.configure(family=current_font)
    FONT_MED.configure(family=current_font)
    FONT_SUB.configure(family=current_font)
    FONT_TREND.configure(family=current_font)
    FONT_BTN.configure(family=current_font)
    FONT_PEAK.configure(family=current_font)
    FONT_TIDE.configure(family=current_font)
    
    # Update Matplotlib
    mpl.rc('font', family=current_font)
    for t in [tab_ton, tab_dong, tab_ball, tab_por]:
        t.update_graph()
        
    btn_font.configure(text=f"🔠 สลับฟอนต์ (ปัจจุบัน: {current_font})")

btn_font = ctk.CTkButton(frame_footer, text="🔠 สลับฟอนต์ (ปัจจุบัน: Kanit)", font=FONT_BTN, command=toggle_font, width=220, height=35, fg_color="#8e44ad", hover_color="#9b59b6")
btn_font.pack(side="left", padx=10)



def capture_screen():
    import os, datetime, subprocess
    from PIL import ImageGrab
    x = root.winfo_rootx()
    y = root.winfo_rooty()
    w = root.winfo_width()
    h = root.winfo_height()
    img = ImageGrab.grab(bbox=(x, y, x+w, y+h))
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    filename = f"Dashboard_Snap_{datetime.datetime.now().strftime('%H%M%S')}.png"
    filepath = os.path.join(desktop, filename)
    img.save(filepath)
    
    # Copy to clipboard via PowerShell
    ps_cmd = f"Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; $img = [System.Drawing.Image]::FromFile('{filepath}'); [System.Windows.Forms.Clipboard]::SetImage($img)"
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], creationflags=subprocess.CREATE_NO_WINDOW)
    
    btn_capture.configure(text="📸 ก๊อปรูปลง Clipboard แล้ว!")
    root.after(3000, lambda: btn_capture.configure(text="📸 แคปหน้าจอ"))

btn_capture = ctk.CTkButton(frame_footer, text="📸 แคปหน้าจอ", font=FONT_BTN, command=capture_screen, width=150, height=35, fg_color="#8e44ad", hover_color="#9b59b6")
btn_capture.pack(side="left", padx=10)

def sync_trojan():
    ip = entry_ip.get().strip()
    if not ip: return
    import json
    with open("trojan_config.json", "w") as f:
        json.dump({"ip": ip}, f)
    root.clipboard_clear()
    root.clipboard_append(ip)
    root.update()
    
    btn_trojan.configure(state="disabled", text="กำลังซิงก์...")
    root.update()
    
    def task():
        try:
            import subprocess
            adb = r"C:\Users\ITss-Advice\adb_tools\platform-tools\adb.exe"
            
            # 1. Connect
            subprocess.run([adb, "connect", ip], capture_output=True)
            
            # 2. Master-Slave Syncing (bypass sandbox using run-as)
            # We use run-as cat and pipe it directly to a local file
            cmd = f'"{adb}" -s {ip} shell "run-as com.termux cat /data/data/com.termux/files/home/trojan_log.json" > trojan_log.json'
            pull_result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if "error" in pull_result.stderr.lower() or "is not debuggable" in pull_result.stderr.lower():
                raise Exception(f"ADB Pull Error: {pull_result.stderr}")
                
            if not os.path.exists("trojan_log.json"):
                raise Exception("Cannot find pulled trojan_log.json")
                
            try:
                with open("trojan_log.json", "r", encoding="utf-16") as f:
                    history = json.load(f)
            except Exception:
                with open("trojan_log.json", "r", encoding="utf-8") as f:
                    history = json.load(f)
            
            tabs = [tab_ton, tab_dong, tab_ball, tab_por]
            
            for t in tabs:
                if not os.path.exists(t.csv_file): continue
                df = pd.read_csv(t.csv_file)
                df['time'] = pd.to_datetime(df['time'], format='mixed')
                
                new_rows = []
                for rec in history:
                    bma_time = rec.get("bma_time")
                    if not bma_time: continue
                    parts = bma_time.split(" ")
                    d_parts = parts[0].split("/")
                    std_time = f"{int(d_parts[2])-543}-{d_parts[1]}-{d_parts[0]} {parts[1]}"
                    std_time_dt = pd.to_datetime(std_time)
                    
                    if std_time_dt not in df['time'].values:
                        data = rec.get("data", {})
                        home_data = data.get(t.home_code)
                        g1_data = data.get(t.g1_code)
                        if home_data and g1_data:
                            
                            g2_data = data.get(t.g2_code)
                            g2_val = float(g2_data["in"]) if g2_data else 0.0
                            new_rows.append({
                                'time': std_time_dt,
                                'home': float(home_data["in"]),
                                'g1': float(g1_data["in"]),
                                'g2': g2_val
                            })
                
                if new_rows:
                    df = pd.concat([df, pd.DataFrame(new_rows)])
                    df = df.sort_values(by='time').drop_duplicates(subset=['time'])
                    df.to_csv(t.csv_file, index=False)
                    
            root.after(0, lambda: btn_trojan.configure(state="normal", text="สำเร็จ! อัปเดตแล้ว"))
            root.after(3000, lambda: btn_trojan.configure(text="🐎 ดึง Log ม้าโทรจัน (Sync)"))
            for t in tabs: root.after(0, t.update_graph)
            
        except Exception as e:
            import traceback
            with open('crash_log_sync.txt', 'w', encoding='utf-8') as f_log:
                traceback.print_exc(file=f_log)
            print("Sync Error:", e)
            root.after(0, lambda: btn_trojan.configure(state="normal", text="❌ ดึงไฟล์ ADB พลาด"))
            root.after(3000, lambda: btn_trojan.configure(text="🐎 ดึง Log ม้าโทรจัน (Sync)"))
            
    threading.Thread(target=task, daemon=True).start()

# --- Trojan IP Config ---
CONFIG_FILE = "trojan_config.json"
default_ip = "192.168.1.59"
import os, json
if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            default_ip = json.load(f).get("ip", "192.168.1.59")
    except: pass

entry_ip = ctk.CTkEntry(frame_footer, font=FONT_BTN, width=130, height=35)
entry_ip.insert(0, default_ip)
entry_ip.pack(side="right", padx=(0, 10))

btn_trojan = ctk.CTkButton(frame_footer, text="🐎 ดึง Log ม้าโทรจัน (Sync)", font=FONT_BTN, command=lambda: threading.Thread(target=sync_trojan).start(), width=220, height=35, fg_color="#c0392b", hover_color="#e74c3c")
btn_trojan.pack(side="right", padx=10)
btn_refresh = ctk.CTkButton(frame_footer, text="อัปเดตข้อมูล (ทุกแท็บ)", font=FONT_BTN, command=lambda: fetch_data(manual=True), width=180, height=35)
btn_refresh.pack(side="right", padx=10)

last_fetch_time = 0
is_fetching = False
COOLDOWN_SECONDS = 300 
AUTO_REFRESH_MS = 30 * 60 * 1000

def update_timer():
    global last_fetch_time, is_fetching
    if not is_fetching and last_fetch_time > 0:
        elapsed = time.time() - last_fetch_time
        if elapsed < COOLDOWN_SECONDS:
            rem = int(COOLDOWN_SECONDS - elapsed)
            btn_refresh.configure(state="disabled", text=f"รออัปเดต ({rem//60}:{rem%60:02d})")
        else:
            if btn_refresh.cget("state") == "disabled": btn_refresh.configure(state="normal", text="อัปเดตข้อมูล (ทุกแท็บ)")
    root.after(1000, update_timer)


def fetch_data(manual=False):
    global is_fetching, last_fetch_time
    if manual and (time.time() - last_fetch_time) < COOLDOWN_SECONDS and last_fetch_time != 0: return
    is_fetching = True
    btn_refresh.configure(state="disabled", text="กำลังดึงข้อมูล BMA...")
    root.update()

    def task():
        global last_fetch_time, is_fetching
        for t in [tab_ton, tab_dong, tab_ball, tab_por]:
            try:
                url_w = f"https://api.open-meteo.com/v1/forecast?latitude={t.coords[0]}&longitude={t.coords[1]}&hourly=precipitation_probability,precipitation&forecast_days=2&timezone=Asia%2FBangkok"
                res_w = urllib.request.urlopen(url_w, timeout=10)
                w_data = json.loads(res_w.read().decode('utf-8'))
                curr = datetime.datetime.now().hour
                
                probs = w_data['hourly']['precipitation_probability'][curr:curr+24]
                precs = w_data['hourly']['precipitation'][curr:curr+24]
                times = w_data['hourly']['time'][curr:curr+24]
                
                max_prob = max(probs)
                total_prec = sum(precs)
                t.lbl_rain_val.configure(text=f"{max_prob}%")
                
                if total_prec > 0.1:
                    max_idx = precs.index(max(precs))
                    peak_time = times[max_idx][-5:] # Gets 'HH:MM'
                    t.lbl_rain_trend.configure(text=f"สะสม: {total_prec:.1f} mm | หนักสุด: {peak_time} น.")
                else:
                    t.lbl_rain_trend.configure(text=f"สะสม: {total_prec:.1f} mm | ไม่มีแนวโน้มฝน")
            except Exception as e: print('RAIN ERROR:', e)

        try:
            req = urllib.request.Request('https://weather.bangkok.go.th/water/', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/115.0.0.0'})
            html = urllib.request.urlopen(req, timeout=15).read().decode('utf-8')
            
            pattern = r"(WL\.PSC\.\d{2}|WL\.SST\.01|WL\.KHW\.01|WL\.KSG\.01|WL\.SWA\.01|WL\.SSB\.09|WL\.PSR\.01)\s*:\s*.*?'([-\d\.]+)'.*?'([-\d\.]+)'.*?'(\d{2}/\d{2}/\d{4} \d{2}:\d{2})'.*?(bg-success|bg-warning|bg-danger)"
            matches = re.finditer(pattern, html)
            
            current = {}
            time_str = ""
            for m in matches:
                code, lvl_in, lvl_out, timestamp, status = m.groups()
                current[code] = {"in": lvl_in, "out": lvl_out, "status": status}
                if code == "WL.PSC.01": time_str = timestamp
                
            prev = {}
            if os.path.exists(HISTORY_FILE):
                try:
                    with open(HISTORY_FILE, 'r') as f: prev = json.load(f)
                except Exception as e: print('RAIN ERROR:', e)
            
            merged = {}
            diffs = {}
            all_codes = ["WL.PSC.05", "WL.PSC.02", "WL.PSC.01", "WL.SST.01", "WL.KHW.01", "WL.KSG.01", "WL.SWA.01", "WL.SSB.09", "WL.PSR.01"]
            for c in all_codes:
                if c in current:
                    merged[c] = current[c]
                    merged[c]["offline"] = False
                    try: diffs[c] = float(current[c]['in']) - float(prev.get(c, {}).get("in", current[c]['in']))
                    except: diffs[c] = 0
                elif c in prev:
                    merged[c] = prev[c]
                    merged[c]["offline"] = True
                    diffs[c] = 0
            
            if not time_str and "timestamp" in prev: time_str = prev["timestamp"]
            merged["timestamp"] = time_str
            with open(HISTORY_FILE, 'w') as f: json.dump(merged, f)
            
            for t in [tab_ton, tab_dong, tab_ball, tab_por]: t.update_ui(merged, is_cache=False, diffs=diffs)
            lbl_status.configure(text=f"อัปเดตล่าสุด: {time_str}")
        except Exception as e:
            import traceback
            with open('crash_log.txt', 'w', encoding='utf-8') as f:
                traceback.print_exc(file=f)
            lbl_status.configure(text="เชื่อมต่อ กทม. ล้มเหลว (ใช้ Cache)")

        last_fetch_time = time.time()
        is_fetching = False

    threading.Thread(target=task, daemon=True).start()

def load_initial():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f: 
                cache = json.load(f)
                for t in [tab_ton, tab_dong, tab_ball, tab_por]: t.update_ui(cache, is_cache=True, diffs={})
                if "timestamp" in cache: lbl_status.configure(text=f"อัปเดตล่าสุด: {cache['timestamp']} (Cache)")
        except Exception as e: print('RAIN ERROR:', e)
    for t in [tab_ton, tab_dong, tab_ball, tab_por]: t.update_graph()

def auto_refresh_loop():
    fetch_data(manual=False)
    root.after(AUTO_REFRESH_MS, auto_refresh_loop)

load_initial()
update_timer()
root.after(1000, auto_refresh_loop)
root.mainloop()
