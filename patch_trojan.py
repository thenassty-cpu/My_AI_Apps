import re

file_path = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

sync_func = '''
def sync_trojan():
    dialog = ctk.CTkInputDialog(text="กรอก IP ของ Android Box (Termux):\\n(เช่น 192.168.1.xx)", title="ดึง Log ม้าโทรจัน")
    ip = dialog.get_input()
    if not ip: return
    
    btn_trojan.configure(state="disabled", text="กำลังซิงก์...")
    root.update()
    
    def task():
        try:
            url = f"http://{ip}:8000/trojan_log.json"
            req = urllib.request.urlopen(url, timeout=5)
            history = json.loads(req.read().decode('utf-8'))
            
            tabs = [tab_ton, tab_dong, tab_ball]
            
            for t in tabs:
                if not os.path.exists(t.csv_file): continue
                df = pd.read_csv(t.csv_file)
                df['time'] = pd.to_datetime(df['time'])
                
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
                            new_rows.append({
                                'time': std_time_dt,
                                'home': float(home_data["in"]),
                                'g1': float(g1_data["in"])
                            })
                
                if new_rows:
                    df = pd.concat([df, pd.DataFrame(new_rows)])
                    df = df.sort_values(by='time').drop_duplicates(subset=['time'])
                    df.to_csv(t.csv_file, index=False)
                    
            root.after(0, lambda: btn_trojan.configure(state="normal", text="สำเร็จ! กราฟอัปเดตแล้ว"))
            root.after(3000, lambda: btn_trojan.configure(text="🐎 ดึง Log ม้าโทรจัน (Sync)"))
            for t in tabs: root.after(0, t.update_graph)
            
        except Exception as e:
            root.after(0, lambda: btn_trojan.configure(state="normal", text="❌ เชื่อมต่อ IP ไม่ได้"))
            root.after(3000, lambda: btn_trojan.configure(text="🐎 ดึง Log ม้าโทรจัน (Sync)"))
            
    threading.Thread(target=task, daemon=True).start()

'''

btn_code = '''
btn_trojan = ctk.CTkButton(frame_footer, text="🐎 ดึง Log ม้าโทรจัน (Sync)", font=FONT_BTN, command=sync_trojan, width=220, height=35, fg_color="#c0392b", hover_color="#e74c3c")
btn_trojan.pack(side="right", padx=10)
'''

# Insert sync_func before fetch_data
content = content.replace('def fetch_data(manual=False):', sync_func + '\\ndef fetch_data(manual=False):')

# Insert btn_code before btn_refresh
content = content.replace('btn_refresh = ctk.CTkButton(frame_footer', btn_code + '\\nbtn_refresh = ctk.CTkButton(frame_footer')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added Sync Trojan feature!")
