// Ice Age animals, side views facing RIGHT, origin = ground under the middle of the body. `ph` = walk phase (radians),
// legs swing in diagonal pairs. Shaggy hair is drawn as zig-zag fringes. Original designs, no gore.
import React from "react";
import { shade } from "../chars/Rig2";

const leg = (x: number, top: number, len: number, w: number, a: number, c: string, hoof = "#2a1e16") => {
  const r = (a * Math.PI) / 180, fx = x + Math.sin(r) * len, fy = top + Math.cos(r) * len;
  return <g key={x}><path d={`M${x} ${top} L${fx} ${fy}`} stroke={c} strokeWidth={w} strokeLinecap="round" /><ellipse cx={fx} cy={fy - 2} rx={w * 0.55} ry={w * 0.25} fill={hoof} /></g>;
};
const fringe = (x0: number, x1: number, y: number, depth: number, c: string, n = 14) =>
  <path d={`M${x0} ${y} ${Array.from({ length: n }, (_, i) => { const x = x0 + ((i + 0.5) / n) * (x1 - x0), x2 = x0 + ((i + 1) / n) * (x1 - x0); return `L${x} ${y + depth * (0.7 + 0.3 * Math.sin(i * 2.3))} L${x2} ${y}`; }).join(" ")} Z`} fill={c} />;

export const Mammoth: React.FC<{ ph?: number; trunk?: number; s?: number; eye?: number; dark?: number; trumpet?: number; angry?: number; rim?: string }> = ({ ph = 0, trunk = 0, s = 1, eye = 1, dark = 0, trumpet = 0, angry = 0, rim }) => {
  const c = "#6a3e26", d = shade(c, 0.7), l = shade(c, 1.25), sw = Math.sin(ph) * 14;
  return <g transform={`scale(${s})`}>
    <ellipse cx={0} cy={4} rx={330} ry={26} fill="#000" opacity={0.3} />
    {leg(-170, -230, 230, 74, -sw, d)}{leg(150, -230, 230, 74, sw, d)}
    <path d="M-290 -260 Q-310 -420 -170 -470 Q-40 -560 120 -520 Q220 -500 250 -420 Q290 -330 240 -210 L-250 -200 Q-300 -220 -290 -260 Z" fill={c} />
    <path d="M-290 -260 Q-300 -380 -200 -440 Q-120 -480 -60 -470 Q-180 -420 -230 -300 Z" fill={l} opacity={0.35} />
    {fringe(-280, 250, -230, 70, d, 18)}
    {Array.from({ length: 14 }, (_, i) => <path key={i} d={`M${-250 + i * 34} ${-420 + Math.abs(i - 7) * 12} q8 40 -4 80`} stroke={l} strokeWidth={4} opacity={0.35} fill="none" />)}
    {/* head dome + trunk */}
    <path d="M150 -500 Q210 -600 300 -560 Q370 -520 360 -420 Q350 -340 300 -300 L200 -320 Z" fill={c} />
    {trumpet > 0 ? <g><path d="M320 -380 Q420 -420 470 -520 Q500 -600 460 -660 L490 -670 Q540 -600 500 -500 Q450 -390 340 -330 Z" fill={c} />{[0, 1, 2, 3, 4].map(i => <line key={i} x1={360 + i * 26} y1={-400 - i * 50} x2={380 + i * 26} y2={-390 - i * 50} stroke={d} strokeWidth={4} />)}<ellipse cx={476} cy={-668} rx={18} ry={10} fill="#2a1408" />
      <path d="M300 -330 Q330 -290 360 -300 Q340 -320 320 -340 Z" fill="#5a1a1a" /></g> : <>
    <path d={`M330 -360 Q${380 + trunk * 20} -260 ${360 + trunk * 30} -150 Q${350 + trunk * 40} -60 ${310 + trunk * 50} -40 L${300 + trunk * 50} -60 Q${330 + trunk * 30} -110 ${325 + trunk * 20} -170 Q320 -260 290 -320 Z`} fill={c} />
    {[0, 1, 2, 3, 4].map(i => <line key={i} x1={332 + trunk * (10 + i * 6)} y1={-300 + i * 50} x2={352 + trunk * (14 + i * 6)} y2={-296 + i * 50} stroke={d} strokeWidth={4} />)}</>}
    {/* tusk */}
    <path d="M320 -320 Q440 -250 420 -120 Q410 -80 380 -70 Q400 -140 360 -230 Q330 -280 300 -300 Z" fill="#f2ead6" stroke="#c8bca4" strokeWidth={4} />
    <path d="M200 -470 Q230 -420 210 -360 Q180 -390 190 -460 Z" fill={d} />
    {angry > 0 && <><ellipse cx={305} cy={-438} rx={20 * eye} ry={15 * eye} fill="#ffe2c8" /><circle cx={312} cy={-436} r={10 * eye} fill="#8a1a0a" opacity={angry} /><circle cx={312} cy={-436} r={6.5 * eye} fill="#1a0e08" /><circle cx={315} cy={-440} r={2.6} fill="#fff" />
      <path d={`M272 ${-466 - 10 * angry} L${300} ${-458 - 2 * angry} L336 ${-446 + 6 * angry} L334 ${-438 + 6 * angry} L300 ${-448} L272 ${-458 - 8 * angry} Z`} fill={d} />
      <path d={`M272 ${-466 - 10 * angry} L336 ${-446 + 6 * angry}`} stroke="#2a1408" strokeWidth={10} strokeLinecap="round" />
      {trumpet > 0 && <path d="M330 -350 Q360 -320 400 -336 Q380 -300 336 -310 Z" fill="#5a1a14" />}</>}
    {!angry && <><circle cx={305} cy={-440} r={11 * eye} fill="#1a0e08" /><circle cx={309} cy={-444} r={3.5} fill="#fff" opacity={0.8} /></>}
    {Array.from({ length: 26 }, (_, i) => <path key={`h${i}`} d={`M${-260 + (i % 13) * 38} ${-460 + Math.floor(i / 13) * 120 + Math.abs((i % 13) - 6) * 10} q${6 + (i % 3) * 4} 50 -6 ${100}`} stroke={d} strokeWidth={5} opacity={0.45} fill="none" strokeLinecap="round" />)}
    {rim && <path d="M-290 -260 Q-310 -420 -170 -470 Q-40 -560 120 -520 Q220 -500 250 -420" stroke={rim} strokeWidth={10} fill="none" opacity={0.85} strokeLinecap="round" />}
    {leg(-120, -230, 230, 78, sw, c)}{leg(210, -230, 230, 78, -sw, c)}
    {fringe(-150, -90, -60, 40, d, 4)}{fringe(180, 240, -60, 40, d, 4)}
    <path d="M-290 -330 Q-330 -300 -320 -240" stroke={d} strokeWidth={14} fill="none" strokeLinecap="round" />
    {dark > 0 && <path d="M-310 -560 L440 -560 L440 10 L-310 10 Z" fill="#0a1020" opacity={dark} />}
  </g>;
};

export const CaveLion: React.FC<{ ph?: number; s?: number; roar?: number }> = ({ ph = 0, s = 1, roar = 0 }) => {
  const c = "#c8964a", d = shade(c, 0.75), sw = Math.sin(ph) * 22;
  return <g transform={`scale(${s})`}>
    <ellipse cx={0} cy={4} rx={230} ry={18} fill="#000" opacity={0.3} />
    {leg(-150, -150, 150, 38, -sw, d, "#3a2a1a")}{leg(110, -150, 150, 38, sw, d, "#3a2a1a")}
    <path d="M-200 -170 Q-210 -250 -120 -260 L120 -270 Q200 -270 220 -210 Q230 -160 200 -130 L-180 -120 Q-210 -140 -200 -170 Z" fill={c} />
    {[0, 1, 2, 3].map(i => <path key={i} d={`M${-120 + i * 50} -255 q10 30 0 60`} stroke={d} strokeWidth={6} opacity={0.4} fill="none" />)}
    <path d="M-200 -200 Q-280 -220 -300 -150 Q-290 -120 -280 -150 Q-260 -200 -200 -180 Z" fill={c} /><circle cx={-298} cy={-148} r={12} fill="#5a3a1e" />
    {/* head */}
    <g transform={`translate(230 -240) rotate(${-roar * 10})`}>
      <ellipse cx={0} cy={0} rx={70} ry={58} fill={c} /><ellipse cx={46} cy={18} rx={40} ry={30} fill={shade(c, 1.12)} />
      <path d="M-40 -48 L-30 -78 L-10 -50 Z M10 -54 L24 -80 L36 -50 Z" fill={d} />
      <ellipse cx={24} cy={-14} rx={8} ry={6} fill="#ffd34a" /><ellipse cx={24} cy={-14} rx={3} ry={5.5} fill="#111" />
      <ellipse cx={80} cy={8} rx={10} ry={7} fill="#3a2418" />
      <path d={`M40 30 Q70 ${44 + roar * 30} 92 ${30 + roar * 10}`} stroke="#3a2418" strokeWidth={5} fill={roar > 0.2 ? "#5a1a1a" : "none"} />
      {roar > 0.2 && <path d={`M50 34 l4 10 l4 -10 M76 ${36 + roar * 10} l4 ${10} l4 -10`} fill="#fff" />}
    </g>
    {leg(-110, -150, 150, 40, sw, c, "#3a2a1a")}{leg(160, -150, 150, 40, -sw, c, "#3a2a1a")}
  </g>;
};

export const Wolf: React.FC<{ ph?: number; s?: number; howl?: number }> = ({ ph = 0, s = 1, howl = 0 }) => {
  const c = "#8a8e98", d = shade(c, 0.7), sw = Math.sin(ph) * 24;
  return <g transform={`scale(${s})`}>
    <ellipse cx={0} cy={4} rx={150} ry={12} fill="#000" opacity={0.3} />
    {leg(-90, -110, 110, 24, -sw, d, "#2a2a2e")}{leg(70, -110, 110, 24, sw, d, "#2a2a2e")}
    <path d="M-130 -120 Q-140 -180 -70 -190 L80 -200 Q140 -200 150 -150 L140 -100 L-120 -90 Z" fill={c} />
    {fringe(-120, 140, -100, 18, shade(c, 1.2), 10)}
    <path d="M-130 -150 Q-210 -140 -220 -100 Q-180 -120 -130 -120 Z" fill={c} />
    <g transform={`translate(150 -170) rotate(${-howl * 30})`}><path d="M-20 -30 Q20 -50 60 -20 L110 0 Q100 20 60 22 Q20 30 -20 20 Z" fill={c} /><path d="M0 -36 L10 -66 L26 -36 Z" fill={d} /><circle cx={40} cy={-12} r={5} fill="#ffd34a" /><circle cx={108} cy={2} r={7} fill="#222" /></g>
    {leg(-60, -110, 110, 26, sw, c, "#2a2a2e")}{leg(100, -110, 110, 26, -sw, c, "#2a2a2e")}
  </g>;
};

export const Reindeer: React.FC<{ ph?: number; s?: number; graze?: number }> = ({ ph = 0, s = 1, graze = 0 }) => {
  const c = "#7a5a3e", d = shade(c, 0.7), sw = Math.sin(ph) * 20;
  return <g transform={`scale(${s})`}>
    <ellipse cx={0} cy={4} rx={160} ry={12} fill="#000" opacity={0.3} />
    {leg(-100, -150, 150, 20, -sw, d)}{leg(80, -150, 150, 20, sw, d)}
    <path d="M-140 -160 Q-140 -230 -60 -230 L80 -240 Q140 -240 150 -180 L140 -140 L-120 -130 Z" fill={c} />
    <path d="M60 -240 Q110 -260 130 -200 L140 -150 Q100 -170 60 -200 Z" fill="#efe6d6" />
    <g transform={`translate(140 -250) rotate(${graze * 70})`}>
      <path d="M-10 0 L30 -40 L60 -30 L90 -10 Q100 10 80 16 L30 10 Z" fill={c} /><circle cx={50} cy={-18} r={5} fill="#111" />
      <path d="M20 -36 Q0 -100 -40 -120 M10 -70 L-30 -80 M30 -36 Q50 -110 90 -130 M44 -80 L80 -90 M58 -110 L60 -140" stroke="#d8c8a8" strokeWidth={8} fill="none" strokeLinecap="round" />
    </g>
    {leg(-70, -150, 150, 22, sw, c)}{leg(110, -150, 150, 22, -sw, c)}
  </g>;
};

export const Rhino: React.FC<{ ph?: number; s?: number }> = ({ ph = 0, s = 1 }) => {
  const c = "#7a5e44", d = shade(c, 0.72), sw = Math.sin(ph) * 12;
  return <g transform={`scale(${s})`}>
    <ellipse cx={0} cy={4} rx={260} ry={20} fill="#000" opacity={0.3} />
    {leg(-150, -150, 150, 56, -sw, d)}{leg(120, -150, 150, 56, sw, d)}
    <path d="M-230 -170 Q-240 -300 -100 -320 Q60 -350 180 -290 Q240 -250 250 -170 L-200 -140 Z" fill={c} />
    {fringe(-220, 240, -160, 44, d, 16)}
    <path d="M210 -270 Q300 -260 330 -180 L320 -150 L230 -160 Z" fill={c} />
    <path d="M300 -230 Q330 -330 360 -340 Q350 -290 330 -210 Z" fill="#e8dcc0" /><path d="M260 -260 Q270 -300 290 -305 Q290 -280 280 -250 Z" fill="#e8dcc0" />
    <circle cx={262} cy={-220} r={7} fill="#111" />
    {leg(-110, -150, 150, 58, sw, c)}{leg(160, -150, 150, 58, -sw, c)}
  </g>;
};

// a running herd, depth-sorted; kind per member
export const Herd: React.FC<{ f: number; x0: number; x1: number; y: number; n: number; s: number; kind: "mammoth" | "reindeer"; speed?: number; seed?: number; dir?: 1 | -1 }> = ({ f, x0, x1, y, n, s, kind, speed = 1, seed = 1, dir = 1 }) => <g>
  {Array.from({ length: n }, (_, i) => { const rx = ((i * 0.618 + seed * 0.13) % 1), x = x0 + rx * (x1 - x0) + f * speed * dir, yy = y + ((i * 37) % 5) * 14, sc = s * (0.85 + ((i * 53) % 7) / 30);
    return { yy, el: <g key={i} transform={`translate(${x} ${yy}) scale(${dir} 1)`}>{kind === "mammoth" ? <Mammoth ph={f * 0.08 * speed + i} s={sc} trunk={Math.sin(f * 0.05 + i)} /> : <Reindeer ph={f * 0.2 * speed + i} s={sc} />}</g> }; })
    .sort((a, b) => a.yy - b.yy).map(o => o.el)}
</g>;
