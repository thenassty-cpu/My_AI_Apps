import os
import re

file_path = r'C:\Users\ITss-Advice\Documents\GitHub\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the dialog input lines with a hardcoded IP
pattern = r'dialog = ctk\.CTkInputDialog[^)]+\)\s*ip = dialog\.get_input\(\)\s*if not ip: return'
replacement = 'ip = "192.168.1.59"\n    if not ip: return'

new_content = re.sub(pattern, replacement, content)

if new_content != content:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Patched using Regex!")
else:
    print("Regex not matched!")
