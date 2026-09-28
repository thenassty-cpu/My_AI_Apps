import re

file_path = r'C:\Users\ITss-Advice\Desktop\My_AI_Apps\Ultimate_BKK_Flood_Center.pyw'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_code = '''                w_data = json.loads(res_w.read().decode('utf-8'))
                curr = datetime.datetime.now().hour
                t.lbl_rain_val.configure(text=f"{max(w_data['hourly']['precipitation_probability'][curr:curr+24])}%")
                t.lbl_rain_trend.configure(text=f"สะสม: {sum(w_data['hourly']['precipitation'][curr:curr+24]):.1f} mm")'''

new_code = '''                w_data = json.loads(res_w.read().decode('utf-8'))
                curr = datetime.datetime.now().hour
                
                probs = w_data['hourly']['precipitation_probability'][curr:curr+24]
                precs = w_data['hourly']['precipitation'][curr:curr+24]
                times = w_data['hourly']['time'][curr:curr+24]
                
                max_prob = max(probs)
                total_prec = sum(precs)
                t.lbl_rain_val.configure(text=f"{max_prob}%")
                
                if total_prec > 0.1:
                    max_idx = precs.index(max(precs))
                    peak_time = times[max_idx][-5:] # Gets 'HH:MM'
                    t.lbl_rain_trend.configure(text=f"สะสม: {total_prec:.1f} mm | หนักสุด: {peak_time} น.")
                else:
                    t.lbl_rain_trend.configure(text=f"สะสม: {total_prec:.1f} mm | ไม่มีแนวโน้มฝน")'''

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched Rain!")
else:
    print("Code not found")
