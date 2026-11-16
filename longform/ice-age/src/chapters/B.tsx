// Chapters 5–8: fire, the band, life in the band, the sickness.
import React from "react";
import { AbsoluteFill } from "remotion";
import { sat, lerp, rnd, W, H } from "../engine/core";
import { Glow } from "../engine/fx";
import { ChapterPlayer, Ctx, Shot, chLen } from "../Player";
import { S, mv, onHead, P, Big, walk, SIT } from "./H";
import { Riverbank, Camp, Fire, Valley, TentIn } from "../scenes/Ice";
import { Kit, Spark, PopDots, Drawing, Map1492, Germs, Boil } from "../scenes/Inserts";
import { Character } from "../chars/Rig2";
import { ELI, ELI_PACK, ELI_FUR, NIA, TOR, PIP, AMA, BAND } from "../chars/cast";
import { VO_C5 } from "../vo_c5"; import { VO_C6 } from "../vo_c6"; import { VO_C7 } from "../vo_c7"; import { VO_C8 } from "../vo_c8";

const warm = "#ffb060";
// ================= C5 — Day 2: fire =================
const river = (c: Ctx, cam: number[][], eli: any, night = 0, fire = 0) => <S cam={mv(c, cam[0], cam[1])}><Riverbank f={c.f} glint={eli.glint ?? 0}>
  {fire > 0 && <Fire x={1080} y={960} f={c.f} s={0.8 * fire} glow={fire} />}
  {eli.sticks && <g><rect x={900} y={968} width={170} height={16} rx={6} fill="#8a6a44" /><line x1={986 + 6 * Math.sin(c.f * 0.9)} y1={830} x2={984} y2={968} stroke="#6a4a2a" strokeWidth={9} strokeLinecap="round" />{eli.smoke && <circle cx={984} cy={960} r={10 + 4 * Math.sin(c.f)} fill="#c8c8c8" opacity={0.3} />}</g>}
  {P(ELI_PACK, { facing: 1, ...eli }, eli.x ?? 820, 980, 1.05, c.f, 1, fire > 0 ? warm : undefined)}
  {night > 0 && <rect x={-1000} y={-500} width={4000} height={1800} fill="#0a1030" opacity={0.55 * night} style={{ mixBlendMode: "multiply" }} />}
  {night > 0 && fire > 0 && <Glow x={1080} y={900} r={700} color="#ff9a3a" o={0.4 * fire} />}</Riverbank></S>;
const rub = (f: number) => ({ lean: 24, aR: [62 + 6 * Math.sin(f * 0.9), 52], aL: [56 - 6 * Math.sin(f * 0.9), 56], mouth: "flat" as const, brow: -0.4, sticks: true });
const c5: Shot[] = [
  { at: ["n1"], r: c => <Kit f={c.f} n={c.t / 22 + 1} /> },
  { at: ["eli1"], r: c => river(c, [onHead(820, 980, 1.05, 1.9, 60, 60), onHead(820, 980, 1.05, 2.0, 60, 60)], { ...rub(c.f), talk: c.talk("eli1"), mouth: "smile" }) },
  { at: ["n2"], r: c => river(c, [[-60, 20, 1.2], [-60, 20, 1.25]], { ...rub(c.f * 0.4), mouth: "frown", brow: 0, browIn: 0.8, eyes: 0.8 }) },
  { at: ["n3"], r: c => river(c, [[-100, 330, 1.6], [200, 360, 2.0]], { x: -600, glint: sat(c.t / 30) }) },
  { at: ["fact1"], r: c => <Spark f={c.t} /> },
  { at: ["spark"], r: c => <Spark f={c.t + 40} fire={sat(c.t / 30)} /> },
  { at: ["eli2"], r: c => river(c, [onHead(820, 980, 1.05, 2.0, 60, 40), onHead(820, 980, 1.05, 2.1, 60, 40)], { talk: c.talk("eli2"), mouth: "grin", eyes: 1.2, brow: 0.6, aR: [110 + 10 * Math.sin(c.f * 0.4), 30], aL: [100, 30] }, 0.6, 1) },
  { at: ["n5"], r: c => river(c, [[100, 60, 1.35], [120, 60, 1.4]], { ...SIT, facing: 1, hold: "can", aR: [40, 100], mouth: "smile", eyes: 0.8 }, 0.8, 1) },
  { at: ["n4"], r: c => <S cam={mv(c, [0, -60, 1.0], [0, -60, 1.08])}><Valley f={c.f} time="dusk" herd={false}>
    {[0, 1, 2, 3].map(i => <g key={i}><Character look={BAND[i]} pose={{ facing: -1, aR: [10, 20], look: [-0.8, 0.4] }} x={1520 + i * 80} y={700} s={0.32} f={c.f} seed={i + 9} /></g>)}
    <rect x={-1000} y={-500} width={4000} height={1800} fill="#0a1030" opacity={0.6} style={{ mixBlendMode: "multiply" }} /><Fire x={960} y={900} f={c.f} s={0.35} glow={0.6} /></Valley></S> },
];
export const C5: React.FC = () => <ChapterPlayer ch="c5" vo={VO_C5} shots={c5}
  facts={[["fact1", "Strike flint against pyrite and you get real sparks. Neanderthals were probably making fire this way 50,000 years ago."]]} />;
export const C5_LEN = chLen("c5", VO_C5);

// ================= C6 — Day 3: the band =================
const standoff = (c: Ctx, cam: number[][], o: { eli?: any; tor?: any; nia?: any; pip?: any; show?: string; lower?: number }) => { const show = o.show ?? "etnpb", low = o.lower ?? 0;
  return <S cam={mv(c, cam[0], cam[1])}><Riverbank f={c.f}><Fire x={760} y={970} f={c.f} s={0.45} glow={0.4} />
    {show.includes("b") && P(BAND[0], { facing: -1, hold: "spear", aR: [lerp(70, 20, low), 20], look: [0.8, 0] }, 1700, 990, 1.0, c.f, 12)}
    {show.includes("t") && P(TOR, { facing: -1, hold: "spear", aR: [lerp(80, 20, low), 10], mouth: "frown", brow: -0.5, look: [0.8, 0], ...o.tor }, 1420, 990, 1.05, c.f, 3)}
    {show.includes("n") && P(NIA, { facing: -1, hold: "spear", aR: [lerp(76, 15, low), 14], mouth: "flat", look: [0.8, 0], ...o.nia }, 1180, 990, 1.0, c.f, 4)}
    {show.includes("p") && P(PIP, { facing: -1, mouth: "o", look: [0.8, 0.2], ...o.pip }, o.pip?.x ?? 1050, 990, 1.0, c.f, 5)}
    {show.includes("e") && P(ELI_PACK, { facing: 1, aR: [60, 90], aL: [55, 95], mouth: "worried", eyes: 1.2, look: [0.8, 0], ...o.eli }, 520, 990, 1.05, c.f, 1)}</Riverbank></S>; };
const OldEnglish: React.FC<{ f: number }> = ({ f }) => <svg width={W} height={H} style={{ position: "absolute" }}><rect width={W} height={H} fill="#2a1e14" />
  <g transform={`translate(820 ${470 - f * 0.15}) rotate(-3) scale(0.86)`}><rect x={-640} y={-380} width={1280} height={760} fill="#e8d8b0" /><rect x={-610} y={-350} width={1220} height={700} fill="none" stroke="#8a5a2a" strokeWidth={6} />
    {["Fæder ūre þū þe eart on heofonum,", "sī þīn nama gehālgod.", "Tōbecume þīn rīce,", "gewurþe þīn willa…"].map((l, i) => <text key={i} x={-540} y={-200 + i * 110} fontFamily="Permanent Marker" fontSize={56} fill="#3a2010" opacity={sat((f - i * 8) / 10)}>{l}</text>)}
    <text x={0} y={320} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={40} fill="#8a2a1a">ENGLISH · ABOUT 1,000 YEARS AGO</text></g></svg>;
const c6: Shot[] = [
  { at: ["n1"], r: c => standoff(c, [[0, -20, 1.05], [0, -20, 1.1]], { eli: { ...SIT, aR: [10, 20], aL: [10, 20], eyes: c.t < 30 ? 0.1 : 1.3, mouth: c.t < 30 ? "flat" : "o" } }) },
  { at: ["tor1"], r: c => standoff(c, [onHead(1420, 990, 1.05 * 1.12, 2.2, -40, 40), onHead(1420, 990, 1.05 * 1.12, 2.35, -40, 40)], { show: "t", tor: { talk: c.talk("tor1"), mouth: "shout", brow: -0.8 } }) },
  { at: ["n2"], r: c => standoff(c, [[60, -20, 1.0], [100, -20, 1.06]], {}) },
  { at: ["fact1"], r: c => <OldEnglish f={c.t} /> },
  { at: ["eli1"], r: c => standoff(c, [onHead(520, 990, 1.05, 2.2, 40, 40), onHead(520, 990, 1.05, 2.35, 40, 40)], { show: "e", eli: { talk: c.talk("eli1"), mouth: "smile", brow: 0.5 } }) },
  { at: ["n3"], r: c => standoff(c, [[-60, 40, 1.3], [-60, 40, 1.4]], { pip: { x: lerp(1050, 880, sat(c.t / 40)), aR: [100, 0], mouth: "grin", ...walk(c.t < 40 ? c.f : 0, -1, 0.5) } }) },
  { at: ["pip1"], r: c => standoff(c, [onHead(880, 990, 0.66, 2.6, 0, 10), onHead(880, 990, 0.66, 2.75, 0, 10)], { show: "p", pip: { x: 880, talk: c.talk("pip1"), mouth: "grin", aR: [100, 0], eyes: 1.2 } }) },
  { at: ["nia1"], r: c => standoff(c, [onHead(1180, 990, 1.0, 2.3, -40, 40), onHead(1180, 990, 1.0, 2.45, -40, 40)], { show: "n", nia: { talk: c.talk("nia1"), mouth: "smile", brow: 0.4, aR: [20, 15], hold: null } }) },
  { at: ["n4"], r: c => standoff(c, [[0, -20, 1.05], [0, -20, 1.0]], { lower: sat(c.t / 30), pip: { x: 880, mouth: "grin" }, eli: { aR: [10, 20], aL: [10, 20], mouth: "smile" }, nia: { mouth: "smile" } }) },
];
export const C6: React.FC = () => <ChapterPlayer ch="c6" vo={VO_C6} shots={c6}
  facts={[["fact1", "English from 1,000 years ago is almost unreadable today. From 30,000 years ago, you'd share not a single word.", "right"]]} />;
export const C6_LEN = chLen("c6", VO_C6);

// ================= C7 — life in the band =================
const camp = (c: Ctx, cam: number[][], kids: React.ReactNode, night = false) => <S cam={mv(c, cam[0], cam[1])}><Camp f={c.f} night={night}>{kids}</Camp></S>;
const crowd = (f: number, gather = 0, pipX = 900) => <>
  {P(BAND[1], { ...SIT, facing: 1, aR: [40, 80], mouth: "smile", look: [0.8, 0.3] }, 420, 1000, 0.95, f, 21)}
  {P(BAND[3], { facing: -1, look: [-0.8, 0.2], mouth: gather ? "o" : "flat" }, 1340 - gather * 200, 1000, 1.0, f, 22)}
  {P(BAND[4], { facing: -1, mouth: "grin", look: [-0.8, 0.2] }, 1500 - gather * 300, 1010, 1.0, f, 23)}
  {P(PIP, { facing: 1, mouth: "grin", look: [0.6, 0.4], hold: gather ? "clipboard" : null, aR: gather ? [40, 80] : [10, 20] }, pipX, 1010, 1.0, f, 5)}
  {P(TOR, { facing: -1, mouth: "flat", look: [-0.8, 0.1] }, 1700, 1000, 1.05, f, 3)}</>;
const c7: Shot[] = [
  { at: ["n1"], r: c => camp(c, [[-200, -40, 1.0], [100, -40, 1.05]], <>{crowd(c.f)}{P(ELI_PACK, { facing: 1, ...walk(c.f), look: [0.8, 0], mouth: "o" }, 200 + c.t * 3, 1010, 1.0, c.f, 1)}{P(NIA, { facing: 1, ...walk(c.f + 6), hold: "spear", aR: [20, 20] }, 380 + c.t * 3, 1010, 1.0, c.f, 4)}</>) },
  { at: ["fact1"], r: c => <PopDots f={c.f} k={c.t / (c.d * 0.6)} /> },
  { at: ["n2"], r: c => camp(c, [[-200, 60, 1.35], [-160, 60, 1.4]], <>{P(AMA, { ...SIT, facing: 1, aR: [50, 90], aL: [45, 95], look: [0.9, 0.2], mouth: "smirk" }, 560, 1010, 1.0, c.f, 6)}
    {P(ELI_PACK, { facing: -1, aR: [c.t < 30 ? 70 : 20, 40], aL: [c.t < 30 ? 66 : 20, 40], mouth: c.t < 30 ? "flat" : "o", eyes: c.t < 30 ? 1 : 1.3, look: [0.4, 0.8] }, 860, 1010, 1.05, c.f, 1)}
    {c.t < 30 ? <rect x={760} y={760} width={150} height={110} rx={20} fill="#b08a60" /> : <ellipse cx={900} cy={1010} rx={90} ry={20} fill="#b08a60" />}</>) },
  { at: ["ama1"], r: c => camp(c, [onHead(560, 1010, 0.94 * 0.88, 2.4, 60, 30), onHead(560, 1010, 0.94 * 0.88, 2.55, 60, 30)], <>{P(AMA, { ...SIT, facing: 1, talk: c.talk("ama1"), mouth: "smirk", look: [0.9, 0.1], aR: [50, 90] }, 560, 1010, 1.0, c.f, 6)}</>) },
  { at: ["n3"], r: c => camp(c, [onHead(860, 1010, 1.05, 2.3, -30, 40), onHead(860, 1010, 1.05, 2.45, -30, 40)], <>{P(ELI_PACK, { facing: -1, mouth: "flat", brow: 0, browIn: 0.6, eyes: 0.8, look: [0.4, 0.5] }, 860, 1010, 1.05, c.f, 1)}</>) },
  { at: ["n3b"], r: c => <Drawing f={c.f} k={sat(c.t / (c.d * 0.55))} /> },
  { at: ["n3b", 0.62], r: c => camp(c, [[-60, 40, 1.4], [-40, 40, 1.45]], <>{crowd(c.f, 1, 880)}{P(ELI_PACK, { facing: 1, mouth: "smile", look: [0.6, 0.4] }, 700, 1010, 1.05, c.f, 1)}</>) },
  { at: ["n4"], r: c => camp(c, [onHead(820, 1010, 1.05, 2.0, 80, 40), onHead(820, 1010, 1.05, 2.15, 80, 40)], <>{P(ELI_PACK, { ...SIT, facing: 1, mouth: "flat", eyes: 0.9, look: [0.8, 0.3], aR: [40, 70], aL: [36, 72] }, 820, 1010, 1.05, c.f, 1, warm)}</>, true) },
];
export const C7: React.FC = () => <ChapterPlayer ch="c7" vo={VO_C7} shots={c7}
  facts={[["fact1", "Scientists estimate only a few thousand people lived in all of Western Europe back then — fewer than in one small town today.", "right"]]} />;
export const C7_LEN = chLen("c7", VO_C7);

// ================= C8 — Day 9: the sickness =================
// Pip lying under furs: render him upright but clip to the head and place it on the pillow (face stays upright)
const LyingPip: React.FC<{ f: number; x: number; y: number; s?: number }> = ({ f, x, y, s = 1.6 }) => <g>
  <ellipse cx={x - 40} cy={y + 30} rx={120} ry={40} fill="#d8c8a8" />
  <clipPath id="piphead"><circle cx={x} cy={y} r={70 * s * 0.66 + 30} /></clipPath>
  <g clipPath="url(#piphead)"><Character look={PIP} pose={{ facing: 1, eyes: 0.5, mouth: "sad", brow: 0, browIn: 0.9, tears: 0 }} x={x - 6 * s * 0.66} y={y + 362 * s * 0.66} s={s} f={f} seed={5} /></g>
  <path d={`M${x + 60} ${y + 20} Q${x + 260} ${y - 70} ${x + 520} ${y + 10} Q${x + 560} ${y + 90} ${x + 500} ${y + 120} L${x + 40} ${y + 120} Q${x + 10} ${y + 60} ${x + 60} ${y + 20} Z`} fill="#8a6a4a" />
  <path d={`M${x + 60} ${y + 20} ${Array.from({ length: 12 }, (_, i) => `l${20} ${i % 2 ? 10 : -10}`).join(" ")}`} stroke="#efe6d2" strokeWidth={8} fill="none" />
</g>;
const tent = (c: Ctx, cam: number[][], kids: React.ReactNode = null) => <S cam={mv(c, cam[0], cam[1])}><TentIn f={c.f}><LyingPip f={c.f} x={700} y={820} />{kids}</TentIn></S>;
const c8: Shot[] = [
  { at: ["n1"], r: c => tent(c, [[-100, 40, 1.4], [-80, 40, 1.5]], <>{P(AMA, { ...SIT, facing: -1, aR: [60, 80], mouth: "worried", brow: 0, browIn: 0.8, look: [-0.8, 0.4] }, 1240, 1000, 1.0, c.f, 6, warm)}</>) },
  { at: ["n2"], r: c => camp(c, [onHead(860, 1010, 1.05, 2.4, 0, 40), onHead(860, 1010, 1.05, 2.7, 0, 40)], <>{P(ELI_PACK, { facing: 1, mouth: "o", eyes: 1.35, brow: 0.8, look: [0, 0.6], aR: [50, 90], aL: [45, 95] }, 860, 1010, 1.05, c.f, 1)}</>) },
  { at: ["n2", 0.55], r: c => <Germs f={c.f} /> },
  { at: ["fact1"], r: c => <Map1492 f={c.f} k={c.t / (c.d * 0.7)} /> },
  { at: ["eli1"], r: c => camp(c, [onHead(860, 1010, 1.05, 2.3, 0, 40), onHead(860, 1010, 1.05, 2.4, 0, 40)], <>{P(ELI_PACK, { facing: 1, talk: c.talk("eli1"), mouth: "sad", brow: 0, browIn: 0.9, eyes: 1.1, look: [0.4, 0.6] }, 860, 1010, 1.05, c.f, 1)}</>) },
  { at: ["n3"], r: c => <Boil f={c.t} k={sat(c.t / 40)} /> },
  { at: ["eli2"], r: c => camp(c, [[-100, 20, 1.2], [-80, 20, 1.25]], <>{crowd(c.f, 1, 1060)}{P(ELI_PACK, { facing: 1, talk: c.talk("eli2"), mouth: "open", aR: [80 + 15 * Math.sin(c.f * 0.6), 30], aL: [75 - 15 * Math.sin(c.f * 0.6), 30], look: [0.8, 0] }, 700, 1010, 1.05, c.f, 1)}</>) },
  { at: ["tor1"], r: c => camp(c, [onHead(1700, 1000, 1.05 * 1.12, 2.2, -60, 40), onHead(1700, 1000, 1.05 * 1.12, 2.35, -60, 40)], <>{P(TOR, { facing: -1, talk: c.talk("tor1"), mouth: "worried", brow: 0, browIn: 0.8, look: [-0.8, 0.1] }, 1700, 1000, 1.05, c.f, 3)}</>) },
  { at: ["n4"], r: c => camp(c, [[0, -30, 1.05], [0, -30, 1.1]], <>{P(PIP, { facing: 1, ...walk(c.f * 2.5, 1, 1.2), mouth: "grin" }, 400 + ((c.t * 6) % 1200), 1010, 1.0, c.f, 5)}{P(TOR, { facing: -1, mouth: "smile", look: [-0.8, 0.1], head: 6 }, 1500, 1000, 1.05, c.f, 3)}{P(ELI_PACK, { facing: 1, mouth: "smile", look: [0.8, 0] }, 1120, 1010, 1.05, c.f, 1)}</>) },
];
export const C8: React.FC = () => <ChapterPlayer ch="c8" vo={VO_C8} shots={c8}
  facts={[["fact1", "After 1492, diseases from Europe reached people who had never met them. In some places, up to 9 in 10 died."]]} />;
export const C8_LEN = chLen("c8", VO_C8);
