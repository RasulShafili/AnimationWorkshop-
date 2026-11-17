// Character rig v2 (our own design). Same skeleton as hearing-100x Rig (root between the feet, hips 168 up, head
// centre 362 up, head r 60) so all camera maths carries over. New: glossy soft-shaded head with specular highlight,
// mitten hands, shaded clothes with styles (jacket / hoodie / coat / cardigan / suit), hats and hair, blink +
// breathing (idle), lip-sync (talk 0..1), gold "memory" irises, blush, earring, glasses, tie, props in hand.
import React from "react";
import { rnd } from "../engine/core";

export type Look = {
  skin?: string; top: string; topDark?: string; pants: string; shoes?: string; mitt?: string;
  style?: "jacket" | "hoodie" | "coat" | "cardigan" | "suit" | "shirt" | "labcoat" | "vest" | "scrubs" | "raincoat" | "uniform" | "fur";
  hair?: "beanie" | "bun" | "short" | "curly" | "bald" | "cap" | "long" | "none" | "pigtails" | "ponytail" | "messy" | "cowboy" | "helmet" | "wild" | "braid" | "hood"; hairColor?: string; hatColor?: string;
  glasses?: boolean; earring?: string; zombie?: boolean; mustache?: boolean; necklace?: string; paint?: boolean; scar?: boolean; furTrim?: string; backpack?: string; outfit?: "hazmat" | "police" | "pilot" | "hivis" | "flannel" | "nurse"; vest?: string; badge?: boolean; tie?: string; blush?: boolean; scale?: number; lashes?: boolean; beard?: boolean;
};
export type Pose = { seat?: boolean;
  lean?: number; head?: number; aL?: number[]; aR?: number[]; lL?: number[]; lR?: number[];
  eyes?: number; look?: number[]; brow?: number; browIn?: number;
  mouth?: "smile" | "grin" | "o" | "flat" | "open" | "frown" | "shout" | "worried" | "smirk" | "sad";
  talk?: number; bob?: number; facing?: 1 | -1; gold?: number; tears?: number; breath?: number; hold?: "cup" | "phone" | "photo" | "cards" | "pills" | "torch" | "walkie" | "keys" | "clipboard" | "binoculars" | "map" | "can" | "radio" | "mop" | "bat" | "crowbar" | "rifle" | "spear" | "torchfire" | "receiver" | "aim" | "port" | null; beam?: number; noBlink?: boolean;
};
type Rim = { dx: number; dy: number; color: string } | null;

const rad = (d: number) => (d * Math.PI) / 180;
const fk = (j: number[], len: number, a: number) => [j[0] + len * Math.sin(rad(a)), j[1] + len * Math.cos(rad(a))];
export const shade = (hex: string, k: number) => {
  const n = parseInt(hex.slice(1), 16); const c = (v: number) => Math.max(0, Math.min(255, Math.round(v * k)));
  return `rgb(${c((n >> 16) & 255)},${c((n >> 8) & 255)},${c(n & 255)})`;
};
let uidN = 0;
const R: React.FC<{ rim: Rim; children: (c: string | null) => React.ReactNode }> = ({ rim, children }) =>
  <>{rim && <g transform={`translate(${rim.dx},${rim.dy})`}>{children(rim.color)}</g>}{children(null)}</>;

// idle life: blink every 2–5 s (4-frame close), breathing, tiny head sway. seed per character.
export const idle = (f: number, seed = 1) => {
  let blink = 1; const period = 70 + Math.floor(rnd(seed, 3) * 80);
  const k = Math.floor((f + seed * 37) / period), t = (f + seed * 37) % period, at = Math.floor(rnd(k, seed) * (period - 8));
  if (t >= at && t < at + 5) blink = [0.5, 0.1, 0.05, 0.3, 0.8][t - at];
  return { blink, breath: Math.sin((f + seed * 11) / 34) * 2.2, sway: Math.sin((f + seed * 23) / 61) * 1.6 };
};

export const Character: React.FC<{ look: Look; pose: Pose; x: number; y: number; s?: number; rim?: Rim; f?: number; seed?: number; rot?: number; opacity?: number }> =
  ({ look, pose, x, y, s = 1, rim = null, f = 0, seed = 1, rot = 0, opacity = 1 }) => {
  const id = React.useMemo(() => `c${++uidN}`, []);
  const life = idle(f, seed);
  const P = { lean: 0, head: 0, aL: [8, 12], aR: [-6, 10], lL: [4, 4], lR: [-4, 4], eyes: 1, look: [0.5, 0], brow: 0, browIn: 0,
    mouth: "flat", talk: 0, bob: 0, facing: 1 as 1 | -1, gold: 0, tears: 0, breath: 1, hold: null, ...pose };
  const Z = !!look.zombie; const skin = Z ? (look.skin ?? "#6b8068") : (look.skin ?? "#24212f"), dark = look.topDark ?? shade(look.top, 0.68), shoes = look.shoes ?? "#17161d", mitt = look.mitt ?? skin;
  const lum = (() => { const n = parseInt(skin.slice(1), 16); return (0.299 * ((n >> 16) & 255) + 0.587 * ((n >> 8) & 255) + 0.114 * (n & 255)) / 255; })();
  const LIGHT = lum > 0.42, lineC = LIGHT ? "#5a2a24" : "#f4f1ea";
  const br = life.breath * P.breath;
  const hipY = -168 + P.bob, hipL = [-13, hipY], hipR = [13, hipY];
  const sh = [0, -292 + P.bob + br * 0.5], shL = [-27, sh[1] + 8], shR = [27, sh[1] + 8];
  const style = look.style ?? "jacket";
  const longCoat = style === "coat" || style === "labcoat" || style === "raincoat" || style === "fur";

  const leg = (hip: number[], a: number[], back: boolean) => {
    const k = fk(hip, 88, a[0]), ft = fk(k, 86, a[0] - a[1]);
    return <R rim={rim}>{(c) => <g>
      <path d={`M${hip[0]} ${hip[1]} L${k[0]} ${k[1]} L${ft[0]} ${ft[1]}`} stroke={c ?? (back ? shade(look.pants, 0.72) : look.pants)} strokeWidth={24} strokeLinecap="round" strokeLinejoin="round" fill="none" />
      <path d={`M${ft[0] - 14} ${ft[1] + 9} Q${ft[0] - 14} ${ft[1] - 8} ${ft[0] + 4} ${ft[1] - 6} Q${ft[0] + 30} ${ft[1] - 2} ${ft[0] + 30} ${ft[1] + 9} Z`}
        fill={c ?? (back ? shade(shoes, 0.7) : shoes)} transform={`rotate(${-(a[0] - a[1]) * 0.25} ${ft[0]} ${ft[1]})`} />
      {!c && <path d={`M${ft[0] - 14} ${ft[1] + 9} L${ft[0] + 30} ${ft[1] + 9}`} stroke="#fff" strokeOpacity={0.25} strokeWidth={3} transform={`rotate(${-(a[0] - a[1]) * 0.25} ${ft[0]} ${ft[1]})`} />}
    </g>}</R>;
  };
  const prop = (h: number[], ang: number) => {
    if (!P.hold) return null;
    const t = `translate(${h[0]} ${h[1]}) rotate(${-ang * 0.15})`;
    if (P.hold === "cup") return <g transform={`translate(${h[0]} ${h[1]})`}><path d="M-13 -30 L13 -30 L10 12 L-10 12 Z" fill="#f2efe6" /><rect x={-14} y={-36} width={28} height={7} rx={2} fill="#3a3530" /><rect x={-12} y={-14} width={24} height={10} fill="#b0623a" /></g>;
    if (P.hold === "phone") return <g transform={t}><rect x={-12} y={-34} width={24} height={44} rx={5} fill="#16151c" /><rect x={-10} y={-31} width={20} height={36} rx={3} fill="#7fd0ff" opacity={0.9} /></g>;
    if (P.hold === "photo") return <g transform={t}><rect x={-26} y={-40} width={52} height={40} fill="#f4f1e8" /><rect x={-22} y={-36} width={44} height={28} fill="#59606e" /></g>;
    if (P.hold === "cards") return <g transform={t}>{[0, 1, 2, 3].map(i => <rect key={i} x={-12 + i * 5} y={-36} width={24} height={34} rx={3} fill="#fbf8f0" stroke="#c9302c" strokeWidth={1.5} transform={`rotate(${-18 + i * 12} 0 -2)`} />)}</g>;
    if (P.hold === "pills") return <g transform={t}><rect x={-10} y={-34} width={20} height={30} rx={4} fill="#e8a33a" opacity={0.9} /><rect x={-11} y={-40} width={22} height={9} rx={2} fill="#f4f4f4" /></g>;
    if (P.hold === "torch") return <g transform={`translate(${h[0]} ${h[1]}) rotate(${-ang + 90})`}>{(P.beam ?? 0) > 0 && <path d="M30 -10 L560 -150 L560 150 L30 10 Z" fill="#fff6c8" opacity={0.16 * (P.beam ?? 0)} style={{ mixBlendMode: "screen" }} />}<rect x={-14} y={-8} width={44} height={16} rx={4} fill="#2a2a32" /><rect x={26} y={-11} width={10} height={22} rx={3} fill="#4a4a54" /><ellipse cx={36} cy={0} rx={3} ry={9} fill="#fff7cf" opacity={(P.beam ?? 0) > 0 ? 1 : 0.3} /></g>;
    if (P.hold === "walkie") return <g transform={t}><rect x={-11} y={-40} width={22} height={40} rx={5} fill="#e84a3a" /><rect x={-8} y={-35} width={16} height={12} rx={2} fill="#2a1a1a" /><line x1={6} y1={-40} x2={6} y2={-62} stroke="#222" strokeWidth={4} strokeLinecap="round" /><circle cx={0} cy={-14} r={4} fill="#ffd34a" /></g>;
    if (P.hold === "keys") return <g transform={t}><circle cx={0} cy={6} r={9} stroke="#c9b57a" strokeWidth={3} fill="none" />{[-30, 0, 30].map(r => <rect key={r} x={-2} y={12} width={4} height={18} fill="#d8d2c0" transform={`rotate(${r} 0 8)`} />)}</g>;
    if (P.hold === "clipboard") return <g transform={t}><rect x={-26} y={-58} width={52} height={66} rx={4} fill="#9a6a3a" /><rect x={-21} y={-50} width={42} height={54} fill="#f6f3ea" /><rect x={-9} y={-62} width={18} height={9} rx={2} fill="#9aa0aa" />{[0, 1, 2, 3].map(i => <line key={i} x1={-15} y1={-40 + i * 12} x2={15} y2={-40 + i * 12} stroke="#8a8a96" strokeWidth={2.5} />)}</g>;
    if (P.hold === "binoculars") return <g transform={`translate(${h[0]} ${h[1]})`}><rect x={-6} y={-22} width={18} height={30} rx={6} fill="#26262e" /><rect x={14} y={-22} width={18} height={30} rx={6} fill="#26262e" /><rect x={8} y={-14} width={10} height={10} fill="#3a3a44" /></g>;
    if (P.hold === "map") return <g transform={t}><path d="M-44 -50 L-14 -58 L16 -50 L46 -58 L46 4 L16 12 L-14 4 L-44 12 Z" fill="#efe4c6" /><path d="M-14 -58 L-14 4 M16 -50 L16 12" stroke="#c8b88e" strokeWidth={2} /><path d="M-34 -30 Q0 -10 34 -40" stroke="#d24a3a" strokeWidth={3} fill="none" strokeDasharray="5 4" /></g>;
    if (P.hold === "can") return <g transform={t}><rect x={-10} y={-26} width={20} height={26} rx={3} fill="#c8342c" /><rect x={-10} y={-18} width={20} height={9} fill="#f2ead8" /></g>;
    if (P.hold === "radio") return <g transform={t}><rect x={-30} y={-44} width={60} height={40} rx={6} fill="#4a3a2e" /><circle cx={-12} cy={-24} r={11} fill="#2a221c" /><rect x={6} y={-36} width={18} height={10} fill="#e8c86a" /></g>;
    if (P.hold === "bat") return <g transform={`translate(${h[0]} ${h[1]}) rotate(${-ang + 180})`}><path d="M-5 -10 L5 -10 L11 150 Q0 162 -11 150 Z" fill="#c8ccd4" /><path d="M-2 -10 L-1 150" stroke="#fff" strokeOpacity={0.5} strokeWidth={3} /><rect x={-6} y={-24} width={12} height={22} rx={3} fill="#1a1a20" /></g>;
    if (P.hold === "crowbar") return <g transform={`translate(${h[0]} ${h[1]}) rotate(${-ang + 180})`}><path d="M0 -20 L0 130 Q0 150 18 150" stroke="#b8323a" strokeWidth={9} fill="none" strokeLinecap="round" /><path d="M0 -20 l-10 -10" stroke="#b8323a" strokeWidth={8} strokeLinecap="round" /><path d="M-2 0 L-2 120" stroke="#fff" strokeOpacity={0.25} strokeWidth={2} /></g>;
    if (P.hold === "aim") return <g><rect x={-30} y={-306} width={70} height={18} rx={5} fill="#6a4a2e" /><rect x={30} y={-302} width={170} height={11} rx={3} fill="#2a2a2e" /><rect x={196} y={-300} width={14} height={7} fill="#1a1a1e" />
      <rect x={60} y={-292} width={12} height={22} rx={2} fill="#1a1a1e" /><rect x={90} y={-292} width={46} height={10} rx={3} fill="#6a4a2e" /><rect x={70} y={-312} width={34} height={8} rx={3} fill="#3a3a40" /></g>;
    if (P.hold === "port") return <g transform="rotate(-45 15 -250)"><rect x={-95} y={-259} width={70} height={18} rx={5} fill="#6a4a2e" /><rect x={-35} y={-255} width={170} height={11} rx={3} fill="#2a2a2e" /><rect x={131} y={-253} width={14} height={7} fill="#1a1a1e" /><rect x={25} y={-245} width={46} height={10} rx={3} fill="#6a4a2e" /></g>;
    if (P.hold === "rifle") return <g transform={`translate(${h[0]} ${h[1]}) rotate(${-ang + 150})`}><rect x={-6} y={-60} width={12} height={150} rx={3} fill="#2a2a2e" /><path d="M-8 60 L8 60 L14 120 L-10 120 Z" fill="#6a4a2e" /><rect x={-4} y={-90} width={6} height={36} fill="#1a1a1e" /><rect x={-10} y={0} width={10} height={26} rx={2} fill="#1a1a1e" /></g>;
    if (P.hold === "spear") return <g transform={`translate(${h[0]} ${h[1]}) rotate(${-ang * 0.3})`}><line x1={0} y1={170} x2={0} y2={-230} stroke="#8a6a44" strokeWidth={8} strokeLinecap="round" /><path d="M-12 -226 L0 -290 L12 -226 Z" fill="#7a808a" stroke="#4a4e58" strokeWidth={3} /><path d="M-8 -230 L8 -210" stroke="#5a3e28" strokeWidth={4} /></g>;
    if (P.hold === "torchfire") return <g transform={`translate(${h[0]} ${h[1]}) rotate(${-ang * 0.3})`}><line x1={0} y1={60} x2={0} y2={-90} stroke="#6a4a2a" strokeWidth={10} strokeLinecap="round" /><path d={`M-18 -90 Q0 ${-170 - 10 * Math.sin(f * 0.5)} 18 -90 Z`} fill="#ffb84a" /><path d={`M-9 -92 Q0 ${-140 - 8 * Math.sin(f * 0.7)} 9 -92 Z`} fill="#fff2b0" /></g>;
    if (P.hold === "receiver") return <g transform={`translate(${h[0]} ${h[1]})`}><path d="M-10 -46 Q-26 -40 -22 -20 L-14 24 Q-12 44 6 46 L14 40 Q4 30 2 10 L0 -20 Q2 -34 10 -42 Z" fill="#e8dcc0" stroke="#b8a888" strokeWidth={2} />
      <path d="M2 44 q10 30 -6 50 q-16 20 4 44 q16 22 -4 46" stroke="#d4c6a4" strokeWidth={4} fill="none" strokeDasharray="6 3" /></g>;
    if (P.hold === "mop") return <g transform={`translate(${h[0]} ${h[1]}) rotate(${-ang * 0.3})`}><line x1={0} y1={-150} x2={0} y2={160} stroke="#b08a5a" strokeWidth={8} strokeLinecap="round" /><path d="M-26 150 Q0 196 26 150 Z" fill="#d8d4c8" /></g>;
    return null;
  };
  const arm = (s0: number[], a: number[], back: boolean) => {
    const e = fk(s0, 78, a[0]), h = fk(e, 70, a[0] + a[1]);
    return <R rim={rim}>{(c) => <g>
      <path d={`M${s0[0]} ${s0[1]} L${e[0]} ${e[1]} L${h[0]} ${h[1]}`} stroke={c ?? (back ? dark : look.top)} strokeWidth={21} strokeLinecap="round" strokeLinejoin="round" fill="none" />
      {!c && !back && <path d={`M${s0[0]} ${s0[1]} L${e[0]} ${e[1]}`} stroke="#fff" strokeOpacity={0.12} strokeWidth={6} strokeLinecap="round" transform="translate(-4,-2)" />}
      {!c && style !== "shirt" && <circle cx={h[0] - (h[0] - e[0]) * 0.12} cy={h[1] - (h[1] - e[1]) * 0.12} r={12} fill={back ? shade(look.top, 0.55) : shade(look.top, 0.8)} />}
      <circle cx={h[0]} cy={h[1]} r={15} fill={c ?? (back ? shade(mitt, 0.8) : `url(#${id}m)`)} />
      {!c && <circle cx={h[0] + 9 * Math.cos(rad(a[0] + a[1]))} cy={h[1] - 9 * Math.sin(rad(a[0] + a[1])) - 4} r={6.5} fill={back ? shade(mitt, 0.8) : mitt} />}
      {!c && (P.hold === "receiver" ? back : !back) && prop(h, a[0] + a[1])}
    </g>}</R>;
  };
  const bot = longCoat ? hipY + 74 : hipY + 14;
  const torso = <R rim={rim}>{(c) => <g>
    {look.backpack && !c && <rect x={-58} y={sh[1] + 4} width={44} height={110} rx={14} fill={look.backpack} />}
    {style === "hoodie" && !c && <path d={`M-34 ${sh[1] - 2} Q0 ${sh[1] - 30} 34 ${sh[1] - 2} Q0 ${sh[1] + 14} -34 ${sh[1] - 2} Z`} fill={dark} />}
    <path d={`M-32 ${sh[1] - 4} Q0 ${sh[1] - 18} 32 ${sh[1] - 4} Q46 ${sh[1] + 2} 44 ${sh[1] + 34} Q42 ${hipY - 20} ${longCoat ? 50 : 40} ${bot} Q0 ${bot + 12} ${longCoat ? -50 : -40} ${bot} Q-42 ${hipY - 20} -44 ${sh[1] + 34} Q-46 ${sh[1] + 2} -32 ${sh[1] - 4} Z`}
      fill={c ?? `url(#${id}t)`} />
    {!c && <>
      <path d={`M-42 ${sh[1] + 4} Q-16 ${sh[1] - 8} -8 ${sh[1]} L-12 ${bot + 6} Q-28 ${bot + 4} -38 ${bot} Z`} fill={dark} opacity={0.45} />
      {style === "jacket" && <><path d={`M-20 ${sh[1] - 10} L0 ${sh[1] + 14} L20 ${sh[1] - 10}`} stroke={shade(look.top, 1.25)} strokeWidth={7} fill="none" strokeLinejoin="round" /><line x1={2} y1={sh[1] + 14} x2={2} y2={bot + 4} stroke={shade(look.top, 0.55)} strokeWidth={3} /><rect x={-40} y={bot - 12} width={80} height={12} rx={5} fill={shade(look.top, 0.75)} /></>}
      {style === "hoodie" && <><path d={`M-8 ${sh[1] + 4} L-10 ${sh[1] + 40} M8 ${sh[1] + 4} L10 ${sh[1] + 40}`} stroke="#f4f1ea" strokeWidth={3} strokeLinecap="round" /><path d={`M-24 ${hipY - 30} Q0 ${hipY - 36} 24 ${hipY - 30} L22 ${hipY - 6} L-22 ${hipY - 6} Z`} fill={dark} opacity={0.6} /></>}
      {longCoat && <><path d={`M-18 ${sh[1] - 8} L0 ${sh[1] + 40} L18 ${sh[1] - 8}`} fill={style === "labcoat" ? "#9ab0c8" : "#e9e2d2"} /><path d={`M-22 ${sh[1] - 8} L-4 ${sh[1] + 48} L-14 ${sh[1] + 50} L-34 ${sh[1] + 4} Z`} fill={shade(look.top, style === "labcoat" ? 0.9 : 1.15)} /><path d={`M22 ${sh[1] - 8} L4 ${sh[1] + 48} L14 ${sh[1] + 50} L34 ${sh[1] + 4} Z`} fill={shade(look.top, style === "labcoat" ? 0.9 : 1.15)} /><line x1={0} y1={sh[1] + 48} x2={0} y2={bot + 8} stroke={shade(look.top, 0.6)} strokeWidth={3} /></>}
      {style === "cardigan" && <><path d={`M-16 ${sh[1] - 8} L0 ${sh[1] + 30} L16 ${sh[1] - 8}`} fill="#f0e8dc" />{[0, 1, 2, 3].map(i => <circle key={i} cx={3} cy={sh[1] + 40 + i * 22} r={3.6} fill="#f4ecd8" />)}<line x1={0} y1={sh[1] + 30} x2={0} y2={bot + 6} stroke={shade(look.top, 0.6)} strokeWidth={2.5} /></>}
      {style === "suit" && <><path d={`M-18 ${sh[1] - 8} L0 ${sh[1] + 50} L18 ${sh[1] - 8}`} fill="#f4f2ee" /><path d={`M0 ${sh[1] + 2} L-6 ${sh[1] + 10} L0 ${sh[1] + 56} L6 ${sh[1] + 10} Z`} fill={look.tie ?? "#c8a23a"} /><path d={`M-20 ${sh[1] - 8} L-2 ${sh[1] + 56} L-30 ${sh[1] + 10} Z M20 ${sh[1] - 8} L2 ${sh[1] + 56} L30 ${sh[1] + 10} Z`} fill={shade(look.top, 1.3)} /></>}
      {look.outfit === "hazmat" && <><rect x={-44} y={sh[1] + 30} width={88} height={10} fill="#3a3a30" opacity={0.5} /><rect x={-14} y={sh[1] + 50} width={28} height={20} rx={3} fill="#2a2a24" opacity={0.6} /></>}
      {look.outfit === "police" && <><path d={`M-20 ${sh[1] - 6} L0 ${sh[1] + 10} L20 ${sh[1] - 6}`} stroke="#141a2a" strokeWidth={5} fill="none" /><path d={`M-30 ${sh[1] + 26} l10 -6 l10 6 l-2 12 l-8 4 l-8 -4 Z`} fill="#c8b06a" /><rect x={-42} y={hipY - 16} width={84} height={11} fill="#141418" /></>}
      {look.outfit === "pilot" && <><path d={`M0 ${sh[1] + 2} L-6 ${sh[1] + 10} L0 ${sh[1] + 56} L6 ${sh[1] + 10} Z`} fill="#1a2238" />{[-1, 1].map(k => <rect key={k} x={k > 0 ? 26 : -40} y={sh[1] - 4} width={14} height={8} fill="#1a2238" />)}<rect x={12} y={sh[1] + 24} width={20} height={5} fill="#c8a83a" /></>}
      {look.outfit === "hivis" && <><path d={`M-40 ${sh[1] + 4} L-12 ${sh[1] - 4} L-8 ${bot} L-38 ${bot} Z M40 ${sh[1] + 4} L12 ${sh[1] - 4} L8 ${bot} L38 ${bot} Z`} fill="#f08a1a" opacity={0.85} /><rect x={-42} y={sh[1] + 60} width={84} height={8} fill="#e8e8a0" opacity={0.8} /></>}
      {look.outfit === "flannel" && <>{[0, 1, 2, 3, 4].map(i => <line key={i} x1={-44} y1={sh[1] + 10 + i * 22} x2={44} y2={sh[1] + 10 + i * 22} stroke="#000" strokeOpacity={0.25} strokeWidth={5} />)}{[-30, -10, 10, 30].map(x => <line key={x} x1={x} y1={sh[1] - 6} x2={x} y2={bot} stroke="#000" strokeOpacity={0.2} strokeWidth={5} />)}</>}
      {look.outfit === "nurse" && <><path d={`M-16 ${sh[1] - 8} L0 ${sh[1] + 20} L16 ${sh[1] - 8}`} stroke={shade(look.top, 0.6)} strokeWidth={5} fill={skin} /><rect x={10} y={sh[1] + 40} width={20} height={18} rx={3} fill={shade(look.top, 0.85)} /></>}
      {style === "fur" && <>{[-1, 1].map(k => <path key={k} d={`M${k * 4} ${sh[1] - 4} L${k * 6} ${bot + 6}`} stroke={shade(look.top, 0.55)} strokeWidth={3} strokeDasharray="6 6" />)}
        <path d={`M-46 ${sh[1] + 2} ${Array.from({ length: 9 }, (_, i) => `Q${-40 + i * 10} ${sh[1] - 16 + (i % 2) * 8} ${-36 + i * 10} ${sh[1] - 2}`).join(" ")} L46 ${sh[1] + 2} Q0 ${sh[1] + 20} -46 ${sh[1] + 2} Z`} fill={look.furTrim ?? "#efe6d6"} />
        <path d={`M${longCoat ? -50 : -40} ${bot} ${Array.from({ length: 10 }, (_, i) => `l5 ${i % 2 ? 9 : -9} l5 ${i % 2 ? -9 : 9}`).join(" ")}`} stroke={look.furTrim ?? "#efe6d6"} strokeWidth={7} fill="none" strokeLinejoin="round" />
        <path d={`M-44 ${hipY - 18} Q0 ${hipY - 8} 44 ${hipY - 18}`} stroke="#5a3e24" strokeWidth={6} fill="none" /></>}
      {look.necklace && <g>{[-3, -2, -1, 0, 1, 2, 3].map(i => <path key={i} d={`M${i * 9} ${sh[1] + 22 - Math.abs(i) * 3} l-3 ${10 - Math.abs(i)} l6 0 Z`} fill={look.necklace} />)}<path d={`M-30 ${sh[1] + 12} Q0 ${sh[1] + 30} 30 ${sh[1] + 12}`} stroke="#3a2a1a" strokeWidth={2} fill="none" /></g>}
      {style === "vest" && <><path d={`M-40 ${sh[1] + 4} Q-30 ${sh[1] - 10} -12 ${sh[1] - 4} L-6 ${bot - 2} L-38 ${bot} Z`} fill={look.vest ?? "#2f8a4e"} /><path d={`M40 ${sh[1] + 4} Q30 ${sh[1] - 10} 12 ${sh[1] - 4} L6 ${bot - 2} L38 ${bot} Z`} fill={look.vest ?? "#2f8a4e"} /><rect x={14} y={sh[1] + 34} width={22} height={10} rx={2} fill="#f4f1e8" /></>}
      {style === "scrubs" && <><path d={`M-16 ${sh[1] - 8} L0 ${sh[1] + 22} L16 ${sh[1] - 8}`} stroke={shade(look.top, 0.6)} strokeWidth={5} fill={skin} strokeLinejoin="round" /><rect x={10} y={sh[1] + 40} width={22} height={20} rx={3} fill={shade(look.top, 0.85)} />{look.badge && <rect x={-34} y={sh[1] + 36} width={20} height={26} rx={3} fill="#f4f4f8" stroke="#3a6ad8" strokeWidth={3} />}</>}
      {style === "raincoat" && <><line x1={2} y1={sh[1] + 2} x2={2} y2={bot + 4} stroke={shade(look.top, 0.6)} strokeWidth={3} />{[0, 1, 2].map(i => <rect key={i} x={-4} y={sh[1] + 22 + i * 26} width={12} height={5} rx={2} fill={shade(look.top, 0.55)} />)}<path d={`M-40 ${bot - 4} L40 ${bot - 4}`} stroke={shade(look.top, 0.7)} strokeWidth={5} /></>}
      {style === "uniform" && <><rect x={-30} y={sh[1] + 24} width={22} height={18} rx={3} fill={shade(look.top, 0.8)} /><rect x={8} y={sh[1] + 24} width={22} height={18} rx={3} fill={shade(look.top, 0.8)} /><rect x={-42} y={hipY - 16} width={84} height={12} fill="#2a2620" /><rect x={-6} y={hipY - 17} width={12} height={14} fill="#a89a6a" /><path d={`M-24 ${sh[1] - 6} L0 ${sh[1] + 8} L24 ${sh[1] - 6}`} stroke={shade(look.top, 0.7)} strokeWidth={5} fill="none" /></>}
      {look.backpack && <><path d={`M-26 ${sh[1] - 6} Q-30 ${sh[1] + 40} -22 ${sh[1] + 96}`} stroke={shade(look.backpack, 0.7)} strokeWidth={8} fill="none" /><path d={`M26 ${sh[1] - 6} Q30 ${sh[1] + 40} 22 ${sh[1] + 96}`} stroke={shade(look.backpack, 0.7)} strokeWidth={8} fill="none" /></>}
      {Z && <path d={`M-40 ${bot} l10 -16 l8 14 l9 -20 l8 18 l10 -12 l9 14 l10 -18 l8 16 l8 -8`} stroke="#000" strokeOpacity={0.35} strokeWidth={4} fill="none" />}
      {style === "shirt" && look.tie && <path d={`M0 ${sh[1] - 4} L-6 ${sh[1] + 6} L0 ${sh[1] + 60} L6 ${sh[1] + 6} Z`} fill={look.tie} />}
    </>}
  </g>}</R>;

  // head — glossy sphere, features shifted to the facing side (3/4 view)
  const hc = [6, -362 + P.bob + br * 0.7], fx = 11, hr = 62;
  const eyeY = hc[1] - 2, eo = Math.max(0.06, P.eyes * (P.noBlink || Z ? 1 : life.blink));
  const mx = hc[0] + fx + 2, my = hc[1] + 30;
  const talkO = Math.max(0, Math.min(1, P.talk));
  const mouthD: Record<string, string> = {
    smile: `M${mx - 13} ${my - 2} Q${mx} ${my + 11} ${mx + 13} ${my - 2}`,
    smirk: `M${mx - 11} ${my + 1} Q${mx + 2} ${my + 5} ${mx + 13} ${my - 5}`,
    flat: `M${mx - 9} ${my} L${mx + 9} ${my}`,
    frown: `M${mx - 11} ${my + 5} Q${mx} ${my - 5} ${mx + 11} ${my + 5}`,
    sad: `M${mx - 10} ${my + 4} Q${mx} ${my - 2} ${mx + 10} ${my + 4}`,
    worried: `M${mx - 11} ${my + 3} Q${mx - 4} ${my - 3} ${mx} ${my + 1} Q${mx + 5} ${my + 4} ${mx + 11} ${my - 1}`,
  };
  const goldC = "#ffc94a";
  const hairC = look.hairColor ?? "#15131c", hatC = look.hatColor ?? "#e0a53a";
  const backHair = look.hair === "bun" ? <g><circle cx={hc[0] - 20} cy={hc[1] - 62} r={26} fill={hairC} /><circle cx={hc[0] - 26} cy={hc[1] - 70} r={9} fill="#fff" opacity={0.25} /></g>
    : look.hair === "ponytail" ? <path d={`M${hc[0] - 50} ${hc[1] - 40} Q${hc[0] - 100} ${hc[1] - 20} ${hc[0] - 92} ${hc[1] + 50} Q${hc[0] - 80} ${hc[1] + 10} ${hc[0] - 40} ${hc[1] - 10} Z`} fill={hairC} />
    : look.hair === "wild" ? <path d={`M${hc[0] - 70} ${hc[1] - 30} Q${hc[0] - 96} ${hc[1] + 40} ${hc[0] - 70} ${hc[1] + 96} Q${hc[0] - 40} ${hc[1] + 70} ${hc[0] - 30} ${hc[1] + 104} Q${hc[0]} ${hc[1] + 60} ${hc[0] + 20} ${hc[1] + 80} L${hc[0] + 40} ${hc[1] - 30} Z`} fill={hairC} />
    : look.hair === "braid" ? <g>{[0, 1, 2, 3, 4].map(i => <ellipse key={i} cx={hc[0] - 58 - i * 2} cy={hc[1] + 10 + i * 26} rx={13 - i} ry={16} fill={hairC} />)}<rect x={hc[0] - 72} y={hc[1] + 134} width={20} height={8} rx={3} fill="#c8402e" /></g>
    : look.hair === "hood" ? <ellipse cx={hc[0] - 4} cy={hc[1] + 2} rx={80} ry={82} fill={look.hatColor ?? "#8a6a4a"} />
    : look.hair === "pigtails" ? <g>{[-1, 1].map(k => <g key={k}><ellipse cx={hc[0] + k * 70} cy={hc[1] + 4} rx={18} ry={30} fill={hairC} transform={`rotate(${k * -18} ${hc[0] + k * 70} ${hc[1] + 4})`} /><circle cx={hc[0] + k * 60} cy={hc[1] - 22} r={7} fill="#ff5a8a" /></g>)}</g>
    : look.hair === "long" ? <path d={`M${hc[0] - 60} ${hc[1] - 10} Q${hc[0] - 74} ${hc[1] + 70} ${hc[0] - 40} ${hc[1] + 92} L${hc[0] + 30} ${hc[1] + 70} Z`} fill={hairC} /> : null;
  const headG = <g transform={`rotate(${P.head + life.sway} ${hc[0]} ${hc[1] + 44})`}>
    {style === "raincoat" && <path d={`M${hc[0] - 70} ${hc[1] + 50} Q${hc[0] - 92} ${hc[1] - 40} ${hc[0] - 30} ${hc[1] - 74} Q${hc[0] - 70} ${hc[1] + 10} ${hc[0] - 20} ${hc[1] + 70} Z`} fill={shade(look.top, 0.8)} />}
    {backHair}
    <R rim={rim}>{(c) => <circle cx={hc[0]} cy={hc[1]} r={hr} fill={c ?? `url(#${id}h)`} />}</R>
    {/* specular + bounce light */}
    <ellipse cx={hc[0] + 18} cy={hc[1] - 36} rx={20} ry={11} fill="#fff" opacity={0.22} transform={`rotate(-20 ${hc[0] + 18} ${hc[1] - 36})`} />
    <ellipse cx={hc[0] + 27} cy={hc[1] - 40} rx={6} ry={3.5} fill="#fff" opacity={0.55} />
    <path d={`M${hc[0] - 50} ${hc[1] + 30} Q${hc[0]} ${hc[1] + 70} ${hc[0] + 50} ${hc[1] + 30}`} stroke="#fff" strokeOpacity={0.08} strokeWidth={8} fill="none" />
    {look.hair === "short" && <path d={`M${hc[0] - 58} ${hc[1] - 18} Q${hc[0] - 50} ${hc[1] - 74} ${hc[0] + 6} ${hc[1] - 68} Q${hc[0] + 56} ${hc[1] - 66} ${hc[0] + 60} ${hc[1] - 22} Q${hc[0] + 30} ${hc[1] - 44} ${hc[0] - 6} ${hc[1] - 40} Q${hc[0] - 36} ${hc[1] - 38} ${hc[0] - 58} ${hc[1] - 18} Z`} fill={hairC} />}
    {(look.hair === "pigtails" || look.hair === "ponytail") && <path d={`M${hc[0] - 60} ${hc[1] - 12} Q${hc[0] - 56} ${hc[1] - 70} ${hc[0] + 4} ${hc[1] - 66} Q${hc[0] + 58} ${hc[1] - 62} ${hc[0] + 62} ${hc[1] - 14} Q${hc[0] + 36} ${hc[1] - 40} ${hc[0] + 12} ${hc[1] - 44} Q${hc[0] + 4} ${hc[1] - 30} ${hc[0] - 8} ${hc[1] - 44} Q${hc[0] - 40} ${hc[1] - 40} ${hc[0] - 60} ${hc[1] - 12} Z`} fill={hairC} />}
    {look.hair === "messy" && <path d={`M${hc[0] - 60} ${hc[1] - 10} L${hc[0] - 66} ${hc[1] - 44} L${hc[0] - 44} ${hc[1] - 52} L${hc[0] - 40} ${hc[1] - 78} L${hc[0] - 14} ${hc[1] - 66} L${hc[0] + 2} ${hc[1] - 88} L${hc[0] + 20} ${hc[1] - 66} L${hc[0] + 46} ${hc[1] - 80} L${hc[0] + 48} ${hc[1] - 54} L${hc[0] + 70} ${hc[1] - 46} L${hc[0] + 62} ${hc[1] - 18} Q${hc[0] + 40} ${hc[1] - 44} ${hc[0] + 14} ${hc[1] - 40} Q${hc[0] - 4} ${hc[1] - 30} ${hc[0] - 22} ${hc[1] - 42} Q${hc[0] - 46} ${hc[1] - 32} ${hc[0] - 60} ${hc[1] - 10} Z`} fill={hairC} />}
    {look.hair === "wild" && <path d={`M${hc[0] - 64} ${hc[1] - 6} Q${hc[0] - 76} ${hc[1] - 74} ${hc[0] - 10} ${hc[1] - 74} Q${hc[0] + 60} ${hc[1] - 80} ${hc[0] + 66} ${hc[1] - 16} L${hc[0] + 52} ${hc[1] - 34} L${hc[0] + 40} ${hc[1] - 22} L${hc[0] + 26} ${hc[1] - 44} L${hc[0] + 6} ${hc[1] - 30} L${hc[0] - 14} ${hc[1] - 48} L${hc[0] - 34} ${hc[1] - 28} L${hc[0] - 50} ${hc[1] - 40} Z`} fill={hairC} />}
    {look.hair === "braid" && <path d={`M${hc[0] - 62} ${hc[1] - 4} Q${hc[0] - 58} ${hc[1] - 70} ${hc[0] + 4} ${hc[1] - 66} Q${hc[0] + 58} ${hc[1] - 62} ${hc[0] + 62} ${hc[1] - 14} Q${hc[0] + 20} ${hc[1] - 50} ${hc[0] - 26} ${hc[1] - 36} Q${hc[0] - 48} ${hc[1] - 20} ${hc[0] - 62} ${hc[1] - 4} Z`} fill={hairC} />}
    {look.hair === "hood" && <g><path d={`M${hc[0] - 80} ${hc[1] + 10} Q${hc[0] - 78} ${hc[1] - 96} ${hc[0]} ${hc[1] - 96} Q${hc[0] + 78} ${hc[1] - 96} ${hc[0] + 80} ${hc[1] + 10} L${hc[0] + 62} ${hc[1] - 6} Q${hc[0] + 56} ${hc[1] - 62} ${hc[0]} ${hc[1] - 64} Q${hc[0] - 56} ${hc[1] - 62} ${hc[0] - 62} ${hc[1] - 6} Z`} fill={look.hatColor ?? "#8a6a4a"} />
      <path d={`M${hc[0] - 80} ${hc[1] + 10} ${Array.from({ length: 12 }, (_, i) => { const a = Math.PI * (1 - i / 11); return `L${hc[0] + Math.cos(a) * (84 + (i % 2) * 10)} ${hc[1] - Math.sin(a) * (90 + (i % 2) * 10)}`; }).join(" ")}`} stroke={look.furTrim ?? "#efe6d6"} strokeWidth={9} fill="none" strokeLinejoin="round" /></g>}
    {look.paint && <><path d={`M${hc[0] + fx - 40} ${hc[1] + 14} l14 4 M${hc[0] + fx - 40} ${hc[1] + 24} l14 2`} stroke="#c8582a" strokeWidth={5} strokeLinecap="round" /><path d={`M${hc[0] + fx + 30} ${hc[1] + 16} l14 -4 M${hc[0] + fx + 30} ${hc[1] + 26} l14 -2`} stroke="#c8582a" strokeWidth={5} strokeLinecap="round" /></>}
    {look.scar && <path d={`M${hc[0] + fx + 30} ${hc[1] - 8} l12 26`} stroke="#8a5a5a" strokeWidth={4} strokeLinecap="round" />}
    {look.hair === "cowboy" && <g><ellipse cx={hc[0]} cy={hc[1] - 44} rx={104} ry={18} fill={shade(hatC, 0.8)} /><path d={`M${hc[0] - 52} ${hc[1] - 46} Q${hc[0] - 50} ${hc[1] - 112} ${hc[0] - 14} ${hc[1] - 104} Q${hc[0]} ${hc[1] - 92} ${hc[0] + 14} ${hc[1] - 104} Q${hc[0] + 50} ${hc[1] - 112} ${hc[0] + 52} ${hc[1] - 46} Z`} fill={hatC} /><rect x={hc[0] - 52} y={hc[1] - 62} width={104} height={12} fill={shade(hatC, 0.5)} /></g>}
    {look.hair === "helmet" && <g><path d={`M${hc[0] - 70} ${hc[1] - 12} Q${hc[0] - 68} ${hc[1] - 100} ${hc[0] + 4} ${hc[1] - 100} Q${hc[0] + 72} ${hc[1] - 98} ${hc[0] + 72} ${hc[1] - 12} Z`} fill={hatC} /><path d={`M${hc[0] - 76} ${hc[1] - 14} L${hc[0] + 78} ${hc[1] - 14}`} stroke={shade(hatC, 0.7)} strokeWidth={9} strokeLinecap="round" /><path d={`M${hc[0] - 40} ${hc[1] - 80} Q${hc[0]} ${hc[1] - 96} ${hc[0] + 40} ${hc[1] - 80}`} stroke="#fff" strokeOpacity={0.15} strokeWidth={6} fill="none" /></g>}
    {look.hair === "curly" && [[-44, -40], [-22, -58], [4, -64], [30, -58], [50, -40], [-54, -16]].map(([dx, dy], i) => <circle key={i} cx={hc[0] + dx} cy={hc[1] + dy} r={18} fill={hairC} />)}
    {look.hair === "bun" && <path d={`M${hc[0] - 60} ${hc[1] - 6} Q${hc[0] - 56} ${hc[1] - 66} ${hc[0] + 4} ${hc[1] - 64} Q${hc[0] + 58} ${hc[1] - 60} ${hc[0] + 62} ${hc[1] - 10} Q${hc[0] + 30} ${hc[1] - 46} ${hc[0] - 10} ${hc[1] - 44} Q${hc[0] - 40} ${hc[1] - 40} ${hc[0] - 60} ${hc[1] - 6} Z`} fill={hairC} />}
    {look.hair === "long" && <path d={`M${hc[0] - 62} ${hc[1] + 4} Q${hc[0] - 60} ${hc[1] - 70} ${hc[0] + 6} ${hc[1] - 66} Q${hc[0] + 60} ${hc[1] - 64} ${hc[0] + 62} ${hc[1] - 14} Q${hc[0] + 20} ${hc[1] - 50} ${hc[0] - 30} ${hc[1] - 30} Q${hc[0] - 46} ${hc[1] - 12} ${hc[0] - 62} ${hc[1] + 4} Z`} fill={hairC} />}
    {look.hair === "beanie" && <g><path d={`M${hc[0] - 64} ${hc[1] - 18} Q${hc[0] - 62} ${hc[1] - 96} ${hc[0] + 2} ${hc[1] - 94} Q${hc[0] + 64} ${hc[1] - 92} ${hc[0] + 66} ${hc[1] - 18} Z`} fill={hatC} />
      {[-40, -20, 0, 20, 40].map(dx => <line key={dx} x1={hc[0] + dx} y1={hc[1] - 30} x2={hc[0] + dx * 0.7} y2={hc[1] - 86} stroke={shade(hatC, 0.8)} strokeWidth={3} />)}
      <rect x={hc[0] - 68} y={hc[1] - 36} width={136} height={24} rx={11} fill={shade(hatC, 0.85)} /><rect x={hc[0] - 66} y={hc[1] - 34} width={132} height={6} rx={3} fill="#fff" opacity={0.18} /></g>}
    {look.hair === "cap" && <g><path d={`M${hc[0] - 62} ${hc[1] - 20} Q${hc[0] - 58} ${hc[1] - 84} ${hc[0] + 4} ${hc[1] - 82} Q${hc[0] + 62} ${hc[1] - 80} ${hc[0] + 64} ${hc[1] - 20} Z`} fill={hatC} /><path d={`M${hc[0] + 30} ${hc[1] - 24} Q${hc[0] + 80} ${hc[1] - 30} ${hc[0] + 100} ${hc[1] - 14} L${hc[0] + 40} ${hc[1] - 12} Z`} fill={shade(hatC, 0.8)} /></g>}
    {/* eyes */}
    {[-1, 1].map(k => { const ex = hc[0] + fx + k * 22 - (k < 0 ? 3 : 0), rx = 15, ry = 19 * eo;
      const px = ex + P.look[0] * 5.5, py = eyeY + P.look[1] * 6;
      return <g key={k}>
        <ellipse cx={ex} cy={eyeY} rx={rx} ry={ry} fill="#f6f3ec" />
        <ellipse cx={ex} cy={eyeY + ry * 0.45} rx={rx * 0.9} ry={ry * 0.4} fill="#c9c3d6" opacity={0.35} />
        {Z && <><ellipse cx={ex} cy={eyeY + 3} rx={rx + 7} ry={19 + 6} fill="#1e2a1e" opacity={0.5} /><circle cx={ex} cy={eyeY} r={22} fill="#c8ffb0" opacity={0.18} /><ellipse cx={ex} cy={eyeY} rx={rx} ry={ry} fill="#e4ffd4" /><circle cx={px} cy={py} r={5} fill="#9ad88a" opacity={0.8} /></>}
        {!Z && eo > 0.3 && <>
          {P.gold > 0 && <circle cx={px} cy={py} r={13 * P.gold} fill={goldC} opacity={0.35 * P.gold} />}
          <circle cx={px} cy={py} r={8.6} fill={P.gold > 0 ? `url(#${id}g)` : "#0d0c12"} />
          <circle cx={px} cy={py} r={4.2} fill="#07060a" opacity={P.gold > 0 ? 0.9 : 0} />
          <circle cx={px + 3} cy={py - 3.5} r={2.8} fill="#fff" />
          <circle cx={px - 2.5} cy={py + 3} r={1.2} fill="#fff" opacity={0.7} />
        </>}
        {eo <= 0.3 && <path d={`M${ex - rx} ${eyeY} Q${ex} ${eyeY + 5} ${ex + rx} ${eyeY}`} stroke="#0d0c12" strokeWidth={3.5} fill="none" strokeLinecap="round" />}
        {look.lashes && eo > 0.3 && <path d={`M${ex + k * 11} ${eyeY - ry * 0.75} l${k * 7} -5`} stroke="#0d0c12" strokeWidth={3.5} strokeLinecap="round" />}
        <path d={`M${ex - 12} ${eyeY - 28 - k * P.brow * 5 + (k > 0 ? P.browIn : -P.browIn) * 0} Q${ex} ${eyeY - 33 - Math.abs(P.brow) * 2 + P.browIn * 4} ${ex + 12} ${eyeY - 28 + k * P.brow * 5}`}
          stroke="#0b0a10" strokeWidth={6.5} strokeLinecap="round" fill="none" transform={`rotate(${k * P.browIn * 12} ${ex} ${eyeY - 30})`} />
        {P.tears > 0 && <path d={`M${ex + 4} ${eyeY + 16} q3 ${10 + 20 * P.tears} 0 ${14 + 26 * P.tears}`} stroke="#9fd4ff" strokeWidth={4} strokeLinecap="round" opacity={0.85} />}
      </g>; })}
    {look.blush && <><ellipse cx={hc[0] + fx - 30} cy={hc[1] + 20} rx={10} ry={6} fill="#ff7a8a" opacity={0.35} /><ellipse cx={hc[0] + fx + 36} cy={hc[1] + 20} rx={10} ry={6} fill="#ff7a8a" opacity={0.35} /></>}
    {look.glasses && [-1, 1].map(k => <circle key={k} cx={hc[0] + fx + k * 22 - (k < 0 ? 3 : 0)} cy={eyeY} r={20} stroke="#d9d2c0" strokeWidth={3.5} fill="#fff" fillOpacity={0.06} />)}
    {look.glasses && <line x1={hc[0] + fx - 6} y1={eyeY - 2} x2={hc[0] + fx + 2} y2={eyeY - 2} stroke="#d9d2c0" strokeWidth={3} />}
    {look.beard && <path d={`M${hc[0] - 44} ${hc[1] + 10} Q${hc[0] - 40} ${hc[1] + 70} ${hc[0] + fx} ${hc[1] + 84} Q${hc[0] + 60} ${hc[1] + 70} ${hc[0] + 60} ${hc[1] + 10} Q${hc[0] + 46} ${hc[1] + 40} ${hc[0] + fx + 16} ${hc[1] + 44} L${hc[0] + fx - 12} ${hc[1] + 44} Q${hc[0] - 30} ${hc[1] + 40} ${hc[0] - 44} ${hc[1] + 10} Z`} fill={LIGHT ? (look.hairColor ?? "#2a1a10") : "#0e0d14"} opacity={LIGHT ? 1 : 0.7} />}
    {look.mustache && <path d={`M${mx - 20} ${my - 6} Q${mx - 10} ${my - 18} ${mx} ${my - 10} Q${mx + 10} ${my - 18} ${mx + 20} ${my - 6} Q${mx + 10} ${my - 9} ${mx} ${my - 5} Q${mx - 10} ${my - 9} ${mx - 20} ${my - 6} Z`} fill={look.hairColor ?? "#8a8a90"} />}
    {/* mouth: lip-sync overrides the expression while talking */}
    {talkO > 0.06 || P.mouth === "open" || P.mouth === "shout" || P.mouth === "o"
      ? (() => { const o = P.mouth === "shout" ? 1 : P.mouth === "o" ? 0.6 : P.mouth === "open" ? 0.7 : talkO; const w = P.mouth === "o" ? 7 : 8 + 6 * o, hgt = 3 + 15 * o;
        return <g><ellipse cx={mx} cy={my + hgt * 0.35} rx={Z ? w * 1.3 : w} ry={hgt * 0.6 + 1.5} fill="#120d14" /><ellipse cx={mx} cy={my + hgt * 0.62} rx={w * 0.6} ry={hgt * 0.22} fill={Z ? "#6a2a3a" : "#d4626e"} opacity={o > 0.3 ? 0.8 : 0} />{Z && [-1, -0.33, 0.33, 1].map((k, i) => <path key={i} d={`M${mx + k * w * 0.9 - 3} ${my + hgt * 0.35 - hgt * 0.6} l3 ${4 + o * 3} l3 ${-4 - o * 3} Z`} fill="#e8e4c8" />)}</g>; })()
      : <path d={mouthD[P.mouth] ?? mouthD.flat} stroke={lineC} strokeWidth={4.2} fill={P.mouth === "grin" ? "#120d14" : "none"} strokeLinecap="round" />}
    {P.mouth === "grin" && talkO <= 0.06 && <path d={`M${mx - 15} ${my - 8} Q${mx} ${my + 14} ${mx + 15} ${my - 8} Z`} fill="#120d14" stroke={lineC} strokeWidth={3} />}
    {look.earring && <path d={`M${hc[0] - 44} ${hc[1] + 30} l3 7 7 1 -5 5 1 7 -6 -3 -6 3 1 -7 -5 -5 7 -1 Z`} fill={look.earring} />}
  </g>;
  const upper = <g transform={`rotate(${P.lean} 0 ${hipY})`}>{arm(shL, P.aL, true)}{torso}{headG}{arm(shR, P.aR, false)}</g>;
  return <g transform={`translate(${x} ${y}) rotate(${rot}) scale(${s * (look.scale ?? 1) * P.facing} ${s * (look.scale ?? 1)})`} opacity={opacity}>
    <defs>
      <radialGradient id={`${id}h`} cx="0.62" cy="0.3" r="0.85"><stop offset="0" stopColor={shade(skin, LIGHT ? 1.12 : 2.1)} /><stop offset="0.45" stopColor={skin} /><stop offset="1" stopColor={shade(skin, LIGHT ? 0.78 : 0.55)} /></radialGradient>
      <linearGradient id={`${id}t`} x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={shade(look.top, 1.15)} /><stop offset="1" stopColor={shade(look.top, 0.82)} /></linearGradient>
      <radialGradient id={`${id}m`} cx="0.6" cy="0.3" r="0.8"><stop offset="0" stopColor={shade(mitt, LIGHT ? 1.12 : 2.0)} /><stop offset="1" stopColor={shade(mitt, 0.7)} /></radialGradient>
      <radialGradient id={`${id}g`}><stop offset="0" stopColor="#fff6cf" /><stop offset="0.5" stopColor={goldC} /><stop offset="1" stopColor="#b8780e" /></radialGradient>
    </defs>
    {/* contact shadow */}
    <ellipse cx={4} cy={6} rx={56} ry={10} fill="#000" opacity={0.28} />
    {leg(hipL, P.lL, true)}{leg(hipR, P.lR, false)}{upper}
  </g>;
};
export const runPose = (ph: number, amp = 1): Pose => { const s = Math.sin(ph), c = Math.cos(ph);
  return { lean: 10 * amp, aL: [-50 * s * amp, 80], aR: [50 * s * amp, 80], lL: [40 * s * amp, 20 + 60 * Math.max(0, -c) * amp], lR: [-40 * s * amp, 20 + 60 * Math.max(0, c) * amp], bob: -Math.abs(c) * 10 * amp }; };
export const walkPose = (ph: number, amp = 1): Pose => { const s = Math.sin(ph), c = Math.cos(ph);
  return { lean: 3, aL: [-22 * s * amp, 14], aR: [22 * s * amp, 14], lL: [24 * s * amp, 6 + 22 * Math.max(0, -c) * amp], lR: [-24 * s * amp, 6 + 22 * Math.max(0, c) * amp], bob: -Math.abs(c) * 4 * amp }; };
// seated on a chair with feet on the floor at the root: thighs horizontal, shins down, hips lowered by bob 82.
// → seat top at rootY − 86·s, head centre at rootY − 280·s. Put the chair BEHIND the character (draw it first).
export const SIT: Pose = { bob: 82, lL: [90, 90], lR: [84, 84] };
export const SIT_Y = 86, SIT_HEAD = 280;

// ---- poses solved with 2-bone IK (upper arm 78, forearm 70; angle 0 = straight down, 90 = forward) ----
export const ik = (sx: number, sy: number, tx: number, ty: number, elbowUp = false): number[] => {
  const dx = tx - sx, dy = ty - sy, L = Math.min(147.9, Math.max(9, Math.hypot(dx, dy)));
  const dir = Math.atan2(dx, dy) * 180 / Math.PI, a = Math.acos((78 * 78 + L * L - 70 * 70) / (2 * 78 * L)) * 180 / Math.PI;
  const a0 = elbowUp ? dir + a : dir - a; const ex = sx + 78 * Math.sin(a0 * Math.PI / 180), ey = sy + 78 * Math.cos(a0 * Math.PI / 180);
  return [a0, Math.atan2(tx - ex, ty - ey) * 180 / Math.PI - a0];
};
// rifle aimed level from the shoulder: front hand on the fore-grip, back hand on the trigger (hold: "aim")
export const AIM: Pose = { hold: "aim", aR: ik(27, -284, 112, -290), aL: ik(-27, -284, 50, -284), head: 4, look: [1, 0], brow: -0.4, browIn: 0.8 };
// hands on top of the head (ducking / covering)
export const COVER: Pose = { aR: ik(27, -284, 30, -410, true), aL: ik(-27, -284, -20, -405, true) };
// muzzle of the aimed rifle in world space for a character at (x, y), scale s (incl. look.scale), facing ±1
export const muzzle = (x: number, y: number, s: number, facing = 1) => [x + 210 * s * facing, y - 296 * s];
// rifle carried diagonally across the chest (port arms): rifle line rotated −45° about (15, −250); the muzzle end
// stays right of the head (it crossed the face at −62°)
const rp = (d: number) => { const a = -45 * Math.PI / 180; return [15 + d * Math.cos(a), -250 + d * Math.sin(a)]; };
const [px1, py1] = rp(85), [px2, py2] = rp(-50);
export const PORT: Pose = { hold: "port", aR: ik(27, -284, px1, py1, false), aL: ik(-27, -284, px2, py2, false) };
