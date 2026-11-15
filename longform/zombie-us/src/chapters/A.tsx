// Chapters 1–5: cold open (Day 3, 2:14 AM), a normal Tuesday, how it started, patient zero, the math + Mom's call.
import React from "react";
import { AbsoluteFill } from "remotion";
import { Stage, Layer, camAt, sat, ease, lerp, W, H } from "../engine/core";
import { Glow } from "../engine/fx";
import { ChapterPlayer, Ctx, Shot, chLen } from "../Player";
import { StoreAisle, StoreFront, Shelf, P } from "../scenes/Store";
import { Kitchen, KitchenTable, Ranch, Bat, NerveMicro, Terminal, DepBoard, PlaneSky, USMap } from "../scenes/World";
import { Street } from "../scenes/Outdoor";
import { Phone, Doubling, ER, TitleCard, GlassFace } from "../scenes/Inserts";
import { KAI, MIRA, MOM, RANCHER, GUARD } from "../chars/cast";
import { Character } from "../chars/Rig2";
import { VO_C1 } from "../vo_c1"; import { VO_C2 } from "../vo_c2"; import { VO_C3 } from "../vo_c3"; import { VO_C4 } from "../vo_c4"; import { VO_C5 } from "../vo_c5";

// camera that eases from key a to key b over the shot
export const mv = (c: Ctx, a: number[], b: number[]) => camAt(c.t, [[0, ...a], [c.d, ...b]]);
// a StoreFront child is split automatically: the outside (crowd) gets depth-of-field blur + darkening, the glass,
// frame, hands and the interior stay sharp — so heroes never read as standing among the infected.
export const S: React.FC<{ cam: any; children: React.ReactNode; bg?: string }> = ({ cam, children, bg = "#000" }) => {
  if (React.isValidElement(children) && children.type === StoreFront) return <Stage cam={cam} bg={bg}>
    <Layer depth={1} blur={4}>{React.cloneElement(children as any, { part: "out" })}</Layer><Layer depth={1}>{React.cloneElement(children as any, { part: "in" })}</Layer></Stage>;
  return <Stage cam={cam} bg={bg}><Layer depth={1}>{children}</Layer></Stage>; };
// close-up camera on a character at (x, rootY) with scale s: centre the head
export const onHead = (x: number, y: number, s: number, z: number, dx = 0, dy = 0) => [x - 960 + dx, y - 362 * s - 540 + dy, z];
export const Big: React.FC<{ text: string; k: number; color?: string; y?: number; size?: number }> = ({ text, k, color = "#fff", y = 540, size = 120 }) => k <= 0 ? null :
  <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}><div style={{ position: "absolute", top: y - size * 0.6, width: "100%", textAlign: "center", fontFamily: "Inter", fontWeight: 900, fontSize: size, color, opacity: Math.min(1, k), textShadow: "0 6px 0 rgba(0,0,0,.5), 0 0 40px rgba(0,0,0,.6)", transform: `scale(${0.92 + 0.08 * Math.min(1, k)})` }}>{text}</div></AbsoluteFill>;
const SICK = { ...RANCHER, skin: "#3a4a3a" };

// ================= C1 — cold open =================
const c1: Shot[] = [
  { at: ["open"], r: c => { const cx = lerp(560, 820, ease(c.t / 30)); return <S cam={mv(c, [0, 40, 1.05], [0, 30, 1.12])}><StoreFront f={c.f} crowd={44} hands={2} cart={false} inside={<>
    {P(MIRA, { facing: 1, hold: "torch", beam: 1, aR: [78, 6], mouth: "worried", brow: 0, browIn: 0.8 }, 300, 1060, 1.05, c.f, 2)}
    <g transform={`translate(${cx} 1000)`}><g transform="translate(-820 -1000)"><StoreFrontCart /></g></g>
    {P(KAI, { facing: 1, aR: [70, 20], aL: [64, 24], lean: 14, mouth: "flat", brow: -0.3 }, cx - 230, 1060, 1.1, c.f, 1, "#8ad0ff")}
    <g transform="translate(1120 1010)"><g transform="translate(-1120 -1010)"><StoreFrontCart2 /></g></g></>} /></S>; } },
  { at: ["n1"], r: c => <S cam={mv(c, [-515, 200, 1.45], [-505, 205, 1.58])}><StoreFront f={c.f} crowd={44} hands={3} inside={<>
    {P(MIRA, { facing: 1, hold: "torch", beam: 1, aR: [104, 4], mouth: "worried", brow: 0, browIn: 0.8, look: [0.8, -0.4] }, 250, 1060, 1.05, c.f, 2)}
    {P(KAI, { facing: 1, mouth: "flat", brow: 0, browIn: 0.5, look: [0.8, -0.1] }, 560, 1060, 1.1, c.f, 1, "#8ad0ff")}</>} /></S> },
  { at: ["n2"], r: c => <S cam={mv(c, [80, -40, 1.25], [120, -60, 1.45])}><StoreFront f={c.f} crowd={60} hands={4} press={0.5} /></S> },
  { at: ["slap"], r: c => <S cam={{ ...mv(c, [100, -80, 1.7], [100, -80, 1.8]), x: 100 + (c.t % 6 < 2 ? 4 : 0) }}><StoreFront f={c.f} crowd={60} hands={4 + Math.floor(c.t / 3)} press={1} /></S> },
  { at: ["slap", 0.45], r: c => <GlassFace f={c.f} t={c.t} /> },
  { at: ["mira1"], r: c => <S cam={mv(c, onHead(330, 1060, 1.05 * 0.68, 2.6, 30, 0), onHead(330, 1060, 1.05 * 0.68, 2.8, 30, 0))}><StoreFront f={c.f} crowd={50} hands={14} inside={<>
    {P(MIRA, { facing: 1, hold: "torch", beam: 1, aR: [70, 10], talk: c.talk("mira1"), brow: 0, browIn: 0.9, look: [-0.6, -0.3], eyes: 1.15 }, 330, 1060, 1.05, c.f, 2)}</>} /></S> },
  { at: ["kai1"], r: c => <S cam={mv(c, onHead(560, 1060, 1.1, 2.4, -40, 10), onHead(560, 1060, 1.1, 2.55, -40, 10))}><StoreFront f={c.f} crowd={50} hands={14} inside={<>
    {P(KAI, { facing: -1, talk: c.talk("kai1"), brow: 0, browIn: 0.7, look: [0.6, 0.4], mouth: "flat" }, 560, 1060, 1.1, c.f, 1, "#8ad0ff")}</>} /></S> },
  { at: ["hush"], r: c => { const off = c.t > 14; return <><S cam={mv(c, [-515, 190, 1.4], [-515, 195, 1.45])}><StoreFront f={c.f} crowd={50} hands={14} light="dark" inside={<>
    {P(MIRA, { facing: 1, hold: "torch", beam: off ? 0 : 1, aR: off ? [20, 30] : [104, 4], mouth: "worried", look: [0.4, 0.3] }, 250, 1060, 1.05, c.f, 2)}
    {P(KAI, { facing: -1, aR: off ? [40, 40] : [52, 50], mouth: "flat", brow: 0, browIn: 0.6, look: [0.5, 0.4] }, 560, 1060, 1.1, c.f, 1, "#8ad0ff")}</>} /></S>
    <AbsoluteFill style={{ background: "#000", opacity: off ? 0.45 : 0 }} /></>; } },
  { at: ["n3"], r: c => <S cam={mv(c, [0, 0, 1.0], [40, 20, 1.08])}><Kitchen f={c.f}><KitchenTable x={760} y={900} />{P(MIRA, { facing: 1, mouth: "smile" }, 900, 960, 1.1, c.f, 2)}{P(MOM, { facing: -1, mouth: "smile", hold: "keys", aR: [20, 40] }, 1350, 950, 1.1, c.f, 3)}</Kitchen></S> },
  { at: ["n3", 0.5], r: c => <USMap f={c.f} spread={0.15 + 0.6 * c.t / c.d} dots={c.t / c.d} /> },
  { at: ["n4"], r: c => <S cam={mv(c, [100, -60, 1.3], [140, -90, 1.7])}><StoreFront f={c.f} crowd={70} hands={16} press={1} /></S> },
  { at: ["title"], r: c => <TitleCard f={c.t} /> },
];
// the carts as standalone so they can slide (the StoreFront default carts are off in the opening shot)
import { Cart } from "../scenes/Store";
const StoreFrontCart: React.FC = () => <Cart x={820} y={1000} s={1.0} full />;
const StoreFrontCart2: React.FC = () => <Cart x={1120} y={1010} s={1.0} full flip />;
export const C1: React.FC = () => <ChapterPlayer ch="c1" vo={VO_C1} shots={c1} days={[["n1", "DAY 3", "2:14 A.M.", 130]]} />;
export const C1_LEN = chLen("c1", VO_C1);

// ================= C2 — a normal Tuesday =================
const kit = (c: Ctx, cam: number[][], mom: any = {}, kai: any = {}, mira: any = {}, show = "kmr") => <S cam={camAt(c.t, [[0, ...cam[0]], [c.d, ...cam[1]]])}><Kitchen f={c.f}>
  <KitchenTable x={760} y={900} />
  {show.includes("m") && P(MIRA, { facing: 1, mouth: "smile", hold: "walkie", aR: [30, 60], ...mira }, 860, 960, 1.1, c.f, 2)}
  {show.includes("k") && P(KAI, { facing: 1, mouth: "flat", eyes: 0.65, ...kai }, 420, 960, 1.1, c.f, 1)}
  {show.includes("r") && P(MOM, { facing: -1, mouth: "smile", hold: "keys", aR: [20, 40], ...mom }, 1360, 960, 1.1, c.f, 3)}
</Kitchen></S>;
const c2: Shot[] = [
  { at: ["n1"], r: c => kit(c, [[0, 0, 1.0], [30, 10, 1.06]], {}, { lL: [10, 10], lR: [-10, 10] }) },
  { at: ["mom1"], r: c => kit(c, [onHead(1360, 960, 1.12, 2.0, -120, 40), onHead(1360, 960, 1.12, 2.15, -120, 40)], { talk: c.talk("mom1"), look: [-0.7, 0.1] }, {}, {}, "r") },
  { at: ["mira1"], r: c => kit(c, [onHead(860, 960, 1.1 * 0.68, 2.6, 60, 0), onHead(860, 960, 1.1 * 0.68, 2.7, 60, 0)], {}, {}, { talk: c.talk("mira1"), aR: [60, 90], mouth: "grin", look: [0.8, -0.2] }, "m") },
  { at: ["mom2"], r: c => kit(c, [onHead(1360, 960, 1.12, 2.4, -60, 30), onHead(1360, 960, 1.12, 2.6, -60, 30)], { talk: c.talk("mom2"), mouth: "flat", brow: 0, browIn: 0.5, look: [-0.8, 0] }, {}, {}, "r") },
  { at: ["kai1"], r: c => kit(c, [onHead(420, 960, 1.1, 2.3, 60, 20), onHead(420, 960, 1.1, 2.4, 60, 20)], {}, { talk: c.talk("kai1"), mouth: "smile", eyes: 0.75, look: [0.9, 0] }, {}, "k") },
  { at: ["n2"], r: c => kit(c, [[-200, -90, 2.0], [-200, -110, 3.6]], {}, {}, {}, "") },
];
export const C2: React.FC = () => <ChapterPlayer ch="c2" vo={VO_C2} shots={c2} days={[["n1", "DAY 1", "7:02 A.M.", 150]]} />;
export const C2_LEN = chLen("c2", VO_C2);

// ================= C3 — how it started =================
const c3: Shot[] = [
  { at: ["open"], r: c => <S cam={mv(c, [-200, -80, 1.15], [0, -60, 1.2])}><Ranch f={c.f}>{P(RANCHER, { facing: 1, ...walk(c.f * 0.12) }, 700 + c.t * 3, 880, 0.8, c.f)}</Ranch></S> },
  { at: ["n2"], r: c => { const k = c.t / c.d, bit = k > 0.42, reach = ease(sat(c.t / (c.d * 0.38))); return <S cam={mv(c, [-40, -90, 1.2], [-20, -110, 1.3])}><Ranch f={c.f} inside>
    <Bat x={1121} y={238} f={c.f} s={1.1} flap={bit ? 1 : 0} />
    {P(RANCHER, { facing: 1, aR: bit ? [40, 80] : [lerp(20, 125, reach), lerp(20, 0, reach)], aL: [10, 20], mouth: bit ? "shout" : "flat", brow: bit ? 0.6 : 0, look: [0.6, -0.9], eyes: bit ? 1.25 : 1, lean: bit ? -6 : 0 }, 900, 900, 1.45, c.f)}
  </Ranch></S>; } },
  { at: ["n2", 0.72], r: c => <S cam={mv(c, onHead(900, 900, 1.45 * 1.08, 1.7, 40, 80), onHead(900, 900, 1.45 * 1.08, 1.8, 40, 80))}><Ranch f={c.f} inside>{P(RANCHER, { facing: 1, aR: [40, 100], aL: [30, 90], mouth: "frown", look: [0.4, 0.8] }, 900, 900, 1.45, c.f)}</Ranch></S> },
  { at: ["n3"], r: c => <S cam={mv(c, [161, -290, 3.0], [161, -290, 3.3])}><Ranch f={c.f} inside><Bat x={1121} y={238} f={c.f} s={1.1} /></Ranch></S> },
  { at: ["fact1"], r: c => <div style={{ position: "absolute", inset: 0, transform: `scale(${1 + 0.25 * c.t / c.d}) translate(${-60 * c.t / c.d}px, ${30 * c.t / c.d}px)` }}><NerveMicro f={c.t} /></div> },
  { at: ["n4"], r: c => <><NerveMicro f={c.t * 4 + 200} k={3} /><Big text={c.t < c.d * 0.45 ? "WEEKS" : "6 HOURS"} k={sat(c.t / 8)} color={c.t < c.d * 0.45 ? "#fff" : "#ff4a3a"} size={170} /></> },
  { at: ["n5"], r: c => <PlaneSky f={c.t} n={1} /> },
];
const walk = (ph: number) => ({ aL: [-22 * Math.sin(ph), 14], aR: [22 * Math.sin(ph), 14], lL: [24 * Math.sin(ph), 6 + 22 * Math.max(0, -Math.cos(ph))], lR: [-24 * Math.sin(ph), 6 + 22 * Math.max(0, Math.cos(ph))], bob: -Math.abs(Math.cos(ph)) * 4 });
export const C3: React.FC = () => <ChapterPlayer ch="c3" vo={VO_C3} shots={c3} days={[["open", "DAY 1", "WEST TEXAS · 5:40 A.M.", 110]]}
  facts={[["fact1", "Rabies travels along the nerves to the brain and makes animals aggressive. Once symptoms start, it's almost always fatal."]]} />;
export const C3_LEN = chLen("c3", VO_C3);

// ================= C4 — patient zero =================
const ROWS = [["13:10", "DENVER", "UA 1182", "B10", "ON TIME"], ["13:25", "ATLANTA", "DL 2207", "C3", "BOARDING"], ["13:40", "CHICAGO", "AA 302", "A7", "ON TIME"], ["13:55", "PHOENIX", "WN 418", "B2", "ON TIME"], ["14:10", "NEW YORK", "DL 911", "C9", "DELAYED"], ["14:25", "MIAMI", "AA 1450", "A3", "ON TIME"], ["14:40", "SEATTLE", "AS 77", "B6", "ON TIME"]];
const c4: Shot[] = [
  { at: ["n1"], r: c => <DepBoard f={c.f} rows={ROWS} hi={1} title="DEPARTURES · DALLAS" /> },
  { at: ["n1", 0.55], r: c => <S cam={mv(c, [-200, -40, 1.1], [100, -40, 1.1])}><Terminal f={c.f} crowd={22} gate="B12" /></S> },
  { at: ["n2"], r: c => <S cam={mv(c, onHead(900, 980, 1.3 * 1.08, 2.0, 0, 30), onHead(900, 980, 1.3 * 1.08, 2.3, 0, 30))}><Terminal f={c.f} crowd={0} gate="B12">
    {P(SICK, { facing: 1, mouth: "worried", brow: -0.4, eyes: 0.9, tears: 0, look: [0.2, 0.4], aR: [10, 30], lean: 6 + 2 * Math.sin(c.t * 0.2) }, 900, 980, 1.3, c.f)}
    <AbsoluteFillSvg><rect width={W} height={H} fill="#4a8a3a" opacity={0.12} /></AbsoluteFillSvg></Terminal></S> },
  { at: ["n3"], r: c => { const lunge = sat((c.t - 30) / 10), hitT = c.t - 40, shake = hitT > 0 && hitT < 10 ? Math.sin(hitT * 3) * 14 : 0; return <><S cam={{ ...mv(c, [-80, -120, 1.5], [-60, -140, 1.65]), x: -80 + shake }}><Terminal f={c.f} crowd={0} gate="B12">
    {P(GUARD, { facing: -1, mouth: lunge ? "o" : "flat", eyes: lunge ? 1.3 : 1, brow: lunge ? 0.8 : 0, aR: lunge ? [80, 40] : [8, 10], lean: -6 * lunge }, 1060, 960, 1.2, c.f, 4)}
    {P(SICK, { facing: 1, mouth: "open", brow: -0.7, aR: [90 * lunge + 10, 10], aL: [80 * lunge + 10, 10], lean: 18 * lunge }, 700 + 150 * lunge, 960, 1.2, c.f)}</Terminal></S>
    {hitT > 0 && hitT < 8 && <AbsoluteFill style={{ background: "#c8101a", opacity: 0.45 * (1 - hitT / 8), mixBlendMode: "multiply" }} />}</>; } },
  { at: ["n3", 0.55], r: c => <S cam={mv(c, [-100, -40, 1.15], [-40, -40, 1.2])}><Street f={c.f} kind="day" smoke={false}>{P(GUARD, { facing: 1, ...walk(c.f * 0.12), mouth: "flat" }, 640 + c.t * 3, 760, 0.85, c.f, 4)}</Street></S> },
  { at: ["n4"], r: c => <USMap f={c.f} routes={sat(c.t / (c.d * 0.8))} label="300 PASSENGERS · 40 CITIES" /> },
];
const AbsoluteFillSvg: React.FC<{ children: React.ReactNode }> = ({ children }) => <g>{children}</g>;
export const C4: React.FC = () => <ChapterPlayer ch="c4" vo={VO_C4} shots={c4} days={[["n2", "DAY 1", "ATLANTA · 4:05 P.M.", 110]]}
  facts={[["fact1", "Atlanta's airport is the busiest in the world: over 100 million passengers a year, almost 300,000 a day.", "right"]]} />;
export const C4_LEN = chLen("c4", VO_C4);

// ================= C5 — the math of the end + Mom's call =================
const aisle = (c: Ctx, cam: number[][], kai: any, light: any = "day") => <S cam={camAt(c.t, [[0, ...cam[0]], [c.d, ...cam[1]]])}><StoreAisle f={c.f} light={light}>
  <Shelf x={340} y={900} w={1100} seed={12} />
  {P(KAI, { facing: 1, ...kai }, 960, 990, 1.15, c.f, 1)}</StoreAisle></S>;
const NOTIFS: [string, string][] = [["NEWS", "Attacks reported at ATL airport"], ["MOM", "Are you at work??"], ["X", "#AtlantaAttacks is trending"], ["POLICE", "Avoid Hartsfield-Jackson area"]];
const c5: Shot[] = [
  { at: ["n1"], r: c => <Doubling f={c.f} k={c.t > c.d * 0.6 ? 0.1 : 0} /> },
  { at: ["fact1"], r: c => <Doubling f={c.f} k={0.1 + 0.25 * c.t / c.d} /> },
  { at: ["n2"], r: c => <Doubling f={c.f} k={0.36 + 0.64 * sat(c.t / (c.d * 0.85))} /> },
  { at: ["n3"], r: c => aisle(c, [[0, -60, 1.25], [0, -60, 1.3]], { hold: "can", aR: [100, 40], aL: [10, 10], look: [0.8, -0.3] }) },
  { at: ["n3", 0.6], r: c => aisle(c, [onHead(960, 990, 1.15, 2.2, 0, 60), onHead(960, 990, 1.15, 2.3, 0, 60)], { hold: "phone", aR: [52, 110], look: [0.2, 0.8], brow: 0.3 }) },
  { at: ["kai1"], r: c => <Phone f={c.f} mode={{ kind: "notifs", items: NOTIFS, n: 1 + c.t / 9 }} /> },
  { at: ["ring"], r: c => <Phone f={c.f} shake={1} mode={{ kind: "call", name: "MOM", t: 0 }} /> },
  { at: ["mom1"], r: c => <div style={{ position: "absolute", inset: 0, transform: `scale(${1.05 + 0.2 * c.t / c.d})`, transformOrigin: "45% 35%" }}><ER f={c.f} talk={c.talk("mom1")} /></div> },
  { at: ["kai2"], r: c => aisle(c, [onHead(960, 990, 1.15, 2.4, 0, 40), onHead(960, 990, 1.15, 2.6, 0, 40)], { hold: "phone", aR: [52, 110], talk: c.talk("kai2"), brow: 0, browIn: 0.8, mouth: "worried", look: [0.2, 0.7] }) },
  { at: ["mom2"], r: c => <div style={{ position: "absolute", inset: 0, transform: `scale(${1.3 + 0.2 * c.t / c.d})`, transformOrigin: "45% 30%" }}><ER f={c.f} talk={c.talk("mom2")} /></div> },
  { at: ["dead"], r: c => <Phone f={c.f} mode={{ kind: "call", name: "MOM", t: 0, ended: true }} /> },
  { at: ["n4"], r: c => aisle(c, [onHead(960, 990, 1.15, 2.4, 0, 40), [0, -40, 1.05]], { hold: "phone", aR: [30, 60], brow: 0, browIn: 0.9, mouth: "sad", tears: sat(c.t / 60), look: [0, 0.6] }, c.t % 37 < 3 ? "night" : "day") },
];
export const C5: React.FC = () => <ChapterPlayer ch="c5" vo={VO_C5} shots={c5} days={[["n3", "DAY 1", "11:04 P.M.", 110]]}
  facts={[["fact1", "2009, University of Ottawa: mathematicians modelled a zombie outbreak. Unless the response is fast and hard, zombies win."]]} />;
export const C5_LEN = chLen("c5", VO_C5);
