import json
import pandas as pd
import os
import subprocess
import traceback

try:
    ip = "192.168.1.59"
    adb = r"C:\Users\ITss-Advice\adb_tools\platform-tools\adb.exe"
    
    subprocess.run([adb, "connect", ip], capture_output=True)
    
    cmd = f'"{adb}" -s {ip} shell "run-as com.termux cat /data/data/com.termux/files/home/trojan_log.json" > trojan_log.json'
    pull_result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if "error" in pull_result.stderr.lower() or "is not debuggable" in pull_result.stderr.lower():
        raise Exception(f"ADB Pull Error: {pull_result.stderr}")
        
    if not os.path.exists("trojan_log.json"):
        raise Exception("Cannot find pulled trojan_log.json")
        
    try:
        with open("trojan_log.json", "r", encoding="utf-16") as f:
            history = json.load(f)
    except Exception as e:
        print("UTF-16 failed:", e)
        with open("trojan_log.json", "r", encoding="utf-8") as f:
            history = json.load(f)
            
    print("Parsed JSON successfully, len:", len(history))
except Exception as e:
    print("SYNC ERROR:", e)
    traceback.print_exc()
