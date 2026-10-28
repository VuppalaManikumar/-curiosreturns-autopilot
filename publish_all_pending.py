import os
import sys
import time
from pathlib import Path
from config import OUTPUTS_DIR, get_config
from meta_publisher import publish_video

def publish_all_created_videos():
    print("=" * 68)
    print("     BROADCASTING ALL CREATED REELS TO FACEBOOK & INSTAGRAM")
    print("=" * 68)
    
    fb_token = get_config("FACEBOOK_ACCESS_TOKEN", "").strip()
    ig_token = get_config("INSTAGRAM_ACCESS_TOKEN", "").strip() or fb_token
    fb_page_id = get_config("FACEBOOK_PAGE_ID", "").strip()
    ig_user_id = get_config("INSTAGRAM_ACCOUNT_ID", "").strip()
    
    if not fb_token:
        print("[ERROR] No Meta Access Token found in config.env!")
        return
        
    mp4_files = sorted(OUTPUTS_DIR.glob("*.mp4"))
    if not mp4_files:
        print("[i] No video files found in CREATED_VIDEOS folder.")
        return
        
    print(f"[*] Found {len(mp4_files)} rendered video(s) ready for broadcast.\n")
    
    success_count = 0
    for video in mp4_files:
        caption_file = video.with_suffix(".caption.txt")
        caption_text = ""
        pinned_comment = ""
        
        if caption_file.exists():
            with open(caption_file, "r", encoding="utf-8") as f:
                content = f.read()
                if "=== REEL CAPTION ===" in content and "=== PINNED MARKETING COMMENT ===" in content:
                    parts = content.split("=== PINNED MARKETING COMMENT ===")
                    caption_text = parts[0].replace("=== REEL CAPTION ===", "").strip()
                    pinned_comment = parts[1].strip()
                else:
                    caption_text = content
                    
        print(f"\n[+] Broadcasting: {video.name}")
        posted_fb, posted_ig = publish_video(video, caption_text, pinned_comment)
        if posted_fb or posted_ig:
            success_count += 1
            print(f"[OK] Successfully uploaded: {video.name}")
            time.sleep(5)
        else:
            print(f"[!] Upload failed for: {video.name}")
            break
            
    print("\n" + "=" * 68)
    print(f"   COMPLETED: {success_count}/{len(mp4_files)} videos broadcasted live!")
    print("=" * 68)

if __name__ == "__main__":
    publish_all_created_videos()
