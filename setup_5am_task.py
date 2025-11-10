"""
Setup 5 AM Scheduled Task for BeyondTrust Daily Reports
Runs Monday through Friday at 5:00 AM
"""
import subprocess
import sys
from pathlib import Path

def create_scheduled_task():
    """Create Windows scheduled task for Monday-Friday at 5 AM"""

    script_path = Path(__file__).parent / "daily_report_automation.py"

    # Task command
    task_name = "BeyondTrustDailyReport5AM"
    python_exe = sys.executable
    task_action = f'{python_exe} "{script_path}"'

    # Create the task
    cmd = [
        "schtasks", "/Create",
        "/TN", task_name,
        "/TR", task_action,
        "/SC", "WEEKLY",
        "/D", "MON,TUE,WED,THU,FRI",
        "/ST", "05:00",
        "/RL", "HIGHEST",
        "/F"  # Force overwrite if exists
    ]

    print("=" * 60)
    print("BeyondTrust 5 AM Daily Report Setup (Mon-Fri)")
    print("=" * 60)
    print()
    print(f"Task Name: {task_name}")
    print(f"Schedule: Monday-Friday at 5:00 AM")
    print(f"Script: {script_path}")
    print(f"Python: {python_exe}")
    print()
    print("Creating scheduled task...")
    print()

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("=" * 60)
            print("[SUCCESS] Scheduled task created successfully!")
            print("=" * 60)
            print()
            print("Starting next weekday at 5:00 AM (Mon-Fri), you will get:")
            print("  - Automatic download from BeyondTrust")
            print("  - Automatic HTML report generation")
            print("  - Desktop notification when ready")
            print("  - ZERO interaction needed!")
            print()
            print("The report will be in your Downloads folder:")
            print("  Daily-Support-Performance-Report-[DATE].html")
            print()
            print("=" * 60)
            print("Task Management Commands:")
            print("=" * 60)
            print()
            print("Run now to test:")
            print(f"  schtasks /Run /TN {task_name}")
            print()
            print("View in Task Scheduler:")
            print("  - Open 'Task Scheduler'")
            print(f"  - Look for: {task_name}")
            print()
            print("Disable temporarily:")
            print(f"  schtasks /Change /TN {task_name} /DISABLE")
            print()
            print("Enable again:")
            print(f"  schtasks /Change /TN {task_name} /ENABLE")
            print()
            print("Delete task:")
            print(f"  schtasks /Delete /TN {task_name} /F")
            print()
            return True
        else:
            print("=" * 60)
            print("[ERROR] Failed to create scheduled task")
            print("=" * 60)
            print()
            print("Error output:")
            print(result.stderr)
            print()
            print("You may need Administrator privileges.")
            print("Try running this script as administrator.")
            return False

    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")
        return False

if __name__ == "__main__":
    success = create_scheduled_task()
    sys.exit(0 if success else 1)
