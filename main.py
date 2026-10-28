import os
import sys
import time
import re
import argparse
from pathlib import Path
from datetime import datetime

# Safe standard output encoding on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from config import BASE_DIR, TEMP_DIR, OUTPUTS_DIR, get_config
from script_generator import get_next_script
from viral_auditor import enforce_elite_quality
from tts_engine import generate_voiceover
from video_engine import create_reel
from meta_publisher import publish_video
from daily_styles import get_today_style

def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>| ]+', "_", name).strip("_")

def run_single_pipeline(preferred_niche="random", voice=None, highlight_color=None, custom_marketing_hook=None):
    start_time = time.time()
    
    # 1. Fetch script and pass through the Algorithmic Quality Auditor
    raw_script = get_next_script(preferred_niche)
    script_data = enforce_elite_quality(raw_script)
    audit = script_data.get("audit", {})
    score = audit.get("total_score", 95)
    
    title = script_data.get("title", "Viral_Reel")
    script_text = script_data.get("script", "")
    caption = script_data.get("caption", "")
    pinned_comment = custom_marketing_hook or script_data.get("pinned_comment", "")
    
    print("\n" + "-" * 65)
    print(f"[*] AUDIT SCORE: {score}/100 -> {audit.get('verdict', 'ELITE')}")
    for k, v in audit.get("metrics", {}).items():
        print(f"    - {k.replace('_', ' ').title()}: {v}")
    print("-" * 65)
    print(f"[+] Title:   {title}")
    print(f"[+] Script:  {script_text[:85]}...\n")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_title = sanitize_filename(title)
    
    audio_path = TEMP_DIR / f"{timestamp}_voice.mp3"
    ass_path = TEMP_DIR / f"{timestamp}_subs.ass"
    output_video = OUTPUTS_DIR / f"{timestamp}_{clean_title}.mp4"
    
    # 2. Voiceover & Karaoke Subtitles with Dynamic Daily Palette
    print("--- [Step 1/3] Synthesizing Neural Audio & Glowing Subtitles ---")
    active_voice = script_data.get("voice") or voice or "en-US-ChristopherNeural"
    active_color = script_data.get("subtitle_color") or highlight_color or "&H0024E0FB"
    generate_voiceover(script_text, audio_path, ass_path, voice=active_voice, highlight_color=active_color)
    
    # 3. Video Rendering with Micro-Zoom Retention
    print("\n--- [Step 2/3] Rendering 9:16 Video (Micro-Zoom & Sub-Bass Audio) ---")
    create_reel(audio_path, ass_path, output_video)
    
    # 4. Meta Dual-Publishing (Facebook Page & Instagram Reels)
    print("\n--- [Step 3/3] Delivering High-Conversion Marketing Content ---")
    publish_video(output_video, caption, pinned_comment)
    
    # Clean up temp files
    for temp_f in [audio_path, ass_path]:
        if temp_f.exists():
            try:
                temp_f.unlink()
            except Exception:
                pass
                
    elapsed = time.time() - start_time
    print(f"[OK] Completed '{title}' in {elapsed:.1f}s -> {output_video.name}")
    return output_video

def run():
    parser = argparse.ArgumentParser(description="AI Influencer Autopilot Pipeline")
    parser.add_argument("--count", type=int, default=1, help="Number of reels to generate in this batch")
    parser.add_argument("--niche", type=str, default="", help="Specific niche override")
    args = parser.parse_args()
    
    today_info = get_today_style()
    niche = args.niche if args.niche else today_info["primary_niche"]
    count = max(1, args.count)
    
    print("=" * 68)
    print(f"      AI INFLUENCER AUTOPILOT - DAILY THEME: {today_info['day_name'].upper()} {today_info['emoji']}      ")
    print(f"      Theme: {today_info['theme_title']} | Voice: {today_info['voice']} ")
    print("=" * 68)
    print(f"[*] Target Niche: {niche} | Total Videos to Produce: {count}\n")
    
    created_videos = []
    for i in range(count):
        if count > 1:
            print(f"\n>>>>>>>>>>>> CREATING ELITE VIDEO {i+1} of {count} <<<<<<<<<<<<")
        v = run_single_pipeline(
            preferred_niche=niche,
            voice=today_info["voice"],
            highlight_color=today_info["subtitle_color"],
            custom_marketing_hook=today_info["marketing_hook"]
        )
        created_videos.append(v)
        if i < count - 1:
            time.sleep(2)
            
    print("\n" + "=" * 68)
    print(f"  ALL DONE! Successfully engineered {len(created_videos)} elite reel(s).")
    print(f"  Folder: {OUTPUTS_DIR.resolve()}")
    print("=" * 68)
    
    try:
        os.startfile(str(OUTPUTS_DIR.resolve()))
    except Exception:
        pass

if __name__ == "__main__":
    run()
