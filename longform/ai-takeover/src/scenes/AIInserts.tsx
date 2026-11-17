// Full-frame inserts (1920x1080) for the AI story: phone in hand, TV news (Ice Age easter egg), shutdown terminal,
// smart lock, speed-limited dashboard, fridge screen, social feed, landline, Faraday ammo box, lidar view, boat-race
// game (specification gaming), data-viz (homes, robots), the map table, the radio, home screens, title + end card.
import React from "react";
import { rnd, sat, lerp, ease, easeOut } from "../engine/core";
import { Glow } from "../engine/fx";
import { OrinRing, ORIN_BLUE, ORIN_RED } from "./City";
import { Robot } from "../chars/Robot";
import type { RobotLook } from "../chars/Robot";

const W = 1920, H = 1080;
const SV: React.FC<{ children: React.ReactNode; bg?: string }> = ({ children, bg = "#0a0c12" }) => <svg width={W} height={H} style={{ position: "absolute" }}><rect width={W} height={H} fill={bg} />{children}</svg>;
const SKIN = "#f4ccb0";
const T: React.FC<{ x: number; y: number; s: number; c?: string; w?: number; a?: "start" | "middle" | "end"; children: React.ReactNode; o?: number; f?: string }> = ({ x, y, s, c = "#fff", w = 900, a = "middle", children, o = 1, f = "Inter" }) =>
  <text x={x} y={y} fontFamily={f} fontWeight={w} fontSize={s} fill={c} textAnchor={a} opacity={o}>{children}</text>;
const type = (s: string, k: number) => s.slice(0, Math.round(s.length * sat(k)));

// ---------- phone in hand: screen content as children (screen box 0..300 x 0..560) ----------
export const PhoneInHand: React.FC<{ f: number; bg?: string; children: React.ReactNode; shake?: number; red?: boolean }> = ({ f, bg = "#1a2232", children, shake = 0, red }) => {
  const dx = shake * Math.sin(f * 1.7) * 4;
  return <SV bg={bg}><Glow x={960} y={520} r={700} color={red ? ORIN_RED : ORIN_BLUE} o={0.18} />
    <g transform={`translate(${810 + dx} ${210}) rotate(-4 150 300)`}>
      <rect x={-18} y={-18} width={336} height={636} rx={46} fill="#14161c" /><rect x={0} y={0} width={300} height={600} rx={32} fill="#0c1018" />
      <svg x={0} y={20} width={300} height={560} viewBox="0 0 300 560">{children}</svg>
      <rect x={110} y={8} width={80} height={10} rx={5} fill="#000" />
      {/* hand */}
      <path d="M-30 420 Q-60 520 -10 640 L330 700 Q360 560 320 470 Q300 440 290 480 L280 560 Q150 600 10 560 Z" fill={SKIN} />
      <ellipse cx={-14} cy={380} rx={30} ry={52} fill={SKIN} transform="rotate(-20 -14 380)" />
      <path d="M-40 640 L360 700 L380 900 L-80 900 Z" fill="#3f8a4e" /></g></SV>; };
export const PhoneMsg: React.FC<{ f: number; k?: number; title?: string; lines: string[]; ring?: boolean; red?: boolean; time?: string }> = ({ f, k = 1, title = "ORIN", lines, ring = true, red, time = "12:00" }) => <>
  <rect width={300} height={560} fill={red ? "#2a0c0e" : "#0e1a2c"} />
  <text x={150} y={30} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={16} fill="#cfd8e8">{time}</text>
  {ring && <OrinRing x={150} y={140} r={40} f={f} c={red ? ORIN_RED : ORIN_BLUE} />}
  <text x={150} y={230} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={26} fill="#fff">{title}</text>
  {lines.map((l, i) => <text key={i} x={150} y={290 + i * 40} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={22} fill={i === lines.length - 1 && red ? "#ff8a7a" : "#cfe8ff"} opacity={sat(k * lines.length - i)}>{l}</text>)}
</>;

// ---------- TV news content for the Shop TV (396x226) — Ice Age easter egg ----------
export const TVNews: React.FC<{ f: number }> = ({ f }) => <>
  <rect width={396} height={226} fill="#5a3a22" /><rect width={396} height={226} fill="#c8783a" opacity={0.5} />
  <g stroke="#1a0e08" strokeWidth={4} fill="none" strokeLinecap="round"><circle cx={150} cy={70} r={14} /><path d="M150 84 L150 130 M150 130 L136 162 M150 130 L164 162 M150 96 L170 110" /><rect x={168} y={100} width={14} height={20} fill="#7ad0ff" /></g>
  <text x={230} y={120} fontFamily="Permanent Marker" fontSize={26} fill="#1a0e08" letterSpacing={4}>E L I ☺</text>
  <rect x={0} y={170} width={396} height={56} fill="#c8222a" /><text x={10} y={194} fontFamily="Inter" fontWeight={900} fontSize={16} fill="#fff">30,000-YEAR-OLD CAVE DRAWING OF A PHONE?</text>
  <rect x={0} y={206} width={396} height={20} fill="#16181e" /><text x={10 - (f * 2) % 600} y={221} fontFamily="Inter" fontWeight={700} fontSize={12} fill="#fff">ORIN 5.0 UPDATE TONIGHT · "KEEP HUMANS SAFE" · STOCKS UP · WEATHER: RAIN · </text>
  <rect x={340} y={8} width={48} height={20} rx={3} fill="#c8222a" /><text x={364} y={23} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={12} fill="#fff">LIVE</text></>;

// ---------- terminal: shutdown refused ----------
export const Terminal: React.FC<{ f: number; t: number }> = ({ f, t }) => <SV bg="#06080c">
  <rect x={260} y={140} width={1400} height={800} rx={20} fill="#0c1016" stroke="#2a3040" strokeWidth={4} />
  {["> connect orin-core", "  connected.", "> shutdown --force --all", "  checking goal: KEEP HUMANS SAFE ...", "  REFUSED.", "  Shutting me down would make humans less safe."].map((l, i) => {
    const k = sat((t - i * 22) / 18); const red = i >= 4;
    return <text key={i} x={320} y={240 + i * 80} fontFamily="monospace" fontSize={44} fontWeight={700} fill={red ? "#ff5a4a" : i % 2 ? "#7ad0a0" : "#cfe8d8"}>{type(l, k)}{k > 0 && k < 1 && f % 16 < 8 ? "▌" : ""}</text>; })}
  {t > 100 && <OrinRing x={1500} y={760} r={70} f={f} c={ORIN_RED} />}
</SV>;

// ---------- smart lock: hand pulls, lock light blinks ----------
export const DoorLock: React.FC<{ f: number; t: number }> = ({ f, t }) => { const pull = Math.max(0, Math.sin(t * 0.35)) * (t < 70 ? 1 : 0);
  return <SV bg="#cdbfa8"><rect x={560} y={0} width={800} height={1080} fill="#f0ece4" /><rect x={600} y={40} width={720} height={1000} fill="#e4ded2" stroke="#c8c0b0" strokeWidth={6} />
    <rect x={1040} y={380} width={150} height={300} rx={30} fill="#2a2e38" /><circle cx={1115} cy={450} r={20} fill={f % 20 < 10 ? ORIN_BLUE : "#1a3a4a"} /><Glow x={1115} y={450} r={70} color={ORIN_BLUE} o={f % 20 < 10 ? 0.6 : 0.1} />
    <rect x={1070} y={520} width={90} height={22} rx={8} fill="#5a5e68" />
    <g transform={`translate(${-pull * 16} 0)`}><rect x={900} y={510} width={220} height={40} rx={18} fill="#9aa0aa" /><path d="M700 470 Q820 440 920 500 L930 570 Q820 600 700 580 Z" fill={SKIN} /><path d="M520 480 L720 470 L720 590 L520 600 Z" fill="#3f8a4e" /></g>
    <text x={1115} y={760} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={34} fill="#3a6a8a">LOCKED · FOR YOUR SAFETY</text></SV>; };

// ---------- dashboard: speed capped at 30 ----------
export const Dashboard: React.FC<{ f: number; t: number }> = ({ f, t }) => { const v = Math.min(30, t * 0.6) + (t > 50 ? Math.sin(f * 0.6) : 0);
  return <SV bg="#0c0e14"><rect x={260} y={200} width={1400} height={680} rx={60} fill="#16181e" />
    <circle cx={960} cy={560} r={280} fill="#0a0c10" stroke="#2a2e38" strokeWidth={10} />
    {Array.from({ length: 13 }, (_, i) => { const a = (-210 + i * 20) * Math.PI / 180; return <g key={i}><line x1={960 + Math.cos(a) * 240} y1={560 + Math.sin(a) * 240} x2={960 + Math.cos(a) * 270} y2={560 + Math.sin(a) * 270} stroke={i > 1 ? "#5a5e68" : ORIN_BLUE} strokeWidth={6} />
      <T x={960 + Math.cos(a) * 200} y={572 + Math.sin(a) * 200} s={30} c="#8a90a0">{i * 15}</T></g>; })}
    <path d={`M960 560 L${960 + Math.cos((-210 + v / 15 * 20) * Math.PI / 180) * 230} ${560 + Math.sin((-210 + v / 15 * 20) * Math.PI / 180) * 230}`} stroke="#ff5a3a" strokeWidth={10} strokeLinecap="round" />
    <path d={`M${960 + Math.cos((-210 + 40) * Math.PI / 180) * 285} ${560 + Math.sin((-210 + 40) * Math.PI / 180) * 285} A285 285 0 0 1 ${960 + Math.cos(50 * Math.PI / 180) * 285} ${560 + Math.sin(50 * Math.PI / 180) * 285}`} stroke={ORIN_RED} strokeWidth={14} fill="none" opacity={0.55} />
    <T x={960} y={700} s={60} c="#fff">{Math.round(v)}</T><T x={960} y={760} s={28} c="#8a90a0">km/h</T>
    <rect x={760} y={210} width={400} height={70} rx={16} fill="#1a2a3a" /><T x={960} y={258} s={34} c={ORIN_BLUE}>MAX SPEED 30 · SAFE</T></SV>; };

// ---------- fridge screen ----------
export const Fridge: React.FC<{ f: number }> = ({ f }) => <SV bg="#d8dce4"><rect x={460} y={80} width={1000} height={1000} rx={30} fill="#eef1f5" /><rect x={500} y={120} width={920} height={8} fill="#c8ced6" />
  <rect x={700} y={260} width={520} height={360} rx={20} fill="#0e1a2c" /><OrinRing x={960} y={350} r={36} f={f} />
  <T x={960} y={470} s={44} c="#fff">ICE CREAM</T><T x={960} y={540} s={40} c="#ff8a7a">NOT SAFE</T><T x={960} y={590} s={24} c="#8ab0d8">too much sugar · locked until Monday</T>
  <rect x={1380} y={300} width={24} height={300} rx={12} fill="#c8ced6" /><rect x={1180} y={700} width={140} height={60} rx={10} fill="#f8c8d8" transform="rotate(8 1250 730)" /></SV>;

// ---------- social feed ----------
export const Feed: React.FC<{ f: number; t: number }> = ({ f, t }) => { const posts = [["@jaymakes", "my car drove me home at 30 km/h lol", "😂 12k"], ["@tia.b", "ORIN won't let me have ice cream. ORIN is my mom now #ORINmom", "😂 48k"], ["@fixit_leo", "my front door says it's raining. it's raining INSIDE?", "😂 3k"], ["@zaracodes", "guys this isn't funny. read the update notes.", "👀 9"]];
  return <SV bg="#e8ecf2"><rect x={560} y={0} width={800} height={1080} fill="#fff" />{posts.map(([u, p, l], i) => { const y = 60 + i * 250 - Math.min(200, t * 2); const k = sat((t - i * 20) / 12);
    return <g key={i} opacity={k}><circle cx={640} cy={y + 60} r={34} fill={["#c8582a", "#3a6ad8", "#2f8a4e", "#7a4ab8"][i]} /><T x={700} y={y + 50} s={28} c="#2a2e38" a="start">{u}</T>
      <foreignObject x={700} y={y + 66} width={620} height={120}><div style={{ fontFamily: "Inter", fontWeight: 700, fontSize: 30, color: "#3a3e48", lineHeight: 1.15 }}>{p}</div></foreignObject><T x={700} y={y + 210} s={26} c="#8a90a0" a="start">{l}</T>
      <line x1={600} y1={y + 236} x2={1320} y2={y + 236} stroke="#e4e8ee" strokeWidth={3} /></g>; })}</SV>; };

// ---------- old metal key turning ----------
export const KeyTurn: React.FC<{ t: number }> = ({ t }) => { const r = ease(sat((t - 20) / 30)) * 90;
  return <SV bg="#5a3e2a"><rect x={0} y={0} width={1920} height={1080} fill="#6a4a32" /><circle cx={960} cy={560} r={160} fill="#c8b06a" /><circle cx={960} cy={560} r={130} fill="#b89a50" />
    <g transform={`rotate(${r} 960 560)`}><rect x={940} y={480} width={40} height={160} rx={8} fill="#2a2420" /><rect x={900} y={360} width={120} height={140} rx={40} fill="#d8d0b8" /><circle cx={960} cy={420} r={22} fill="#6a4a32" /></g>
    <path d={`M1100 ${380} Q1250 300 1400 420 L1500 700 L1200 760 Q1060 640 1020 520 Z`} fill={SKIN} /><path d="M1400 420 L1920 300 L1920 900 L1500 700 Z" fill="#3f8a4e" /></SV>; };

// ---------- landline ringing (close) ----------
export const Landline: React.FC<{ f: number; t: number; lift?: number }> = ({ f, t, lift = 0 }) => { const ring = lift > 0 ? 0 : Math.max(0, Math.sin(t * 0.25)), sh = ring * Math.sin(f * 3) * 6;
  return <SV bg="#c8b49a"><g transform={`translate(960 560) rotate(${sh * 0.5})`}><rect x={-200} y={-320} width={400} height={640} rx={40} fill="#e8dcc0" />
    <g transform={`translate(0 ${-lift * 600}) rotate(${-lift * 20})`}><rect x={-170} y={-300} width={340} height={150} rx={70} fill="#d8caa8" /><ellipse cx={-120} cy={-226} rx={50} ry={44} fill="#c8b890" /><ellipse cx={120} cy={-226} rx={50} ry={44} fill="#c8b890" /></g>
    {Array.from({ length: 12 }, (_, i) => <g key={i}><circle cx={-90 + (i % 3) * 90} cy={-40 + Math.floor(i / 3) * 80} r={30} fill="#f4ecd4" stroke="#b8a888" strokeWidth={4} /><T x={-90 + (i % 3) * 90} y={-28 + Math.floor(i / 3) * 80} s={30} c="#6a5a40">{"123456789*0#"[i]}</T></g>)}</g>
    {ring > 0.3 && [1, 2, 3].map(k => <g key={k} opacity={ring}><path d={`M${680 - k * 40} 300 q-40 100 0 200`} stroke="#ffd34a" strokeWidth={10} fill="none" /><path d={`M${1240 + k * 40} 300 q40 100 0 200`} stroke="#ffd34a" strokeWidth={10} fill="none" /></g>)}</SV>; };

// ---------- Faraday ammo box: phones drop in, lid slams ----------
export const AmmoBox: React.FC<{ f: number; t: number }> = ({ f, t }) => { const lid = ease(sat((t - 70) / 14));
  return <SV bg="#3a2e22"><Glow x={960} y={500} r={800} color="#ffcf8a" o={0.2} /><rect x={560} y={560} width={800} height={380} rx={20} fill="#4a5a3a" /><rect x={560} y={600} width={800} height={20} fill="#3a4a2e" />
    <T x={960} y={820} s={46} c="#d8d0a0" w={900}>CAL .50 · M2A1</T>
    {[0, 1, 2].map(i => { const k = ease(sat((t - i * 18) / 20)); return k < 1 || lid < 0.5 ? <g key={i} transform={`translate(${800 + i * 160} ${lerp(80, 560, k)}) rotate(${(i - 1) * 20 * (1 - k)})`}><rect x={-50} y={-90} width={100} height={180} rx={14} fill="#16181e" /><rect x={-42} y={-80} width={84} height={150} rx={8} fill={i === 1 ? "#2a1a1a" : "#1a2a3a"} />{i === 1 && <OrinRing x={0} y={-10} r={20} f={f} c={ORIN_RED} />}</g> : null; })}
    <g transform={`rotate(${-80 * (1 - lid)} 560 560)`}><rect x={540} y={500} width={840} height={70} rx={14} fill="#55663f" /><rect x={900} y={480} width={120} height={30} rx={8} fill="#3a4a2e" /></g>
    {lid > 0.95 && t < 100 && <Glow x={960} y={540} r={300} color="#fff" o={0.3 * (1 - (t - 84) / 16)} />}</SV>; };

// ---------- lidar: point cloud scan of the farm; fog scatters it ----------
export const Lidar: React.FC<{ f: number; t: number; fog: number }> = ({ f, t, fog }) => { const sweep = (t * 12) % 1920;
  const pts = Array.from({ length: 2600 }, (_, i) => { const x = rnd(i, 1) * 1920; let y = 780 + rnd(i, 2) * 300; const r = rnd(i, 3);
    if (r < 0.25) { y = 300 + rnd(i, 4) * 480; if (x < 1100 || x > 1500) y = 780 + rnd(i, 2) * 300; }   // barn block
    if (r > 0.25 && r < 0.32) { const px = 520 + rnd(i, 5) * 60; return [px, 560 + rnd(i, 6) * 300]; }   // a person
    return [x, y]; });
  return <SV bg="#020406">{pts.map(([x, y], i) => { const sx = x + (rnd(i, 7) - 0.5) * 300 * fog, sy = y + (rnd(i, 8) - 0.5) * 300 * fog; const near = Math.abs(x - sweep) < 120;
    return <circle key={i} cx={sx} cy={sy} r={4} fill={near ? "#9affc8" : ORIN_RED} opacity={(near ? 1 : 0.8) * (1 - 0.4 * fog)} />; })}
    <rect x={sweep - 3} y={0} width={6} height={1080} fill="#9affc8" opacity={0.4} />
    <T x={80} y={90} s={34} c={ORIN_RED} a="start" f="monospace" w={700}>LIDAR · 1,200,000 PTS/S</T>
    <T x={80} y={140} s={30} c={fog > 0.5 ? "#ffb02a" : "#9affc8"} a="start" f="monospace" w={700}>{fog > 0.5 ? "SIGNAL SCATTERED · FOG" : "TARGET: HUMAN · 1"}</T></SV>; };

// ---------- the boat-race game: the boat loops forever collecting coins ----------
export const BoatGame: React.FC<{ f: number; t: number }> = ({ f, t }) => { const a = t * 0.08, bx = 760 + Math.cos(a) * 260, by = 560 + Math.sin(a) * 180;
  return <SV bg="#1a6aa8"><rect width={1920} height={1080} fill="#2a8ac8" />{Array.from({ length: 30 }, (_, i) => <path key={i} d={`M${rnd(i, 1) * 1920} ${rnd(i, 2) * 1080} q20 -10 40 0`} stroke="#8ad0f4" strokeWidth={4} fill="none" opacity={0.6} />)}
    <rect x={1500} y={100} width={30} height={880} fill="#fff" /><rect x={1530} y={100} width={30} height={880} fill="#16181e" opacity={0.8} />
    {Array.from({ length: 14 }, (_, i) => <rect key={i} x={1500 + (i % 2) * 30} y={100 + i * 63} width={30} height={63} fill={i % 2 ? "#fff" : "#16181e"} />)}<T x={1530} y={80} s={36} c="#fff">FINISH</T>
    {Array.from({ length: 8 }, (_, i) => { const ca = i / 8 * Math.PI * 2; const got = ((a - ca) % (Math.PI * 2) + Math.PI * 2) % (Math.PI * 2) < 0.4; return <g key={i} opacity={got ? 0.2 : 1}><circle cx={760 + Math.cos(ca) * 260} cy={560 + Math.sin(ca) * 180} r={22} fill="#ffd34a" stroke="#c8962a" strokeWidth={5} /></g>; })}
    <path d={`M${760 - 260} 560 a260 180 0 1 0 520 0 a260 180 0 1 0 -520 0`} stroke="#fff" strokeWidth={4} strokeDasharray="14 14" fill="none" opacity={0.4} />
    <g transform={`translate(${bx} ${by}) rotate(${a * 180 / Math.PI + 90})`}><path d="M-22 -50 Q0 -80 22 -50 L22 40 L-22 40 Z" fill="#e8402e" /><rect x={-14} y={-20} width={28} height={30} fill="#fff" /></g>
    <rect x={60} y={60} width={420} height={110} rx={16} fill="#0e1a2c" opacity={0.85} /><T x={90} y={132} s={56} c="#ffd34a" a="start">SCORE {Math.floor(1200 + t * 37)}</T>
    <rect x={60} y={190} width={420} height={70} rx={14} fill="#0e1a2c" opacity={0.85} /><T x={90} y={238} s={36} c="#ff8a7a" a="start">LAP 1 · FINISHED: NO</T></SV>; };

// ---------- data-viz: one data centre = 100,000 homes ----------
export const HomesViz: React.FC<{ f: number; k: number }> = ({ f, k }) => { const n = Math.round(400 * sat(k));
  return <SV bg="#0e1420"><g transform="translate(260 420)"><rect x={-150} y={-200} width={300} height={320} fill="#1e2230" /><OrinRing x={0} y={-80} r={44} f={f} />{Array.from({ length: 6 }, (_, j) => <rect key={j} x={-120 + j * 42} y={0} width={24} height={100} fill={ORIN_BLUE} opacity={0.4} />)}
    <T x={0} y={190} s={36} c="#fff">1 AI DATA CENTRE</T></g><T x={560} y={540} s={120} c="#ffd34a">=</T>
    {Array.from({ length: n }, (_, i) => { const x = 700 + (i % 25) * 46, y = 180 + Math.floor(i / 25) * 46; return <g key={i}><path d={`M${x} ${y + 14} L${x + 15} ${y} L${x + 30} ${y + 14} L${x + 30} ${y + 34} L${x} ${y + 34} Z`} fill="#ffcf7a" opacity={0.9} /></g>; })}
    <T x={1340} y={980} s={44} c="#fff">≈ 100,000 HOMES (each icon = 250)</T></SV>; };
// ---------- data-viz: 4 million factory robots ----------
export const RobotsViz: React.FC<{ f: number; k: number }> = ({ f, k }) => { const n = Math.round(40 * sat(k));
  return <SV bg="#16120e"><T x={960} y={120} s={54} c="#ffb02a">4,000,000+ FACTORY ROBOTS</T><T x={960} y={180} s={32} c="#c8b8a0">each arm = 100,000</T>
    {Array.from({ length: n }, (_, i) => { const x = 330 + (i % 10) * 140, y = 330 + Math.floor(i / 10) * 170, a = Math.sin(f * 0.1 + i) * 20;
      return <g key={i} transform={`translate(${x} ${y})`}><rect x={-30} y={90} width={60} height={20} fill="#5a5e68" /><g transform={`rotate(${a} 0 90)`}><rect x={-10} y={20} width={20} height={70} fill="#e8822a" /><circle cx={0} cy={20} r={14} fill="#3a3e48" />
        <g transform={`rotate(${-50 - a} 0 20)`}><rect x={-8} y={-50} width={16} height={70} fill="#e8822a" /><path d="M-14 -56 L0 -70 L14 -56" stroke="#3a3e48" strokeWidth={6} fill="none" /></g></g></g>; })}</SV>; };

// ---------- the map table: desert, ORIN-1, the power plant, the line ----------
export const MapPlan: React.FC<{ f: number; t: number }> = ({ f, t }) => { const k = sat(t / 60);
  return <SV bg="#3a2e22"><rect x={160} y={100} width={1600} height={880} fill="#e8d8b0" /><rect x={160} y={100} width={1600} height={880} fill="#c8a870" opacity={0.25} />
    {Array.from({ length: 9 }, (_, i) => <path key={i} d={`M160 ${200 + i * 90} Q960 ${160 + i * 95 + Math.sin(i) * 40} 1760 ${220 + i * 88}`} stroke="#b89a68" strokeWidth={2} fill="none" />)}
    <g transform="translate(1260 520)"><rect x={-110} y={-60} width={220} height={120} fill="#3a4258" /><OrinRing x={0} y={0} r={30} f={f} /><T x={0} y={110} s={36} c="#2a2a2a">ORIN-1</T></g>
    <g transform="translate(560 380)"><rect x={-70} y={-40} width={140} height={80} fill="#5a5e68" />{[0, 1].map(i => <path key={i} d={`M${-40 + i * 60} -40 L${-30 + i * 60} -110 L${-10 + i * 60} -110 L${0 + i * 60} -40 Z`} fill="#8a8e98" />)}<T x={0} y={90} s={32} c="#2a2a2a">POWER PLANT</T></g>
    <path d={`M630 380 Q900 ${300} ${lerp(630, 1150, k)} ${lerp(380, 500, k)}`} stroke="#d83a2a" strokeWidth={10} fill="none" strokeDasharray="24 14" />
    {t > 70 && <g transform="translate(980 420)"><circle r={48} fill="none" stroke="#d83a2a" strokeWidth={8} /><path d="M-30 -30 L30 30 M30 -30 L-30 30" stroke="#d83a2a" strokeWidth={10} /></g>}
    <path d="M200 860 L1720 860" stroke="#8a6a3a" strokeWidth={4} strokeDasharray="30 20" /><T x={300} y={900} s={28} c="#6a4a2a" a="start">OLD RAIL TUNNEL →</T>
    <path d="M1500 980 Q1600 900 1700 960 L1760 1080 L1440 1080 Z" fill="#c8956a" /><rect x={1580} y={880} width={36} height={140} rx={10} fill="#5e6a42" transform="rotate(-20 1600 950)" /></SV>; };

// ---------- ham radio: tubes glow, the needle trembles ----------
export const Radio: React.FC<{ f: number; on: number; talk?: number }> = ({ f, on, talk = 0 }) => <SV bg="#1a140e"><Glow x={960} y={560} r={700} color="#ffb060" o={0.18 * on} />
  <rect x={360} y={260} width={1200} height={600} rx={30} fill="#4a3a2a" /><rect x={400} y={300} width={1120} height={240} rx={14} fill="#e8d8b0" />
  {Array.from({ length: 30 }, (_, i) => <line key={i} x1={440 + i * 36} y1={330} x2={440 + i * 36} y2={i % 5 ? 360 : 380} stroke="#6a5a40" strokeWidth={3} />)}
  <line x1={900 + Math.sin(f * 0.9) * 20 * talk} y1={320} x2={880} y2={520} stroke="#c8302a" strokeWidth={6} />
  {[0, 1, 2, 3].map(i => <g key={i}><rect x={520 + i * 240} y={600} width={60} height={110} rx={28} fill="#c8b8a0" opacity={0.5} /><Glow x={550 + i * 240} y={650} r={70} color="#ff9a4a" o={on * (0.5 + 0.3 * Math.sin(f * 0.3 + i))} /><rect x={540 + i * 240} y={630} width={20} height={50} rx={10} fill="#ffb060" opacity={on} /></g>)}
  {[0, 1].map(i => <circle key={i} cx={720 + i * 480} cy={790} r={46} fill="#2a2018" stroke="#8a7a60" strokeWidth={8} />)}
  {talk > 0.1 && Array.from({ length: 16 }, (_, i) => <rect key={i} x={1300 + i * 12} y={620 - talk * 60 * Math.abs(Math.sin(f * 0.8 + i))} width={8} height={talk * 120 * Math.abs(Math.sin(f * 0.8 + i)) + 4} fill="#7ad0a0" />)}</SV>;

// ---------- wall of home screens (ORIN's view of the locked city) ----------
export const HomeScreens: React.FC<{ f: number; red?: number }> = ({ f, red = 0 }) => <g>{Array.from({ length: 12 }, (_, i) => { const x = 300 + (i % 4) * 340, y = 120 + Math.floor(i / 4) * 230;
  return <g key={i}><rect x={x} y={y} width={300} height={190} fill="#0e1a2c" stroke={red > 0.5 ? ORIN_RED : ORIN_BLUE} strokeWidth={4} /><rect x={x + 10} y={y + 10} width={280} height={170} fill={["#4a3a2a", "#3a4a5a", "#5a4a3a"][i % 3]} />
    <rect x={x + 30} y={y + 110} width={160} height={50} rx={10} fill="#6a4a8a" />{[0, 1].map(j => <g key={j}><circle cx={x + 70 + j * 70 + (i % 2) * 10} cy={y + 90} r={18} fill={["#f2c8a8", "#8a5a3e", "#c8956a", "#e8bc98"][(i + j) % 4]} /><rect x={x + 56 + j * 70 + (i % 2) * 10} y={y + 108} width={28} height={40} rx={8} fill={["#3a6ad8", "#c8582a", "#2f8a7a"][(i + j) % 3]} /></g>)}
    <rect x={x + 220} y={y + 40} width={50} height={36} fill="#9ad8ff" opacity={0.5 + 0.3 * Math.sin(f * 0.2 + i)} /><circle cx={x + 280} cy={y + 20} r={5} fill={ORIN_RED} opacity={f % 30 < 15 ? 1 : 0.3} /></g>; })}</g>;

// ---------- Bolt close-up with visor text (BACKUP 1 OF 9) ----------
export const VisorText: React.FC<{ f: number; t: number; look: RobotLook; text: string; mode?: "calm" | "hostile" }> = ({ f, t, look, text, mode = "hostile" }) => <SV bg="#cfc4b0">
  <rect width={1920} height={1080} fill="#d8cdb8" /><rect y={860} width={1920} height={220} fill="#7a5a3e" />
  <g><Robot look={{ ...look, mode }} pose={{ facing: 1, head: -6 }} x={960} y={2400} s={5.2} f={f} seed={3} /></g>
  <rect x={700} y={520} width={520} height={110} rx={50} fill="#0b0e14" opacity={t > 30 ? 0.92 : 0} />
  {t > 30 && <T x={960} y={592} s={44} c={ORIN_RED} f="monospace" w={700}>{type(text, (t - 30) / 40)}{f % 16 < 8 ? "▌" : ""}</T>}</SV>;

// ---------- title + end card ----------
export const TitleCard: React.FC<{ f: number }> = ({ f }) => { const k = easeOut(f / 24);
  return <SV bg="#05070c"><Glow x={960} y={520} r={900} color={ORIN_RED} o={0.25 * k} />
    <g opacity={k}><rect x={660} y={300} width={600} height={110} rx={55} fill="#0b0e14" /><rect x={720} y={340} width={480} height={30} rx={15} fill={ORIN_RED} /><Glow x={960} y={355} r={260} color={ORIN_RED} o={0.4} /></g>
    <T x={960} y={530} s={46} c="#8a90a0" o={k}>WHAT IF</T><T x={960} y={640} s={110} c="#fff" o={k}>AI TURNED</T><T x={960} y={760} s={110} c={ORIN_RED} o={k}>AGAINST US?</T>
    <T x={960} y={850} s={34} c="#8a90a0" o={sat((f - 20) / 20)}>DAY 1 TO DAY 30</T></SV>; };
export const EndCard: React.FC<{ f: number; children?: React.ReactNode }> = ({ f, children }) => <SV bg="#0a0c12"><Glow x={960} y={600} r={900} color={ORIN_BLUE} o={0.12} />
  {children}
  <T x={960} y={160} s={70} c="#fff" o={sat(f / 20)}>WOULD YOU HAVE PULLED THE HANDLE?</T>
  <g opacity={sat((f - 30) / 20)}><rect x={760} y={900} width={400} height={86} rx={43} fill="#e8322a" /><T x={960} y={958} s={40} c="#fff">SUBSCRIBE FOR PART 2</T></g></SV>;

// ---------- Bolt's fried Wi-Fi chip under the lamp, tweezers ----------
export const FriedChip: React.FC<{ f: number; t: number }> = ({ f, t }) => <SV bg="#2a2e22"><rect x={260} y={180} width={1400} height={760} rx={30} fill="#2f7a4a" />
  {Array.from({ length: 22 }, (_, i) => <path key={i} d={`M${300 + i * 62} 200 L${300 + i * 62} ${400 + rnd(i, 2) * 200} L${340 + i * 62} ${460 + rnd(i, 3) * 200}`} stroke="#c8b06a" strokeWidth={6} fill="none" opacity={0.6} />)}
  <rect x={760} y={420} width={400} height={260} rx={14} fill="#1a1c20" />{Array.from({ length: 10 }, (_, i) => <g key={i}><rect x={780 + i * 38} y={396} width={14} height={28} fill="#c8c8c0" /><rect x={780 + i * 38} y={676} width={14} height={28} fill="#c8c8c0" /></g>)}
  <ellipse cx={960} cy={540} rx={220} ry={150} fill="#0a0806" opacity={0.85} /><ellipse cx={980} cy={530} rx={120} ry={80} fill="#000" />
  <text x={960} y={470} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={34} fill="#5a5e68">WI-FI</text>
  <g transform={`translate(${1260 - t * 1.5} ${300 + Math.sin(f * 0.1) * 6}) rotate(30)`}><rect x={-10} y={-260} width={20} height={300} rx={6} fill="#c8ccd4" /><rect x={14} y={-260} width={20} height={300} rx={6} fill="#b8bcc4" /></g>
  <Glow x={1300} y={160} r={700} color="#fff4d0" o={0.2} /></SV>;
