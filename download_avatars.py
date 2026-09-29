import json
import re
import ssl
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = Path("/Users/ricksabchez/workspace/projects/iranian-youtubers")
DATA_FILE = BASE_DIR / "data" / "youtubers.json"
AVATARS_DIR = BASE_DIR / "avatars"
AVATARS_DIR.mkdir(parents=True, exist_ok=True)

SSL_CTX = ssl._create_unverified_context()
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}

def extract_avatar_url_from_html(html):
    # Try channelRenderer first
    m_cr = re.findall(r'\"channelRenderer\":\{.*?\"thumbnail\":\{\"thumbnails\":\[\{\"url\":\"([^\"]+)\"', html)
    if m_cr:
        url = m_cr[0]
        if url.startswith("//"):
            url = "https:" + url
        return url
    
    # Try avatar thumbnails
    m_av = re.findall(r'\"avatar\":\{\"thumbnails\":\[\{\"url\":\"([^\"]+)\"', html)
    if m_av:
        url = m_av[0]
        if url.startswith("//"):
            url = "https:" + url
        return url

    # Try any yt3 googleusercontent or ggpht avatar
    matches = re.findall(r'https?://yt3\.(?:googleusercontent\.com|ggpht\.com)/[a-zA-Z0-9_\-=]+', html)
    if matches:
        return matches[0]

    return None

def fetch_and_save_avatar(entry):
    handle = entry["handle"]
    name = entry["name"]
    jpg_filename = f"{handle.lower()}.jpg"
    jpg_path = AVATARS_DIR / jpg_filename

    # If already downloaded and valid image > 2KB, keep it
    if jpg_path.exists() and jpg_path.stat().st_size > 2048:
        return entry["id"], jpg_filename, True, None, None

    avatar_url = None
    canonical_handle = None

    # Step 1: Try direct channel URL
    channel_url = entry.get("channel_url", f"https://www.youtube.com/@{handle}")
    try:
        req = urllib.request.Request(channel_url, headers=HEADERS)
        with urllib.request.urlopen(req, context=SSL_CTX, timeout=9) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            avatar_url = extract_avatar_url_from_html(html)
            # check canonical
            m_canon = re.findall(r'\"canonicalBaseUrl\":\"(/@[^\"]+)\"', html)
            if m_canon:
                canonical_handle = m_canon[0].replace("/@", "")
    except Exception:
        pass

    # Step 2: Fallback to search query by creator name
    if not avatar_url:
        try:
            search_query = f"{name} یوتیوب"
            search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}"
            req = urllib.request.Request(search_url, headers=HEADERS)
            with urllib.request.urlopen(req, context=SSL_CTX, timeout=9) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
                avatar_url = extract_avatar_url_from_html(html)
                m_canon = re.findall(r'\"canonicalBaseUrl\":\"(/@[^\"]+)\"', html)
                if m_canon:
                    canonical_handle = m_canon[0].replace("/@", "")
        except Exception as e:
            print(f"Search failed for {name}: {e}")

    # Step 3: Download avatar image
    if avatar_url:
        try:
            # Clean and upscale to 240px
            base_url = avatar_url.split("=")[0]
            clean_url = f"{base_url}=s240-c-k-c0x00ffffff-no-rj"
            img_req = urllib.request.Request(clean_url, headers=HEADERS)
            with urllib.request.urlopen(img_req, context=SSL_CTX, timeout=9) as img_resp:
                img_data = img_resp.read()
                if len(img_data) > 1024:
                    jpg_path.write_bytes(img_data)
                    return entry["id"], jpg_filename, True, canonical_handle, clean_url
        except Exception as e:
            print(f"Image download failed for {handle}: {e}")

    # Fallback to SVG
    svg_filename = f"{handle.lower()}.svg"
    return entry["id"], svg_filename, False, canonical_handle, None

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        youtubers = json.load(f)

    print(f"Fetching avatars for {len(youtubers)} creators with search fallback...")
    results = {}

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_and_save_avatar, y): y for y in youtubers}
        for future in as_completed(futures):
            y_id, filename, success, canon, av_url = future.result()
            results[y_id] = (filename, success, canon)

    success_count = 0
    for y in youtubers:
        filename, success, canon = results.get(y["id"], (f"{y['handle'].lower()}.svg", False, None))
        y["avatar"] = f"avatars/{filename}"
        if canon and canon != y["handle"]:
            y["channel_url"] = f"https://www.youtube.com/@{canon}"
        if success:
            success_count += 1

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(youtubers, f, ensure_ascii=False, indent=2)

    print(f"Completed! {success_count}/{len(youtubers)} real photo avatars downloaded.")

if __name__ == "__main__":
    main()
