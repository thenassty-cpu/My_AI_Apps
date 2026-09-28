import urllib.request
import re
import time
import json
import os
import datetime

LOG_FILE = "trojan_log.json"
CODES = ["WL.PSC.05", "WL.PSC.02", "WL.PSC.01", "WL.SST.01", "WL.KHW.01", "WL.KSG.01", "WL.SWA.01", "WL.SSB.09", "WL.PSR.01"]

print("🐎 3BB Trojan Scraper is running...")
print("Press Ctrl+C to stop.")

def scrape_and_save():
    try:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Fetching BMA...")
        req = urllib.request.Request('https://weather.bangkok.go.th/water/', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/115.0.0.0'})
        html = urllib.request.urlopen(req, timeout=15).read().decode('utf-8')
        
        pattern = r"(WL\.PSC\.\d{2}|WL\.SST\.01|WL\.KHW\.01|WL\.KSG\.01|WL\.SWA\.01|WL\.SSB\.09|WL\.PSR\.01)\s*:\s*.*?'([-\d\.]+)'.*?'([-\d\.]+)'.*?'(\d{2}/\d{2}/\d{4} \d{2}:\d{2})'.*?(bg-success|bg-warning|bg-danger)"
        matches = re.finditer(pattern, html)
        
        current_data = {}
        bma_time = ""
        for m in matches:
            code, lvl_in, lvl_out, timestamp, status = m.groups()
            current_data[code] = {"in": lvl_in, "out": lvl_out, "status": status}
            if code == "WL.PSC.01": bma_time = timestamp
            
        if not bma_time:
            return
            
        # Load existing log
        history = []
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, 'r') as f:
                    history = json.load(f)
            except:
                pass
                
        # Check if BMA time is already logged to avoid duplicates
        if history and history[-1].get("bma_time") == bma_time:
            print(f" -> No new data (BMA Time: {bma_time})")
            return
            
        # Append new record
        record = {
            "fetch_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "bma_time": bma_time,
            "data": current_data
        }
        history.append(record)
        
        # Keep only last 100 records to save space
        if len(history) > 100:
            history = history[-100:]
            
        with open(LOG_FILE, 'w') as f:
            json.dump(history, f)
            
        print(f" -> Saved new record for {bma_time} (Total: {len(history)} records)")
        
    except Exception as e:
        print(f" -> Error: {e}")

while True:
    scrape_and_save()
    time.sleep(30 * 60) # Sleep 30 minutes
