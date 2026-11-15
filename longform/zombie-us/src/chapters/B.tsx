// Chapters 6–10: the exodus, the fortress, the rules, the knock, why it makes them attack.
import React from "react";
import { AbsoluteFill } from "remotion";
import { camAt, sat, ease, easeOut, lerp, rnd, W, H } from "../engine/core";
import { Glow } from "../engine/fx";
import { Noise, AO } from "../engine/tex";
import { ChapterPlayer, Ctx, Shot, chLen } from "../Player";
import { StoreAisle, StoreFront, StaffRoom, DockDoor, Shelf, Cart, P } from "../scenes/Store";
import { Street, Highway, RoofView } from "../scenes/Outdoor";
import { Phone, Clipboard, RulesBoard, BrainBoard, AntFungus, RatCat, Threes, Peephole, Binoculars } from "../scenes/Inserts";
import { KAI, KAI_PACK, MIRA, RUIZ, DANA } from "../chars/cast";
import { runPose, walkPose } from "../chars/Rig2";
import { S, mv, onHead } from "./A";
import { VO_C6 } from "../vo_c6"; import { VO_C7 } from "../vo_c7"; import { VO_C8 } from "../vo_c8"; import { VO_C9 } from "../vo_c9"; import { VO_C10 } from "../vo_c10";

const run = (f: number, dir: 1 | -1 = 1) => runPose(f * 0.38 * dir, 1);
const walk = (f: number, dir: 1 | -1 = 1) => walkPose(f * 0.14 * dir, 1);

// ================= C6 — Day 2: the exodus =================
const street = (c: Ctx, cam: number[][], kids: React.ReactNode) => <S cam={camAt(c.t, [[0, ...cam[0]], [c.d, ...cam[1]]])}><Street f={c.f}>{kids}</Street></S>;
const c6: Shot[] = [
  { at: ["n1"], r: c => { const kx = Math.min(780, -200 + c.t * 14); return street(c, [[-40, -40, 1.15], [0, -40, 1.2]], <>
    {P(MIRA, { facing: 1, mouth: "worried", look: [-0.6, 0.2], hold: "walkie", aR: [20, 50] }, 960, 702, 0.95, c.f, 2)}
    {P(KAI_PACK, kx < 780 ? { facing: 1, ...run(c.f) } : { facing: 1, mouth: "flat" }, kx, 990, 1.0, c.f, 1)}</>); } },
  { at: ["n1", 0.58], r: c => <Phone f={c.f} shake={1} mode={{ kind: "alert" }} bg="#2a1a14" /> },
  { at: ["mira1"], r: c => street(c, [onHead(960, 702, 0.95 * 0.68, 2.6, 60, 20), onHead(960, 702, 0.95 * 0.68, 2.75, 60, 20)], <>
    {P(MIRA, { facing: 1, talk: c.talk("mira1"), brow: 0, browIn: 0.8, look: [0.7, 0.2], hold: "walkie", aR: [20, 50] }, 960, 702, 0.95, c.f, 2)}</>) },
  { at: ["kai1"], r: c => street(c, [onHead(1120, 760, 1.0, 2.3, -40, 0), onHead(1120, 760, 1.0, 2.45, -40, 0)], <>
    {P(KAI_PACK, { facing: -1, talk: c.talk("kai1"), mouth: "smile", brow: 0, browIn: 0.6, aR: [30, 30], look: [0.6, 0.3] }, 1120, 760, 1.0, c.f, 1)}</>) },
  { at: ["n2"], r: c => <S cam={mv(c, [0, -20, 1.0], [60, -20, 1.05])}><Highway f={c.f} /></S> },
  { at: ["fact1"], r: c => <S cam={mv(c, [-300, 60, 1.5], [200, 60, 1.5])}><Highway f={c.f} /></S> },
  { at: ["n3"], r: c => <S cam={mv(c, [360, -60, 2.2], [380, -70, 2.4])}><Highway f={c.f} /></S> },
  { at: ["n3", 0.5], r: c => <S cam={mv(c, [-200, 120, 1.6], [-420, 120, 1.7])}><Highway f={c.f} man={false} /></S> },
  { at: ["n4"], r: c => street(c, [[-100, -40, 1.15], [100, -40, 1.15]], <>
    {P(MIRA, { facing: 1, ...walk(c.f), hold: "walkie" }, 300 + c.t * 4.2, 1000, 0.95, c.f, 2)}{P(KAI_PACK, { facing: 1, ...walk(c.f + 7), look: [0.9, 0.2] }, 470 + c.t * 4.2, 1000, 1.0, c.f, 1)}</>) },
];
export const C6: React.FC = () => <ChapterPlayer ch="c6" vo={VO_C6} shots={c6} days={[["n1", "DAY 2", "6:30 A.M.", 120]]}
  facts={[["fact1", "Hurricane Rita, 2005: about 3 million people evacuated at once. The traffic jam stretched over 100 miles, and cars ran out of gas."]]} />;
export const C6_LEN = chLen("c6", VO_C6);

// ================= C7 — the fortress =================
const outsideKids = (f: number, kt = 0) => <g transform="translate(0 0)"><rect x={0} y={0} width={360} height={600} fill="#c8d8e4" /><rect x={0} y={420} width={360} height={180} fill="#9a9a90" />
  <g transform="translate(150 600) scale(0.8)"><g>{P(KAI_PACK, { facing: -1, mouth: "flat", look: [0.6, 0], talk: kt }, 0, 0, 1, f, 1)}</g></g><g transform="translate(270 600) scale(0.8)">{P(MIRA, { facing: -1, mouth: "worried", hold: "walkie", aR: [20, 50] }, 0, 0, 1, f, 2)}</g></g>;
const dock = (c: Ctx, cam: number[][], open: number, ruiz: any, kids = true, kt = 0, showR = true) => <S cam={camAt(c.t, [[0, ...cam[0]], [c.d, ...cam[1]]])}><DockDoor f={c.f} open={open} outside={kids ? outsideKids(c.f, kt) : undefined} />
  {showR && P(RUIZ, { facing: 1, hold: "keys", aR: [40, 40], ...ruiz }, 700, 900, 1.15, c.f, 3)}</S>;
const c7: Shot[] = [
  { at: ["dock"], r: c => dock(c, [[0, -40, 1.0], [0, -40, 1.05]], sat((c.t - 8) / 18), { aR: [70, 20], look: [0.8, 0] }) },
  { at: ["ruiz1"], r: c => dock(c, [onHead(700, 900, 1.15 * 1.06, 2.1, 120, 40), onHead(700, 900, 1.15 * 1.06, 2.25, 120, 40)], 1, { talk: c.talk("ruiz1"), mouth: "smile", brow: 0.5, look: [0.8, 0] }) },
  { at: ["kai1"], r: c => dock(c, [onHead(1030, 760, 0.8, 2.8, 30, 20), onHead(1030, 760, 0.8, 3.0, 30, 20)], 1, { look: [0.8, 0] }, true, c.talk("kai1"), false) },
  { at: ["ruiz2"], r: c => dock(c, [onHead(700, 900, 1.15 * 1.06, 2.3, 100, 40), onHead(700, 900, 1.15 * 1.06, 2.45, 100, 40)], 1, { talk: c.talk("ruiz2"), mouth: "smile", look: [0.8, 0.1] }) },
  { at: ["n1"], r: c => <S cam={mv(c, [-100, -40, 1.1], [100, -40, 1.12])}><StoreAisle f={c.f} light="day" sign="AISLE 7 · CANNED FOOD"><Shelf x={300} y={900} w={1300} seed={5} empty={0.2} />
    {P(RUIZ, { facing: 1, ...walk(c.f), hold: "keys" }, 500 + c.t * 3, 1000, 1.1, c.f, 3)}{P(KAI, { facing: 1, ...walk(c.f + 9), hold: "can" }, 330 + c.t * 3, 1000, 1.1, c.f, 1)}{P(MIRA, { facing: 1, ...walk(c.f + 4), hold: "walkie" }, 160 + c.t * 3, 1000, 1.1, c.f, 2)}</StoreAisle></S> },
  { at: ["n1", 0.5], r: c => <Clipboard f={c.f} items={["WATER", "CANNED FOOD", "BATTERIES", "FIRST AID"]} ticks={c.t / 14} /> },
  { at: ["fact1"], r: c => <S cam={mv(c, [-100, 100, 1.5], [-60, 100, 1.6])}><StoreAisle f={c.f} light="day" sign="AISLE 7 · CANNED FOOD"><Shelf x={300} y={900} w={1300} seed={5} empty={0.15 + 0.8 * sat(c.t / (c.d * 0.8))} /></StoreAisle></S> },
  { at: ["n2"], r: c => <S cam={mv(c, [-300, -60, 1.25], [100, -60, 1.25])}><Highway f={c.f} man={false} /></S> },
  { at: ["n3"], r: c => <S cam={mv(c, [100, -60, 1.25], [140, -100, 1.75])}><StoreFront f={c.f} crowd={70} hands={16} press={1} /></S> },
];
export const C7: React.FC = () => <ChapterPlayer ch="c7" vo={VO_C7} shots={c7}
  facts={[["fact1", "Most supermarkets get deliveries almost every day. If the trucks stop, the shelves are empty in about three days.", "right"]]} />;
export const C7_LEN = chLen("c7", VO_C7);

// ================= C8 — Day 5: the rules =================
const roof = (c: Ctx, cam: number[][], kai: any, extra: any = {}) => <S cam={camAt(c.t, [[0, ...cam[0]], [c.d, ...cam[1]]])}><RoofView f={c.f} {...extra}>{P(KAI_PACK, { facing: 1, ...kai }, 560, 496, 0.8, c.f, 1, "#ffe8b0")}</RoofView></S>;
const staff = (c: Ctx, cam: number[][], board: React.ReactNode, who: React.ReactNode) => <S cam={camAt(c.t, [[0, ...cam[0]], [c.d, ...cam[1]]])}><StaffRoom f={c.f} board={board}>{who}</StaffRoom></S>;
const c8: Shot[] = [
  { at: ["n1"], r: c => roof(c, [[-60, -40, 1.05], [-40, -50, 1.12]], { hold: "binoculars", aR: [62, 92], aL: [56, 96], look: [0.9, -0.3] }) },
  { at: ["n1", 0.5], r: c => <Binoculars><S cam={mv(c, [500, 420, 2.4], [700, 420, 2.4])}><RoofView f={c.f} /></S></Binoculars> },
  { at: ["n2"], r: c => { const throwT = 10, armA = c.t < throwT ? 150 : lerp(150, 60, sat((c.t - throwT) / 5));
    return roof(c, [[40, 0, 1.0], [40, 0, 1.0]], { hold: c.t < throwT + 2 ? "can" : null, aR: [armA, 20], look: [0.9, -0.4], mouth: "flat" }, { canT: c.t - throwT - 2, turn: sat((c.t - throwT - 26) / 20) }); } },
  { at: ["n2", 0.62], r: c => <S cam={mv(c, [480, 400, 2.0], [480, 400, 2.2])}><RoofView f={c.f + 60} turn={1} canT={60} /></S> },
  { at: ["n3"], r: c => roof(c, [[0, 60, 1.0], [-60, 0, 1.25]], { mouth: "smirk", look: [0.6, 0.8] }, { turn: 1, canT: 60 }) },
  { at: ["n4"], r: c => staff(c, [[-40, -40, 1.2], [-20, -40, 1.25]], <RulesBoard n={0.6 + 2.6 * sat(c.t / c.d)} />, <>{P(KAI, { facing: 1, aR: [118, 12], look: [0.8, -0.4], mouth: "flat" }, 470, 900, 1.15, c.f, 1)}</>) },
  { at: ["fact1"], r: c => <Threes f={c.f} k={c.t / (c.d * 0.8)} /> },
  { at: ["ruiz1"], r: c => staff(c, [onHead(1500, 940, 1.15 * 1.06, 2.0, -60, 40), onHead(1500, 940, 1.15 * 1.06, 2.15, -60, 40)], <RulesBoard n={3} />, <>{P(RUIZ, { facing: -1, hold: "clipboard", aR: [50, 80], talk: c.talk("ruiz1"), mouth: "smile", look: [-0.6, 0.2] }, 1500, 940, 1.15, c.f, 3)}</>) },
  { at: ["kai1"], r: c => staff(c, [onHead(700, 940, 1.15, 2.4, 40, 30), onHead(700, 940, 1.15, 2.5, 40, 30)], <RulesBoard n={3} />, <>{P(KAI, { facing: 1, talk: c.talk("kai1"), brow: 0.8, eyes: 1.2, look: [0.9, 0] }, 700, 940, 1.15, c.f, 1)}</>) },
  { at: ["ruiz2"], r: c => staff(c, [onHead(1500, 940, 1.15 * 1.06, 2.2, -40, 40), onHead(1500, 940, 1.15 * 1.06, 2.35, -40, 40)], <RulesBoard n={3} />, <>{P(RUIZ, { facing: 1, hold: "clipboard", aR: [30, 50], talk: c.talk("ruiz2"), mouth: "flat", brow: -0.3, look: [1, 0] }, 1500, 940, 1.15, c.f, 3)}</>) },
  { at: ["knock"], r: c => <S cam={mv(c, [80, -120, 1.6], [80, -120, 1.7])}><DockDoor f={c.f} knock={[0, 10, 20].some(k => c.t >= k && c.t < k + 5) ? 1 : 0} /></S> },
];
export const C8: React.FC = () => <ChapterPlayer ch="c8" vo={VO_C8} shots={c8} days={[["n1", "DAY 5", "NOON", 110]]} />;
export const C8_LEN = chLen("c8", VO_C8);

// ================= C9 — Day 7: the knock =================
const Alley: React.FC<{ f: number }> = ({ f }) => <g><rect x={-200} y={-200} width={2400} height={1500} fill="#c8ccd4" />
  {Array.from({ length: 30 }, (_, r) => Array.from({ length: 24 }, (_, k) => <rect key={`${r}-${k}`} x={-200 + k * 100 + (r % 2) * 50} y={-200 + r * 40} width={94} height={34} fill="#a8644a" />))}
  <rect x={-200} y={820} width={2400} height={500} fill="#6a6e78" /><g transform="translate(1300 820)"><rect x={0} y={-260} width={420} height={260} fill="#2f6a4a" /><rect x={-10} y={-280} width={440} height={30} fill="#245a3a" /></g>
  <rect x={-200} y={-200} width={2400} height={1500} fill="#fff6d8" opacity={0.15} /></g>;
const danaOut = (c: Ctx, pose: any) => <><Alley f={c.f} />{P(DANA, { facing: 1, aR: [60, 90], aL: [55, 95], mouth: "worried", brow: 0, browIn: 0.8, look: [0.5, -0.1], ...pose }, 960, 1080, 1.4, c.f, 4)}</>;
const inside = (c: Ctx, cam: number[][], open: number, ruiz: any = {}, kai: any = {}, dana?: any) => <S cam={camAt(c.t, [[0, ...cam[0]], [c.d, ...cam[1]]])}><DockDoor f={c.f} open={open} outside={<rect x={0} y={0} width={360} height={600} fill="#d8c8b0" />} />
  {dana && P(DANA, { facing: -1, mouth: "worried", ...dana }, 1080, 900, 1.15, c.f, 4)}
  {P(RUIZ, { facing: 1, hold: "mop", aR: [30, 30], brow: -0.4, ...ruiz }, 420, 920, 1.15, c.f, 3)}
  {P(KAI, { facing: 1, aR: [6, 10], ...kai }, kai.x ?? 760, 920, 1.15, c.f, 1)}</S>;
const c9: Shot[] = [
  { at: ["knock"], r: c => inside(c, [[0, -40, 1.05], [0, -40, 1.1]], 0, { look: [0.9, 0], mouth: "flat" }, { look: [0.9, 0], mouth: "o" }) },
  { at: ["dana1"], r: c => <Peephole f={c.f}><svg width={W} height={H} style={{ position: "absolute" }}><g transform="translate(960 560) scale(1.15) translate(-960 -560)">{danaOut(c, { talk: c.talk("dana1") })}</g></svg></Peephole> },
  { at: ["ruiz1"], r: c => inside(c, [onHead(420, 920, 1.15 * 1.06, 2.2, 60, 40), onHead(420, 920, 1.15 * 1.06, 2.35, 60, 40)], 0, { talk: c.talk("ruiz1"), mouth: "frown", look: [0.9, 0] }) },
  { at: ["kai1"], r: c => inside(c, [onHead(760, 920, 1.15, 2.3, 20, 30), onHead(760, 920, 1.15, 2.45, 20, 30)], 0, {}, { talk: c.talk("kai1"), look: [-0.9, 0], facing: -1, brow: 0.2 }) },
  { at: ["n1"], r: c => <S cam={mv(c, [220, -110, 2.6], [220, -110, 3.0])}><DockDoor f={c.f} /></S> },
  { at: ["check"], r: c => inside(c, [[100, -40, 1.25], [120, -40, 1.3]], 1, { look: [0.9, 0] }, { x: 620, hold: "torch", beam: 1, aR: [84, 10], look: [0.9, 0.3], mouth: "flat" }, { aR: [86, 0], aL: [80, 4], look: [-0.6, 0.3] }) },
  { at: ["n2"], r: c => inside(c, [[230, -10, 2.4], [250, -10, 2.5]], 1, {}, { x: 620, hold: "torch", beam: 1, aR: [84, 10], look: [0.9, 0.3] }, { aR: [86, 0], aL: [80, 4], look: [-0.6, 0.4] }) },
  { at: ["dana2"], r: c => inside(c, [onHead(1080, 900, 1.15, 2.3, -40, 30), onHead(1080, 900, 1.15, 2.45, -40, 30)], 1, {}, {}, { talk: c.talk("dana2"), mouth: "sad", brow: 0, browIn: 0.7, look: [-0.8, 0.1] }) },
];
export const C9: React.FC = () => <ChapterPlayer ch="c9" vo={VO_C9} shots={c9} days={[["knock", "DAY 7", "9:15 A.M.", 110]]} />;
export const C9_LEN = chLen("c9", VO_C9);

// ================= C10 — why it makes them attack =================
const room = (c: Ctx, cam: number[][], k: number, dana: any, mira?: any, all = false) => <S cam={camAt(c.t, [[0, ...cam[0]], [c.d, ...cam[1]]])}><StaffRoom f={c.f} board={<BrainBoard k={k} />}>
  {all && P(RUIZ, { facing: -1, mouth: "flat", look: [-0.6, 0.2] }, 1580, 940, 1.1, c.f, 3)}
  {all && P(KAI, { facing: -1, mouth: "flat", look: [-0.6, 0.1] }, 1420, 940, 1.1, c.f, 1)}
  {mira && P(MIRA, { facing: -1, ...mira }, 980, 940, 1.1, c.f, 2)}
  {P(DANA, { facing: 1, ...dana }, 450, 920, 1.12, c.f, 4)}</StaffRoom></S>;
const c10: Shot[] = [
  { at: ["dana1"], r: c => room(c, [[-40, -60, 1.15], [-20, -60, 1.2]], sat(c.t / c.d) * 0.95, { aR: [118, 12], talk: c.talk("dana1"), look: [0.9, -0.3] }) },
  { at: ["n1"], r: c => <S cam={mv(c, [-20, -200, 1.9], [-20, -200, 2.1])}><StaffRoom f={c.f} board={<BrainBoard k={1} />} /></S> },
  { at: ["fact1"], r: c => <div style={{ position: "absolute", inset: 0, transform: `scale(${1 + 0.3 * c.t / c.d})`, transformOrigin: "50% 30%" }}><AntFungus f={c.t * 1.2} /></div> },
  { at: ["fact2"], r: c => <RatCat f={c.t} /> },
  { at: ["mira1"], r: c => room(c, [onHead(980, 940, 1.1 * 0.68, 2.6, -40, 10), onHead(980, 940, 1.1 * 0.68, 2.75, -40, 10)], 1, {}, { talk: c.talk("mira1"), brow: 0, browIn: 0.8, look: [-0.8, -0.3], hold: "walkie", aR: [20, 50] }) },
  { at: ["dana2"], r: c => room(c, [onHead(450, 920, 1.12, 2.3, 60, 30), onHead(450, 920, 1.12, 2.45, 60, 30)], 1, { talk: c.talk("dana2"), mouth: "smile", brow: 0, browIn: 0.4, look: [0.9, 0.3] }) },
  { at: ["n2"], r: c => room(c, [[0, -40, 1.05], [-100, -40, 1.18]], 1, { mouth: "sad", brow: 0, browIn: 0.8, look: [-0.8, 0.5], facing: -1 }, { mouth: "flat", look: [-0.8, 0], hold: "walkie", aR: [20, 50] }, true) },
];
export const C10: React.FC = () => <ChapterPlayer ch="c10" vo={VO_C10} shots={c10}
  facts={[["fact1", "The Ophiocordyceps fungus takes over an ant's body: it climbs, bites down and waits. Then the fungus grows out of its head."],
    ["fact2", "The parasite Toxoplasma makes infected rats lose their fear of cats. They even walk toward them.", "right"]]} />;
export const C10_LEN = chLen("c10", VO_C10);
