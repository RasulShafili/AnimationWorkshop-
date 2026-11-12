# quick look at the sim: projected density images (no matplotlib needed), written as one PNG via ffmpeg
import json, sys, subprocess, numpy as np
m = json.load(open('public/meta.json')); S, N = m['S'], m['N']
sn = np.fromfile('public/snaps.bin', dtype=np.int16).reshape(S, N, 3)
st = np.fromfile('public/stars.bin', dtype=np.float32).reshape(N, 5)
ts = [float(x) for x in sys.argv[1].split(',')]; W = 300
tiles = []
for t in ts:
    i = min(S - 1, int(round(t / m['dtSnap']))); p = sn[i] / m['QSCALE']; c = (np.array(m['cores'][i][0]) + np.array(m['cores'][i][1])) / 2
    img = np.zeros((W, W, 3))
    x = ((p[:, 0] - c[0]) / 10 + 0.5) * W; y = ((p[:, 2] - c[2]) / 10 + 0.5) * W
    ok = (x >= 0) & (x < W) & (y >= 0) & (y < W)
    np.add.at(img, (W - 1 - y[ok].astype(int), x[ok].astype(int)), st[ok, :3])
    img = np.clip(np.log1p(img * 2) / 2.5, 0, 1); tiles.append(img)
out = np.concatenate(tiles, 1); h, w, _ = out.shape
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w}x{h}', '-i', '-', sys.argv[2]], input=(out * 255).astype(np.uint8).tobytes())
print("seps", [round(m['sep'][min(S - 1, int(round(t / m['dtSnap'])))], 2) for t in ts])
