import re

file_path = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace constant tuples with CTkFont
font_replacements = [
    ('FONT_TITLE = ("Kanit", 18, "bold")', 'FONT_TITLE = ctk.CTkFont(family="Kanit", size=18, weight="bold")'),
    ('FONT_BIG = ("Kanit", 52, "bold")', 'FONT_BIG = ctk.CTkFont(family="Kanit", size=52, weight="bold")'),
    ('FONT_MED = ("Kanit", 36, "bold")', 'FONT_MED = ctk.CTkFont(family="Kanit", size=36, weight="bold")'),
    ('FONT_SUB = ("Kanit", 15)', 'FONT_SUB = ctk.CTkFont(family="Kanit", size=15)'),
    ('FONT_TREND = ("Kanit", 16)', 'FONT_TREND = ctk.CTkFont(family="Kanit", size=16)'),
    ('FONT_BTN = ("Kanit", 16, "bold")', 'FONT_BTN = ctk.CTkFont(family="Kanit", size=16, weight="bold")'),
]
for old, new in font_replacements:
    content = content.replace(old, new)

# 2. Add extra font objects for hardcoded ones
content = content.replace('CARD_BG = "#22272e"', 'CARD_BG = "#22272e"\nFONT_PEAK = ctk.CTkFont(family="Kanit", size=14)\nFONT_TIDE = ctk.CTkFont(family="Kanit", size=15, weight="bold")')

# 3. Replace hardcoded fonts with the new objects
content = content.replace('font=("Kanit", 14)', 'font=FONT_PEAK')
content = content.replace('font=("Kanit", 15, "bold")', 'font=FONT_TIDE')
content = content.replace('font=("Kanit", 16, "bold")', 'font=FONT_BTN')

# 4. Add the toggle function and button
toggle_code = '''
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
    for t in [tab_ton, tab_dong, tab_ball]:
        t.update_graph()
        
    btn_font.configure(text=f"🔠 สลับฟอนต์ (ปัจจุบัน: {current_font})")

btn_font = ctk.CTkButton(frame_footer, text="🔠 สลับฟอนต์ (ปัจจุบัน: Kanit)", font=FONT_BTN, command=toggle_font, width=220, height=35, fg_color="#8e44ad", hover_color="#9b59b6")
btn_font.pack(side="left", padx=10)
'''

# Insert toggle_code before btn_refresh
content = content.replace('btn_refresh = ctk.CTkButton(frame_footer', toggle_code + '\nbtn_refresh = ctk.CTkButton(frame_footer')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched successfully!")
