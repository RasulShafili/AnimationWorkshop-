#!/usr/bin/env python3
"""Share one finished video to YouTube + Instagram + TikTok right now via Buffer, then record it in memory_db.json.

Usage: python3 share_video.py <topic-id> <video.mp4> <caption.txt> [services]
  services: comma list, default "youtube,instagram,tiktok". Give a subset (e.g. "tiktok") to add a platform
  to a topic that was already posted elsewhere; it is then appended to that topic's history entry.

Why not publish_reel.py: Litterbox returns 403 from this machine and Buffer cannot read Catbox links
(Catbox answers HEAD with content-length 0). Uguu works, but its links expire within hours, so this
script always uploads and posts in one go.
"""
import datetime, json, os, sys
import requests
import publish_reel as p

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "memory_db.json")


ALL = ("youtube", "instagram", "tiktok")


def main(topic, video, cap, services=",".join(ALL)):
    want = [x.strip() for x in services.split(",") if x.strip()]
    adding = set(want) != set(ALL)
    caption = open(cap, encoding="utf-8").read().strip()
    first = caption.splitlines()[0]
    db = json.load(open(DB, encoding="utf-8"))
    if topic in db.get("processed_topics", []) and not adding:
        sys.exit(f"[STOP] {topic} is already in memory_db.json; not posting twice.")

    chans = [c for c in p.get_connected_channels() if c["service"] in want]
    if len(chans) != len(want):
        sys.exit(f"[STOP] expected {want}, got {[c['service'] for c in chans]}")

    with open(video, "rb") as f:
        r = requests.post("https://uguu.se/upload.php", files={"files[]": (os.path.basename(video), f, "video/mp4")}, timeout=240)
    url = r.json()["files"][0]["url"]
    size = int(requests.head(url, allow_redirects=True, timeout=30).headers.get("content-length", 0))
    print("uploaded:", url, size, "bytes")
    if size < 1_000_000:
        sys.exit("[STOP] host reports an empty file; Buffer would reject it.")

    done = []
    for c in chans:
        q = f"""mutation {{ createPost(input: {{
          channelId: "{c['id']}" text: {json.dumps(caption)} mode: shareNow
          schedulingType: automatic needsApproval: false
          assets: [{{ video: {{ url: "{url}" }} }}]
          {p.build_metadata_block(c['service'], first)}
        }}) {{ __typename ... on PostActionSuccess {{ post {{ id status }} }}
          ... on InvalidInputError {{ message }} ... on UnauthorizedError {{ message }}
          ... on UnexpectedError {{ message }} ... on LimitReachedError {{ message }} }} }}"""
        res = requests.post("https://api.buffer.com", json={"query": q}, headers=p.HEADERS, timeout=60).json()
        out = (res.get("data") or {}).get("createPost") or res.get("errors")
        print(c["service"].upper(), c["name"], "->", json.dumps(out))
        if isinstance(out, dict) and out.get("__typename") == "PostActionSuccess":
            done.append({"service": c["service"], "name": c["name"], "post_id": out["post"]["id"]})

    if not done:
        sys.exit("[FAIL] nothing was posted.")
    # Buffer answers "sending" at once; the real result (sent / error) comes later. Poll it so a failure is never missed.
    import time
    pending = {d["post_id"]: d for d in done}
    for _ in range(12):
        time.sleep(10)
        for pid, d in list(pending.items()):
            q = 'query { post(input: { id: "%s" }) { status error { message } externalLink } }' % pid
            st = (requests.post("https://api.buffer.com", json={"query": q}, headers=p.HEADERS, timeout=30).json().get("data") or {}).get("post") or {}
            if st.get("status") == "sent":
                print(f"[SENT] {d['service']}: {st.get('externalLink')}"); pending.pop(pid)
            elif st.get("status") == "error":
                msg = (st.get("error") or {}).get("message")
                print(f"[ERROR] {d['service']}: {msg}"); d["status"] = f"error: {msg}"; pending.pop(pid)
        if not pending: break
    for d in pending.values(): print(f"[?] {d['service']}: still sending after 2 min — check Buffer")
    done_ok = [d for d in done if not d.get("status", "").startswith("error")]
    db = json.load(open(DB, encoding="utf-8"))
    old = next((h for h in db["history"] if h["id"] == topic), None)
    if old is not None:
        old["channels"] += done
        json.dump(db, open(DB, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"[OK] posted to {len(done)}/{len(want)} channels, added to {topic} in memory_db.json"); return
    db["processed_topics"].append(topic)
    db["history"].append({
        "id": topic, "title": first,
        "published_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "channels": done, "status": "published" if len(done_ok) == len(want) else "partial",
    })
    json.dump(db, open(DB, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"[OK] posted to {len(done)}/{len(want)} channels and recorded {topic} in memory_db.json")


if __name__ == "__main__":
    if len(sys.argv) not in (4, 5):
        sys.exit(__doc__)
    main(*sys.argv[1:])
