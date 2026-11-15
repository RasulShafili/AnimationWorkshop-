// Close-up inserts and graphics: phone (notifications / alert / call), clipboard, whiteboards (rules, brain), the
// zombie-ant fungus, the rat and the cat, radio workbench, data viz (doubling, density, rule of threes), peephole and
// binocular POVs, the bite on the sleeve, mom's badge, the notebook, ER corridor, title / part 2 / end cards.
import React from "react";
import { rnd, sat, ease, easeOut, lerp, W, H } from "../engine/core";
import { Glow, Shaft, Bokeh } from "../engine/fx";
import { Noise, AO } from "../engine/tex";
import { Character, Pose, shade } from "../chars/Rig2";
import { KAI, MIRA, MOM, ZOMBIES, zombiePose, EXTRAS } from "../chars/cast";

const SV: React.FC<{ children: React.ReactNode; bg?: string }> = ({ children, bg = "#0a0c12" }) => <svg width={W} height={H} style={{ position: "absolute" }}><rect width={W} height={H} fill={bg} />{children}</svg>;
// a hand (rig style mitten) holding things from below the frame
const Hand: React.FC<{ x: number; y: number; r?: number; s?: number; sleeve?: string }> = ({ x, y, r = 0, s = 1, sleeve = "#e8742a" }) => <g transform={`translate(${x} ${y}) rotate(${r}) scale(${s})`}>
  <path d="M-60 0 L60 0 L80 600 L-80 600 Z" fill={sleeve} /><path d="M-60 0 L60 0 L64 40 L-64 40 Z" fill={shade(sleeve, 0.75)} />
  <ellipse cx={0} cy={-40} rx={66} ry={60} fill="#2a2532" /><ellipse cx={20} cy={-62} rx={24} ry={14} fill="#fff" opacity={0.12} /><ellipse cx={-62} cy={-60} rx={24} ry={36} fill="#2a2532" transform="rotate(-20 -62 -60)" />
</g>;

// ---------- phone ----------
export type PhoneMode = { kind: "notifs"; items: [string, string][]; n: number } | { kind: "alert" } | { kind: "call"; name: string; t: number; ended?: boolean } | { kind: "search"; text: string };
export const Phone: React.FC<{ f: number; mode: PhoneMode; bg?: string; shake?: number }> = ({ f, mode, bg = "#141a26", shake = 0 }) => {
  const sx = shake ? Math.sin(f * 2.1) * 6 : 0;
  return <SV bg={bg}>
    <Bokeh x={0} y={0} w={W} h={H} n={26} f={f} colors={["#ffd38a", "#8ac8ff", "#ff9a6a"]} />
    <g transform={`translate(${960 + sx} 560) rotate(-4)`}>
      <Hand x={0} y={420} s={1.6} />
      <rect x={-250} y={-500} width={500} height={980} rx={56} fill="#0e0e12" /><rect x={-232} y={-482} width={464} height={944} rx={44} fill={mode.kind === "alert" ? "#1a0808" : "#0a1220"} />
      <rect x={-60} y={-470} width={120} height={28} rx={14} fill="#000" />
      <text x={-200} y={-410} fontFamily="Inter" fontWeight={800} fontSize={26} fill="#fff">11:07</text><text x={200} y={-410} textAnchor="end" fontFamily="Inter" fontWeight={800} fontSize={22} fill="#fff">▮▮▮ 18%</text>
      {mode.kind === "notifs" && mode.items.slice(0, Math.max(0, Math.floor(mode.n))).map(([app, txt], i) => <g key={i} transform={`translate(0 ${-330 + i * 132})`} opacity={sat(mode.n - i)}>
        <rect x={-210} y={0} width={420} height={118} rx={22} fill="#e8ecf2" opacity={0.95} /><rect x={-190} y={18} width={44} height={44} rx={10} fill={["#d8323a", "#2f6ad8", "#2f9a5a", "#e8742a"][i % 4]} />
        <text x={-132} y={44} fontFamily="Inter" fontWeight={800} fontSize={20} fill="#555">{app}</text><text x={-190} y={92} fontFamily="Inter" fontWeight={800} fontSize={24} fill="#111">{txt}</text></g>)}
      {mode.kind === "alert" && <g><rect x={-210} y={-300} width={420} height={420} rx={26} fill="#2a0e0e" stroke="#ff3a2a" strokeWidth={4} opacity={0.6 + 0.4 * Math.abs(Math.sin(f * 0.25))} />
        <text x={0} y={-230} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={30} fill="#ff5a4a">⚠ EMERGENCY ALERT</text>
        {["STAY INDOORS.", "LOCK ALL DOORS.", "AVOID CONTACT", "WITH SICK PEOPLE.", "DO NOT GO TO", "HOSPITALS."].map((l, i) => <text key={i} x={0} y={-160 + i * 50} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={34} fill="#fff">{l}</text>)}
        <rect x={-150} y={190} width={300} height={70} rx={35} fill="#3a3a44" /><text x={0} y={236} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={30} fill="#fff">OK</text></g>}
      {mode.kind === "call" && <g><circle cx={0} cy={-200} r={90} fill="#2e4a7a" /><text x={0} y={-176} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={70} fill="#fff">M</text>
        <text x={0} y={-50} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={48} fill="#fff">{mode.name}</text>
        <text x={0} y={0} textAnchor="middle" fontFamily="Inter" fontWeight={700} fontSize={30} fill={mode.ended ? "#ff5a4a" : "#9ad8a8"}>{mode.ended ? "Call ended" : `00:${String(Math.floor(mode.t / 30)).padStart(2, "0")}`}</text>
        {!mode.ended && Array.from({ length: 18 }, (_, i) => <rect key={i} x={-170 + i * 20} y={100 - (10 + 40 * Math.abs(Math.sin(f * 0.4 + i))) / 2} width={10} height={10 + 40 * Math.abs(Math.sin(f * 0.4 + i))} rx={5} fill="#6ad88a" />)}
        <circle cx={0} cy={330} r={56} fill="#e8322a" /><rect x={-28} y={322} width={56} height={16} rx={8} fill="#fff" /></g>}
      {mode.kind === "search" && <g><rect x={-210} y={-360} width={420} height={70} rx={35} fill="#e8ecf2" /><text x={-180} y={-314} fontFamily="Inter" fontWeight={700} fontSize={26} fill="#222">{mode.text}</text></g>}
    </g>
  </SV>;
};

// ---------- clipboard checklist ----------
export const Clipboard: React.FC<{ f: number; items: string[]; ticks: number }> = ({ f, items, ticks }) => <SV bg="#2a2e36">
  <Noise x={0} y={0} w={W} h={H} freq={0.6} o={0.25} />
  <g transform="translate(960 560) rotate(3)"><rect x={-380} y={-470} width={760} height={940} rx={24} fill="#9a6a3a" /><rect x={-340} y={-420} width={680} height={860} fill="#f6f3ea" /><rect x={-110} y={-500} width={220} height={70} rx={14} fill="#aab0ba" />
    <text x={-300} y={-330} fontFamily="Permanent Marker" fontSize={56} fill="#1a2a6a">SUPPLIES</text>
    {items.map((it, i) => <g key={i} transform={`translate(-300 ${-220 + i * 130})`}><rect x={0} y={-50} width={64} height={64} rx={8} fill="none" stroke="#1a2a6a" strokeWidth={5} />
      {ticks > i && <path d={`M10 -18 L28 4 L${10 + 56 * sat((ticks - i) * 2)} -48`} stroke="#2a8a3a" strokeWidth={10} fill="none" strokeLinecap="round" />}
      <text x={100} y={0} fontFamily="Permanent Marker" fontSize={50} fill="#1a2a6a">{it}</text></g>)}</g>
</SV>;

// whiteboard contents (inside StaffRoom board coords 760x440)
export const RulesBoard: React.FC<{ n: number }> = ({ n }) => <g fontFamily="Permanent Marker" fill="#1a3a8a">
  <text x={30} y={80} fontSize={64} fill="#c8282a">RULES</text>
  {["1. NO NOISE. THEY HUNT BY SOUND", "2. THEY CAN'T CLIMB → STAY HIGH", "3. NEVER GO ANYWHERE ALONE"].map((l, i) => n > i && <text key={i} x={40} y={170 + i * 90} fontSize={40}>{l.slice(0, Math.floor((n - i) * 40))}</text>)}
  <text x={520} y={420} fontSize={30} fill="#555">DAY 5 IIII</text>
</g>;
export const BrainBoard: React.FC<{ k: number }> = ({ k }) => <g fontFamily="Permanent Marker">
  <path d="M220 300 Q120 300 120 220 Q100 140 180 110 Q220 50 310 70 Q380 30 450 80 Q540 80 560 160 Q620 220 560 290 Q520 340 440 320 Q380 360 300 330 Q250 340 220 300 Z" fill="none" stroke="#1a3a8a" strokeWidth={7} opacity={sat(k * 3)} />
  <path d="M200 200 Q260 180 300 220 M330 120 Q340 200 400 220 M450 140 Q480 220 540 230" stroke="#1a3a8a" strokeWidth={5} fill="none" opacity={sat(k * 3)} />
  {k > 0.3 && <g><circle cx={260} cy={260} r={36} fill="#c8282a" opacity={0.25} /><text x={60} y={400} fontSize={40} fill="#1a3a8a">FEAR</text><path d={`M50 390 L${50 + 130 * sat((k - 0.4) * 4)} 370`} stroke="#c8282a" strokeWidth={8} /><path d="M150 380 L240 280" stroke="#1a3a8a" strokeWidth={4} /></g>}
  {k > 0.6 && <g><circle cx={460} cy={200} r={44} fill="#c8282a" opacity={0.35} /><text x={560} y={400} fontSize={44} fill="#c8282a">ANGER</text><ellipse cx={630} cy={385} rx={110} ry={44} fill="none" stroke="#c8282a" strokeWidth={6} /><path d="M600 340 L480 240" stroke="#c8282a" strokeWidth={4} /><text x={600} y={330} fontSize={50} fill="#c8282a">↑↑↑</text></g>}
</g>;

// ---------- nature: zombie-ant fungus; rat walks up to a cat ----------
export const AntFungus: React.FC<{ f: number }> = ({ f }) => { const climb = sat(f / 90), grow = sat((f - 110) / 70); const ay = lerp(900, 380, ease(climb));
  return <SV bg="#0e1a10">
    <defs><radialGradient id="rf" cx="0.5" cy="0.4" r="0.8"><stop offset="0" stopColor="#2a4a2a" /><stop offset="1" stopColor="#060e06" /></radialGradient></defs><rect width={W} height={H} fill="url(#rf)" />
    <Bokeh x={0} y={0} w={W} h={H} n={30} colors={["#8ad86a", "#c8f08a", "#4a8a3a"]} f={f} />
    <g transform="translate(960 560) scale(2.1) translate(-960 -560)"><path d="M900 1100 Q920 700 960 300" stroke="#3a6a2a" strokeWidth={26} fill="none" /><path d="M960 360 Q1200 250 1400 330 Q1180 420 960 360 Z" fill="#4a8a3a" /><path d="M940 600 Q700 520 560 600 Q740 680 940 600 Z" fill="#3e7a32" />
    <g transform={`translate(${940 + (ay < 400 ? 20 : 0)} ${ay}) rotate(${ay < 400 ? 70 : -88})`}>
      <ellipse cx={-40} cy={0} rx={36} ry={22} fill="#3a1e14" /><ellipse cx={10} cy={0} rx={18} ry={14} fill="#4a2a1a" /><ellipse cx={48} cy={-2} rx={26} ry={20} fill="#4a2a1a" />
      {[-1, 1].map(k => [-10, 10, 30].map((lx, i) => <path key={`${k}${i}`} d={`M${lx} 0 l${-14 + i * 10} ${k * 34} l${-10} ${k * 10}`} stroke="#2a140c" strokeWidth={5} fill="none" />))}
      <path d="M66 -14 Q86 -40 100 -30 M66 -10 Q90 -20 104 -8" stroke="#2a140c" strokeWidth={4} fill="none" /><path d="M70 10 L84 22 M70 12 L80 26" stroke="#2a140c" strokeWidth={5} />
      {grow > 0 && <g><path d={`M48 -20 Q60 ${-20 - 160 * grow} 40 ${-30 - 260 * grow}`} stroke="#d8c8a0" strokeWidth={10} fill="none" strokeLinecap="round" /><circle cx={40} cy={-30 - 260 * grow} r={14 * grow} fill="#e8a86a" /><Glow x={40} y={-30 - 260 * grow} r={60} color="#ffd88a" o={0.5 * grow} /></g>}
    </g></g>
    <text x={80} y={1010} fontFamily="Inter" fontWeight={800} fontSize={28} fill="#8ab88a" letterSpacing={4}>OPHIOCORDYCEPS · "ZOMBIE-ANT FUNGUS"</text>
  </SV>; };
export const RatCat: React.FC<{ f: number }> = ({ f }) => { const rx = lerp(300, 1080, sat(f / 110)), step = Math.sin(f * 0.6) * 4;
  return <SV bg="#2a2420">
    <rect width={W} height={700} fill="#5a4a3e" /><rect y={700} width={W} height={380} fill="#3a2e26" /><AO x={0} y={700} w={W} h={40} dir="down" o={0.5} /><Noise x={0} y={0} w={W} h={H} freq={0.5} o={0.25} />
    {/* cat sitting, right side, facing left */}
    <g transform="translate(1420 760)"><ellipse cx={0} cy={0} rx={120} ry={18} fill="#000" opacity={0.3} /><path d="M-80 0 Q-110 -150 -40 -220 Q20 -250 70 -200 Q120 -120 90 0 Z" fill="#e8963a" /><circle cx={-50} cy={-260} r={80} fill="#e8963a" />
      <path d="M-110 -310 L-100 -380 L-60 -330 Z M-20 -330 L10 -390 L20 -320 Z" fill="#e8963a" /><ellipse cx={-80} cy={-270} rx={14} ry={20} fill="#c8ff6a" /><ellipse cx={-30} cy={-270} rx={14} ry={20} fill="#c8ff6a" /><ellipse cx={-80} cy={-270} rx={4} ry={16} fill="#111" /><ellipse cx={-30} cy={-270} rx={4} ry={16} fill="#111" />
      <path d="M-62 -236 l-8 10 l16 0 Z" fill="#d8606a" /><path d="M90 -20 Q180 -40 160 -140" stroke="#e8963a" strokeWidth={22} fill="none" strokeLinecap="round" />{[0, 1, 2].map(i => <path key={i} d={`M-40 ${-180 + i * 40} q30 10 50 0`} stroke="#c8762a" strokeWidth={8} fill="none" />)}</g>
    {/* rat walking right toward the cat, calm */}
    <g transform={`translate(${rx} ${760 + step * 0.3})`}><ellipse cx={0} cy={4} rx={90} ry={12} fill="#000" opacity={0.3} /><path d="M-80 -10 Q-200 0 -260 -40" stroke="#c89a9a" strokeWidth={8} fill="none" />
      <ellipse cx={0} cy={-40} rx={90} ry={48} fill="#8a8a92" /><ellipse cx={80} cy={-56} rx={44} ry={34} fill="#9a9aa2" /><circle cx={60} cy={-96} r={20} fill="#c89a9a" /><circle cx={98} cy={-62} r={7} fill="#111" /><circle cx={124} cy={-50} r={7} fill="#e88a9a" />
      {[-40, 40].map((lx, i) => <rect key={i} x={lx - 8} y={-10 + (i ? step : -step)} width={14} height={20} rx={6} fill="#c89a9a" />)}</g>
    <text x={80} y={1010} fontFamily="Inter" fontWeight={800} fontSize={28} fill="#c8a88a" letterSpacing={4}>TOXOPLASMA · INFECTED RAT</text>
  </SV>; };

// ---------- radio workbench (dark store), wire up to the roof ----------
export const RadioBench: React.FC<{ f: number; on?: number; children?: React.ReactNode }> = ({ f, on = 0, children }) => <g>
  <rect x={-600} y={-200} width={3200} height={1500} fill="#0c0e14" />
  <rect x={-600} y={640} width={3200} height={700} fill="#14161c" /><rect x={200} y={600} width={1500} height={40} fill="#3a3e48" /><rect x={200} y={640} width={1500} height={300} fill="#262a32" />
  <path d="M1250 560 Q1300 200 1500 -100" stroke="#c8a83a" strokeWidth={4} fill="none" />
  <g transform="translate(1100 600)"><rect x={-180} y={-160} width={360} height={160} rx={14} fill="#4a3a2e" /><rect x={-160} y={-140} width={180} height={120} rx={8} fill="#2a221c" />{Array.from({ length: 8 }, (_, i) => <line key={i} x1={-150} y1={-130 + i * 14} x2={10} y2={-130 + i * 14} stroke="#4a3a2e" strokeWidth={4} />)}
    <rect x={40} y={-140} width={120} height={46} rx={4} fill={on ? "#ffd86a" : "#4a4030"} /><line x1={60 + ((f * 0.8) % 80)} y1={-136} x2={60 + ((f * 0.8) % 80)} y2={-98} stroke="#c8282a" strokeWidth={3} />{on > 0 && <Glow x={100} y={-117} r={120} color="#ffd86a" o={0.5} />}
    <circle cx={70} cy={-50} r={22} fill="#1a1612" /><circle cx={130} cy={-50} r={22} fill="#1a1612" /><path d="M160 -160 L230 -340" stroke="#888" strokeWidth={6} /></g>
  <g transform="translate(560 600)"><rect x={-110} y={-120} width={220} height={120} rx={10} fill="#1a1a1e" /><rect x={-70} y={-140} width={30} height={22} fill="#c8282a" /><rect x={40} y={-140} width={30} height={22} fill="#2a2a2a" /><text x={0} y={-50} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={24} fill="#888">12V</text></g>
  <path d="M500 480 Q700 420 940 520" stroke="#c8282a" strokeWidth={5} fill="none" /><path d="M630 480 Q800 450 960 540" stroke="#222" strokeWidth={5} fill="none" />
  {children}
</g>;

// ---------- data viz ----------
export const Doubling: React.FC<{ f: number; k: number }> = ({ f, k }) => { const gen = Math.min(10, Math.floor(k * 11)), n = Math.pow(2, gen);
  const cols = Math.max(1, Math.ceil(Math.sqrt(n * 2.2))), rows = Math.ceil(n / cols), cell = Math.min(1500 / cols, 640 / rows), sc = cell / 60;
  const ox = 960 - (cols * cell) / 2 + cell / 2, oy = 260 + (640 - rows * cell) / 2 + cell / 2;
  return <SV bg="#0a0e18">
    <text x={960} y={140} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={64} fill="#fff">ROUND {gen}: <tspan fill="#ff4a3a">{n.toLocaleString()}</tspan> INFECTED</text>
    {Array.from({ length: n }, (_, i) => { const x = ox + (i % cols) * cell, y = oy + Math.floor(i / cols) * cell, fresh = i >= n / 2 && gen > 0;
      return <g key={i} transform={`translate(${x} ${y}) scale(${sc})`}><circle cx={0} cy={-12} r={12} fill={fresh ? "#ff7a5a" : "#d8322a"} /><path d="M-16 24 Q-16 4 0 4 Q16 4 16 24 Z" fill={fresh ? "#ff7a5a" : "#d8322a"} /></g>; })}
    <text x={960} y={1000} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={36} fill="#8a9ab8" letterSpacing={4}>EVERY ROUND, EVERY INFECTED PERSON BITES TWO</text>
  </SV>; };
export const Density: React.FC<{ f: number; k: number }> = ({ f, k }) => <SV bg="#0a0e18">
  {[["NEW YORK CITY", 29000, 140, "#ff5a4a"], ["MONTANA", 7.5, 1100, "#4ae88a"]].map(([name, per, x, c], j) => { const n = j === 0 ? 290 : 1; return <g key={j}>
    <rect x={(x as number) - 40} y={170} width={720} height={720} rx={20} fill="none" stroke={c as string} strokeWidth={5} strokeDasharray="16 10" />
    {Array.from({ length: Math.round(n * sat(k * 2 - j * 0.3)) }, (_, i) => <circle key={i} cx={(x as number) + rnd(i, j + 3) * 640} cy={210 + rnd(i, j + 4) * 640} r={j ? 18 : 9} fill={c as string} />)}
    <text x={(x as number) + 320} y={950} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={44} fill="#fff">{name as string}</text>
    <text x={(x as number) + 320} y={1010} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={36} fill={c as string}>{(per as number).toLocaleString()} people / sq mile</text></g>; })}
  <text x={960} y={110} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={44} fill="#8a9ab8" letterSpacing={4}>ONE SQUARE MILE</text>
</SV>;
export const Threes: React.FC<{ f: number; k: number }> = ({ f, k }) => <SV bg="#0c1018">
  {[["3 MINUTES", "WITHOUT AIR", "#8ac8ff", "air"], ["3 DAYS", "WITHOUT WATER", "#4aa8ff", "water"], ["3 WEEKS", "WITHOUT FOOD", "#ffb84a", "food"]].map(([a, b, c, ic], i) => { const o = sat(k * 3.4 - i);
    return <g key={i} transform={`translate(${360 + i * 600} 520) scale(${0.9 + 0.1 * o})`} opacity={o}><circle cx={0} cy={-80} r={150} fill={c as string} opacity={0.15} stroke={c as string} strokeWidth={6} />
      {ic === "air" && <g fill="none" stroke={c as string} strokeWidth={14} strokeLinecap="round"><path d="M-80 -110 Q0 -140 40 -110 Q70 -80 40 -60" /><path d="M-80 -70 Q20 -80 60 -40 Q80 -10 50 0" /><path d="M-80 -30 L0 -30" /></g>}
      {ic === "water" && <path d="M0 -190 Q70 -90 70 -50 Q70 10 0 10 Q-70 10 -70 -50 Q-70 -90 0 -190 Z" fill={c as string} />}
      {ic === "food" && <g><rect x={-50} y={-150} width={100} height={130} rx={12} fill={c as string} /><rect x={-50} y={-110} width={100} height={40} fill="#fff" opacity={0.6} /></g>}
      <text x={0} y={150} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={66} fill="#fff">{a}</text><text x={0} y={210} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={34} fill={c as string}>{b}</text></g>; })}
</SV>;

// ---------- POVs ----------
export const Peephole: React.FC<{ f: number; children: React.ReactNode }> = ({ f, children }) => <div style={{ position: "absolute", inset: 0, background: "#000" }}>
  <div style={{ position: "absolute", inset: 0, clipPath: "circle(420px at 50% 50%)", filter: "saturate(0.8)" }}>{children}</div>
  <div style={{ position: "absolute", inset: 0, background: "radial-gradient(circle at 50% 50%, rgba(0,0,0,0) 300px, rgba(0,0,0,.9) 420px)" }} /></div>;
export const Binoculars: React.FC<{ children: React.ReactNode }> = ({ children }) => <div style={{ position: "absolute", inset: 0, background: "#000" }}>
  <div style={{ position: "absolute", inset: 0, clipPath: "path('M 960 540 m -720 0 a 380 380 0 1 0 760 0 a 380 380 0 1 0 -760 0 Z M 960 540 m -40 0 a 380 380 0 1 0 760 0 a 380 380 0 1 0 -760 0 Z')" }}>{children}</div>
  <div style={{ position: "absolute", left: 950, top: 520, width: 20, height: 2, background: "rgba(255,255,255,.5)" }} /></div>;

// ---------- the bite: torn sleeve close-up (no blood: a dark bruise-like mark) ----------
export const Sleeve: React.FC<{ f: number; k?: number }> = ({ f, k = 1 }) => <SV bg="#0e1018">
  <rect width={W} height={H} fill="#1a1e28" /><Glow x={1300} y={300} r={700} color="#8ab0d8" o={0.15} />
  <g transform="translate(900 560) rotate(-10)">
    {/* white shirt sleeve, Ruiz's green vest edge on the left, his hand on the right */}
    <path d="M-1100 -190 L520 -150 L520 150 L-1100 200 Z" fill="#e8e4da" /><path d="M-1100 110 L520 100 L520 150 L-1100 200 Z" fill="#c8c2b4" />
    <path d="M-1100 -200 L-760 -190 L-760 210 L-1100 220 Z" fill="#2f8a4e" />
    {[-500, -200, 100].map(x => <path key={x} d={`M${x} -170 q40 160 0 310`} stroke="#c8c2b4" strokeWidth={6} fill="none" />)}
    {/* torn hole with a ring of tooth marks (no blood) */}
    <path d="M-80 -150 L-50 -90 L-10 -140 L20 -70 L70 -130 L110 -60 L150 -120 L170 40 L130 120 L60 90 L0 130 L-60 80 L-100 110 Z" fill="#2a2532" opacity={k} />
    <ellipse cx={40} cy={0} rx={90} ry={60} fill="#5a4060" opacity={0.6 * k} />
    {Array.from({ length: 10 }, (_, i) => { const a = (i / 10) * Math.PI * 2; return <ellipse key={i} cx={40 + Math.cos(a) * 62} cy={Math.sin(a) * 40} rx={7} ry={10} fill="#1a0e1e" opacity={k} transform={`rotate(${a * 57} ${40 + Math.cos(a) * 62} ${Math.sin(a) * 40})`} />; })}
    <path d="M520 -150 L560 -150 L560 150 L520 150 Z" fill="#b8b2a4" />
    <ellipse cx={700} cy={0} rx={170} ry={150} fill="#2a2532" /><ellipse cx={740} cy={-60} rx={60} ry={30} fill="#fff" opacity={0.1} /><ellipse cx={640} cy={-150} rx={60} ry={40} fill="#2a2532" />
  </g>
</SV>;

// ---------- Mom: ER corridor (red light) for the phone call ----------
export const ER: React.FC<{ f: number; talk: number; children?: React.ReactNode }> = ({ f, talk, children }) => { const alarm = 0.5 + 0.5 * Math.sin(f * 0.2);
  return <SV bg="#1a1214">
    <rect width={W} height={700} fill="#d8dee2" /><rect y={700} width={W} height={380} fill="#9aa4a8" />{Array.from({ length: 12 }, (_, i) => <line key={i} x1={i * 180} y1={700} x2={i * 260 - 600} y2={1080} stroke="#000" strokeOpacity={0.08} strokeWidth={3} />)}
    {[200, 1400].map(x => <g key={x}><rect x={x} y={240} width={300} height={460} fill="#7a9ab8" /><rect x={x + 20} y={260} width={120} height={200} fill="#c8e0f0" /><text x={x + 150} y={220} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={30} fill="#2a4a6a">{x === 200 ? "TRAUMA 2" : "TRAUMA 3"}</text></g>)}
    <rect x={0} y={560} width={W} height={20} fill="#6aa8c8" /><g transform="translate(960 120)"><rect x={-120} y={-30} width={240} height={60} rx={12} fill="#c8282a" /><text x={0} y={12} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={34} fill="#fff">EMERGENCY</text></g>
    {/* gurney */}
    <g transform="translate(1500 860)"><rect x={-200} y={-80} width={400} height={30} rx={8} fill="#e8ecf0" /><rect x={-180} y={-50} width={10} height={100} fill="#8a8a94" /><rect x={170} y={-50} width={10} height={100} fill="#8a8a94" /><circle cx={-175} cy={60} r={14} fill="#333" /><circle cx={175} cy={60} r={14} fill="#333" /></g>
    <Character look={MOM} pose={{ facing: 1, hold: "phone", aR: [52, 120], aL: [10, 20], talk, brow: 0, browIn: 0.8, mouth: "worried", look: [0.6, 0.2] }} x={820} y={1080} s={1.9} f={f} seed={5} rim={{ dx: 5, dy: -3, color: "#ff5a4a" }} />
    <rect width={W} height={H} fill="#ff2a2a" opacity={0.12 + 0.1 * alarm} style={{ mixBlendMode: "multiply" }} />
    <Glow x={960} y={120} r={500} color="#ff3a2a" o={0.35 * alarm} />
    {children}
  </SV>; };

// ---------- mom's badge on the board / cot; the notebook ----------
export const Badge: React.FC<{ x: number; y: number; s?: number; note?: string }> = ({ x, y, s = 1, note }) => <g transform={`translate(${x} ${y}) scale(${s}) rotate(-4)`}>
  <rect x={-140} y={-190} width={280} height={380} rx={18} fill="#f4f6fa" stroke="#3a6ad8" strokeWidth={8} /><rect x={-140} y={-190} width={280} height={70} rx={14} fill="#3a6ad8" /><text x={0} y={-142} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={28} fill="#fff">GRADY ER</text>
  <rect x={-80} y={-100} width={160} height={150} fill="#8aa0b8" /><circle cx={0} cy={-30} r={50} fill="#2a2532" /><circle cx={-24} cy={-82} r={22} fill="#17141c" /><rect x={-60} y={20} width={120} height={30} fill="#2e4a7a" />
  <text x={0} y={92} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={30} fill="#1a1a2a">DR. GRACE COLE</text><text x={0} y={130} textAnchor="middle" fontFamily="Inter" fontWeight={700} fontSize={22} fill="#555">EMERGENCY MEDICINE</text>
  {note && <g transform="translate(40 230) rotate(6)"><rect x={-230} y={-44} width={460} height={96} fill="#fff6a8" /><text x={0} y={18} textAnchor="middle" fontFamily="Permanent Marker" fontSize={30} fill="#1a2a8a">{note}</text></g>}
</g>;
export const Notebook: React.FC<{ f: number; k: number }> = ({ f, k }) => { const txt = "THE BAT WASN'T AN ACCIDENT."; const n = Math.floor(txt.length * sat(k));
  return <SV bg="#140e0a">
    <Glow x={1300} y={200} r={900} color="#ffb84a" o={0.25} />
    <g transform="translate(960 560) rotate(-3)"><rect x={-720} y={-420} width={1440} height={840} rx={12} fill="#5a3a24" /><rect x={-690} y={-400} width={680} height={800} fill="#efe6d0" /><rect x={10} y={-400} width={680} height={800} fill="#f4ecd8" />
      {Array.from({ length: 16 }, (_, i) => <g key={i}><line x1={-670} y1={-330 + i * 46} x2={-30} y2={-330 + i * 46} stroke="#8ab0d8" strokeWidth={2} /><line x1={30} y1={-330 + i * 46} x2={670} y2={-330 + i * 46} stroke="#8ab0d8" strokeWidth={2} /></g>)}
      {["Day 9 — 3rd patient from the", "airport flight. Same strain.", "Fever 6 hrs, then aggression.", "Day 11 — CDC team asked about", "the ranch. They already knew", "the name of the ranch."].map((l, i) => <text key={i} x={-650} y={-290 + i * 92} fontFamily="Permanent Marker" fontSize={34} fill="#3a3a5a" opacity={0.55}>{l}</text>)}
      <text x={60} y={-150} fontFamily="Permanent Marker" fontSize={36} fill="#3a3a5a" opacity={0.5}>Day 12 — Montana.</text>
      <text x={60} y={40} fontFamily="Permanent Marker" fontSize={50} fill="#a8182a">{txt.slice(0, Math.min(n, 15))}</text>
      <text x={60} y={130} fontFamily="Permanent Marker" fontSize={50} fill="#a8182a">{n > 15 ? txt.slice(15, n) : ""}</text>
      {n >= txt.length && <path d="M60 160 L560 150" stroke="#a8182a" strokeWidth={6} />}
      <rect x={-20} y={-400} width={40} height={800} fill="#000" opacity={0.15} /></g>
  </SV>; };

// ---------- title / part 2 / end cards ----------
export const TitleCard: React.FC<{ f: number }> = ({ f }) => { const k = easeOut(f / 20);
  return <SV bg="#07090e">
    <Glow x={960} y={560} r={900} color="#3a8a3a" o={0.18} />
    {Array.from({ length: 22 }, (_, i) => { const x = rnd(i, 1) * 1920, y = 1080 - 60 - rnd(i, 2) * 120; return <g key={i} transform={`translate(${x} ${y + Math.sin(f * 0.1 + i) * 4}) rotate(${(rnd(i, 3) - 0.5) * 30})`} opacity={0.5}><ellipse cx={0} cy={0} rx={30} ry={36} fill="#3a4a3a" />{[-22, -8, 6, 20].map((fx, kk) => <rect key={kk} x={fx - 6} y={-74} width={13} height={44} rx={6} fill="#3a4a3a" />)}</g>; })}
    <text x={960} y={420} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={54} fill="#9ad88a" letterSpacing={18} opacity={k}>WHAT IF</text>
    <text x={960} y={560} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={120} fill="#fff" opacity={sat((f - 8) / 12)}>A ZOMBIE VIRUS</text>
    <text x={960} y={700} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={120} fill="#fff" opacity={sat((f - 14) / 12)}>STARTED IN THE <tspan fill="#e8322a">US</tspan>?</text>
  </SV>; };
export const Part2: React.FC<{ f: number }> = ({ f }) => <SV bg="#050306">
  <text x={960} y={420} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={66} fill="#e8322a" letterSpacing={16} opacity={sat(f / 14)}>PART 2</text>
  <text x={960} y={570} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={140} fill="#fff" opacity={sat((f - 10) / 14)}>PATIENT ZERO</text>
  <text x={960} y={680} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={40} fill="#8a809a" letterSpacing={10} opacity={sat((f - 30) / 14)}>COMING SOON</text>
</SV>;
export const EndCard: React.FC<{ f: number }> = ({ f }) => <SV bg="#0a0e14">
  <Glow x={500} y={560} r={600} color="#e8742a" o={0.22} />
  <Character look={KAI} pose={{ facing: 1, mouth: "smile", aR: [125 + 6 * Math.sin(f * 0.3), 25 + 15 * Math.sin(f * 0.3)], hold: null }} x={420} y={960} s={1.25} f={f} seed={1} rim={{ dx: 4, dy: -3, color: "#e8742a" }} />
  <Character look={MIRA} pose={{ facing: 1, mouth: "smile", hold: "walkie", aR: [40, 70] }} x={640} y={960} s={1.25} f={f} seed={2} />
  <text x={110} y={150} fontFamily="Inter" fontWeight={900} fontSize={64} fill="#fff" opacity={sat(f / 12)}>THANKS FOR WATCHING</text>
  <text x={110} y={220} fontFamily="Inter" fontWeight={800} fontSize={36} fill="#e8742a" opacity={sat((f - 8) / 12)}>WOULD YOU HAVE OPENED THE DOOR?</text>
  <g opacity={sat((f - 20) / 10)} transform={`translate(520 1010) scale(${1 + 0.04 * Math.sin(f * 0.15)})`}><rect x={-230} y={-44} width={460} height={88} rx={44} fill="#e8322a" /><text x={0} y={16} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={40} fill="#fff">SUBSCRIBE FOR PART 2</text></g>
</SV>;
