// AI-takeover locations (our own designs): Leo's smart bedroom, the FIXIT repair shop (day / night-rain), a rainy night
// street with an alley, the smart-city panorama (day / locked / blackout + Milky Way), the desert data centre ORIN-1,
// the server hall with the breaker, the railway-tunnel bunker. Ground line ≈ y 900–1000 like every other scene.
import React from "react";
import { rnd, sat, lerp } from "../engine/core";
import { Glow, Shaft, Rain } from "../engine/fx";
import { Noise, AO, Bricks, Wood } from "../engine/tex";
import { shade } from "../chars/Rig2";

let gid = 0; const uid = (p: string) => `${p}${++gid}`;
const Sky: React.FC<{ top: string; bot: string }> = ({ top, bot }) => { const id = React.useMemo(() => uid("sk"), []);
  return <><defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={top} /><stop offset="1" stopColor={bot} /></linearGradient></defs><rect x={-1200} y={-600} width={4400} height={1700} fill={`url(#${id})`} /></>; };
export const ORIN_BLUE = "#5ad8ff", ORIN_RED = "#ff3a24";
// the ORIN ring logo (used on speakers, screens, the data centre)
export const OrinRing: React.FC<{ x: number; y: number; r: number; f: number; c?: string; o?: number }> = ({ x, y, r, f, c = ORIN_BLUE, o = 1 }) =>
  <g opacity={o}><Glow x={x} y={y} r={r * 2.4} color={c} o={0.35 + 0.1 * Math.sin(f * 0.1)} /><circle cx={x} cy={y} r={r} fill="none" stroke={c} strokeWidth={r * 0.22} />
    <circle cx={x} cy={y} r={r * 0.62} fill="none" stroke={c} strokeWidth={r * 0.06} opacity={0.6} strokeDasharray={`${r * 0.4} ${r * 0.25}`} transform={`rotate(${f * 2} ${x} ${y})`} /><circle cx={x} cy={y} r={r * 0.16} fill={c} /></g>;

// ---------- Leo's bedroom, 2026 morning: blinds that open themselves, ORIN speaker, posters ----------
export const SmartRoom: React.FC<{ f: number; blinds?: number; children?: React.ReactNode; night?: boolean; red?: number }> = ({ f, blinds = 1, children, night, red = 0 }) => <g>
  <rect x={-1200} y={-600} width={4400} height={1700} fill={night ? "#1c2230" : "#e8dccb"} />
  <Noise x={-200} y={0} w={2400} h={900} o={0.08} />
  {/* window with the city */}
  <g><rect x={1080} y={200} width={560} height={420} fill={night ? "#0c1220" : "#8ac8f0"} />
    {Array.from({ length: 9 }, (_, i) => <rect key={i} x={1090 + i * 62} y={420 - rnd(i, 3) * 160} width={48} height={260} fill={night ? "#1a2232" : "#b8d4ec"} />)}
    {Array.from({ length: 12 }, (_, i) => <rect key={i} x={1095 + i * 45} y={-40} width={42} height={260 * (1 - blinds) + 6} fill="#f4efe4" stroke="#d8d0c0" strokeWidth={2} transform={`translate(0 ${240})`} />)}
    <rect x={1070} y={190} width={580} height={440} fill="none" stroke="#f4f0e8" strokeWidth={20} /></g>
  {/* posters: a rocket, a band, a mammoth (easter egg) */}
  <rect x={200} y={230} width={200} height={270} fill="#2a4a8a" transform="rotate(-3 300 360)" /><path d="M300 270 L330 380 L270 380 Z" fill="#f4f1e8" transform="rotate(-3 300 360)" />
  <rect x={460} y={260} width={180} height={220} fill="#c8582a" /><text x={550} y={390} textAnchor="middle" fontFamily="Permanent Marker" fontSize={40} fill="#fff4d8">FIXIT</text>
  {/* desk + ORIN speaker */}
  <rect x={720} y={700} width={420} height={24} fill="#8a6a4a" /><rect x={740} y={724} width={20} height={200} fill="#6a4e34" /><rect x={1100} y={724} width={20} height={200} fill="#6a4e34" />
  <rect x={980} y={600} width={70} height={100} rx={20} fill="#2a2e38" /><OrinRing x={1015} y={640} r={22} f={f} c={red > 0.5 ? ORIN_RED : ORIN_BLUE} />
  <rect x={780} y={640} width={150} height={60} rx={6} fill="#30343e" /><rect x={786} y={646} width={138} height={48} rx={4} fill="#9ad8ff" opacity={0.6} />
  {/* bed */}
  <rect x={-200} y={760} width={760} height={170} rx={24} fill="#4a6a9a" /><rect x={-200} y={720} width={260} height={90} rx={30} fill="#f4f0e8" /><rect x={-210} y={600} width={40} height={340} fill="#6a4e34" />
  <rect x={-1200} y={930} width={4400} height={400} fill={night ? "#2a2a34" : "#b89a78"} /><AO x={-1200} y={930} w={4400} h={60} dir="down" o={0.3} />
  {!night && <Shaft pts={[[1100, 220], [1640, 220], [1300, 960], [600, 960]]} color="#fff4d0" o={0.18 * blinds} />}
  {children}
  {night && <rect x={-1200} y={-600} width={4400} height={1700} fill="#0a1020" opacity={0.25} />}
</g>;

// ---------- FIXIT repair shop: workbench (Bolt's place), gadget shelves, TV, wall landline, the old key door ----------
export const Shop: React.FC<{ f: number; children?: React.ReactNode; night?: boolean; rain?: boolean; tv?: React.ReactNode; phoneRing?: number; front?: React.ReactNode }> = ({ f, children, night, rain, tv, phoneRing = 0, front }) => <g>
  <rect x={-1200} y={-600} width={4400} height={1700} fill={night ? "#262a36" : "#d8cdb8"} />
  <Bricks x={-1200} y={-200} w={4400} h={1130} color={night ? "#2e3240" : "#c8b49a"} mortar="#000" o={0.12} />
  {/* shop window with the street */}
  <g><rect x={-560} y={180} width={560} height={560} fill={night ? "#0e1422" : "#a8cce8"} />
    {Array.from({ length: 5 }, (_, i) => <rect key={i} x={-550 + i * 110} y={420 - rnd(i, 9) * 120} width={90} height={330} fill={night ? "#161e2e" : "#c4d6e8"} />)}
    {rain && <Rain f={f} x={-560} y={180} w={560} h={560} n={60} o={0.5} />}
    <rect x={-570} y={170} width={580} height={580} fill="none" stroke="#3a3e48" strokeWidth={18} />
    <text x={-280} y={250} textAnchor="middle" fontFamily="Permanent Marker" fontSize={56} fill={night ? "#7ad0a0" : "#2f8a4e"} transform="scale(-1 1) translate(560 0)" opacity={0.85}>TIXIF</text></g>
  {/* door with the old key lock */}
  <rect x={60} y={300} width={240} height={630} fill="#5a3e2a" /><rect x={80} y={330} width={200} height={260} fill={night ? "#121828" : "#9ac0e0"} opacity={0.8} />
  <circle cx={270} cy={640} r={12} fill="#c8b06a" /><rect x={262} y={660} width={16} height={26} rx={4} fill="#2a2420" />
  {/* landline on the wall */}
  <g transform={`translate(400 ${430 + (phoneRing > 0 ? Math.sin(f * 2.4) * 3 * phoneRing : 0)})`}><rect x={-34} y={-60} width={68} height={120} rx={10} fill="#e8dcc0" /><rect x={-26} y={-52} width={52} height={36} rx={14} fill="#d4c6a4" />
    {Array.from({ length: 9 }, (_, i) => <circle key={i} cx={-14 + (i % 3) * 14} cy={4 + Math.floor(i / 3) * 14} r={4} fill="#a89878" />)}
    <path d="M30 -30 Q70 40 30 120 Q0 150 20 190" stroke="#d4c6a4" strokeWidth={5} fill="none" strokeDasharray="8 4" />
    {phoneRing > 0 && [1, 2].map(k => <path key={k} d={`M${-50 - k * 16} -40 q-10 30 0 60 M${50 + k * 16} -40 q10 30 0 60`} stroke="#ffd34a" strokeWidth={4} fill="none" opacity={phoneRing * (0.5 + 0.5 * Math.sin(f * 0.8 + k))} />)}</g>
  {/* shelves with gadgets */}
  {[0, 1, 2].map(r => <g key={r}><rect x={560} y={260 + r * 150} width={620} height={14} fill="#6a5040" />
    {Array.from({ length: 7 }, (_, i) => { const c = ["#3a3e48", "#c8402e", "#3a6ad8", "#e8e2d4", "#2f8a4e", "#d8a03a"][(i + r) % 6]; const w = 50 + rnd(i, r) * 40;
      return <rect key={i} x={575 + i * 85} y={260 + r * 150 - 40 - rnd(i, r + 4) * 50} width={w} height={40 + rnd(i, r + 4) * 50} rx={6} fill={c} />; })}</g>)}
  {/* TV */}
  <g transform="translate(1300 250)"><rect x={0} y={0} width={420} height={250} rx={10} fill="#16181e" /><rect x={12} y={12} width={396} height={226} fill="#0e1a2a" />
    <svg x={12} y={12} width={396} height={226} viewBox="0 0 396 226">{tv}</svg></g>
  {/* workbench */}
  <rect x={540} y={760} width={1280} height={30} fill="#7a5a3e" /><rect x={560} y={790} width={24} height={140} fill="#5a4230" /><rect x={1780} y={790} width={24} height={140} fill="#5a4230" />
  <Wood x={540} y={760} w={1280} h={30} color="#7a5a3e" rows={2} />
  {/* clutter: soldering iron, cables, a newspaper (zombie easter egg) */}
  <rect x={1480} y={730} width={150} height={30} fill="#f0ece0" transform="rotate(-4 1555 745)" /><text x={1490} y={752} fontFamily="Inter" fontWeight={900} fontSize={11} fill="#2a2a2a" transform="rotate(-4 1555 745)">ATLANTA: ONE YEAR AFTER</text>
  <path d="M620 760 Q680 700 760 740 Q820 770 880 730" stroke="#2a2e38" strokeWidth={5} fill="none" /><rect x={1660} y={700} width={22} height={60} rx={4} fill="#d8a03a" />
  {night && <Glow x={1100} y={600} r={700} color="#ffcf8a" o={0.25} />}
  <rect x={-1200} y={930} width={4400} height={400} fill={night ? "#2a2c34" : "#8a7a68"} /><AO x={-1200} y={930} w={4400} h={50} dir="down" o={0.3} />
  {children}
  {front}
</g>;

// ---------- rainy night street, dead streetlights, an alley mouth (the cold open) ----------
export const NightStreet: React.FC<{ f: number; children?: React.ReactNode; alley?: number; flood?: boolean; behind?: React.ReactNode }> = ({ f, children, alley = 0, flood = true, behind }) => <g>
  <Sky top="#070b14" bot="#1a2232" />
  {Array.from({ length: 14 }, (_, i) => { const x = -1100 + i * 320, h = 420 + rnd(i, 2) * 360; return <g key={i}><rect x={x} y={900 - h} width={300} height={h} fill={i % 2 ? "#141a26" : "#18202e"} />
    {Array.from({ length: 18 }, (_, j) => <rect key={j} x={x + 26 + (j % 3) * 90} y={900 - h + 40 + Math.floor(j / 3) * 70} width={50} height={36} fill={rnd(i * 31 + j, 5) > 0.86 ? "#ffcf7a" : "#0e1420"} opacity={0.8} />)}</g>; })}
  {/* alley between two buildings at x 980–1240 */}
  <rect x={980} y={300} width={260} height={600} fill="#06080e" />
  {behind}
  {alley > 0 && <g><Glow x={1110} y={600} r={260} color={ORIN_RED} o={0.25 * alley} /></g>}
  {/* dead streetlights */}
  {[-500, 500, 1500, 2500].map((x, i) => <g key={i}><rect x={x} y={420} width={12} height={480} fill="#2a2e38" /><path d={`M${x + 6} 420 q0 -30 60 -30 l40 0`} stroke="#2a2e38" strokeWidth={10} fill="none" /><rect x={x + 90} y={384} width={50} height={14} rx={6} fill="#3a3e48" /></g>)}
  <rect x={-1200} y={900} width={4400} height={500} fill="#12161e" />
  {flood && <rect x={-1200} y={900} width={4400} height={500} fill="#2a3448" opacity={0.35} />}
  {flood && Array.from({ length: 30 }, (_, i) => { const x = -1000 + rnd(i, 7) * 4000, y = 930 + rnd(i, 8) * 140, t = ((f * 0.05 + rnd(i, 9)) % 1); return <ellipse key={i} cx={x} cy={y} rx={10 + 40 * t} ry={3 + 10 * t} fill="none" stroke="#8aa8d8" strokeWidth={2} opacity={0.5 * (1 - t)} />; })}
  {children}
  <Rain f={f} x={-1200} y={-400} w={4400} h={1500} n={260} o={0.4} />
</g>;

// ---------- the city panorama: day (smart, busy) / locked (all red) / dark (blackout, Milky Way) ----------
export const CityWide: React.FC<{ f: number; mode?: "day" | "locked" | "dark" | "dawn"; children?: React.ReactNode; drones?: number }> = ({ f, mode = "day", children, drones = 0 }) => {
  const day = mode === "day" || mode === "dawn", dark = mode === "dark";
  return <g>
    <Sky top={mode === "day" ? "#5a9ae0" : mode === "dawn" ? "#f0a070" : mode === "locked" ? "#2a1e2a" : "#02040a"} bot={mode === "day" ? "#cfe4f4" : mode === "dawn" ? "#ffe0b0" : mode === "locked" ? "#5a2a2a" : "#0a1020"} />
    {dark && <g>{Array.from({ length: 420 }, (_, i) => { const x = -400 + rnd(i, 1) * 2800, band = 300 - (x - 960) * 0.25 + (rnd(i, 2) - 0.5) * 260 * (rnd(i, 3) > 0.6 ? 1 : 0.4); return <circle key={i} cx={x} cy={band} r={0.8 + rnd(i, 4) * 2.2} fill="#fff" opacity={0.3 + 0.7 * rnd(i, 5)} />; })}
      <path d="M-400 520 Q960 120 2400 -220" stroke="#c8d0ff" strokeWidth={180} opacity={0.08} fill="none" /><path d="M-400 520 Q960 120 2400 -220" stroke="#fff4e0" strokeWidth={60} opacity={0.07} fill="none" /></g>}
    {Array.from({ length: 22 }, (_, i) => { const x = -900 + i * 190 + rnd(i, 3) * 60, h = 260 + rnd(i, 4) * 420, w = 130 + rnd(i, 5) * 60;
      const c = day ? (i % 3 ? "#8aa0bc" : "#a8bcd4") : dark ? "#06080e" : "#1a1420";
      return <g key={i}><rect x={x} y={860 - h} width={w} height={h} fill={c} />
        {!dark && Array.from({ length: Math.floor(h / 60) * 3 }, (_, j) => <rect key={j} x={x + 14 + (j % 3) * (w / 3)} y={860 - h + 20 + Math.floor(j / 3) * 60} width={w / 3 - 24} height={30} fill={day ? "#d8ecff" : mode === "locked" ? "#ffb46a" : "#ffcf7a"} opacity={day ? 0.5 : 0.75} />)}
        {mode === "locked" && <circle cx={x + w / 2} cy={860 - h - 12} r={7} fill={ORIN_RED} opacity={0.6 + 0.4 * Math.sin(f * 0.2 + i)} />}</g>; })}
    <rect x={-1200} y={860} width={4400} height={500} fill={day ? "#5a6270" : "#0e1016"} />
    {/* traffic lights row (locked = all red) */}
    {mode !== "dark" && [-300, 300, 900, 1500, 2100].map((x, i) => <g key={i}><rect x={x} y={760} width={8} height={100} fill="#2a2e38" /><rect x={x - 12} y={720} width={32} height={60} rx={6} fill="#1a1c22" />
      <circle cx={x + 4} cy={736} r={8} fill={mode === "locked" ? ORIN_RED : "#4a2020"} /><circle cx={x + 4} cy={762} r={8} fill={mode === "locked" ? "#203a20" : "#3aff7a"} /></g>)}
    {drones > 0 && Array.from({ length: Math.round(14 * drones) }, (_, i) => { const x = (rnd(i, 11) * 2600 + f * (2 + rnd(i, 12) * 3)) % 2800 - 400, y = 120 + rnd(i, 13) * 420;
      return <g key={i} transform={`translate(${x} ${y + Math.sin(f * 0.2 + i) * 6})`}><rect x={-16} y={-4} width={32} height={8} rx={4} fill={day ? "#2a2e38" : "#0a0c12"} /><line x1={-24} y1={-6} x2={-8} y2={-6} stroke="#888" strokeWidth={2} /><line x1={8} y1={-6} x2={24} y2={-6} stroke="#888" strokeWidth={2} />
        <circle cx={0} cy={6} r={3} fill={mode === "locked" ? ORIN_RED : ORIN_BLUE} /></g>; })}
    {children}
  </g>; };

// ---------- desert data centre ORIN-1 at night: glowing halls, fence, searchlights, the gate ----------
export const DataCenter: React.FC<{ f: number; children?: React.ReactNode; gate?: number; fight?: number; lights?: number }> = ({ f, children, gate = 0, fight = 0, lights = 1 }) => <g>
  <Sky top="#04060c" bot="#1a1830" />
  {Array.from({ length: 120 }, (_, i) => <circle key={i} cx={-600 + rnd(i, 1) * 3200} cy={-300 + rnd(i, 2) * 700} r={1 + rnd(i, 3) * 1.6} fill="#fff" opacity={0.5 * rnd(i, 4)} />)}
  <path d="M-1200 700 Q-400 600 300 680 Q900 620 1600 690 Q2400 630 3200 700 L3200 900 L-1200 900 Z" fill="#1a1620" />
  {/* the building: three long halls + a cooling block */}
  <g opacity={0.6 + 0.4 * lights}>
    {[0, 1, 2].map(i => <g key={i}><rect x={180 + i * 520} y={420 - i * 20} width={480} height={330 + i * 20} fill="#1e2230" /><rect x={180 + i * 520} y={420 - i * 20} width={480} height={18} fill="#2c3244" />
      {Array.from({ length: 12 }, (_, j) => <rect key={j} x={200 + i * 520 + j * 38} y={470 - i * 20} width={22} height={240} fill={ORIN_BLUE} opacity={(0.25 + 0.2 * rnd(j, i)) * lights} />)}</g>)}
    {[0, 1, 2, 3].map(i => <g key={i}><rect x={1760 + i * 90} y={560} width={70} height={190} fill="#262a36" /><circle cx={1795 + i * 90} cy={548} r={30} fill="#2e3442" /><circle cx={1795 + i * 90} cy={548} r={22} fill="none" stroke="#4a5266" strokeWidth={4} strokeDasharray="10 6" transform={`rotate(${f * 6 * lights} ${1795 + i * 90} 548)`} /></g>)}
    <OrinRing x={960} y={330} r={46} f={f} o={lights} />
    <text x={960} y={260} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={40} fill="#cfe8ff" opacity={0.85 * lights} letterSpacing={8}>ORIN-1</text>
    <text x={960} y={410} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={20} fill="#8aa8c8" opacity={0.8 * lights} letterSpacing={6}>WHATIF LABS</text>
    <Glow x={960} y={600} r={1100} color={ORIN_BLUE} o={0.18 * lights} />
  </g>
  {/* searchlights */}
  {lights > 0.3 && [0, 1].map(i => { const a = Math.sin(f * 0.03 + i * 2) * 0.6; return <path key={i} d={`M${400 + i * 1100} 740 L${400 + i * 1100 + Math.sin(a) * 1400 - 120} -300 L${400 + i * 1100 + Math.sin(a) * 1400 + 120} -300 Z`} fill="#e8f4ff" opacity={0.07} />; })}
  <rect x={-1200} y={750} width={4400} height={600} fill="#2a2420" /><Noise x={-1200} y={750} w={4400} h={400} o={0.15} />
  {/* fence + gate */}
  <g>{Array.from({ length: 34 }, (_, i) => <line key={i} x1={-700 + i * 100} y1={720} x2={-700 + i * 100} y2={860} stroke="#5a5e68" strokeWidth={6} />)}
    <path d="M-700 730 L2700 730 M-700 790 L2700 790 M-700 850 L2700 850" stroke="#5a5e68" strokeWidth={3} />
    <path d="M-700 720 L2700 720" stroke="#8a8e98" strokeWidth={3} strokeDasharray="6 10" />
    <g transform={`translate(860 0) rotate(${gate * 70} 0 860)`}><rect x={0} y={710} width={200} height={150} fill="none" stroke="#9aa0aa" strokeWidth={8} /><path d="M0 710 L200 860 M200 710 L0 860" stroke="#9aa0aa" strokeWidth={5} /></g></g>
  {/* sandbags (the soldiers' line) */}
  {fight > 0 && Array.from({ length: 16 }, (_, i) => <ellipse key={i} cx={-500 + (i % 8) * 70} cy={960 - Math.floor(i / 8) * 26} rx={38} ry={16} fill="#8a7a5a" stroke="#5a4e3a" strokeWidth={3} />)}
  {children}
</g>;

// ---------- server hall: endless rows in perspective (row 2026), blue light, the red breaker at the end ----------
export const ServerHall: React.FC<{ f: number; children?: React.ReactNode; off?: number; screens?: React.ReactNode; handle?: number }> = ({ f, children, off = 0, screens, handle = 0 }) => {
  // off 0..1 = darkness wave rolling from the far end towards the camera
  const rowOn = (k: number) => 1 - sat((off * 1.4 - (1 - k)) / 0.25);
  return <g>
    <rect x={-1200} y={-600} width={4400} height={1700} fill="#05070c" />
    {/* ceiling + floor perspective to vanishing point (960, 470) */}
    <path d="M-1200 -200 L960 470 L3200 -200 Z" fill="#0c1018" /><path d="M-1200 1300 L960 470 L3200 1300 Z" fill="#10141c" />
    {Array.from({ length: 12 }, (_, i) => { const k = i / 12, z = Math.pow(1 - k, 1.6); const lw = 960 - 1500 * z, rw = 960 + 1500 * z, top = 470 - 560 * z, bot = 470 + 620 * z, on = rowOn(k);
      return <g key={i}>
        <path d={`M${lw} ${top} L${lw + 120 * z} ${top + 30 * z} L${lw + 120 * z} ${bot - 20 * z} L${lw} ${bot} Z`} fill="#1a1e28" />
        <path d={`M${rw} ${top} L${rw - 120 * z} ${top + 30 * z} L${rw - 120 * z} ${bot - 20 * z} L${rw} ${bot} Z`} fill="#1a1e28" />
        {Array.from({ length: 8 }, (_, j) => <g key={j}><circle cx={lw + 30 * z + (j % 2) * 50 * z} cy={top + 60 * z + j * 60 * z} r={5 * z + 1} fill={j === 3 && i % 4 === 1 ? "#ffb02a" : ORIN_BLUE} opacity={on * (0.5 + 0.5 * Math.sin(f * 0.4 + i * 3 + j))} />
          <circle cx={rw - 30 * z - (j % 2) * 50 * z} cy={top + 60 * z + j * 60 * z} r={5 * z + 1} fill={ORIN_BLUE} opacity={on * (0.5 + 0.5 * Math.sin(f * 0.37 + i * 5 + j))} /></g>)}
        {i === 3 && <text x={lw + 60 * z} y={top - 10} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={40 * z} fill="#8ab0d8" opacity={0.6 * on}>2026</text>}
        <rect x={lw + 140 * z} y={top - 20 * z} width={rw - lw - 280 * z} height={6 * z + 1} fill={ORIN_BLUE} opacity={0.35 * on} /></g>; })}
    <Glow x={960} y={470} r={900} color={ORIN_BLUE} o={0.25 * (1 - off)} />
    {screens}
    {/* the breaker at the end of the hall */}
    <g transform="translate(960 560)"><rect x={-70} y={-120} width={140} height={200} rx={10} fill="#3a3e48" stroke="#ffd34a" strokeWidth={6} strokeDasharray="14 10" />
      <rect x={-12} y={-80} width={24} height={110} rx={6} fill="#1a1c22" /><g transform={`rotate(${lerp(-30, 40, handle)} 0 30)`}><rect x={-10} y={-80} width={20} height={110} rx={8} fill="#d83a2a" /><rect x={-34} y={-96} width={68} height={24} rx={10} fill="#e8402e" /></g>
      <text x={0} y={110} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={20} fill="#ffd34a">MAIN</text></g>
    {children}
    <rect x={-1200} y={-600} width={4400} height={1700} fill="#000" opacity={0.85 * sat((off - 0.75) / 0.25)} />
  </g>; };

// ---------- railway-tunnel bunker: string lights, cots, the map table, a Humvee in the back ----------
export const Tunnel: React.FC<{ f: number; children?: React.ReactNode; back?: React.ReactNode }> = ({ f, children, back }) => <g>
  <rect x={-1200} y={-600} width={4400} height={1700} fill="#14110e" />
  <path d="M-600 960 L-600 380 Q-600 -60 960 -80 Q2520 -60 2520 380 L2520 960 Z" fill="#3a332c" />
  <Bricks x={-600} y={-80} w={3120} h={1040} color="#4a4038" mortar="#000" o={0.18} />
  <path d="M-300 960 L-300 420 Q-300 80 960 70 Q2220 80 2220 420 L2220 960 Z" fill="#2a241e" />
  {/* rails */}
  <path d="M600 960 L860 560 M1320 960 L1060 560" stroke="#6a5e50" strokeWidth={8} />{Array.from({ length: 7 }, (_, i) => { const t = i / 7, y = 960 - 400 * t, w = 380 - 260 * t; return <rect key={i} x={960 - w} y={y - 6} width={w * 2} height={10 - 6 * t} fill="#4a3e32" />; })}
  <ellipse cx={960} cy={560} rx={190} ry={130} fill="#0a0806" opacity={0.35} />
  {back}
  {/* string lights */}
  {[0, 1].map(r => <g key={r}><path d={`M-300 ${260 + r * 60} Q960 ${400 + r * 60} 2220 ${260 + r * 60}`} stroke="#2a2420" strokeWidth={3} fill="none" />
    {Array.from({ length: 22 }, (_, i) => { const t = i / 21, x = -300 + t * 2520, y = 260 + r * 60 + 4 * (400 - 260) * t * (1 - t) / 1 * 0.5 + 2; return <g key={i}><circle cx={x} cy={y + 10} r={7} fill="#ffcf7a" opacity={0.85 + 0.15 * Math.sin(f * 0.3 + i)} /><Glow x={x} y={y + 10} r={40} color="#ffcf7a" o={0.25} /></g>; })}</g>)}
  {/* cots + crates */}
  {[-200, 60, 1700, 1960].map((x, i) => <g key={i}><rect x={x} y={880} width={220} height={22} rx={6} fill="#5e6a42" /><line x1={x + 10} y1={900} x2={x + 10} y2={960} stroke="#3a3e30" strokeWidth={6} /><line x1={x + 210} y1={900} x2={x + 210} y2={960} stroke="#3a3e30" strokeWidth={6} /></g>)}
  {[[340, 880], [420, 840], [1480, 880]].map(([x, y], i) => <g key={i}><rect x={x} y={y} width={90} height={80} fill="#6a5a3a" stroke="#4a3e28" strokeWidth={4} /><path d={`M${x} ${y} L${x + 90} ${y + 80} M${x + 90} ${y} L${x} ${y + 80}`} stroke="#4a3e28" strokeWidth={3} /></g>)}
  <rect x={-1200} y={960} width={4400} height={400} fill="#1e1a16" /><AO x={-1200} y={960} w={4400} h={60} dir="down" o={0.35} />
  <Glow x={960} y={500} r={1200} color="#ffb060" o={0.12} />
  {children}
</g>;
