import os
import sys
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

# Safe encoding on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from config import BASE_DIR
from daily_styles import get_today_style, DAILY_SLOTS
from main import run_single_pipeline

STATE_FILE = BASE_DIR / "scheduler_state.json"
LOG_FILE = Path(r"C:\Users\manik\Desktop\AUTO\autopilot_log.txt")

def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_msg = f"[{timestamp}] {msg}"
    print(full_msg)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(full_msg + "\n")
    except Exception:
        pass


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"history": {}, "total_published": 0}

def save_state(state: dict):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def get_today_key() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def init_today_state(state: dict) -> dict:
    today_key = get_today_key()
    today_style = get_today_style()
    
    if today_key not in state["history"]:
        state["history"][today_key] = {
            "day_name": today_style["day_name"],
            "theme_title": today_style["theme_title"],
            "style_tag": today_style["style_tag"],
            "slots": {}
        }
        for slot in DAILY_SLOTS:
            state["history"][today_key]["slots"][slot["slot_id"]] = {
                "name": slot["name"],
                "target_time": slot["target_time"],
                "niche": slot["niche_bias"],
                "done": False,
                "completed_at": None,
                "video_file": None
            }
        save_state(state)
    return state

def time_to_minutes(time_str: str) -> int:
    h, m = map(int, time_str.split(":"))
    return h * 60 + m

def check_and_execute_slots():
    """
    Checks today's slots against the current time.
    If laptop was powered off or asleep, executes missed slots automatically!
    """
    state = load_state()
    state = init_today_state(state)
    today_key = get_today_key()
    today_data = state["history"][today_key]
    today_style = get_today_style()
    
    now = datetime.now()
    now_minutes = now.hour * 60 + now.minute
    
    print("=" * 68)
    print(f"   AUTOPILOT SCHEDULER: {today_style['day_name'].upper()} {today_style['emoji']} | {now.strftime('%H:%M:%S')}")
    print(f"   Theme: {today_style['theme_title']}")
    print("=" * 68)
    
    executed_any = False
    
    for slot in DAILY_SLOTS:
        s_id = slot["slot_id"]
        slot_data = today_data["slots"].get(s_id, {})
        target_min = time_to_minutes(slot["target_time"])
        
        # Check if slot time has arrived or passed and is not yet completed
        if now_minutes >= target_min and not slot_data.get("done", False):
            log(f"TRIGGERING DUE SLOT: {slot['name']} (Scheduled for {slot['target_time']})")
            if now_minutes > target_min + 15:
                log(f"[RECOVERY] Laptop was off/asleep during {slot['target_time']}. Running catch-up post now!")
                
            try:
                # Produce video with today's dynamic style parameters
                video_path = run_single_pipeline(
                    preferred_niche=slot["niche_bias"],
                    voice=today_style["voice"],
                    highlight_color=today_style["subtitle_color"],
                    custom_marketing_hook=today_style["marketing_hook"]
                )
                
                # Mark as completed
                slot_data["done"] = True
                slot_data["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                slot_data["video_file"] = video_path.name
                state["total_published"] = state.get("total_published", 0) + 1
                save_state(state)
                executed_any = True
                
                log(f"[OK] Slot '{s_id}' completed and broadcasted successfully to Facebook & Instagram: {video_path.name}")
                time.sleep(3)
            except Exception as e:
                log(f"[ERROR] Failed executing slot '{s_id}': {e}")
                
    if not executed_any:
        print("[i] All past slots are up-to-date. Waiting for the next scheduled time.")
        
    print_status(today_data, today_style, now_minutes)

def force_run_next():
    """Forces execution of the next uncompleted slot right now."""
    state = load_state()
    state = init_today_state(state)
    today_key = get_today_key()
    today_data = state["history"][today_key]
    today_style = get_today_style()
    
    for slot in DAILY_SLOTS:
        s_id = slot["slot_id"]
        slot_data = today_data["slots"].get(s_id, {})
        if not slot_data.get("done", False):
            print(f"\n[+] Force-executing: {slot['name']} ({slot['target_time']})...")
            video_path = run_single_pipeline(
                preferred_niche=slot["niche_bias"],
                voice=today_style["voice"],
                highlight_color=today_style["subtitle_color"],
                custom_marketing_hook=today_style["marketing_hook"]
            )
            slot_data["done"] = True
            slot_data["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            slot_data["video_file"] = video_path.name
            state["total_published"] = state.get("total_published", 0) + 1
            save_state(state)
            print(f"[OK] Slot {s_id} complete!")
            return
            
    print("[i] All 4 slots for today are already completed! Amazing job.")

def print_status(today_data=None, today_style=None, now_minutes=None):
    if not today_data:
        state = load_state()
        state = init_today_state(state)
        today_data = state["history"][get_today_key()]
        today_style = get_today_style()
        now = datetime.now()
        now_minutes = now.hour * 60 + now.minute

    print("\n" + "-" * 68)
    print(f"  TODAY'S 4 POSTING SLOTS STATUS ({today_style['day_name']} - {today_style['theme_title']}):")
    print("-" * 68)
    
    for slot in DAILY_SLOTS:
        s_id = slot["slot_id"]
        s_info = today_data["slots"].get(s_id, {})
        target_min = time_to_minutes(slot["target_time"])
        target_time = slot["target_time"]
        
        if s_info.get("done"):
            status_text = f"[DONE] Uploaded at {s_info.get('completed_at', '')[11:16]} ({s_info.get('video_file', '')})"
        elif now_minutes >= target_min:
            status_text = "[PENDING RECOVERY] Will post on next tick"
        else:
            diff = target_min - now_minutes
            hrs = diff // 60
            mins = diff % 60
            status_text = f"[QUEUED] Scheduled in {hrs}h {mins}m"
            
        print(f"  {target_time} - {slot['name'][:24]:<24} : {status_text}")
    print("-" * 68 + "\n")

def run_daemon():
    """Runs continuous background monitoring loop."""
    print("[*] Starting Autopilot Daemon... (Press Ctrl+C to stop)")
    while True:
        try:
            check_and_execute_slots()
        except Exception as e:
            print(f"[!] Daemon error: {e}")
        # Sleep for 15 minutes before checking again
        time.sleep(900)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "--check":
            check_and_execute_slots()
        elif cmd == "--status":
            print_status()
        elif cmd == "--force-next":
            force_run_next()
        elif cmd == "--daemon":
            run_daemon()
    else:
        check_and_execute_slots()
