# run_all.py or scheduler.py

import subprocess
import time
from datetime import datetime
import sys
import threading

def run_script(script_name):
    print(f"\n🟡 Running {script_name} @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        subprocess.run([sys.executable, script_name], check=True)
        print(f"✅ Finished {script_name}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}: {e}")

# Delayed execution logic
def delayed_actual(delay_seconds, script_name):
    delay_minutes = delay_seconds / 60
    print(f"⏳ Waiting {delay_minutes:.0f} min before running {script_name}")
    time.sleep(delay_seconds)
    print(f"🟢 Triggering {script_name} @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    run_script(script_name)

# Last execution timestamps
last_run = {
    "5min": None,
    "8h": None,
    "24h": None
}

def should_run(last_time, interval_minutes):
    if last_time is None:
        return True
    elapsed = (datetime.now() - last_time).total_seconds() / 60.0
    return elapsed >= interval_minutes

print("🚀 Scheduler started. Waiting for tasks to trigger...")

while True:
    now = datetime.now()

    # 5-Minute Task Block
    if should_run(last_run["5min"], 5):
        run_script("predict_price.py")
        threading.Thread(target=delayed_actual, args=(310, "log_actual_price.py")).start()  # 5 min + 10 sec buffer
        last_run["5min"] = now

    # 8-Hour Task Block
    if should_run(last_run["8h"], 8 * 60):
        run_script("predict_8h.py")
        threading.Thread(target=delayed_actual, args=(8 * 60 * 60, "actual_8h.py")).start()
        last_run["8h"] = now

    # 24-Hour Task Block
    if should_run(last_run["24h"], 24 * 60):
        run_script("predict_24h.py")
        threading.Thread(target=delayed_actual, args=(24 * 60 * 60, "actual_24h.py")).start()
        last_run["24h"] = now

    time.sleep(60)  # Check every 1 minute
