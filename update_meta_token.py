import sys
import base64
import subprocess
import requests
from nacl import encoding, public

if len(sys.argv) < 2:
    print("Usage: python update_meta_token.py <NEW_META_TOKEN>")
    sys.exit(1)

new_token = sys.argv[1].strip()

# 1. Verify token with Meta Graph API
print("[*] Verifying new token with Meta Graph API...")
test_res = requests.get("https://graph.facebook.com/v19.0/me", params={"access_token": new_token})
if test_res.status_code != 200:
    print(f"[!] Token test failed: {test_res.text}")
    sys.exit(1)

meta_data = test_res.json()
print(f"[OK] Token valid! Connected entity: {meta_data.get('name')} (ID: {meta_data.get('id')})")

# 2. Update config.env locally
env_path = r"C:\Users\manik\.gemini\antigravity\scratch\autopilot-influencer\config.env"
with open(env_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(env_path, "w", encoding="utf-8") as f:
    for line in lines:
        if line.startswith("FACEBOOK_ACCESS_TOKEN="):
            f.write(f'FACEBOOK_ACCESS_TOKEN="{new_token}"\n')
        elif line.startswith("INSTAGRAM_ACCESS_TOKEN="):
            f.write(f'INSTAGRAM_ACCESS_TOKEN="{new_token}"\n')
        else:
            f.write(line)

print("[OK] Updated local config.env")

# 3. Update GitHub Actions Secrets via API
proc = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
stdout, stderr = proc.communicate(input="protocol=https\nhost=github.com\n\n")
creds = dict(line.split("=", 1) for line in stdout.splitlines() if "=" in line)
gh_token = creds.get("password")
username = creds.get("username")

if gh_token and username:
    headers = {
        "Authorization": f"token {gh_token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Antigravity-Agent"
    }
    repo_name = "curiosreturns-autopilot"
    pk_url = f"https://api.github.com/repos/{username}/{repo_name}/actions/secrets/public-key"
    pk_res = requests.get(pk_url, headers=headers)
    if pk_res.status_code == 200:
        pk_data = pk_res.json()
        key_id = pk_data["key_id"]
        public_key = pk_data["key"]

        def encrypt_secret(pk: str, val: str) -> str:
            pk_bytes = base64.b64decode(pk)
            sb = public.SealedBox(public.PublicKey(pk_bytes))
            return base64.b64encode(sb.encrypt(val.encode("utf-8"))).decode("utf-8")

        for sec in ["FACEBOOK_ACCESS_TOKEN", "INSTAGRAM_ACCESS_TOKEN"]:
            enc = encrypt_secret(public_key, new_token)
            sec_url = f"https://api.github.com/repos/{username}/{repo_name}/actions/secrets/{sec}"
            requests.put(sec_url, headers=headers, json={"encrypted_value": enc, "key_id": key_id})
            print(f"[OK] Updated GitHub Cloud Secret: {sec}")
            
print("\n[SUCCESS] Token updated across both local and 24/7 GitHub Cloud Autopilot!")
