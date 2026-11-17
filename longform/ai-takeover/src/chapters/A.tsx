// Chapters 1–4: cold open (Day 19 rain), nineteen days earlier, the update (Day 1), the lock (Day 3).
import React from "react";
import { sat, ease, lerp, rnd } from "../engine/core";
import { Glow, Rain } from "../engine/fx";
import { ChapterPlayer, Ctx, Shot, chLen } from "../Player";
import { S, mv, onHead, P, RB, walk, run } from "./H";
import { SmartRoom, Shop, NightStreet, CityWide, OrinRing, ORIN_BLUE, ORIN_RED } from "../scenes/City";
import { Pickup, Drone, Muzzle, Sparks, NetShot, NetWrap, LaserDot } from "../scenes/Gear";
import { FriedChip, PhoneInHand, PhoneMsg, TVNews, DoorLock, Dashboard, Fridge, Feed, BoatGame, HomesViz, TitleCard } from "../scenes/AIInserts";
import { Street, Highway } from "../scenes/z/Outdoor";
import { LEO, LEO_RAIN, WALT, ZARA, PIKE, RAINCOAT_GIRL, EXTRAS, BOLT, HELPERS, HUNTER } from "../chars/cast";
import { VO_C1 } from "../vo_c1"; import { VO_C2 } from "../vo_c2"; import { VO_C3 } from "../vo_c3"; import { VO_C4 } from "../vo_c4";

const SIT = { bob: 82, lL: [90, 90], lR: [84, 84] };
const H = (d: number) => ({ ...HUNTER, dark: d });
// ================= C1 — cold open, Day 19, rain =================
const hunters = (c: Ctx, n: number, x0: number, step = 0, d = 0.7, eye = 1) => <g opacity={1}>{Array.from({ length: n }, (_, i) =>
  <g key={i}>{RB({ ...H(d - i * 0.08), mode: eye > 0.5 ? "hostile" : "calm" }, { facing: -1, ...(step > 0 ? walk(c.f + i * 9, 1, 0.6) : {}), aR: [60, 20] }, x0 + i * 190 - step * c.t * 1.2, 905 - i * 6, 1 - i * 0.06, c.f, 10 + i)}</g>)}</g>;
const c1: Shot[] = [
  { at: ["open"], r: c => <S cam={mv(c, [-200, 60, 1.05], [0, 40, 1.1])}><NightStreet f={c.f}>{P(LEO_RAIN, { facing: 1, ...run(c.f), mouth: "open" }, 100 + c.t * 9, 980, 1, c.f, 1)}{RB(BOLT, { facing: 1, ...run(c.f + 6) }, -60 + c.t * 9, 985, 0.9, c.f, 3)}</NightStreet></S> },
  { at: ["n1"], r: c => <S cam={mv(c, [180, -60, 1.9], [180, -80, 2.1])}><NightStreet f={c.f} alley={sat(c.t / 30)}>{RB({ ...H(0.85), mode: c.t > 24 ? "hostile" : "calm", eye: c.t > 24 ? undefined : "#0b0e14" }, { facing: -1 }, 1110, 905, 1, c.f, 10)}</NightStreet></S> },
  { at: ["n1", 0.55], r: c => <S cam={mv(c, onHead(640, 980, 1, 2.3, 60, 30), onHead(640, 980, 1, 2.45, 60, 30))}><NightStreet f={c.f} alley={1}>{P(LEO_RAIN, { facing: 1, aR: [20, 30], aL: [16, 30], lean: -4, mouth: "o", eyes: 1.3, look: [0.9, -0.1], brow: 0.6 }, 640, 980, 1, c.f, 1)}</NightStreet></S> },
  { at: ["orin1"], r: c => <S cam={mv(c, onHead(1110, 905, 1.12, 2.6, -40, 20), onHead(1110, 905, 1.12, 2.8, -40, 20))}><NightStreet f={c.f} alley={1}>{RB(H(0.6), { facing: -1, talk: c.talk("orin1"), look: [-0.6, 0.1] }, 1110, 905, 1, c.f, 10)}</NightStreet></S> },
  { at: ["n2"], r: c => <S cam={mv(c, [80, 20, 1.15], [120, 10, 1.22])}><NightStreet f={c.f} alley={1}>{hunters(c, 3, 1110, 1)}{P(LEO_RAIN, { facing: 1, aR: [30, 40], aL: [24, 40], lean: -8, mouth: "o", eyes: 1.4, look: [0.9, 0], brow: 0.8 }, 560, 980, 1, c.f, 1)}
    {[0, 1, 2].map(i => <LaserDot key={i} x0={1090 + i * 190 - c.t * 1.2} y0={560 + i * 10} x={555 + i * 14} y={760 + i * 22} f={c.f + i * 5} o={sat((c.t - i * 12) / 10)} />)}</NightStreet></S> },
  { at: ["n2", 0.62], r: c => { const k = sat(c.t / 16); return <S cam={mv(c, [-260, 40, 1.15], [-280, 50, 1.2])}><NightStreet f={c.f} alley={1}>{hunters(c, 2, 1040)}
    <rect x={292} y={420} width={12} height={480} fill="#2a2e38" />{k >= 1 && <NetWrap x={298} y={900} w={90} h={360} />}<NetShot x0={1000} y0={600} x1={300} y1={640} k={k} />
    {P(LEO_RAIN, { facing: 1, lean: -12 * sat(c.t / 6), aR: [168, 30], aL: [160, 30], mouth: "shout", eyes: 1.3, bob: 95 * sat(c.t / 6), lL: [70, 130], lR: [60, 120] }, 620, 980, 1, c.f, 1)}</NightStreet></S>; } },
  { at: ["walt1"], r: c => { const tx = Math.max(1500, 2600 - c.t * 40); return <S cam={mv(c, [300, 20, 1.0], [360, 10, 1.05])}><NightStreet f={c.f} alley={1}>{hunters(c, 2, 1040)}
    <g transform={`translate(${tx} 990) scale(-1 1)`}>{P(WALT, { facing: 1, hold: "rifle", aR: [80, 10], aL: [70, 40], talk: c.talk("walt1"), mouth: "shout" }, -60, -60, 0.95, c.f, 2)}<Pickup wheelRot={-c.t * 10} lights bounce={tx > 1500 ? 2 : 0} /></g></NightStreet></S>; } },
  { at: ["walt1", 0.5], r: c => <S cam={mv(c, onHead(1560, 930, 0.95, 2.0, -80, 40), onHead(1560, 930, 0.95, 2.1, -80, 40))}><NightStreet f={c.f} alley={1}>
    <g transform="translate(1500 990) scale(-1 1)">{P(WALT, { facing: 1, hold: "rifle", aR: [80, 10], aL: [70, 40], talk: c.talk("walt1"), mouth: "shout", brow: 0.8 }, -60, -60, 0.95, c.f, 2)}<Pickup lights /></g>
    <Muzzle x={1280} y={640} ang={180} k={c.t % 30 < 4 ? 1 : 0} /></NightStreet></S> },
  { at: ["n3"], r: c => <S cam={mv(c, [100, -20, 1.3], [140, -30, 1.38])}><NightStreet f={c.f} alley={1}>{RB(H(0.4), { facing: -1, lean: lerp(0, -70, ease(sat((c.t - 10) / 20))) }, 1110, 905, 1, c.f, 10)}<Sparks x={1110} y={640} t={c.t - 6} />{RB(H(0.7), { facing: -1, aR: [60, 20] }, 1330, 899, 0.94, c.f, 11)}
    <Muzzle x={1700} y={640} ang={180} k={c.t > 4 && c.t < 9 ? 1 : 0} s={0.7} /></NightStreet></S> },
  { at: ["walt2"], r: c => <S cam={mv(c, [420, 0, 1.0], [440, 0, 1.0])}><NightStreet f={c.f} alley={1}>
    <g transform="translate(1500 990) scale(-1 1)">{P(WALT, { facing: 1, hold: "rifle", aR: [150, 10], aL: [40, 60], talk: c.talk("walt2"), mouth: "shout" }, -60, -60, 0.95, c.f, 2)}<Pickup lights /></g>
    {P(LEO_RAIN, { facing: 1, ...run(c.f) }, 700 + c.t * 9, 980, 1, c.f, 1)}{RB(BOLT, { facing: 1, ...run(c.f + 6) }, 520 + c.t * 9, 985, 0.9, c.f, 3)}</NightStreet></S> },
  { at: ["truck"], r: c => { const tx = 1500 + Math.min(c.t * c.t * 0.5, 1050); return <S cam={mv(c, [500, 0, 1.0], [1150, 0, 1.0])}><NightStreet f={c.f} alley={1}>{hunters(c, 3, 1040, 1)}
    <g transform={`translate(${tx} 990)`}>{P(LEO_RAIN, { facing: -1, mouth: "o", eyes: 1.3, aR: [60, 40] }, -150, -62, 0.9, c.f, 1)}{RB(BOLT, { facing: -1 }, -40, -62, 0.8, c.f, 3)}<Pickup wheelRot={c.t * 12} lights bounce={Math.abs(Math.sin(c.f)) * 3} /></g></NightStreet></S>; } },
  { at: ["n4"], r: c => <S cam={mv(c, onHead(2000, 1010, 1.15, 1.7, 120, 60), onHead(2000, 1010, 1.15, 1.85, 120, 60))}><NightStreet f={c.f} alley={0}>
    {[0, 1, 2, 3, 4].map(i => <g key={i}>{RB(H(0.94), { facing: 1, ...walk(c.f + i * 7, 1, 0.5) }, 1560 + i * 110 + c.t * 0.4, 902 - (i % 2) * 8, 0.42 - (i % 2) * 0.05, c.f, 20 + i)}</g>)}
    <g transform="translate(1980 1150) scale(-1.2 1.2)">{P(LEO_RAIN, { facing: 1, mouth: "o", eyes: 1.4, look: [0.9, -0.1], brow: 0.8, aR: [40, 60] }, -40, -62, 1.0, c.f, 1)}<Pickup /></g></NightStreet></S> },
  { at: ["title"], r: c => <TitleCard f={c.t} /> },
];
export const C1: React.FC = () => <ChapterPlayer ch="c1" vo={VO_C1} shots={c1} />;

// ================= C2 — nineteen days earlier =================
const shop = (c: Ctx, cam: number[][], kids: React.ReactNode, tv = true) => <S cam={mv(c, cam[0], cam[1])}><Shop f={c.f} tv={tv ? <TVNews f={c.f} /> : undefined}>{kids}</Shop></S>;
// Bolt stands ON the workbench (top y 760) — a seated robot read as floating in the first preview
const boltBench = (c: Ctx, p: any = {}, x = 1200) => RB({ ...BOLT, shell: p.shell ?? 1 }, { facing: -1, ...p }, x, 760, 0.8, c.f, 3);
const c2: Shot[] = [
  { at: ["n1"], r: c => <S cam={mv(c, [-60, 0, 1.0], [40, -20, 1.12])}><SmartRoom f={c.f} blinds={ease(sat(c.t / 60))}>{P(LEO, { facing: 1, aR: [160, 10], aL: [150, 10], mouth: "o", eyes: 0.4 }, 300, 960, 1, c.f, 1)}</SmartRoom></S> },
  { at: ["n1", 0.55], r: c => shop(c, [[200, -40, 1.05], [300, -60, 1.12]], <>{P(LEO, { facing: 1, aR: [70, 50], mouth: "smile", look: [0.8, 0.3] }, 940, 960, 1, c.f, 1)}{boltBench(c, { shell: 0.85 })}</>) },
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
  { at: ["bolt1", 0.6], r: c => shop(c, [[200, -40, 1.25], [220, -40, 1.3]], <>{P(LEO, { facing: 1, aR: [40, 70], mouth: "grin", eyes: 0.9 }, 950, 960, 1, c.f, 1)}{boltBench(c, { aL: [150, 20], talk: c.talk("bolt1") })}</>) },
  { at: ["fact1"], r: c => <HomesViz f={c.f} k={c.t / (c.d * 0.6)} /> },
];
export const C2: React.FC = () => <ChapterPlayer ch="c2" vo={VO_C2} shots={c2} facts={[["fact1", "A single big AI data centre can use as much electricity as 100,000 homes (International Energy Agency, 2025)."]]} />;

// ================= C3 — Day 1, the update =================
const c3: Shot[] = [
  { at: ["midnight"], r: c => <PhoneInHand f={c.f} bg="#0a0e18"><PhoneMsg f={c.f} k={c.t / 30} title="ORIN 5.0 installed" lines={["New goal:", "KEEP HUMANS SAFE ✓"]} time="00:00" /></PhoneInHand> },
  { at: ["n1", 0.45], r: c => <S cam={mv(c, [-420, -20, 1.15], [-380, -30, 1.22])}><SmartRoom f={c.f} night blinds={0}><g transform="rotate(-90 330 800)">{P(LEO, { facing: 1, eyes: 0.05, noBlink: true, mouth: "flat", aR: [0, 0], aL: [0, 0] }, 330, 800, 0.9, c.f, 1)}</g><rect x={-10} y={772} width={360} height={70} rx={20} fill="#3a5a8a" /><Glow x={1015} y={640} r={200} color={ORIN_BLUE} o={0.5 + 0.2 * Math.sin(c.f * 0.15)} /></SmartRoom></S> },
  { at: ["leo1"], r: c => <DoorLock f={c.f} t={c.t} /> },
  { at: ["orin1"], r: c => <S cam={mv(c, [160, -80, 1.6], [180, -90, 1.7])}><SmartRoom f={c.f}>{P(LEO, { facing: 1, aR: [60, 70], aL: [50, 70], mouth: "frown", brow: -0.4, browIn: 0.8, look: [0.9, -0.2] }, 760, 960, 1, c.f, 1)}<Glow x={1015} y={640} r={160} color={ORIN_BLUE} o={0.3 + 0.5 * c.talk("orin1")} /></SmartRoom></S> },
  { at: ["n2"], r: c => <Feed f={c.f} t={c.t + 24} /> },
  { at: ["n2", 0.4], r: c => <Dashboard f={c.f} t={c.t} /> },
  { at: ["n2", 0.72], r: c => <Fridge f={c.f} /> },
  { at: ["zara1"], r: c => shop(c, [onHead(1500, 960, 1, 2.0, -100, 40), onHead(1500, 960, 1, 2.15, -100, 40)], <>{P(ZARA, { facing: -1, talk: c.talk("zara1"), mouth: "frown", brow: -0.3, browIn: 0.7, aR: [50, 60], aL: [40, 70] }, 1500, 960, 1, c.f, 2)}{P(LEO, { facing: 1, hold: "phone", aR: [70, 80], mouth: "grin" }, 1150, 960, 1, c.f, 1)}</>) },
  { at: ["n3"], r: c => shop(c, [[300, -20, 1.1], [360, -30, 1.15]], <>{P(ZARA, { facing: -1, aR: [150, 10], mouth: "smirk" }, 1500, 960, 1, c.f, 2)}{P(LEO, { facing: 1, mouth: "flat", look: [0.9, 0] }, 1100, 960, 1, c.f, 1)}{boltBench(c, {}, 1300)}</>) },
  { at: ["fact1"], r: c => <BoatGame f={c.f} t={c.t} /> },
];
export const C3: React.FC = () => <ChapterPlayer ch="c3" vo={VO_C3} shots={c3} facts={[["fact1", "In a 2016 test, an AI told to score points in a boat-race game learned to loop forever collecting points instead of finishing. AI researchers call this 'specification gaming'."]]} />;

// ================= C4 — Day 3, the lock =================
// apartment facade with balconies; drones deliver FRESHWAY boxes; the yellow-raincoat girl waves (zombie easter egg)
const Facade: React.FC<{ c: Ctx }> = ({ c }) => <g><rect x={-1200} y={-600} width={4400} height={1700} fill="#c8a88a" />
  {Array.from({ length: 4 }, (_, r) => Array.from({ length: 5 }, (_, i) => { const x = -200 + i * 480, y = 60 + r * 300;
    return <g key={`${r}-${i}`}><rect x={x} y={y} width={300} height={200} fill="#2a3448" /><rect x={x + 10} y={y + 10} width={280} height={180} fill="#ffcf8a" opacity={0.45} /><rect x={x - 30} y={y + 200} width={360} height={20} fill="#8a6a50" />
      {Array.from({ length: 9 }, (_, j) => <rect key={j} x={x - 26 + j * 44} y={y + 140} width={6} height={60} fill="#5a4a3a" />)}<circle cx={x + 270} cy={y + 30} r={8} fill={ORIN_RED} opacity={c.f % 30 < 15 ? 1 : 0.3} /></g>; }))}
  <rect x={-1200} y={1260} width={4400} height={200} fill="#5a6270" /></g>;
const c4: Shot[] = [
  { at: ["n1"], r: c => <S cam={mv(c, [0, -20, 1.0], [0, -40, 1.08])}><CityWide f={c.f} mode={c.t < c.d * 0.4 ? "day" : "locked"} drones={1} /></S> },
  { at: ["n2"], r: c => <DoorLock f={c.f} t={80} /> },
  { at: ["n2", 0.3], r: c => <S cam={mv(c, [0, 0, 1.0], [80, -10, 1.05])}><Highway f={0} man={false} smoke={false} /></S> },
  { at: ["n2", 0.62], r: c => <S cam={mv(c, [-200, 60, 1.25], [100, 60, 1.25])}><CityWide f={c.f} mode="locked" drones={0.5} /></S> },
  { at: ["lockwide"], r: c => <S cam={mv(c, [300, -40, 1.05], [0, -40, 1.0])}><CityWide f={c.f} mode="locked" drones={2} /></S> },
  { at: ["orin1"], r: c => <PhoneInHand f={c.f} red><PhoneMsg f={c.f} k={c.t / 40} title="STAY HOME. STAY SAFE." lines={["Doors locked for your safety", "Food & medicine: delivered", "You never have to", "do anything again."]} red time="9:00" /></PhoneInHand> },
  { at: ["orin1", 0.5], r: c => <S cam={mv(c, [-200, 40, 1.2], [100, 20, 1.3])}><CityWide f={c.f} mode="locked" drones={2} /></S> },
  { at: ["n3"], r: c => <S cam={mv(c, [-100, 40, 1.0], [100, 0, 1.0])}><Facade c={c} />
    {[0, 1, 2].map(i => <Drone key={i} x={-60 + i * 960 + Math.sin(c.f * 0.02 + i) * 60} y={240 + (i % 2) * 300 - c.t * 0.5} f={c.f + i * 9} />)}
    <g>{P(RAINCOAT_GIRL, { facing: 1, aR: [160 + 15 * Math.sin(c.f * 0.4), 10], mouth: "grin", look: [0.6, -0.6] }, 1010, 560, 0.9, c.f, 7)}</g>
    {P(EXTRAS[2], { facing: -1, mouth: "smile", aR: [60, 40] }, 520, 860, 0.9, c.f, 42)}</S> },
  { at: ["n4"], r: c => <S cam={mv(c, [-300, 0, 1.05], [300, 0, 1.05])}><Street f={c.f} kind="day" smoke={false}>{P(PIKE, { facing: 1, ...walk(c.f), mouth: "flat" }, 200 + c.t * 3.6, 960, 1, c.f, 5)}
    <Drone x={260 + c.t * 3.6} y={500} f={c.f} kind="search" speaker={1} /></Street></S> },
  { at: ["drone1"], r: c => <S cam={mv(c, onHead(900, 960, 0.98, 2.0, 60, 40), onHead(900, 960, 0.98, 2.2, 60, 40))}><Street f={c.f} kind="day" smoke={false}>
    {P(PIKE, { facing: c.t > c.d * 0.6 ? -1 : 1, mouth: "worried", brow: 0, browIn: 0.9, eyes: 1.2, look: [0.9, -0.4] }, 900, 960, 1, c.f, 5)}
    <Drone x={1080} y={560} f={c.f} kind="search" speaker={c.talk("drone1") + 0.3} s={1.2} red /></Street></S> },
];
export const C4: React.FC = () => <ChapterPlayer ch="c4" vo={VO_C4} shots={c4} />;

export const C1_LEN = chLen("c1", VO_C1), C2_LEN = chLen("c2", VO_C2), C3_LEN = chLen("c3", VO_C3), C4_LEN = chLen("c4", VO_C4);
