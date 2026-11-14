// Chapter 4 sets: a neon strip at night (original casino names), the casino floor with a blackjack table, and Lina's
// bedroom at night (present day; also reused later). Palette: magenta + gold neon, deep purple shadows.
import React from "react";
import { Layer, rnd, W, H, sat, lerp } from "../engine/core";
import { Glow, Bokeh, Shaft } from "../engine/fx";
import { Noise, Wood, Wallpaper, AO } from "../engine/tex";
import { Character, Pose, SIT, walkPose } from "../chars/Rig2";
import { LINA, LINA_ADULT, SAM, MANAGER, GUARD, EXTRAS } from "../chars/cast";

const GOLD = "#ffc94a", MAG = "#ff3aa8";
const Neon: React.FC<{ x: number; y: number; text: string; size: number; color: string; f: number; flick?: number }> = ({ x, y, text, size, color, f, flick = 0 }) => {
  const on = flick && (f + flick * 13) % 97 < 3 ? 0.3 : 1;
  return <g opacity={on}><text x={x} y={y} fontFamily="Inter" fontWeight={900} fontSize={size} fill={color} textAnchor="middle" style={{ filter: `drop-shadow(0 0 ${size * 0.25}px ${color}) drop-shadow(0 0 ${size * 0.6}px ${color})` }}>{text}</text>
    <text x={x} y={y} fontFamily="Inter" fontWeight={900} fontSize={size} fill="#fff" opacity={0.55} textAnchor="middle">{text}</text></g>;
};

// the strip: Lina (adult) and Sam walk toward the casino entrance (x0 → x1 by k)
export const VegasStreet: React.FC<{ f: number; walkX: number; still?: Pose | null }> = ({ f, walkX, still = null }) => <>
  <Layer depth={0.3}>
    <rect x={-1000} y={-500} width={3920} height={1300} fill="#12081f" />
    <Glow x={960} y={600} r={1400} color="#6a1a8a" o={0.5} />
    {Array.from({ length: 14 }, (_, i) => { const x = -900 + i * 300, h = 350 + rnd(i, 1) * 350; return <g key={i}><rect x={x} y={640 - h} width={240} height={h + 200} fill="#1c1030" />
      {Array.from({ length: 40 }, (_, k) => <rect key={k} x={x + 14 + (k % 5) * 44} y={660 - h + Math.floor(k / 5) * 40} width={22} height={18} fill={rnd(i * 40 + k, 3) > 0.6 ? "#ffd890" : "#2a1a40"} />)}</g>; })}
  </Layer>
  <Layer depth={0.75}>
    <rect x={-900} y={60} width={1300} height={640} fill="#2a1240" />
    <Neon x={-250} y={260} text="THE LUCKY STAR" size={110} color={MAG} f={f} flick={1} />
    {Array.from({ length: 24 }, (_, i) => <circle key={i} cx={-860 + i * 52} cy={330} r={9} fill={(i + Math.floor(f / 4)) % 3 === 0 ? GOLD : "#6a4a20"} />)}
    <rect x={520} y={0} width={1300} height={700} fill="#20123a" />
    <Neon x={1170} y={210} text="ORBIT CASINO" size={120} color={GOLD} f={f} />
    <path d="M820 300 L1520 300 L1450 380 L890 380 Z" fill="#3a1a5a" />{Array.from({ length: 16 }, (_, i) => <circle key={i} cx={860 + i * 42} cy={340} r={8} fill={(i + Math.floor(f / 3)) % 2 ? MAG : GOLD} />)}
    <rect x={960} y={400} width={420} height={300} fill="#ffcf7a" opacity={0.85} /><rect x={1160} y={400} width={20} height={300} fill="#3a1a5a" />
    <Glow x={1170} y={560} r={500} color="#ffcf7a" o={0.45} />
  </Layer>
  <Layer depth={1}>
    <rect x={-1000} y={700} width={3920} height={600} fill="#1a1024" />
    <rect x={-1000} y={700} width={3920} height={600} fill="url(#vwet)" />
    <defs><linearGradient id="vwet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={MAG} stopOpacity={0.25} /><stop offset="0.5" stopColor={GOLD} stopOpacity={0.08} /><stop offset="1" stopColor="#000" stopOpacity={0} /></linearGradient></defs>
    {/* car light trails on the road */}
    {[0, 1, 2].map(i => <rect key={i} x={((f * (30 + i * 12) + i * 700) % 4200) - 1200} y={1010 + i * 22} width={500} height={6} rx={3} fill={i === 1 ? "#ff5a5a" : "#fff2c8"} opacity={0.7} style={{ filter: "blur(2px)" }} />)}
    <Character look={LINA_ADULT} pose={still ? { facing: -1, look: [0.6, -0.2], ...still } : { ...walkPose((walkX + 3000) / 290 * Math.PI * 2), facing: 1, look: [0.8, -0.3], mouth: "smile" }} x={walkX} y={860} f={f} seed={1} rim={{ dx: 4, dy: -3, color: MAG }} />
    <Character look={{ ...SAM, scale: 1.06 }} pose={still ? { facing: 1, look: [0.7, -0.2], mouth: "o", eyes: 1.15, brow: 0.6 } : { ...walkPose((walkX + 3140) / 290 * Math.PI * 2), facing: 1, look: [0.8, -0.3], mouth: "grin", brow: 0.6 }} x={walkX - 190} y={860} f={f} seed={3} rim={{ dx: 4, dy: -3, color: GOLD }} />
    <Bokeh x={-600} y={120} w={3200} h={600} n={30} colors={[MAG, GOLD, "#7a5aff"]} seed={11} f={f} />
  </Layer>
</>;

// casino floor: slot machines + bokeh behind, blackjack table in the middle; Lina seated, Sam standing behind her
export const Casino: React.FC<{ f: number; lina: Pose; sam: Pose; chips?: number; guards?: number; manager?: Pose | null; dealCards?: number }> = ({ f, lina, sam, chips = 0, guards = 0, manager = null, dealCards = 3 }) => <>
  <Layer depth={0.5}>
    <rect x={-1000} y={-500} width={3920} height={1300} fill="#1c0a24" />
    <Wallpaper x={-1000} y={-500} w={3920} h={1100} base="#2a0f30" ink={GOLD} kind="diamond" o={0.12} />
    {Array.from({ length: 12 }, (_, i) => { const x = -800 + i * 300; return <g key={i}><rect x={x} y={300} width={200} height={360} rx={20} fill="#3a1a4a" /><rect x={x + 20} y={330} width={160} height={110} rx={10} fill={i % 2 ? "#ff5ab0" : "#ffc94a"} opacity={0.7} />
      {[0, 1, 2].map(k => <rect key={k} x={x + 30 + k * 50} y={350} width={40} height={70} rx={6} fill="#fff6e0" />)}<circle cx={x + 100} cy={300} r={18} fill={(f + i * 7) % 20 < 10 ? MAG : GOLD} /></g>; })}
    <Bokeh x={-900} y={-200} w={3700} h={700} n={50} colors={[MAG, GOLD, "#7a5aff"]} seed={5} f={f} />
    {[0, 1, 2].map(i => <g key={i}><rect x={-400 + i * 1100} y={-120} width={600} height={40} rx={20} fill="#ffe8a0" opacity={0.6} /><Glow x={-100 + i * 1100} y={-100} r={400} color={GOLD} o={0.3} /></g>)}
  </Layer>
  <Layer depth={1}>
    <rect x={-1000} y={720} width={3920} height={600} fill="#2a0a1a" />
    <rect x={-1000} y={720} width={3920} height={600} fill="url(#cpat)" opacity={0.25} />
    <defs><pattern id="cpat" width={80} height={80} patternUnits="userSpaceOnUse"><circle cx={40} cy={40} r={14} fill="none" stroke={GOLD} strokeWidth={4} /><circle cx={0} cy={0} r={8} fill={MAG} /></pattern></defs>
    {/* dealer behind the table */}
    <Character look={{ ...EXTRAS[5], top: "#f2f2f2", style: "suit", tie: "#c8302c" }} pose={{ facing: -1, lean: 10, aR: [50, 30], aL: [44, 30], look: [-0.5, 0.4] }} x={1250} y={820} s={0.95} f={f} seed={8} />
    {/* Lina on a stool, Sam behind her */}
    <rect x={640} y={720} width={120} height={14} rx={6} fill="#c8a03a" /><line x1={700} y1={734} x2={700} y2={860} stroke="#8a6a2a" strokeWidth={10} />
    <Character look={{ ...SAM, scale: 1.06 }} pose={{ facing: 1, ...sam }} x={520} y={870} f={f} seed={3} rim={{ dx: 4, dy: -3, color: MAG }} />
    <Character look={LINA_ADULT} pose={{ ...SIT, facing: 1, ...lina }} x={700} y={860} f={f} seed={1} rim={{ dx: 4, dy: -3, color: GOLD }} />
    {/* blackjack table: green felt half-moon with gold rail */}
    <path d="M560 700 L1460 700 Q1460 790 1010 800 Q560 790 560 700 Z" fill="#0f6a3a" />
    <path d="M560 700 L1460 700" stroke="#c8a03a" strokeWidth={14} />
    <path d="M560 706 Q1010 830 1460 706" stroke="#5a2a10" strokeWidth={22} fill="none" />
    <text x={1010} y={760} fontFamily="Inter" fontWeight={900} fontSize={22} fill="#e8d890" textAnchor="middle" opacity={0.7}>BLACKJACK PAYS 3 TO 2</text>
    {/* the shoe + dealt cards + Lina's chip stacks (grow with chips 0..1) */}
    <rect x={1300} y={668} width={90} height={34} rx={6} fill="#3a1a1a" /><rect x={1306} y={672} width={60} height={26} fill="#2a4a9a" />
    {Array.from({ length: dealCards }, (_, i) => <g key={i} transform={`translate(${1090 + i * 46} 688) rotate(${-8 + i * 6})`}><rect x={-20} y={-28} width={40} height={56} rx={4} fill="#fdfbf4" stroke="#222" strokeWidth={1.5} /><text x={-12} y={-8} fontFamily="Inter" fontWeight={900} fontSize={16} fill={i % 2 ? "#c8302c" : "#111"}>{["A", "K", "10", "Q", "J"][i % 5]}</text></g>)}
    {Array.from({ length: 5 }, (_, c) => { const n = Math.floor(2 + chips * (5 + c)); return <g key={c}>{Array.from({ length: n }, (_, k) => <g key={k}><ellipse cx={850 + c * 40} cy={700 - k * 7} rx={18} ry={6} fill={["#c8302c", "#2a6ad8", "#1a1a1a", "#2aa85a", GOLD][c]} /><ellipse cx={850 + c * 40} cy={698 - k * 7} rx={18} ry={6} fill="none" stroke="#fff" strokeWidth={2} strokeDasharray="4 4" /></g>)}</g>; })}
    {/* guards walk in from the right, manager between them */}
    {guards > 0 && <>
      <Character look={GUARD} pose={{ ...walkPose(lerp(2260, 1600, guards) / 290 * -Math.PI * 2), facing: -1, mouth: "flat", brow: -0.4 }} x={lerp(2260, 1600, guards)} y={880} f={f} seed={12} />
      <Character look={GUARD} pose={{ ...walkPose(lerp(2720, 2080, guards) / 290 * -Math.PI * 2), facing: -1, mouth: "flat", brow: -0.4 }} x={lerp(2720, 2080, guards)} y={880} f={f} seed={13} />
    </>}
    {manager && <Character look={MANAGER} pose={{ facing: -1, ...manager }} x={lerp(2500, 1840, guards)} y={870} f={f} seed={14} rim={{ dx: -4, dy: -3, color: GOLD }} />}
    <Glow x={1010} y={600} r={700} color={GOLD} o={0.18} />
  </Layer>
</>;

// Lina's bedroom at night (present). Desk + lamp, bed, posters, window with the moon; phone on the desk.
export const Bedroom: React.FC<{ f: number; lina: Pose; phoneGlow?: number; seated?: boolean; onBed?: boolean; lamp?: number }> = ({ f, lina, phoneGlow = 0, seated = true, onBed = false, lamp = 1 }) => <>
  <Layer depth={0.7}>
    <rect x={-800} y={-400} width={3520} height={1200} fill="#1e2440" />
    <Wallpaper x={-800} y={-400} w={3520} h={1100} base="#232a4a" ink="#4a5a8a" kind="stripe" o={0.12} />
    <rect x={1150} y={120} width={420} height={380} fill="#0e1430" /><circle cx={1460} cy={210} r={46} fill="#f4eccc" /><Glow x={1460} y={210} r={180} color="#f4eccc" o={0.35} />
    <rect x={1140} y={110} width={440} height={400} fill="none" stroke="#3a4468" strokeWidth={16} /><line x1={1360} y1={120} x2={1360} y2={500} stroke="#3a4468" strokeWidth={10} />
    <rect x={200} y={150} width={180} height={240} fill="#e3a83b" opacity={0.8} /><rect x={420} y={190} width={160} height={200} fill="#6ab0d8" opacity={0.7} />
    <circle cx={290} cy={260} r={50} fill="#1f6f78" opacity={0.8} />
    <Shaft pts={[[1160, 130], [1560, 130], [1400, 1100], [700, 1100]]} color="#9ab8ff" o={0.12} />
  </Layer>
  <Layer depth={1}>
    <Wood x={-900} y={760} w={3720} h={600} color="#3a2a30" rows={10} />
    <AO x={-900} y={760} w={3720} h={70} dir="up" o={0.4} />
    {/* bed on the right */}
    {onBed ? <><rect x={1260} y={770} width={760} height={90} rx={16} fill="#3a4a7a" /><rect x={1270} y={730} width={170} height={60} rx={22} fill="#d8dcec" /><path d={`M1700 770 Q1800 740 2020 760 L2020 790 L1700 790 Z`} fill="#4a5a8a" /></>
      : <><rect x={1300} y={640} width={700} height={140} rx={20} fill="#3a4a7a" /><rect x={1300} y={600} width={160} height={70} rx={24} fill="#d8dcec" /><rect x={1290} y={520} width={30} height={270} fill="#2a2030" /></>}
    {/* desk + lamp + phone */}
    <rect x={500} y={690} width={520} height={20} rx={4} fill="#6a4a3a" /><rect x={520} y={710} width={14} height={150} fill="#3a2a24" /><rect x={986} y={710} width={14} height={150} fill="#3a2a24" />
    <ellipse cx={930} cy={688} rx={34} ry={8} fill="#2a2a34" /><path d="M930 688 L936 570 L880 524" stroke="#2a2a34" strokeWidth={8} fill="none" strokeLinecap="round" /><path d="M852 516 L908 516 L928 562 L832 562 Z" fill="#e3a83b" /><ellipse cx={880} cy={562} rx={48} ry={7} fill="#fff2c0" />
    <Glow x={880} y={600} r={380} color="#ffd890" o={0.55 * lamp} />
    <Shaft pts={[[836, 562], [924, 562], [1010, 690], [740, 690]]} color="#ffd890" o={0.3 * lamp} blur={10} />
    <rect x={760} y={680} width={44} height={12} rx={3} fill="#16151c" />{phoneGlow > 0 && <><rect x={762} y={681} width={40} height={9} rx={2} fill="#7fd0ff" opacity={phoneGlow} /><Glow x={782} y={680} r={120} color="#7fd0ff" o={0.6 * phoneGlow} /></>}
    {seated && !onBed && <><rect x={560} y={600} width={18} height={180} rx={6} fill="#4a3a5a" /><rect x={560} y={770} width={130} height={16} rx={5} fill="#5a4a6a" /></>}
    {onBed ? <Character look={LINA} pose={{ ...SIT, facing: -1, ...lina }} x={1560} y={856} f={f} seed={1} rim={{ dx: -4, dy: -3, color: "#9ab8ff" }} />
      : <Character look={LINA} pose={seated ? { ...SIT, facing: 1, ...lina } : { facing: 1, ...lina }} x={630} y={860} f={f} seed={1} rim={{ dx: 4, dy: -3, color: "#ffd890" }} />}
  </Layer>
</>;

// the counting data-viz: dealt cards fly into a glowing memory column; a meter shows the deck turning in her favour
export const CountViz: React.FC<{ f: number }> = ({ f }) => {
  const n = Math.min(40, Math.floor(f / 2)), tilt = sat(f / 80);
  return <svg width={W} height={H} style={{ position: "absolute" }}>
    <rect width={W} height={H} fill="#12081f" /><Glow x={700} y={540} r={800} color={MAG} o={0.15} /><Glow x={1400} y={540} r={600} color={GOLD} o={0.12} />
    <rect x={160} y={100} width={1000} height={760} rx={30} fill="#0f6a3a" opacity={0.9} /><rect x={160} y={100} width={1000} height={760} rx={30} fill="none" stroke="#c8a03a" strokeWidth={12} />
    <text x={660} y={170} fontFamily="Inter" fontWeight={900} fontSize={44} fill="#e8d890" textAnchor="middle">6 DECKS · 312 CARDS</text>
    {Array.from({ length: n }, (_, i) => { const col = i % 10, row = Math.floor(i / 10), t = sat((f - i * 2) / 12);
      return <g key={i} transform={`translate(${lerp(1100, 230 + col * 92, t)} ${lerp(160, 230 + row * 150, t)}) rotate(${(1 - t) * 30})`}><rect x={-36} y={-52} width={72} height={104} rx={8} fill="#fdfbf4" stroke={GOLD} strokeWidth={t > 0.9 ? 3 : 0} />
        <text x={0} y={14} fontFamily="Inter" fontWeight={900} fontSize={34} fill={i % 2 ? "#c8302c" : "#111"} textAnchor="middle">{["2", "5", "K", "7", "A", "3", "10", "6", "Q", "4", "9", "J", "8"][i % 13]}</text></g>; })}
    <g transform="translate(1520 480)">
      <text x={0} y={-330} fontFamily="Inter" fontWeight={900} fontSize={38} fill="#fff" textAnchor="middle">CARDS LEFT IN THE SHOE</text>
      <rect x={-200} y={-280} width={180} height={520} rx={18} fill="#2a1a3a" /><rect x={20} y={-280} width={180} height={520} rx={18} fill="#2a1a3a" />
      <rect x={-200} y={240 - 520 * (0.5 - 0.22 * tilt)} width={180} height={520 * (0.5 - 0.22 * tilt)} rx={18} fill="#5a7aff" />
      <rect x={20} y={240 - 520 * (0.5 + 0.3 * tilt)} width={180} height={520 * (0.5 + 0.3 * tilt)} rx={18} fill={GOLD} />
      <text x={-110} y={300} fontFamily="Inter" fontWeight={900} fontSize={34} fill="#9ab0ff" textAnchor="middle">LOW</text><text x={110} y={300} fontFamily="Inter" fontWeight={900} fontSize={34} fill={GOLD} textAnchor="middle">HIGH</text>
      {tilt > 0.8 && <text x={0} y={380} fontFamily="Inter" fontWeight={900} fontSize={44} fill={GOLD} textAnchor="middle" style={{ filter: `drop-shadow(0 0 12px ${GOLD})` }}>BET BIG</text>}
    </g>
  </svg>;
};

// incoming call on Lina's phone (close-up): "Grandma Ayla" with a little portrait, pulsing rings
export const PhoneCall: React.FC<{ f: number }> = ({ f }) => <svg width={W} height={H} style={{ position: "absolute" }}>
  <rect width={W} height={H} fill="#3a2a30" /><Glow x={960} y={540} r={700} color="#7fd0ff" o={0.25} />
  <ellipse cx={960} cy={1000} rx={500} ry={60} fill="#000" opacity={0.3} />
  <g transform={`translate(960 560) rotate(${Math.sin(f * 1.7) * (f % 30 < 12 ? 2 : 0)})`}>
    <rect x={-250} y={-470} width={500} height={940} rx={60} fill="#16151c" /><rect x={-226} y={-446} width={452} height={892} rx={44} fill="#20304a" />
    <rect x={-60} y={-430} width={120} height={20} rx={10} fill="#0a0a10" />
    {[0, 1, 2].map(i => { const t = ((f + i * 12) % 36) / 36; return <circle key={i} cx={0} cy={-150} r={110 + t * 120} fill="none" stroke="#7fd0ff" strokeWidth={4} opacity={1 - t} />; })}
    <circle cx={0} cy={-150} r={110} fill="#a58bc9" />
    <circle cx={0} cy={-160} r={64} fill="#2e2a38" /><circle cx={-22} cy={-215} r={30} fill="#d8d6e2" /><path d="M-62 -170 Q-58 -230 0 -228 Q58 -226 62 -176 Q30 -204 -6 -202 Q-40 -198 -62 -170 Z" fill="#d8d6e2" />
    {[-1, 1].map(k => <g key={k}><circle cx={k * 22} cy={-160} r={12} fill="#f6f3ec" /><circle cx={k * 22 + 2} cy={-158} r={6} fill="#111" /><circle cx={k * 22} cy={-160} r={17} fill="none" stroke="#d9d2c0" strokeWidth={3} /></g>)}
    <path d="M-16 -128 Q0 -116 16 -128" stroke="#f4f1ea" strokeWidth={4} fill="none" strokeLinecap="round" />
    <text x={0} y={30} fontFamily="Inter" fontWeight={900} fontSize={56} fill="#fff" textAnchor="middle">Grandma Ayla</text>
    <text x={0} y={90} fontFamily="Inter" fontWeight={700} fontSize={34} fill="#9ab8d8" textAnchor="middle">incoming call…</text>
    <text x={0} y={150} fontFamily="Inter" fontWeight={900} fontSize={60} fill="#ff6a8a" textAnchor="middle">♥</text>
    <circle cx={-120} cy={330} r={54} fill="#e84a4a" /><circle cx={120} cy={330} r={54} fill="#3ac86a" />
    <path d="M-148 330 Q-120 316 -92 330" stroke="#fff" strokeWidth={10} fill="none" strokeLinecap="round" /><path d="M92 322 Q120 346 148 322" stroke="#fff" strokeWidth={10} fill="none" strokeLinecap="round" />
  </g>
</svg>;
