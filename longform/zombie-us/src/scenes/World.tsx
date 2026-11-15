// Day 1 locations: the Cole family kitchen, the West Texas ranch + barn + bat, the nerve/virus micro insert,
// Atlanta airport (terminal, departures board, gate B12), plane take-off, and the US map with the spread.
import React from "react";
import { rnd, sat, ease, lerp, W, H } from "../engine/core";
import { Glow, Shaft, Bokeh } from "../engine/fx";
import { Noise, AO, Wood, Wallpaper } from "../engine/tex";
import { Character, Pose } from "../chars/Rig2";
import { EXTRAS, RANCHER, GUARD } from "../chars/cast";

// ---------- kitchen, morning ----------
export const Kitchen: React.FC<{ f: number; children?: React.ReactNode; tv?: number }> = ({ f, children, tv = 1 }) => <g>
  <Wallpaper x={-600} y={-200} w={3200} h={900} base="#e8d8b8" ink="#c8a878" kind="stripe" o={0.22} />
  {/* window with morning sun */}
  <g transform="translate(1180 140)"><rect x={0} y={0} width={420} height={330} fill="#bfe2ff" /><rect x={0} y={200} width={420} height={130} fill="#9ac88a" /><circle cx={330} cy={80} r={46} fill="#fff6c8" />
    {[[60, 220, 60], [180, 210, 80], [300, 230, 50]].map(([x, y, r], i) => <circle key={i} cx={x} cy={y} r={r} fill="#6aa86a" />)}
    <rect x={-14} y={-14} width={448} height={358} fill="none" stroke="#f4f1e8" strokeWidth={22} /><line x1={210} y1={0} x2={210} y2={330} stroke="#f4f1e8" strokeWidth={12} /><line x1={0} y1={165} x2={420} y2={165} stroke="#f4f1e8" strokeWidth={12} />
    <path d="M-40 -30 L120 -30 L60 360 L-40 360 Z" fill="#e86a4a" opacity={0.85} /><path d="M460 -30 L300 -30 L360 360 L460 360 Z" fill="#e86a4a" opacity={0.85} /></g>
  <Shaft pts={[[1180, 140], [1600, 140], [1300, 1000], [700, 1000]]} color="#fff2c0" o={0.3} />
  {/* cabinets + counter */}
  <rect x={-200} y={120} width={1240} height={220} fill="#f4efe2" />{[0, 1, 2, 3].map(i => <g key={i}><rect x={-180 + i * 300} y={136} width={280} height={190} rx={6} fill="#fbf7ec" stroke="#d8d0bc" strokeWidth={3} /><rect x={-60 + i * 300} y={290} width={40} height={8} rx={3} fill="#b8b0a0" /></g>)}
  <rect x={-200} y={520} width={1920} height={30} fill="#c8b89a" /><rect x={-200} y={550} width={1920} height={230} fill="#f4efe2" />{[0, 1, 2, 3, 4, 5].map(i => <rect key={i} x={-180 + i * 320} y={566} width={300} height={200} rx={6} fill="#fbf7ec" stroke="#d8d0bc" strokeWidth={3} />)}
  {/* coffee machine, toaster, fridge */}
  <rect x={120} y={430} width={90} height={90} rx={8} fill="#2a2a30" /><rect x={140} y={490} width={50} height={30} fill="#f4f1e8" /><rect x={380} y={470} width={120} height={50} rx={10} fill="#d8dce2" />
  <g transform="translate(1720 120)"><rect x={0} y={0} width={300} height={660} rx={14} fill="#e8ecf0" /><line x1={0} y1={240} x2={300} y2={240} stroke="#b8bec6" strokeWidth={4} /><rect x={24} y={120} width={12} height={90} rx={5} fill="#a8aeb8" /><rect x={24} y={280} width={12} height={120} rx={5} fill="#a8aeb8" />
    <rect x={120} y={60} width={110} height={80} fill="#fff6a8" transform="rotate(4 175 100)" /><text x={175} y={96} textAnchor="middle" fontFamily="Permanent Marker" fontSize={18} fill="#2a2a8a" transform="rotate(4 175 100)">KAI —</text><text x={175} y={120} textAnchor="middle" fontFamily="Permanent Marker" fontSize={14} fill="#2a2a8a" transform="rotate(4 175 100)">NIGHT 10PM</text>
    <rect x={60} y={300} width={90} height={70} fill="#f4f4f4" transform="rotate(-6 105 335)" /><path d="M75 350 l15 -25 l15 15 l15 -20 l20 30 Z" fill="#4a9ad8" transform="rotate(-6 105 335)" /></g>
  {/* small TV on the counter */}
  <g transform="translate(640 380)"><rect x={0} y={0} width={240} height={150} rx={8} fill="#1a1a20" /><rect x={10} y={10} width={220} height={120} fill={tv ? "#2a4a7a" : "#111"} />
    {tv > 0 && <><rect x={10} y={100} width={220} height={30} fill="#c8282a" /><text x={120} y={121} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={13} fill="#fff">MYSTERY ILLNESS · W. TEXAS</text><circle cx={60} cy={60} r={26} fill="#24212f" /><rect x={40} y={86} width={40} height={20} fill="#3a4a6a" /><rect x={110} y={30} width={100} height={60} fill="#c8a86a" opacity={0.6} /></>}
    <rect x={100} y={150} width={40} height={40} fill="#1a1a20" /></g>
  {/* floor + table */}
  <rect x={-600} y={780} width={3200} height={600} fill="#a8805a" /><Wood x={-600} y={780} w={3200} h={600} color="#b08a5e" rows={6} />
  <AO x={-600} y={780} w={3200} h={50} dir="down" o={0.35} />
  {children}
</g>;
export const KitchenTable: React.FC<{ x: number; y: number }> = ({ x, y }) => <g transform={`translate(${x} ${y})`}>
  <rect x={-260} y={-16} width={520} height={26} rx={6} fill="#8a5e3a" /><rect x={-230} y={10} width={18} height={150} fill="#6a4628" /><rect x={212} y={10} width={18} height={150} fill="#6a4628" />
  <ellipse cx={-80} cy={-22} rx={50} ry={10} fill="#f4f4f4" /><ellipse cx={-80} cy={-26} rx={34} ry={7} fill="#e8b85a" /><rect x={60} y={-56} width={40} height={40} rx={6} fill="#f4f1e8" /><rect x={130} y={-80} width={60} height={64} fill="#e8742a" /><text x={160} y={-44} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={12} fill="#fff">OATS</text>
</g>;

// ---------- West Texas ranch, dawn ----------
export const Ranch: React.FC<{ f: number; children?: React.ReactNode; inside?: boolean }> = ({ f, children, inside }) => inside ? <g>
  {/* barn interior: plank walls, light beams through gaps, hay, a beam with the bat */}
  <rect x={-600} y={-200} width={3200} height={1500} fill="#3a2418" />
  {Array.from({ length: 30 }, (_, i) => <rect key={i} x={-600 + i * 110} y={-200} width={104} height={1100} fill={i % 2 ? "#5a3622" : "#4e2e1c"} />)}
  {Array.from({ length: 8 }, (_, i) => <Shaft key={i} pts={[[i * 280 - 100, 0], [i * 280 - 92, 0], [i * 280 + 260, 900], [i * 280 + 200, 900]]} color="#ffcf8a" o={0.25} blur={8} />)}
  <rect x={-600} y={180} width={3200} height={46} fill="#2a1a10" /><rect x={-600} y={180} width={3200} height={8} fill="#8a5a36" />
  <rect x={-600} y={820} width={3200} height={600} fill="#6a4a28" />{Array.from({ length: 60 }, (_, i) => <line key={i} x1={-600 + rnd(i, 1) * 3200} y1={820 + rnd(i, 2) * 300} x2={-600 + rnd(i, 1) * 3200 + 30} y2={820 + rnd(i, 2) * 300 - 8} stroke="#d8b060" strokeWidth={3} opacity={0.5} />)}
  <g transform="translate(1500 820)"><rect x={-160} y={-170} width={320} height={170} rx={20} fill="#d8a84a" /><rect x={-160} y={-170} width={320} height={170} rx={20} fill="url(#none)" />{Array.from({ length: 14 }, (_, i) => <line key={i} x1={-150 + i * 22} y1={-160} x2={-140 + i * 22} y2={-10} stroke="#b8862a" strokeWidth={3} />)}</g>
  <Noise x={-600} y={-200} w={3200} h={1500} freq={0.5} o={0.25} />
  {children}
</g> : <g>
  {/* exterior: dawn sky gradient, mesas, windmill, red barn, fence */}
  <defs><linearGradient id="dawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#3a4a8a" /><stop offset="0.5" stopColor="#e8946a" /><stop offset="1" stopColor="#ffd08a" /></linearGradient></defs>
  <rect x={-600} y={-200} width={3200} height={900} fill="url(#dawn)" /><circle cx={1500} cy={640} r={90} fill="#fff0b8" /><Glow x={1500} y={640} r={500} color="#ffb860" o={0.5} />
  <path d="M-600 640 L-200 640 L-160 560 L200 560 L240 640 L900 640 L940 590 L1180 590 L1210 640 L2600 640 L2600 700 L-600 700 Z" fill="#a8604a" />
  <rect x={-600} y={660} width={3200} height={700} fill="#c89a5a" />{Array.from({ length: 50 }, (_, i) => <ellipse key={i} cx={-600 + rnd(i, 3) * 3200} cy={700 + rnd(i, 4) * 500} rx={20 + rnd(i, 5) * 30} ry={6} fill="#8a6a3a" opacity={0.4} />)}
  {/* windmill */}
  <g transform="translate(300 700)"><path d="M-40 0 L-6 -420 L6 -420 L40 0" stroke="#5a4a3a" strokeWidth={8} fill="none" /><path d="M-30 -120 L30 -120 M-20 -260 L20 -260" stroke="#5a4a3a" strokeWidth={6} />
    <g transform={`translate(0 -430) rotate(${f * 2})`}>{Array.from({ length: 12 }, (_, i) => <path key={i} d="M0 0 L-10 -110 L10 -110 Z" fill="#8a8070" transform={`rotate(${i * 30})`} />)}<circle r={14} fill="#5a4a3a" /></g></g>
  {/* barn */}
  <g transform="translate(1080 720)"><path d="M-300 0 L-300 -300 L0 -460 L300 -300 L300 0 Z" fill="#b8322a" /><path d="M-320 -300 L0 -480 L320 -300" stroke="#f4efe2" strokeWidth={22} fill="none" />
    <rect x={-120} y={-260} width={240} height={260} fill="#7a1e18" /><path d="M-120 -260 L120 0 M120 -260 L-120 0" stroke="#f4efe2" strokeWidth={12} /><rect x={-124} y={-264} width={248} height={268} fill="none" stroke="#f4efe2" strokeWidth={12} />
    <rect x={-40} y={-400} width={80} height={70} fill="#2a1410" /><path d="M-300 -300 L-300 0" stroke="#7a1e18" strokeWidth={10} /></g>
  {/* fence */}
  {Array.from({ length: 22 }, (_, i) => <rect key={i} x={-500 + i * 150} y={760} width={14} height={110} fill="#6a4a2a" />)}
  <rect x={-600} y={780} width={3200} height={10} fill="#7a5a3a" /><rect x={-600} y={820} width={3200} height={10} fill="#7a5a3a" />
  {children}
</g>;
export const Bat: React.FC<{ x: number; y: number; s?: number; f: number; flap?: number; sick?: boolean }> = ({ x, y, s = 1, f, flap = 0, sick = true }) => {
  const w = flap ? Math.sin(f * 0.9) * 40 : 0;
  return <g transform={`translate(${x} ${y}) scale(${s})`}>
    {/* hanging upside down from the beam unless flapping */}
    <g transform={flap ? "" : "rotate(180)"}>
      <path d={`M0 0 Q-60 ${-30 - w} -120 ${-10 - w} Q-100 10 -90 30 Q-70 14 -56 34 Q-40 18 -20 30 Z`} fill="#2a2228" />
      <path d={`M0 0 Q60 ${-30 - w} 120 ${-10 - w} Q100 10 90 30 Q70 14 56 34 Q40 18 20 30 Z`} fill="#2a2228" />
      <ellipse cx={0} cy={10} rx={24} ry={32} fill="#3a2e34" /><circle cx={0} cy={-26} r={20} fill="#3a2e34" /><path d="M-16 -40 L-10 -62 L-2 -42 M16 -40 L10 -62 L2 -42" fill="#3a2e34" />
      <circle cx={-7} cy={-28} r={4} fill={sick ? "#e8ffd0" : "#111"} /><circle cx={7} cy={-28} r={4} fill={sick ? "#e8ffd0" : "#111"} />{sick && <Glow x={0} y={-28} r={30} color="#c8ffb0" o={0.4} />}
      <path d="M-5 -16 L-3 -10 M5 -16 L3 -10" stroke="#fff" strokeWidth={2.5} />
    </g>
  </g>;
};
// micro insert: a glowing nerve fibre with bullet-shaped virions crawling toward the brain (top-right)
export const NerveMicro: React.FC<{ f: number; k?: number }> = ({ f, k = 1 }) => <svg width={W} height={H} style={{ position: "absolute" }}>
  <defs><radialGradient id="mic" cx="0.5" cy="0.5" r="0.7"><stop offset="0" stopColor="#1a2a3a" /><stop offset="1" stopColor="#05080e" /></radialGradient></defs>
  <rect width={W} height={H} fill="url(#mic)" />
  {Array.from({ length: 40 }, (_, i) => <circle key={i} cx={rnd(i, 1) * W} cy={rnd(i, 2) * H} r={4 + rnd(i, 3) * 18} fill="#4a7a9a" opacity={0.08} />)}
  <path id="nv" d="M-100 900 C 400 820, 600 600, 1000 560 S 1600 300, 2050 120" stroke="#e8b86a" strokeWidth={70} fill="none" opacity={0.35} />
  <path d="M-100 900 C 400 820, 600 600, 1000 560 S 1600 300, 2050 120" stroke="#ffd88a" strokeWidth={26} fill="none" opacity={0.6} />
  <path d="M-100 900 C 400 820, 600 600, 1000 560 S 1600 300, 2050 120" stroke="#fff2c8" strokeWidth={6} fill="none" strokeDasharray="30 60" strokeDashoffset={-f * 6} opacity={0.8} />
  {Array.from({ length: 14 }, (_, i) => { const u = ((f * 0.004 * k + i / 14) % 1); const t = u; const bx = lerp(-100, 2050, t), by = 900 - 780 * Math.pow(t, 1.2) + Math.sin(t * 9) * 60;
    return <g key={i} transform={`translate(${bx} ${by}) rotate(${-25 - t * 10})`}><rect x={-34} y={-13} width={60} height={26} rx={13} fill="#7ad86a" /><path d="M26 -13 L40 0 L26 13 Z" fill="#7ad86a" />{[-24, -12, 0, 12].map(s => <line key={s} x1={s} y1={-13} x2={s} y2={13} stroke="#3a8a3a" strokeWidth={3} />)}<Glow x={0} y={0} r={50} color="#a8ff8a" o={0.35} /></g>; })}
  <text x={1840} y={90} textAnchor="end" fontFamily="Inter" fontWeight={900} fontSize={34} fill="#ffd88a" letterSpacing={6}>→ BRAIN</text>
  <text x={80} y={1010} fontFamily="Inter" fontWeight={800} fontSize={28} fill="#8ab0c8" letterSpacing={4}>NERVE FIBRE · ×40,000</text>
</svg>;

// ---------- Atlanta airport ----------
export const Terminal: React.FC<{ f: number; children?: React.ReactNode; crowd?: number; gate?: string; panic?: number }> = ({ f, children, crowd = 14, gate = "B12", panic = 0 }) => <g>
  <rect x={-600} y={-200} width={3200} height={1500} fill="#c8d2da" />
  {/* glass wall with planes outside */}
  <rect x={-600} y={60} width={3200} height={560} fill="#9ec8e8" />
  <rect x={-600} y={420} width={3200} height={200} fill="#8a9aa4" />
  {[[-200, 380], [900, 400], [1900, 370]].map(([px, py], i) => <g key={i} transform={`translate(${px} ${py}) scale(${0.9 + i * 0.1})`}><path d="M0 0 L520 0 Q580 0 600 30 L520 50 L0 50 Q-30 25 0 0 Z" fill="#f4f6f8" /><path d="M200 30 L330 120 L380 120 L300 30 Z" fill="#d8dee4" /><path d="M10 0 L-30 -90 L20 -90 L80 0 Z" fill="#2f6ad8" /><rect x={120} y={14} width={360} height={10} fill="#2f6ad8" opacity={0.5} />{Array.from({ length: 14 }, (_, k) => <circle key={k} cx={140 + k * 24} cy={20} r={5} fill="#3a4a5a" />)}</g>)}
  {Array.from({ length: 12 }, (_, i) => <rect key={i} x={-560 + i * 300} y={60} width={16} height={560} fill="#5a6470" />)}
  <rect x={-600} y={40} width={3200} height={30} fill="#5a6470" /><rect x={-600} y={610} width={3200} height={20} fill="#5a6470" />
  {Array.from({ length: 6 }, (_, i) => <path key={i} d={`M${-400 + i * 560} 70 l120 0 l-200 540 l-120 0 Z`} fill="#fff" opacity={0.08} />)}
  {/* gate sign */}
  <g transform="translate(400 120)"><rect x={0} y={0} width={300} height={110} rx={10} fill="#1a2a4a" /><text x={40} y={78} fontFamily="Inter" fontWeight={900} fontSize={64} fill="#ffd34a">{gate}</text><text x={190} y={50} fontFamily="Inter" fontWeight={800} fontSize={20} fill="#fff">GATE</text><path d="M200 70 l40 0 m-14 -14 l14 14 l-14 14" stroke="#fff" strokeWidth={5} fill="none" /></g>
  {/* floor */}
  <rect x={-600} y={630} width={3200} height={700} fill="#e4e0d8" />{Array.from({ length: 30 }, (_, i) => <line key={i} x1={-600 + i * 130} y1={630} x2={-1200 + i * 180} y2={1300} stroke="#000" strokeOpacity={0.06} strokeWidth={3} />)}
  <rect x={-600} y={640} width={3200} height={100} fill="#fff" opacity={0.25} />
  {/* seat rows */}
  {[-300, 1500].map((sx, k) => <g key={k}>{Array.from({ length: 6 }, (_, i) => <g key={i}><rect x={sx + i * 70} y={700} width={60} height={70} rx={10} fill="#3a4a6a" /><rect x={sx + i * 70} y={760} width={60} height={20} rx={4} fill="#2a3a5a" /></g>)}<rect x={sx} y={780} width={420} height={10} fill="#8a8a94" /></g>)}
  {/* travellers */}
  {Array.from({ length: crowd }, (_, i) => { const dir = rnd(i, 5) > 0.5 ? 1 : -1, sp = panic ? 9 : 2.2, x = -400 + ((rnd(i, 6) * 2800 + f * sp * dir) % 2800 + 2800) % 2800 - 200, ph = (x * dir) / 60;
    const s = 0.62 + rnd(i, 7) * 0.12, y = 860 + rnd(i, 8) * 120;
    return { i, el: <Character key={i} look={{ ...EXTRAS[i % EXTRAS.length], backpack: i % 3 === 0 ? "#4a5a6a" : undefined }} pose={{ facing: dir as 1 | -1, ...(panic ? { lean: 12, aL: [-50 * Math.sin(ph), 80], aR: [50 * Math.sin(ph), 80], lL: [40 * Math.sin(ph), 50], lR: [-40 * Math.sin(ph), 50], mouth: "o" } : { aL: [-20 * Math.sin(ph), 14], aR: [20 * Math.sin(ph), 14], lL: [22 * Math.sin(ph), 18], lR: [-22 * Math.sin(ph), 18] }) }} x={x} y={y} s={s} f={f} seed={i + 3} />, y };
  }).sort((a, b) => a.y - b.y).map(o => o.el)}
  {children}
</g>;
// departures board insert (diegetic text), one row highlighted
export const DepBoard: React.FC<{ f: number; rows: string[][]; hi?: number; title?: string }> = ({ f, rows, hi = -1, title = "DEPARTURES" }) => <svg width={W} height={H} style={{ position: "absolute" }}>
  <rect width={W} height={H} fill="#0c1220" /><rect x={160} y={110} width={1600} height={860} rx={20} fill="#05080e" stroke="#2a3446" strokeWidth={10} />
  <text x={220} y={200} fontFamily="Inter" fontWeight={900} fontSize={54} fill="#ffd34a" letterSpacing={8}>✈ {title}</text>
  {["TIME", "TO", "FLIGHT", "GATE", "STATUS"].map((h, i) => <text key={h} x={[220, 420, 900, 1180, 1400][i]} y={280} fontFamily="Inter" fontWeight={800} fontSize={26} fill="#6a7a94" letterSpacing={4}>{h}</text>)}
  {rows.map((r, j) => <g key={j}>{j === hi && <rect x={190} y={310 + j * 84} width={1540} height={72} fill="#ffd34a" opacity={0.15 + 0.1 * Math.sin(f * 0.3)} />}
    {r.map((c, i) => <text key={i} x={[220, 420, 900, 1180, 1400][i]} y={362 + j * 84} fontFamily="VT323" fontSize={60} fill={i === 4 ? (c.includes("DELAY") || c.includes("CANCEL") ? "#ff5a4a" : "#6ae86a") : "#f4f1e0"}>{c}</text>)}</g>)}
</svg>;
export const PlaneSky: React.FC<{ f: number; n?: number }> = ({ f, n = 3 }) => <svg width={W} height={H} style={{ position: "absolute" }}>
  <defs><linearGradient id="dusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#2a3a7a" /><stop offset="1" stopColor="#e88a5a" /></linearGradient></defs>
  <rect width={W} height={H} fill="url(#dusk)" />{Array.from({ length: 8 }, (_, i) => <ellipse key={i} cx={(rnd(i, 1) * 2400 - f * 2) % 2400} cy={200 + rnd(i, 2) * 500} rx={200} ry={30} fill="#fff" opacity={0.12} />)}
  <rect y={900} width={W} height={180} fill="#2a2a3a" /><rect y={960} width={W} height={10} fill="#f4f1e0" opacity={0.4} />
  {Array.from({ length: n }, (_, i) => { const t = f - i * 40; if (t < 0) return null; const x = -300 + t * 18, y = 900 - Math.max(0, t - 10) * 7;
    return <g key={i} transform={`translate(${x} ${y}) rotate(-14) scale(${1 - i * 0.2})`}><path d="M0 0 L420 0 Q470 0 490 24 L420 40 L0 40 Q-24 20 0 0 Z" fill="#f4f6f8" /><path d="M160 24 L260 100 L300 100 L240 24 Z" fill="#c8ced4" /><path d="M10 0 L-24 -70 L16 -70 L64 0 Z" fill="#2f6ad8" />{Array.from({ length: 10 }, (_, k) => <circle key={k} cx={110 + k * 26} cy={16} r={4} fill="#3a4a5a" />)}<circle cx={-6} cy={20} r={5} fill="#ff4a3a" opacity={Math.floor(f / 10) % 2} /></g>; })}
</svg>;

// ---------- the map of the United States (simplified outline) ----------
// contiguous US outline from real lon/lat points, sinusoidal projection centred on 96°W
const LL: number[][] = [[-124.7,48.4],[-124.1,46.9],[-124.0,44.0],[-124.4,42.0],[-124.2,40.4],[-123.7,38.9],[-122.5,37.7],[-121.9,36.6],[-120.6,34.6],[-118.5,34.0],[-117.1,32.5],
  [-114.7,32.7],[-111.1,31.3],[-108.2,31.3],[-106.5,31.8],[-104.9,30.6],[-103.3,29.0],[-102.4,29.8],[-101.4,29.8],[-99.5,27.5],[-97.4,25.9],[-97.4,27.8],[-96.0,28.6],[-94.0,29.7],[-92.0,29.6],[-90.0,29.1],[-89.4,30.0],
  [-88.0,30.4],[-86.5,30.4],[-85.0,29.7],[-84.0,30.1],[-83.0,29.0],[-82.7,27.5],[-81.8,26.1],[-81.0,25.2],[-80.4,25.2],[-80.1,26.5],[-80.6,28.4],[-81.3,30.0],[-81.4,31.4],[-80.9,32.1],[-79.2,33.2],[-77.9,33.9],
  [-76.5,34.7],[-75.5,35.3],[-75.9,36.9],[-75.6,37.9],[-75.0,38.8],[-74.1,39.7],[-73.9,40.5],[-72.0,41.0],[-70.0,41.6],[-70.0,41.8],[-70.8,42.3],[-70.6,43.1],[-69.0,44.0],[-67.0,44.8],[-67.8,47.1],[-69.2,47.4],
  [-70.0,46.7],[-71.5,45.0],[-74.7,45.0],[-76.2,44.2],[-79.1,43.3],[-79.8,42.5],[-82.6,41.8],[-83.1,42.1],[-82.4,43.0],[-82.5,45.3],[-84.1,46.5],[-88.4,48.3],[-89.6,48.0],[-95.2,49.0],[-123.3,49.0],[-122.8,48.9]];
export const proj = (lon: number, lat: number): [number, number] => [960 + (lon + 96) * 31 * Math.cos(lat * Math.PI / 180), 110 + (49.5 - lat) * 31 * 1.12];
const US = "M" + LL.map(([lo, la]) => proj(lo, la).map(v => v.toFixed(0)).join(" ")).join(" L") + " Z";
const C = (lo: number, la: number) => proj(lo, la);
export const CITIES: Record<string, [number, number]> = { ATL: C(-84.4, 33.75), NYC: C(-74, 40.7), LA: C(-118.2, 34.05), CHI: C(-87.6, 41.9), DAL: C(-96.8, 32.8), MIA: C(-80.2, 25.8), SEA: C(-122.3, 47.6), DEN: C(-105, 39.7), HOU: C(-95.4, 29.8), PHX: C(-112, 33.4), BOS: C(-71.1, 42.4), DC: C(-77, 38.9), SF: C(-122.4, 37.8), MT: C(-110, 47), TX: C(-102, 31.5) };
export const USMap: React.FC<{ f: number; spread?: number; routes?: number; safe?: number; path?: number; label?: string; dots?: number; bare?: boolean }> = ({ f, spread = 0, routes = 0, safe = 0, path = 0, label, dots = 0, bare = false }) => {
  const order = ["ATL", "NYC", "CHI", "LA", "MIA", "DAL", "HOU", "DC", "BOS", "DEN", "PHX", "SEA", "SF"];
  return <svg width={W} height={H} style={{ position: "absolute" }}>
    <defs><radialGradient id="mapbg" cx="0.5" cy="0.45" r="0.8"><stop offset="0" stopColor="#14223a" /><stop offset="1" stopColor="#060a14" /></radialGradient>
      <clipPath id="usclip"><path d={US} /></clipPath>
      <filter id="redglow"><feGaussianBlur stdDeviation="22" /></filter></defs>
    {!bare && <rect width={W} height={H} fill="url(#mapbg)" />}
    {!bare && Array.from({ length: 24 }, (_, i) => <line key={i} x1={i * 90} y1={0} x2={i * 90} y2={H} stroke="#2a3a5a" strokeOpacity={0.25} />)}{!bare && Array.from({ length: 14 }, (_, i) => <line key={i} x1={0} y1={i * 90} x2={W} y2={i * 90} stroke="#2a3a5a" strokeOpacity={0.25} />)}
    <path d={US} fill="#22344e" stroke="#6a8ab8" strokeWidth={4} />
    {/* spread blobs (clipped to the country) */}
    <g clipPath="url(#usclip)" filter="url(#redglow)">{order.map((c, i) => { const k = sat(spread * order.length - i * 0.75); return k > 0 ? <circle key={c} cx={CITIES[c][0]} cy={CITIES[c][1]} r={40 + 260 * ease(k)} fill="#e8322a" opacity={0.55} /> : null; })}</g>
    {/* flight routes from ATL */}
    {routes > 0 && order.slice(1).map((c, i) => { const k = sat(routes * 1.6 - i * 0.1); if (k <= 0) return null; const [x0, y0] = CITIES.ATL, [x1, y1] = CITIES[c], mx = (x0 + x1) / 2, my = Math.min(y0, y1) - 140;
      return <g key={c}><path d={`M${x0} ${y0} Q${mx} ${my} ${x1} ${y1}`} stroke="#ffd34a" strokeWidth={3} fill="none" strokeDasharray="1400" strokeDashoffset={1400 * (1 - k)} opacity={0.8} />
        {k >= 1 && <circle cx={x1} cy={y1} r={9 + 3 * Math.sin(f * 0.3 + i)} fill="#ff5a4a" />}</g>; })}
    {/* random infection dots */}
    {dots > 0 && Array.from({ length: Math.floor(dots * 220) }, (_, i) => <circle key={i} cx={300 + rnd(i, 41) * 1350} cy={150 + rnd(i, 42) * 700} r={4} fill="#ff4a3a" opacity={0.8} clipPath="url(#usclip)" />)}
    {/* safe zone: northern Rockies */}
    {safe > 0 && <g opacity={sat(safe * 2)}><ellipse cx={CITIES.MT[0]} cy={CITIES.MT[1]} rx={170 * ease(safe)} ry={90 * ease(safe)} fill="#4ae88a" opacity={0.25} stroke="#4ae88a" strokeWidth={5} strokeDasharray="14 10" />
      <text x={CITIES.MT[0]} y={CITIES.MT[1] - 110} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={34} fill="#6aff9a">SAFE ZONE · MONTANA</text></g>}
    {/* the trip north: Atlanta → Montana */}
    {path > 0 && <g><path d={`M${CITIES.ATL[0]} ${CITIES.ATL[1]} C ${CITIES.ATL[0] - 150} ${CITIES.ATL[1] - 100}, ${CITIES.CHI[0] - 200} ${CITIES.CHI[1] + 60}, ${(CITIES.CHI[0] + CITIES.MT[0]) / 2} ${CITIES.MT[1] + 80} S ${CITIES.MT[0] + 80} ${CITIES.MT[1] + 10}, ${CITIES.MT[0]} ${CITIES.MT[1]}`} stroke="#ffd34a" strokeWidth={8} fill="none" strokeDasharray="1300" strokeDashoffset={1300 * (1 - path)} strokeLinecap="round" />
      <text x={CITIES.ATL[0] + 20} y={CITIES.ATL[1] + 50} fontFamily="Inter" fontWeight={900} fontSize={28} fill="#ffd34a">ATLANTA</text>
      <text x={(CITIES.ATL[0] + CITIES.MT[0]) / 2} y={CITIES.MT[1] + 210} fontFamily="Inter" fontWeight={900} fontSize={30} fill="#fff" opacity={sat(path * 2)}>~2,000 MILES</text></g>}
    {Object.entries(CITIES).filter(([k]) => ["ATL", "NYC", "LA", "CHI", "DAL"].includes(k)).map(([k, [x, y]]) => <g key={k}><circle cx={x} cy={y} r={6} fill="#fff" /><text x={x + 12} y={y - 10} fontFamily="Inter" fontWeight={800} fontSize={22} fill="#c8d8f0">{k}</text></g>)}
    {label && <text x={1860} y={1020} textAnchor="end" fontFamily="Inter" fontWeight={900} fontSize={44} fill="#fff" letterSpacing={4}>{label}</text>}
  </svg>;
};
