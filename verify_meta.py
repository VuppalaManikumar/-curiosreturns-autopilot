import requests
from config import get_config

def test_connection():
    print("=" * 60)
    print("      TESTING META (INSTAGRAM & FACEBOOK) CONNECTION        ")
    print("=" * 60)
    
    fb_token = get_config("FACEBOOK_ACCESS_TOKEN", "").strip()
    fb_page_id = get_config("FACEBOOK_PAGE_ID", "").strip()
    ig_id = get_config("INSTAGRAM_ACCOUNT_ID", "").strip()
    
    if not fb_token:
        print("[!] ERROR: FACEBOOK_ACCESS_TOKEN is missing in config.env")
        return False
        
    # 1. Test token with Facebook Graph API
    url = "https://graph.facebook.com/v19.0/me"
    res = requests.get(url, params={"access_token": fb_token})
    if res.status_code != 200:
        print(f"[!] Invalid Token: {res.text}")
        return False
        
    data = res.json()
    print(f"[OK] Token valid! Connected entity: {data.get('name')} (ID: {data.get('id')})")
    
    # 2. Check Facebook Page
    if fb_page_id:
        p_res = requests.get(f"https://graph.facebook.com/v19.0/{fb_page_id}", params={"access_token": fb_token, "fields": "name,instagram_business_account"})
        if p_res.status_code == 200:
            p_data = p_res.json()
            print(f"[OK] Facebook Page verified: '{p_data.get('name')}'")
            ig_account = p_data.get("instagram_business_account", {})
            if ig_account:
                print(f"[OK] Linked Instagram Business Account found! ID: {ig_account.get('id')}")
            else:
                print("[!] Notice: No Instagram account linked to this Facebook Page yet.")
        else:
            print(f"[!] Could not verify Facebook Page ID {fb_page_id}: {p_res.text}")
            
    print("=" * 60)
    print("ALL CHECKS COMPLETE!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    test_connection()
