#!/usr/bin/env python3
import os, sys, json, time, datetime, subprocess

BASE_DIR = "/home/rasul/Desktop/Animations"
FINAL_VIDEOS_DIR = os.path.join(BASE_DIR, "Final videos")
MEMORY_DB_PATH = os.path.join(BASE_DIR, "memory_db.json")
TOPICS_PATH = os.path.join(BASE_DIR, "topics.json")
PUBLISH_SCRIPT = os.path.join(BASE_DIR, "publish_reel.py")

# Schedule time in Baku (UTC+4): STRICT 1 Reel per day at 20:00 (prevents Impression Cannibalization)
SCHEDULE_HOURS_BAKU = [20]

def load_memory_db():
    if not os.path.exists(MEMORY_DB_PATH):
        return {"processed_topics": [], "history": []}
    with open(MEMORY_DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory_db(db):
    with open(MEMORY_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)

def get_ready_queue():
    db = load_memory_db()
    processed = set(db.get("processed_topics", []))

    # Priority queue: 100% ORIGINAL 'LEARN WITH 8-BIT' Viral Science Videos (Zero Competitor Clones!)
    priority_order = [
        "nicotine-brain-hijack",
        "coffee-adenosine-blocker",
        "mosquito-6-needles",
        "phagocyte-eats-bacteria",
        "synapse-dopamine-spark",
        "blind-spot-glitch",
        "stomach-acid-razor",
        "brain-deletes-nose",
        "statue-of-liberty-rust",
        "ear-rumble-superpower"
    ]

    queue = []
    for topic_id in priority_order:
        if topic_id in processed:
            continue
        v_path = os.path.join(FINAL_VIDEOS_DIR, f"{topic_id}_v1.mp4")
        c_path = os.path.join(FINAL_VIDEOS_DIR, f"{topic_id}_caption.txt")
        if os.path.exists(v_path) and os.path.exists(c_path):
            queue.append({
                "id": topic_id,
                "video": v_path,
                "caption": c_path,
                "size_mb": round(os.path.getsize(v_path) / (1024 * 1024), 2)
            })

    return queue

def publish_next():
    queue = get_ready_queue()
    if not queue:
        print("[!] No ready videos found in queue.")
        return None

    item = queue[0]
    topic_id = item["id"]
    print(f"[*] Publishing next queued topic: {topic_id} ({item['size_mb']} MB)...")

    cmd = ["python3", PUBLISH_SCRIPT, item["video"], item["caption"], "--now"]
    res = subprocess.run(cmd, capture_output=True, text=True)

    print(res.stdout)
    if res.returncode != 0:
        print(f"[ERROR] Publishing failed:\n{res.stderr}", file=sys.stderr)
        return None

    # Parse post ID from output
    post_id = None
    for line in res.stdout.split("\n"):
        if "Post ID:" in line:
            post_id = line.split("Post ID:")[1].strip()

    # Update database
    db = load_memory_db()
    if topic_id not in db["processed_topics"]:
        db["processed_topics"].append(topic_id)

    now_utc = datetime.datetime.now(datetime.timezone.utc)
    pub_entry = {
        "id": topic_id,
        "title": open(item["caption"]).readline().strip(),
        "published_at": now_utc.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "channel": "pixel_fact.8bit",
        "post_id": post_id or "unknown",
        "status": "published"
    }
    db["history"].append(pub_entry)
    save_memory_db(db)

    print(f"[SUCCESS] Topic '{topic_id}' recorded in memory_db.json!")
    return pub_entry

def show_status():
    db = load_memory_db()
    queue = get_ready_queue()

    print("========================================")
    print("      PIXEL_FACT.8BIT AUTO PUBLISHER    ")
    print("========================================")
    print(f"Published Reels Count: {len(db.get('history', []))}")
    print("\nRecent Published History:")
    for h in db.get("history", [])[-5:]:
        print(f"  - [{h.get('published_at', '')}] {h.get('title', h.get('id'))}")
        if h.get("url"):
            print(f"    Link: {h.get('url')}")

    print("\nReady In-Queue for Publishing:")
    if queue:
        for idx, item in enumerate(queue, 1):
            print(f"  {idx}. {item['id']} ({item['size_mb']} MB)")
    else:
        print("  (Queue empty - all rendered videos are published)")

    now_utc = datetime.datetime.now(datetime.timezone.utc)
    now_baku = now_utc + datetime.timedelta(hours=4)
    print(f"\nCurrent Time (Baku): {now_baku.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Posting Window Schedule: 1 Reel / Day at 20:00 Baku Time (Anti-Cannibalization Mode)")
    print(f"Format Standard: 32.0s (960 frames @ 30fps) Single-Focus Center Text Standard")
    print("========================================")

if __name__ == "__main__":
    if "--publish-next" in sys.argv:
        publish_next()
    elif "--status" in sys.argv or len(sys.argv) == 1:
        show_status()
    else:
        print("Usage: python3 auto_publisher.py [--status | --publish-next]")
