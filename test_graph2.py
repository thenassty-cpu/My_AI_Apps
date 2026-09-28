import pandas as pd
csv_file = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\flood_data_ton.csv'
df = pd.read_csv(csv_file)
df['time'] = pd.to_datetime(df['time'], format='mixed')
df = df.tail(24)
print("SUCCESS!")
