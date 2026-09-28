import os

file_path = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_func = '''def capture_screen():
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
    root.after(3000, lambda: btn_capture.configure(text="📸 แคปหน้าจอ"))'''

new_func = '''def capture_screen():
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
    ps_cmd = f"Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; \ = [System.Drawing.Image]::FromFile('{filepath}'); [System.Windows.Forms.Clipboard]::SetImage(\)"
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], creationflags=subprocess.CREATE_NO_WINDOW)
    
    btn_capture.configure(text="📸 ก๊อปรูปลง Clipboard แล้ว!")
    root.after(3000, lambda: btn_capture.configure(text="📸 แคปหน้าจอ"))'''

if old_func in content:
    content = content.replace(old_func, new_func)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched!")
else:
    print("Function not found!")
