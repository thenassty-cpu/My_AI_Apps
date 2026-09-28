import os

file_path = r'C:\Users\ITss-Advice\Documents\GitHub\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_code = '''def sync_trojan():
    dialog = ctk.CTkInputDialog(text="กรอก IP ของ Android Box (Termux):\n(เช่น 192.168.1.xxx)", title="ดึง Log โทรจัน", font=("Tahoma", 16))
    ip = dialog.get_input()
    if not ip: return'''

new_code = '''def sync_trojan():
    # Hardcoded IP for convenience, as requested by P'Ton
    ip = "192.168.1.59"
    if not ip: return'''

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched!")
else:
    print("Not found! Let's try with raw bytes if encoding is messed up.")
