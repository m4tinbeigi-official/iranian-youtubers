import json
import re
import ssl
import urllib.request
import urllib.parse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = Path("/Users/ricksabchez/workspace/projects/iranian-youtubers")
DATA_FILE = BASE_DIR / "data" / "youtubers.json"
OUT_JSON = BASE_DIR / "data" / "youtube_audit_report.json"
OUT_MD = BASE_DIR / "data" / "youtube_audit_summary.md"

SSL_CTX = ssl._create_unverified_context()
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

def parse_views(v_str):
    if not v_str:
        return 0
    s = str(v_str).strip()
    farsi_digits = "۰۱۲۳۴۵۶۷۸۹"
    for i, d in enumerate(farsi_digits):
        s = s.replace(d, str(i))
    s = s.replace("بازدید", "").replace("views", "").strip()
    if "M" in s or "میلیون" in s:
        num = re.findall(r"[0-9\.]+", s)
        return int(float(num[0]) * 1_000_000) if num else 0
    if "K" in s or "هزار" in s:
        num = re.findall(r"[0-9\.]+", s)
        return int(float(num[0]) * 1_000) if num else 0
    num = re.findall(r"[0-9]+", s.replace(",", ""))
    return int(num[0]) if num else 0

def fetch_creator_videos(creator):
    channel_url = creator.get("channel_url", f"https://www.youtube.com/@{creator['handle']}")
    url = f"{channel_url}/videos"
    videos = []
    
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=SSL_CTX, timeout=12) as r:
            html = r.read().decode("utf-8", errors="ignore")
            m = re.search(r"var ytInitialData = ({.*?});</script>", html)
            if m:
                data = json.loads(m.group(1))
                tabs = data.get("contents", {}).get("twoColumnBrowseResultsRenderer", {}).get("tabs", [])
                for t in tabs:
                    c = t.get("tabRenderer", {}).get("content", {})
                    grid = c.get("richGridRenderer", {})
                    for item in grid.get("contents", []):
                        # lockupViewModel
                        lvm = item.get("richItemRenderer", {}).get("content", {}).get("lockupViewModel", {})
                        if lvm:
                            meta = lvm.get("metadata", {}).get("lockupMetadataViewModel", {})
                            title = meta.get("title", {}).get("content", "")
                            rows = meta.get("metadata", {}).get("contentMetadataViewModel", {}).get("metadataRows", [])
                            views_raw = ""
                            time_raw = ""
                            for row in rows:
                                parts = row.get("metadataParts", [])
                                if len(parts) >= 1:
                                    views_raw = parts[0].get("text", {}).get("content", "")
                                if len(parts) >= 2:
                                    time_raw = parts[1].get("text", {}).get("content", "")
                            if title:
                                videos.append({
                                    "title": title,
                                    "views_raw": views_raw,
                                    "views": parse_views(views_raw),
                                    "published": time_raw
                                })
                        # legacy videoRenderer
                        vr = item.get("richItemRenderer", {}).get("content", {}).get("videoRenderer", {})
                        if vr:
                            title = vr.get("title", {}).get("runs", [{}])[0].get("text", "")
                            views_raw = vr.get("viewCountText", {}).get("simpleText", "")
                            time_raw = vr.get("publishedTimeText", {}).get("simpleText", "")
                            if title:
                                videos.append({
                                    "title": title,
                                    "views_raw": views_raw,
                                    "views": parse_views(views_raw),
                                    "published": time_raw
                                })
    except Exception as e:
        print(f"Failed audit for {creator['name']}: {e}")
        
    return creator["id"], creator["name"], creator["handle"], creator["category"], creator["subscribers"], videos

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        creators = json.load(f)
        
    print(f"Auditing recent videos for {len(creators)} Iranian YouTubers...")
    audit_results = []
    
    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = {executor.submit(fetch_creator_videos, c): c for c in creators}
        for future in as_completed(futures):
            c_id, name, handle, cat, subs, vids = future.result()
            total_views = sum(v["views"] for v in vids)
            avg_views = int(total_views / len(vids)) if vids else 0
            audit_results.append({
                "id": c_id,
                "name": name,
                "handle": handle,
                "category": cat,
                "subscribers": subs,
                "video_count_sampled": len(vids),
                "total_sample_views": total_views,
                "avg_views": avg_views,
                "videos": vids
            })
            
    # Sort by avg_views descending
    audit_results.sort(key=lambda x: x["avg_views"], reverse=True)
    
    # Global metrics
    total_videos_scraped = sum(c["video_count_sampled"] for c in audit_results)
    total_views_scraped = sum(c["total_sample_views"] for c in audit_results)
    
    # Category aggregation
    cat_stats = {}
    for c in audit_results:
        cat = c["category"]
        if cat not in cat_stats:
            cat_stats[cat] = {"count": 0, "total_views": 0, "total_vids": 0, "creators": []}
        cat_stats[cat]["count"] += 1
        cat_stats[cat]["total_views"] += c["total_sample_views"]
        cat_stats[cat]["total_vids"] += c["video_count_sampled"]
        cat_stats[cat]["creators"].append(c["name"])
        
    for cat, stat in cat_stats.items():
        stat["avg_views_per_video"] = int(stat["total_views"] / stat["total_vids"]) if stat["total_vids"] else 0
        
    # Top 15 most viewed individual videos
    all_videos_flat = []
    for c in audit_results:
        for v in c["videos"]:
            all_videos_flat.append({
                "creator": c["name"],
                "handle": c["handle"],
                "category": c["category"],
                "title": v["title"],
                "views": v["views"],
                "views_raw": v["views_raw"],
                "published": v["published"]
            })
    all_videos_flat.sort(key=lambda x: x["views"], reverse=True)
    top_15_videos = all_videos_flat[:15]

    report = {
        "summary": {
            "creators_analyzed": len(audit_results),
            "total_videos_sampled": total_videos_scraped,
            "total_views_recorded": total_views_scraped,
            "avg_views_across_platform": int(total_views_scraped / total_videos_scraped) if total_videos_scraped else 0
        },
        "category_performance": cat_stats,
        "top_creators_by_avg_views": [
            {
                "rank": i + 1,
                "name": c["name"],
                "handle": c["handle"],
                "category": c["category"],
                "avg_views": c["avg_views"],
                "subscribers": c["subscribers"]
            }
            for i, c in enumerate(audit_results[:15])
        ],
        "top_15_most_viewed_videos": top_15_videos,
        "detailed_creators": audit_results
    }
    
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    print(f"Audit Complete! {total_videos_scraped} videos scraped across {len(audit_results)} creators.")
    print(f"Total Views Sampled: {total_views_scraped:,}")

if __name__ == "__main__":
    main()
