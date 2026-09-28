import urllib.request, json, datetime
for coords in [(13.722, 100.435), (13.9569, 100.6520), (13.862383, 100.695103)]:
    url_w = f'https://api.open-meteo.com/v1/forecast?latitude={coords[0]}&longitude={coords[1]}&hourly=precipitation_probability,precipitation&forecast_days=2&timezone=Asia%2FBangkok'
    res_w = urllib.request.urlopen(url_w, timeout=10)
    w_data = json.loads(res_w.read().decode('utf-8'))
    curr = datetime.datetime.now().hour
    probs = w_data['hourly']['precipitation_probability'][curr:curr+24]
    precs = w_data['hourly']['precipitation'][curr:curr+24]
    times = w_data['hourly']['time'][curr:curr+24]
    
    # Check for None
    print(f"Coords {coords}: None in precs? {None in precs}")
    max_prob = max(probs)
    total_prec = sum(precs)
    print("Max prob:", max_prob)
    print("Total prec:", total_prec)
