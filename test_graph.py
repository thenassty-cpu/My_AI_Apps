import pandas as pd
csv_file = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\flood_data_ton.csv'
df = pd.read_csv(csv_file)
df['time'] = pd.to_datetime(df['time'])
df = df.tail(24)
print("DF tail:")
print(df)
max_val = df['home'].max()
current_val = df['home'].iloc[-1]
diff_cm = (max_val - current_val) * 100
