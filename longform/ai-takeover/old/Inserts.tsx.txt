// Ice Age close-ups and graphics: the survival kit, flint + pyrite sparks, frostbite fingers, the phone, the carved
// bone tally (museum + Eli's own), the spear-thrower, hot stones boiling water, the splint, Pip's horse drawing,
// Europe then vs now, people-in-Europe dots, 1492 arrows, the virus jump, the carbon-date tablet, title + end cards.
import React from "react";
import { rnd, sat, ease, easeOut, lerp, W, H } from "../engine/core";
import { Glow, Bokeh } from "../engine/fx";
import { Noise, AO } from "../engine/tex";
import { Character, shade } from "../chars/Rig2";
import { ELI, NIA, PIP } from "../chars/cast";
import { Mammoth } from "./Animals";

const SV: React.FC<{ children: React.ReactNode; bg?: string }> = ({ children, bg = "#0a0c12" }) => <svg width={W} height={H} style={{ position: "absolute" }}><rect width={W} height={H} fill={bg} />{children}</svg>;
const SKIN = "#f2c8a8";
const Hand: React.FC<{ x: number; y: number; r?: number; s?: number; sleeve?: string; flip?: boolean }> = ({ x, y, r = 0, s = 1, sleeve = "#8a909c", flip }) =>
  <g transform={`translate(${x} ${y}) rotate(${r}) scale(${(flip ? -1 : 1) * s} ${s})`}>
    <path d="M-70 40 L70 40 L90 700 L-90 700 Z" fill={sleeve} /><path d="M-70 40 L70 40 L74 90 L-74 90 Z" fill={shade(sleeve, 0.75)} />
    <ellipse cx={0} cy={0} rx={74} ry={66} fill={SKIN} /><ellipse cx={22} cy={-24} rx={26} ry={14} fill="#fff" opacity={0.25} /><ellipse cx={-70} cy={-20} rx={26} ry={40} fill={SKIN} transform="rotate(-20 -70 -20)" /><ellipse cx={0} cy={0} rx={74} ry={66} fill="none" stroke="#c89878" strokeWidth={4} />
  </g>;

// ---------- the survival kit flat-lay on snow ----------
export const Kit: React.FC<{ f: number; n: number }> = ({ f, n }) => <SV bg="#e8eef4">
  <Noise x={0} y={0} w={W} h={H} freq={0.5} o={0.15} />
  {[
    <g key="p" transform="translate(420 520) rotate(-8)"><rect x={-80} y={-150} width={160} height={300} rx={24} fill="#111" /><rect x={-68} y={-136} width={136} height={272} rx={14} fill="#1a2a4a" /><text x={0} y={-60} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={18} fill="#ff6a5a">NO SERVICE</text><text x={0} y={0} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={34} fill="#fff">12%</text></g>,
    <g key="b" transform="translate(800 470) rotate(12)"><rect x={-24} y={-180} width={10} height={360} rx={4} fill="#2a5ad8" /><rect x={-24} y={-200} width={10} height={30} rx={3} fill="#f4f4f4" /></g>,
    <g key="w" transform="translate(1120 520) rotate(-4)"><rect x={-70} y={-200} width={140} height={400} rx={40} fill="#9ad0f4" opacity={0.85} /><rect x={-40} y={-240} width={80} height={50} rx={10} fill="#2a5ad8" /><rect x={-60} y={-120} width={120} height={200} rx={30} fill="#fff" opacity={0.6} /><text x={0} y={30} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={22} fill="#2a5ad8">FROZEN</text></g>,
    <g key="g" transform="translate(1480 520) rotate(10)"><rect x={-110} y={-50} width={220} height={100} rx={10} fill="#e8b84a" /><rect x={-110} y={-50} width={220} height={36} fill="#c8402e" /><text x={0} y={-24} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={20} fill="#fff">GRANOLA</text></g>,
    <g key="n" transform="translate(800 820) rotate(-6)"><rect x={-140} y={-90} width={280} height={180} rx={8} fill="#2a3a5a" /><rect x={-126} y={-80} width={250} height={160} fill="#f4efe0" />{[0, 1, 2, 3].map(i => <line key={i} x1={-110} y1={-50 + i * 34} x2={110} y2={-50 + i * 34} stroke="#9ab0c8" strokeWidth={3} />)}</g>,
  ].slice(0, Math.ceil(n)).map((el, i) => <g key={i} opacity={sat(n - i)}>{el}</g>)}
  <text x={960} y={110} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={54} fill="#2a3a5a" letterSpacing={6}>YOUR SURVIVAL KIT</text>
</SV>;

// ---------- flint + pyrite: two hands strike, sparks fly into tinder ----------
export const Spark: React.FC<{ f: number; fire?: number }> = ({ f, fire = 0 }) => { const hit = (f % 16) < 3, t = (f % 16) / 16;
  return <SV bg="#1a1410">
    <Glow x={960} y={760} r={700} color="#ff9a3a" o={0.15 + 0.5 * fire} />
    <ellipse cx={960} cy={860} rx={260} ry={60} fill="#5a4630" />{Array.from({ length: 40 }, (_, i) => <line key={i} x1={760 + rnd(i, 1) * 400} y1={830 + rnd(i, 2) * 50} x2={790 + rnd(i, 1) * 400} y2={820 + rnd(i, 2) * 50} stroke="#c8a870" strokeWidth={3} />)}
    {fire > 0 && <g transform="translate(960 840)">{Array.from({ length: 5 }, (_, i) => <path key={i} d={`M${(i - 2) * 18 - 14} 0 Q${(i - 2) * 18} ${-(60 + 40 * Math.sin(f * 0.5 + i)) * fire * 1.8} ${(i - 2) * 18 + 14} 0 Z`} fill={["#ff8a2a", "#ffb84a", "#ffe08a", "#ffb84a", "#ff8a2a"][i]} />)}</g>}
    <g transform={`translate(${760 + (hit ? 20 : 0)} ${470 + Math.sin(t * Math.PI * 2) * 30})`}><Hand x={0} y={0} r={28} s={1.1} /><path d="M40 -80 L130 -60 L110 30 L20 10 Z" fill="#7a808a" stroke="#4a4e58" strokeWidth={5} /></g>
    <g transform="translate(1180 520)"><Hand x={0} y={0} r={-28} s={1.1} flip /><path d="M-130 -60 Q-60 -100 -30 -40 Q-50 20 -120 10 Z" fill="#c8a84a" stroke="#8a7030" strokeWidth={5} /><ellipse cx={-90} cy={-50} rx={20} ry={10} fill="#fff6c8" opacity={0.8} /></g>
    {hit && Array.from({ length: 22 }, (_, i) => { const a = -Math.PI / 2 + (rnd(i + Math.floor(f / 16) * 30, 3) - 0.5) * 2.6, len = 60 + rnd(i, 4) * 220; return <line key={i} x1={960} y1={490} x2={960 + Math.cos(a) * len} y2={490 + Math.sin(a) * len + 180} stroke="#ffe08a" strokeWidth={4} strokeLinecap="round" />; })}
    {hit && <Glow x={960} y={490} r={180} color="#ffe08a" o={0.9} />}
  </SV>; };

// ---------- frostbite: fingers turning pale ----------
export const Frost: React.FC<{ f: number; k: number }> = ({ f, k }) => <SV bg="#b8c8d8">
  {Array.from({ length: 80 }, (_, i) => <circle key={i} cx={(rnd(i, 1) * 2200 + f * 12) % 2200 - 100} cy={(rnd(i, 2) * 1200 + f * 6) % 1200} r={3 + rnd(i, 3) * 4} fill="#fff" opacity={0.8} />)}
  <g transform="translate(960 640) scale(2.2)"><path d="M-80 60 L80 60 L100 300 L-100 300 Z" fill="#8a909c" />
    {[-54, -20, 14, 48].map((x, i) => <rect key={i} x={x - 14} y={-140 + Math.abs(i - 1.5) * 14} width={28} height={130} rx={14} fill={i < 3 ? `url(#frostg)` : SKIN} />)}
    <defs><linearGradient id="frostg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={k > 0.5 ? "#f4f6fa" : SKIN} /><stop offset={0.2 + 0.5 * k} stopColor="#e0e6f0" /><stop offset="1" stopColor={SKIN} /></linearGradient></defs>
    <ellipse cx={0} cy={20} rx={84} ry={70} fill={SKIN} /><path d="M-84 0 Q-130 -40 -110 -90 L-90 -80 Q-100 -40 -70 -10 Z" fill={SKIN} /></g>
  <text x={960} y={120} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={60} fill="#1a3a6a">−25°C · WIND</text>
</SV>;

// ---------- phone screen held in a gloved/bare hand ----------
export const PhoneShot: React.FC<{ f: number; pct: number; lines: string[]; bg?: string }> = ({ f, pct, lines, bg = "#cfdbe6" }) => <SV bg={bg}>
  {Array.from({ length: 60 }, (_, i) => <circle key={i} cx={(rnd(i, 1) * 2200 + f * 10) % 2200 - 100} cy={(rnd(i, 2) * 1200 + f * 5) % 1200} r={3 + rnd(i, 3) * 3} fill="#fff" opacity={0.7} />)}
  <g transform="translate(960 560) rotate(-5)"><Hand x={0} y={420} s={1.5} />
    <rect x={-250} y={-480} width={500} height={960} rx={56} fill="#0e0e12" /><rect x={-232} y={-462} width={464} height={924} rx={44} fill="#0a1424" />
    <text x={-190} y={-390} fontFamily="Inter" fontWeight={800} fontSize={28} fill="#fff">{Math.floor(f / 7) % 3 ? "??:??" : "--:--"}</text><text x={200} y={-390} textAnchor="end" fontFamily="Inter" fontWeight={800} fontSize={26} fill={pct < 5 ? "#ff5a4a" : "#fff"}>{pct}%</text>
    {lines.map((l, i) => <text key={i} x={0} y={-120 + i * 90} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={i === 0 ? 46 : 38} fill={i === 0 ? "#ff6a5a" : "#e8eef8"}>{l}</text>)}
  </g>
</SV>;

// ---------- the carved bone with tally scratches (n lines), optional glow ----------
export const BoneTally: React.FC<{ f: number; n: number; glow?: number; bg?: string; label?: string }> = ({ f, n, glow = 0, bg = "#2a1e16", label }) => <SV bg={bg}>
  <Noise x={0} y={0} w={W} h={H} freq={0.4} o={0.3} />
  {glow > 0 && <Glow x={960} y={540} r={700} color="#ffd86a" o={0.5 * glow} />}
  <g transform="translate(960 540) rotate(-8)">
    <path d="M-760 -70 Q-820 -120 -760 -150 Q-700 -170 -680 -110 L680 -110 Q700 -170 760 -150 Q820 -120 760 -70 Q820 -20 760 10 Q700 30 680 -30 L-680 -30 Q-700 30 -760 10 Q-820 -20 -760 -70 Z" fill="#e8dcc0" />
    <path d="M-680 -100 L680 -100" stroke="#fff" strokeWidth={8} opacity={0.4} />
    {Array.from({ length: Math.floor(n) }, (_, i) => <line key={i} x1={-640 + (i % 64) * 20} y1={-104 + Math.floor(i / 64) * 0} x2={-644 + (i % 64) * 20} y2={-38} stroke={glow > 0 ? "#ffcf4a" : "#6a5a40"} strokeWidth={5} strokeLinecap="round" />)}
  </g>
  {label && <text x={960} y={960} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={54} fill="#f4efe0" letterSpacing={4}>{label}</text>}
</SV>;

// ---------- the spear-thrower: diagram ----------
export const Thrower: React.FC<{ f: number; k: number }> = ({ f, k }) => <SV bg="#e8eef0">
  <text x={960} y={120} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={58} fill="#3a2a1a" letterSpacing={4}>SPEAR-THROWER</text>
  {[["ARM ONLY", 300, 0.5, "#8a7a64"], ["+ SPEAR-THROWER", 640, 1, "#c8402e"]].map(([lab, y, mult, c], j) => { const fly = sat(k * 1.4 - j * 0.2), x = 360 + fly * 1300 * (mult as number);
    return <g key={j}><text x={120} y={(y as number) + 14} fontFamily="Inter" fontWeight={900} fontSize={34} fill={c as string}>{lab}</text>
      <line x1={360} y1={(y as number) + 60} x2={1800} y2={(y as number) + 60} stroke="#c8ccd2" strokeWidth={4} strokeDasharray="20 16" />
      <g transform={`translate(${x} ${(y as number) + 60})`}><line x1={-220} y1={0} x2={0} y2={0} stroke="#6a4a2a" strokeWidth={10} strokeLinecap="round" /><path d="M0 -14 L50 0 L0 14 Z" fill="#7a808a" /></g>
      {j === 1 && <text x={Math.min(x + 80, 1560)} y={(y as number) - 40} fontFamily="Inter" fontWeight={900} fontSize={40} fill="#c8402e" opacity={sat(fly * 2 - 1)}>150 km/h</text>}</g>; })}
  <g transform="translate(1420 870)"><path d="M-260 0 L240 0 L260 -26 L232 -24" stroke="#c8a87a" strokeWidth={22} fill="none" strokeLinecap="round" /><text x={0} y={70} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={28} fill="#6a5a40">REINDEER ANTLER · HOOK</text></g>
</SV>;

// ---------- hot stones into a hide pot of snow water ----------
export const Boil: React.FC<{ f: number; k: number }> = ({ f, k }) => { const z = 1 + 0.18 * sat(f / 330), heat = sat(f / 260);
  return <SV bg="#2a1e16"><g transform={`translate(960 600) scale(${z}) translate(-960 -600)`}>
  <Glow x={960} y={700} r={800} color="#ff9a3a" o={0.25 + 0.15 * heat} />
  <path d="M600 520 Q960 460 1320 520 L1240 900 Q960 980 680 900 Z" fill="#9a7650" /><path d="M600 520 Q960 460 1320 520 Q960 580 600 520 Z" fill="#b8d8e8" />
  {Array.from({ length: 22 }, (_, i) => { const t = ((f * (0.03 + 0.02 * heat) + i / 22) % 1); return <circle key={i} cx={680 + rnd(i, 1) * 560 + Math.sin(f * 0.05 + i) * 20} cy={520 - t * (220 + 140 * heat)} r={(6 + rnd(i, 2) * 12) * (1 + t)} fill="#fff" opacity={(1 - t) * (0.3 + 0.4 * heat) * k} />; })}
  {k > 0.2 && Array.from({ length: 6 + Math.round(10 * heat) }, (_, i) => <circle key={i} cx={720 + rnd(i, 4) * 480} cy={515 + Math.sin(f * (0.5 + heat) + i) * (3 + 5 * heat)} r={8 + 4 * rnd(i, 5)} fill="#fff" opacity={0.7} />)}
  {[[0, 960], [110, 860], [210, 1070]].map(([t0, x], j) => { const u = sat((f - t0) / 26); if (f < t0 - 1) return null;
    return <g key={j} transform={`translate(${x} ${lerp(160, 510, u * u)})`}><ellipse rx={56} ry={40} fill="#4a3a30" /><ellipse rx={56} ry={40} fill="#ff6a2a" opacity={0.5} /><Glow x={0} y={0} r={110} color="#ff6a2a" o={0.55} />
      {u >= 1 && f - t0 < 46 && Array.from({ length: 8 }, (_, i) => { const a = i / 8 * Math.PI * 2, d = (f - t0 - 26) * 6; return <circle key={i} cx={Math.cos(a) * d} cy={-Math.abs(Math.sin(a)) * d * 0.8} r={7} fill="#cfe8f4" opacity={1 - (f - t0 - 26) / 20} />; })}</g>; })}
  {(() => { const j = f < 110 ? 0 : f < 210 ? 1 : 2, t0 = [0, 110, 210][j], x = [960, 860, 1070][j], u = sat((f - t0) / 26), lift = sat((f - t0 - 30) / 30);
    return <path d={`M${x - 200} ${-40 + 380 * u - 300 * lift} L${x - 60} ${130 + 380 * u - 300 * lift} M${x + 200} ${-40 + 380 * u - 300 * lift} L${x + 60} ${130 + 380 * u - 300 * lift}`} stroke="#5a3e28" strokeWidth={18} strokeLinecap="round" />; })()}
  </g></SV>; };

// ---------- Pip's horse drawing in the notebook ----------
export const Drawing: React.FC<{ f: number; k: number }> = ({ f, k }) => { const L = 2200; return <SV bg="#3a2418">
  <Glow x={960} y={540} r={900} color="#ffb060" o={0.3} />
  <g transform="translate(960 560) rotate(-4)"><rect x={-560} y={-360} width={1120} height={720} rx={12} fill="#2a3a5a" /><rect x={-530} y={-340} width={1060} height={680} fill="#f4efe0" />
    {Array.from({ length: 14 }, (_, i) => <line key={i} x1={-500} y1={-300 + i * 48} x2={500} y2={-300 + i * 48} stroke="#9ab0c8" strokeWidth={2} />)}
    <path d="M-300 40 Q-260 -120 -40 -130 Q160 -150 240 -60 L320 -130 L330 -60 L270 10 L260 180 M180 20 L190 180 M-220 30 L-240 180 M-140 40 L-120 180 M-300 40 Q-380 60 -400 140" stroke="#1a2a8a" strokeWidth={9} fill="none" strokeLinecap="round" strokeDasharray={L} strokeDashoffset={L * (1 - k)} />
    <circle cx={270} cy={-90} r={6} fill="#1a2a8a" opacity={sat(k * 2 - 1)} /></g>
</SV>; };

// ---------- Europe 30,000 years ago vs today (ice sheet, low sea, land bridge) ----------
const EUR = "M280 980 L240 820 L300 700 L420 640 L470 560 L560 520 L600 440 L700 420 L760 360 L840 380 L900 330 L980 300 L1060 320 L1160 280 L1300 300 L1420 260 L1560 300 L1700 280 L1800 360 L1800 980 Z";
const BRIT = "M560 300 L620 240 L660 160 L700 120 L740 200 L720 280 L760 340 L700 380 L620 370 Z";
const SCAN = "M980 260 L1020 140 L1100 60 L1220 20 L1300 80 L1260 180 L1180 240 L1100 280 Z";
export const EuropeMap: React.FC<{ f: number; k: number }> = ({ f, k }) => <SV bg="#0e2a44">
  {Array.from({ length: 22 }, (_, i) => <line key={i} x1={i * 90} y1={0} x2={i * 90} y2={H} stroke="#2a4a6a" strokeOpacity={0.3} />)}
  {/* land shelf exposed by the low sea (grows with k) */}
  <path d={EUR} fill="#8aa06a" stroke="#c8e0a8" strokeWidth={30 * k} strokeLinejoin="round" opacity={0.9} />
  <path d={BRIT} fill="#8aa06a" stroke="#c8e0a8" strokeWidth={30 * k} strokeLinejoin="round" />
  {k > 0.3 && <path d="M700 380 L760 360 L840 380 L760 420 Z" fill="#c8e0a8" opacity={sat((k - 0.3) * 3)} stroke="#c8e0a8" strokeWidth={40} />}
  <path d={EUR} fill="#6a8a4a" /><path d={BRIT} fill="#6a8a4a" /><path d={SCAN} fill="#6a8a4a" />
  {/* the ice sheet */}
  <g opacity={k}><path d="M420 60 Q700 -40 1100 -20 Q1500 0 1700 120 Q1700 300 1400 300 Q1200 330 1060 300 Q880 320 760 300 Q620 300 560 220 Q480 140 420 60 Z" fill="#f4f8fc" /><path d="M560 220 Q800 260 1060 300" stroke="#c8dcf0" strokeWidth={8} fill="none" /></g>
  <text x={1120} y={160} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={40} fill="#2a5a8a" opacity={k}>ICE · UP TO 3 KM THICK</text>
  <text x={800} y={480} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={30} fill="#fff" opacity={sat(k * 2 - 1)}>WALK TO BRITAIN</text>
  <text x={960} y={1030} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={44} fill="#fff" letterSpacing={6}>{k > 0.5 ? "30,000 YEARS AGO" : "TODAY"}</text>
</SV>;

// ---------- dots: people in all of Western Europe vs a small town ----------
export const PopDots: React.FC<{ f: number; k: number }> = ({ f, k }) => <SV bg="#0e1420">
  {[["WESTERN EUROPE, 30,000 YEARS AGO", 120, 60, "#ffb84a"], ["ONE SMALL TOWN TODAY", 1000, 220, "#8ab0d8"]].map(([lab, x, n, c], j) => <g key={j}>
    <rect x={x as number} y={190} width={800} height={500} rx={20} fill="none" stroke={c as string} strokeWidth={4} strokeDasharray="14 10" />
    {Array.from({ length: Math.round((n as number) * sat(k * 1.5 - j * 0.3)) }, (_, i) => <circle key={i} cx={(x as number) + 40 + rnd(i, j + 5) * 720} cy={225 + rnd(i, j + 6) * 430} r={7} fill={c as string} />)}
    <text x={(x as number) + 400} y={750} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={34} fill="#fff">{lab as string}</text></g>)}
  <text x={960} y={120} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={42} fill="#8a9ab8" letterSpacing={4}>EACH DOT ≈ 50 PEOPLE</text>
</SV>;

// ---------- 1492: ships' arrows and the death toll ----------
export const Map1492: React.FC<{ f: number; k: number }> = ({ f, k }) => <SV bg="#0e2a44">
  <path d="M1300 200 L1500 160 L1700 220 L1760 500 L1660 700 L1500 760 L1420 600 L1380 400 Z" fill="#6a7a5a" />
  <path d="M120 120 L520 140 L640 300 L600 500 L700 640 L620 900 L520 980 L460 760 L360 600 L240 420 L140 300 Z" fill="#6a7a5a" />
  {[0, 1, 2].map(i => { const kk = sat(k * 1.6 - i * 0.2); return <path key={i} d={`M1380 ${360 + i * 80} Q960 ${220 + i * 80} ${620} ${420 + i * 80}`} stroke="#ffd34a" strokeWidth={8} fill="none" strokeDasharray="1000" strokeDashoffset={1000 * (1 - kk)} />; })}
  <text x={960} y={140} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={64} fill="#fff">1492</text>
  <g opacity={sat(k * 2 - 1)}>{Array.from({ length: 10 }, (_, i) => <g key={i} transform={`translate(${1010 + i * 60} 930)`}><circle cy={-50} r={14} fill={i < 9 ? "#ff5a4a" : "#f4f4f4"} /><path d="M-18 -10 Q-18 -32 0 -32 Q18 -32 18 -10 Z" fill={i < 9 ? "#ff5a4a" : "#f4f4f4"} /></g>)}
    <text x={990} y={1010} fontFamily="Inter" fontWeight={900} fontSize={40} fill="#ff6a5a">UP TO 9 IN 10 DIED</text></g>
</SV>;

// ---------- virus jump: from Eli's breath to Pip ----------
export const Germs: React.FC<{ f: number }> = ({ f }) => <SV bg="#120e14">
  <Glow x={960} y={540} r={900} color="#3a8a5a" o={0.2} />
  <g transform="translate(420 1100)"><Character look={ELI} pose={{ facing: 1, mouth: "o", look: [0.9, 0] }} x={0} y={0} s={1.8} f={f} seed={1} /></g>
  <g transform="translate(1520 1100)"><Character look={PIP} pose={{ facing: -1, mouth: "flat", eyes: 0.6, brow: 0, browIn: 0.8 }} x={0} y={0} s={2.1} f={f} seed={2} /></g>
  {Array.from({ length: 18 }, (_, i) => { const t = ((f * 0.012 + i / 18) % 1), x = lerp(560, 1420, t), y = 440 + Math.sin(t * 6 + i) * 60 - Math.sin(t * Math.PI) * 120;
    return <g key={i} transform={`translate(${x} ${y}) rotate(${f * 3 + i * 20})`} opacity={Math.sin(t * Math.PI)}><circle r={16} fill="#6ad88a" />{Array.from({ length: 8 }, (_, k) => <line key={k} x1={0} y1={0} x2={Math.cos(k * 0.785) * 26} y2={Math.sin(k * 0.785) * 26} stroke="#6ad88a" strokeWidth={4} />)}</g>; })}
</SV>;

// ---------- 2026 tablet: carbon date ----------
export const Tablet: React.FC<{ f: number; k: number }> = ({ f, k }) => <SV bg="#1a1e26">
  <g transform="translate(960 540) rotate(-3)"><rect x={-520} y={-340} width={1040} height={680} rx={40} fill="#111" /><rect x={-490} y={-310} width={980} height={620} rx={18} fill="#e8eef4" />
    <text x={-430} y={-220} fontFamily="Inter" fontWeight={800} fontSize={30} fill="#5a6a80" letterSpacing={4}>LAB RESULT · PANEL 7 · CHARCOAL</text>
    <rect x={-430} y={-170} width={860} height={10} rx={5} fill="#c8d4e0" /><rect x={-430} y={-170} width={860 * sat(k * 1.4)} height={10} rx={5} fill="#2a6ad8" />
    <text x={0} y={20} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={110} fill="#1a2a4a" opacity={sat(k * 2 - 0.8)}>30,140</text>
    <text x={0} y={110} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={50} fill="#c8282a" opacity={sat(k * 2 - 0.8)}>YEARS OLD</text></g>
</SV>;

// ---------- title card + end card ----------
export const TitleCard: React.FC<{ f: number }> = ({ f }) => <SV bg="#0e1a2a">
  <Glow x={960} y={540} r={900} color="#8ac0ff" o={0.25} />
  {Array.from({ length: 70 }, (_, i) => <circle key={i} cx={(rnd(i, 1) * 2200 + f * 8) % 2200 - 100} cy={(rnd(i, 2) * 1200 + f * 4) % 1200} r={2 + rnd(i, 3) * 3} fill="#fff" opacity={0.6} />)}
  <g transform="translate(1500 1100) scale(0.9)" opacity={0.35}><Mammoth ph={f * 0.05} /></g>
  <text x={960} y={420} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={54} fill="#8ac0ff" letterSpacing={18} opacity={sat(f / 14)}>WHAT IF</text>
  <text x={960} y={560} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={116} fill="#fff" opacity={sat((f - 8) / 12)}>YOU WOKE UP</text>
  <text x={960} y={700} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={116} fill="#fff" opacity={sat((f - 14) / 12)}><tspan fill="#ffd34a">30,000</tspan> YEARS AGO?</text>
</SV>;
export const EndCard: React.FC<{ f: number }> = ({ f }) => <SV bg="#140e0a">
  <Glow x={500} y={600} r={700} color="#ff9a3a" o={0.3} />
  <Character look={ELI} pose={{ facing: 1, mouth: "smile", aR: [125 + 6 * Math.sin(f * 0.3), 25 + 15 * Math.sin(f * 0.3)] }} x={380} y={960} s={1.25} f={f} seed={1} rim={{ dx: 4, dy: -3, color: "#ffb060" }} />
  <Character look={NIA} pose={{ facing: 1, mouth: "smile" }} x={600} y={960} s={1.2} f={f} seed={2} />
  <Character look={PIP} pose={{ facing: 1, mouth: "grin" }} x={780} y={960} s={1.2} f={f} seed={3} />
  <text x={110} y={150} fontFamily="Inter" fontWeight={900} fontSize={64} fill="#fff" opacity={sat(f / 12)}>THANKS FOR WATCHING</text>
  <text x={110} y={220} fontFamily="Inter" fontWeight={800} fontSize={34} fill="#ffb060" opacity={sat((f - 8) / 12)}>WHAT WOULD YOU TAKE 30,000 YEARS BACK?</text>
  <g opacity={sat((f - 20) / 10)} transform={`translate(560 1020) scale(${1 + 0.04 * Math.sin(f * 0.15)})`}><rect x={-230} y={-44} width={460} height={88} rx={44} fill="#e8322a" /><text x={0} y={16} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={40} fill="#fff">SUBSCRIBE FOR PART 2</text></g>
</SV>;
