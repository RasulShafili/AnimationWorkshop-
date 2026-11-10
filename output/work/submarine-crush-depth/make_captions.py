import json, re

with open("audio/words.json") as f:
    words = json.load(f)

FPS = 30
HIGHLIGHT_TERMS = {
    "submarine", "dives", "crush", "depth", "meters", "abyss", "hydrostatic",
    "pressure", "atmosphere", "kilograms", "steel", "hull", "groan", "rivets",
    "implosion", "milliseconds", "adiabatic", "vaporizing", "relentless", "explore",
    "submersible"
}

chunks = []
current_chunk = []
current_sentence = None

for w in words:
    s_idx = w.get("sentence_idx", 0)
    if current_sentence is None:
        current_sentence = s_idx
    
    # break chunk if sentence changes or chunk len >= 3
    if s_idx != current_sentence or len(current_chunk) >= 3:
        if current_chunk:
            chunks.append(current_chunk)
            current_chunk = []
        current_sentence = s_idx
    
    current_chunk.append(w)

if current_chunk:
    chunks.append(current_chunk)

captions = []
cap_id = 1
for chunk in chunks:
    clean_words = [re.sub(r'^[^\w]+|[^\w]+$', '', c["word"]) for c in chunk]
    # Find yellow word index
    yellow_idx = -1
    for i, w_str in enumerate(clean_words):
        if w_str.lower() in HIGHLIGHT_TERMS:
            yellow_idx = i
            break
    
    start_t = chunk[0]["start"]
    end_t = chunk[-1]["end"]
    start_frame = int(round(start_t * FPS))
    end_frame = int(round(end_t * FPS))
    if end_frame <= start_frame:
        end_frame = start_frame + 1

    captions.append({
        "id": cap_id,
        "words": [c["word"] for c in chunk],
        "yellowWordIndex": yellow_idx,
        "startTime": start_t,
        "endTime": end_t,
        "startFrame": start_frame,
        "endFrame": end_frame
    })
    cap_id += 1

with open("src/captions.json", "w") as f:
    json.dump(captions, f, indent=2)

print(f"Generated {len(captions)} captions successfully for Submarine Crush Depth.")
