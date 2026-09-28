import json
import numpy as np
import pandas as pd

def generate_tide_2026(output_path="tide_2026.json", interval_min=30):
    # สร้างช่วงเวลาตลอดปี 2026
    idx = pd.date_range(
        start="2026-01-01 00:00",
        end="2026-12-31 23:30",
        freq=f"{interval_min}min",
        tz="Asia/Bangkok"
    )
    t_h = np.arange(len(idx)) * (interval_min / 60)
    
    # โมเดลจำลองน้ำขึ้นน้ำลงอ่าวไทย (Mixed Semi-diurnal)
    M2 = 0.65 * np.sin(2 * np.pi * t_h / 12.42 + np.radians(30))
    S2 = 0.25 * np.sin(2 * np.pi * t_h / 12.00 + np.radians(60))
    K1 = 0.35 * np.sin(2 * np.pi * t_h / 23.93 + np.radians(120))
    O1 = 0.20 * np.sin(2 * np.pi * t_h / 25.82 + np.radians(200))
    MSf = 0.15 * np.sin(2 * np.pi * t_h / 354.37)
    
    # ฐานน้ำทะเลปานกลาง (MSL) ประมาณ 1.05m
    tide = 1.05 + M2 + S2 + K1 + O1 + MSf
    
    # จัดโครงสร้างเป็น JSON
    records = []
    for ts, val in zip(idx, tide):
        records.append({
            "time": ts.isoformat(),
            "tide_m": round(float(val), 3)
        })
        
    # เขียนลงไฟล์
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
        
    print(f"✓ Created {output_path} successfully! ({len(records):,} records)")

if __name__ == "__main__":
    generate_tide_2026()