@echo off
echo ==========================================
echo 🌊 รันระบบ Ultimate BKK Flood Center
echo ==========================================

:: รัน Python ดึงข้อมูลและคำนวณ Risk
echo 1. Running Risk Pipeline...
python layer4_export.py

:: ส่งไฟล์ขึ้น GitHub
echo 2. Pushing updates to GitHub...
git add dashboard_data.json flood_history_master.json *.csv
git commit -m "🤖 อัปเดตข้อมูลน้ำท่วมจากเครื่อง Local"
git push origin main

echo ==========================================
echo ✅ อัปเดตเสร็จสมบูรณ์!
echo ==========================================
timeout /t 5