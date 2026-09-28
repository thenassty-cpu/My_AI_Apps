file_path = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the sync_trojan function block
import re
func_match = re.search(r'def sync_trojan\(\):.*?threading\.Thread\(target=task, daemon=True\)\.start\(\)', content, re.DOTALL)
if func_match:
    func_code = func_match.group(0)
    # Remove it from its current location
    content = content.replace(func_code + '\n\n', '')
    content = content.replace(func_code + '\n', '')
    content = content.replace(func_code, '')
    
    # Find btn_trojan and insert the function right above it
    btn_marker = 'btn_trojan = ctk.CTkButton(frame_footer'
    content = content.replace(btn_marker, func_code + '\n\n' + btn_marker)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Moved sync_trojan successfully.")
