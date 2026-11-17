// Ice Age locations: blizzard, the glacier valley at dawn, the snow cave, the riverbank with flint + pyrite, the band's
// camp under a rock overhang (warm firelight), a hide tent interior, the painted cave by torchlight, a storm gully,
// the museum Ice Age hall (2026) and the modern research cave (2026). Cold exteriors / warm interiors.
import React from "react";
import { rnd, sat, lerp } from "../engine/core";
import { Glow, Shaft } from "../engine/fx";
import { Noise, AO } from "../engine/tex";
import { Mammoth, Herd, Reindeer, Rhino } from "./Animals";

let gid = 0; const uid = (p: string) => `${p}${++gid}`;
const SkyG: React.FC<{ top: string; bot: string }> = ({ top, bot }) => { const id = React.useMemo(() => uid("sk"), []);
  return <><defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={top} /><stop offset="1" stopColor={bot} /></linearGradient></defs><rect x={-1200} y={-500} width={4400} height={1500} fill={`url(#${id})`} /></>; };
export const Snow: React.FC<{ f: number; n?: number; wind?: number; speed?: number; o?: number; size?: number }> = ({ f, n = 160, wind = 6, speed = 9, o = 0.9, size = 1 }) =>
  <g opacity={o}>{Array.from({ length: n }, (_, i) => { const x = ((rnd(i, 1) * 2600 + f * wind * (0.6 + rnd(i, 4))) % 2600) - 340, y = ((rnd(i, 2) * 1400 + f * speed * (0.6 + rnd(i, 5))) % 1400) - 160;
    return <ellipse key={i} cx={x} cy={y} rx={(2 + rnd(i, 3) * 4) * size + wind * 0.3} ry={(2 + rnd(i, 3) * 4) * size} fill="#fff" opacity={0.5 + 0.5 * rnd(i, 6)} />; })}</g>;
const Mountains: React.FC<{ y: number; c: string; snow?: string; seed?: number; h?: number }> = ({ y, c, snow = "#f4f8fc", seed = 1, h = 300 }) => {
  const pts = Array.from({ length: 14 }, (_, i) => [-900 + i * 300, y - h * (0.3 + rnd(i, seed) * 0.7)]);
  return <g><path d={`M-1000 ${y + 400} L-1000 ${y} ${pts.map(([x, py], i) => `L${x} ${py} L${x + 150} ${y - h * 0.15 * rnd(i, seed + 3)}`).join(" ")} L3000 ${y} L3000 ${y + 400} Z`} fill={c} />
    {pts.map(([x, py], i) => <path key={i} d={`M${x - 60} ${py + 70} L${x} ${py} L${x + 60} ${py + 70} L${x + 30} ${py + 50} L${x} ${py + 66} L${x - 30} ${py + 48} Z`} fill={snow} />)}</g>; };
const Tufts: React.FC<{ y0: number; y1: number; n?: number; seed?: number; c?: string }> = ({ y0, y1, n = 60, seed = 7, c = "#b8a070" }) =>
  <g>{Array.from({ length: n }, (_, i) => { const x = -900 + rnd(i, seed) * 3800, y = y0 + rnd(i, seed + 1) * (y1 - y0), s = 0.5 + rnd(i, seed + 2); return <path key={i} d={`M${x} ${y} l${-6 * s} ${-26 * s} M${x} ${y} l${2 * s} ${-32 * s} M${x} ${y} l${10 * s} ${-24 * s}`} stroke={c} strokeWidth={3} strokeLinecap="round" />; })}</g>;
const Rock: React.FC<{ x: number; y: number; s?: number; c?: string; snow?: boolean }> = ({ x, y, s = 1, c = "#6a6e78", snow = true }) =>
  <g transform={`translate(${x} ${y}) scale(${s})`}><path d="M-90 0 Q-100 -60 -40 -80 Q20 -100 70 -60 Q100 -30 90 0 Z" fill={c} /><path d="M-40 -80 Q20 -100 70 -60 Q30 -70 -20 -60 Z" fill="#fff" opacity={snow ? 0.85 : 0.1} /><path d="M-90 0 L90 0" stroke="#000" strokeOpacity={0.3} strokeWidth={6} /></g>;

// ---------- blizzard: whiteout, a figure, shapes moving behind the snow curtain ----------
export const Blizzard: React.FC<{ f: number; children?: React.ReactNode; behind?: React.ReactNode; vis?: number }> = ({ f, children, behind, vis = 0.25 }) => <g>
  <SkyG top="#b8c8d8" bot="#e8eef4" />
  <g opacity={vis}><Mountains y={620} c="#9aaabc" seed={3} /></g>
  {behind && <g opacity={0.35 + vis}>{behind}</g>}
  <rect x={-1200} y={-500} width={4400} height={1500} fill="#eef4fa" opacity={0.55 - vis * 0.5} />
  <rect x={-1000} y={760} width={4000} height={600} fill="#f4f8fc" /><path d="M-1000 780 Q0 740 960 790 T3000 770 L3000 1300 L-1000 1300 Z" fill="#e4ecf4" />
  {children}
  <Snow f={f} n={260} wind={14} speed={10} size={1.4} />
</g>;

// ---------- the valley at dawn: glacier wall, mountains, frozen river, herd ----------
export const Valley: React.FC<{ f: number; children?: React.ReactNode; herd?: boolean; time?: "dawn" | "day" | "dusk" }> = ({ f, children, herd = true, time = "dawn" }) => {
  const sky = { dawn: ["#6a7ab8", "#f4c8a0"], day: ["#7ab0e0", "#dceaf4"], dusk: ["#3a3a6a", "#e8906a"] }[time];
  return <g>
    <SkyG top={sky[0]} bot={sky[1]} />
    {time !== "day" && <><circle cx={1500} cy={520} r={70} fill="#fff4d0" /><Glow x={1500} y={520} r={500} color="#ffd8a0" o={0.5} /></>}
    {/* the glacier wall on the horizon */}
    <path d="M-1000 520 L-400 470 L200 500 L800 450 L1400 480 L2000 440 L3000 470 L3000 600 L-1000 600 Z" fill="#dceaf6" />
    {Array.from({ length: 40 }, (_, i) => <line key={i} x1={-1000 + i * 100} y1={470 + rnd(i, 3) * 30} x2={-1000 + i * 100 + 10} y2={600} stroke="#a8c8e4" strokeWidth={3} opacity={0.6} />)}
    <Mountains y={640} c="#7a8aa8" seed={5} h={260} />
    <rect x={-1000} y={640} width={4000} height={700} fill="#e8eef0" />
    <path d="M-1000 700 Q-200 680 400 720 T1800 700 T3000 720 L3000 1300 L-1000 1300 Z" fill="#d8e2e4" />
    {/* frozen river */}
    <path d="M-1000 860 Q-300 820 300 880 Q900 940 1500 860 Q2100 790 3000 850 L3000 920 Q2100 860 1500 930 Q900 1010 300 950 Q-300 890 -1000 930 Z" fill="#a8d0e8" />
    <path d="M-600 880 Q0 900 600 930" stroke="#fff" strokeWidth={4} opacity={0.6} fill="none" />
    <Tufts y0={700} y1={1080} n={70} />
    <Rock x={-200} y={1000} s={1.2} /><Rock x={1900} y={980} s={0.9} />
    {herd && <Herd f={f} x0={-300} x1={1300} y={740} n={5} s={0.32} kind="mammoth" speed={0.5} />}
    {herd && <Herd f={f} x0={900} x1={2100} y={800} n={7} s={0.3} kind="reindeer" speed={0.9} seed={4} dir={-1} />}
    {children}
  </g>; };

// ---------- the snow cave (interior, blue glow) ----------
export const SnowCave: React.FC<{ f: number; children?: React.ReactNode }> = ({ f, children }) => <g>
  <rect x={-1000} y={-500} width={4000} height={1700} fill="#1a2a3e" />
  <ellipse cx={960} cy={700} rx={900} ry={620} fill="#4a6a8e" /><ellipse cx={960} cy={720} rx={760} ry={500} fill="#6a8ab0" />
  <ellipse cx={1500} cy={520} rx={160} ry={120} fill="#c8e0f4" opacity={0.6} /><Glow x={1500} y={520} r={500} color="#a8d0ff" o={0.4} />
  {Array.from({ length: 30 }, (_, i) => <ellipse key={i} cx={300 + rnd(i, 1) * 1300} cy={250 + rnd(i, 2) * 500} rx={30 + rnd(i, 3) * 40} ry={14} fill="#fff" opacity={0.08} />)}
  <rect x={-1000} y={900} width={4000} height={400} fill="#8aa8c8" /><AO x={-1000} y={900} w={4000} h={60} dir="down" o={0.4} />
  {children}
</g>;

// ---------- riverbank: ice edge + stones (grey flint, shiny pyrite) ----------
export const Riverbank: React.FC<{ f: number; children?: React.ReactNode; glint?: number }> = ({ f, children, glint = 0 }) => <g>
  <SkyG top="#8ab0d8" bot="#e8eef4" /><Mountains y={520} c="#8a9ab8" seed={9} />
  <rect x={-1000} y={520} width={4000} height={240} fill="#e4ecf0" />
  <path d="M-1000 700 Q960 640 3000 700 L3000 860 L-1000 860 Z" fill="#9ac8e4" /><path d="M-1000 700 Q960 640 3000 700" stroke="#fff" strokeWidth={8} fill="none" opacity={0.8} />
  <rect x={-1000} y={840} width={4000} height={500} fill="#8a7a64" />
  {Array.from({ length: 70 }, (_, i) => { const x = -800 + rnd(i, 3) * 3600, y = 860 + rnd(i, 4) * 220, r = 14 + rnd(i, 5) * 22, kind = rnd(i, 6);
    return <g key={i}><ellipse cx={x} cy={y} rx={r} ry={r * 0.6} fill={kind > 0.86 ? "#c8a84a" : kind > 0.7 ? "#7a808a" : "#a8988a"} />
      {kind > 0.86 && <><ellipse cx={x - r * 0.3} cy={y - r * 0.2} rx={r * 0.3} ry={r * 0.15} fill="#fff6c8" opacity={0.8} />{glint > 0 && <Glow x={x} y={y} r={50} color="#ffe8a0" o={0.6 * glint * (0.5 + 0.5 * Math.sin(f * 0.3 + i))} />}</>}</g>; })}
  {children}
</g>;

// ---------- the band's camp under a rock overhang (warm) ----------
export const BoneTent: React.FC<{ x: number; y: number; s?: number; c?: string }> = ({ x, y, s = 1, c = "#8a6a48" }) => <g transform={`translate(${x} ${y}) scale(${s})`}>
  <path d="M-200 0 Q-180 -260 0 -300 Q180 -260 200 0 Z" fill={c} /><path d="M-200 0 Q-180 -260 0 -300 Q-60 -200 -90 0 Z" fill="#000" opacity={0.18} />
  {[-1, 1].map(k => <path key={k} d={`M${k * 170} 0 Q${k * 190} -200 ${k * 40} -310`} stroke="#efe6d2" strokeWidth={16} fill="none" strokeLinecap="round" />)}
  <path d="M-60 0 Q0 -120 60 0 Z" fill="#2a1a10" /><path d="M-60 0 Q0 -120 60 0" stroke="#5a3e28" strokeWidth={6} fill="none" />
  {[0, 1, 2].map(i => <path key={i} d={`M${-150 + i * 120} ${-80 - i * 40} l30 0`} stroke="#5a3e28" strokeWidth={3} strokeDasharray="4 4" />)}
</g>;
export const Fire: React.FC<{ x: number; y: number; f: number; s?: number; glow?: number }> = ({ x, y, f, s = 1, glow = 1 }) => <g transform={`translate(${x} ${y}) scale(${s})`}>
  {[-1, 0, 1].map(k => <rect key={k} x={-60} y={-8} width={120} height={16} rx={8} fill="#4a2e1a" transform={`rotate(${k * 30})`} />)}
  {Array.from({ length: 5 }, (_, i) => { const h = 70 + 30 * Math.sin(f * 0.4 + i * 1.7), w = 30 - i * 3; return <path key={i} d={`M${(i - 2) * 16 - w / 2} 0 Q${(i - 2) * 16} ${-h * 1.2} ${(i - 2) * 16 + w / 2} 0 Z`} fill={["#ff8a2a", "#ffb84a", "#ffd86a", "#ffb84a", "#ff8a2a"][i]} opacity={0.9} />; })}
  <path d={`M-16 0 Q0 ${-50 - 10 * Math.sin(f * 0.6)} 16 0 Z`} fill="#fff6c8" />
  {Array.from({ length: 6 }, (_, i) => { const t = ((f * 0.03 + i / 6) % 1); return <circle key={i} cx={Math.sin(i * 7 + f * 0.05) * 30} cy={-80 - t * 260} r={3} fill="#ffb84a" opacity={1 - t} />; })}
  {glow > 0 && <><Glow x={0} y={-40} r={700 * glow} color="#ff9a3a" o={0.4} /><Glow x={0} y={-40} r={160} color="#ffe8b0" o={0.6} /></>}
</g>;
export const Camp: React.FC<{ f: number; children?: React.ReactNode; night?: boolean; fire?: boolean }> = ({ f, children, night = false, fire = true }) => <g>
  <SkyG top={night ? "#0a1028" : "#7a9ac8"} bot={night ? "#2a3048" : "#e4d8c8"} />
  <Mountains y={560} c={night ? "#2a3048" : "#8a96b0"} seed={11} />
  <rect x={-1000} y={560} width={4000} height={800} fill={night ? "#3a3a44" : "#d8d4cc"} />
  {/* rock overhang */}
  <path d="M-900 -200 L2900 -200 L2900 120 Q2200 260 1400 200 Q800 150 300 260 Q-200 330 -900 300 Z" fill={night ? "#2a2420" : "#6a5a4e"} />
  <path d="M-900 260 Q-200 300 300 230 Q800 120 1400 170 Q2200 230 2900 90" stroke={night ? "#1a1612" : "#4a3e34"} strokeWidth={30} fill="none" />
  <Noise x={-900} y={-200} w={3800} h={520} freq={0.4} o={0.3} />
  <rect x={-1000} y={760} width={4000} height={600} fill={night ? "#3a2e26" : "#7a6450"} /><Noise x={-1000} y={760} w={4000} h={600} freq={0.5} o={0.3} />
  <BoneTent x={260} y={790} s={0.95} /><BoneTent x={1680} y={800} s={1.05} c="#7a5a3e" /><BoneTent x={-260} y={770} s={0.7} c="#6a4a32" /><BoneTent x={2200} y={770} s={0.7} c="#8a6448" />
  {/* drying rack with hides + antlers */}
  <g transform="translate(1260 790)"><path d="M-120 0 L-120 -220 M120 0 L120 -220 M-140 -210 L140 -210" stroke="#5a3e28" strokeWidth={10} /><path d="M-100 -205 L-30 -205 L-40 -80 L-90 -90 Z" fill="#b08a60" /><path d="M10 -205 L90 -205 L80 -100 L20 -110 Z" fill="#9a7650" /></g>
  <path d="M560 800 q-40 -60 -20 -110 M560 800 q30 -70 60 -90 M580 770 q-30 -10 -50 -40" stroke="#e8dcc4" strokeWidth={8} fill="none" strokeLinecap="round" />
  {[[620, 860], [1420, 880]].map(([x, y], i) => <ellipse key={i} cx={x} cy={y} rx={60} ry={28} fill="#9a7a50" stroke="#6a5030" strokeWidth={4} />)}
  {fire && <Fire x={960} y={880} f={f} s={1.1} glow={night ? 1.4 : 0.9} />}
  {children}
  {night && <rect x={-1000} y={-500} width={4000} height={1800} fill="#0a1030" opacity={0.25} style={{ mixBlendMode: "multiply" }} />}
</g>;

// ---------- hide tent interior: Pip sick under furs (head only, face upright) ----------
export const TentIn: React.FC<{ f: number; children?: React.ReactNode }> = ({ f, children }) => <g>
  <rect x={-1000} y={-500} width={4000} height={1800} fill="#3a2418" />
  <path d="M-200 1100 Q-100 100 960 -60 Q2000 100 2100 1100 Z" fill="#7a5638" /><path d="M960 -60 L960 1100" stroke="#5a3e28" strokeWidth={10} />
  {Array.from({ length: 6 }, (_, i) => <path key={i} d={`M${200 + i * 300} 1100 Q${400 + i * 200} 400 960 -60`} stroke="#6a4a30" strokeWidth={4} fill="none" opacity={0.5} />)}
  <rect x={-1000} y={860} width={4000} height={400} fill="#4a3020" />
  <Fire x={1500} y={900} f={f} s={0.6} glow={1.1} />
  {children}
</g>;

// ---------- the painted cave by torchlight ----------
export const PaintedCave: React.FC<{ f: number; children?: React.ReactNode; torch?: [number, number]; extra?: React.ReactNode; modern?: boolean }> = ({ f, children, torch = [960, 400], extra, modern = false }) => {
  const fl = 0.85 + 0.15 * Math.sin(f * 0.6) * Math.sin(f * 0.27);
  return <g>
    <rect x={-1000} y={-500} width={4000} height={1800} fill="#1a120c" />
    <path d="M-900 -300 Q960 -420 2900 -300 L2900 820 Q960 900 -900 820 Z" fill="#8a6a50" /><Noise x={-900} y={-420} w={3800} h={1320} freq={0.35} o={0.45} />
    {Array.from({ length: 12 }, (_, i) => <path key={i} d={`M${-800 + i * 330} ${-200 + rnd(i, 4) * 200} q${60} ${200 + rnd(i, 5) * 300} ${-20} ${600}`} stroke="#5a4232" strokeWidth={5} fill="none" opacity={0.4} />)}
    {/* paintings (red ochre + charcoal): horses, a lion, a rhino, handprints */}
    <g opacity={0.85}>
      <g transform="translate(250 260) scale(0.55)" fill="none" stroke="#2a1a14" strokeWidth={10}><path d="M-160 0 Q-120 -80 0 -80 Q100 -90 140 -30 L170 -60 L180 -20 L150 10 L130 90 M100 0 L110 90 M-120 10 L-130 90 M-80 10 L-70 90 M-160 0 Q-200 20 -210 60" /></g>
      <g transform="translate(700 180) scale(0.6)" fill="#a8402a" opacity={0.8}><path d="M-150 0 Q-110 -70 10 -70 Q110 -80 150 -20 L180 -30 L170 10 L140 20 L130 80 L110 80 L100 20 L-90 20 L-100 80 L-120 80 L-130 10 Q-170 20 -180 50 Q-170 0 -150 0 Z" /></g>
      <g transform="translate(1250 280) scale(0.7)" fill="none" stroke="#2a1a14" strokeWidth={9}><path d="M-200 0 Q-180 -70 -60 -80 L120 -80 Q190 -70 210 -20 L250 -30 Q240 10 210 20 L200 90 M150 20 L150 90 M-150 10 L-160 90 M-100 10 L-90 90" /><path d="M200 -60 l40 -40 M190 -70 l20 -50" /></g>
      <g transform="translate(1700 200) scale(0.55)" fill="#a8402a" opacity={0.75}><path d="M-200 20 Q-200 -90 -40 -100 Q140 -110 200 -40 Q250 -10 240 40 L-180 50 Z" /><path d="M220 -40 Q270 -120 290 -110 Q270 -60 250 -10 Z" /></g>
      {[[-100, 520], [80, 560], [1900, 520], [1760, 600]].map(([x, y], i) => <g key={i} transform={`translate(${x} ${y}) rotate(${(i - 1.5) * 12})`} opacity={0.7}><ellipse cx={0} cy={0} rx={34} ry={40} fill="#a8402a" />{[-24, -10, 4, 18].map((fx, k) => <rect key={k} x={fx - 6} y={-80 + Math.abs(k - 1.5) * 6} width={12} height={46} rx={6} fill="#a8402a" />)}<rect x={26} y={-14} width={12} height={34} rx={6} fill="#a8402a" transform="rotate(30 30 0)" /></g>)}
    </g>
    {extra}
    <rect x={-1000} y={820} width={4000} height={500} fill="#3a2a1e" />
    {/* torchlight (or modern lamps) */}
    {modern ? <><rect x={-1000} y={-500} width={4000} height={1800} fill="#000" opacity={0.25} /><Glow x={500} y={300} r={900} color="#f4f6ff" o={0.35} /><Glow x={1500} y={300} r={900} color="#f4f6ff" o={0.35} /></>
      : <><rect x={-1000} y={-500} width={4000} height={1800} fill="#000" opacity={0.55 - 0.15 * fl} /><Glow x={torch[0]} y={torch[1]} r={1000 * fl} color="#ffa040" o={0.45} /><Glow x={torch[0]} y={torch[1]} r={200} color="#ffe0a0" o={0.6} /></>}
    {children}
  </g>; };

// ---------- museum Ice Age hall at night (2026) ----------
export const Museum: React.FC<{ f: number; children?: React.ReactNode; glow?: number; flicker?: boolean }> = ({ f, children, glow = 0, flicker = false }) => {
  const on = flicker ? (rnd(Math.floor(f / 2), 9) > 0.35 ? 1 : 0.3) : 1;
  return <g>
    <rect x={-1000} y={-500} width={4000} height={1800} fill="#141820" />
    <rect x={-1000} y={-500} width={4000} height={1180} fill="#1e2430" />
    {Array.from({ length: 7 }, (_, i) => <g key={i}><rect x={-700 + i * 520} y={40} width={300} height={14} rx={4} fill={on > 0.5 ? "#e8f0ff" : "#3a3e48"} opacity={0.8} /><Shaft pts={[[-700 + i * 520, 54], [-400 + i * 520, 54], [-300 + i * 520, 700], [-800 + i * 520, 700]]} color="#c8d8ff" o={0.06 * on} /></g>)}
    {/* exhibit banner */}
    <g transform="translate(960 130)"><rect x={-360} y={-50} width={720} height={100} rx={10} fill="#2a3a5a" /><text x={0} y={18} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={44} fill="#e8eef8" letterSpacing={6}>THE ICE AGE</text><text x={0} y={44} textAnchor="middle" fontFamily="Inter" fontWeight={700} fontSize={18} fill="#9ab0d0" letterSpacing={6}>30,000 YEARS AGO</text></g>
    {/* mammoth skeleton */}
    <g transform="translate(470 860) scale(0.75)" stroke="#e8e0cc" fill="none" strokeLinecap="round">
      {Array.from({ length: 12 }, (_, i) => <path key={i} d={`M${-220 + i * 36} ${-430 + Math.abs(i - 5) * 8} q-6 120 4 200`} strokeWidth={10} />)}
      <path d="M-260 -420 Q-60 -540 200 -470" strokeWidth={18} /><path d="M200 -470 Q300 -520 330 -420 Q340 -340 290 -300" strokeWidth={20} />
      <path d="M310 -320 Q430 -250 410 -120 Q400 -80 380 -70" strokeWidth={22} />
      {[-200, -130, 170, 240].map(x => <path key={x} d={`M${x} -230 L${x + 6} 0`} strokeWidth={22} />)}
      <path d="M-200 0 L300 0" stroke="#5a5e68" strokeWidth={14} />
    </g>
    {/* the glass case with the carved bone */}
    <g transform="translate(1300 760)">
      <rect x={-140} y={-80} width={280} height={300} fill="#2a2e38" />
      <rect x={-130} y={-320} width={260} height={240} fill="#9ab0c8" opacity={0.12} stroke="#c8d8f0" strokeOpacity={0.5} strokeWidth={4} />
      <g transform="translate(0 -150) rotate(-10)"><rect x={-90} y={-14} width={180} height={28} rx={14} fill="#e8dcc0" />{Array.from({ length: 22 }, (_, i) => <line key={i} x1={-76 + i * 7} y1={-10} x2={-76 + i * 7} y2={10} stroke={glow > 0 ? "#ffe08a" : "#8a7a5a"} strokeWidth={2.5} />)}
        {glow > 0 && <Glow x={0} y={0} r={260 * glow} color="#ffd86a" o={0.8 * glow} />}</g>
      <rect x={-100} y={-40} width={200} height={40} fill="#e8eef8" /><text x={0} y={-14} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={14} fill="#2a3a5a">CARVED BONE · c. 28,000 BC</text>
    </g>
    <rect x={-1000} y={880} width={4000} height={420} fill="#2a2e38" /><rect x={-1000} y={880} width={4000} height={120} fill="#c8d8ff" opacity={0.05} />
    {children}
    {glow > 0 && <rect x={-1000} y={-500} width={4000} height={1800} fill="#fff6d0" opacity={sat(glow - 0.7) * 3} />}
  </g>; };

// ---------- 2026 research cave: lamps, tripods, cables ----------
export const ResearchCave: React.FC<{ f: number; children?: React.ReactNode; figure?: number }> = ({ f, children, figure = 1 }) =>
  <PaintedCave f={f} modern extra={<>
    {/* the hooded figure with a glowing rectangle + E L I + smiley (panel 7) */}
    <g transform="translate(980 560)" opacity={figure}><circle cx={0} cy={-120} r={34} fill="none" stroke="#1a120c" strokeWidth={9} /><path d="M-40 -130 Q0 -190 40 -130" stroke="#1a120c" strokeWidth={9} fill="none" />
      <path d="M0 -86 L0 20 M0 20 L-30 100 M0 20 L30 100 M0 -60 L40 -30" stroke="#1a120c" strokeWidth={9} fill="none" strokeLinecap="round" />
      <rect x={40} y={-58} width={30} height={48} rx={5} fill="none" stroke="#1a120c" strokeWidth={7} />
      {[0, 1, 2, 3].map(i => <line key={i} x1={48 + i * 0} y1={-50 + i * 10} x2={62} y2={-50 + i * 10} stroke="#a8402a" strokeWidth={3} opacity={0.6} />)}
      <text x={110} y={60} fontFamily="Permanent Marker" fontSize={46} fill="#1a120c" opacity={0.85}>E L I</text>
      <g transform="translate(250 40)"><circle r={22} fill="none" stroke="#1a120c" strokeWidth={5} /><circle cx={-8} cy={-6} r={3} fill="#1a120c" /><circle cx={8} cy={-6} r={3} fill="#1a120c" /><path d="M-10 6 Q0 16 10 6" stroke="#1a120c" strokeWidth={4} fill="none" /></g></g>
    {/* lamps */}
    {[300, 1650].map(x => <g key={x}><path d={`M${x - 60} 820 L${x} 420 L${x + 60} 820`} stroke="#2a2a2e" strokeWidth={8} fill="none" /><rect x={x - 60} y={380} width={120} height={60} rx={8} fill="#3a3a40" /><rect x={x - 50} y={390} width={100} height={40} rx={6} fill="#fffef0" /></g>)}
    <path d="M300 820 Q960 900 1650 820" stroke="#c8282a" strokeWidth={5} fill="none" />
  </>}>{children}</PaintedCave>;
