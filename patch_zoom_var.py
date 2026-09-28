file_path = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("self.zoom_var = ctk.IntVar(value=24)", "self.zoom_val = 24")
content = content.replace("self.zoom_var.set(24)", "self.zoom_val = 24")
content = content.replace("self.zoom_var.set(48)", "self.zoom_val = 48")
content = content.replace("self.zoom_var.set(96)", "self.zoom_val = 96")

old_z = '''z = self.zoom_var.get()
            print('ZOOM VAR:', z)
            df = df.tail(z)'''
content = content.replace(old_z, "df = df.tail(self.zoom_val)")

# Also clean up the exception logging to normal 'except: pass' to avoid console issues if run with pythonw
content = content.replace('except Exception as e: print("GRAPH ERROR:", e)', 'except: pass')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
