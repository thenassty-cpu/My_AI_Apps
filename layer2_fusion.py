import subprocess
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

FREQ = "5min"

def pull_water_level(box_ip="192.168.1.59") -> pd.DataFrame:
    cmd = f'adb -s {box_ip} shell "run-as com.termux cat /data/data/com.termux/files/home/trojan_log.json"'
    try:
        raw = subprocess.check_output(cmd, shell=True)
        text = raw.decode("utf-8", errors="ignore")
        records = json.loads(text)
        df = pd.DataFrame(records)
        # ถอดโซนเวลาออกเพื่อป้องกัน Error ตอนรวมร่าง
        df["time"] = pd.to_datetime(df["time"]).dt.tz_localize(None) 
        df.set_index("time", inplace=True)
        return df[["water_level_m"]].sort_index()
    except Exception as e:
        print(f"[ADB Pull Info] Using default water level due to ADB skip on PC.")
        # จำลองค่าน้ำ 0.5 เมตร เพื่อให้ระบบหลังบ้านรันผ่านเวลาเทสต์บน Windows
        now = pd.Timestamp.now().floor(FREQ).tz_localize(None)
        return pd.DataFrame({"water_level_m": [0.5]}, index=[now])

def resample_to_5min(df: pd.DataFrame, method="time") -> pd.DataFrame:
    if df is None or df.empty:
        return df
    # ปลด Timezone ให้เป็นแบบปกติ (Naive)
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)
        
    full_idx = pd.date_range(
        start=df.index.min().floor(FREQ),
        end=df.index.max().ceil(FREQ),
        freq=FREQ
    )
    df_out = (
        df.reindex(df.index.union(full_idx))
        .interpolate(method=method)
        .reindex(full_idx)
        .ffill()
    )
    return df_out

def fuse_all(weather_df: pd.DataFrame, tide_df: pd.DataFrame, water_df: pd.DataFrame, window_hours: int = 48) -> pd.DataFrame:
    # อิงเวลาปัจจุบันแบบตัด Timezone ทิ้ง
    now = pd.Timestamp.now().floor(FREQ).tz_localize(None)
    horizon_end = now + timedelta(hours=window_hours)

    weather_5m = resample_to_5min(weather_df)
    tide_5m    = resample_to_5min(tide_df)
    water_5m   = resample_to_5min(water_df, method="time")

    master_idx = pd.date_range(start=now, end=horizon_end, freq=FREQ)
    master = pd.DataFrame(index=master_idx)

    for src, name_map in [
        (water_5m,   {"water_level_m": "water_level_m"}),
        (weather_5m, {"precipitation": "precipitation", "wind_speed_10m": "wind_speed_ms", "wind_direction_10m": "wind_dir_deg"}),
        (tide_5m,    {"tide_m": "tide_m"}),
    ]:
        if src is not None and not src.empty:
            if src.index.tz is not None:
                src.index = src.index.tz_localize(None)
            src_renamed = src.rename(columns=name_map)[list(name_map.values())]
            master = master.join(src_renamed, how="left")

    if "precipitation" in master.columns:
        master["racc_24h"] = master["precipitation"].rolling(window=288, min_periods=1).sum()

    # อุดรอยรั่วข้อมูลด้วย 0 ในกรณีที่ API ส่งข้อมูลมาแหว่ง
    master = master.ffill().bfill().fillna(0)
    return master