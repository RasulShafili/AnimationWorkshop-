#!/usr/bin/env python3
"""
Multi-Platform Video Publisher (Instagram Reels + TikTok + YouTube Shorts)
Powered by Buffer GraphQL API. Automatically detects all connected channels
in the organization and publishes the video across every connected platform.
"""
import sys, os, re, json, requests

def _load_buffer_token():
    """The Buffer token is never stored in the repo: $BUFFER_TOKEN, or the git-ignored file .secrets/buffer_token."""
    import os
    tok = os.environ.get("BUFFER_TOKEN")
    if not tok:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".secrets", "buffer_token")
        if os.path.exists(path):
            tok = open(path).read().strip()
    if not tok:
        raise SystemExit("No Buffer token: set BUFFER_TOKEN or create .secrets/buffer_token")
    return tok


BUFFER_TOKEN = _load_buffer_token()
ORG_ID = "6ae5ed3ab180b26edaa4813d"
DEFAULT_IG_CHANNEL_ID = "6ae5ee322f1f5ed648315919"

HEADERS = {
    "Authorization": f"Bearer {BUFFER_TOKEN}",
    "Content-Type": "application/json"
}


def get_connected_channels():
    """Fetch all connected social channels (Instagram, TikTok, YouTube) in Buffer."""
    q = """
    query GetChannels($orgId: OrganizationId!) {
      channels(input: { organizationId: $orgId }) {
        id
        name
        service
        type
      }
    }
    """
    r = requests.post(
        "https://api.buffer.com",
        json={"query": q, "variables": {"orgId": ORG_ID}},
        headers=HEADERS,
        timeout=20
    )
    data = r.json()
    channels = data.get("data", {}).get("channels", [])
    if not channels:
        return [{"id": DEFAULT_IG_CHANNEL_ID, "name": "pixel_fact.8bit", "service": "instagram"}]
    return channels


def upload_video_temporarily(video_path: str) -> str:
    fname = os.path.basename(video_path)
    print(f"[*] Uploading video {fname} to fast temporary host...")

    # 1. Try Litterbox (Catbox 24h temporary direct MP4 CDN)
    try:
        with open(video_path, "rb") as f:
            r = requests.post(
                "https://litterbox.catbox.moe/resources/internals/api.php",
                data={"reqtype": "fileupload", "time": "24h"},
                files={"fileToUpload": (fname, f, "video/mp4")},
                timeout=90
            )
        if r.status_code == 200 and r.text.strip().startswith("https://"):
            url = r.text.strip()
            print(f"[+] Public video URL (Litterbox CDN): {url}")
            return url
    except Exception as e:
        print(f"[!] Litterbox fallback notice: {e}")

    # 2. Try Catbox direct CDN
    try:
        with open(video_path, "rb") as f:
            r = requests.post(
                "https://catbox.moe/user/api.php",
                data={"reqtype": "fileupload"},
                files={"fileToUpload": (fname, f, "video/mp4")},
                timeout=90
            )
        if r.status_code == 200 and r.text.strip().startswith("https://"):
            url = r.text.strip()
            print(f"[+] Public video URL (Catbox CDN): {url}")
            return url
    except Exception as e:
        print(f"[!] Catbox fallback notice: {e}")

    # 3. Try Uguu.se
    try:
        with open(video_path, "rb") as f:
            r = requests.post(
                "https://uguu.se/upload.php",
                files={"files[]": (fname, f, "video/mp4")},
                timeout=90
            )
        if r.status_code == 200:
            data = r.json()
            url = data["files"][0]["url"]
            print(f"[+] Public video URL (Uguu CDN): {url}")
            return url
    except Exception as e:
        print(f"[!] Uguu fallback notice: {e}")

    # 4. Try tmpfiles.org (convert /dl/ link)
    with open(video_path, "rb") as f:
        r = requests.post(
            "https://tmpfiles.org/api/v1/upload",
            files={"file": (fname, f, "video/mp4")},
            timeout=90
        )
    if r.status_code == 200:
        raw_url = r.json().get("data", {}).get("url", "")
        if "tmpfiles.org/" in raw_url:
            url = raw_url.replace("http://", "https://").replace("tmpfiles.org/", "tmpfiles.org/dl/")
            print(f"[+] Public video URL (Tmpfiles CDN): {url}")
            return url

    raise RuntimeError(f"All temporary video upload hosts failed (last status: {r.status_code})")


def build_metadata_block(service: str, title_line: str) -> str:
    """Build the platform-specific GraphQL metadata block for Instagram, TikTok, or YouTube Shorts."""
    clean_title = title_line.strip()
    if len(clean_title) > 90:
        clean_title = clean_title[:87] + "..."

    if service == "instagram":
        return """
        metadata: {
          instagram: {
            type: reel
            shouldShareToFeed: true
            isAiGenerated: false
          }
        }
        """
    elif service == "tiktok":
        escaped_title = json.dumps(clean_title)
        return f"""
        metadata: {{
          tiktok: {{
            title: {escaped_title}
            isAiGenerated: false
          }}
        }}
        """
    elif service == "youtube":
        yt_title = clean_title if "#shorts" in clean_title.lower() else f"{clean_title} #Shorts"
        if len(yt_title) > 100:
            yt_title = yt_title[:100]
        escaped_yt_title = json.dumps(yt_title)
        return f"""
        metadata: {{
          youtube: {{
            title: {escaped_yt_title}
            categoryId: "28"
            privacy: public
            madeForKids: false
            notifySubscribers: true
            embeddable: true
            isAiGenerated: false
          }}
        }}
        """
    return ""


def publish_reel(video_path: str, caption_path: str, share_now: bool = True):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    if not os.path.exists(caption_path):
        raise FileNotFoundError(f"Caption file not found: {caption_path}")

    with open(caption_path, "r", encoding="utf-8") as f:
        caption = f.read().strip()

    # Enforce maximum 5 hashtags rule
    hashtags = re.findall(r"#\w+", caption)
    if len(hashtags) > 5:
        print(f"[!] Warning: Found {len(hashtags)} hashtags. Truncating to strictly 5 hashtags.")
        for tag in hashtags[5:]:
            caption = re.sub(rf"{re.escape(tag)}\b", "", caption).strip()

    first_line = caption.splitlines()[0] if caption.splitlines() else "Learn With 8-Bit Science Fact!"
    video_url = upload_video_temporarily(video_path)
    mode = "shareNow" if share_now else "addToQueue"

    channels = get_connected_channels()
    supported = [c for c in channels if c.get("service") in ("instagram", "tiktok", "youtube")]

    print(f"[*] Detected {len(supported)} connected channel(s): " +
          ", ".join(f"{c['service'].upper()} ({c['name']})" for c in supported))

    escaped_caption = json.dumps(caption)
    published_posts = []

    for ch in supported:
        ch_id = ch["id"]
        ch_name = ch["name"]
        service = ch["service"]
        meta_block = build_metadata_block(service, first_line)

        print(f"[*] Dispatching to {service.upper()} channel '{ch_name}' (mode: {mode})...")

        q = f"""
        mutation {{
          createPost(input: {{
            channelId: "{ch_id}"
            text: {escaped_caption}
            mode: {mode}
            schedulingType: automatic
            needsApproval: false
            assets: [
              {{
                video: {{
                  url: "{video_url}"
                }}
              }}
            ]
            {meta_block}
          }}) {{
            __typename
            ... on PostActionSuccess {{
              post {{
                id
                status
                dueAt
              }}
            }}
            ... on InvalidInputError {{
              message
            }}
            ... on UnauthorizedError {{
              message
            }}
            ... on UnexpectedError {{
              message
            }}
            ... on LimitReachedError {{
              message
            }}
          }}
        }}
        """

        r = requests.post("https://api.buffer.com", json={"query": q}, headers=HEADERS, timeout=30)
        res_data = r.json()

        if "errors" in res_data:
            print(f"[ERROR] GraphQL error on {service} ({ch_name}): {json.dumps(res_data['errors'])}")
            continue

        result = res_data.get("data", {}).get("createPost", {})
        typename = result.get("__typename")

        if typename == "PostActionSuccess":
            post = result["post"]
            print(f"[SUCCESS] Video published to {service.upper()} ({ch_name})!")
            print(f"Post ID: {post['id']}")
            print(f"Status: {post['status']}")
            published_posts.append({"service": service, "channel": ch_name, "post": post})
        else:
            error_msg = result.get("message", "Unknown error")
            print(f"[ERROR] Failed on {service.upper()} ({ch_name}): {typename} - {error_msg}")

    if not published_posts:
        raise RuntimeError("Failed to publish video to any connected channel.")

    return published_posts


if __name__ == "__main__":
    if "--channels" in sys.argv:
        chs = get_connected_channels()
        print("Connected Buffer Channels:")
        for c in chs:
            print(f"  - {c['service'].upper()}: {c['name']} (ID: {c['id']})")
        sys.exit(0)

    if len(sys.argv) < 3:
        print("Usage: python3 publish_reel.py <video_path> <caption_path> [--now | --queue | --channels]")
        sys.exit(1)

    video = sys.argv[1]
    cap = sys.argv[2]
    now = "--queue" not in sys.argv

    try:
        publish_reel(video, cap, share_now=now)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
