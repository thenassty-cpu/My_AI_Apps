import numpy as np
import pandas as pd

CANAL_OUTLET_DEG = 180
THRESHOLDS = {
    "racc_24h"     : (0.0,  80.0),
    "delta_h_wind" : (-0.10, 0.20),
    "tide_m"       : (0.40,  2.00),
    "water_level_m": (0.20,  1.80),
}
WEIGHTS = {
    "racc_24h"     : 0.35,
    "delta_h_wind" : 0.25,
    "tide_m"       : 0.25,
    "water_level_m": 0.15,
}
RISK_LABELS = [
    (0.65, "🔴 HIGH",   "ระดับอันตราย — เตรียมรับมือน้ำท่วม"),
    (0.35, "🟡 MEDIUM", "ระดับเฝ้าระวัง — ติดตามทุก 30 นาที"),
    (0.00, "🟢 LOW",    "ปกติ"),
]

def _normalize(val: float, lo: float, hi: float) -> float:
    return max(0.0, min(1.0, (val - lo) / (hi - lo)))

def calc_wind_influence(wind_speed_ms: float, wind_dir_deg: float) -> float:
    Cd    = 0.02
    g     = 9.81
    D     = 1.50
    theta = np.radians(wind_dir_deg - CANAL_OUTLET_DEG)
    return Cd * (wind_speed_ms ** 2) * np.cos(theta) / (g * D)

def _get_label(index: float) -> tuple[str, str]:
    for threshold, label, desc in RISK_LABELS:
        if index >= threshold:
            return label, desc
    return RISK_LABELS[-1][1], RISK_LABELS[-1][2]

def score_risk_row(row: pd.Series) -> dict:
    dh_wind = calc_wind_influence(row.get("wind_speed_ms", 0), row.get("wind_dir_deg",  180))
    components = {
        "racc_24h"     : row.get("racc_24h",      0.0),
        "delta_h_wind" : dh_wind,
        "tide_m"       : row.get("tide_m",        1.05),
        "water_level_m": row.get("water_level_m",  0.5),
    }
    norm_scores = {k: _normalize(v, *THRESHOLDS[k]) for k, v in components.items()}
    risk_index = sum(WEIGHTS[k] * norm_scores[k] for k in WEIGHTS)
    label, desc = _get_label(risk_index)
    
    out_dict = {
        "risk_index"       : round(risk_index, 4),
        "risk_label"       : label,
        "risk_desc"        : desc,
        "delta_h_wind_m"   : round(dh_wind, 4)
    }
    for k, v in norm_scores.items():
        out_dict[f"norm_{k}"] = round(v, 3)
    return out_dict

def run_risk_pipeline(fused_df: pd.DataFrame) -> pd.DataFrame:
    if fused_df is None or fused_df.empty:
        raise ValueError("Fused DataFrame ว่างเปล่า — ตรวจสอบ Layer 2")
    results = fused_df.apply(score_risk_row, axis=1, result_type="expand")
    out = pd.concat([fused_df, results], axis=1)
    return out

def generate_alert_summary(risk_df: pd.DataFrame) -> dict:
    windows = {"12h": 144, "24h": 288, "48h": 576}
    summary = {}
    for label, periods in windows.items():
        window = risk_df.iloc[:periods]
        peak   = window["risk_index"].max()
        peak_t = window["risk_index"].idxmax()
        rl, rd = _get_label(peak)
        summary[label] = {
            "peak_index" : round(peak, 4),
            "peak_time"  : peak_t.strftime("%d/%m %H:%M"),
            "label"      : rl,
            "desc"       : rd,
        }
    return summary