file_path = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("except: pass", "except Exception as e: print('RAIN ERROR:', e)")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
