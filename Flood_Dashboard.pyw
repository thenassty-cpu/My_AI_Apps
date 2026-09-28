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

mpl.rc('font', family='Tahoma')
mpl.rcParams['axes.unicode_minus'] = False

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("BKK Flood Monitor V14 (Sensor Offline Detection - ประจาน กทม.)")
root.geometry("1100x550")
root.resizable(False, False)

icon_path = "C:/Users/ITss-Advice/Desktop/My_AI_Apps/flood_icon.ico"
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

FONT_TITLE = ("Tahoma", 16, "bold")
FONT_BIG = ("Tahoma", 46, "bold")
FONT_MED = ("Tahoma", 32, "bold")
FONT_SUB = ("Tahoma", 13)
FONT_TREND = ("Tahoma", 14)
FONT_BTN = ("Tahoma", 14, "bold")
CARD_BG = "#22272e"

frame_left = ctk.CTkFrame(root, fg_color="transparent", width=620, height=550)
frame_left.pack_propagate(False) 
frame_left.pack(side="left", fill="y", expand=False)

frame_right = ctk.CTkFrame(root, fg_color=CARD_BG, corner_radius=10)
frame_right.pack(side="right", fill="both", expand=True, padx=(5, 15), pady=15)

frame_top = ctk.CTkFrame(frame_left, fg_color="transparent")
frame_top.pack(fill="x", padx=15, pady=(15, 5))

frame_neighbors = ctk.CTkFrame(frame_top, fg_color="transparent")
frame_neighbors.pack(fill="x")

card_nk = ctk.CTkFrame(frame_neighbors, fg_color=CARD_BG, corner_radius=10, height=100)
card_nk.pack_propagate(False)
card_nk.pack(side="left", fill="x", expand=True, padx=(0, 5))
ctk.CTkLabel(card_nk, text="ต้นน้ำ (หนองแขม)", font=FONT_SUB, text_color="gray").pack(pady=(10,0))
lbl_nk_val = ctk.CTkLabel(card_nk, text="-- ม.", font=FONT_MED)
lbl_nk_val.pack()
lbl_nk_trend = ctk.CTkLabel(card_nk, text="--", font=FONT_TREND, text_color="gray")
lbl_nk_trend.pack(pady=(0,10))

card_bk = ctk.CTkFrame(frame_neighbors, fg_color=CARD_BG, corner_radius=10, height=100)
card_bk.pack_propagate(False)
card_bk.pack(side="right", fill="x", expand=True, padx=(5, 0))
ctk.CTkLabel(card_bk, text="กลางน้ำ (บางแค)", font=FONT_SUB, text_color="gray").pack(pady=(10,0))
lbl_bk_val = ctk.CTkLabel(card_bk, text="-- ม.", font=FONT_MED)
lbl_bk_val.pack()
lbl_bk_trend = ctk.CTkLabel(card_bk, text="--", font=FONT_TREND, text_color="gray")
lbl_bk_trend.pack(pady=(0,10))

card_home = ctk.CTkFrame(frame_top, fg_color=CARD_BG, corner_radius=10, height=180)
card_home.pack_propagate(False)
card_home.pack(fill="x", pady=10)
ctk.CTkLabel(card_home, text="🏠 คลองภาษีเจริญ (หน้าบ้านพี่ต้น)", font=FONT_TITLE, text_color="white").pack(pady=(15,0))
lbl_home_val = ctk.CTkLabel(card_home, text="--", font=FONT_BIG)
lbl_home_val.pack(pady=5)
lbl_home_trend = ctk.CTkLabel(card_home, text="(รอโหลดข้อมูล...)", font=FONT_TREND, text_color="gray")
lbl_home_trend.pack(pady=(0, 10))

frame_bot = ctk.CTkFrame(frame_left, fg_color="transparent")
frame_bot.pack(fill="x", padx=15, pady=(0, 10))

card_rain = ctk.CTkFrame(frame_bot, fg_color=CARD_BG, corner_radius=10, height=100)
card_rain.pack_propagate(False)
card_rain.pack(side="left", fill="x", expand=True, padx=(0, 5))
ctk.CTkLabel(card_rain, text="☁️ ฝน 24 ชม. (บางแวก)", font=FONT_SUB, text_color="gray").pack(pady=(10,0))
lbl_rain_val = ctk.CTkLabel(card_rain, text="-- %", font=FONT_MED, text_color="#3498db")
lbl_rain_val.pack()
lbl_rain_trend = ctk.CTkLabel(card_rain, text="ปริมาณสะสม: -- mm", font=FONT_TREND, text_color="gray")
lbl_rain_trend.pack(pady=(0,10))

card_dam = ctk.CTkFrame(frame_bot, fg_color=CARD_BG, corner_radius=10, height=100)
card_dam.pack_propagate(False)
card_dam.pack(side="right", fill="x", expand=True, padx=(5, 0))
ctk.CTkLabel(card_dam, text="🏭 เจ้าพระยา / เขื่อน", font=FONT_SUB, text_color="gray").pack(pady=(10,0))
lbl_out_val = ctk.CTkLabel(card_dam, text="-- ม.", font=FONT_MED, text_color="#e67e22")
lbl_out_val.pack()
ctk.CTkLabel(card_dam, text="ระบายน้ำ: 1,950 ลบ.ม./วิ", font=FONT_TREND, text_color="gray").pack(pady=(0,10))

frame_footer = ctk.CTkFrame(frame_left, fg_color="transparent", height=40)
frame_footer.pack_propagate(False)
frame_footer.pack(fill="x", padx=15, pady=5)
lbl_status = ctk.CTkLabel(frame_footer, text="กำลังเตรียมข้อมูล...", font=FONT_SUB, text_color="gray")
lbl_status.pack(side="left", padx=5)
btn_refresh = ctk.CTkButton(frame_footer, text="อัปเดตข้อมูล", font=FONT_BTN, command=lambda: fetch_data(manual=True), width=180, height=35)
btn_refresh.pack(side="right")

lbl_graph_title = ctk.CTkLabel(frame_right, text="📈 กราฟระดับน้ำย้อนหลัง (อัปเดตออโต้ทุก 30 นาที)", font=FONT_TITLE, text_color="white")
lbl_graph_title.pack(pady=10)
fig = Figure(figsize=(4, 4), dpi=100, facecolor=CARD_BG)
ax = fig.add_subplot(111)
ax.set_facecolor(CARD_BG)
canvas = FigureCanvasTkAgg(fig, master=frame_right)
canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))

# --- Logic ---
last_fetch_time = 0
is_fetching = False
COOLDOWN_SECONDS = 300 
AUTO_REFRESH_MS = 30 * 60 * 1000  # 30 mins
HISTORY_FILE = "C:/Users/ITss-Advice/Desktop/My_AI_Apps/flood_history.json"
CSV_FILE = "C:/Users/ITss-Advice/Desktop/My_AI_Apps/flood_data.csv"
user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36']

def get_color_emoji(status_class):
    if "bg-success" in status_class: return "#2ecc71"
    if "bg-warning" in status_class: return "#f39c12"
    if "bg-danger" in status_class: return "#e74c3c"
    return "white"

def update_graph():
    if not os.path.exists(CSV_FILE): return
    try:
        df = pd.read_csv(CSV_FILE)
        df['time'] = pd.to_datetime(df['time'])
        df = df.tail(24)
        
        ax.clear()
        ax.plot(df['time'], df['level_in'], label="ในประตู (คลอง)", color="#f39c12", marker="o", linewidth=2)
        ax.plot(df['time'], df['level_out'], label="นอกประตู (เจ้าพระยา)", color="#3498db", marker="x", linewidth=2)
        
        ax.set_facecolor(CARD_BG)
        ax.tick_params(colors='gray')
        ax.spines['bottom'].set_color('gray')
        ax.spines['top'].set_color(CARD_BG) 
        ax.spines['right'].set_color(CARD_BG)
        ax.spines['left'].set_color('gray')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.legend(facecolor=CARD_BG, labelcolor='white')
        fig.tight_layout()
        canvas.draw()
    except: pass

def append_to_csv(time_str, level_in, level_out):
    try:
        parts = time_str.split(" ")
        d_parts = parts[0].split("/")
        std_time = f"{int(d_parts[2])-543}-{d_parts[1]}-{d_parts[0]} {parts[1]}"
        
        new_row = pd.DataFrame({'time': [std_time], 'level_in': [float(level_in)], 'level_out': [float(level_out)]})
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            if std_time not in df['time'].values:
                new_row.to_csv(CSV_FILE, mode='a', header=False, index=False)
        else:
            new_row.to_csv(CSV_FILE, index=False)
        update_graph()
    except: pass

def update_ui_from_data(data, is_cache=False, diffs=None):
    if not data: return
    if not diffs: diffs = {}
    
    # หนองแขม
    if "WL.PSC.05" in data:
        c = data["WL.PSC.05"]
        lbl_nk_val.configure(text=f"{c['in']} ม.", text_color="gray" if c.get("offline") else get_color_emoji(c['status']))
        if c.get("offline"):
            lbl_nk_trend.configure(text="❌ เซ็นเซอร์ กทม. ขัดข้อง", text_color="#e74c3c")
        else:
            diff = diffs.get("WL.PSC.05", 0)
            if is_cache:
                lbl_nk_trend.configure(text="(ข้อมูลเก่าใน Cache)", text_color="gray")
            else:
                lbl_nk_trend.configure(text=f"🔺 +{diff:.2f}" if diff > 0 else f"🔽 {diff:.2f}" if diff < 0 else "คงที่", text_color="gray")
                
    # บางแค
    if "WL.PSC.02" in data:
        c = data["WL.PSC.02"]
        lbl_bk_val.configure(text=f"{c['in']} ม.", text_color="gray" if c.get("offline") else get_color_emoji(c['status']))
        if c.get("offline"):
            lbl_bk_trend.configure(text="❌ เซ็นเซอร์ กทม. ขัดข้อง", text_color="#e74c3c")
        else:
            diff = diffs.get("WL.PSC.02", 0)
            if is_cache:
                lbl_bk_trend.configure(text="(ข้อมูลเก่าใน Cache)", text_color="gray")
            else:
                lbl_bk_trend.configure(text=f"🔺 +{diff:.2f}" if diff > 0 else f"🔽 {diff:.2f}" if diff < 0 else "คงที่", text_color="gray")
                
    # ภาษีเจริญ
    if "WL.PSC.01" in data:
        c = data["WL.PSC.01"]
        lbl_home_val.configure(text=f"{c['in']} ม.", text_color="gray" if c.get("offline") else get_color_emoji(c['status']))
        lbl_out_val.configure(text=f"{c['out']} ม.")
        if c.get("offline"):
            lbl_home_trend.configure(text="❌ เซ็นเซอร์หลัก กทม. ขัดข้อง", text_color="#e74c3c")
        else:
            diff = diffs.get("WL.PSC.01", 0)
            if is_cache:
                lbl_home_trend.configure(text="โหลดจาก Cache...", text_color="gray")
            else:
                lbl_home_trend.configure(text=f"เทียบรอบก่อน: 🔺 +{diff:.2f}" if diff > 0 else f"เทียบรอบก่อน: 🔽 {diff:.2f}" if diff < 0 else "เทียบรอบก่อน: คงที่", text_color="gray")
                
    if "timestamp" in data:
        lbl_status.configure(text=f"อัปเดตล่าสุด: {data['timestamp']} {'(Cache)' if is_cache else ''}")

def load_initial_cache():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f: 
                cache_data = json.load(f)
                update_ui_from_data(cache_data, is_cache=True)
        except: pass
    update_graph()

def update_timer():
    global last_fetch_time, is_fetching
    if not is_fetching and last_fetch_time > 0:
        elapsed = time.time() - last_fetch_time
        if elapsed < COOLDOWN_SECONDS:
            remaining = int(COOLDOWN_SECONDS - elapsed)
            mins, secs = divmod(remaining, 60)
            btn_refresh.configure(state="disabled", text=f"รออัปเดต ({mins}:{secs:02d})")
        else:
            if btn_refresh.cget("state") == "disabled":
                btn_refresh.configure(state="normal", text="อัปเดตข้อมูล")
    root.after(1000, update_timer)

def fetch_data(manual=False):
    global is_fetching, last_fetch_time
    if manual and (time.time() - last_fetch_time) < COOLDOWN_SECONDS and last_fetch_time != 0: return
        
    is_fetching = True
    btn_refresh.configure(state="disabled", text="กำลังดึงข้อมูล...")
    root.update()

    def task():
        global last_fetch_time, is_fetching
        try:
            url_w = "https://api.open-meteo.com/v1/forecast?latitude=13.737&longitude=100.456&hourly=precipitation_probability,precipitation&forecast_days=2&timezone=Asia%2FBangkok"
            res_w = urllib.request.urlopen(url_w, timeout=10)
            w_data = json.loads(res_w.read().decode('utf-8'))
            curr_hour = datetime.datetime.now().hour
            lbl_rain_val.configure(text=f"{max(w_data['hourly']['precipitation_probability'][curr_hour:curr_hour+24])}%")
            lbl_rain_trend.configure(text=f"สะสม: {sum(w_data['hourly']['precipitation'][curr_hour:curr_hour+24]):.1f} mm")
        except: pass

        try:
            url = 'https://weather.bangkok.go.th/water/'
            req = urllib.request.Request(url, headers={'User-Agent': random.choice(user_agents), 'Accept': 'text/html'})
            res = urllib.request.urlopen(req, timeout=15)
            html = res.read().decode('utf-8')
            
            pattern = r"(WL\.PSC\.\d{2})\s*:\s*.*?'([-\d\.]+)'.*?'([-\d\.]+)'.*?'(\d{2}/\d{2}/\d{4} \d{2}:\d{2})'.*?(bg-success|bg-warning|bg-danger)"
            matches = re.finditer(pattern, html)
            
            current_data = {}
            time_str = ""
            for m in matches:
                code, lvl_in, lvl_out, timestamp, status = m.groups()
                current_data[code] = {"in": lvl_in, "out": lvl_out, "status": status}
                if code == "WL.PSC.01": time_str = timestamp
                
            prev_data = {}
            if os.path.exists(HISTORY_FILE):
                try:
                    with open(HISTORY_FILE, 'r') as f: prev_data = json.load(f)
                except: pass
            
            # --- SHAME THE SENSOR LOGIC ---
            merged_data = {}
            diffs = {}
            for code in ["WL.PSC.05", "WL.PSC.02", "WL.PSC.01"]:
                if code in current_data:
                    merged_data[code] = current_data[code]
                    merged_data[code]["offline"] = False
                    try: diffs[code] = float(current_data[code]['in']) - float(prev_data.get(code, {}).get("in", current_data[code]['in']))
                    except: diffs[code] = 0
                elif code in prev_data:
                    # Sensor is missing in new fetch! Fallback to cache and flag it.
                    merged_data[code] = prev_data[code]
                    merged_data[code]["offline"] = True
                    diffs[code] = 0
            
            if not time_str and "timestamp" in prev_data:
                time_str = prev_data["timestamp"]
                
            merged_data["timestamp"] = time_str
            with open(HISTORY_FILE, 'w') as f: json.dump(merged_data, f)
            
            update_ui_from_data(merged_data, is_cache=False, diffs=diffs)
            
            if "WL.PSC.01" in current_data:
                append_to_csv(time_str, current_data["WL.PSC.01"]["in"], current_data["WL.PSC.01"]["out"])
            
        except Exception as e:
            lbl_status.configure(text="เชื่อมต่อ กทม. ล้มเหลว (ใช้ Cache)")
        
        last_fetch_time = time.time()
        is_fetching = False

    threading.Thread(target=task, daemon=True).start()

def auto_refresh_loop():
    fetch_data(manual=False)
    root.after(AUTO_REFRESH_MS, auto_refresh_loop)

load_initial_cache()
update_timer()
root.after(1000, auto_refresh_loop)

root.mainloop()
