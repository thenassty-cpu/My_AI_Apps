import re

file_path = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace graph header
old_graph_header = '''        # Graph
        lbl_graph_title = ctk.CTkLabel(self.frame_right, text=title_graph, font=FONT_TITLE, text_color="white")
        lbl_graph_title.pack(pady=10)
        self.fig = Figure(figsize=(4, 4), dpi=100, facecolor=CARD_BG)'''

new_graph_header = '''        # Graph
        frame_gh = ctk.CTkFrame(self.frame_right, fg_color="transparent")
        frame_gh.pack(fill="x", padx=10, pady=10)
        lbl_graph_title = ctk.CTkLabel(frame_gh, text=title_graph, font=FONT_TITLE, text_color="white")
        lbl_graph_title.pack(side="left")
        
        self.zoom_var = ctk.IntVar(value=24)
        
        def on_zoom_change(choice):
            if choice == "12 ชม.": self.zoom_var.set(24)
            elif choice == "24 ชม.": self.zoom_var.set(48)
            elif choice == "48 ชม.": self.zoom_var.set(96)
            self.update_graph()
            
        self.seg_zoom = ctk.CTkSegmentedButton(frame_gh, values=["12 ชม.", "24 ชม.", "48 ชม."], font=FONT_BTN, command=on_zoom_change)
        self.seg_zoom.set("12 ชม.")
        self.seg_zoom.pack(side="right")
        
        self.fig = Figure(figsize=(4, 4), dpi=100, facecolor=CARD_BG)'''

content = content.replace(old_graph_header, new_graph_header)

# Replace df.tail(24)
content = content.replace('df = df.tail(24)', 'df = df.tail(self.zoom_var.get())')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch successful!")
