import os

file_path = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update fetch_data new_row to include g2
old_row = "new_row = pd.DataFrame({'time': [std_time], 'home': [float(home_val)], 'g1': [float(g1_val)]})"
new_row = "new_row = pd.DataFrame({'time': [std_time], 'home': [float(home_val)], 'g1': [float(g1_val)], 'g2': [float(g2_val)]})"
content = content.replace(old_row, new_row)

# 2. Update plot_graph to draw 3 lines
old_plot = '''self.ax.plot(df['time'], df['home'], color="#e74c3c", marker="o", markersize=4, label="หน้าบ้าน/จุดหลัก")
            self.ax.plot(df['time'], df['g1'], color="#f1c40f", marker="x", markersize=4, label="จุดสกัด/ต้นน้ำ")
            self.ax.legend(loc="lower left", facecolor="#2c3e50", edgecolor="#7f8c8d", labelcolor="white")'''
            
new_plot = '''self.ax.plot(df['time'], df['home'], color="#e74c3c", marker="o", markersize=4, label="หน้าบ้าน/จุดหลัก")
            self.ax.plot(df['time'], df['g1'], color="#f1c40f", marker="x", markersize=4, label="จุดสกัด/ต้นน้ำ")
            if 'g2' in df.columns:
                self.ax.plot(df['time'], df['g2'], color="#3498db", marker="s", markersize=3, label="ปลายทางระบาย")
            self.ax.legend(loc="lower left", facecolor="#2c3e50", edgecolor="#7f8c8d", labelcolor="white", fontsize=8)'''
content = content.replace(old_plot, new_plot)

# 3. Add Screen Capture function and button
capture_func = '''
def capture_screen():
    import os, datetime
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
    btn_capture.configure(text="📸 เซฟรูปลง Desktop แล้ว!")
    root.after(3000, lambda: btn_capture.configure(text="📸 แคปหน้าจอ"))

btn_capture = ctk.CTkButton(frame_footer, text="📸 แคปหน้าจอ", font=FONT_BTN, command=capture_screen, width=150, height=35, fg_color="#8e44ad", hover_color="#9b59b6")
btn_capture.pack(side="left", padx=10)
'''

# We will inject the button logic right before btn_trojan
btn_trojan_line = '''def sync_trojan():'''
content = content.replace(btn_trojan_line, capture_func + "\n" + btn_trojan_line)

# 4. Update trojan sync to include g2
old_sync_row = '''new_rows.append({
                                'time': std_time_dt,
                                'home': float(home_data["in"]),
                                'g1': float(g1_data["in"])
                            })'''
new_sync_row = '''
                            g2_data = data.get(t.g2_code)
                            g2_val = float(g2_data["in"]) if g2_data else 0.0
                            new_rows.append({
                                'time': std_time_dt,
                                'home': float(home_data["in"]),
                                'g1': float(g1_data["in"]),
                                'g2': g2_val
                            })'''
content = content.replace(old_sync_row, new_sync_row)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patch applied successfully!")
