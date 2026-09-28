file_path = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("df['time'] = pd.to_datetime(df['time'])", "df['time'] = pd.to_datetime(df['time'], format='mixed')")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Patched successfully!')
