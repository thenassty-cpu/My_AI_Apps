import json
import pandas as pd
import os

with open('trojan_log.json', 'r', encoding='utf-8') as f:
    history = json.load(f)

print('Loaded history, len:', len(history))

df = pd.read_csv('flood_data_ton.csv')
print('Read df, len:', len(df))
print(df.columns)
