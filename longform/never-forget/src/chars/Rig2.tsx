// Character rig v2 (our own design). Same skeleton as hearing-100x Rig (root between the feet, hips 168 up, head
// centre 362 up, head r 60) so all camera maths carries over. New: glossy soft-shaded head with specular highlight,
// mitten hands, shaded clothes with styles (jacket / hoodie / coat / cardigan / suit), hats and hair, blink +
// breathing (idle), lip-sync (talk 0..1), gold "memory" irises, blush, earring, glasses, tie, props in hand.
import React from "react";
import { rnd } from "../engine/core";

export type Look = {
  skin?: string; top: string; topDark?: string; pants: string; shoes?: string; mitt?: string;
  style?: "jacket" | "hoodie" | "coat" | "cardigan" | "suit" | "shirt" | "labcoat";
  hair?: "beanie" | "bun" | "short" | "curly" | "bald" | "cap" | "long" | "none"; hairColor?: string; hatColor?: string;
  glasses?: boolean; earring?: string; tie?: string; blush?: boolean; scale?: number; lashes?: boolean; beard?: boolean;
};
export type Pose = {
  lean?: number; head?: number; aL?: number[]; aR?: number[]; lL?: number[]; lR?: number[];
  eyes?: number; look?: number[]; brow?: number; browIn?: number;
  mouth?: "smile" | "grin" | "o" | "flat" | "open" | "frown" | "shout" | "worried" | "smirk" | "sad";
  talk?: number; bob?: number; facing?: 1 | -1; gold?: number; tears?: number; breath?: number; hold?: "cup" | "phone" | "photo" | "cards" | "pills" | null; noBlink?: boolean;
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
  const skin = look.skin ?? "#24212f", dark = look.topDark ?? shade(look.top, 0.68), shoes = look.shoes ?? "#17161d", mitt = look.mitt ?? skin;
  const br = life.breath * P.breath;
  const hipY = -168 + P.bob, hipL = [-13, hipY], hipR = [13, hipY];
  const sh = [0, -292 + P.bob + br * 0.5], shL = [-27, sh[1] + 8], shR = [27, sh[1] + 8];
  const style = look.style ?? "jacket";
  const longCoat = style === "coat" || style === "labcoat";

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
    if (P.hold === "cup") return <g transform={t}><path d="M-12 -30 L12 -30 L9 4 L-9 4 Z" fill="#f2efe6" /><rect x={-13} y={-34} width={26} height={6} rx={2} fill="#3a3530" /><rect x={-11} y={-20} width={22} height={9} fill="#b0623a" /></g>;
    if (P.hold === "phone") return <g transform={t}><rect x={-12} y={-34} width={24} height={44} rx={5} fill="#16151c" /><rect x={-10} y={-31} width={20} height={36} rx={3} fill="#7fd0ff" opacity={0.9} /></g>;
    if (P.hold === "photo") return <g transform={t}><rect x={-26} y={-40} width={52} height={40} fill="#f4f1e8" /><rect x={-22} y={-36} width={44} height={28} fill="#59606e" /></g>;
    if (P.hold === "cards") return <g transform={t}>{[0, 1, 2, 3].map(i => <rect key={i} x={-12 + i * 5} y={-36} width={24} height={34} rx={3} fill="#fbf8f0" stroke="#c9302c" strokeWidth={1.5} transform={`rotate(${-18 + i * 12} 0 -2)`} />)}</g>;
    if (P.hold === "pills") return <g transform={t}><rect x={-10} y={-34} width={20} height={30} rx={4} fill="#e8a33a" opacity={0.9} /><rect x={-11} y={-40} width={22} height={9} rx={2} fill="#f4f4f4" /></g>;
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
      {!c && !back && prop(h, a[0] + a[1])}
    </g>}</R>;
  };
  const bot = longCoat ? hipY + 74 : hipY + 14;
  const torso = <R rim={rim}>{(c) => <g>
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
      {style === "shirt" && look.tie && <path d={`M0 ${sh[1] - 4} L-6 ${sh[1] + 6} L0 ${sh[1] + 60} L6 ${sh[1] + 6} Z`} fill={look.tie} />}
    </>}
  </g>}</R>;

  // head — glossy sphere, features shifted to the facing side (3/4 view)
  const hc = [6, -362 + P.bob + br * 0.7], fx = 11, hr = 62;
  const eyeY = hc[1] - 2, eo = Math.max(0.06, P.eyes * (P.noBlink ? 1 : life.blink));
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
    : look.hair === "long" ? <path d={`M${hc[0] - 60} ${hc[1] - 10} Q${hc[0] - 74} ${hc[1] + 70} ${hc[0] - 40} ${hc[1] + 92} L${hc[0] + 30} ${hc[1] + 70} Z`} fill={hairC} /> : null;
  const headG = <g transform={`rotate(${P.head + life.sway} ${hc[0]} ${hc[1] + 44})`}>
    {backHair}
    <R rim={rim}>{(c) => <circle cx={hc[0]} cy={hc[1]} r={hr} fill={c ?? `url(#${id}h)`} />}</R>
    {/* specular + bounce light */}
    <ellipse cx={hc[0] + 18} cy={hc[1] - 36} rx={20} ry={11} fill="#fff" opacity={0.22} transform={`rotate(-20 ${hc[0] + 18} ${hc[1] - 36})`} />
    <ellipse cx={hc[0] + 27} cy={hc[1] - 40} rx={6} ry={3.5} fill="#fff" opacity={0.55} />
    <path d={`M${hc[0] - 50} ${hc[1] + 30} Q${hc[0]} ${hc[1] + 70} ${hc[0] + 50} ${hc[1] + 30}`} stroke="#fff" strokeOpacity={0.08} strokeWidth={8} fill="none" />
    {look.hair === "short" && <path d={`M${hc[0] - 58} ${hc[1] - 18} Q${hc[0] - 50} ${hc[1] - 74} ${hc[0] + 6} ${hc[1] - 68} Q${hc[0] + 56} ${hc[1] - 66} ${hc[0] + 60} ${hc[1] - 22} Q${hc[0] + 30} ${hc[1] - 44} ${hc[0] - 6} ${hc[1] - 40} Q${hc[0] - 36} ${hc[1] - 38} ${hc[0] - 58} ${hc[1] - 18} Z`} fill={hairC} />}
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
        {eo > 0.3 && <>
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
    {look.beard && <path d={`M${hc[0] - 40} ${hc[1] + 22} Q${hc[0] + fx} ${hc[1] + 80} ${hc[0] + 56} ${hc[1] + 22} Q${hc[0] + fx} ${hc[1] + 52} ${hc[0] - 40} ${hc[1] + 22} Z`} fill="#0e0d14" opacity={0.7} />}
    {/* mouth: lip-sync overrides the expression while talking */}
    {talkO > 0.06 || P.mouth === "open" || P.mouth === "shout" || P.mouth === "o"
      ? (() => { const o = P.mouth === "shout" ? 1 : P.mouth === "o" ? 0.6 : P.mouth === "open" ? 0.7 : talkO; const w = P.mouth === "o" ? 7 : 8 + 6 * o, hgt = 3 + 15 * o;
        return <g><ellipse cx={mx} cy={my + hgt * 0.35} rx={w} ry={hgt * 0.6 + 1.5} fill="#120d14" /><ellipse cx={mx} cy={my + hgt * 0.62} rx={w * 0.6} ry={hgt * 0.22} fill="#d4626e" opacity={o > 0.3 ? 0.8 : 0} /></g>; })()
      : <path d={mouthD[P.mouth] ?? mouthD.flat} stroke="#f4f1ea" strokeWidth={4.2} fill={P.mouth === "grin" ? "#120d14" : "none"} strokeLinecap="round" />}
    {P.mouth === "grin" && talkO <= 0.06 && <path d={`M${mx - 15} ${my - 8} Q${mx} ${my + 14} ${mx + 15} ${my - 8} Z`} fill="#120d14" stroke="#f4f1ea" strokeWidth={3} />}
    {look.earring && <path d={`M${hc[0] - 44} ${hc[1] + 30} l3 7 7 1 -5 5 1 7 -6 -3 -6 3 1 -7 -5 -5 7 -1 Z`} fill={look.earring} />}
  </g>;
  const upper = <g transform={`rotate(${P.lean} 0 ${hipY})`}>{arm(shL, P.aL, true)}{torso}{headG}{arm(shR, P.aR, false)}</g>;
  return <g transform={`translate(${x} ${y}) rotate(${rot}) scale(${s * (look.scale ?? 1) * P.facing} ${s * (look.scale ?? 1)})`} opacity={opacity}>
    <defs>
      <radialGradient id={`${id}h`} cx="0.62" cy="0.3" r="0.85"><stop offset="0" stopColor={shade(skin, 2.1)} /><stop offset="0.45" stopColor={skin} /><stop offset="1" stopColor={shade(skin, 0.55)} /></radialGradient>
      <linearGradient id={`${id}t`} x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={shade(look.top, 1.15)} /><stop offset="1" stopColor={shade(look.top, 0.82)} /></linearGradient>
      <radialGradient id={`${id}m`} cx="0.6" cy="0.3" r="0.8"><stop offset="0" stopColor={shade(mitt, 2.0)} /><stop offset="1" stopColor={shade(mitt, 0.7)} /></radialGradient>
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
