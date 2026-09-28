import urllib.request, json, datetime
url_w = 'https://api.open-meteo.com/v1/forecast?latitude=13.722&longitude=100.435&hourly=precipitation_probability,precipitation&forecast_days=2&timezone=Asia%2FBangkok'
res_w = urllib.request.urlopen(url_w, timeout=10)
w_data = json.loads(res_w.read().decode('utf-8'))
curr = datetime.datetime.now().hour
precs = w_data['hourly']['precipitation'][curr:curr+24]
times = w_data['hourly']['time'][curr:curr+24]
for t, p in zip(times, precs):
    print(f"{t}: {p}")
