#!/usr/bin/env python3
"""Generate an image with Gemini (key read from ~/.config/watch/.env, never printed).
  python3 tools/gemini_image.py out.png "prompt" [ref1.jpg ref2.jpg …] [--model gemini-3.1-flash-image]"""
import sys, json, base64, urllib.request, mimetypes
args = sys.argv[1:]; model = "gemini-3.1-flash-image"
if "--model" in args: i = args.index("--model"); model = args[i + 1]; del args[i:i + 2]
out, prompt, refs = args[0], args[1], args[2:]
key = [l.split("=", 1)[1].strip().strip('"') for l in open("/home/rasul/.config/watch/.env") if l.startswith("GEMINI_API_KEY=")][-1]
parts = [{"inlineData": {"mimeType": mimetypes.guess_type(r)[0] or "image/jpeg", "data": base64.b64encode(open(r, "rb").read()).decode()}} for r in refs] + [{"text": prompt}]
body = {"contents": [{"parts": parts}], "generationConfig": {"responseModalities": ["IMAGE", "TEXT"], "imageConfig": {"aspectRatio": "16:9"}}}
req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent", data=json.dumps(body).encode(),
                             headers={"x-goog-api-key": key, "Content-Type": "application/json"})
try: d = json.load(urllib.request.urlopen(req, timeout=300))
except urllib.error.HTTPError as e: print("HTTP", e.code, e.read().decode()[:400]); sys.exit(1)
for c in d.get("candidates", []):
    for p in c.get("content", {}).get("parts", []):
        if "inlineData" in p: open(out, "wb").write(base64.b64decode(p["inlineData"]["data"])); print("saved", out); sys.exit(0)
        if "text" in p: print("model text:", p["text"][:300])
print("no image returned", json.dumps(d)[:300]); sys.exit(2)
