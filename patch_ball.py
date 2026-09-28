file_path = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('(13.840, 100.700)', '(13.862383, 100.695103)')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
