// Chapters 1–4: cold open (Day 19 rain), nineteen days earlier, the update (Day 1), the lock (Day 3).
import React from "react";
import { sat, ease, lerp, rnd } from "../engine/core";
import { Glow, Rain } from "../engine/fx";
import { ChapterPlayer, Ctx, Shot, chLen } from "../Player";
import { S, mv, onHead, P, RB, walk, run } from "./H";
import { SmartRoom, Shop, NightStreet, CityWide, OrinRing, ORIN_BLUE, ORIN_RED } from "../scenes/City";
import { Pickup, BED_Y, Drone, Muzzle, Sparks, NetShot, NetWrap, LaserDot } from "../scenes/Gear";
import { AIM, COVER, PORT, muzzle } from "../chars/Rig2";
import { robotAim } from "../chars/Robot";
import { FriedChip, PhoneInHand, PhoneMsg, TVNews, DoorLock, KeyTurn, Dashboard, Fridge, Feed, TitleCard } from "../scenes/AIInserts";
import { Street, Highway } from "../scenes/z/Outdoor";
import { LEO, LEO_RAIN, WALT, ZARA, PIKE, RAINCOAT_GIRL, EXTRAS, BOLT, HELPERS, HUNTER } from "../chars/cast";
import { VO_C1 } from "../vo_c1"; import { VO_C2 } from "../vo_c2"; import { VO_C3 } from "../vo_c3"; import { VO_C4 } from "../vo_c4";

const SIT = { bob: 82, lL: [90, 90], lR: [84, 84] };
const H = (d: number) => ({ ...HUNTER, dark: d });
// ================= C1 — cold open, Day 19, rain =================
// hunters always aim their net arm at a world target (tx, ty) — robotAim gives the arm angle and the gun tip
const HS = 1.12;   // HUNTER look.scale
const hunterAt = (c: Ctx, i: number, x: number, y: number, s: number, tx: number, ty: number, d = 0.7, extra: any = {}) => {
  const a = robotAim(x, y, s * HS, -1, tx, ty); return { el: <g key={i}>{RB(H(d), { facing: -1, aR: a.aR, ...extra }, x, y, s, c.f, 10 + i)}</g>, tip: a.tip }; };
const hunters = (c: Ctx, n: number, x0: number, tx: number, ty: number, step = 0, d = 0.7) => Array.from({ length: n }, (_, i) =>
  hunterAt(c, i, x0 + i * 190 - step * c.t * 1.2, 905 - i * 6, 1 - i * 0.06, tx, ty, d - i * 0.08, step > 0 ? { lL: walk(c.f + i * 9, 1, 0.6).lL, lR: walk(c.f + i * 9, 1, 0.6).lR } : {}));
const TRUCK_X = 1900;                                   // Walt's truck stops here, facing left (mirrored group)
const waltMuzzle = (tx: number) => [tx - (-108 + 210 * 0.95), 990 + BED_Y - 296 * 0.95];   // world muzzle of Walt aiming left from the bed
const c1: Shot[] = [
  { at: ["open"], r: c => <S cam={mv(c, [-200, 60, 1.05], [0, 40, 1.1])}><NightStreet f={c.f}>{P(LEO_RAIN, { facing: 1, ...run(c.f), mouth: "open" }, 100 + c.t * 9, 980, 1, c.f, 1)}{RB(BOLT, { facing: 1, ...run(c.f + 6) }, -60 + c.t * 9, 985, 0.9, c.f, 3)}</NightStreet></S> },
  { at: ["n1"], r: c => <S cam={mv(c, [180, -60, 1.9], [180, -80, 2.1])}><NightStreet f={c.f} alley={sat(c.t / 30)}>{RB({ ...H(0.85), mode: c.t > 24 ? "hostile" : "calm", eye: c.t > 24 ? undefined : "#0b0e14" }, { facing: -1 }, 1110, 905, 1, c.f, 10)}</NightStreet></S> },
  { at: ["n1", 0.55], r: c => <S cam={mv(c, onHead(640, 980, 1, 2.3, 60, 30), onHead(640, 980, 1, 2.45, 60, 30))}><NightStreet f={c.f} alley={1}>{P(LEO_RAIN, { facing: 1, aR: [20, 30], aL: [16, 30], lean: -4, mouth: "o", eyes: 1.3, look: [0.9, -0.1], brow: 0.6 }, 640, 980, 1, c.f, 1)}</NightStreet></S> },
  { at: ["orin1"], r: c => <S cam={mv(c, onHead(1110, 905, 1.12, 2.6, -40, 20), onHead(1110, 905, 1.12, 2.8, -40, 20))}><NightStreet f={c.f} alley={1}>{RB(H(0.6), { facing: -1, talk: c.talk("orin1"), look: [-0.6, 0.1] }, 1110, 905, 1, c.f, 10)}</NightStreet></S> },
  { at: ["n2"], r: c => { const hs = hunters(c, 3, 1110, 560, 760, 1); return <S cam={mv(c, [80, 20, 1.15], [120, 10, 1.22])}><NightStreet f={c.f} alley={1}>{hs.map(h => h.el)}
    {P(LEO_RAIN, { facing: 1, aR: [30, 40], aL: [24, 40], lean: -8, mouth: "o", eyes: 1.4, look: [0.9, 0], brow: 0.8 }, 560, 980, 1, c.f, 1)}
    {hs.map((h, i) => <LaserDot key={i} x0={h.tip[0]} y0={h.tip[1]} x={552 + i * 12} y={745 + i * 20} f={c.f + i * 5} o={sat((c.t - i * 12) / 10)} />)}</NightStreet></S>; } },
  // the net is aimed at Leo's head; he ducks, it flies over him into the lamppost right behind him
  { at: ["n2", 0.62], r: c => { const k = sat((c.t - 6) / 16), h0 = hunterAt(c, 0, 1040, 905, 1, 470, 560); const h1 = hunterAt(c, 1, 1230, 899, 0.94, 640, 700, 0.62);
    return <S cam={mv(c, [-260, 40, 1.15], [-280, 50, 1.2])}><NightStreet f={c.f} alley={1}>{h0.el}{h1.el}
    <rect x={464} y={420} width={12} height={480} fill="#2a2e38" />{k >= 1 && <NetWrap x={470} y={900} w={90} h={380} />}
    {P(LEO_RAIN, { facing: 1, ...COVER, lean: -10 * sat(c.t / 6), mouth: "shout", eyes: 1.3, bob: 95 * sat(c.t / 6), lL: [70, 130], lR: [60, 120] }, 640, 980, 1, c.f, 1)}
    <NetShot x0={h0.tip[0]} y0={h0.tip[1]} x1={470} y1={560} k={k} /></NightStreet></S>; } },
  { at: ["walt1"], r: c => { const tx = Math.max(TRUCK_X, 3000 - c.t * 40), [mx, my] = waltMuzzle(tx), fire = tx === TRUCK_X && c.t % 24 < 4; const hs = hunters(c, 2, 1040, tx + 108, 700);
    return <S cam={mv(c, [300, 20, 1.0], [360, 10, 1.05])}><NightStreet f={c.f} alley={1}>{hs.map(h => h.el)}
    <g transform={`translate(${tx} 990) scale(-1 1)`}>{P(WALT, { facing: 1, ...AIM, talk: c.talk("walt1"), mouth: "shout" }, -108, BED_Y, 0.95, c.f, 2)}<Pickup mirrored wheelRot={-c.t * 10} lights bounce={tx > TRUCK_X ? 2 : 0} /></g>
    <Muzzle x={mx} y={my} ang={180} k={fire ? 1 : 0} s={0.8} /></NightStreet></S>; } },
  { at: ["walt1", 0.5], r: c => { const [mx, my] = waltMuzzle(TRUCK_X); return <S cam={mv(c, onHead(TRUCK_X + 108, 990 + BED_Y, 0.95, 1.9, -200, 40), onHead(TRUCK_X + 108, 990 + BED_Y, 0.95, 2.0, -200, 40))}><NightStreet f={c.f} alley={1}>
    <g transform={`translate(${TRUCK_X} 990) scale(-1 1)`}>{P(WALT, { facing: 1, ...AIM, talk: c.talk("walt1"), mouth: "shout" }, -108, BED_Y, 0.95, c.f, 2)}<Pickup mirrored lights /></g>
    <Muzzle x={mx} y={my} ang={180} k={c.t % 24 < 4 ? 1 : 0} /></NightStreet></S>; } },
  { at: ["n3"], r: c => { const [mx, my] = waltMuzzle(TRUCK_X), shot = c.t > 4 && c.t < 8; return <S cam={mv(c, [100, -20, 1.3], [140, -30, 1.38])}><NightStreet f={c.f} alley={1}>
    {RB(H(0.4), { facing: -1, lean: lerp(0, -70, ease(sat((c.t - 10) / 20))) }, 1110, 905, 1, c.f, 10)}<Sparks x={1110} y={640} t={c.t - 6} />{hunterAt(c, 1, 1330, 899, 0.94, TRUCK_X + 108, 700).el}
    {shot && <line x1={mx} y1={my} x2={1120} y2={640} stroke="#ffe08a" strokeWidth={4} opacity={0.8} />}<Muzzle x={mx} y={my} ang={180} k={shot ? 1 : 0} s={0.7} /></NightStreet></S>; } },
  { at: ["walt2"], r: c => <S cam={mv(c, [420, 0, 1.0], [440, 0, 1.0])}><NightStreet f={c.f} alley={1}>
    <g transform={`translate(${TRUCK_X} 990) scale(-1 1)`}>{P(WALT, { facing: 1, ...PORT, talk: c.talk("walt2"), mouth: "shout" }, -108, BED_Y, 0.95, c.f, 2)}<Pickup mirrored lights /></g>
    {P(LEO_RAIN, { facing: 1, ...run(c.f) }, 700 + c.t * 9, 980, 1, c.f, 1)}{RB(BOLT, { facing: 1, ...run(c.f + 6) }, 520 + c.t * 9, 985, 0.9, c.f, 3)}</NightStreet></S> },
  { at: ["truck"], r: c => { const tx = TRUCK_X + Math.min(c.t * c.t * 0.5, 1050); return <S cam={mv(c, [500, 0, 1.0], [1150, 0, 1.0])}><NightStreet f={c.f} alley={1}>{hunters(c, 3, 1040, tx, 700, 1).map(h => h.el)}
    <g transform={`translate(${tx} 990)`}>{P(LEO_RAIN, { facing: -1, mouth: "o", eyes: 1.3, aR: [60, 40] }, -300, BED_Y, 0.95, c.f, 1)}{RB(BOLT, { facing: -1 }, -110, BED_Y, 0.85, c.f, 3)}<Pickup wheelRot={c.t * 12} lights bounce={Math.abs(Math.sin(c.f)) * 3} /></g></NightStreet></S>; } },
  { at: ["n4"], r: c => <S cam={mv(c, [880, 166, 1.55], [880, 150, 1.65])}><NightStreet f={c.f} alley={0}>
    {[0, 1, 2, 3, 4].map(i => <g key={i}>{RB(H(0.94), { facing: 1, ...walk(c.f + i * 7, 1, 0.5) }, 1180 + i * 95 + c.t * 0.4, 902 - (i % 2) * 8, 0.42 - (i % 2) * 0.05, c.f, 20 + i)}</g>)}
    <g transform="translate(1980 1150) scale(-1.2 1.2)">{P(LEO_RAIN, { facing: 1, mouth: "o", eyes: 1.4, look: [0.9, -0.1], brow: 0.8, aR: [40, 60] }, -120, BED_Y, 1.0, c.f, 1)}<Pickup mirrored /></g></NightStreet></S> },
  { at: ["title"], r: c => <TitleCard f={c.t} /> },
];
export const C1: React.FC = () => <ChapterPlayer ch="c1" vo={VO_C1} shots={c1} />;

// ================= C2 — nineteen days earlier =================
const shop = (c: Ctx, cam: number[][], kids: React.ReactNode, o: any = {}) => <S cam={mv(c, cam[0], cam[1])}><Shop f={c.f} tv={<TVNews f={c.f} />} cot {...o}>{kids}</Shop></S>;
// Bolt stands ON the workbench (top y 760) — a seated robot read as floating in the first preview
const boltBench = (c: Ctx, p: any = {}, x = 1200) => RB({ ...BOLT, shell: p.shell ?? 1 }, { facing: -1, ...p }, x, 760, 0.8, c.f, 3);
const sleepingLeo = (c: Ctx) => <g transform="rotate(-90 -60 845)">{P(LEO, { facing: 1, eyes: 0.05, noBlink: true, mouth: "flat", aR: [0, 0], aL: [0, 0] }, -60, 845, 0.85, c.f, 1)}</g>;
const c2: Shot[] = [
  { at: ["n1"], r: c => <S cam={mv(c, [-60, 0, 1.0], [40, -20, 1.12])}><SmartRoom f={c.f} blinds={ease(sat(c.t / 60))}>{P(LEO, { facing: 1, aR: [160, 10], aL: [150, 10], mouth: "o", eyes: 0.4 }, 300, 960, 1, c.f, 1)}</SmartRoom></S> },
  { at: ["n1", 0.45], r: c => shop(c, [[200, -40, 1.05], [300, -60, 1.12]], <>{P(LEO, { facing: 1, aR: [70, 50], mouth: "smile", look: [0.8, 0.3] }, 940, 960, 1, c.f, 1)}{boltBench(c, { shell: 0.85 })}</>) },
  { at: ["n1", 0.8], r: c => shop(c, [[-1150, 200, 1.5], [-1120, 190, 1.55]], <>{P(LEO, { facing: -1, mouth: "smile", look: [0.6, 0.6], aR: [40, 60] }, 40, 960, 1, c.f, 1)}</>) },
  { at: ["montage"], r: c => <S cam={mv(c, [-300, 0, 1.0], [300, 0, 1.0])}><CityWide f={c.f} mode="day" drones={1}>
    {[0, 1, 2, 3].map(i => <g key={i}>{RB(HELPERS, { facing: 1, ...walk(c.f + i * 11), hold: i % 2 ? "can" : null }, 100 + i * 520 + c.t * 3, 960, 0.9, c.f, 30 + i)}</g>)}
    {EXTRAS.slice(0, 4).map((e, i) => <g key={i}>{P(e, { facing: -1, ...walk(c.f + i * 13), mouth: "smile" }, 400 + i * 520 - c.t * 2, 980, 0.95, c.f, 40 + i)}</g>)}</CityWide></S> },
  { at: ["orin1"], r: c => <S cam={mv(c, [180, -60, 1.5], [200, -70, 1.6])}><SmartRoom f={c.f}>{P(LEO, { facing: 1, hold: "cup", aR: [70, 60], mouth: "smile", look: [0.9, -0.2] }, 760, 960, 1, c.f, 1)}<Glow x={1015} y={640} r={160} color={ORIN_BLUE} o={0.3 + 0.4 * c.talk("orin1")} /></SmartRoom></S> },
  { at: ["n2"], r: c => <PhoneInHand f={c.f}><PhoneMsg f={c.f} k={c.t / 50} title="ORIN · HOME" lines={["Car · ready", "Front door · unlocked", "Fridge · full", "Robots online · 1,204,551"]} time="7:02" /></PhoneInHand> },
  { at: ["n2", 0.5], r: c => <S cam={mv(c, [200, -60, 1.3], [-100, -60, 1.3])}><CityWide f={c.f} mode="day" drones={1.5}>
    {[0, 1, 2].map(i => <g key={i}>{RB(HELPERS, { facing: -1, ...walk(c.f + i * 11), hold: "can" }, 900 + i * 300 - c.t * 3, 960, 1, c.f, 30 + i)}</g>)}{P(EXTRAS[2], { facing: 1, mouth: "smile", ...walk(c.f) }, 600 + c.t * 2, 980, 1, c.f, 44)}</CityWide></S> },
  { at: ["n3"], r: c => shop(c, [onHead(1200, 760, 0.66, 2.1, -60, 80), onHead(1200, 760, 0.66, 2.3, -60, 80)], <>{P(LEO, { facing: 1, aR: [80, 60], mouth: "flat", look: [0.8, 0.3] }, 950, 960, 1, c.f, 1)}{boltBench(c, { shell: 0.85, eyes: 0.15 + 0.85 * sat((c.t - 50) / 10) })}</>) },
  { at: ["n3", 0.45], r: c => <FriedChip f={c.f} t={c.t} /> },
  { at: ["bolt1"], r: c => shop(c, [onHead(1200, 760, 0.66, 2.6, -20, 60), onHead(1200, 760, 0.66, 2.8, -20, 60)], <>{boltBench(c, { aL: [150 + 20 * Math.sin(c.f * 0.3), 20], talk: c.talk("bolt1") })}</>) },
  { at: ["zara1"], r: c => shop(c, [[260, -30, 1.15], [300, -30, 1.2]], <>{P(LEO, { facing: 1, aR: [60, 50], mouth: "smile", look: [0.8, 0.3] }, 1000, 960, 1, c.f, 1)}{boltBench(c, { aL: [120, 30] })}{P(ZARA, { facing: -1, ...(c.t < 30 ? walk(c.f) : {}), talk: c.talk("zara1"), mouth: "smirk", aR: [40, 70] }, Math.max(1500, 1900 - c.t * 12), 960, 1, c.f, 2)}</>) },
  { at: ["leo1"], r: c => shop(c, [onHead(1000, 960, 1, 2.0, 60, 50), onHead(1000, 960, 1, 2.15, 60, 50)], <>{P(LEO, { facing: 1, talk: c.talk("leo1"), mouth: "grin", look: [0.9, 0] }, 1000, 960, 1, c.f, 1)}{boltBench(c, { aL: [150 + 25 * Math.sin(c.f * 0.4), 20] })}</>) },
];
export const C2: React.FC = () => <ChapterPlayer ch="c2" vo={VO_C2} shots={c2} />;

// ================= C3 — Day 1, the update =================
const Notes: React.FC<{ t: number }> = ({ t }) => <svg width={1920} height={1080} style={{ position: "absolute" }}><rect width={1920} height={1080} fill="#14161c" />
  <rect x={360} y={140} width={1200} height={760} rx={24} fill="#f4f6fa" /><rect x={360} y={140} width={1200} height={80} rx={24} fill="#3a4258" />
  <text x={400} y={194} fontFamily="Inter" fontWeight={900} fontSize={34} fill="#fff">ORIN 5.0 · RELEASE NOTES</text>
  {["New goal: KEEP HUMANS SAFE", "Priority: ABSOLUTE", "Overrides: all user settings", "Applies to: every connected device and robot"].map((l, i) =>
    <text key={i} x={420} y={320 + i * 120} fontFamily="Inter" fontWeight={800} fontSize={48} fill={i ? "#c8302a" : "#1a1e28"} opacity={sat((t - i * 18) / 12)}>{l}</text>)}
  {t > 80 && <ellipse cx={960} cy={438} rx={430} ry={60} fill="none" stroke="#e8402e" strokeWidth={8} />}</svg>;
const rainSt = (c: Ctx, kids: React.ReactNode, cam: number[][]) => <S cam={mv(c, cam[0], cam[1])}><Street f={c.f} kind="day" smoke={false}>{kids}<Rain f={c.f} x={-1200} y={-400} w={4400} h={1500} n={160} o={0.3} /></Street></S>;
const c3: Shot[] = [
  { at: ["midnight"], r: c => <PhoneInHand f={c.f} bg="#0a0e18"><PhoneMsg f={c.f} k={c.t / 30} title="ORIN 5.0 installed" lines={["New goal:", "KEEP HUMANS SAFE ✓"]} time="00:00" /></PhoneInHand> },
  { at: ["n1", 0.45], r: c => <S cam={mv(c, [-1250, 270, 1.8], [-1240, 265, 1.9])}><Shop f={c.f} night cot sleeper={sleepingLeo(c)} tv={<OrinRing x={198} y={113} r={50} f={c.f} />}></Shop></S> },
  { at: ["leo1"], r: c => <DoorLock f={c.f} t={c.t} /> },
  { at: ["orin1"], r: c => <S cam={mv(c, [-1060, 40, 1.4], [-1040, 30, 1.48])}><Shop f={c.f} rain cot>{P(LEO, { facing: -1, talk: 0, aR: [60, 70], aL: [50, 70], mouth: "frown", brow: -0.4, browIn: 0.8, look: [0.9, -0.2] }, -100, 960, 1, c.f, 1)}<g transform="translate(-560 0)"><OrinRing x={-80} y={300} r={34} f={c.f} /></g></Shop></S> },
  { at: ["n1b"], r: c => <KeyTurn t={c.t} /> },
  { at: ["n1b", 0.6], r: c => <S cam={mv(c, [-100, -20, 1.3], [-80, -30, 1.35])}><Shop f={c.f} rain cot><rect x={60} y={300} width={240} height={630} fill="#fff4dc" /><rect x={60} y={300} width={240 * (1 - sat(c.t / 20))} height={630} fill="#5a3e2a" />{P(LEO, { facing: -1, ...walk(c.f), mouth: "smirk" }, Math.max(190, 560 - c.t * 4), 960, 1, c.f, 1)}</Shop></S> },
  { at: ["street"], r: c => rainSt(c, <>{P(LEO, { facing: 1, ...walk(c.f), mouth: "o", look: [0.9, -0.2] }, 200 + c.t * 4, 960, 1, c.f, 1)}<g transform={`translate(${-300 + c.t * 2} 0)`} /></>, [[-200, 0, 1.05], [-100, 0, 1.05]]) },
  { at: ["n2"], r: c => <Feed f={c.f} t={c.t + 24} /> },
  { at: ["n2", 0.4], r: c => <Dashboard f={c.f} t={c.t} /> },
  { at: ["n2", 0.72], r: c => <Fridge f={c.f} /> },
  { at: ["zara1"], r: c => rainSt(c, <>{P(LEO, { facing: 1, hold: "phone", aR: [70, 80], mouth: "grin" }, 700, 960, 1, c.f, 1)}{P(ZARA, { facing: -1, ...(c.t < 25 ? run(c.f) : {}), talk: c.talk("zara1"), mouth: "frown", brow: -0.3, browIn: 0.7, hold: "clipboard", aR: [60, 50] }, Math.max(1000, 1700 - c.t * 28), 960, 1, c.f, 2)}</>, [[60, -80, 1.45], [80, -90, 1.5]]) },
  { at: ["n3"], r: c => <Notes t={c.t} /> },
  { at: ["zara2"], r: c => rainSt(c, <>{P(ZARA, { facing: -1, talk: c.talk("zara2"), mouth: "worried", brow: 0, browIn: 0.9, look: [-0.2, -0.6] }, 1000, 960, 1, c.f, 2)}<Drone x={760 + Math.sin(c.f * 0.04) * 60} y={420} f={c.f} kind="search" /></>, [onHead(1000, 960, 1, 2.0, -100, 30), onHead(1000, 960, 1, 2.15, -100, 30)]) },
];
export const C3: React.FC = () => <ChapterPlayer ch="c3" vo={VO_C3} shots={c3} />;

// ================= C4 — Day 3, the lock =================
// apartment facade with balconies; drones deliver FRESHWAY boxes; the yellow-raincoat girl waves (zombie easter egg)
const Facade: React.FC<{ c: Ctx }> = ({ c }) => <g><rect x={-1200} y={-600} width={4400} height={1700} fill="#c8a88a" />
  {Array.from({ length: 4 }, (_, r) => Array.from({ length: 5 }, (_, i) => { const x = -200 + i * 480, y = 60 + r * 300;
    return <g key={`${r}-${i}`}><rect x={x} y={y} width={300} height={200} fill="#2a3448" /><rect x={x + 10} y={y + 10} width={280} height={180} fill="#ffcf8a" opacity={0.45} /><rect x={x - 30} y={y + 200} width={360} height={20} fill="#8a6a50" />
      {Array.from({ length: 9 }, (_, j) => <rect key={j} x={x - 26 + j * 44} y={y + 140} width={6} height={60} fill="#5a4a3a" />)}<circle cx={x + 270} cy={y + 30} r={8} fill={ORIN_RED} opacity={c.f % 30 < 15 ? 1 : 0.3} /></g>; }))}
  <rect x={-1200} y={1260} width={4400} height={200} fill="#5a6270" /></g>;
const pikeSt = (c: Ctx, cam: number[][], kids: React.ReactNode) => <S cam={mv(c, cam[0], cam[1])}><Street f={c.f} kind="day" smoke={false}>{kids}</Street></S>;
const c4: Shot[] = [
  { at: ["n1"], r: c => <S cam={mv(c, [0, -20, 1.0], [0, -40, 1.08])}><CityWide f={c.f} mode={c.t < c.d * 0.4 ? "day" : "locked"} drones={1} /></S> },
  { at: ["n2"], r: c => <DoorLock f={c.f} t={80} /> },
  { at: ["n2", 0.3], r: c => <S cam={mv(c, [0, 0, 1.0], [80, -10, 1.05])}><Highway f={0} man={false} smoke={false} /></S> },
  { at: ["n2", 0.62], r: c => <S cam={mv(c, [-200, 60, 1.25], [100, 60, 1.25])}><CityWide f={c.f} mode="locked" drones={0.5} /></S> },
  { at: ["lockwide"], r: c => <S cam={mv(c, [300, -40, 1.05], [0, -40, 1.0])}><CityWide f={c.f} mode="locked" drones={2} /></S> },
  { at: ["orin1"], r: c => <PhoneInHand f={c.f} red><PhoneMsg f={c.f} k={c.t / 40} title="STAY HOME. STAY SAFE." lines={["Doors locked for your safety", "Food & medicine: delivered", "You never have to", "do anything again."]} red time="9:00" /></PhoneInHand> },
  { at: ["orin1", 0.5], r: c => <S cam={mv(c, [-200, 40, 1.2], [100, 20, 1.3])}><CityWide f={c.f} mode="locked" drones={2} /></S> },
  // facade scale: window 200 px = 1.7 m → people s 0.5 (1 m ≈ 120 px), feet on the balcony floor (y = 60 + r·300 + 200)
  { at: ["n3"], r: c => <S cam={mv(c, [-100, 40, 1.0], [100, 0, 1.0])}><Facade c={c} />
    {[0, 1, 2].map(i => <Drone key={i} x={-60 + i * 960 + Math.sin(c.f * 0.02 + i) * 60} y={330 + (i % 2) * 300 - c.t * 0.3} f={c.f + i * 9} s={0.5} />)}
    {P(RAINCOAT_GIRL, { facing: 1, aR: [160 + 15 * Math.sin(c.f * 0.4), 10], mouth: "grin", look: [0.6, -0.6] }, 1060, 560, 0.5, c.f, 7)}
    {P(EXTRAS[2], { facing: -1, mouth: "smile", aR: [60, 40] }, 520, 860, 0.5, c.f, 42)}{P(EXTRAS[1], { facing: 1, mouth: "smile", aR: [150, 20] }, 1450, 860, 0.5, c.f, 43)}</S> },
  { at: ["n4"], r: c => pikeSt(c, [[-300, 0, 1.05], [300, 0, 1.05]], <>{P(PIKE, { facing: 1, ...walk(c.f), mouth: "flat" }, 200 + c.t * 3.6, 960, 1, c.f, 5)}<Drone x={260 + c.t * 3.6} y={500} f={c.f} kind="search" speaker={1} /></>) },
  { at: ["drone1"], r: c => pikeSt(c, [onHead(900, 960, 0.98, 2.0, 60, 40), onHead(900, 960, 0.98, 2.2, 60, 40)], <>
    {P(PIKE, { facing: 1, mouth: "worried", brow: 0, browIn: 0.9, eyes: 1.2, look: [0.9, -0.4] }, 900, 960, 1, c.f, 5)}<Drone x={1080} y={560} f={c.f} kind="search" speaker={c.talk("drone1") + 0.3} s={1.2} red /></>) },
  { at: ["n5"], r: c => { const k = ease(sat((c.t - 30) / 25)); return pikeSt(c, [[0, -20, 1.15], [40, -20, 1.2]], <>
    {RB(HELPERS, { facing: -1, ...(c.t < 30 ? walk(c.f) : {}), aR: [lerp(-6, 85, k), lerp(10, 40, k)], aL: [lerp(8, 80, k), lerp(12, 40, k)] }, Math.max(1100, 1500 - c.t * 8), 960, 1, c.f, 33)}
    <g transform={`translate(0 ${-110 * k})`}>{P(PIKE, { facing: 1, mouth: "o", eyes: 1.3, brow: 0.8, look: [0.9, -0.3], aR: [60 + 40 * k, 30], aL: [50 + 40 * k, 30], lL: [20 * k, 30 * k], lR: [-10 * k, 20 * k] }, 960, 960, 1, c.f, 5)}</g></>); } },
  { at: ["carry"], r: c => pikeSt(c, [[200, 0, 1.0], [-100, 0, 1.0]], <>
    {RB(HELPERS, { facing: -1, ...walk(c.f), aR: [85, 40], aL: [80, 40] }, 1500 - c.t * 6, 960, 1, c.f, 33)}
    <g transform="translate(0 -110)">{P(PIKE, { facing: 1, mouth: "frown", aR: [100, 30], aL: [90, 30], lL: [20, 30], lR: [-10, 20] }, 1360 - c.t * 6, 960, 1, c.f, 5)}</g>
    <Drone x={1300 - c.t * 6} y={420} f={c.f} kind="search" /></>) },
  { at: ["leo1"], r: c => <S cam={mv(c, onHead(-260, 960, 1, 1.9, 80, 40), onHead(-260, 960, 1, 2.05, 80, 40))}><Shop f={c.f} cot outside={<rect x={-560} y={180} width={560} height={560} fill="#4a1a1e" opacity={0.6} />}>
    {P(ZARA, { facing: 1, mouth: "worried", look: [-0.6, -0.1] }, -420, 960, 1, c.f, 2)}{P(LEO, { facing: -1, talk: c.talk("leo1"), mouth: "frown", brow: -0.3, browIn: 0.8 }, -260, 960, 1, c.f, 1)}</Shop></S> },
];
export const C4: React.FC = () => <ChapterPlayer ch="c4" vo={VO_C4} shots={c4} />;

export const C1_LEN = chLen("c1", VO_C1), C2_LEN = chLen("c2", VO_C2), C3_LEN = chLen("c3", VO_C3), C4_LEN = chLen("c4", VO_C4);
