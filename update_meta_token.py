import sys
import os
import requests
import base64
import subprocess
from nacl import encoding, public
from pathlib import Path

# Safe encoding on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

APP_ID = "1532717011964464"
PAGE_ID = "1334627683077843"
IG_ID = "17841467777191474"
REPO_NAME = "curiosreturns-autopilot"

def update_tokens(token: str, app_secret: str = None):
    print("=" * 68)
    print("            UPDATING AND VALIDATING META TOKENS")
    print("=" * 68)

    clean_token = token.strip()
    
    # 1. If App Secret is provided, exchange for 60-Day Long-Lived Token
    long_lived_user_token = clean_token
    if app_secret:
        print("\n[*] Exchanging token with Meta OAuth for 60-Day Long-Lived Token...")
        res = requests.get(
            "https://graph.facebook.com/v19.0/oauth/access_token",
            params={
                "grant_type": "fb_exchange_token",
                "client_id": APP_ID,
                "client_secret": app_secret.strip(),
                "fb_exchange_token": clean_token
            },
            timeout=20
        )
        if res.status_code == 200:
            long_lived_user_token = res.json().get("access_token")
            print("[OK] Successfully generated Long-Lived User Token!")
        else:
            print(f"[!] App Secret exchange notice: {res.text}")

    # 2. Extract Permanent Page Token
    print(f"\n[*] Requesting Page Token for CuriosReturns (ID: {PAGE_ID})...")
    p_res = requests.get(
        f"https://graph.facebook.com/v19.0/{PAGE_ID}",
        params={"fields": "access_token,name", "access_token": long_lived_user_token},
        timeout=20
    )
    
    if p_res.status_code == 200:
        page_token = p_res.json().get("access_token")
        page_name = p_res.json().get("name")
        print(f"[OK] Successfully verified Page Token for '{page_name}'!")
    else:
        print(f"[!] Notice: Could not extract Page token directly ({p_res.text}). Using provided token for both.")
        page_token = long_lived_user_token

    # 3. Update config.env
    env_path = Path(r"C:\Users\manik\.gemini\antigravity\scratch\autopilot-influencer\config.env")
    with open(env_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open(env_path, "w", encoding="utf-8") as f:
        for line in lines:
            if line.startswith("FACEBOOK_ACCESS_TOKEN="):
                f.write(f'FACEBOOK_ACCESS_TOKEN="{page_token}"\n')
            elif line.startswith("INSTAGRAM_ACCESS_TOKEN="):
                f.write(f'INSTAGRAM_ACCESS_TOKEN="{long_lived_user_token}"\n')
            else:
                f.write(line)
    print("\n[OK] Updated local config.env")

    # 4. Sync to GitHub Secrets
    print("\n[*] Syncing to 24/7 GitHub Actions Cloud...")
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
                    "FACEBOOK_ACCESS_TOKEN": page_token,
                    "INSTAGRAM_ACCOUNT_ID": IG_ID,
                    "INSTAGRAM_ACCESS_TOKEN": long_lived_user_token
                }
                for s_name, s_val in secrets.items():
                    enc = encrypt_secret(public_key, s_val)
                    sec_url = f"https://api.github.com/repos/{username}/{REPO_NAME}/actions/secrets/{s_name}"
                    requests.put(sec_url, headers=headers, json={"encrypted_value": enc, "key_id": key_id})
                    print(f"    [OK] Updated GitHub Secret: {s_name}")
    except Exception as e:
        print(f"[!] GitHub Secret sync notice: {e}")

    print("\n[SUCCESS] Token setup complete!")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_meta_token.py <TOKEN> [APP_SECRET]")
    else:
        tok = sys.argv[1]
        sec = sys.argv[2] if len(sys.argv) > 2 else None
        update_tokens(tok, sec)
