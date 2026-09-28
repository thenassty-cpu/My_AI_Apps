file_path = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

insert_code = '''    if not ip: return
    root.clipboard_clear()
    root.clipboard_append(ip)
    root.update()'''

content = content.replace('    if not ip: return', insert_code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Clipboard feature added!")
