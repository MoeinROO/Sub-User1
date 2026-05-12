import requests
import base64
import re
import subprocess

# ================== CONFIG ==================
SUB_URL = "https://fineartsinfo.org/up/NzQzMDQzMTA2NCwxNzc4NDA5NTIzhJVjG5bZu8"
LOCAL_FILE = "User1.txt"

GIT_NAME = "usage-bot"
GIT_EMAIL = "usage-bot@users.noreply.github.com"
# ============================================


def get_usage_text():
    """Download main subscription and extract usage text"""
    resp = requests.get(SUB_URL, timeout=15)
    resp.raise_for_status()
    raw = resp.text.strip()

    # try base64 decode
    try:
        decoded = base64.b64decode(raw).decode("utf-8", errors="ignore")
    except Exception:
        decoded = raw

    # regex for usage
    pattern = r"Usage:\s*([\d.]+\s*(?:KB|MB|GB))\s*of\s*([\d.]+\s*(?:KB|MB|GB))"
    match = re.search(pattern, decoded)

    if not match:
        raise RuntimeError("Usage information not found in subscription")

    used = match.group(1)
    total = match.group(2)

    return f"✅Usage: {used} of {total}"


def update_remarks(remark_text):
    """Replace remarks field in User1.txt"""
    with open(LOCAL_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = re.sub(
        r'"remarks"\s*:\s*".*?"',
        f'"remarks": "{remark_text}"',
        content,
    )

    with open(LOCAL_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)


def git_commit_push():
    """Commit and push changes"""
    subprocess.run(["git", "config", "user.name", GIT_NAME], check=False)
    subprocess.run(["git", "config", "user.email", GIT_EMAIL], check=False)
    subprocess.run(["git", "add", LOCAL_FILE], check=False)
    subprocess.run(["git", "commit", "-m", "Auto update usage"], check=False)
    subprocess.run(["git", "push"], check=False)


def main():
    print("Updating usage...")
    remark = get_usage_text()
    print("New remark:", remark)

    update_remarks(remark)
    git_commit_push()

    print("Done ✅")


if __name__ == "__main__":
    main()
