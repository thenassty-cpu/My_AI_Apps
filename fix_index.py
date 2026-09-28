file_path = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line 273 is index 272
# Line 274 is index 273
fixed_text = '    dialog = ctk.CTkInputDialog(text="กรอก IP ของ Android Box (Termux):\\n(เช่น 192.168.1.xxx)", title="ดึง Log ม้าโทรจัน", font=("Tahoma", 16))\n'

# We know the bug is at these lines. We can replace them.
# But just to be sure, let's find 'dialog = ctk.CTkInputDialog'
for i, line in enumerate(lines):
    if 'dialog = ctk.CTkInputDialog' in line:
        if '(' in line and ')' not in line:
            lines[i] = fixed_text
            lines[i+1] = '' # Clear the broken continuation line
        else:
            lines[i] = fixed_text
        break

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Line replaced by index successfully!")
