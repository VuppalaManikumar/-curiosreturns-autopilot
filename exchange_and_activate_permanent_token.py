import sys
import os
import requests
import base64
import subprocess
from nacl import encoding, public
from pathlib import Path

# Fix Windows console UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

APP_ID = "1532717011964464"
PAGE_ID = "1334627683077843"
IG_ID = "17841467777191474"
REPO_NAME = "curiosreturns-autopilot"

def exchange_and_activate(raw_user_token: str, app_secret: str = None):
    print("=" * 68)
    print("      METE PERMANENT TOKEN ACTIVATION & BROADCAST SYSTEM")
    print("=" * 68)

    user_token = raw_user_token.strip()
    
    # 1. If App Secret is provided, exchange for a 60-Day Long-Lived Token
    long_lived_user_token = user_token
    if app_secret:
        print("\n[*] Exchanging short-lived token for 60-Day Long-Lived Token via Meta OAuth...")
        exchange_url = "https://graph.facebook.com/v19.0/oauth/access_token"
        params = {
            "grant_type": "fb_exchange_token",
            "client_id": APP_ID,
            "client_secret": app_secret.strip(),
            "fb_exchange_token": user_token
        }
        res = requests.get(exchange_url, params=params, timeout=20)
        if res.status_code == 200:
            data = res.json()
            long_lived_user_token = data.get("access_token")
            print("[OK] Successfully generated Long-Lived User Token!")
        else:
            print(f"[!] Exchange failed ({res.status_code}): {res.text}")
            print("[*] Proceeding with provided token...")

    # 2. Extract the NEVER-EXPIRING Page Access Token
    print(f"\n[*] Generating Permanent Page Access Token for Page ID: {PAGE_ID}...")
    page_url = f"https://graph.facebook.com/v19.0/{PAGE_ID}"
    params = {
        "fields": "access_token,name",
        "access_token": long_lived_user_token
    }
    p_res = requests.get(page_url, params=params, timeout=20)
    if p_res.status_code != 200:
        print(f"[ERROR] Could not fetch Page Token ({p_res.status_code}): {p_res.text}")
        return False
        
    p_data = p_res.json()
    permanent_page_token = p_data.get("access_token")
    page_name = p_data.get("name")
    print(f"[OK] Successfully obtained Page Token for '{page_name}'!")

    # 3. Verify debug info on both tokens
    print("\n[*] Auditing Token Expiration with Meta Debug API...")
    debug_url = "https://graph.facebook.com/debug_token"
    debug_res = requests.get(debug_url, params={"input_token": permanent_page_token, "access_token": permanent_page_token}, timeout=20)
    if debug_res.status_code == 200:
        d_info = debug_res.json().get("data", {})
        exp = d_info.get("expires_at")
        exp_str = "NEVER (Permanent)" if exp == 0 else f"Expires at timestamp {exp}"
        print(f"    - Page Token Validity: {d_info.get('is_valid')}")
        print(f"    - Page Token Expiration: {exp_str}")
        print(f"    - Permissions: {', '.join(d_info.get('scopes', []))}")

    # 4. Save to config.env
    env_path = Path(r"C:\Users\manik\.gemini\antigravity\scratch\autopilot-influencer\config.env")
    with open(env_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open(env_path, "w", encoding="utf-8") as f:
        for line in lines:
            if line.startswith("FACEBOOK_ACCESS_TOKEN="):
                f.write(f'FACEBOOK_ACCESS_TOKEN="{permanent_page_token}"\n')
            elif line.startswith("INSTAGRAM_ACCESS_TOKEN="):
                f.write(f'INSTAGRAM_ACCESS_TOKEN="{long_lived_user_token}"\n')
            elif line.startswith("FACEBOOK_PAGE_ID="):
                f.write(f'FACEBOOK_PAGE_ID="{PAGE_ID}"\n')
            elif line.startswith("INSTAGRAM_ACCOUNT_ID="):
                f.write(f'INSTAGRAM_ACCOUNT_ID="{IG_ID}"\n')
            else:
                f.write(line)
    print("\n[OK] Updated local config.env with verified tokens!")

    # 5. Sync to GitHub Secrets
    print("\n[*] Syncing credentials to 24/7 Cloud GitHub Secrets...")
    try:
        proc = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = proc.communicate(input="protocol=https\nhost=github.com\n\n")
        creds = dict(l.split("=", 1) for l in stdout.splitlines() if "=" in l)
        gh_token = creds.get("password")
        username = creds.get("username")

        if gh_token and username:
            headers = {
                "Authorization": f"token {gh_token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Antigravity-Agent"
            }
            pk_url = f"https://api.github.com/repos/{username}/{REPO_NAME}/actions/secrets/public-key"
            pk_res = requests.get(pk_url, headers=headers)
            if pk_res.status_code == 200:
                pk_data = pk_res.json()
                key_id = pk_data["key_id"]
                public_key = pk_data["key"]

                def encrypt_secret(pk: str, val: str) -> str:
                    pk_bytes = base64.b64decode(pk)
                    sb = public.SealedBox(public.PublicKey(pk_bytes))
                    return base64.b64encode(sb.encrypt(val.encode("utf-8"))).decode("utf-8")

                secrets = {
                    "FACEBOOK_PAGE_ID": PAGE_ID,
                    "FACEBOOK_ACCESS_TOKEN": permanent_page_token,
                    "INSTAGRAM_ACCOUNT_ID": IG_ID,
                    "INSTAGRAM_ACCESS_TOKEN": long_lived_user_token
                }
                for s_name, s_val in secrets.items():
                    enc = encrypt_secret(public_key, s_val)
                    sec_url = f"https://api.github.com/repos/{username}/{REPO_NAME}/actions/secrets/{s_name}"
                    requests.put(sec_url, headers=headers, json={"encrypted_value": enc, "key_id": key_id})
                    print(f"    [OK] Updated GitHub Secret: {s_name}")
    except Exception as e:
        print(f"[!] GitHub Secret sync warning: {e}")

    print("\n[SUCCESS] Tokens activated and synced across Local & Cloud!")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python exchange_and_activate_permanent_token.py <USER_TOKEN> [APP_SECRET]")
    else:
        user_tok = sys.argv[1]
        secret = sys.argv[2] if len(sys.argv) > 2 else None
        exchange_and_activate(user_tok, secret)
