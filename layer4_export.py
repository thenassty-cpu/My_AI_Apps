# layer4_export.py
import os
import json
import pandas as pd
from datetime import datetime

# ─────────────────────────────────────────
# 1. FRONTEND EXPORT (Dashboard JSON)
# ─────────────────────────────────────────
def export_dashboard_data(risk_df: pd.DataFrame, summary: dict, output_path="dashboard_data.json"):
    """แปลงข้อมูลและสรุป Alert เป็น JSON ให้ Frontend ดึงไปแสดงกราฟ 48 ชม."""
    cols_to_export = ["water_level_m", "racc_24h", "tide_m", "delta_h_wind_m", "risk_index", "risk_label"]
    
    df_export = risk_df[cols_to_export].copy()
    df_export.index = df_export.index.astype(str) 
    
    records = df_export.reset_index().rename(columns={"index": "time"}).to_dict(orient="records")

    payload = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "alert_summary": summary,
        "timeline_48h": records
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Exported dashboard data to {output_path}")

# ─────────────────────────────────────────
# 2. LOCAL CSV LOGGER (Calibration Data)
# ─────────────────────────────────────────
def log_to_local_csv(risk_df: pd.DataFrame, csv_path="flood_data_ton.csv"):
    """นำข้อมูลสถานะปัจจุบัน (แถวแรก) ไปต่อท้ายไฟล์ CSV ในเครื่อง"""
    # ดึงเฉพาะข้อมูลแถวปัจจุบันและคอลัมน์ที่ต้องการ
    current_state = risk_df.iloc[[0]].copy()
    cols_to_log = ["water_level_m", "racc_24h", "tide_m", "delta_h_wind_m", "risk_index", "risk_label"]
    current_state = current_state[cols_to_log]
    current_state.index.name = "Time"
    
    # เช็กว่าไฟล์มีอยู่แล้วหรือไม่ เพื่อตัดสินใจว่าจะเขียน Header หรือไม่
    write_header = not os.path.exists(csv_path)
    
    try:
        # บันทึกแบบต่อท้าย (mode='a')
        current_state.to_csv(csv_path, mode='a', header=write_header)
        print(f"[OK] Logged current state to local file: {csv_path}")
    except Exception as e:
        print(f"[WARN] Error saving to CSV: {e}")

# ─────────────────────────────────────────
# 3. PUSH ALERT (Backlog)
# ─────────────────────────────────────────
def send_push_alert(risk_index: float, risk_label: str, message: str):
    """
    # TODO: แจ้งเตือน LINE/Telegram เมื่อ risk_index >= 0.65 (🔴 HIGH)
    """
    pass

# ─────────────────────────────────────────
# RUNNER
# ─────────────────────────────────────────
if __name__ == "__main__":
    # 1. นำเข้าฟังก์ชันจาก Layer 1, 2, 3 ที่เราเตรียมไว้
    from layer1_collection import fetch_weather_data, load_tide_data
    from layer2_fusion import pull_water_level, fuse_all
    from layer3_risk import run_risk_pipeline, generate_alert_summary

    print("=== STARTING FLOOD PIPELINE ===")
    
    # 2. ดึงข้อมูลและรวมร่าง (Layer 1 & 2)
    weather_df = fetch_weather_data()
    tide_df = load_tide_data()
    water_df = pull_water_level()
    fused_df = fuse_all(weather_df, tide_df, water_df, window_hours=48)

    # 3. คำนวณสมการความเสี่ยง (Layer 3)
    risk_df = run_risk_pipeline(fused_df)
    summary = generate_alert_summary(risk_df)

    # 4. ส่งออกข้อมูลให้หน้าจอและบันทึก Log ลงเครื่อง (Layer 4)
    export_dashboard_data(risk_df, summary, output_path="dashboard_data.json")
    log_to_local_csv(risk_df, csv_path="flood_data_ton.csv")
    
    print("=== PIPELINE COMPLETED SUCCESSFULLY ===")