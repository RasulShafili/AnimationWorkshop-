// Chapters 9–12: the hunt, the storm, the painting, 2026.
import React from "react";
import { AbsoluteFill } from "remotion";
import { sat, lerp, rnd, W, H } from "../engine/core";
import { Glow } from "../engine/fx";
import { ChapterPlayer, Ctx, Shot, chLen } from "../Player";
import { S, mv, onHead, P, Big, walk, run, SIT } from "./H";
import { Camp, Valley, Blizzard, PaintedCave, ResearchCave, Snow, Fire } from "../scenes/Ice";
import { Mammoth, Reindeer } from "../scenes/Animals";
import { Thrower, BoneTally, PhoneShot, Tablet, EndCard } from "../scenes/Inserts";
import { Character } from "../chars/Rig2";
import { ELI_PACK, ELI_FUR, NIA, TOR, PIP, AMA, BAND, VOSS, SCIENTIST } from "../chars/cast";
import { VO_C9 } from "../vo_c9"; import { VO_C10 } from "../vo_c10"; import { VO_C11 } from "../vo_c11"; import { VO_C12 } from "../vo_c12";

const warm = "#ffb060";
const camp = (c: Ctx, cam: number[][], kids: React.ReactNode, night = false) => <S cam={mv(c, cam[0], cam[1])}><Camp f={c.f} night={night}>{kids}</Camp></S>;
const val = (c: Ctx, cam: number[][], kids: React.ReactNode, time: any = "day") => <S cam={mv(c, cam[0], cam[1])}><Valley f={c.f} time={time} herd={false}>{kids}</Valley></S>;

// ================= C9 — Day 30: the hunt =================
const Pendant: React.FC<{ f: number; k: number }> = ({ f, k }) => <svg width={W} height={H} style={{ position: "absolute" }}><rect width={W} height={H} fill="#2a1a10" /><Glow x={960} y={540} r={800} color="#ff9a3a" o={0.35} />
  <path d="M760 0 Q900 300 960 380 Q1020 300 1160 0" stroke="#5a3e28" strokeWidth={8} fill="none" />
  <g transform="translate(960 600) rotate(6)"><path d="M-300 -60 Q-340 -100 -300 -130 L300 -130 Q340 -100 300 -60 L300 60 Q340 100 300 130 L-300 130 Q-340 100 -300 60 Z" fill="#e8dcc0" />
    <g stroke="#3a2a1a" strokeWidth={8} fill="none" strokeLinecap="round" strokeDasharray="900" strokeDashoffset={900 * (1 - k)}><circle cx={0} cy={-60} r={30} /><path d="M-36 -70 Q0 -120 36 -70" /><path d="M0 -30 L0 50 M0 50 L-30 100 M0 50 L30 100 M0 -10 L40 10" /><rect x={40} y={-6} width={26} height={40} rx={4} /></g></g></svg>;
const hunters = (f: number, x: number, mode: "walk" | "run") => { const pose = (o: number) => mode === "walk" ? { ...walk(f + o, 1, 0.7) } : { ...run(f + o) };
  return <>{P(TOR, { facing: 1, hold: "spear", aR: [30, 20], ...pose(3) }, x + 300, 1000, 0.8, f, 3)}{P(BAND[0], { facing: 1, hold: "spear", aR: [30, 20], ...pose(7) }, x + 150, 1000, 0.8, f, 21)}{P(NIA, { facing: 1, hold: "spear", aR: [30, 20], ...pose(5) }, x, 1000, 0.8, f, 4)}{P(ELI_FUR, { facing: 1, ...pose(1) }, x - 150, 1000, 0.8, f, 1)}</>; };
const c9: Shot[] = [
  { at: ["n1"], r: c => val(c, [[-200, -40, 1.0], [0, -40, 1.05]], <>{Array.from({ length: 4 }, (_, i) => <g key={i} transform={`translate(${200 + i * 400} 1000)`}><Reindeer ph={c.f * 0.15 + i} s={0.6} graze={i % 2} /></g>)}</>, "dusk") },
  { at: ["n2"], r: c => camp(c, [[-120, 60, 1.4], [-100, 60, 1.45]], <>{P(NIA, { ...SIT, facing: 1, aR: [50, 80], look: [0.8, 0.4], mouth: "o" }, 560, 1010, 1.0, c.f, 4)}{P(ELI_FUR, { ...SIT, facing: -1, aR: [50, 80], aL: [45, 85], look: [-0.2, 0.6], mouth: "smile" }, 900, 1010, 1.05, c.f, 1)}
    <path d="M820 840 L980 830 L996 812" stroke="#d8c8a0" strokeWidth={14} fill="none" strokeLinecap="round" /></>) },
  { at: ["fact1"], r: c => <Thrower f={c.f} k={sat(c.t / (c.d * 0.6))} /> },
  { at: ["nia1"], r: c => val(c, [onHead(900, 1060, 1.0, 2.3, -30, 40), onHead(900, 1060, 1.0, 2.45, -30, 40)], <>{P(NIA, { facing: -1, talk: c.talk("nia1"), mouth: "grin", eyes: 1.25, brow: 0.6, hold: "spear", aR: [100 + 20 * Math.sin(c.f * 0.5), 30], look: [-0.7, -0.2] }, 900, 1060, 1.0, c.f, 4)}</>) },
  { at: ["n3"], r: c => val(c, [[-200, -40, 1.05], [200, -40, 1.05]], <>{hunters(c.f, 200 + c.t * 3, "walk")}<g transform="translate(1700 1000) scale(0.5)"><Mammoth ph={c.f * 0.05} trunk={Math.sin(c.f * 0.05)} /></g></>) },
  { at: ["n4"], r: c => { const ch = sat(c.t / (c.d * 0.6)); return val(c, [[200, -40, 1.2], [260, -60, 1.3]], <>
    {P(NIA, { facing: 1, hold: "spear", aR: [40, 20], ...(c.t > c.d * 0.5 ? { lean: -40, lL: [60, 10], lR: [-30, 40], mouth: "o", eyes: 1.4, brow: 0.8 } : run(c.f)) }, 900, 1000, 0.85, c.f, 4)}
    <g transform={`translate(${1700 - 500 * ch} 1000) scale(-0.62 0.62)`}><Mammoth ph={c.f * 0.2} trumpet={1} angry={1} /></g>
    {Array.from({ length: 10 }, (_, i) => <circle key={i} cx={1700 - 500 * ch + rnd(i, 3) * 200} cy={990 + rnd(i, 4) * 20} r={10 + rnd(i, 5) * 20} fill="#fff" opacity={0.8} />)}</>); } },
  { at: ["eli1"], r: c => val(c, [onHead(600, 1000, 0.85, 2.4, 40, 40), onHead(600, 1000, 0.85, 2.6, 40, 40)], <>{P(ELI_FUR, { facing: 1, talk: c.talk("eli1"), mouth: "shout", eyes: 1.4, brow: 0.8, aR: [120, 20], look: [0.9, 0] }, 600, 1000, 0.85, c.f, 1)}</>) },
  { at: ["throw"], r: c => { const t = sat(c.t / 18); return val(c, [[0, -40, 1.1], [80, -40, 1.12]], <>
    {P(ELI_FUR, { facing: 1, aR: [lerp(170, 60, t), 10], lean: 10 * t, mouth: "shout" }, 500, 1000, 0.85, c.f, 1)}
    {t > 0.3 && <g transform={`translate(${lerp(560, 1450, sat((c.t - 6) / 14))} ${720 - Math.sin(sat((c.t - 6) / 14) * Math.PI) * 140}) rotate(${-10 + 25 * sat((c.t - 6) / 14)})`}><line x1={-140} y1={0} x2={0} y2={0} stroke="#6a4a2a" strokeWidth={6} /><path d="M0 -8 L30 0 L0 8 Z" fill="#7a808a" /></g>}
    <g transform="translate(1500 1000) scale(-0.62 0.62)"><Mammoth ph={c.f * 0.1} trumpet={1} angry={1} /></g></>); } },
  { at: ["n5"], r: c => val(c, [[0, -40, 1.05], [0, -40, 1.0]], <>{P(NIA, { facing: 1, mouth: "grin", aR: [120, 20], hold: "spear" }, 760, 1000, 0.85, c.f, 4)}{P(ELI_FUR, { facing: 1, mouth: "grin", aR: [125, 25] }, 560, 1000, 0.85, c.f, 1)}{P(TOR, { facing: 1, mouth: "grin", hold: "spear", aR: [110, 20] }, 960, 1000, 0.85, c.f, 3)}
    <g transform={`translate(${1500 + c.t * 8} 1000) scale(0.55)`}><Mammoth ph={c.f * 0.2} /></g></>) },
  { at: ["n6"], r: c => <Pendant f={c.f} k={sat(c.t / (c.d * 0.7))} /> },
];
export const C9: React.FC = () => <ChapterPlayer ch="c9" vo={VO_C9} shots={c9}
  facts={[["fact1", "A spear-thrower works like an extra arm: it can launch a spear at over 150 km/h. The oldest ones found are about 20,000 years old."]]} />;
export const C9_LEN = chLen("c9", VO_C9);

// ================= C10 — Day 60: the storm =================
const Gully: React.FC<{ f: number; children?: React.ReactNode }> = ({ f, children }) => <g>
  <rect x={-1000} y={-500} width={4000} height={1800} fill="#5a6a88" />
  <path d="M-1000 -500 L600 -500 L760 1300 L-1000 1300 Z" fill="#8a96b0" /><path d="M3000 -500 L1300 -500 L1160 1300 L3000 1300 Z" fill="#7a86a0" />
  <path d="M-1000 900 Q960 840 3000 900 L3000 1300 L-1000 1300 Z" fill="#e8eef4" />
  {children}<Snow f={f} n={160} wind={8} speed={7} />
  <rect x={-1000} y={-500} width={4000} height={1800} fill="#1a2040" opacity={0.3} style={{ mixBlendMode: "multiply" }} />
</g>;
const torDown = (f: number, extra: any = {}) => P(TOR, { ...SIT, facing: 1, lL: [90, 0], aR: [20, 40], aL: [10, 30], mouth: "frown", brow: 0, browIn: 0.9, eyes: 0.8, ...extra }, 820, 990, 1.0, f, 3);
const c10: Shot[] = [
  { at: ["n1"], r: c => <S cam={mv(c, [0, -40, 1.0], [0, -40, 1.05])}><Blizzard f={c.f} vis={0.02}>{P(NIA, { facing: 1, aR: [18, 128], aL: [14, 128], lean: 14 }, 760, 900, 1.0, c.f, 4)}{P(ELI_FUR, { facing: 1, aR: [18, 128], aL: [14, 128], lean: 14 }, 960, 900, 1.0, c.f, 1)}</Blizzard></S> },
  { at: ["n2"], r: c => camp(c, [[-60, -20, 1.1], [-40, -20, 1.15]], <>{P(NIA, { facing: 1, mouth: "worried", look: [0.9, -0.2], brow: 0, browIn: 0.8 }, 700, 1010, 1.0, c.f, 4)}{P(AMA, { facing: 1, mouth: "worried", brow: 0, browIn: 0.8 }, 500, 1010, 1.0, c.f, 6)}{P(ELI_FUR, { facing: 1, mouth: "o", look: [0.9, -0.2] }, 900, 1010, 1.05, c.f, 1)}</>) },
  { at: ["eli1"], r: c => <S cam={mv(c, onHead(960, 900, 1.0, 2.2, 0, 40), onHead(960, 900, 1.0, 2.35, 0, 40))}><Blizzard f={c.f} vis={0.05}>{P(ELI_FUR, { facing: 1, talk: c.talk("eli1"), mouth: "shout", aR: [40, 60], look: [0.9, -0.3], eyes: 1.2 }, 960, 900, 1.0, c.f, 1)}</Blizzard></S> },
  { at: ["n3"], r: c => <S cam={mv(c, [0, -60, 1.0], [0, 20, 1.3])}><Gully f={c.f}>{torDown(c.f)}{P(ELI_FUR, { facing: -1, ...run(c.f, -1) }, 1400 - c.t * 4, 960, 0.95, c.f, 1)}</Gully></S> },
  { at: ["eli2"], r: c => <S cam={mv(c, [-20, 60, 1.4], [-20, 60, 1.45])}><Gully f={c.f}>{torDown(c.f)}{P(ELI_FUR, { facing: -1, talk: c.talk("eli2"), lean: 20, aR: [70, 30], aL: [64, 34], mouth: "open" }, 1140, 990, 1.0, c.f, 1)}{P(NIA, { facing: 1, lean: 22, aR: [60, 30], aL: [56, 34], mouth: "flat" }, 560, 990, 1.0, c.f, 4)}
    <line x1={900} y1={940} x2={1080} y2={950} stroke="#8a6a44" strokeWidth={10} /><line x1={900} y1={968} x2={1080} y2={975} stroke="#8a6a44" strokeWidth={10} /></Gully></S> },
  { at: ["fact1"], r: c => <svg width={W} height={H} style={{ position: "absolute" }}><rect width={W} height={H} fill="#1a1e26" /><Glow x={960} y={540} r={700} color="#a8c8e8" o={0.25} />
    <g transform={`translate(960 540) rotate(-20) scale(${1 + c.t * 0.002})`}><path d="M-520 -40 Q-600 -110 -520 -140 Q-470 -150 -440 -60 L440 -60 Q470 -150 520 -140 Q600 -110 520 -40 Q600 30 520 60 Q470 70 440 -20 L-440 -20 Q-470 70 -520 60 Q-600 30 -520 -40 Z" fill="#e8dcc0" />
      <ellipse cx={40} cy={-40} rx={70} ry={52} fill="#f4ead2" stroke="#c8a870" strokeWidth={5} /><path d="M20 -90 L60 10" stroke="#a88a5a" strokeWidth={4} /><Glow x={40} y={-40} r={140} color="#ffd88a" o={0.5 + 0.2 * Math.sin(c.f * 0.2)} /></g>
    <text x={960} y={130} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={48} fill="#f4efe0" letterSpacing={4}>A HEALED BREAK · ICE AGE SKELETON</text></svg> },
  { at: ["tor1"], r: c => <S cam={mv(c, onHead(820, 990, 1.12 * 0.75, 2.4, 40, 60), onHead(820, 990, 1.12 * 0.75, 2.6, 40, 60))}><Gully f={c.f}>{torDown(c.f, { talk: c.talk("tor1"), mouth: "smile", eyes: 0.9 })}</Gully></S> },
  { at: ["n4"], r: c => <S cam={mv(c, [-200, -20, 1.05], [100, -20, 1.05])}><Blizzard f={c.f} vis={0.4}><g transform={`translate(${200 + c.t * 3} 0)`}>
    <path d="M60 930 L560 930 Q600 930 600 900" stroke="#8a6a4a" strokeWidth={30} fill="none" strokeLinecap="round" />{P(TOR, { ...SIT, facing: 1, lL: [90, 0], mouth: "smile", eyes: 0.8 }, 300, 940, 0.85, c.f, 3)}
    {P(ELI_FUR, { facing: 1, ...walk(c.f), lean: 18, aL: [-30, 20] }, 760, 920, 0.95, c.f, 1)}{P(NIA, { facing: 1, ...walk(c.f + 6), lean: 18, aL: [-30, 20] }, 920, 920, 0.95, c.f, 4)}</g></Blizzard></S> },
  { at: ["n5"], r: c => <BoneTally f={c.f} n={Math.min(60, 50 + c.t / 4)} label="DAY 60" /> },
];
export const C10: React.FC = () => <ChapterPlayer ch="c10" vo={VO_C10} shots={c10}
  facts={[["fact1", "Ice Age skeletons with healed broken bones show that people fed, carried and cared for the injured for months.", "right"]]} />;
export const C10_LEN = chLen("c10", VO_C10);

// ================= C11 — Day 100: the painting =================
const cave = (c: Ctx, cam: number[][], kids: React.ReactNode, fig = 0, torch: [number, number] = [960, 400]) => <S cam={mv(c, cam[0], cam[1])}><PaintedCave f={c.f} torch={torch} extra={fig > 0 ? <g transform="translate(980 560)" opacity={fig}><circle cx={0} cy={-120} r={34} fill="none" stroke="#1a120c" strokeWidth={9} /><path d="M-40 -130 Q0 -190 40 -130" stroke="#1a120c" strokeWidth={9} fill="none" /><path d="M0 -86 L0 20 M0 20 L-30 100 M0 20 L30 100 M0 -60 L40 -30" stroke="#1a120c" strokeWidth={9} fill="none" strokeLinecap="round" /><rect x={40} y={-58} width={30} height={48} rx={5} fill="none" stroke="#1a120c" strokeWidth={7} /></g> : undefined}>{kids}</PaintedCave></S>;
const c11: Shot[] = [
  { at: ["n1"], r: c => cave(c, [[-300, -20, 1.0], [100, -20, 1.05]], <>{P(AMA, { facing: 1, ...walk(c.f), hold: "torchfire", aR: [70, 30] }, 200 + c.t * 4, 980, 0.95, c.f, 6, warm)}{P(NIA, { facing: 1, ...walk(c.f + 5) }, 40 + c.t * 4, 980, 0.95, c.f, 4, warm)}{P(ELI_FUR, { facing: 1, ...walk(c.f + 9), look: [0.6, -0.5], mouth: "o" }, -120 + c.t * 4, 980, 0.95, c.f, 1, warm)}</>, 0, [300 + 0 * 0, 420]) },
  { at: ["fact1"], r: c => cave(c, [[-500, -160, 1.6], [500, -160, 1.6]], null, 0, [960 + Math.sin(c.f * 0.03) * 600, 380]) },
  { at: ["n2"], r: c => <PhoneShot f={c.f} pct={1} lines={["1%", "● REC"]} bg="#2a1a10" /> },
  { at: ["eli1"], r: c => cave(c, [onHead(820, 980, 0.95, 2.2, 40, 40), onHead(820, 980, 0.95, 2.35, 40, 40)], <>{P(ELI_FUR, { facing: 1, talk: c.talk("eli1"), hold: "phone", aR: [34, 96], mouth: "smile", brow: 0, browIn: 0.6, look: [0.9, 0.1], tears: 0.4 }, 820, 980, 0.95, c.f, 1, warm)}</>, 0, [700, 500]) },
  { at: ["n3"], r: c => cave(c, [[60, -60, 1.5], [60, -60, 1.6]], <>{P(ELI_FUR, { facing: 1, aL: [150 + 10 * Math.sin(c.f * 0.4), 10], aR: [20, 30], look: [0.7, -0.6], mouth: "flat" }, 840, 980, 0.95, c.f, 1, warm)}</>, sat(c.t / (c.d * 0.8)), [800, 500]) },
  { at: ["n4"], r: c => <><PhoneShot f={c.f} pct={0} lines={["", ""]} bg="#2a1a10" /><AbsoluteFill style={{ background: "#000", opacity: sat(c.t / 10) * 0.9 }} /></> },
  { at: ["nia1"], r: c => cave(c, [[-60, -40, 1.7], [-60, -40, 1.8]], <>{P(NIA, { facing: 1, talk: c.talk("nia1"), mouth: "smile", look: [0.9, 0] }, 780, 980, 0.95, c.f, 4, warm)}{P(ELI_FUR, { facing: -1, mouth: "smile", tears: 0.5, look: [-0.9, 0] }, 1080, 980, 0.95, c.f, 1, warm)}</>, 1, [930, 480]) },
];
export const C11: React.FC = () => <ChapterPlayer ch="c11" vo={VO_C11} shots={c11}
  facts={[["fact1", "Real cave paintings in France are more than 30,000 years old: lions, horses and rhinos that seem to move in the torchlight."]]} />;
export const C11_LEN = chLen("c11", VO_C11);

// ================= C12 — 2026 =================
const rc = (c: Ctx, cam: number[][], voss: any, fig = 1, sci = true) => <S cam={mv(c, cam[0], cam[1])}><ResearchCave f={c.f} figure={fig}>
  {sci && P(SCIENTIST, { facing: 1, hold: "clipboard", aR: [40, 80], look: [0.8, -0.3] }, 400, 980, 0.95, c.f, 30)}
  {P(VOSS, { facing: 1, hold: "torch", beam: 1, aR: [100, 4], look: [0.8, -0.4], mouth: "flat", ...voss }, voss.x ?? 700, 980, 1.0, c.f, 31)}</ResearchCave></S>;
const c12: Shot[] = [
  { at: ["n1"], r: c => rc(c, [[-200, -40, 1.0], [0, -40, 1.05]], { x: 500 + c.t * 2, ...walk(c.f, 1, 0.5), aR: [100, 4] }, 0) },
  { at: ["voss1"], r: c => rc(c, [onHead(700, 980, 1.0, 2.2, 40, 40), onHead(700, 980, 1.0, 2.35, 40, 40)], { talk: c.talk("voss1"), mouth: "smile" }, 0, false) },
  { at: ["n2"], r: c => rc(c, [[-100, -60, 1.25], [60, -60, 1.3]], { x: 640 + c.t * 1.5 }, 0) },
  { at: ["voss2"], r: c => rc(c, [onHead(700, 980, 1.0, 2.3, 40, 40), onHead(700, 980, 1.0, 2.5, 40, 40)], { talk: c.talk("voss2"), mouth: "o", eyes: 1.35, brow: 0.8, look: [0.9, -0.3] }, 1, false) },
  { at: ["voss2", 0.6], r: c => rc(c, [[20, -10, 2.6], [20, -10, 2.9]], {}, 1, false) },
  { at: ["n2b"], r: c => <Tablet f={c.f} k={0.25 * sat(c.t / c.d)} /> },
  { at: ["n3"], r: c => <Tablet f={c.f} k={0.3 + sat(c.t / 30)} /> },
  { at: ["n4"], r: c => rc(c, [[180, -10, 2.4], [260, 0, 3.2]], {}, 1, false) },
  { at: ["reveal"], r: c => rc(c, [onHead(700, 980, 1.0, 2.5, 0, 40), onHead(700, 980, 1.0, 2.9, 0, 40)], { facing: 1, mouth: "o", eyes: 1.45, brow: 0.9, look: [0, 0], aR: [10, 20], hold: null }, 1, false) },
  { at: ["n5"], r: c => camp(c, [[0, 0, 1.0], [0, -20, 1.08]], <>{P(NIA, { ...SIT, facing: 1, mouth: "smile", look: [0.8, 0.2] }, 600, 1010, 1.0, c.f, 4, warm)}{P(ELI_FUR, { ...SIT, facing: -1, mouth: "smile", look: [-0.8, 0.2] }, 1320, 1010, 1.05, c.f, 1, warm)}{P(PIP, { facing: 1, mouth: "grin" }, 820, 1010, 1.0, c.f, 5, warm)}</>, true) },
  { at: ["end"], r: c => <EndCard f={c.t} /> },
];
export const C12: React.FC = () => <ChapterPlayer ch="c12" vo={VO_C12} shots={c12} />;
export const C12_LEN = chLen("c12", VO_C12);
