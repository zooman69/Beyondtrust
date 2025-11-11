"""
Windows Task Scheduler Setup for BeyondTrust Report Watcher
===========================================================
This script sets up a Windows scheduled task to run the folder watcher
automatically at system startup or on a schedule.

Usage:
    python setup_scheduler.py [startup|scheduled|remove]

Options:
    startup   - Run watcher at system startup (recommended)
    scheduled - Run at specific time daily
    remove    - Remove the scheduled task
"""

import sys
import subprocess
from pathlib import Path
import os


def create_startup_task():
    """Create a task that runs at system startup"""
    script_dir = Path(__file__).parent
    python_exe = sys.executable
    watcher_script = script_dir / "enhanced_watch_folder.py"

    task_name = "BeyondTrustReportWatcher"

    # XML for task scheduler
    task_xml = f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Automatically processes BeyondTrust support session reports</Description>
    <Author>{os.getenv('USERNAME')}</Author>
  </RegistrationInfo>
  <Triggers>
    <BootTrigger>
      <Enabled>true</Enabled>
    </BootTrigger>
  </Triggers>
  <Principals>
    <Principal>
      <UserId>{os.getenv('USERDOMAIN')}\\{os.getenv('USERNAME')}</UserId>
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{python_exe}</Command>
      <Arguments>"{watcher_script}"</Arguments>
      <WorkingDirectory>{script_dir}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>'''

    # Save XML to temp file
    temp_xml = script_dir / "temp_task.xml"
    with open(temp_xml, 'w', encoding='utf-16') as f:
        f.write(task_xml)

    try:
        # Create the task
        print(f"Creating scheduled task: {task_name}")
        print(f"Python: {python_exe}")
        print(f"Script: {watcher_script}")
        print()

        result = subprocess.run(
            ['schtasks', '/Create', '/TN', task_name, '/XML', str(temp_xml), '/F'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("[SUCCESS] Scheduled task created!")
            print(f"\nThe report watcher will now start automatically when Windows boots.")
            print(f"\nTo manage the task:")
            print(f"  - View: Task Scheduler > Task Scheduler Library > {task_name}")
            print(f"  - Start now: schtasks /Run /TN {task_name}")
            print(f"  - Stop: schtasks /End /TN {task_name}")
            print(f"  - Remove: python setup_scheduler.py remove")
            return True
        else:
            print(f"[ERROR] Failed to create task: {result.stderr}")
            return False

    finally:
        # Clean up temp file
        if temp_xml.exists():
            temp_xml.unlink()


def create_scheduled_task(time="09:00"):
    """Create a task that runs at a specific time daily"""
    script_dir = Path(__file__).parent
    python_exe = sys.executable
    watcher_script = script_dir / "enhanced_watch_folder.py"

    task_name = "BeyondTrustReportWatcher"

    try:
        # Create the task
        print(f"Creating scheduled task: {task_name}")
        print(f"Schedule: Daily at {time}")
        print(f"Python: {python_exe}")
        print(f"Script: {watcher_script}")
        print()

        result = subprocess.run([
            'schtasks', '/Create',
            '/TN', task_name,
            '/TR', f'"{python_exe}" "{watcher_script}"',
            '/SC', 'DAILY',
            '/ST', time,
            '/F'
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("[SUCCESS] Scheduled task created!")
            print(f"\nThe report watcher will run daily at {time}.")
            print(f"\nTo manage the task:")
            print(f"  - Start now: schtasks /Run /TN {task_name}")
            print(f"  - Stop: schtasks /End /TN {task_name}")
            print(f"  - Remove: python setup_scheduler.py remove")
            return True
        else:
            print(f"[ERROR] Failed to create task: {result.stderr}")
            return False

    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def remove_task():
    """Remove the scheduled task"""
    task_name = "BeyondTrustReportWatcher"

    try:
        result = subprocess.run(
            ['schtasks', '/Delete', '/TN', task_name, '/F'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"[SUCCESS] Scheduled task '{task_name}' removed.")
            return True
        else:
            print(f"[ERROR] Failed to remove task: {result.stderr}")
            return False

    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def main():
    print("=" * 60)
    print("BeyondTrust Report Watcher - Scheduler Setup")
    print("=" * 60)
    print()

    if len(sys.argv) < 2:
        print("Usage: python setup_scheduler.py [startup|scheduled|remove]")
        print()
        print("Options:")
        print("  startup   - Run watcher at system startup (recommended)")
        print("  scheduled - Run at specific time daily")
        print("  remove    - Remove the scheduled task")
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == "startup":
        create_startup_task()
    elif mode == "scheduled":
        time = input("Enter time to run daily (HH:MM, default 09:00): ").strip()
        if not time:
            time = "09:00"
        create_scheduled_task(time)
    elif mode == "remove":
        remove_task()
    else:
        print(f"[ERROR] Invalid option: {mode}")
        print("Use: startup, scheduled, or remove")
        sys.exit(1)


if __name__ == "__main__":
    main()
