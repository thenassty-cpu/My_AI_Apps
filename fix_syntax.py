file_path = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the broken string literal with a valid one
import re
# We look for the broken dialog line
broken_part = r'dialog = ctk.CTkInputDialog\(text=".*?\n.*?", title=".*?", font=\("Tahoma", 16\)\)'
fixed_text = 'dialog = ctk.CTkInputDialog(text="กรอก IP ของ Android Box (Termux):\\n(เช่น 192.168.1.xxx)", title="ดึง Log ม้าโทรจัน", font=("Tahoma", 16))'

content = re.sub(broken_part, fixed_text, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Syntax fixed!")
