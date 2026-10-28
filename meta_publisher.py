import os
import time
import requests
from pathlib import Path
from config import get_config

def get_linked_instagram_id(page_id: str, access_token: str):
    """Dynamically queries Meta to get the linked Instagram Business/Creator Account ID."""
    try:
        url = f"https://graph.facebook.com/v19.0/{page_id}"
        params = {"access_token": access_token, "fields": "instagram_business_account"}
        res = requests.get(url, params=params, timeout=15)
        if res.status_code == 200:
            data = res.json()
            ig_account = data.get("instagram_business_account", {})
            if ig_account and "id" in ig_account:
                return ig_account["id"]
    except Exception as e:
        print(f"[!] Error detecting linked Instagram account: {e}")
    return None

def format_marketing_caption(base_caption: str, pinned_comment: str) -> tuple[str, str]:
    brand = get_config("BRAND_NAME", "@curiosreturns").strip()
    cta = get_config("CALL_TO_ACTION", "").strip()
    link = get_config("MARKETING_LINK", "").strip()
    
    extra_marketing = ""
    if brand:
        extra_marketing += f"\nFollow {brand} for daily mind-bending curiosities & psychology!\n"
    if cta:
        extra_marketing += f"{cta}\n"
    if link and link != "https://yourlink.com":
        extra_marketing += f"🔗 Link: {link}\n"
        
    full_caption = f"{base_caption.strip()}\n{extra_marketing}"
    final_pinned = pinned_comment if pinned_comment else "🔥 Follow @curiosreturns for daily mind-expanding secrets! 🧠✨"
    return full_caption, final_pinned

def upload_to_facebook_page(video_path: Path, caption: str, page_id: str, access_token: str):
    print(f"[*] Uploading to Facebook Page (ID: {page_id})...")
    url = f"https://graph-video.facebook.com/v19.0/{page_id}/videos"
    
    with open(video_path, "rb") as video_file:
        files = {"source": (video_path.name, video_file, "video/mp4")}
        data = {
            "access_token": access_token,
            "description": caption,
            "published": "true"
        }
        response = requests.post(url, files=files, data=data, timeout=120)
        
    if response.status_code == 200:
        res_data = response.json()
        video_id = res_data.get("id")
        print(f"[OK] Successfully posted to Facebook Page! Video ID: {video_id}")
        return video_id
    else:
        print(f"[!] Facebook Page upload error: {response.text}")
        return None

def upload_to_instagram_reels(video_path: Path, caption: str, ig_user_id: str, access_token: str):
    print(f"[*] Uploading Reel to Instagram Account (ID: {ig_user_id})...")
    file_size = os.path.getsize(video_path)
    
    # 1. Initialize resumable upload session
    init_url = f"https://graph.facebook.com/v19.0/{ig_user_id}/media"
    init_data = {
        "access_token": access_token,
        "media_type": "REELS",
        "caption": caption,
        "upload_type": "resumable"
    }
    
    init_res = requests.post(init_url, data=init_data, timeout=30)
    if init_res.status_code != 200:
        print(f"[!] Instagram session init error: {init_res.text}")
        return None
        
    session_data = init_res.json()
    video_container_id = session_data.get("id")
    upload_url = session_data.get("uri")
    
    if not upload_url:
        print(f"[!] No upload URI returned by Instagram: {session_data}")
        return None
        
    # 2. Upload video binary stream
    print("[*] Transferring video stream to Instagram servers...")
    headers = {
        "Authorization": f"OAuth {access_token}",
        "offset": "0",
        "file_size": str(file_size),
        "Content-Type": "application/octet-stream"
    }
    with open(video_path, "rb") as video_file:
        video_bytes = video_file.read()
        
    upload_res = requests.post(upload_url, headers=headers, data=video_bytes, timeout=180)
    if upload_res.status_code not in (200, 204):
        print(f"[!] Instagram byte transfer error: {upload_res.text}")
        return None
        
    # 3. Wait for Meta encoding & processing
    print("[*] Waiting for Instagram media processing...")
    status_url = f"https://graph.facebook.com/v19.0/{video_container_id}"
    for _ in range(20):
        time.sleep(3)
        check_res = requests.get(status_url, params={"access_token": access_token, "fields": "status_code"}, timeout=15)
        if check_res.status_code == 200:
            status = check_res.json().get("status_code")
            if status == "FINISHED":
                break
            elif status == "ERROR":
                print(f"[!] Instagram video encoding failed.")
                return None
                
    # 4. Publish media container
    publish_url = f"https://graph.facebook.com/v19.0/{ig_user_id}/media_publish"
    pub_res = requests.post(publish_url, data={"access_token": access_token, "creation_id": video_container_id}, timeout=30)
    
    if pub_res.status_code == 200:
        pub_id = pub_res.json().get("id")
        print(f"[OK] Successfully published to Instagram Reels! Media ID: {pub_id}")
        return pub_id
    else:
        print(f"[!] Instagram publish error: {pub_res.text}")
        return None

def publish_video(video_path: Path, base_caption: str, pinned_comment: str = ""):
    fb_page_id = get_config("FACEBOOK_PAGE_ID", "").strip()
    fb_token = get_config("FACEBOOK_ACCESS_TOKEN", "").strip()
    ig_user_id = get_config("INSTAGRAM_ACCOUNT_ID", "").strip()
    ig_token = get_config("INSTAGRAM_ACCESS_TOKEN", "").strip() or fb_token

    final_caption, final_pinned = format_marketing_caption(base_caption, pinned_comment)

    # Save caption and pinned comment files alongside the video
    caption_file = video_path.with_suffix(".caption.txt")
    with open(caption_file, "w", encoding="utf-8") as f:
        f.write(f"=== REEL CAPTION ===\n{final_caption}\n\n=== PINNED MARKETING COMMENT ===\n{final_pinned}\n")

    posted_fb = False
    posted_ig = False

    # 1. Post to Facebook Page
    if fb_page_id and fb_token:
        try:
            fb_res = upload_to_facebook_page(video_path, final_caption, fb_page_id, fb_token)
            if fb_res:
                posted_fb = True
        except Exception as e:
            print(f"[!] Facebook posting failed: {e}")

    # 2. Post to Instagram Reels
    if ig_user_id and ig_token:
        try:
            ig_res = upload_to_instagram_reels(video_path, final_caption, ig_user_id, ig_token)
            if ig_res:
                posted_ig = True
        except Exception as e:
            print(f"[!] Instagram posting failed: {e}")

    print("\n=======================================================")
    print(f"  Facebook Page:   {'[POSTED LIVE]' if posted_fb else '[FAILED]'}")
    print(f"  Instagram Reels: {'[POSTED LIVE]' if posted_ig else '[FAILED]'}")
    print(f"  Video file:      {video_path.name}")
    print("=======================================================\n")
    return posted_fb, posted_ig
