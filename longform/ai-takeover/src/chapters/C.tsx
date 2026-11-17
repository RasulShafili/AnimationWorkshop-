// Chapters 10–14: the resistance (Day 22), the assault (Day 27), the switch (Day 30), after, the cliffhanger.
import React from "react";
import { sat, ease, lerp, rnd } from "../engine/core";
import { Glow } from "../engine/fx";
import { ChapterPlayer, Ctx, Shot, chLen } from "../Player";
import { S, mv, onHead, P, RB, walk, run } from "./H";
import { Shop, CityWide, DataCenter, ServerHall, Tunnel, OrinRing, ORIN_BLUE, ORIN_RED } from "../scenes/City";
import { Pickup, CAB_CLIP, BED_Y, Humvee, Drone, Muzzle, Sparks, NetShot, Boom } from "../scenes/Gear";
import { AIM, COVER, PORT, muzzle } from "../chars/Rig2";
import { robotAim } from "../chars/Robot";
import { MapPlan, RobotsViz, HomeScreens, VisorText, EndCard } from "../scenes/AIInserts";
import { Street } from "../scenes/z/Outdoor";
import { LEO, WALT, ZARA, REYES, SOLDIERS, EXTRAS, PIKE, PIKE_DAUGHTER, RAINCOAT_GIRL, OKAFOR_EGG, LINA_EGG, BOLT, BOLT_1ARM, HUNTER } from "../chars/cast";
import { VO_C10 } from "../vo_c10"; import { VO_C11 } from "../vo_c11"; import { VO_C12 } from "../vo_c12"; import { VO_C13 } from "../vo_c13"; import { VO_C14 } from "../vo_c14";

const SV: React.FC<{ children: React.ReactNode; bg?: string }> = ({ children, bg = "#0a0c12" }) => <svg width={1920} height={1080} style={{ position: "absolute" }}><rect width={1920} height={1080} fill={bg} />{children}</svg>;
const SIT = { bob: 82, lL: [90, 90], lR: [84, 84] };
const OFF = { eye: "#0b0e14" };   // Bolt powered down

// ================= C10 — Day 22, the resistance =================
const table = <g><rect x={700} y={820} width={520} height={26} fill="#6a5a3a" /><rect x={720} y={846} width={18} height={150} fill="#4a3e28" /><rect x={1182} y={846} width={18} height={150} fill="#4a3e28" /><rect x={760} y={800} width={400} height={22} fill="#e8d8b0" transform="rotate(-2 960 810)" /></g>;
const crowd = (c: Ctx) => <g>
  {P(SOLDIERS[0], { facing: 1, ...SIT, ...PORT, mouth: "flat", seat: false }, -120, 1000, 1, c.f, 21)}
  {P(EXTRAS[3], { facing: 1, mouth: "smile", aR: [40, 50] }, 160, 1000, 1, c.f, 22)}
  {P(OKAFOR_EGG, { facing: 1, hold: "cup", aR: [70, 60], mouth: "flat", eyes: 0.7 }, 380, 1000, 1, c.f, 23)}
  {P(LINA_EGG, { facing: -1, hold: "map", aR: [70, 50], mouth: "smile" }, 1440, 1000, 1, c.f, 24)}
  {P(SOLDIERS[1], { facing: -1, ...PORT, mouth: "flat" }, 1700, 1000, 1, c.f, 25)}
  {P(EXTRAS[5], { facing: -1, mouth: "flat" }, 1940, 1000, 1, c.f, 26)}{P(SOLDIERS[3], { facing: 1, ...PORT }, 2160, 1000, 1, c.f, 27)}</g>;
const c10: Shot[] = [
  { at: ["n1"], r: c => <S cam={mv(c, [-200, -40, 1.0], [200, -40, 1.0])}><Tunnel f={c.f} back={<g transform="translate(960 720) scale(0.45)"><Humvee f={c.f} /></g>}>{crowd(c)}</Tunnel></S> },
  { at: ["n1", 0.5], r: c => <S cam={mv(c, [-100, -20, 1.2], [0, -30, 1.25])}><Tunnel f={c.f}>{crowd(c)}{P(LEO, { facing: 1, ...walk(c.f), mouth: "o", look: [0.6, -0.2] }, 560 + c.t * 2, 1000, 1, c.f, 1)}{P(ZARA, { facing: 1, ...walk(c.f + 5) }, 420 + c.t * 2, 1000, 1, c.f, 2)}{P(WALT, { facing: 1, ...walk(c.f + 9), ...PORT }, 760 + c.t * 2, 1000, 1, c.f, 2)}{RB(BOLT_1ARM, { facing: 1, ...walk(c.f + 3) }, 300 + c.t * 2, 1000, 0.8, c.f, 3)}</Tunnel></S> },
  { at: ["reyes1"], r: c => <S cam={mv(c, onHead(960, 1000, 1.02, 2.0, 40, 70), onHead(960, 1000, 1.02, 2.15, 40, 70))}><Tunnel f={c.f}>{P(REYES, { facing: 1, talk: c.talk("reyes1"), mouth: "flat", aR: [60, 70], aL: [50, 70], look: [0.6, 0.4] }, 960, 1000, 1, c.f, 4)}{table}</Tunnel></S> },
  { at: ["reyes1", 0.45], r: c => <MapPlan f={c.f} t={c.t} /> },

  { at: ["zara1"], r: c => <S cam={mv(c, onHead(1300, 1000, 1, 2.0, -60, 70), onHead(1300, 1000, 1, 2.15, -60, 70))}><Tunnel f={c.f}>{table}{P(ZARA, { facing: -1, talk: c.talk("zara1"), mouth: "smirk", aR: [80, 30], look: [0.8, 0.4] }, 1300, 1000, 1, c.f, 2)}{P(REYES, { facing: 1, mouth: "flat", look: [0.9, 0] }, 620, 1000, 1, c.f, 4)}</Tunnel></S> },
  { at: ["reyes2"], r: c => <S cam={mv(c, onHead(960, 1000, 1.02, 2.0, 40, 70), onHead(960, 1000, 1.02, 2.12, 40, 70))}><Tunnel f={c.f}>{P(REYES, { facing: 1, talk: c.talk("reyes2"), mouth: "flat", aR: [80, 30], look: [0.6, 0.4], brow: -0.3, browIn: 0.6 }, 960, 1000, 1, c.f, 4)}{table}</Tunnel></S> },
  { at: ["bolt1"], r: c => <S cam={mv(c, [100, -40, 1.25], [120, -50, 1.3])}><Tunnel f={c.f}>{table}{P(REYES, { facing: 1, mouth: "o", look: [0.9, 0.1] }, 620, 1000, 1, c.f, 4)}{P(ZARA, { facing: -1, mouth: "o", look: [0.9, 0.2] }, 1400, 1000, 1, c.f, 2)}{P(LEO, { facing: -1, mouth: "smile", look: [0.9, 0.3] }, 1560, 1000, 1, c.f, 1)}
    {RB(BOLT_1ARM, { facing: 1, talk: c.talk("bolt1"), aL: [160, 10] }, 1060, 1000, 0.85, c.f, 3)}</Tunnel></S> },
  { at: ["walt1"], r: c => <S cam={mv(c, onHead(760, 1000, 1.04, 1.9, 60, 70), onHead(760, 1000, 1.04, 2.2, 60, 70))}><Tunnel f={c.f}>{table}{P(WALT, { facing: 1, ...PORT, talk: c.talk("walt1"), mouth: "smirk", brow: -0.4 }, 760, 1000, 1, c.f, 2)}{P(LEO, { facing: -1, mouth: "smile" }, 1180, 1000, 1, c.f, 1)}</Tunnel></S> },
];
c10.push({ at: ["gear"], r: c => <S cam={mv(c, [-200, -20, 1.1], [100, -20, 1.1])}><Tunnel f={c.f} back={<g transform="translate(960 720) scale(0.45)"><Humvee f={c.f} /></g>}>{SOLDIERS.map((so, i) => <g key={i}>{P(so, { facing: i % 2 ? -1 : 1, ...PORT, mouth: "flat" }, -200 + i * 420, 1000, 1, c.f, 30 + i)}</g>)}
  {P(WALT, { facing: 1, ...PORT, mouth: "smirk" }, 760, 1000, 1, c.f, 2)}{P(LEO, { facing: 1, ...walk(c.f), mouth: "flat" }, 400 + c.t * 3, 1000, 1, c.f, 1)}</Tunnel></S> });
export const C10: React.FC = () => <ChapterPlayer ch="c10" vo={VO_C10} shots={c10} />;

// ================= C11 — Day 27, the assault =================
// soldiers aim level from behind the sandbags; the flash sits exactly on each muzzle (muzzle() uses s × look.scale)
const squad = (c: Ctx, fire: boolean) => <g>{SOLDIERS.map((s, i) => { const x = -480 + i * 150, y = 1000 + (i % 2) * 20, [mx, my] = muzzle(x, y, 0.95 * (s.scale ?? 1), 1);
  return <g key={i}>{P(s, { facing: 1, ...AIM, mouth: fire ? "shout" : "flat" }, x, y, 0.95, c.f, 30 + i)}
  {fire && <Muzzle x={mx} y={my} k={(c.f + i * 5) % 14 < 3 ? 1 : 0} s={0.6} />}</g>; })}</g>;
const horde = (c: Ctx, n: number, step: number) => <g>{Array.from({ length: n }, (_, i) => { const x = 700 + (i % 8) * 170 + rnd(i, 3) * 60 - step * c.t, y = 860 + Math.floor(i / 8) * 18;
  const sc = 0.5 + Math.floor(i / 8) * 0.06, w = walk(c.f + i * 5, 1, 0.5);   // gun arms aimed at the soldiers' line
  return <g key={i}>{RB({ ...HUNTER, dark: 0.55 + 0.1 * (i % 3), gun: true }, { facing: -1, lL: w.lL, lR: w.lR, aR: robotAim(x, y, sc * 1.12, -1, -300, 780).aR }, x, y, sc, c.f, 60 + i)}</g>; })}</g>;
const hordeTip = (i: number, step: number, t: number) => { const x = 700 + (i % 8) * 170 + rnd(i, 3) * 60 - step * t, y = 860 + Math.floor(i / 8) * 18; return robotAim(x, y, (0.5 + Math.floor(i / 8) * 0.06) * 1.12, -1, -300, 780).tip; };
const Corridor: React.FC<{ f: number; children?: React.ReactNode }> = ({ f, children }) => <g><rect x={-1200} y={-600} width={4400} height={1700} fill="#dfe6ee" />
  <path d="M-1200 -200 L960 420 L3200 -200 Z" fill="#c8d2de" /><path d="M-1200 1300 L960 420 L3200 1300 Z" fill="#b8c2ce" />
  {Array.from({ length: 6 }, (_, i) => { const z = Math.pow(1 - i / 6, 1.5); return <rect key={i} x={960 - 1300 * z} y={420 - 480 * z} width={2600 * z} height={6} fill={ORIN_BLUE} opacity={0.5} />; })}
  <rect x={880} y={330} width={160} height={180} fill="#9aa8b8" /><circle cx={1030} cy={420} r={8} fill={ORIN_RED} opacity={f % 30 < 15 ? 1 : 0.3} />
  <text x={960} y={300} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={30} fill="#5a6a7a" letterSpacing={4}>CORE · ROW 2026</text>{children}</g>;
const c11: Shot[] = [
  { at: ["n1"], r: c => <S cam={mv(c, [0, -60, 1.0], [0, -40, 1.12])}><DataCenter f={c.f} /></S> },
  { at: ["n1", 0.5], r: c => <S cam={mv(c, [-500, 40, 1.05], [-440, 30, 1.1])}><DataCenter f={c.f} fight={1}>{squad(c, false)}</DataCenter></S> },
  { at: ["reyes1"], r: c => <S cam={mv(c, onHead(-200, 1000, 1.02, 2.0, 60, 60), onHead(-200, 1000, 1.02, 2.2, 60, 60))}><DataCenter f={c.f} fight={1}>{P(REYES, { facing: 1, ...PORT, talk: c.talk("reyes1"), mouth: "shout", brow: 0.6 }, -200, 1000, 1, c.f, 4)}
    <g transform={`translate(${200 + c.t * 4} ${700 - c.t * 9})`}><circle r={12} fill="#ffe8b0" /><Glow x={0} y={0} r={90} color="#ffb04a" o={0.8} /></g></DataCenter></S> },
  { at: ["fire"], r: c => <S cam={mv(c, [-200, 0, 1.0], [-100, 0, 1.0])}><DataCenter f={c.f} fight={1}>{horde(c, 24, 1.5)}{squad(c, true)}
    {[0, 1, 2, 3].map(i => { const t0 = i * 14, tt = c.t - t0; return <g key={i}><Drone x={500 + i * 300} y={200 + i * 40 + Math.max(0, tt) * Math.max(0, tt) * 0.08} f={c.f} kind="search" red tilt={tt > 0 ? tt * 3 : 0} />{tt > 0 && tt < 20 && <Sparks x={500 + i * 300} y={200 + i * 40} t={tt} />}</g>; })}
    <Boom x={1300} y={760} t={c.t - 30} s={1.3} />{(() => { const tp = hordeTip(1, 1.5, c.t); return <NetShot x0={tp[0]} y0={tp[1]} x1={-300} y1={800} k={(c.t % 40) / 22} s={0.7} />; })()}</DataCenter></S> },
  { at: ["n2"], r: c => <S cam={mv(c, [-260, 140, 1.6], [-240, 130, 1.7])}><DataCenter f={c.f} fight={1}>{horde(c, 16, 1)}{squad(c, true)}<Sparks x={720} y={760} t={(c.t % 20)} seed={3} /><Sparks x={880} y={770} t={((c.t + 9) % 20)} seed={6} /></DataCenter></S> },
  { at: ["n2", 0.55], r: c => <S cam={mv(c, [300, -140, 1.4], [340, -160, 1.45])}><DataCenter f={c.f} fight={1}>{horde(c, 24, 2)}<Boom x={1100} y={720} t={c.t - 8} s={1.6} /><Drone x={1400} y={400 + c.t * 4} f={c.f} kind="search" red tilt={c.t * 2} /><Sparks x={1400} y={400} t={c.t - 4} /></DataCenter></S> },
  { at: ["walt1"], r: c => <S cam={mv(c, [-1254, 100, 1.6], [-1244, 95, 1.7])}><DataCenter f={c.f}><g transform="translate(-600 1000)"><Pickup lights wheelRot={c.f * 10} bounce={Math.abs(Math.sin(c.f)) * 4} />
    <g clipPath="url(#cabw2)"><defs><clipPath id="cabw2"><path d={CAB_CLIP} /></clipPath></defs>{P(WALT, { facing: 1, talk: c.talk("walt1"), mouth: "shout", brow: 0.8, eyes: 1.2 }, 280, -26, 0.95, c.f, 2)}</g></g></DataCenter></S> },
  { at: ["ram"], r: c => { const tx = Math.min(1250, -500 + c.t * 40), hit = tx > 840; return <S cam={mv(c, [-200, 60, 1.05], [80, 60, 1.05])}><DataCenter f={c.f} gate={hit ? ease(sat((tx - 840) / 200)) : 0}>{horde(c, 8, 0)}
    <g transform={`translate(${tx} 900) scale(0.6)`}><Pickup wheelRot={c.t * 14} lights bounce={hit ? 6 : 0} /></g>{hit && <><Sparks x={960} y={790} t={(tx - 840) / 10} n={24} s={1.3} /><Glow x={960} y={790} r={260} color="#fff4c0" o={Math.max(0, 0.8 - (tx - 840) / 300)} /></>}</DataCenter></S>; } },
  { at: ["n3"], r: c => <S cam={mv(c, [200, 40, 1.15], [500, 40, 1.15])}><DataCenter f={c.f} gate={1}>{horde(c, 10, -1)}<g transform={`translate(${1250 + c.t * 14} 900) scale(0.6)`}><Pickup wheelRot={c.t * 14} lights /></g></DataCenter></S> },
  { at: ["walt2"], r: c => <S cam={mv(c, onHead(760, 1000, 1.04, 1.9, 120, 60), onHead(760, 1000, 1.04, 2.05, 120, 60))}><DataCenter f={c.f} fight={0}><rect x={560} y={480} width={420} height={520} fill="#dfe6ee" /><rect x={600} y={520} width={340} height={480} fill="#c8d2de" />
    {P(WALT, { facing: -1, ...AIM, talk: c.talk("walt2"), mouth: "shout", brow: -0.4, browIn: 0.8 }, 760, 1000, 1, c.f, 2)}</DataCenter></S> },
  { at: ["hold"], r: c => <S cam={mv(c, [-300, 40, 1.15], [-260, 40, 1.2])}><DataCenter f={c.f}><rect x={160} y={480} width={420} height={520} fill="#dfe6ee" /><rect x={200} y={520} width={340} height={480} fill="#c8d2de" />
    {[0, 1, 2].map(i => <g key={i}>{RB({ ...HUNTER, dark: 0.45 }, { facing: -1, ...walk(c.f + i * 8, 1, 0.6), aR: [70, 20], lean: (c.t % 24) < 4 && i === (Math.floor(c.t / 24) % 3) ? -20 : 0 }, 1100 + i * 220 - c.t * 2, 1000 - i * 8, 0.95, c.f, 80 + i)}</g>)}
    {P(WALT, { facing: 1, ...AIM, mouth: "shout", brow: -0.4, browIn: 0.8 }, 420, 1000, 1, c.f, 2)}<Muzzle x={420 + 218} y={1000 - 308} k={(c.t % 24) < 4 ? 1 : 0} /><Sparks x={1100 + (Math.floor(c.t / 24) % 3) * 220 - c.t * 2} y={700} t={c.t % 24} /></DataCenter></S> },
  { at: ["n4"], r: c => <S cam={mv(c, [0, 0, 1.0], [0, -20, 1.1])}><Corridor f={c.f}>{RB({ ...BOLT_1ARM, mode: "scan" }, { facing: 1, ...run(c.f) }, 300 + c.t * 6, 1000, 0.85, c.f, 3)}{P(LEO, { facing: 1, ...run(c.f + 4) }, 100 + c.t * 6, 1000, 1, c.f, 1)}{P(ZARA, { facing: 1, ...run(c.f + 8) }, -80 + c.t * 6, 1000, 1, c.f, 2)}</Corridor></S> },
  { at: ["bolt1"], r: c => <S cam={mv(c, onHead(960, 1000, 0.7, 2.4, 0, 60), onHead(960, 1000, 0.7, 2.6, 0, 60))}><Corridor f={c.f}>{RB(BOLT_1ARM, { facing: 1, talk: c.talk("bolt1"), head: -8, look: [-0.3, -0.4] }, 960, 1000, 0.85, c.f, 3)}</Corridor></S> },
];
export const C11: React.FC = () => <ChapterPlayer ch="c11" vo={VO_C11} shots={c11} />;

// ================= C12 — Day 30, the switch =================
const Lever: React.FC<{ f: number; k: number }> = ({ f, k }) => <SV bg="#0a0c12"><Glow x={960} y={540} r={700} color={k > 0.95 ? "#000" : ORIN_BLUE} o={0.25 * (1 - k)} />
  <rect x={700} y={300} width={520} height={640} rx={30} fill="#3a3e48" stroke="#ffd34a" strokeWidth={12} strokeDasharray="40 24" /><rect x={930} y={380} width={60} height={420} rx={20} fill="#16181e" />
  <g transform={`rotate(${lerp(-35, 45, ease(k))} 960 760)`}><rect x={935} y={380} width={50} height={380} rx={18} fill="#d83a2a" /><rect x={860} y={330} width={200} height={80} rx={30} fill="#e8402e" />
    <path d="M840 300 Q960 250 1080 300 L1100 420 Q960 460 820 420 Z" fill="#f4ccb0" /><path d="M1080 300 L1500 160 L1600 400 L1100 420 Z" fill="#3f8a4e" /></g>
  <text x={960} y={1010} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={44} fill="#ffd34a">MAIN</text></SV>;
const blackout = (c: Ctx, k: number) => <S cam={mv(c, [0, -20, 1.0], [0, -20, 1.0])}><CityWide f={c.f} mode="locked" drones={0.6} /><rect x={-1200} y={-600} width={4400 * k} height={1700} fill="#000" opacity={0.92} /></S>;
const c12: Shot[] = [
  { at: ["n1"], r: c => { const red = c.t > c.d * 0.6 && c.t < c.d * 0.75; return <S cam={mv(c, [80, -40, 1.4], [100, -60, 1.5])}><Corridor f={c.f}><rect x={1100} y={600} width={40} height={60} rx={6} fill="#3a3e48" /><circle cx={1120} cy={620} r={7} fill={ORIN_BLUE} />
    {RB({ ...BOLT_1ARM, mode: red ? "hostile" : "calm" }, { facing: 1, aL: [80, 10], lean: 6 }, 980, 1000, 0.85, c.f, 3)}{P(LEO, { facing: 1, mouth: "worried", brow: 0, browIn: 0.8 }, 700, 1000, 1, c.f, 1)}
    {red && <Glow x={1060} y={560} r={200} color={ORIN_RED} o={0.4} />}</Corridor></S>; } },
  { at: ["orin1"], r: c => <S cam={mv(c, [0, 40, 1.0], [0, 20, 1.12])}><ServerHall f={c.f}><OrinRing x={960} y={300} r={90} f={c.f} o={0.6 + 0.4 * c.talk("orin1")} />{P(LEO, { facing: 1, mouth: "o", look: [0.6, -0.6] }, 640, 1040, 1.05, c.f, 1)}{RB(BOLT_1ARM, { facing: 1, look: [0.5, -0.6] }, 1240, 1040, 0.9, c.f, 3)}</ServerHall></S> },
  { at: ["n2"], r: c => <SV bg="#05070c"><g transform={`translate(960 540) scale(${1 + c.t * 0.0015}) translate(-960 -540)`}><HomeScreens f={c.f} /></g></SV> },
  { at: ["bolt2"], r: c => <S cam={mv(c, onHead(1240, 1040, 0.74, 2.5, -40, 60), onHead(1240, 1040, 0.74, 2.7, -40, 60))}><ServerHall f={c.f}>{RB({ ...BOLT_1ARM, mode: c.f % 10 < 5 ? "hostile" : "calm" }, { facing: -1, talk: c.talk("bolt2"), head: 10 * Math.sin(c.f * 0.9), lean: 6 * Math.sin(c.f * 0.7) }, 1240, 1040, 0.9, c.f, 3)}<Glow x={1240} y={760} r={260} color={ORIN_RED} o={0.25 + 0.2 * Math.sin(c.f)} /></ServerHall></S> },
  { at: ["bolt1"], r: c => <S cam={mv(c, onHead(1240, 1040, 0.74, 2.4, -40, 60), onHead(1240, 1040, 0.74, 2.55, -40, 60))}><ServerHall f={c.f}>{RB(BOLT_1ARM, { facing: -1, talk: c.talk("bolt1"), head: 6 }, 1240, 1040, 0.9, c.f, 3)}</ServerHall></S> },
  { at: ["leo1"], r: c => <S cam={mv(c, onHead(640, 1040, 1.05, 2.3, 60, 60), onHead(640, 1040, 1.05, 2.45, 60, 60))}><ServerHall f={c.f}>{P(LEO, { facing: 1, talk: c.talk("leo1"), mouth: "sad", tears: 0.6, brow: 0, browIn: 0.9, eyes: 0.9 }, 640, 1040, 1.05, c.f, 1)}</ServerHall></S> },
  { at: ["pull"], r: c => <Lever f={c.f} k={sat((c.t - 18) / 14)} /> },
  { at: ["n3"], r: c => <S cam={mv(c, [0, 20, 1.05], [0, 20, 1.08])}><ServerHall f={c.f} off={sat(c.t / (c.d * 0.8))} handle={1}>{P(LEO, { facing: 1, mouth: "sad", look: [0.9, 0] }, 760, 1040, 1.05, c.f, 1)}{RB({ ...BOLT_1ARM, ...(c.t > c.d * 0.7 ? OFF : {}) }, { facing: -1, eyes: Math.max(0.1, 1 - sat((c.t - c.d * 0.5) / (c.d * 0.2))), head: 14 * sat((c.t - c.d * 0.6) / 20), lean: 10 * sat((c.t - c.d * 0.6) / 20) }, 1100, 1040, 0.9, c.f, 3)}</ServerHall></S> },
  { at: ["dark"], r: c => blackout(c, ease(sat(c.t / 50))) },
];
export const C12: React.FC = () => <ChapterPlayer ch="c12" vo={VO_C12} shots={c12} />;

// ================= C13 — after =================
const c13: Shot[] = [
  { at: ["n1"], r: c => <S cam={mv(c, [0, 60, 1.0], [0, -40, 1.0])}><CityWide f={c.f} mode="dark">{[0, 1, 2, 3, 4, 5].map(i => <g key={i}>{P(EXTRAS[i], { facing: i % 2 ? -1 : 1, look: [0.3, -1], mouth: "o", aR: i === 2 ? [150, 10] : [-6, 10] }, 200 + i * 300, 1000, 0.9, c.f, 40 + i)}</g>)}<rect x={-1200} y={700} width={4400} height={700} fill="#02040a" opacity={0.45} /></CityWide></S> },
  { at: ["n1", 0.55], r: c => <S cam={mv(c, [-100, 0, 1.0], [-80, -60, 1.05])}><CityWide f={c.f} mode="dark">{P(PIKE, { facing: 1, aR: [60, 70], mouth: "smile", look: [0.3, -0.9] }, 640, 1000, 1, c.f, 5)}{P(PIKE_DAUGHTER, { facing: -1, aR: [60, 70], mouth: "smile", look: [0.3, -0.9] }, 820, 1000, 1, c.f, 6)}{P(RAINCOAT_GIRL, { facing: 1, aR: [160, 10], mouth: "grin", look: [0.3, -1] }, 1100, 1000, 0.9, c.f, 7)}<rect x={-1200} y={700} width={4400} height={700} fill="#02040a" opacity={0.35} /></CityWide></S> },
  { at: ["stars"], r: c => <S cam={mv(c, [0, 0, 1.0], [0, -160, 1.0])}><CityWide f={c.f} mode="dark" /></S> },
  { at: ["n2"], r: c => <S cam={mv(c, [0, 40, 1.1], [0, 20, 1.2])}><DataCenter f={c.f} lights={0}><rect x={-1200} y={-600} width={4400} height={1350} fill="#ffb070" opacity={0.35} /><Glow x={960} y={700} r={900} color="#ffb060" o={0.4} />
    {P(WALT, { facing: -1, ...PORT, ...walk(c.f, 1, 0.4), lean: 6 + 4 * Math.sin(c.f * 0.3), mouth: "smirk" }, 1300 - c.t * 2, 1000, 1, c.f, 2)}{P(LEO, { facing: 1, ...run(c.f) }, 200 + c.t * 7, 1000, 1, c.f, 1)}{P(ZARA, { facing: 1, ...run(c.f + 5) }, 60 + c.t * 7, 1000, 1, c.f, 2)}</DataCenter></S> },
  { at: ["walt1"], r: c => <S cam={mv(c, onHead(900, 1000, 1.04, 1.9, 40, 60), onHead(900, 1000, 1.04, 2.05, 40, 60))}><CityWide f={c.f} mode="dawn"><g transform="translate(1500 1010)"><Pickup /></g>
    {P(WALT, { facing: 1, talk: c.talk("walt1"), mouth: "smirk", ...PORT, look: [0.5, -0.2] }, 900, 1000, 1, c.f, 2)}{P(REYES, { facing: -1, mouth: "smile", look: [0.4, -0.2] }, 1300, 1000, 1, c.f, 4)}</CityWide></S> },
  { at: ["zara1"], r: c => <S cam={mv(c, [-80, -10, 1.35], [-60, -20, 1.42])}><CityWide f={c.f} mode="dawn">{P(ZARA, { facing: 1, talk: c.talk("zara1"), mouth: "smile", look: [0.6, 0.3] }, 760, 1000, 1, c.f, 2)}
    {P(LEO, { facing: -1, mouth: "sad", look: [0.6, 0.5], aR: [60, 70], aL: [60, 70] }, 1080, 1000, 1, c.f, 1)}{RB({ ...BOLT_1ARM, ...OFF }, { facing: -1, eyes: 0.1, head: 18, lean: 8 }, 1180, 1000, 0.8, c.f, 3)}</CityWide></S> },
];
export const C13: React.FC = () => <ChapterPlayer ch="c13" vo={VO_C13} shots={c13} />;

// ================= C14 — cliffhanger =================
const c14: Shot[] = [
  { at: ["n1"], r: c => <S cam={mv(c, [100, -40, 1.1], [160, -50, 1.16])}><Shop f={c.f}>{RB({ ...BOLT_1ARM, ...OFF }, { facing: -1, eyes: 0.1, head: 10 }, 1200, 760, 0.8, c.f, 3)}{P(LEO, { facing: c.t > c.d * 0.55 ? -1 : 1, mouth: "sad", ...(c.t > c.d * 0.55 ? walk(c.f, 1, 0.5) : {}) }, c.t > c.d * 0.55 ? 960 - (c.t - c.d * 0.55) * 5 : 960, 960, 1, c.f, 1)}
    <rect x={-1200} y={-600} width={4400} height={1700} fill="#05070c" opacity={0.7 * sat((c.t - c.d * 0.8) / 20)} /></Shop></S> },
  { at: ["n2"], r: c => { const blue = c.t > 30 && c.t < 60 && c.f % 8 < 5, red = c.t > 70; return <S cam={mv(c, onHead(1200, 760, 0.66, 2.6, -20, 60), onHead(1200, 760, 0.66, 2.9, -20, 60))}><Shop f={c.f}>
    {RB({ ...BOLT_1ARM, ...(red ? { mode: "hostile" as const } : blue ? {} : OFF) }, { facing: -1, eyes: red || blue ? 1 : 0.1, head: 10 }, 1200, 760, 0.8, c.f, 3)}<rect x={-1200} y={-600} width={4400} height={1700} fill="#05070c" opacity={0.7} />
    {(red || blue) && <Glow x={1180} y={540} r={240} color={red ? ORIN_RED : ORIN_BLUE} o={0.5} />}</Shop></S>; } },
  { at: ["orin1"], r: c => <VisorText f={c.f} t={c.t + 30} look={BOLT_1ARM} text="BACKUP 1 OF 9" /> },
  { at: ["n3"], r: c => <EndCard f={c.t}><g transform="translate(0 0)">{P(LEO, { facing: 1, mouth: "smile" }, 640, 860, 1, c.f, 1)}{P(ZARA, { facing: 1, mouth: "smile" }, 820, 860, 1, c.f, 2)}{P(WALT, { facing: -1, ...PORT, mouth: "smirk" }, 1080, 860, 1, c.f, 2)}{RB({ ...BOLT_1ARM, mode: "hostile" }, { facing: -1 }, 1280, 860, 0.8, c.f, 3)}</g></EndCard> },
];
export const C14: React.FC = () => <ChapterPlayer ch="c14" vo={VO_C14} shots={c14} />;

export const C10_LEN = chLen("c10", VO_C10), C11_LEN = chLen("c11", VO_C11), C12_LEN = chLen("c12", VO_C12), C13_LEN = chLen("c13", VO_C13), C14_LEN = chLen("c14", VO_C14);
