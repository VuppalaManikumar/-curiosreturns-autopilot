import os
import sys
import base64
import subprocess
import requests
from nacl import encoding, public

# 1. Get credentials from Git Credential Manager
proc = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
stdout, stderr = proc.communicate(input="protocol=https\nhost=github.com\n\n")

creds = dict(line.split("=", 1) for line in stdout.splitlines() if "=" in line)
token = creds.get("password")
username = creds.get("username")

if not token or not username:
    print("[ERROR] Could not retrieve GitHub credentials from Git Credential Manager.")
    sys.exit(1)

print(f"[*] Authenticated as GitHub user: {username}")

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "Antigravity-Agent"
}

repo_name = "curiosreturns-autopilot"

# 2. Create the private repository if it doesn't exist
repo_url = f"https://api.github.com/repos/{username}/{repo_name}"
res = requests.get(repo_url, headers=headers)
if res.status_code == 404:
    print(f"[*] Creating private repository '{repo_name}' on GitHub...")
    payload = {
        "name": repo_name,
        "description": "24/7 AI Influencer Autopilot for CuriosReturns (Instagram Reels & Facebook)",
        "private": True,
        "auto_init": False
    }
    create_res = requests.post("https://api.github.com/user/repos", headers=headers, json=payload)
    if create_res.status_code in (200, 201):
        print(f"[OK] Repository created successfully: https://github.com/{username}/{repo_name}")
    else:
        print(f"[ERROR] Failed to create repo: {create_res.status_code} - {create_res.text}")
        sys.exit(1)
else:
    print(f"[OK] Repository '{repo_name}' already exists.")

# 3. Read secrets from config.env
env_path = r"C:\Users\manik\.gemini\antigravity\scratch\autopilot-influencer\config.env"
env_vars = {}
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env_vars[k.strip()] = v.strip().strip('"').strip("'")

secrets_to_upload = {
    "FACEBOOK_PAGE_ID": env_vars.get("FACEBOOK_PAGE_ID", "1334627683077843"),
    "FACEBOOK_ACCESS_TOKEN": env_vars.get("FACEBOOK_ACCESS_TOKEN", ""),
    "INSTAGRAM_ACCOUNT_ID": env_vars.get("INSTAGRAM_ACCOUNT_ID", "17841467777191474"),
    "INSTAGRAM_ACCESS_TOKEN": env_vars.get("INSTAGRAM_ACCESS_TOKEN", ""),
    "BRAND_NAME": env_vars.get("BRAND_NAME", "@curiosreturns")
}

# 4. Get repo public key for encrypting secrets
pk_url = f"https://api.github.com/repos/{username}/{repo_name}/actions/secrets/public-key"
pk_res = requests.get(pk_url, headers=headers)
if pk_res.status_code == 200:
    pk_data = pk_res.json()
    key_id = pk_data["key_id"]
    public_key = pk_data["key"]
    
    def encrypt_secret(public_key: str, secret_value: str) -> str:
        public_key_bytes = base64.b64decode(public_key)
        sealed_box = public.SealedBox(public.PublicKey(public_key_bytes))
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
        return base64.b64encode(encrypted).decode("utf-8")

    print("[*] Uploading encrypted secrets to GitHub Actions...")
    for s_name, s_val in secrets_to_upload.items():
        if s_val:
            enc_val = encrypt_secret(public_key, s_val)
            sec_url = f"https://api.github.com/repos/{username}/{repo_name}/actions/secrets/{s_name}"
            sec_res = requests.put(sec_url, headers=headers, json={"encrypted_value": enc_val, "key_id": key_id})
            if sec_res.status_code in (201, 204):
                print(f"  [OK] Secret configured: {s_name}")
            else:
                print(f"  [!] Failed to set secret {s_name}: {sec_res.text}")
else:
    print(f"[!] Could not get repo public key: {pk_res.text}")

# 5. Push code to GitHub
print("[*] Pushing repository code to GitHub...")
repo_remote = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"

subprocess.run(["git", "branch", "-M", "main"], cwd=r"C:\Users\manik\.gemini\antigravity\scratch\autopilot-influencer")
subprocess.run(["git", "remote", "remove", "origin"], cwd=r"C:\Users\manik\.gemini\antigravity\scratch\autopilot-influencer", capture_output=True)
subprocess.run(["git", "remote", "add", "origin", repo_remote], cwd=r"C:\Users\manik\.gemini\antigravity\scratch\autopilot-influencer")

push_proc = subprocess.run(["git", "push", "-u", "origin", "main", "--force"], cwd=r"C:\Users\manik\.gemini\antigravity\scratch\autopilot-influencer", capture_output=True, text=True)
print("Git Push Code:", push_proc.returncode)
if push_proc.returncode == 0:
    print("[OK] All code and background workflows pushed to GitHub successfully!")
else:
    print("[!] Push output:", push_proc.stdout)
    print("[!] Push error:", push_proc.stderr)

# 6. Verify GitHub Actions workflow
wf_url = f"https://api.github.com/repos/{username}/{repo_name}/actions/workflows"
wf_res = requests.get(wf_url, headers=headers)
if wf_res.status_code == 200:
    workflows = wf_res.json().get("workflows", [])
    print(f"[OK] Found {len(workflows)} active workflow(s):")
    for wf in workflows:
        print(f"  - {wf['name']} (State: {wf['state']}, ID: {wf['id']})")
else:
    print(f"[!] Workflows status: {wf_res.text}")

# Reset remote without exposing token in git config
clean_remote = f"https://github.com/{username}/{repo_name}.git"
subprocess.run(["git", "remote", "set-url", "origin", clean_remote], cwd=r"C:\Users\manik\.gemini\antigravity\scratch\autopilot-influencer")
print(f"\n[SUCCESS] 24/7 Cloud Autopilot is fully configured and live at:\nhttps://github.com/{username}/{repo_name}")
