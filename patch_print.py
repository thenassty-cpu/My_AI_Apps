file_path = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("df = df.tail(self.zoom_var.get())", "z = self.zoom_var.get()\n            print('ZOOM VAR:', z)\n            df = df.tail(z)")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
