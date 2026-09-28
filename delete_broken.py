file_path = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# The bad line starts with '( 192.168.1.xxx)' or something like it.
new_lines = []
for line in lines:
    if '192.168.1.xxx)", title="' in line and 'dialog =' not in line:
        continue # skip this broken line
    new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Deleted broken line")
