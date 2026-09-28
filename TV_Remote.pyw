import tkinter as tk
import subprocess

adb_path = r"C:\Users\ITss-Advice\adb_tools\platform-tools\adb.exe"
ip = "192.168.1.59"

def run_adb(args):
    try:
        result = subprocess.run([adb_path] + args, capture_output=True, text=True, creationflags=0x08000000)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

def connect_tv():
    status_label.config(text="Connecting...", fg="orange")
    root.update()
    out = run_adb(['connect', ip])
    if "connected" in out or "already" in out:
        status_label.config(text="Status: Connected ✅", fg="#2ecc71")
    else:
        status_label.config(text="Status: Failed ❌", fg="#e74c3c")


def launch_app(package_name):
    # Mapping package names to their exact Android TV (Leanback) activities
    activities = {
        'com.hbo.asia.androidtv': 'com.wbd.stream/com.wbd.beam.BeamActivity',
        'com.doonung.dtv': 'com.doonung.dtv/com.doonung.activity.tv.ui.TVSplashActivity',
        'com.ais.mimo.aisplay.tv': 'com.ais.mimo.aisplay.tv/com.amt.launcher_ais.ui.activity.LoginActivity',
        'com.google.android.youtube.tv': 'com.google.android.youtube.tv/com.google.android.apps.youtube.tv.activity.ShellActivity'
    }
    
    if package_name in activities:
        run_adb(['shell', 'am', 'start', '-n', activities[package_name]])
    else:
        run_adb(['shell', 'monkey', '-p', package_name, '-c', 'android.intent.category.LEANBACK_LAUNCHER', '1'])

def send_key(keycode):
    run_adb(['shell', 'input', 'keyevent', str(keycode)])

def send_text(event=None):
    text = text_entry.get()
    if text:
        formatted_text = text.replace(" ", "%s")
        run_adb(['shell', 'input', 'text', formatted_text])
        text_entry.delete(0, tk.END)

def youtube_search(event=None):
    text = text_entry.get()
    if text:
        formatted_text = text.replace(" ", "+")
        run_adb(['shell', 'am', 'start', '-d', f'"vnd.youtube://results?search_query={formatted_text}"', '-a', 'android.intent.action.VIEW', '-p', 'com.google.android.youtube.tv'])
        text_entry.delete(0, tk.END)

root = tk.Tk()
root.title("3BB TV Remote V3")
root.geometry("340x700")
root.configure(bg="#2c3e50")
root.attributes("-topmost", True)

tk.Label(root, text="3BB Ghost Remote 👻", font=("Tahoma", 16, "bold"), bg="#2c3e50", fg="white").pack(pady=10)

status_label = tk.Label(root, text="Status: Unknown", font=("Tahoma", 10), bg="#2c3e50", fg="white")
status_label.pack()

tk.Button(root, text="CONNECT / WAKE", bg="#f39c12", fg="white", font=("Tahoma", 10, "bold"), command=connect_tv).pack(pady=5)


# App Shortcuts Section
frame_apps = tk.Frame(root, bg="#2c3e50")
frame_apps.pack(pady=5)
tk.Label(frame_apps, text="🔥 แอปลัด (Shortcuts)", font=("Tahoma", 10, "bold"), bg="#2c3e50", fg="#f1c40f").grid(row=0, column=0, columnspan=4, pady=2)

tk.Button(frame_apps, text="HBO", bg="#8e44ad", fg="white", font=("Tahoma", 9, "bold"), width=6, command=lambda: launch_app('com.hbo.asia.androidtv')).grid(row=1, column=0, padx=2)
tk.Button(frame_apps, text="MONO", bg="#d35400", fg="white", font=("Tahoma", 9, "bold"), width=6, command=lambda: launch_app('com.doonung.dtv')).grid(row=1, column=1, padx=2)
tk.Button(frame_apps, text="AIS", bg="#27ae60", fg="white", font=("Tahoma", 9, "bold"), width=6, command=lambda: launch_app('com.ais.mimo.aisplay.tv')).grid(row=1, column=2, padx=2)
tk.Button(frame_apps, text="YouTube", bg="#c0392b", fg="white", font=("Tahoma", 9, "bold"), width=7, command=lambda: launch_app('com.google.android.youtube.tv')).grid(row=1, column=3, padx=2)
tk.Button(frame_apps, text="📺 กลับหน้าดูทีวี (LIVE TV)", bg="#16a085", fg="white", font=("Tahoma", 10, "bold"), command=lambda: run_adb(['shell', 'input', 'keyevent', '170'])).grid(row=2, column=0, columnspan=4, pady=8, sticky="ew")

# Text Input Section

frame_text = tk.Frame(root, bg="#2c3e50")
frame_text.pack(pady=10)
tk.Label(frame_text, text="พิมพ์ข้อความส่งเข้าทีวี:", font=("Tahoma", 10), bg="#2c3e50", fg="white").grid(row=0, column=0, columnspan=2)
text_entry = tk.Entry(frame_text, font=("Tahoma", 12), width=20)
text_entry.grid(row=1, column=0, padx=5, pady=5)
text_entry.bind('<Return>', send_text)
tk.Button(frame_text, text="พิมพ์เฉยๆ", bg="#8e44ad", fg="white", font=("Tahoma", 9, "bold"), command=send_text).grid(row=1, column=1, padx=2, pady=5)
tk.Button(frame_text, text="🔍 ค้นหาใน YT", bg="#c0392b", fg="white", font=("Tahoma", 9, "bold"), command=youtube_search).grid(row=1, column=2, padx=2, pady=5)

# Keys Section
frame_keys = tk.Frame(root, bg="#2c3e50")
frame_keys.pack(pady=10)

btn_style = {"font": ("Tahoma", 12, "bold"), "width": 5, "height": 2, "bg": "#ecf0f1"}

tk.Button(frame_keys, text="PWR", bg="#e74c3c", fg="white", font=("Tahoma", 10, "bold"), width=5, height=2, command=lambda: send_key(26)).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_keys, text="SEARCH", bg="#9b59b6", fg="white", font=("Tahoma", 10, "bold"), width=7, height=2, command=lambda: send_key(84)).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_keys, text="HOME", bg="#3498db", fg="white", font=("Tahoma", 10, "bold"), width=5, height=2, command=lambda: send_key(3)).grid(row=0, column=2, padx=5, pady=5)

tk.Button(frame_keys, text="▲", **btn_style, command=lambda: send_key(19)).grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame_keys, text="◀", **btn_style, command=lambda: send_key(21)).grid(row=2, column=0, padx=5, pady=5)
tk.Button(frame_keys, text="OK", bg="#f1c40f", font=("Tahoma", 12, "bold"), width=5, height=2, command=lambda: send_key(66)).grid(row=2, column=1, padx=5, pady=5)
tk.Button(frame_keys, text="▶", **btn_style, command=lambda: send_key(22)).grid(row=2, column=2, padx=5, pady=5)
tk.Button(frame_keys, text="▼", **btn_style, command=lambda: send_key(20)).grid(row=3, column=1, padx=5, pady=5)

tk.Button(frame_keys, text="BACK", bg="#95a5a6", font=("Tahoma", 10, "bold"), width=5, height=2, command=lambda: send_key(4)).grid(row=4, column=0, padx=5, pady=20)
tk.Button(frame_keys, text="VOL-", bg="#2ecc71", font=("Tahoma", 10, "bold"), width=5, height=2, command=lambda: send_key(25)).grid(row=4, column=1, padx=5, pady=20)
tk.Button(frame_keys, text="VOL+", bg="#2ecc71", font=("Tahoma", 10, "bold"), width=5, height=2, command=lambda: send_key(24)).grid(row=4, column=2, padx=5, pady=20)

# Media Controls
tk.Button(frame_keys, text="⏮ PREV", bg="#34495e", fg="white", font=("Tahoma", 9, "bold"), width=6, height=2, command=lambda: send_key(88)).grid(row=5, column=0, padx=5, pady=5)
tk.Button(frame_keys, text="⏯ PLAY/PAUSE", bg="#f39c12", fg="white", font=("Tahoma", 8, "bold"), width=11, height=2, command=lambda: send_key(85)).grid(row=5, column=1, padx=5, pady=5)
tk.Button(frame_keys, text="NEXT ⏭", bg="#34495e", fg="white", font=("Tahoma", 9, "bold"), width=6, height=2, command=lambda: send_key(87)).grid(row=5, column=2, padx=5, pady=5)

connect_tv()
root.mainloop()
