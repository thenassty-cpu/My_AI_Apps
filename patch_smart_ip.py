import os
import json

file_path = r'C:\Users\ITss-Advice\Documents\GitHub\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add a config loading logic at the top (or just read/write from a simple txt file in the sync_trojan scope)
# Let's just modify frame_footer

old_footer = '''btn_trojan = ctk.CTkButton(frame_footer, text="🐎 ดึง Log ม้าโทรจัน (Sync)", font=FONT_BTN, command=lambda: threading.Thread(target=sync_trojan).start(), width=200, height=35, fg_color="#c0392b", hover_color="#e74c3c")
btn_trojan.pack(side="right", padx=10)'''

new_footer = '''
# --- Trojan IP Config ---
CONFIG_FILE = "trojan_config.json"
default_ip = "192.168.1.59"
if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, "r") as f:
            default_ip = json.load(f).get("ip", "192.168.1.59")
    except: pass

entry_ip = ctk.CTkEntry(frame_footer, font=FONT_BTN, width=130, height=35)
entry_ip.insert(0, default_ip)
entry_ip.pack(side="right", padx=(0, 10))

btn_trojan = ctk.CTkButton(frame_footer, text="🐎 ดึง Log (Sync)", font=FONT_BTN, command=lambda: threading.Thread(target=sync_trojan).start(), width=150, height=35, fg_color="#c0392b", hover_color="#e74c3c")
btn_trojan.pack(side="right", padx=5)
'''

# Update sync_trojan to use the IP from the entry field
old_sync = '''def sync_trojan():
    ip = "192.168.1.59"
    if not ip: return
    root.clipboard_clear()'''

new_sync = '''def sync_trojan():
    ip = entry_ip.get().strip()
    if not ip: return
    # Save to config
    import json
    with open(CONFIG_FILE, "w") as f:
        json.dump({"ip": ip}, f)
        
    root.clipboard_clear()'''

if 'def sync_trojan():' in content:
    content = content.replace(old_footer, new_footer)
    content = content.replace(old_sync, new_sync)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched Smart IP Entry!")
else:
    print("Failed to patch.")
