import base64
file_path = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_text = base64.b64decode('ZGlhbG9nID0gY3RrLkNUa0lucHV0RGlhbG9nKHRleHQ9IuC4geC4o+C4reC4gSBJUCDguILguK3guIcgQW5kcm9pZCBCb3ggKFRlcm11eCk6XG4o4LmA4LiK4LmI4LiZIDE5Mi4xNjguMS54eHgpIiwgdGl0bGU9IuC4lOC4tuC4hyBMb2cg4Lih4LmJ4Liy4LmC4LiX4Lij4LiI4Lix4LiZIiwgZm9udD0oIlRhaG9tYSIsIDE2KSkK').decode('utf-8')

for i in range(len(lines)):
    if 'dialog = ctk.CTkInputDialog' in lines[i]:
        # If it spans two lines, replace this line and clear the next
        if '(' in lines[i] and ')' not in lines[i]:
            lines[i] = '    ' + new_text
            lines[i+1] = ''
        else:
            lines[i] = '    ' + new_text
        break

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Replaced with base64 decoded string successfully")
