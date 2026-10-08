@echo off
echo Disabling Flood Center Auto Update task...
schtasks /change /tn "Flood Center Auto Update" /disable
if %errorlevel% equ 0 (
    echo [SUCCESS] Task "Flood Center Auto Update" is now DISABLED!
) else (
    echo [NOTE] Please right click this file and select 'Run as administrator' to disable the scheduled task.
)
pause
