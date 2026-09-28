file_path = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add tab for Por
old_tabs_init = '''tab_ball = DashboardTab(t3, "🏡 พระยาสุเรนทร์ (บ้านคุณบอล)", "ต้นน้ำ (พระยาสุเรนทร์)", "ปลายทางระบายน้ำ (แสนแสบ)", "📈 กราฟความเสี่ยงน้ำท่วม (ตะวันออก)", "C:/Users/ITss-Advice/Desktop/My_AI_Apps/flood_data_ball.csv", (13.862383, 100.695103), "WL.SWA.01", "WL.PSR.01", "WL.SSB.09")'''

new_tabs_init = old_tabs_init + '''
tabview.add("🏡 สายไหม 85 (ปอกะดั่น)")
t4 = tabview.tab("🏡 สายไหม 85 (ปอกะดั่น)")
tab_por = DashboardTab(t4, "🏡 สายไหม 85 (บ้านปอกะดั่น)", "ต้นน้ำ (หกวา)", "ปลายทาง (พระยาสุเรนทร์)", "📈 กราฟความเสี่ยงน้ำท่วม (สายไหม)", "C:/Users/ITss-Advice/Desktop/My_AI_Apps/flood_data_por.csv", (13.927, 100.688), "WL.KHW.01", "WL.SST.01", "WL.PSR.01")
'''

content = content.replace(old_tabs_init, new_tabs_init)

# 2. Update all loops [tab_ton, tab_dong, tab_ball] -> [tab_ton, tab_dong, tab_ball, tab_por]
content = content.replace("[tab_ton, tab_dong, tab_ball]", "[tab_ton, tab_dong, tab_ball, tab_por]")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added Por Tab!")
