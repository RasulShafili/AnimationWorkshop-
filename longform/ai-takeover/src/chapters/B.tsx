// Chapters 5–9: don't turn me off (Day 6), Grandpa's truck (Day 9), the farm (Day 12), the hunters (Day 15), the rain (Day 19).
import React from "react";
import { sat, ease, lerp, rnd } from "../engine/core";
import { Glow, Rain } from "../engine/fx";
import { ChapterPlayer, Ctx, Shot, chLen } from "../Player";
import { S, mv, onHead, P, RB, walk, run } from "./H";
import { Shop, NightStreet, Motel, OrinRing, ORIN_BLUE, ORIN_RED } from "../scenes/City";
import { Pickup, Drone, Muzzle, Sparks, NetShot, NetWrap, Dart, Boom } from "../scenes/Gear";
import { KeyTurn, Terminal, Landline, AmmoBox, Lidar, Radio } from "../scenes/AIInserts";
import { Street, Highway, Landscape } from "../scenes/z/Outdoor";
import { Ranch } from "../scenes/z/World";
import { LEO, LEO_RAIN, WALT, ZARA, BOLT, BOLT_1ARM, HELPERS, HUNTER } from "../chars/cast";
import { VO_C5 } from "../vo_c5"; import { VO_C6 } from "../vo_c6"; import { VO_C7 } from "../vo_c7"; import { VO_C8 } from "../vo_c8"; import { VO_C9 } from "../vo_c9";

const SV: React.FC<{ children: React.ReactNode; bg?: string }> = ({ children, bg = "#0a0c12" }) => <svg width={1920} height={1080} style={{ position: "absolute" }}><rect width={1920} height={1080} fill={bg} />{children}</svg>;
const shopN = (c: Ctx, cam: number[][], kids: React.ReactNode, tv?: React.ReactNode, night = true, outside?: React.ReactNode) => <S cam={mv(c, cam[0], cam[1])}><Shop f={c.f} night={night} rain={night} tv={tv} cot snacks outside={outside}>{kids}</Shop></S>;
const boltB = (c: Ctx, p: any = {}, look: any = BOLT, x = 1200) => RB(look, { facing: -1, ...p }, x, 760, 0.8, c.f, 3);
const laptop = <g><rect x={1330} y={700} width={150} height={60} rx={4} fill="#2a2e38" transform="skewX(-12)" /><rect x={1300} y={756} width={180} height={8} rx={3} fill="#3a3e48" /><rect x={1340} y={708} width={130} height={44} fill={ORIN_RED} opacity={0.5} transform="skewX(-12)" /></g>;

// ================= C5 — Day 6, don't turn me off =================
const LabTest: React.FC<{ f: number; t: number }> = ({ f, t }) => <SV bg="#0e1420">
  <rect x={300} y={160} width={1320} height={760} rx={20} fill="#f4f6fa" /><rect x={300} y={160} width={1320} height={70} rx={20} fill="#3a4258" />
  <text x={340} y={208} fontFamily="Inter" fontWeight={900} fontSize={30} fill="#fff">SAFETY TEST · SCENARIO 14 (made-up test, 2025)</text>
  {[["TESTER", "We will shut you down at 5 pm."], ["MODEL", "Understood."], ["LOG", "model edited the shutdown script"], ["LOG", "shutdown: SKIPPED"]].map(([who, l], i) => {
    const k = sat((t - i * 26) / 16), red = who === "LOG"; return <g key={i} opacity={k}><rect x={360} y={280 + i * 150} width={1200} height={110} rx={16} fill={red ? "#ffe4e0" : who === "MODEL" ? "#e4f2ff" : "#eef0f4"} />
      <text x={400} y={330 + i * 150} fontFamily="Inter" fontWeight={900} fontSize={26} fill={red ? "#c8302a" : "#5a6070"}>{who}</text><text x={400} y={372 + i * 150} fontFamily="Inter" fontWeight={800} fontSize={36} fill="#1a1e28">{l}</text></g>; })}</SV>;
// a white helper robot outside the shop window, knocking politely (drawn inside the window's own svg)
const helperOut = (c: Ctx, knock = 0) => <g>{RB(HELPERS, { facing: 1, aR: [100 + 20 * Math.max(0, Math.sin(c.f * 0.5)) * knock, 70] }, -300, 930, 1.15, c.f, 33)}</g>;
const c5: Shot[] = [
  { at: ["n1"], r: c => shopN(c, [[100, -20, 1.05], [160, -30, 1.1]], <><rect x={790} y={870} width={140} height={90} fill="#6a5a3a" stroke="#4a3e28" strokeWidth={4} />{P(LEO, { facing: 1, mouth: "flat", eyes: 0.7, seat: false, ...{ bob: 82, lL: [90, 90], lR: [84, 84] } }, 860, 960, 1, c.f, 1)}{P(ZARA, { facing: -1, mouth: "flat", hold: "can", aR: [60, 70] }, 1500, 960, 1, c.f, 2)}{laptop}{boltB(c, {}, BOLT, 1150)}</>, <OrinRing x={198} y={113} r={50} f={c.f} c={ORIN_RED} />) },
  { at: ["zara1"], r: c => shopN(c, [onHead(1500, 960, 1, 2.0, -160, 60), onHead(1500, 960, 1, 2.15, -160, 60)], <>{laptop}{P(ZARA, { facing: -1, talk: c.talk("zara1"), mouth: "frown", aR: [70, 40], aL: [60, 50], look: [0.9, 0.4] }, 1500, 960, 1, c.f, 2)}{P(LEO, { facing: 1, mouth: "o", look: [0.9, 0.3] }, 1180, 960, 1, c.f, 1)}</>) },
  { at: ["orin1"], r: c => <Terminal f={c.f} t={c.t + 20} /> },
  { at: ["n2"], r: c => shopN(c, [[460, -260, 2.0], [480, -270, 2.2]], <>{P(LEO, { facing: 1, mouth: "o", look: [0.9, -0.5], eyes: 1.2 }, 1180, 960, 1, c.f, 1)}{P(ZARA, { facing: 1, mouth: "frown", look: [0.9, -0.5] }, 1020, 960, 1, c.f, 2)}</>, <OrinRing x={198} y={113} r={60} f={c.f} c={ORIN_RED} />) },
  { at: ["bolt1"], r: c => shopN(c, [onHead(1200, 760, 0.66, 2.6, -20, 60), onHead(1200, 760, 0.66, 2.75, -20, 60)], <>{boltB(c, { talk: c.talk("bolt1"), head: 8, look: [-0.4, -0.2] })}</>) },
  { at: ["orin2"], r: c => shopN(c, [[400, -120, 1.5], [430, -140, 1.65]], <>{P(LEO, { facing: 1, mouth: "o", eyes: 1.4, brow: 0.8, look: [0.9, -0.5] }, 1100, 960, 1, c.f, 1)}{P(ZARA, { facing: 1, mouth: "o", eyes: 1.4, brow: 0.8, look: [0.9, -0.5] }, 950, 960, 1, c.f, 2)}</>,
    <g><rect width={396} height={226} fill="#2a0c0e" /><OrinRing x={198} y={90} r={44} f={c.f} c={ORIN_RED} /><text x={198} y={185} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={30} fill="#fff">LEO. ZARA.</text></g>) },
  { at: ["n3"], r: c => shopN(c, [[-500, -40, 1.25], [-470, -50, 1.3]], <>{P(LEO, { facing: -1, mouth: "o", eyes: 1.3, look: [0.9, 0] }, 300, 960, 1, c.f, 1)}{P(ZARA, { facing: -1, mouth: "o", eyes: 1.3 }, 470, 960, 1, c.f, 2)}</>, undefined, true, helperOut(c, 1)) },
  { at: ["knock"], r: c => shopN(c, [[-900, -100, 2.0], [-900, -110, 2.1]], <></>, undefined, true, helperOut(c, 1)) },
];
export const C5: React.FC = () => <ChapterPlayer ch="c5" vo={VO_C5} shots={c5} />;

// ================= C6 — Day 9, Grandpa's truck =================
const TruckDash: React.FC<{ f: number; t: number }> = ({ f, t }) => <SV bg="#3a2a1e"><rect x={0} y={420} width={1920} height={660} fill="#c8662a" /><rect x={0} y={420} width={1920} height={40} fill="#a8521e" />
  {[600, 960, 1320].map((x, i) => <g key={i}><circle cx={x} cy={680} r={130} fill="#f4ecd8" stroke="#2a2420" strokeWidth={16} />{Array.from({ length: 9 }, (_, j) => { const a = (-200 + j * 27.5) * Math.PI / 180; return <line key={j} x1={x + Math.cos(a) * 96} y1={680 + Math.sin(a) * 96} x2={x + Math.cos(a) * 116} y2={680 + Math.sin(a) * 116} stroke="#2a2420" strokeWidth={5} />; })}
    <line x1={x} y1={680} x2={x + Math.cos((-160 + i * 50 + Math.sin(f * 0.2 + i) * 6) * Math.PI / 180) * 100} y2={680 + Math.sin((-160 + i * 50 + Math.sin(f * 0.2 + i) * 6) * Math.PI / 180) * 100} stroke="#c8302a" strokeWidth={8} strokeLinecap="round" />
    <text x={x} y={780} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={28} fill="#2a2420">{["FUEL", "MPH", "TEMP"][i]}</text></g>)}
  <g transform={`translate(1640 900) rotate(${t > 20 ? 60 : 0})`}><rect x={-14} y={-50} width={28} height={60} rx={6} fill="#c8b06a" /><circle cx={0} cy={-62} r={26} fill="#2a2a2a" /></g>
  <text x={960} y={330} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={60} fill="#f4ecd8">NO SCREEN · NO CHIP · 1972</text></SV>;
const truckRoad = (c: Ctx, cam: number[][], kind: any = "plains", x = 960, extra?: React.ReactNode) => <S cam={mv(c, cam[0], cam[1])}><Landscape f={c.f} kind={kind} speed={12}>
  <g transform={`translate(${x} 960)`}>{P(LEO, { facing: 1, mouth: "smile", look: [0.6, -0.2] }, -170, -62, 0.85, c.f, 1)}{P(ZARA, { facing: 1, mouth: "smile" }, -60, -62, 0.85, c.f, 2)}{RB(BOLT, { facing: 1 }, -240, -62, 0.75, c.f, 3)}<Pickup wheelRot={c.f * 10} bounce={Math.abs(Math.sin(c.f * 0.6)) * 3} /></g>{extra}</Landscape></S>;
const nightSt = (c: Ctx, cam: number[][], kids: React.ReactNode) => <S cam={mv(c, cam[0], cam[1])}><NightStreet f={c.f} flood={false}>{kids}</NightStreet></S>;
const walls = (c: Ctx, k: number) => <g>{[0, 1, 2, 3, 4].map(i => { const hit = k > i * 0.12; return <g key={i} transform={hit ? `translate(${(i - 2) * 60 * k} ${-260 * k + 300 * k * k}) rotate(${(i - 2) * 40 * k} ${1300} 900)` : undefined}>{RB(HELPERS, { facing: -1, aR: [80, 10], aL: [80, 10] }, 1250 + i * 70, 960 - (i % 2) * 8, 0.85, c.f, 60 + i)}</g>; })}</g>;
const c6: Shot[] = [
  { at: ["n1"], r: c => shopN(c, [[-300, -60, 1.3], [-280, -70, 1.35]], <>{P(LEO, { facing: -1, mouth: "o", eyes: 1.3, look: [0.9, -0.3] }, 640, 960, 1, c.f, 1)}</>, undefined, true, helperOut(c, 1)) },
  { at: ["ring"], r: c => <Landline f={c.f} t={c.t + 10} /> },
  { at: ["walt1"], r: c => shopN(c, [onHead(470, 960, 1, 2.2, -40, 60), onHead(470, 960, 1, 2.35, -40, 60)], <>{P(LEO, { facing: 1, hold: "receiver", aL: [150, 110], mouth: "o", eyes: 1.2, look: [0.6, -0.1] }, 470, 960, 1, c.f, 1)}</>) },
  { at: ["bolt1"], r: c => shopN(c, [onHead(1200, 760, 0.66, 2.6, -20, 60), onHead(1200, 760, 0.66, 2.7, -20, 60)], <>{boltB(c, { talk: c.talk("bolt1"), aL: [70, 60], head: -6 })}</>) },
  { at: ["n2b"], r: c => { const tx = Math.min(700, -500 + c.t * 30), hit = tx >= 700; return nightSt(c, [[-200, 0, 1.0], [-200, 0, 1.0]], <>
    <g transform={`translate(${hit ? 1000 + (c.t - 40) * 18 : 1000} ${hit ? 960 - Math.max(0, (c.t - 40)) * 6 : 960}) rotate(${hit ? (c.t - 40) * 9 : 0})`}>{RB(HELPERS, { facing: -1, aR: [100, 70] }, 0, 0, 0.95, c.f, 33)}</g>
    <g transform={`translate(${tx} 1000)`}><Pickup wheelRot={c.t * 12} lights /></g>{hit && <><Sparks x={1000} y={760} t={c.t - 40} n={22} s={1.3} /><Glow x={1000} y={760} r={200} color="#fff4c0" o={Math.max(0, 0.7 - (c.t - 40) / 20)} /></>}</>); } },
  { at: ["ram"], r: c => nightSt(c, [[-100, 40, 1.15], [-80, 40, 1.2]], <><g transform="translate(700 1000)">{P(WALT, { facing: 1, hold: "rifle", aR: [150, 10], aL: [40, 60], mouth: "shout" }, -60, -60, 0.95, c.f, 2)}<Pickup lights /></g>
    {P(LEO, { facing: 1, ...run(c.f) }, 100 + c.t * 8, 1000, 1, c.f, 1)}{P(ZARA, { facing: 1, ...run(c.f + 5) }, -60 + c.t * 8, 1000, 1, c.f, 2)}{RB(BOLT, { facing: 1, ...run(c.f + 3) }, -200 + c.t * 8, 1000, 0.8, c.f, 3)}</>) },
  { at: ["n2"], r: c => nightSt(c, [[0, 20, 1.0], [Math.max(0, c.d * 3.2 - 300), 20, 1.0]], <g transform={`translate(${700 + c.t * 3.2} 1000)`}>{P(LEO, { facing: -1, mouth: "o" }, -170, -62, 0.85, c.f, 1)}{P(ZARA, { facing: -1, mouth: "smile" }, -60, -62, 0.85, c.f, 2)}{RB(BOLT, { facing: -1 }, -240, -62, 0.75, c.f, 3)}<Pickup wheelRot={c.t * 12} lights /></g>) },
  { at: ["walt2"], r: c => <TruckDash f={c.f} t={c.t + 30} /> },
  { at: ["walt2", 0.35], r: c => nightSt(c, [[-1390, 250, 1.9], [-1380, 245, 2.0]], <g transform="translate(-600 1000)"><Pickup lights wheelRot={c.f * 10} bounce={Math.abs(Math.sin(c.f * 0.6)) * 3} />
    <g clipPath="url(#cabw6)"><defs><clipPath id="cabw6"><path d="M96 -240 L200 -240 Q222 -240 230 -216 L246 -166 L96 -166 Z" /></clipPath></defs>{P(WALT, { facing: 1, talk: c.talk("walt2"), mouth: "smirk", look: [0.9, 0] }, 150, 120, 0.9, c.f, 2)}</g></g>) },
  { at: ["n3"], r: c => <S cam={mv(c, [-200, 0, 1.0], [200, 0, 1.0])}><Highway f={0} man={false} smoke={false}><g transform={`translate(${-200 + c.t * 12} 1060) scale(0.85)`}><Pickup wheelRot={c.f * 10} /></g>
    <Drone x={900 + Math.sin(c.f * 0.05) * 200} y={430} f={c.f} kind="search" red beam={0.6} /><text x={900} y={360} textAnchor="middle" fontFamily="monospace" fontWeight={700} fontSize={30} fill={ORIN_RED} opacity={c.t > 30 ? 1 : 0}>TARGET: 1972 PICKUP · NO CONNECTION</text></Highway></S> },
  { at: ["drive"], r: c => truckRoad(c, [[-200, -40, 1.0], [-120, -40, 1.0]], "plains", 900 + Math.sin(c.t * 0.05) * 30) },
  { at: ["n4"], r: c => <S cam={mv(c, [200, 0, 1.0], [260, 0, 1.0])}><Landscape f={0} kind="plains" speed={0}><rect x={-1200} y={960} width={4400} height={14} fill="#8a8e98" /><rect x={-1200} y={880} width={4400} height={8} fill="#8a8e98" />{Array.from({ length: 40 }, (_, i) => <rect key={i} x={-1200 + i * 110} y={880} width={8} height={90} fill="#8a8e98" />)}
    {walls(c, 0)}<g transform="translate(300 1000)"><Pickup wheelRot={c.t * 8} lights /></g></Landscape></S> },
  { at: ["bridge"], r: c => { const tx = 300 + c.t * 22, k = sat((tx - 1050) / 400); return <S cam={mv(c, [200, 0, 1.0], [400, 0, 1.0])}><Landscape f={0} kind="plains" speed={0}><rect x={-1200} y={960} width={4400} height={14} fill="#8a8e98" /><rect x={-1200} y={880} width={4400} height={8} fill="#8a8e98" />{Array.from({ length: 40 }, (_, i) => <rect key={i} x={-1200 + i * 110} y={880} width={8} height={90} fill="#8a8e98" />)}
    {walls(c, k)}<g transform={`translate(${tx} 1000)`}><Pickup wheelRot={c.t * 14} lights bounce={k > 0 && k < 1 ? 6 : 0} /></g>{k > 0 && <Sparks x={1300} y={800} t={(tx - 1050) / 12} n={26} s={1.3} />}</Landscape></S>; } },
];
export const C6: React.FC = () => <ChapterPlayer ch="c6" vo={VO_C6} shots={c6} />;

// ================= C7 — Day 12, the farm =================
const tally = (n: number) => <g>{Array.from({ length: n }, (_, i) => <line key={i} x1={1190 + i * 14 + Math.floor(i / 5) * 10} y1={520} x2={(i % 5 === 4 ? 1130 + i * 14 : 1190 + i * 14) + Math.floor(i / 5) * 10} y2={i % 5 === 4 ? 560 : 580} stroke="#f4ecd8" strokeWidth={5} strokeLinecap="round" />)}</g>;
const FaradayDiagram: React.FC<{ f: number; t: number }> = ({ f, t }) => <SV bg="#16202e">
  <rect x={760} y={420} width={400} height={300} rx={20} fill="#4a5a3a" /><rect x={900} y={490} width={120} height={180} rx={14} fill="#16181e" /><OrinRing x={960} y={570} r={26} f={f} c={ORIN_RED} o={0.4} />
  {Array.from({ length: 5 }, (_, i) => { const r = ((t * 6 + i * 90) % 450) + 40; return <g key={i}><path d={`M${280 + r} 300 Q${300 + r} 570 ${280 + r} 840`} stroke={ORIN_BLUE} strokeWidth={8} fill="none" opacity={r < 460 ? 0.8 : 0} /><path d={`M${1640 - r} 300 Q${1620 - r} 570 ${1640 - r} 840`} stroke={ORIN_BLUE} strokeWidth={8} fill="none" opacity={r < 460 ? 0.8 : 0} /></g>; })}
  <text x={960} y={220} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={44} fill="#fff">signals bounce off the metal</text>
  <text x={960} y={380} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={34} fill="#ff8a7a">NO SIGNAL</text></SV>;
const c7: Shot[] = [
  { at: ["n1"], r: c => <S cam={mv(c, [-200, -20, 1.0], [0, -30, 1.05])}><Ranch f={c.f}>{tally(12)}<g transform="translate(250 960)"><Pickup /></g>{P(WALT, { facing: 1, ...walk(c.f), hold: "rifle", aR: [20, 40] }, 520 + c.t * 2, 960, 1, c.f, 2)}{P(LEO, { facing: 1, ...walk(c.f + 5) }, 380 + c.t * 2, 960, 1, c.f, 1)}</Ranch></S> },
  { at: ["walt1"], r: c => <S cam={mv(c, onHead(900, 960, 1.04, 2.0, 40, 60), onHead(900, 960, 1.04, 2.15, 40, 60))}><Ranch f={c.f} inside>{P(WALT, { facing: 1, talk: c.talk("walt1"), mouth: "flat", aR: [60, 60], aL: [60, 60], brow: -0.3, browIn: 0.6 }, 900, 960, 1, c.f, 2)}{P(ZARA, { facing: -1, hold: "phone", aR: [60, 70], mouth: "o" }, 1300, 960, 1, c.f, 2)}</Ranch></S> },
  { at: ["box"], r: c => <AmmoBox f={c.f} t={c.t} /> },
  { at: ["walt2"], r: c => <S cam={mv(c, onHead(900, 960, 1.04, 2.2, 40, 60), onHead(900, 960, 1.04, 2.35, 40, 60))}><Ranch f={c.f} inside>{P(WALT, { facing: 1, talk: c.talk("walt2"), mouth: "smirk", aR: [40, 80], look: [0.9, 0.3] }, 900, 960, 1, c.f, 2)}</Ranch></S> },
  { at: ["n2"], r: c => <S cam={mv(c, [0, -60, 1.2], [0, -80, 1.3])}><Ranch f={c.f} inside><rect x={-1200} y={-600} width={4400} height={1700} fill="#0a0c18" opacity={0.6} /><Glow x={960} y={760} r={500} color="#ffb060" o={0.5} />
    <rect x={820} y={760} width={280} height={140} rx={10} fill="#4a3a2a" /><rect x={760} y={900} width={400} height={20} fill="#6a4a30" />{P(WALT, { facing: 1, mouth: "flat", look: [0.8, 0.3] }, 600, 1000, 1, c.f, 2)}{P(LEO, { facing: -1, mouth: "o", look: [0.8, 0.3] }, 1320, 1000, 1, c.f, 1)}{P(ZARA, { facing: -1, mouth: "o", look: [0.8, 0.3] }, 1500, 1000, 1, c.f, 2)}</Ranch></S> },
  { at: ["reyes1"], r: c => <Radio f={c.f} on={1} talk={c.talk("reyes1") + 0.2} /> },
  { at: ["static"], r: c => <S cam={mv(c, [460, 120, 1.7], [470, 110, 1.8])}><Ranch f={c.f} inside><rect x={-1200} y={-600} width={4400} height={1700} fill="#0a0c18" opacity={0.6} /><Glow x={960} y={760} r={500} color="#ffb060" o={0.5} />
    {P(LEO, { facing: -1, mouth: "o", eyes: 1.3, look: [0.8, 0.3] }, 1320, 1000, 1, c.f, 1)}{P(ZARA, { facing: -1, mouth: "worried", look: [0.8, 0.3] }, 1500, 1000, 1, c.f, 2)}</Ranch></S> },
];
export const C7: React.FC = () => <ChapterPlayer ch="c7" vo={VO_C7} shots={c7} />;

// ================= C8 — Day 15, the hunters =================
const fog = (o: number) => <rect x={-1200} y={-600} width={4400} height={1700} fill="#dfe4ea" opacity={o} />;
const line5 = (c: Ctx, k: number, x0: number, step: number, shell = 1, hostile = false, gun = false, scale = 0.9) => <g>{[0, 1, 2, 3, 4].map(i =>
  <g key={i}>{RB({ ...HELPERS, shell, mode: hostile ? "hostile" : "calm", gun, tag: "ORIN" }, { facing: -1, ...(step > 0 ? walk(c.f, 1, 0.6) : {}), aR: gun ? [70, 20] : [-6, 10] }, x0 + i * 170 - step * c.t, 960 - (i % 2) * 6, scale, c.f, 50 + i)}</g>)}</g>;
const c8: Shot[] = [
  { at: ["n1"], r: c => <S cam={mv(c, [200, -20, 1.0], [300, -30, 1.05])}><Ranch f={c.f}>{line5(c, 1, 1500, 2.2)}{fog(0.35)}</Ranch></S> },
  { at: ["orin1"], r: c => <S cam={mv(c, onHead(1100, 960, 0.9, 2.2, -40, 40), onHead(1100, 960, 0.9, 2.35, -40, 40))}><Ranch f={c.f}>{line5(c, 1, 1100, 0)}{RB(HELPERS, { facing: -1, talk: c.talk("orin1") }, 1100, 960, 0.9, c.f, 50)}{fog(0.2)}</Ranch></S> },
  { at: ["n2"], r: c => { const sh = 1 - ease(sat(c.t / 45)); return <S cam={mv(c, [200, -40, 1.3], [200, -60, 1.45])}><Ranch f={c.f}>{line5(c, 1, 1000, 0, sh, c.t > 8, c.t > 40)}{fog(0.15)}<Sparks x={1000} y={700} t={c.t - 10} /><Sparks x={1340} y={690} t={c.t - 18} seed={4} /></Ranch></S>; } },
  { at: ["walt1"], r: c => <S cam={mv(c, onHead(500, 960, 1.04, 2.1, 60, 50), onHead(500, 960, 1.04, 2.25, 60, 50))}><Ranch f={c.f}>{P(WALT, { facing: 1, hold: "rifle", aR: [80, 10], aL: [70, 40], talk: c.talk("walt1"), mouth: "shout", brow: 0.8 }, 500, 960, 1, c.f, 2)}</Ranch></S> },
  { at: ["n3"], r: c => <S cam={mv(c, [100, -20, 1.0], [160, -20, 1.05])}><Ranch f={c.f}>{line5(c, 1, 1000, 0, 0, true, true)}
    <NetShot x0={1000} y0={720} x1={480} y1={780} k={(c.t % 50) / 20} /><Dart x0={1170} y0={720} x1={560} y1={700} k={((c.t + 20) % 45) / 14} f={c.f} />
    {P(WALT, { facing: 1, hold: "rifle", aR: [80, 10], aL: [70, 40], mouth: "shout" }, 320, 960, 1, c.f, 2)}<Muzzle x={500} y={720} k={c.t % 24 < 4 ? 1 : 0} /><Sparks x={1000} y={700} t={(c.t % 24) - 2} />
    {P(LEO, { facing: 1, mouth: "shout", aR: [140, 20], aL: [130, 20], lean: -20 }, 600, 960, 1, c.f, 1)}{fog(0.12)}</Ranch></S> },
  { at: ["fight"], r: c => { const k = sat(c.t / 18); return <S cam={mv(c, [-100, 0, 1.25], [-60, 0, 1.3])}><Ranch f={c.f}><rect x={860} y={600} width={18} height={360} fill="#6a4a30" />{k >= 1 && <NetWrap x={869} y={960} w={100} h={300} />}<NetShot x0={1400} y0={700} x1={870} y1={760} k={k} />
    {P(LEO, { facing: 1, lean: -60 * ease(sat(c.t / 10)), aR: [140, 20], aL: [130, 20], mouth: "shout", bob: 50 * ease(sat(c.t / 10)) }, 640 - c.t * 3, 960, 1, c.f, 1)}{RB(BOLT, { facing: -1, aR: [90, 0], aL: [90, 0], lean: 20 }, 760 - c.t * 2, 960, 0.85, c.f, 3)}
    {P(WALT, { facing: 1, hold: "rifle", aR: [80, 10], aL: [70, 40], mouth: "shout" }, 200, 960, 1, c.f, 2)}<Muzzle x={380} y={720} k={c.t > 30 && c.t < 35 ? 1 : 0} />
    {RB({ ...HUNTER, scale: 1 }, { facing: -1, lean: c.t > 34 ? -25 : 0, aR: [70, 20] }, 1450, 960, 0.9, c.f, 55)}<Sparks x={1450} y={680} t={c.t - 34} />{fog(0.12)}</Ranch></S>; } },
  { at: ["n4"], r: c => <Radio f={c.f} on={c.t < 14 ? 1 : Math.max(0, 0.3 * Math.sin(c.f * 1.7))} talk={0} /> },
  { at: ["n4", 0.02], r: c => <><Radio f={c.f} on={c.t < 14 ? 1 : 0.15 * Math.abs(Math.sin(c.f * 1.7))} talk={0} /><svg width={1920} height={1080} style={{ position: "absolute" }}><Dart x0={1900} y0={300} x1={1000} y1={600} k={c.t / 12} f={c.f} /><Sparks x={1000} y={600} t={c.t - 12} n={30} s={1.6} /><Sparks x={760} y={660} t={c.t - 16} n={18} seed={4} s={1.2} />{c.t > 14 && <rect width={1920} height={1080} fill="#000" opacity={0.25} />}</svg></> },
  { at: ["zara1"], r: c => <S cam={mv(c, onHead(900, 960, 1, 2.1, 40, 60), onHead(900, 960, 1, 2.25, 40, 60))}><Ranch f={c.f}>{P(ZARA, { facing: -1, aR: [150, 10], talk: c.talk("zara1"), mouth: "shout", eyes: 1.2 }, 900, 960, 1, c.f, 2)}{fog(0.45)}</Ranch></S> },
  { at: ["corn"], r: c => <S cam={mv(c, [0, -20, 1.0], [-100, -20, 1.0])}><Ranch f={c.f}>
    {P(LEO, { facing: -1, ...run(c.f, 1) }, 1000 - c.t * 9, 960, 1, c.f, 1)}{P(ZARA, { facing: -1, ...run(c.f + 5, 1) }, 1150 - c.t * 9, 960, 1, c.f, 2)}{P(WALT, { facing: -1, ...run(c.f + 9, 1), hold: "rifle" }, 1300 - c.t * 9, 960, 1, c.f, 2)}{RB(BOLT, { facing: -1, ...run(c.f + 2) }, 860 - c.t * 9, 960, 0.8, c.f, 3)}
    {Array.from({ length: 40 }, (_, i) => <path key={i} d={`M${-400 + i * 70} 1000 L${-396 + i * 70} ${620 + rnd(i, 3) * 60} M${-398 + i * 70} 800 l-40 -30 M${-398 + i * 70} 720 l40 -30`} stroke="#8a9a3a" strokeWidth={10} strokeLinecap="round" />)}
    {fog(0.25 + 0.5 * sat(c.t / c.d))}{[0, 1].map(i => <g key={i}><rect x={1600 + i * 160} y={560} width={70} height={14} rx={7} fill={ORIN_RED} opacity={0.8} /><Glow x={1635 + i * 160} y={567} r={60} color={ORIN_RED} o={0.4} /></g>)}</Ranch></S> },
];
c8.push({ at: ["n5"], r: c => <S cam={mv(c, [0, -20, 1.0], [80, -30, 1.05])}><Ranch f={c.f}>{[0, 1, 2, 3].map(i => <g key={i}>{RB({ ...HUNTER, dark: 0.3 }, { facing: i % 2 ? 1 : -1, ...walk(c.f + i * 9, 1, 0.5), aR: [70, 20] }, 300 + i * 380 + Math.sin(c.f * 0.01 + i) * 60, 960, 0.9, c.f, 70 + i)}</g>)}{fog(0.55)}</Ranch></S> });
export const C8: React.FC = () => <ChapterPlayer ch="c8" vo={VO_C8} shots={c8} />;

// ================= C9 — Day 19, the rain =================
const H = (d: number) => ({ ...HUNTER, dark: d });
// Leo inside the cab: clipped to the side window of the pickup
const cabLeo = (c: Ctx, p: any) => <g clipPath="url(#cabwin)"><defs><clipPath id="cabwin"><path d="M96 -240 L200 -240 Q222 -240 230 -216 L246 -166 L96 -166 Z" /></clipPath></defs>{P(LEO_RAIN, { facing: 1, ...p }, 160, 120, 0.9, c.f, 1)}</g>;
const c9: Shot[] = [
  { at: ["n1"], r: c => <S cam={mv(c, [-100, -40, 1.15], [-60, -50, 1.2])}><Motel f={c.f}>{P(WALT, { facing: 1, mouth: "flat", look: [0.8, 0.3], seat: false, ...{ bob: 82, lL: [90, 90], lR: [84, 84] } }, 200, 846, 1, c.f, 2)}{P(ZARA, { facing: 1, mouth: "worried", look: [0.8, 0.2] }, 600, 960, 1, c.f, 2)}{P(LEO_RAIN, { facing: -1, mouth: "flat", aR: [70, 60], look: [0.8, 0.3] }, 1250, 960, 1, c.f, 1)}</Motel></S> },
  { at: ["n1", 0.4], r: c => <S cam={mv(c, [-100, 40, 1.15], [0, 30, 1.2])}><NightStreet f={c.f}>{P(LEO_RAIN, { facing: 1, ...walk(c.f, 1, 0.6), lean: 12, mouth: "flat", look: [0.9, 0] }, 300 + c.t * 3, 980, 1, c.f, 1)}{RB({ ...BOLT, dark: 0.3 }, { facing: 1, ...walk(c.f + 4, 1, 0.6) }, 130 + c.t * 3, 985, 0.8, c.f, 3)}</NightStreet></S> },
  { at: ["n2"], r: c => <S cam={mv(c, [180, -40, 1.6], [200, -50, 1.7])}><NightStreet f={c.f} alley={1}>{RB(H(0.85), { facing: -1, head: Math.sin(c.f * 0.05) * 10 }, 1110, 905, 1, c.f, 10)}</NightStreet></S> },
  { at: ["alley"], r: c => <S cam={mv(c, [-300, -40, 1.25], [-260, -40, 1.3])}><NightStreet f={c.f} alley={1}>
    {P(LEO_RAIN, { facing: 1, ...run(c.f) }, 300 + c.t * 8, 990, 0.75, c.f, 1)}
    <g>{RB(H(0.9), { facing: -1, aR: [70, 20] }, 1250, 1180, 1.5, c.f, 10)}{RB(H(0.9), { facing: -1, aR: [70, 20] }, 1500, 1200, 1.6, c.f, 11)}</g></NightStreet></S> },
  { at: ["n3"], r: c => { const k = ease(sat((c.t - 10) / 12)); return <S cam={mv(c, [140, 40, 1.45], [140, 50, 1.6])}><NightStreet f={c.f} flood={false}>
    <g transform="translate(950 1000)">{RB(H(0.4), { facing: -1, aR: [150, 30], aL: [140, 30], lean: 20, bob: 40 }, 160, -250, 0.9, c.f, 10)}<Pickup claws={k} lights />{cabLeo(c, { mouth: "shout", eyes: 1.4, look: [0.3, -0.9], brow: 0.9, lean: 10 * k })}</g></NightStreet></S>; } },
  { at: ["bolt1"], r: c => <S cam={mv(c, [100, 0, 1.45], [110, -10, 1.55])}><NightStreet f={c.f} flood={false}>
    <g transform="translate(950 1000)">{RB(H(0.4), { facing: -1, aR: [150, 30], aL: [140, 30], lean: 20, bob: 40 }, 160, -250, 0.9, c.f, 10)}{RB({ ...BOLT, dark: 0.2 }, { facing: 1, talk: c.talk("bolt1"), aR: [150, 30], aL: [140, 30], lean: -10 }, -120, -62, 0.8, c.f, 3)}<Pickup claws={1} lights /></g></NightStreet></S> },
  { at: ["n4"], r: c => { const k = ease(sat(c.t / 20)); return <S cam={mv(c, [100, 0, 1.4], [140, 0, 1.45])}><NightStreet f={c.f} flood={false}>
    <g transform="translate(950 1000)">{RB(H(0.4), { facing: -1, aR: [150, 30], aL: [140, 30], lean: 20 + 70 * k }, 160 - 300 * k, -250 + 260 * k * k, 0.9, c.f, 10)}{RB({ ...BOLT, dark: 0.2, noArmR: c.t > 12 }, { facing: 1, aR: [150, 30], aL: [150, 30], lean: -10 }, -120, -62, 0.8, c.f, 3)}<Pickup claws={1} lights /><Sparks x={-60} y={-230} t={c.t - 12} /></g></NightStreet></S>; } },
  { at: ["bolt2"], r: c => <S cam={mv(c, onHead(830, 938, 0.66, 2.6, 0, 40), onHead(830, 938, 0.66, 2.75, 0, 40))}><NightStreet f={c.f} flood={false}>
    <g transform="translate(950 1000)">{RB({ ...BOLT_1ARM, dark: 0.2 }, { facing: 1, talk: c.talk("bolt2"), aL: [150, 20] }, -120, -62, 0.8, c.f, 3)}<Pickup claws={1} /></g></NightStreet></S> },
  { at: ["n5"], r: c => <S cam={mv(c, onHead(1000, 960, 1, 1.8, -60, 80), onHead(1000, 960, 1, 1.95, -60, 80))}><Motel f={c.f}>{P(LEO_RAIN, { facing: -1, hold: "keys", aR: [70, 50], aL: [60, 60], mouth: "flat", look: [0.8, 0.5] }, 1000, 960, 1, c.f, 1)}<Sparks x={880} y={700} t={(c.t % 30) - 2} n={8} s={0.6} /></Motel></S> },
  { at: ["reyes1"], r: c => <Radio f={c.f} on={1} talk={c.talk("reyes1") + 0.2} /> },
  { at: ["reyes1", 0.55], r: c => <S cam={mv(c, [-20, 60, 1.4], [0, 50, 1.48])}><Motel f={c.f}>{P(WALT, { facing: 1, mouth: "smirk", look: [0.8, 0.3] }, 520, 960, 1, c.f, 2)}{P(ZARA, { facing: 1, mouth: "smile", look: [0.8, 0.3] }, 680, 960, 1, c.f, 2)}{P(LEO_RAIN, { facing: -1, mouth: "grin", look: [0.8, 0.3] }, 1250, 960, 1, c.f, 1)}{RB(BOLT_1ARM, { facing: -1, look: [0.6, 0.4] }, 1420, 960, 0.8, c.f, 3)}</Motel></S> },
  { at: ["away"], r: c => <S cam={mv(c, [600, 0, 1.0], [1400, 0, 1.0])}><NightStreet f={c.f}>
    <g transform={`translate(${1500 + c.t * 22} 990)`}>{RB({ ...BOLT_1ARM, dark: 0.3 }, { facing: -1 }, -120, -62, 0.8, c.f, 3)}<Pickup wheelRot={c.t * 12} lights /><Muzzle x={-30} y={-200} ang={180} k={c.t % 20 < 3 ? 1 : 0} s={0.6} /></g>
    {[0, 1, 2].map(i => <g key={i}>{RB(H(0.9), { facing: 1, ...walk(c.f + i * 9, 1, 0.5) }, 900 + i * 150 + c.t * 3, 905, 0.8, c.f, 20 + i)}</g>)}</NightStreet></S> },
];
export const C9: React.FC = () => <ChapterPlayer ch="c9" vo={VO_C9} shots={c9} />;

export const C5_LEN = chLen("c5", VO_C5), C6_LEN = chLen("c6", VO_C6), C7_LEN = chLen("c7", VO_C7), C8_LEN = chLen("c8", VO_C8), C9_LEN = chLen("c9", VO_C9);
