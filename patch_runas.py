import re

file_path = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_task = '''    def task():
        try:
            import subprocess
            adb = r"C:\\Users\\ITss-Advice\\adb_tools\\platform-tools\\adb.exe"
            
            # 1. Connect
            subprocess.run([adb, "connect", ip], capture_output=True)
            
            # 2. Cat the file directly using run-as (bypassing sandbox and sdcard)
            result = subprocess.run([adb, "-s", ip, "shell", "run-as com.termux cat /data/data/com.termux/files/home/trojan_log.json"], capture_output=True, text=True, encoding='utf-8')
            
            if not result.stdout or "No such file" in result.stdout or "Permission denied" in result.stdout:
                raise Exception("Cannot read file via run-as")
                
            history = json.loads(result.stdout)
            
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
                    
            root.after(0, lambda: btn_trojan.configure(state="normal", text="สำเร็จ! อัปเดตแล้ว"))
            root.after(3000, lambda: btn_trojan.configure(text="🐎 ดึง Log ม้าโทรจัน (Sync)"))
            for t in tabs: root.after(0, t.update_graph)
            
        except Exception as e:
            print("Sync Error:", e)
            root.after(0, lambda: btn_trojan.configure(state="normal", text="❌ ดึงไฟล์ ADB พลาด"))
            root.after(3000, lambda: btn_trojan.configure(text="🐎 ดึง Log ม้าโทรจัน (Sync)"))'''

match = re.search(r'    def task\(\):.*?threading\.Thread\(target=task, daemon=True\)\.start\(\)', content, re.DOTALL)
if match:
    old_task_full = match.group(0)
    new_code = new_task + '\n            \n    threading.Thread(target=task, daemon=True).start()'
    content = content.replace(old_task_full, new_code)
    
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated to use run-as cat!")
