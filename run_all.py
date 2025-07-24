import subprocess
import time
from datetime import datetime
import sys
import threading
import logging
import os

# === Setup Logging ===
log_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(log_dir, "scheduler.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def log_and_print(message, level="info"):
    print(message)
    if level == "info":
        logging.info(message)
    elif level == "error":
        logging.error(message)

def run_script(script_name):
    log_and_print(f"🟡 Running {script_name} @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        subprocess.run([sys.executable, script_name], check=True)
        log_and_print(f"✅ Finished {script_name}")
    except subprocess.CalledProcessError as e:
        log_and_print(f"❌ Error running {script_name}: {e}", level="error")

# Delayed execution logic
def delayed_actual(delay_seconds, script_name):
    delay_minutes = delay_seconds / 60
    log_and_print(f"⏳ Waiting {delay_minutes:.0f} min before running {script_name}")
    time.sleep(delay_seconds)
    log_and_print(f"🟢 Triggering {script_name} @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    run_script(script_name)

# Last execution timestamps
last_run = {
    "8h": None,
    "24h": None
}

def should_run(last_time, interval_minutes):
    if last_time is None:
        return True
    elapsed = (datetime.now() - last_time).total_seconds() / 60.0
    return elapsed >= interval_minutes

log_and_print("🚀 Scheduler started. Waiting for tasks to trigger...")

while True:
    now = datetime.now()

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

    time.sleep(60)
