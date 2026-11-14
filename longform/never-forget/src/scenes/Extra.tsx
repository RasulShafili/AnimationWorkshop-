// Extension scenes: the memory lab (age 12), the brain-scan insert, newspaper headlines, Sam's birthday party, the
// empty cinema of her own life, and the illustrated story panels Lina tells Grandma every Sunday.
import React from "react";
import { Layer, rnd, W, H, sat, lerp, ease, easeOut } from "../engine/core";
import { Glow, Shaft, Bokeh } from "../engine/fx";
import { Noise, Wood, Wallpaper, AO } from "../engine/tex";
import { Character, Pose, SIT, walkPose } from "../chars/Rig2";
import { LINA, SAM, EXTRAS, AYLA } from "../chars/cast";
import { Vignette as MemScene } from "./Palace";

const GOLD = "#ffc94a";
export const MORENO = { top: "#f2f2f4", topDark: "#c8ccd6", pants: "#2c3a52", style: "labcoat" as const, hair: "short" as const, hairColor: "#3a3a44", glasses: true, beard: true, skin: "#2a2632", scale: 1.08, tie: "#2a5aa8" };

// lab: Lina (12) at a table with a light cap of electrodes, Dr. Moreno with a tablet, a wall screen counting the score
export const Lab: React.FC<{ f: number; lina: Pose; doc: Pose; score?: number }> = ({ f, lina, doc, score = 0 }) => <>
  <Layer depth={0.7}>
    <rect x={-1000} y={-500} width={3920} height={1300} fill="#e4ecf0" /><Noise x={-1000} y={-500} w={3920} h={1300} freq={0.7} o={0.08} />
    <rect x={1080} y={120} width={640} height={380} rx={14} fill="#10202e" /><rect x={1096} y={136} width={608} height={348} fill="#0c2a40" />
    <text x={1400} y={220} fontFamily="Inter" fontWeight={900} fontSize={44} fill="#7ad0ff" textAnchor="middle">DATE RECALL TEST</text>
    <text x={1400} y={370} fontFamily="Inter" fontWeight={900} fontSize={150} fill="#fff" textAnchor="middle">{Math.round(score)}<tspan fontSize={70} fill="#7ad0ff">/100</tspan></text>
    <text x={1400} y={450} fontFamily="Inter" fontWeight={800} fontSize={34} fill="#5ae08a" textAnchor="middle">{score > 0 ? "✓ ALL CORRECT" : ""}</text>
    <rect x={150} y={180} width={360} height={260} fill="#fff" stroke="#9aa8b4" strokeWidth={8} />
    {Array.from({ length: 6 }, (_, i) => <rect key={i} x={180} y={210 + i * 36} width={160 + (i * 37) % 140} height={14} fill="#c8d4dc" />)}
    {Array.from({ length: 5 }, (_, i) => <rect key={i} x={-600 + i * 70} y={260} width={50} height={300} rx={8} fill={["#9ad0e8", "#c8e0c8", "#e8d8a8", "#d8c8e8", "#e8c0c0"][i]} />)}
  </Layer>
  <Layer depth={1}>
    <rect x={-1100} y={760} width={4120} height={600} fill="#cfd8dc" />
    {Array.from({ length: 22 }, (_, i) => <line key={i} x1={-1100 + i * 200} y1={760} x2={-1300 + i * 200} y2={1360} stroke="#000" strokeOpacity={0.05} strokeWidth={3} />)}
    <rect x={500} y={560} width={18} height={220} rx={6} fill="#5a6a7a" /><rect x={500} y={770} width={130} height={16} rx={5} fill="#6a7a8a" />
    <g opacity={0.9}>{[-30, -10, 10, 30].map(dx => <path key={dx} d={`M${576 + dx} ${860 - 280 * 0.86 - 70} q-40 ${30 + dx * 0.5} -${110 + dx} ${150 + dx}`} stroke="#2a5aa8" strokeWidth={3} fill="none" />)}
      <rect x={380} y={600} width={90} height={70} rx={8} fill="#3a4a5a" /><circle cx={400} cy={622} r={6} fill="#5ae08a" /><rect x={416} y={616} width={40} height={10} fill="#7ad0ff" />
      <rect x={380} y={600} width={90} height={70} rx={8} fill="#3a4a5a" /><circle cx={400} cy={622} r={6} fill="#5ae08a" /><rect x={416} y={616} width={40} height={10} fill="#7ad0ff" /></g>
    <Character look={{ ...LINA, scale: 0.86 }} pose={{ ...SIT, facing: 1, ...lina }} x={570} y={860} f={f} seed={1} rim={{ dx: 4, dy: -3, color: "#e8f4ff" }} />
    <g opacity={0.9}>{[-36, -12, 12, 36].map(dx => <circle key={dx} cx={576 + dx} cy={860 - 280 * 0.86 - 72} r={7} fill="#3a7ad8" />)}</g>

    <Character look={MORENO} pose={{ facing: -1, hold: "phone", aR: [50, 80], ...doc }} x={1000} y={870} f={f} seed={9} rim={{ dx: -4, dy: -3, color: "#e8f4ff" }} />
    <rect x={640} y={690} width={300} height={20} rx={4} fill="#9aa8b4" /><rect x={650} y={710} width={280} height={150} fill="#7a8a98" />
    <Glow x={1400} y={300} r={700} color="#7ad0ff" o={0.15} />
  </Layer>
</>;

// brain-scan insert: a side-view brain; a gold fibre bundle linking the front (planning) and the temporal lobe (memory/emotion) pulses
export const BrainScan: React.FC<{ f: number }> = ({ f }) => { const k = ease(f / 40), pulse = 0.6 + 0.4 * Math.sin(f * 0.25);
  return <svg width={W} height={H} style={{ position: "absolute", transform: `scale(${1 + f * 0.0012})`, transformOrigin: "860px 500px" }}>
    <rect width={W} height={H} fill="#06101a" /><Glow x={960} y={520} r={700} color="#2a6aff" o={0.18} />
    {Array.from({ length: 40 }, (_, i) => <line key={i} x1={0} y1={i * 28} x2={W} y2={i * 28} stroke="#7ad0ff" strokeOpacity={0.03} />)}
    <path d="M520 600 Q480 330 760 240 Q960 170 1160 230 Q1420 290 1430 470 Q1440 620 1300 680 Q1180 720 1100 700 Q1040 780 940 770 Q800 760 760 700 Q600 720 520 600 Z" fill="#12283c" stroke="#3a7ad8" strokeWidth={5} />
    {Array.from({ length: 12 }, (_, i) => <path key={i} d={`M${600 + (i % 6) * 130} ${330 + Math.floor(i / 6) * 180} q30 -36 60 0 t60 0 q20 36 -12 64`} stroke="#24486c" strokeWidth={6} fill="none" />)}
    {/* the bundle */}
    {Array.from({ length: 9 }, (_, i) => { const o = (i - 4) * 7; return <path key={i} d={`M${700 + o} ${420 + o} C ${760} ${620 + o}, ${900} ${700 + o * 0.5}, ${1000 + o} ${650 + o}`} stroke={GOLD} strokeWidth={4} fill="none"
      strokeDasharray={`${900 * k} 900`} opacity={0.5 + 0.5 * pulse} style={{ filter: `drop-shadow(0 0 ${6 + 6 * pulse}px ${GOLD})` }} />; })}
    <circle cx={700} cy={420} r={18 + 6 * pulse} fill={GOLD} opacity={0.8 * k} /><circle cx={1000} cy={650} r={18 + 6 * pulse} fill={GOLD} opacity={0.8 * k} />
    <text x={640} y={380} fontFamily="Inter" fontWeight={800} fontSize={30} fill="#9ac8ff" opacity={k}>PLANNING</text>
    <text x={1030} y={700} fontFamily="Inter" fontWeight={800} fontSize={30} fill="#9ac8ff" opacity={k}>MEMORY + EMOTION</text>
    <text x={120} y={130} fontFamily="Inter" fontWeight={900} fontSize={44} fill="#7ad0ff">MRI · SUBJECT 12-L</text>
  </svg>; };

// newspapers spinning in, one after another (every 26 frames)
export const Headlines: React.FC<{ f: number }> = ({ f }) => {
  const P = [["THE DAILY STAR", "GIRL, 12, WHO\nNEVER FORGETS"], ["MORNING POST", "\"SHE REMEMBERS\nEVERY DAY\""], ["CITY HERALD", "A MEDICAL\nMYSTERY"]];
  return <svg width={W} height={H} style={{ position: "absolute", transform: `scale(${1 + Math.max(0, f - 60) * 0.0015})`, transformOrigin: "960px 540px" }}>
    <rect width={W} height={H} fill="#2a2420" /><Glow x={960} y={540} r={800} color="#ffd890" o={0.25} />
    {P.map(([mast, head], i) => { const t = easeOut((f - i * 26) / 16); if (t <= 0) return null; const rot = (1 - t) * 540 + (i - 1) * 7, sc = 0.3 + 0.7 * t;
      return <g key={i} transform={`translate(${470 + i * 490} ${520 + (i % 2) * 40}) rotate(${rot}) scale(${sc * 0.6})`}>
        <rect x={-430} y={-300} width={860} height={600} fill="#f4efe2" stroke="#c8bea8" strokeWidth={3} />
        <text x={0} y={-220} fontFamily="Georgia, serif" fontWeight={900} fontSize={60} fill="#1a1a1a" textAnchor="middle">{mast}</text>
        <line x1={-400} y1={-190} x2={400} y2={-190} stroke="#1a1a1a" strokeWidth={4} />
        {head.split("\n").map((l, k) => <text key={k} x={-390} y={-110 + k * 84} fontFamily="Inter" fontWeight={900} fontSize={76} fill="#111">{l}</text>)}
        <rect x={150} y={20} width={230} height={240} fill="#8a8a8a" /><circle cx={265} cy={110} r={56} fill="#2a2536" /><path d="M205 80 Q265 30 325 80 L325 100 L205 100 Z" fill="#e3a83b" />
        {Array.from({ length: 6 }, (_, k) => <rect key={k} x={-390} y={60 + k * 32} width={500} height={12} fill="#b8b0a0" />)}
      </g>; })}
  </svg>; };

// Sam's surprise party in a garage: string lights, banner, table with blue cupcakes and a cake with his dog Biscuit
export const Party: React.FC<{ f: number; lina: Pose; sam: Pose & { x?: number }; confetti?: number; showLina?: boolean }> = ({ f, lina, sam, confetti = 0, showLina = true }) => <>
  <Layer depth={0.7}>
    <rect x={-1000} y={-500} width={3920} height={1300} fill="#3a3448" />
    {Array.from({ length: 20 }, (_, i) => <rect key={i} x={-1000 + i * 200} y={-500} width={190} height={1300} fill="#423a52" />)}
    <path d="M-200 120 Q300 220 800 120 Q1300 220 1800 120 Q2200 200 2400 140" stroke="#222" strokeWidth={3} fill="none" />
    {Array.from({ length: 30 }, (_, i) => { const x = -200 + i * 90; const y = 150 + Math.sin(i * 0.7) * 30; return <g key={i}><circle cx={x} cy={y} r={10} fill={["#ffd890", "#ff8ac8", "#8ad8ff", "#aaf08a"][i % 4]} /><circle cx={x} cy={y} r={30} fill={["#ffd890", "#ff8ac8", "#8ad8ff", "#aaf08a"][i % 4]} opacity={0.18} /></g>; })}
    <g transform="translate(860 300)">{"HAPPY BIRTHDAY SAM!".split("").map((ch, i) => <g key={i} transform={`translate(${(i - 9) * 64} ${Math.sin(i * 0.5) * 14})`}><path d="M-28 0 L28 0 L0 60 Z" fill={["#ff6a6a", "#6ab0ff", "#ffd04a", "#6ad08a"][i % 4]} />
      <text x={0} y={34} fontFamily="Inter" fontWeight={900} fontSize={30} fill="#fff" textAnchor="middle">{ch}</text></g>)}</g>
  </Layer>
  <Layer depth={0.85} blur={2.5}>
    {[-200, 150, 1650, 2000].map((x, i) => <Character key={i} look={EXTRAS[(i + 1) % EXTRAS.length]} pose={{ facing: i < 2 ? 1 : -1, aR: [140, 30], mouth: "grin", look: [0.7, -0.2] }} x={x} y={780} s={0.82} f={f} seed={40 + i} />)}
  </Layer>
  <Layer depth={1}>
    <rect x={-1100} y={760} width={4120} height={600} fill="#5a5060" />
    {showLina && <Character look={LINA} pose={{ facing: 1, ...lina }} x={560} y={870} f={f} seed={1} rim={{ dx: 4, dy: -3, color: "#ffd890" }} />}
    <Character look={SAM} pose={{ facing: -1, ...sam }} x={sam.x ?? 1300} y={870} f={f} seed={3} rim={{ dx: -4, dy: -3, color: "#ffd890" }} />
    {/* party table */}
    <rect x={720} y={690} width={440} height={20} rx={4} fill="#fff" /><rect x={730} y={710} width={420} height={150} fill="#e8e4f0" />
    {[0, 1, 2, 3, 4].map(i => <g key={i} transform={`translate(${760 + i * 36} 690)`}><path d="M-14 0 L14 0 L10 -18 L-10 -18 Z" fill="#c8a07a" /><ellipse cx={0} cy={-22} rx={15} ry={10} fill="#5ab0ff" /></g>)}
    <g transform="translate(1030 690)"><rect x={-70} y={-70} width={140} height={70} rx={10} fill="#fbe8d0" /><rect x={-70} y={-80} width={140} height={20} rx={10} fill="#fff" />
      <circle cx={0} cy={-36} r={20} fill="#c8946a" /><circle cx={-14} cy={-52} r={9} fill="#9a6a4a" /><circle cx={14} cy={-52} r={9} fill="#9a6a4a" /><text x={0} y={-6} fontFamily="Inter" fontWeight={900} fontSize={14} fill="#c0392b" textAnchor="middle">BISCUIT</text>
      {[-30, 0, 30].map(dx => <g key={dx}><rect x={dx - 3} y={-104} width={6} height={24} fill="#ff8ac8" /><ellipse cx={dx} cy={-110} rx={5} ry={8} fill="#ffd04a" /></g>)}</g>
    <rect x={850} y={656} width={80} height={34} rx={4} fill="#e84a4a" /><rect x={884} y={656} width={12} height={34} fill="#ffd04a" />
    {confetti > 0 && Array.from({ length: 80 }, (_, i) => { const x = rnd(i, 1) * 2000 - 50, y = ((rnd(i, 2) * 900 + f * (3 + rnd(i, 3) * 3)) % 1100) - 100;
      return <rect key={i} x={x} y={y} width={10} height={16} fill={["#ff6a6a", "#6ab0ff", "#ffd04a", "#6ad08a", "#ff8ac8"][i % 5]} transform={`rotate(${f * 6 + i * 40} ${x + 5} ${y + 8})`} opacity={confetti} />; })}
    <Glow x={900} y={400} r={1000} color="#ffd890" o={0.2} />
  </Layer>
</>;

// the empty cinema of her own life: rows of seats, Lina alone in the middle row, the screen shows memories
export const Cinema: React.FC<{ f: number; lina: Pose; scene: number; flick?: number }> = ({ f, lina, scene, flick = 1 }) => {
  const light = 0.75 + 0.25 * Math.sin(f * 0.9) * flick;
  return <>
    <Layer depth={0.6}>
      <rect x={-1000} y={-500} width={3920} height={1400} fill="#0a0608" />
      <rect x={260} y={20} width={1400} height={600} fill="#111" />
      <g opacity={light}><MemScene x={280} y={40} w={1360} h={560} i={scene} /></g>
      <rect x={280} y={40} width={1360} height={560} fill={scene % 2 ? "#3a5aa8" : "#ffd890"} opacity={0.1} />
      <Glow x={960} y={320} r={900} color={scene % 2 ? "#8aa8ff" : "#ffd890"} o={0.25 * light} />
      {[-700, 1800].map(x => <rect key={x} x={x} y={-100} width={600} height={900} fill="#2a0a12" />)}
    </Layer>
    <Layer depth={0.85}>
      {Array.from({ length: 16 }, (_, i) => <path key={i} d={`M${-400 + i * 180} 860 L${-400 + i * 180} 740 Q${-310 + i * 180} 700 ${-220 + i * 180} 740 L${-220 + i * 180} 860 Z`} fill="#5a1220" />)}
    </Layer>
    <Layer depth={1}>
      <rect x={-1100} y={860} width={4120} height={600} fill="#1a0a10" />
      {Array.from({ length: 14 }, (_, i) => { const x = -500 + i * 200; return <path key={i} d={`M${x} 960 L${x} 790 Q${x + 90} 740 ${x + 180} 790 L${x + 180} 960 Z`} fill="#6a1626" />; })}
      <Character look={LINA} pose={{ ...SIT, facing: 1, look: [0.2, -0.6], ...lina }} x={980} y={960} f={f} seed={1} rim={{ dx: 2, dy: -5, color: scene % 2 ? "#8aa8ff" : "#ffd890" }} />
      <path d="M900 960 L900 800 Q990 750 1080 800 L1080 960 Z" fill="#6a1626" opacity={0} />
    </Layer>
    <Layer depth={1.3} blur={6}>
      {Array.from({ length: 12 }, (_, i) => { const x = -700 + i * 240; return <path key={i} d={`M${x} 1200 L${x} 980 Q${x + 110} 930 ${x + 220} 980 L${x + 220} 1200 Z`} fill="#3a0a14" />; })}
    </Layer>
  </>;
};

// an illustrated story panel (one of Ayla's own memories) that floats up beside them
export const StoryPanel: React.FC<{ x: number; y: number; k: number; kind: "bus" | "bakery" | "dance"; label: string }> = ({ x, y, k, kind, label }) => k <= 0 ? null :
  <g transform={`translate(${x} ${y + (1 - easeOut(k)) * 60}) scale(${0.85 + 0.15 * easeOut(k)})`} opacity={Math.min(1, k * 1.5)}>
    <rect x={-250} y={-180} width={500} height={360} rx={16} fill={GOLD} opacity={0.35} style={{ filter: "blur(10px)" }} />
    <rect x={-240} y={-170} width={480} height={340} rx={12} fill="#fff6dc" />
    <rect x={-224} y={-154} width={448} height={260} fill={kind === "bus" ? "#6a7a94" : kind === "bakery" ? "#f0c890" : "#5a3a6a"} />
    {kind === "bus" && <><rect x={-224} y={40} width={448} height={66} fill="#4a5262" />{Array.from({ length: 30 }, (_, i) => <line key={i} x1={-220 + (i * 37) % 440} y1={-150 + (i * 53) % 190} x2={-226 + (i * 37) % 440} y2={-130 + (i * 53) % 190} stroke="#c8d8ec" strokeWidth={2} />)}
      <rect x={60} y={-120} width={12} height={170} fill="#c8c8c8" /><rect x={30} y={-140} width={80} height={40} rx={6} fill="#2a8a4a" /><text x={70} y={-112} fontFamily="Inter" fontWeight={900} fontSize={18} fill="#fff" textAnchor="middle">BUS</text>
      <path d="M-160 -40 Q-90 -110 -20 -40 Z" fill="#c8302c" /><line x1={-90} y1={-70} x2={-90} y2={40} stroke="#333" strokeWidth={4} />
      <circle cx={-125} cy={-10} r={22} fill="#2e2a38" /><rect x={-142} y={12} width={34} height={60} rx={10} fill="#e8a4c0" /><circle cx={-60} cy={-14} r={22} fill="#2e2a38" /><rect x={-77} y={8} width={34} height={64} rx={10} fill="#3a3a4a" /></>}
    {kind === "bakery" && <><rect x={-180} y={-130} width={360} height={200} fill="#d8a46a" /><rect x={-200} y={-150} width={400} height={50} fill="#c8302c" />
      <text x={0} y={-114} fontFamily="Georgia, serif" fontWeight={900} fontSize={28} fill="#fff" textAnchor="middle">AYLA'S BAKERY · 1978</text>
      <rect x={-150} y={-80} width={140} height={110} fill="#fff4dc" /><rect x={20} y={-80} width={130} height={150} fill="#7a4a2a" />{[0, 1, 2].map(i => <circle key={i} cx={-120 + i * 45} cy={-30} r={16} fill="#e8b04a" />)}</>}
    {kind === "dance" && <><ellipse cx={0} cy={80} rx={220} ry={30} fill="#8a6a9a" />{Array.from({ length: 6 }, (_, i) => <line key={i} x1={-200 + i * 80} y1={-154} x2={-120 + i * 40} y2={60} stroke="#fff4c0" strokeWidth={10} opacity={0.15} />)}
      <circle cx={-50} cy={-30} r={24} fill="#2e2a38" /><path d="M-80 50 Q-50 -10 -20 50 Z" fill="#e84a7a" /><circle cx={40} cy={-34} r={24} fill="#2e2a38" /><rect x={24} y={-10} width={34} height={64} rx={10} fill="#2a2a3a" />
      <path d="M130 -60 L170 -60 L160 -10 L140 -10 Z" fill={GOLD} /><rect x={140} y={-10} width={20} height={30} fill={GOLD} /><text x={-50} y={-62} fontSize={30} textAnchor="middle">😉</text></>}
    <text x={0} y={150} fontFamily="Inter" fontWeight={900} fontSize={30} fill="#5a4030" textAnchor="middle">{label}</text>
  </g>;

// memory flash: bus 42 at a stop, a man in a red jacket stepping off with a yellow umbrella (gold markers)
export const BusMemory: React.FC<{ f: number }> = ({ f }) => { const k = sat((f - 20) / 12);
  return <svg width={W} height={H} style={{ position: "absolute", transform: `scale(${1 + f * 0.001})`, transformOrigin: "960px 540px" }}>
    <rect width={W} height={H} fill="#9ec6e8" /><rect y={560} width={W} height={160} fill="#c8c2b6" /><rect y={720} width={W} height={360} fill="#4a4e58" />
    <rect x={120} y={260} width={1060} height={420} rx={40} fill="#2a8a5a" /><rect x={120} y={600} width={1060} height={60} fill="#1e6a44" />
    {[0, 1, 2, 3, 4].map(i => <rect key={i} x={170 + i * 190} y={310} width={160} height={150} rx={14} fill="#bfe0f0" />)}
    <rect x={1040} y={330} width={110} height={270} rx={10} fill="#1a3a2a" /><rect x={960} y={280} width={190} height={40} rx={8} fill="#111" />
    <text x={1055} y={310} fontFamily="Inter" fontWeight={900} fontSize={30} fill="#ffb03a" textAnchor="middle">42 MAPLE ST</text>
    {[260, 980].map(cx => <g key={cx}><circle cx={cx} cy={690} r={56} fill="#16171c" /><circle cx={cx} cy={690} r={26} fill="#9aa2ae" /></g>)}
    <Character look={{ ...EXTRAS[2], top: "#d8302c", topDark: "#a02020", style: "jacket", hair: "short" }} pose={{ facing: 1, aR: [140, 30], look: [0.6, 0] }} x={1300} y={720} s={1.1} f={f} seed={50} />
    <line x1={1350} y1={190} x2={1352} y2={285} stroke="#333" strokeWidth={6} /><path d="M1220 200 Q1350 90 1480 200 Q1415 186 1350 200 Q1285 186 1220 200 Z" fill="#ffd030" /><path d="M1350 100 L1350 200" stroke="#e8b020" strokeWidth={3} />
    {k > 0 && <g opacity={k}><rect x={950} y={270} width={210} height={60} fill="none" stroke={GOLD} strokeWidth={5} rx={6} /><rect x={1210} y={90} width={280} height={400} fill="none" stroke={GOLD} strokeWidth={5} rx={8} />
      <rect x={1250} y={330} width={130} height={150} fill="none" stroke={GOLD} strokeWidth={0} /></g>}
  </svg>; };

// the case board: three posters get gold FOUND stamps one after another
export const CaseBoard: React.FC<{ f: number; seg: number }> = ({ f, seg }) => {
  const P = [["STOLEN BIKE", "#c0392b"], ["LOST DOG", "#2a6ad8"], ["WITNESS WANTED", "#7a4ab8"]];
  return <svg width={W} height={H} style={{ position: "absolute", transform: `scale(${1 + f * 0.0008})`, transformOrigin: "960px 540px" }}>
    <rect width={W} height={H} fill="#8a6a44" /><Noise x={0} y={0} w={W} h={H} freq={0.6} o={0.3} />
    {P.map(([t, c], i) => { const x = 220 + i * 520, stamp = i < seg ? 1 : i === seg ? sat((f % 40) / 8) : 0;
      return <g key={i} transform={`rotate(${(i - 1) * 3} ${x + 220} 520)`}>
        <rect x={x} y={220} width={440} height={600} fill="#f8f4ea" /><circle cx={x + 220} cy={232} r={12} fill="#d83a3a" />
        <text x={x + 220} y={310} fontFamily="Inter" fontWeight={900} fontSize={46} fill={c} textAnchor="middle">{t}</text>
        <rect x={x + 50} y={340} width={340} height={300} fill="#d8d4c8" />
        {i === 0 && <g transform={`translate(${x + 220} 500)`}><circle cx={-80} cy={30} r={56} fill="none" stroke="#222" strokeWidth={9} /><circle cx={80} cy={30} r={56} fill="none" stroke="#222" strokeWidth={9} /><path d="M-80 30 L0 30 L40 -40 L-40 -40 Z M40 -40 L80 30" stroke="#c0392b" strokeWidth={9} fill="none" /></g>}
        {i === 1 && <g transform={`translate(${x + 220} 500)`}><ellipse cx={0} cy={30} rx={100} ry={60} fill="#c8946a" /><circle cx={-90} cy={-30} r={50} fill="#c8946a" /><ellipse cx={-120} cy={-70} rx={18} ry={34} fill="#9a6a4a" /><circle cx={-100} cy={-36} r={6} fill="#111" /></g>}
        {i === 2 && <g transform={`translate(${x + 220} 500)`}>{Array.from({ length: 9 }, (_, k) => <circle key={k} cx={-110 + (k % 3) * 110} cy={-80 + Math.floor(k / 3) * 80} r={30} fill="#3a3448" />)}<circle cx={0} cy={0} r={44} fill="none" stroke={GOLD} strokeWidth={6} /></g>}
        {Array.from({ length: 3 }, (_, k) => <rect key={k} x={x + 60} y={680 + k * 36} width={320} height={14} fill="#c8c0b0" />)}
        {stamp > 0 && <g transform={`translate(${x + 220} 520) rotate(-14) scale(${1 + 0.5 * (1 - stamp)})`} opacity={stamp}><rect x={-160} y={-60} width={320} height={120} rx={10} fill="none" stroke={GOLD} strokeWidth={12} />
          <text x={0} y={30} fontFamily="Inter" fontWeight={900} fontSize={84} fill={GOLD} textAnchor="middle">FOUND</text></g>}
      </g>; })}
  </svg>; };

// "search engine": a search box typing a vague query, answered instantly by Lina's memory
export const SearchUI: React.FC<{ f: number }> = ({ f }) => { const q = "red jacket, bus stop, last spring", typed = q.slice(0, Math.floor(f / 1.5)), res = sat((f - q.length * 1.5 - 4) / 8);
  return <svg width={W} height={H} style={{ position: "absolute" }}>
    <rect width={W} height={H} fill="#f4f6fa" /><Glow x={960} y={400} r={800} color={GOLD} o={0.15} />
    <text x={960} y={300} fontFamily="Inter" fontWeight={900} fontSize={110} fill="#1f6f78" textAnchor="middle">Ask <tspan fill="#e3a83b">Lina</tspan></text>
    <rect x={360} y={380} width={1200} height={110} rx={55} fill="#fff" stroke="#c8d0dc" strokeWidth={4} />
    <circle cx={430} cy={435} r={22} fill="none" stroke="#7a8494" strokeWidth={6} /><line x1={446} y1={451} x2={466} y2={471} stroke="#7a8494" strokeWidth={6} />
    <text x={500} y={452} fontFamily="Inter" fontWeight={700} fontSize={46} fill="#333">{typed}{f % 20 < 10 && res === 0 ? "|" : ""}</text>
    {res > 0 && <g opacity={res}>{["Bus 42 · got off at Maple Street · 4:51 pm", "Yellow umbrella, left hand · grey sneakers", "Same man seen 14 Mar, Elm St bakery"].map((l, i) =>
      <g key={i} transform={`translate(380 ${560 + i * 120})`}><rect x={0} y={0} width={1160} height={96} rx={16} fill="#fff" stroke="#e0e4ec" strokeWidth={3} /><text x={36} y={60} fontFamily="Inter" fontWeight={800} fontSize={38} fill={i === 0 ? "#1f6f78" : "#444"}>{l}</text></g>)}
      <text x={1540} y={540} fontFamily="Inter" fontWeight={800} fontSize={30} fill="#9aa4b4" textAnchor="end">1 result in 0.0 seconds</text></g>}
  </svg>; };

// Part 2 teaser bits: a figure behind frosted glass; a torn calendar page "MARCH 14" spinning in the dark
export const Frosted: React.FC<{ f: number }> = ({ f }) => <svg width={W} height={H} style={{ position: "absolute" }}>
  <rect width={W} height={H} fill="#05040a" /><rect x={560} y={80} width={800} height={920} fill="#1c2236" /><rect x={560} y={80} width={800} height={920} fill="url(#frost)" />
  <defs><radialGradient id="frost" cx="0.5" cy="0.45" r="0.6"><stop offset="0" stopColor="#7a8ab8" stopOpacity={0.6} /><stop offset="1" stopColor="#1c2236" stopOpacity={0} /></radialGradient></defs>
  <g style={{ filter: "blur(14px)" }} transform={`translate(${Math.sin(f * 0.05) * 20} 0)`}><circle cx={960} cy={420} r={110} fill="#05040a" /><path d="M820 1000 L850 560 Q960 500 1070 560 L1100 1000 Z" fill="#05040a" /></g>
  <Noise x={560} y={80} w={800} h={920} freq={0.9} o={0.35} blend="screen" />
  <rect x={540} y={60} width={840} height={960} fill="none" stroke="#2a2a3a" strokeWidth={30} />
</svg>;
export const TornPage: React.FC<{ f: number }> = ({ f }) => <svg width={W} height={H} style={{ position: "absolute" }}>
  <rect width={W} height={H} fill="#05040a" /><Glow x={960} y={540} r={500} color="#ff3a3a" o={0.15} />
  <g transform={`translate(960 ${520 + f * 2}) rotate(${-10 + f * 1.5}) scale(${1 + f * 0.004})`}>
    <path d="M-220 -280 L220 -280 L220 200 L180 230 L140 196 L90 240 L40 200 L-10 236 L-60 198 L-110 240 L-160 202 L-220 236 Z" fill="#f4efe2" />
    <rect x={-220} y={-280} width={440} height={110} fill="#c8302c" /><text x={0} y={-205} fontFamily="Inter" fontWeight={900} fontSize={64} fill="#fff" textAnchor="middle">MARCH</text>
    <text x={0} y={90} fontFamily="Inter" fontWeight={900} fontSize={240} fill="#1a1a1a" textAnchor="middle">14</text>
    <text x={0} y={160} fontFamily="Inter" fontWeight={800} fontSize={40} fill="#888" textAnchor="middle">2020</text>
  </g>
</svg>;
