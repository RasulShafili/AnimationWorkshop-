// Chapters 11–15: the radio, the cost, the road north, the safe zone, tent 48 + part 2 + end card.
import React from "react";
import { AbsoluteFill } from "remotion";
import { camAt, sat, ease, easeOut, lerp, rnd, W, H } from "../engine/core";
import { Glow, Shaft } from "../engine/fx";
import { Noise, AO } from "../engine/tex";
import { ChapterPlayer, Ctx, Shot, chLen } from "../Player";
import { StoreAisle, Crowd, P } from "../scenes/Store";
import { USMap, Bat, Ranch } from "../scenes/World";
import { Lot, BoxTruck, Cab, Crossroads, Landscape, Checkpoint, TentCity } from "../scenes/Outdoor";
import { RadioBench, Density, Sleeve, Badge, Notebook, Part2, EndCard } from "../scenes/Inserts";
import { DockDoor } from "../scenes/Store";
import { KAI, KAI_PACK, MIRA, RUIZ, DANA, HOLT, ZOMBIES, zombiePose } from "../chars/cast";
import { Character, runPose, walkPose } from "../chars/Rig2";
import { S, mv, onHead, Big } from "./A";
import { VO_C11 } from "../vo_c11"; import { VO_C12 } from "../vo_c12"; import { VO_C13 } from "../vo_c13"; import { VO_C14 } from "../vo_c14"; import { VO_C15 } from "../vo_c15";

const run = (f: number, dir: 1 | -1 = 1) => runPose(f * 0.38 * dir, 1);
const walk = (f: number, dir: 1 | -1 = 1, amp = 1) => walkPose(f * 0.14 * dir, amp);
const SV: React.FC<{ children: React.ReactNode; bg?: string }> = ({ children, bg = "#0a0c12" }) => <svg width={W} height={H} style={{ position: "absolute" }}><rect width={W} height={H} fill={bg} />{children}</svg>;

// ================= C11 — Day 14: the radio =================
const Iono: React.FC<{ f: number }> = ({ f }) => <SV bg="#04060e">
  {Array.from({ length: 80 }, (_, i) => <circle key={i} cx={rnd(i, 1) * W} cy={rnd(i, 2) * 500} r={1.5} fill="#fff" opacity={0.7} />)}
  <path d="M-200 1300 Q960 700 2120 1300" fill="#0e2a1e" stroke="#2a6a4a" strokeWidth={4} />
  <path d="M-200 520 Q960 120 2120 520" fill="none" stroke="#6a8aff" strokeWidth={30} opacity={0.25} /><text x={960} y={250} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={30} fill="#8aa8ff" letterSpacing={6}>IONOSPHERE</text>
  {/* station far away (left) → bounce → your radio (right) */}
  <g transform="translate(330 1000)"><path d="M-30 0 L0 -140 L30 0" stroke="#c8c8d0" strokeWidth={6} fill="none" /><circle cx={0} cy={-140} r={8} fill="#ff4a3a" /></g>
  <g transform="translate(1590 1000)"><rect x={-40} y={-50} width={80} height={50} rx={6} fill="#4a3a2e" /><rect x={10} y={-42} width={24} height={14} fill="#ffd86a" /></g>
  {(() => { const k = (f % 70) / 70; const pts = [[330, 860], [960, 330], [1590, 950]]; const seg = k < 0.5 ? 0 : 1, u = (k % 0.5) * 2; const [a, b] = [pts[seg], pts[seg + 1]];
    return <><path d="M330 860 L960 330 L1590 950" stroke="#ffd86a" strokeWidth={5} fill="none" strokeDasharray="18 14" opacity={0.6} /><circle cx={lerp(a[0], b[0], u)} cy={lerp(a[1], b[1], u)} r={16} fill="#ffd86a" /><Glow x={lerp(a[0], b[0], u)} y={lerp(a[1], b[1], u)} r={70} color="#ffd86a" o={0.6} /></>; })()}
  <text x={330} y={1060} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={26} fill="#c8d0e0">STATION · 800 MILES AWAY</text><text x={1590} y={1060} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={26} fill="#ffd86a">YOUR RADIO</text>
</SV>;
const Doc: React.FC<{ f: number }> = ({ f }) => <SV bg="#1a1612">
  <g transform={`translate(960 560) rotate(-3) scale(${1 + f * 0.0012})`}><rect x={-520} y={-470} width={1040} height={940} fill="#f2ecdc" /><Noise x={-520} y={-470} w={1040} h={940} freq={0.7} o={0.25} />
    <text x={0} y={-370} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={30} fill="#3a3a3a" letterSpacing={6}>U.S. STRATEGIC COMMAND</text>
    <text x={0} y={-270} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={84} fill="#1a1a1a">CONPLAN 8888-11</text>
    <text x={0} y={-190} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={48} fill="#1a1a1a">"COUNTER-ZOMBIE DOMINANCE"</text>
    {Array.from({ length: 9 }, (_, i) => <rect key={i} x={-430} y={-100 + i * 50} width={860 - (i % 3) * 120} height={16} fill="#8a8a84" />)}
    <g transform="translate(240 320) rotate(-14)" opacity={sat((f - 20) / 8)}><rect x={-230} y={-60} width={460} height={120} fill="none" stroke="#c8282a" strokeWidth={10} /><text x={0} y={22} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={56} fill="#c8282a">TRAINING · 2011</text></g></g>
</SV>;
const bench = (c: Ctx, cam: number[][], on: number, kai: any, group = false) => <S cam={camAt(c.t, [[0, ...cam[0]], [c.d, ...cam[1]]])}><RadioBench f={c.f} on={on}>
  {group && <>{P(RUIZ, { facing: 1, mouth: "flat", look: [0.8, 0.3] }, 280, 1000, 1.1, c.f, 3, "#ffd86a")}{P(DANA, { facing: -1, mouth: "o", look: [-0.7, 0.3] }, 1500, 1000, 1.1, c.f, 4, "#ffd86a")}{P(MIRA, { facing: -1, mouth: "o", look: [-0.7, 0.2], hold: "walkie", aR: [20, 50] }, 1330, 1000, 1.1, c.f, 2, "#ffd86a")}</>}
  {P(KAI, { facing: 1, aR: [70, 40], look: [0.6, 0.4], ...kai }, 760, 1000, 1.15, c.f, 1, "#ffd86a")}</RadioBench></S>;
const c11: Shot[] = [
  { at: ["n1"], r: c => <S cam={mv(c, [-100, -40, 1.15], [60, -40, 1.2])}><StoreAisle f={c.f} light="dark" empty={0.75}>{P(KAI, { facing: 1, ...walk(c.f), hold: "torch", beam: 1, aR: [80, 6] }, 500 + c.t * 3.2, 980, 1.15, c.f, 1)}</StoreAisle></S> },
  { at: ["n1", 0.55], r: c => bench(c, [[-100, -40, 1.2], [-80, -40, 1.25]], 0, { mouth: "flat", brow: 0.2 }) },
  { at: ["fact1"], r: c => <Iono f={c.t} /> },
  { at: ["static"], r: c => bench(c, [[150, -150, 2.6], [150, -150, 2.8]], c.t % 9 < 4 ? 1 : 0.2, {}) },
  { at: ["holt1"], r: c => bench(c, [[-20, -40, 1.1], [-20, -40, 1.15]], 1, { mouth: "o", eyes: 1.2, brow: 0.6 }, true) },
  { at: ["holt1", 0.55], r: c => <USMap f={c.f} spread={0.85} safe={sat(c.t / 30)} /> },
  { at: ["fact2"], r: c => <Doc f={c.t} /> },
  { at: ["fact3"], r: c => <USMap f={c.f} spread={0.6 + 0.4 * sat(c.t / c.d)} safe={1} label="CITIES FALL FIRST" /> },
  { at: ["kai1"], r: c => bench(c, [onHead(760, 1000, 1.15, 2.3, 40, 30), onHead(760, 1000, 1.15, 2.45, 40, 30)], 1, { talk: c.talk("kai1"), brow: 0, browIn: 0.7, look: [-0.6, 0.1], facing: -1, aR: [20, 30] }) },
  { at: ["ruiz1"], r: c => bench(c, [onHead(280, 1000, 1.1 * 1.06, 2.2, 80, 30), onHead(280, 1000, 1.1 * 1.06, 2.35, 80, 30)], 1, {}, true) },
  { at: ["n2"], r: c => <S cam={mv(c, [200, -40, 1.1], [300, -60, 1.3])}><Lot f={c.f} zombies={8}><g transform="translate(1250 980)"><BoxTruck /></g>
    <g opacity={sat((c.t - 20) / 10)}><path d="M300 1000 L1240 1000" stroke="#ffd86a" strokeWidth={4} strokeDasharray="20 14" /><text x={770} y={980} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={40} fill="#ffd86a">40 M</text></g></Lot></S> },
];
// fix the Ruiz close-up: he talks in it
c11[9] = { at: ["ruiz1"], r: c => <S cam={mv(c, onHead(280, 1000, 1.1 * 1.06, 2.2, 80, 30), onHead(280, 1000, 1.1 * 1.06, 2.35, 80, 30))}><RadioBench f={c.f} on={1}>{P(RUIZ, { facing: 1, talk: c.talk("ruiz1"), mouth: "flat", brow: 0.2, look: [0.8, 0.2] }, 280, 1000, 1.1, c.f, 3, "#ffd86a")}</RadioBench></S> };
export const C11: React.FC = () => <ChapterPlayer ch="c11" vo={VO_C11} shots={c11} days={[["n1", "DAY 14", "11:40 P.M.", 110]]}
  facts={[["fact1", "At night, AM radio waves bounce off the upper atmosphere, so a station hundreds of miles away can come through clearly."],
    ["fact2", "CONPLAN 8888 (2011): a real U.S. military training plan, written for a zombie attack.", "right"],
    ["fact3", "Cornell University (2015) simulated a U.S. zombie outbreak: cities fall first, the empty northern Rockies are safest."]]} />;
export const C11_LEN = chLen("c11", VO_C11);

// ================= C12 — Day 21: the cost =================
const team = (f: number, x: number, mode: "sneak" | "run" | "stand", y = 1000) => { const pose = (o: number) => mode === "sneak" ? { ...walk(f + o, 1, 0.6), lean: 14, mouth: "flat" as const } : mode === "run" ? { ...run(f + o), mouth: "o" as const } : {};
  return <>{P(DANA, { facing: 1, ...pose(5) }, x, y, 0.85, f, 4)}{P(MIRA, { facing: 1, hold: "walkie", ...pose(11) }, x - 160, y, 0.85, f, 2)}{P(KAI_PACK, { facing: 1, ...pose(2) }, x - 290, y, 0.85, f, 1)}{P(RUIZ, { facing: 1, hold: "keys", ...pose(8) }, x + 170, y, 0.85, f, 3)}</>; };
const cab = (c: Ctx, cam: number[][], out: any, poses: { k?: any; m?: any; d?: any; r?: any }, show = "kmdr", shake = 0) => <S cam={camAt(c.t, [[0, ...cam[0]], [c.d, ...cam[1]]])}><Cab f={c.f} outside={out} shake={shake}>
  {show.includes("d") && P(DANA, { facing: 1, aR: [62, 58], aL: [58, 60], ...poses.d }, 440, 1000, 1.5, c.f, 4)}
  {show.includes("k") && P(KAI_PACK, { facing: -1, ...poses.k }, poses.k?.x ?? 820, 1000, 1.5, c.f, 1)}
  {show.includes("m") && P(MIRA, { facing: -1, hold: "walkie", aR: [20, 50], ...poses.m }, 1110, 1000, 1.5, c.f, 2)}
  {show.includes("r") && P(RUIZ, { facing: -1, aR: [10, 20], ...poses.r }, 1460, 1000, 1.5, c.f, 3)}</Cab></S>;
const c12: Shot[] = [
  { at: ["n1"], r: c => <S cam={mv(c, [-300, -40, 1.15], [-200, -40, 1.2])}><Lot f={c.f} zombies={5} moon><g transform="translate(1300 980)"><BoxTruck /></g>{team(c.f, 500 + c.t * 2, "sneak")}</Lot></S> },
  { at: ["n2"], r: c => <S cam={mv(c, onHead(500 + 2 * 120 - 160, 1000, 0.85 * 0.68, 3.0, 0, 40), onHead(500 + 2 * 120 - 160, 1000, 0.85 * 0.68, 3.2, 0, 40))}><Lot f={c.f} zombies={0} moon>{P(MIRA, { facing: 1, hold: "walkie", aR: [20, 50], mouth: "o", look: [0.4, 0.8] }, 500 + 2 * 120 - 160, 1000, 0.85, c.f, 2)}<g transform={`translate(${500 + 2 * 120 - 160 + 40} ${1000 - 0.85 * 0.68 * 200})`}><Glow x={0} y={0} r={60} color="#ff4a3a" o={0.5 + 0.5 * Math.sin(c.f)} /></g></Lot></S> },
  { at: ["squeal"], r: c => <S cam={mv(c, [-200, -100, 1.4], [-200, -100, 1.5])}><Lot f={c.f} zombies={0} moon><Crowd f={c.f} x0={-400} x1={1600} y={720} n={14} s={0.5} seed={41} dir={1} /></Lot></S> },
  { at: ["kai1"], r: c => <S cam={mv(c, onHead(400, 1000, 0.85, 2.6, 30, 30), onHead(400, 1000, 0.85, 2.8, 30, 30))}><Lot f={c.f} zombies={0} moon>{P(KAI_PACK, { facing: -1, talk: c.talk("kai1"), mouth: "shout", brow: 0.8, eyes: 1.3, look: [0.8, 0] }, 400, 1000, 0.85, c.f, 1)}</Lot></S> },
  { at: ["ruiz1"], r: c => <S cam={mv(c, [-200, -40, 1.1], [100, -40, 1.1])}><Lot f={c.f} zombies={0} moon><g transform="translate(1300 980)"><BoxTruck /></g>
    <Crowd f={c.f} x0={-760 + c.t * 8.5} x1={-160 + c.t * 8.5} y={900} n={10} s={0.75} seed={43} dir={1} run={1} />{team(c.f, 520 + c.t * 9, "run")}</Lot></S> },
  { at: ["run"], r: c => { const grab = c.t > 18; return <S cam={mv(c, [380, -60, 1.6], [400, -60, 1.7])}><Lot f={c.f} zombies={0} moon><g transform="translate(1000 980)"><BoxTruck /></g>
    <Crowd f={c.f} x0={200 + c.t * 6} x1={700 + c.t * 6} y={940} n={3} s={0.85} seed={47} dir={1} run={1} />
    {P(RUIZ, { facing: 1, aR: grab ? [80, 10] : [100, 10], aL: grab ? [60, 20] : [90, 10], mouth: grab ? "shout" : "o", brow: 0.8, lean: grab ? -10 : 10 }, 1560, 1000, 1.0, c.f, 3)}
    {grab && <Character look={ZOMBIES[2]} pose={{ facing: 1, ...zombiePose(c.f, 3, 1), aR: [96, 0] }} x={1400} y={1000} s={0.95} f={c.f} seed={9} />}</Lot>
    {c.t > 34 && <rect width={W} height={H} fill="#000" opacity={sat((c.t - 34) / 4)} />}</S>; } },
  { at: ["n3"], r: c => cab(c, [[0, 0, 1.0], [0, 0, 1.04]], "night", { k: { mouth: "o", look: [0.8, 0.1] }, m: { mouth: "sad", brow: 0, browIn: 0.8 }, d: { mouth: "o", look: [0.8, 0] }, r: { mouth: "frown", look: [-0.3, 0.8], brow: 0, browIn: 0.6 } }, "kmdr", sat(1 - c.t / 30)) },
  { at: ["ruiz2"], r: c => cab(c, [onHead(1460, 1000, 1.5 * 1.06, 1.9, -60, 40), onHead(1460, 1000, 1.5 * 1.06, 2.35, -60, 40)], "night", { r: { talk: c.talk("ruiz2"), mouth: "smile", look: [-0.8, 0] } }, "r") },
  { at: ["ruiz2", 0.55], r: c => <Sleeve f={c.f} /> },
  { at: ["dana1"], r: c => cab(c, [onHead(440, 1000, 1.5, 2.3, 60, 40), onHead(440, 1000, 1.5, 2.45, 60, 40)], "night", { d: { talk: c.talk("dana1"), mouth: "sad", brow: 0, browIn: 0.9, look: [0.9, 0] } }, "d") },
  { at: ["ruiz3"], r: c => cab(c, [onHead(1460, 1000, 1.5 * 1.06, 2.0, -40, 40), onHead(1460, 1000, 1.5 * 1.06, 2.6, -40, 40)], "night", { r: { talk: c.talk("ruiz3"), mouth: "smile", brow: 0, browIn: 0.7, tears: sat(c.t / 80), look: [-0.9, 0.1] } }, "r") },
  { at: ["n4"], r: c => { const rx = 1100 - c.t * 1.2; return <S cam={mv(c, [-60, -40, 1.15], [-60, -60, 1.25])}><Crossroads f={c.f}><g transform="translate(300 900) scale(0.75)"><BoxTruck lights /></g>
    {P(RUIZ, { facing: -1, ...walk(c.f, -1, 0.8), aR: [10, 40] }, rx, 700 - c.t * 0.5, 0.42 - c.t * 0.0006, c.f, 3)}</Crossroads></S>; } },
  { at: ["mira1"], r: c => cab(c, [onHead(1110, 1000, 1.5 * 0.68, 2.6, -30, 20), onHead(1110, 1000, 1.5 * 0.68, 2.75, -30, 20)], "dawn", { m: { talk: c.talk("mira1"), mouth: "sad", brow: 0, browIn: 0.9, tears: 1, look: [0, 0.8] } }, "m") },
  { at: ["kai2"], r: c => cab(c, [[30, -60, 1.5], [30, -60, 1.6]], "dawn", { k: { x: 860, facing: 1, talk: c.talk("kai2"), mouth: "sad", brow: 0, browIn: 0.6, aR: [20, 70], look: [0.8, 0.4] }, m: { mouth: "sad", tears: 0.6, look: [-0.8, -0.2] } }, "km") },
];
export const C12: React.FC = () => <ChapterPlayer ch="c12" vo={VO_C12} shots={c12} days={[["n1", "DAY 21", "1:30 A.M.", 110]]} />;
export const C12_LEN = chLen("c12", VO_C12);

// ================= C13 — the road north =================
const drive = (c: Ctx, kind: any, cam: number[][] = [[0, 0, 1], [0, 0, 1]]) => <S cam={camAt(c.t, [[0, ...cam[0]], [c.d, ...cam[1]]])}><Landscape f={c.f} kind={kind}><g transform={`translate(560 ${880 + Math.sin(c.f * 0.6) * 2}) scale(0.72)`}><BoxTruck wheelRot={c.f * 14} lights={kind === "town"} dirty={0.5} /></g></Landscape></S>;
const c13: Shot[] = [
  { at: ["n1"], r: c => drive(c, "town") },
  { at: ["n1", 0.35], r: c => drive(c, "gas", [[0, -40, 1.1], [0, -40, 1.1]]) },
  { at: ["n1", 0.65], r: c => cab(c, [[0, 0, 1.0], [0, 0, 1.03]], "day", { d: { mouth: "flat", look: [0.6, 0] }, k: { hold: "map", aR: [50, 80], look: [0.4, 0.8] }, m: { eyes: 0.1, mouth: "flat" } }, "dkm", 1) },
  { at: ["fact1"], r: c => <Density f={c.f} k={c.t / (c.d * 0.7)} /> },
  { at: ["n2"], r: c => drive(c, "plains") },
  { at: ["n2", 0.5], r: c => <USMap f={c.f} spread={1} safe={1} path={sat(c.t / (c.d * 0.9))} /> },
  { at: ["n3"], r: c => drive(c, "mountains", [[0, 0, 1.0], [100, -40, 1.15]]) },
];
export const C13: React.FC = () => <ChapterPlayer ch="c13" vo={VO_C13} shots={c13} />;
export const C13_LEN = chLen("c13", VO_C13);

// ================= C14 — Day 30: the safe zone =================
const cp = (c: Ctx, cam: number[][], holt: any, kids: any = {}, showKids = true) => <S cam={camAt(c.t, [[0, ...cam[0]], [c.d, ...cam[1]]])}><Checkpoint f={c.f}>
  {showKids && P(KAI_PACK, { facing: 1, aR: [88, 2], aL: [84, 4], mouth: "flat", look: [0.8, 0], ...kids }, 700, 1000, 1.0, c.f, 1)}
  {showKids && P(MIRA, { facing: 1, aR: [88, 2], aL: [84, 4], mouth: "worried", look: [0.8, -0.2] }, 520, 1000, 1.0, c.f, 2)}
  {P(HOLT, { facing: -1, hold: "torch", beam: 1, aR: [82, 8], look: [0.7, 0.2], ...holt }, 1180, 1000, 1.05, c.f, 6)}</Checkpoint></S>;
const c14: Shot[] = [
  { at: ["n1"], r: c => <S cam={mv(c, [0, -60, 1.0], [0, -60, 1.08])}><Checkpoint f={c.f}><g transform="translate(-200 980) scale(0.8)"><BoxTruck lights dirty={0.7} /></g>{P(HOLT, { facing: -1, hold: "rifle", aR: [50, 70], aL: [40, 60] }, 1180, 1000, 1.05, c.f, 6)}</Checkpoint></S> },
  { at: ["holt1"], r: c => cp(c, [[0, -40, 1.2], [0, -40, 1.25]], { talk: c.talk("holt1"), mouth: "flat" }) },
  { at: ["holt1", 0.6], r: c => cp(c, [onHead(1180, 1000, 1.05 * 1.1, 2.3, -60, 50), onHead(1180, 1000, 1.05 * 1.1, 2.4, -60, 50)], { talk: c.talk("holt1"), mouth: "smile", hold: "rifle", aR: [50, 70], aL: [40, 60] }, {}, false) },
  { at: ["n2"], r: c => <S cam={mv(c, [-300, -40, 1.1], [300, -40, 1.1])}><TentCity f={c.f} board={false} /></S> },
  { at: ["n3"], r: c => <S cam={mv(c, [0, -40, 1.15], [60, -40, 1.2])}><TentCity f={c.f} board={false}>{P(MIRA, { facing: 1, ...walk(c.f), hold: "walkie" }, 500 + c.t * 3, 1030, 0.95, c.f, 2)}{P(KAI_PACK, { facing: 1, ...walk(c.f + 6) }, 340 + c.t * 3, 1030, 0.95, c.f, 1)}</TentCity></S> },
  { at: ["mira1"], r: c => <S cam={mv(c, [-100, 60, 1.35], [-60, 60, 1.4])}><TentCity f={c.f}>{P(MIRA, { facing: 1, aR: [100, 0], talk: c.talk("mira1"), mouth: "open", eyes: 1.25, brow: 0.8, look: [0.8, -0.4] }, 520, 1030, 1.0, c.f, 2)}{P(KAI_PACK, { facing: 1, mouth: "o", look: [0.8, -0.4] }, 340, 1030, 1.0, c.f, 1)}</TentCity></S> },
  { at: ["n4"], r: c => <SV bg="#8a6a44"><rect width={W} height={H} fill="#c8a878" /><Noise x={0} y={0} w={W} h={H} freq={0.5} o={0.3} />
    {Array.from({ length: 10 }, (_, i) => <g key={i} transform={`translate(${(i % 5) * 420 - 100} ${(Math.floor(i / 5)) * 600 - 80}) rotate(${(rnd(i, 3) - 0.5) * 12})`}><rect width={300} height={400} fill="#f4f1e8" /><rect x={30} y={30} width={240} height={220} fill="#8a9ab0" /><circle cx={150} cy={130} r={60} fill="#2a2532" /></g>)}
    <g transform={`translate(960 520) scale(${1.4 + c.t * 0.004})`}><Badge x={0} y={0} s={1} note="ARRIVED DAY 12 · TENT 48" /></g></SV> },
];
export const C14: React.FC = () => <ChapterPlayer ch="c14" vo={VO_C14} shots={c14} days={[["n1", "DAY 30", "MONTANA · 6:50 P.M.", 130]]} />;
export const C14_LEN = chLen("c14", VO_C14);

// ================= C15 — tent 48, the cliffhanger, part 2, end card =================
const Tent48: React.FC<{ f: number; children?: React.ReactNode }> = ({ f, children }) => <g>
  <rect x={-600} y={-200} width={3200} height={1500} fill="#3e4a2a" />
  <path d="M-600 -200 L960 -100 L2600 -200 L2600 900 L-600 900 Z" fill="#55653a" /><path d="M960 -100 L960 900" stroke="#3a4626" strokeWidth={14} />
  {Array.from({ length: 8 }, (_, i) => <path key={i} d={`M${-400 + i * 400} -150 Q${-200 + i * 400} 300 ${-400 + i * 400} 900`} stroke="#4a5a32" strokeWidth={6} fill="none" opacity={0.6} />)}
  <rect x={-600} y={860} width={3200} height={500} fill="#4a4232" /><AO x={-600} y={860} w={3200} h={40} dir="down" o={0.5} />
  {/* cot */}
  <rect x={500} y={760} width={900} height={60} rx={10} fill="#6a7a4a" /><rect x={520} y={740} width={860} height={30} rx={10} fill="#8a9a6a" /><path d="M540 820 L620 980 M1360 820 L1280 980 M620 820 L540 980 M1280 820 L1360 980" stroke="#3a3a3a" strokeWidth={8} />
  <g transform="translate(780 730) rotate(-80) scale(0.35)"><Badge x={0} y={0} s={1} /></g>
  <g transform="translate(1120 720) rotate(4)"><rect x={-110} y={-24} width={220} height={30} rx={4} fill="#5a3a24" /><rect x={-104} y={-30} width={208} height={12} fill="#f4ecd8" /></g>
  {/* lantern on a crate */}
  <rect x={1560} y={740} width={160} height={140} fill="#8a6a3a" /><rect x={1615} y={680} width={50} height={60} rx={8} fill="#ffd88a" /><Glow x={1640} y={700} r={700} color="#ffb84a" o={0.35} />
  {children}
</g>;
const c15: Shot[] = [
  { at: ["run"], r: c => <S cam={mv(c, [-200, -40, 1.15], [200, -40, 1.15])}><TentCity f={c.f} board={false}>{P(MIRA, { facing: 1, ...run(c.f) }, 300 + c.t * 14, 1030, 0.95, c.f, 2)}{P(KAI_PACK, { facing: 1, ...run(c.f + 5) }, 120 + c.t * 14, 1030, 0.95, c.f, 1)}</TentCity></S> },
  { at: ["n1"], r: c => <S cam={mv(c, [0, -20, 1.05], [0, -20, 1.12])}><Tent48 f={c.f}>{P(KAI_PACK, { facing: 1, mouth: "o", look: [0.8, 0.5] }, 300, 1000, 1.1, c.f, 1)}{P(MIRA, { facing: 1, mouth: "o", look: [0.8, 0.4], hold: "walkie", aR: [20, 50] }, 150, 1000, 1.1, c.f, 2)}</Tent48></S> },
  { at: ["n1", 0.55], r: c => <S cam={mv(c, [-100, 210, 2.6], [-60, 210, 2.8])}><Tent48 f={c.f} /></S> },
  { at: ["n2"], r: c => <Notebook f={c.f} k={0} /> },
  { at: ["page"], r: c => <Notebook f={c.f} k={0} /> },
  { at: ["n3"], r: c => <Notebook f={c.f} k={sat(c.t / 40)} /> },
  { at: ["n3", 0.6], r: c => <S cam={mv(c, [-60, -310, 3.0], [-60, -310, 3.5])}><Ranch f={c.f} inside><Bat x={900} y={240} f={c.f} s={1.3} /></Ranch></S> },
  { at: ["part2"], r: c => <Part2 f={c.t} /> },
  { at: ["n4"], r: c => <><S cam={mv(c, [80, -120, 1.5], [80, -120, 1.6])}><DockDoor f={c.f} /></S><Big text="WOULD YOU OPEN THE DOOR?" k={sat(c.t / 10)} size={96} y={880} /></> },
  { at: ["end"], r: c => <EndCard f={c.t} /> },
];
export const C15: React.FC = () => <ChapterPlayer ch="c15" vo={VO_C15} shots={c15} />;
export const C15_LEN = chLen("c15", VO_C15);
