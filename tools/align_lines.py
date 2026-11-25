"""exact word times per LINE (no drift, no whisper inventions between lines, script spelling).  tools/whisper-venv/bin/python tools/align_lines.py <dir> → <dir>/out/words.json
needs <dir>/lines.py (L), <dir>/vo16/*.wav, <dir>/out/global.json"""
import sys, os, re, json, difflib, subprocess, importlib.util, numpy as np
from faster_whisper import WhisperModel
D = os.path.abspath(sys.argv[1]); sp = importlib.util.spec_from_file_location("lines_al", f"{D}/lines.py"); M = importlib.util.module_from_spec(sp); sp.loader.exec_module(M); TX = {i: t for c, i, w, t in M.L}
G = json.load(open(f"{D}/out/global.json")); m = WhisperModel("small.en", device="cpu", compute_type="int8"); n = lambda s: re.sub(r"[^a-z0-9]", "", s.lower()); out = []; bad = []
for l in G["lines"]:
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f"{D}/vo16/{l['id']}.wav", "-ar", "16000", "-ac", "1", "-f", "f32le", "-"], capture_output=True).stdout, np.float32); du = len(a) / 16000
    e = np.sqrt(np.convolve(a ** 2, np.ones(320) / 320, "same")); on = np.where(e > .02)[0]; s0, s1 = (on[0] / 16000, on[-1] / 16000) if len(on) else (0, du)
    segs, _ = m.transcribe(a, word_timestamps=True, condition_on_previous_text=False, initial_prompt=None); ww = [(x.start, x.end, x.word.strip()) for s in segs for x in s.words]; sc = TX[l["id"]].split(); t = [None] * len(sc)
    sm = difflib.SequenceMatcher(None, [n(x) for x in sc], [n(x[2]) for x in ww], autojunk=False)
    for op, i0, i1, j0, j1 in sm.get_opcodes():
        if op == "equal":
            for k in range(i1 - i0): t[i0 + k] = [ww[j0 + k][0], ww[j0 + k][1]]
        elif op == "replace":                               # number etc.: share the span by letters
            a0, a1 = ww[j0][0], ww[j1 - 1][1]; L = sum(len(x) + 1 for x in sc[i0:i1]); p = a0
            for k in range(i0, i1): q = p + (a1 - a0) * (len(sc[k]) + 1) / L; t[k] = [p, q]; p = q
            if len(" ".join(sc[i0:i1])) > 4 and not any(c.isdigit() for x in ww[j0:j1] for c in x[2]): bad.append((l["id"], sc[i0:i1], [x[2] for x in ww[j0:j1]]))
        elif op == "delete": bad.append((l["id"], "MISSING", sc[i0:i1]))
        else: bad.append((l["id"], "EXTRA", [x[2] for x in ww[j0:j1]]))
    for k in range(len(t)):                                 # missing words: between neighbours
        if t[k] is None: p = t[k - 1][1] if k and t[k - 1] else s0; nx = next((x[0] for x in t[k + 1:] if x), s1); t[k] = [p, max(p + .08, nx)]
    t[0][0] = max(t[0][0], s0 - .03)
    for k in range(len(t)):
        if k and t[k][0] < t[k - 1][0] + .04: t[k][0] = t[k - 1][0] + .04
        t[k][1] = max(t[k][1], t[k][0] + .06); out.append([round(l["t0"] + t[k][0], 3), round(l["t0"] + t[k][1], 3), sc[k]])
json.dump(out, open(f"{D}/out/words.json", "w")); print(len(out), "words;", len(bad), "differences to look at:"); [print("  ", b) for b in bad]
