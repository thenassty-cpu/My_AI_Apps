import pandas as pd
file_path = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\flood_data_por.csv'
df = pd.read_csv(file_path)
df = df[df['home'] != 1.25]
df.to_csv(file_path, index=False)
print("Scrubbed!")
