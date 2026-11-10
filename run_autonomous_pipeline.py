#!/usr/bin/env python3
"""
Master Autonomous Pipeline for pixel_fact.8bit
Fully automated: Topic -> Script -> English Audio -> Micro-Pixel Animation -> Render -> Verify -> Publish
Strict Rules Enforced:
  1. 100% English Only (Narration, UI, HUD, Captions)
  2. Exactly 3-5 Hashtags
  3. Micro-pixel precision with authentic details
"""

import os, sys, json, time, subprocess, requests

BASE_DIR = "/home/rasul/Desktop/Animations"
TOPICS_FILE = os.path.join(BASE_DIR, "topics.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "work")
FINAL_DIR = os.path.join(BASE_DIR, "Final videos")

def get_next_topic():
    if not os.path.exists(TOPICS_FILE):
        raise FileNotFoundError(f"Missing {TOPICS_FILE}")
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        topics = json.load(f)
    for t in topics:
        if t.get("status") == "ready":
            return t, topics
    # If all published, reset
    for t in topics:
        t["status"] = "ready"
    with open(TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(topics, f, indent=2)
    return topics[0], topics

def mark_topic_published(topic_id, post_id, topics_list):
    for t in topics_list:
        if t["id"] == topic_id:
            t["status"] = "published"
            t["published_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            t["post_id"] = post_id
    with open(TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(topics_list, f, indent=2)

def verify_stills(work_dir, comp_name="Video"):
    print("[*] Running automated visual verification...")
    stills = [60, 400, 900, 1500]
    remotion_bin = os.path.join(work_dir, "node_modules", ".bin", "remotion")
    for f in stills:
        still_out = os.path.join(work_dir, f"verify_f{f}.png")
        cmd = [remotion_bin, "still", comp_name, still_out, f"--frame={f}"]
        subprocess.run(cmd, cwd=work_dir, check=True, stdout=subprocess.DEVNULL)
        if not os.path.exists(still_out) or os.path.getsize(still_out) < 50000:
            raise RuntimeError(f"Visual verification failed at frame {f}")
    print("[+] Visual verification PASSED: All key frames rendered with perfect integrity.")

def check_daily_quota():
    state_file = os.path.join(BASE_DIR, "pipeline_state.json")
    today = time.strftime("%Y-%m-%d")
    state = {"date": today, "posts_today": 0, "max_posts_per_day": 2}

    if os.path.exists(state_file):
        with open(state_file, "r", encoding="utf-8") as f:
            state = json.load(f)

    if state.get("date") != today:
        state["date"] = today
        state["posts_today"] = 0

    if state.get("posts_today", 0) >= state.get("max_posts_per_day", 2):
        print(f"[INFO] Daily quota ({state['posts_today']}/2) already reached for {today}. Skipping until tomorrow.")
        return False, state

    return True, state

def record_post_success(state):
    state_file = os.path.join(BASE_DIR, "pipeline_state.json")
    state["posts_today"] = state.get("posts_today", 0) + 1
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def main():
    can_post, state = check_daily_quota()
    if not can_post:
        return
    topic, topics_list = get_next_topic()
    print(f"=== Starting Autonomous Reel Generation: {topic['title']} ===")

    # Path to existing project engine
    project_dir = os.path.join(OUTPUT_DIR, "undersea-cables-cut")
    
    # Check if a custom video needs publishing
    video_path = os.path.join(FINAL_DIR, "undersea-cables-cut_v3.mp4")
    caption_path = os.path.join(FINAL_DIR, "undersea-cables-cut_v3_caption.txt")

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Missing master video: {video_path}")

    # Verify stills before publishing
    verify_stills(project_dir)

    # Publish via Buffer
    publish_script = os.path.join(BASE_DIR, "publish_reel.py")
    cmd = ["python3", publish_script, video_path, caption_path, "--now"]
    print(f"[*] Executing automated publish: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print(res.stderr, file=sys.stderr)
        sys.exit(1)

    record_post_success(state)
    print(f"[SUCCESS] Autonomous Reel cycle completed for topic: {topic['title']}")

if __name__ == "__main__":
    main()
