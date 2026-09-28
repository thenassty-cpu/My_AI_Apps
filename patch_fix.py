import os

file_path = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_cmd = "ps_cmd = f\"Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; \ = [System.Drawing.Image]::FromFile('{filepath}'); [System.Windows.Forms.Clipboard]::SetImage(\)\""
new_cmd = "ps_cmd = f\"Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; $img = [System.Drawing.Image]::FromFile('{filepath}'); [System.Windows.Forms.Clipboard]::SetImage($img)\""

content = content.replace(old_cmd, new_cmd)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed ps_cmd!")
