// Chapter 2 places: a football field at dusk, a house cross-section (three rooms), the ear close-up.
import React from "react";
import { Layer, W, H, rnd, lerp, sat } from "../engine/core";
import { Glow, Shaft, Bokeh } from "../engine/fx";
import { Noise, AO, Wallpaper, Wood } from "../engine/tex";
import { Character } from "../chars/Rig";
import { HERO, MIA } from "../chars/cast";

export const Field: React.FC<{ f: number; whisper: number }> = ({ f, whisper }) => {
  const g = 840;
  return <>
    <Layer depth={0.3}>
      <defs><linearGradient id="dusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#2a2a6a" /><stop offset="0.55" stopColor="#c86a7a" /><stop offset="1" stopColor="#ffb07a" /></linearGradient></defs>
      <rect x={-1500} y={-400} width={W + 3000} height={g + 400} fill="url(#dusk)" />
      <Glow x={1500} y={g - 40} r={500} color="#ffd08a" o={0.6} />
      {Array.from({ length: 30 }, (_, i) => <ellipse key={i} cx={-1400 + i * 180} cy={g - 20} rx={110 + rnd(i, 1) * 80} ry={60 + rnd(i, 2) * 60} fill="#2a1e3a" />)}
    </Layer>
    <Layer depth={0.6}>
      {[-600, 2500].map((x, k) => <g key={k}><line x1={x} y1={g} x2={x} y2={180} stroke="#14121e" strokeWidth={14} /><rect x={x - 70} y={140} width={140} height={60} fill="#14121e" />{Array.from({ length: 8 }, (_, i) => <circle key={i} cx={x - 55 + (i % 4) * 36} cy={158 + Math.floor(i / 4) * 24} r={9} fill="#fff6d8" />)}<Glow x={x} y={170} r={380} color="#fff2c8" o={0.5} /></g>)}
      <rect x={-1500} y={g - 120} width={W + 3000} height={40} fill="#1e1a2e" />{Array.from({ length: 60 }, (_, i) => <circle key={i} cx={-1450 + i * 90} cy={g - 125} r={14} fill="#2a2440" />)}
    </Layer>
    <Layer depth={1}>
      <rect x={-1500} y={g} width={W + 3000} height={600} fill="#2a6a3a" />
      {Array.from({ length: 22 }, (_, i) => <rect key={i} x={-1500 + i * 220} y={g} width={110} height={600} fill="#000" opacity={0.08} />)}
      <Noise x={-1500} y={g} w={W + 3000} h={600} freq={0.9} o={0.25} />
      <line x1={-1500} y1={g + 60} x2={W + 1500} y2={g + 60} stroke="#e8f0e0" strokeWidth={6} opacity={0.6} /><line x1={960} y1={g} x2={960} y2={g + 600} stroke="#e8f0e0" strokeWidth={6} opacity={0.6} />
      <g transform={`translate(${-1250} 0)`}><rect x={0} y={g - 260} width={10} height={260} fill="#f0f0f0" /><rect x={0} y={g - 260} width={300} height={10} fill="#f0f0f0" /><rect x={290} y={g - 260} width={10} height={260} fill="#f0f0f0" /></g>
      <Character look={MIA} pose={{ mouth: whisper > 0 && whisper < 0.6 ? (Math.floor(f / 3) % 2 ? "o" : "flat") : "smile", aR: [150, 30], hands: "open", look: [1, 0] }} x={-900} y={g + 40} rim={{ dx: 4, dy: -2, color: "#ffc28a" }} s={0.8} />
      <Character look={HERO} pose={{ mouth: whisper > 0.7 ? "grin" : "flat", look: [-1, 0], facing: -1, brow: whisper > 0.6 ? 0.8 : 0 }} x={2800} y={g + 40} rim={{ dx: -4, dy: -2, color: "#ffc28a" }} s={0.8} />
      {/* the whisper travelling across the field */}
      {whisper > 0 && <g>
        <path d={`M-860 ${g - 270} Q960 ${g - 520} 2760 ${g - 270}`} stroke="#9ef0ff" strokeWidth={5} fill="none" strokeDasharray="6 22" strokeDashoffset={-f * 4} opacity={0.9} pathLength={1000} style={{ filter: "drop-shadow(0 0 8px #5ae0ff)" }} />
        {(() => { const u = sat(whisper), x = lerp(-860, 2760, u), y = g - 270 - Math.sin(u * Math.PI) * 250; return <g><circle cx={x} cy={y} r={30} fill="#9ef0ff" opacity={0.3} /><text x={x} y={y - 46} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={44} fill="#e8faff" style={{ filter: "drop-shadow(0 0 8px #5ae0ff)" }}>psst… pizza?</text></g>; })()}
      </g>}
      <AO x={-1500} y={g} w={W + 3000} h={60} dir="down" o={0.3} />
    </Layer>
  </>;
};

// three rooms side by side, cut away; the hero covers his ears in room 1; a mosquito buzzes in room 3
export const House: React.FC<{ f: number }> = ({ f }) => {
  const rooms = [{ x: 0, wp: "#2a2a44", ink: "#4a4a70" }, { x: 640, wp: "#2e3a2e", ink: "#4a6a4a" }, { x: 1280, wp: "#3a2a2a", ink: "#6a4a4a" }];
  const mx = 1600 + Math.sin(f * 0.13) * 140, my = 430 + Math.sin(f * 0.21) * 70;
  return <>
    <Layer depth={0.5}><rect x={-400} y={-300} width={W + 800} height={H + 600} fill="#120f1c" /><Bokeh x={-300} y={0} w={2500} h={1000} n={30} seed={21} f={f} /></Layer>
    <Layer depth={1}>
      {rooms.map((r, i) => <g key={i}>
        <Wallpaper x={r.x + 20} y={160} w={600} h={600} base={r.wp} ink={r.ink} kind={i === 1 ? "stripe" : "diamond"} o={0.2} />
        <Wood x={r.x + 20} y={760} w={600} h={60} color="#2a1c18" rows={2} />
        <AO x={r.x + 20} y={160} w={600} h={80} dir="down" o={0.5} />
        <line x1={r.x + 320} y1={160} x2={r.x + 320} y2={230} stroke="#000" strokeWidth={3} /><path d={`M${r.x + 290} 230 L${r.x + 350} 230 L${r.x + 340} 252 L${r.x + 300} 252 Z`} fill="#e8d0a0" /><Glow x={r.x + 320} y={260} r={380} color="#ffd8a0" o={0.35} />
      </g>)}
      {/* walls, floors and roof of the cut-away */}
      {[0, 620, 1260, 1900].map(x => <rect key={x} x={x} y={140} width={22} height={700} fill="#0c0a14" />)}
      <rect x={0} y={140} width={1922} height={22} fill="#0c0a14" /><rect x={0} y={820} width={1922} height={40} fill="#0c0a14" />
      <path d="M-40 142 L960 -60 L1960 142 Z" fill="#1a1422" />
      {/* props: kitchen (fridge, table) and bathroom (tub) */}
      <rect x={700} y={520} width={120} height={240} rx={8} fill="#d8dce4" /><rect x={700} y={600} width={120} height={4} fill="#9aa0aa" />
      <rect x={900} y={640} width={200} height={14} fill="#5a3a2a" /><rect x={910} y={654} width={10} height={106} fill="#3a2418" /><rect x={1080} y={654} width={10} height={106} fill="#3a2418" />
      <path d="M1400 680 L1760 680 Q1760 760 1700 760 L1460 760 Q1400 760 1400 680 Z" fill="#e8ecf0" /><rect x={1730} y={600} width={10} height={80} fill="#aab" />
      <Character look={HERO} pose={{ mouth: "frown", brow: -0.8, eyes: 0.6, aL: [150, 110], aR: [150, 110], look: [1, 0] }} x={300} y={760} rim={{ dx: 3, dy: -3, color: "#ffd8a0" }} s={0.9} />
      {/* sound waves from the mosquito across the rooms */}
      {[0, 1, 2, 3].map(k => { const t = ((f + k * 10) % 40) / 40; return <circle key={k} cx={mx} cy={my} r={40 + t * 900} fill="none" stroke="#ff9a5a" strokeWidth={4} opacity={(1 - t) * 0.5} />; })}
      <g transform={`translate(${mx} ${my})`}>
        <ellipse cx={0} cy={0} rx={22} ry={8} fill="#1a1a1a" /><circle cx={-24} cy={-2} r={7} fill="#1a1a1a" /><line x1={-30} y1={0} x2={-48} y2={6} stroke="#1a1a1a" strokeWidth={2} />
        <ellipse cx={-4} cy={-14} rx={16} ry={6} fill="#bfe0ff" opacity={0.6} transform={`rotate(${Math.sin(f * 2) * 30} -4 -10)`} /><ellipse cx={8} cy={-14} rx={16} ry={6} fill="#bfe0ff" opacity={0.6} transform={`rotate(${-Math.sin(f * 2) * 30} 8 -10)`} />
        {[-10, 4, 18].map(x => <line key={x} x1={x} y1={6} x2={x - 8} y2={28} stroke="#1a1a1a" strokeWidth={2} />)}
      </g>
      <text x={1600} y={300} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={54} fill="#ffb07a" opacity={0.9}>BZZZZZZZZ</text>
    </Layer>
  </>;
};

// inside the ear: canal, eardrum, air molecules bouncing (Brownian) — normal ear vs yours
export const Ear: React.FC<{ f: number; zoom: number; mine: number }> = ({ f, zoom, mine }) => {
  const mol = Array.from({ length: 90 }, (_, i) => { const x = 300 + ((rnd(i, 1) * 1000 + f * (rnd(i, 2) - 0.5) * 28) % 1000 + 1000) % 1000, y = 260 + ((rnd(i, 3) * 560 + f * (rnd(i, 4) - 0.5) * 28) % 560 + 560) % 560; return [x, y]; });
  const hit = mol.filter(([x]) => x > 1240).length;
  const jitter = Math.sin(f * 1.7) * 4 + Math.sin(f * 3.1) * 3;
  return <svg width={W} height={H} style={{ position: "absolute" }}>
    <defs><radialGradient id="canal" cx="0.5" cy="0.5" r="0.7"><stop offset="0" stopColor="#3a1e2a" /><stop offset="1" stopColor="#12080e" /></radialGradient></defs>
    <rect width={W} height={H} fill="url(#canal)" />
    <path d={`M200 220 Q700 160 1300 230 L1300 850 Q700 920 200 860 Z`} fill="#5a2a36" opacity={0.6} />
    <path d={`M200 220 Q700 160 1300 230`} stroke="#c87a7a" strokeWidth={6} fill="none" opacity={0.6} /><path d={`M200 860 Q700 920 1300 850`} stroke="#c87a7a" strokeWidth={6} fill="none" opacity={0.6} />
    {/* eardrum */}
    <ellipse cx={1320 + jitter * mine} cy={540} rx={34} ry={320} fill="#e8b8a8" opacity={0.85} />
    <ellipse cx={1320 + jitter * mine} cy={540} rx={20} ry={300} fill="#f8d8c8" opacity={0.6} />
    <Glow x={1320} y={540} r={260} color="#ffb8a8" o={0.25 + 0.3 * mine} />
    {mol.map(([x, y], i) => <g key={i}><circle cx={x} cy={y} r={9} fill="#7ab8ff" opacity={0.85} /><circle cx={x - 3} cy={y - 3} r={3} fill="#e8f4ff" /></g>)}
    <text x={1320} y={170} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={44} fill="#ffd8c8">EARDRUM</text>
    <text x={600} y={140} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={44} fill="#9ec8ff">AIR MOLECULES</text>
    <g opacity={sat(mine * 2)}><rect x={1440} y={420} width={420} height={240} rx={20} fill="rgba(10,10,20,.7)" stroke="#ff7a7a" strokeWidth={4} />
      <text x={1650} y={500} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={34} fill="#fff">NORMAL EAR: misses it</text>
      <text x={1650} y={580} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={40} fill="#ff7a7a">YOURS: hears it</text></g>
  </svg>;
};
