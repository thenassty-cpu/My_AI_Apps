import re
file_path = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'dialog = ctk\.CTkInputDialog\(text="[^"]+", title="[^"]+"\)', 
                 'dialog = ctk.CTkInputDialog(text="กรอก IP ของ Android Box (Termux):\\n(เช่น 192.168.1.xxx)", title="ดึง Log ม้าโทรจัน", font=("Tahoma", 16))', 
                 content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed encoding!")
