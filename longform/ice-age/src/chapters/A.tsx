// Chapters 1–4: cold open (blizzard + mammoth), the night shift, the first hour, the world without us.
import React from "react";
import { AbsoluteFill } from "remotion";
import { sat, ease, lerp, rnd } from "../engine/core";
import { Glow } from "../engine/fx";
import { ChapterPlayer, Ctx, Shot, chLen } from "../Player";
import { S, mv, onHead, P, Big, walk, shiver, SIT } from "./H";
import { Blizzard, Valley, SnowCave, Museum, Snow } from "../scenes/Ice";
import { Mammoth, CaveLion } from "../scenes/Animals";
import { TitleCard, BoneTally, Frost, PhoneShot, EuropeMap } from "../scenes/Inserts";
import { ELI, ELI_PACK } from "../chars/cast";
import { VO_C1 } from "../vo_c1"; import { VO_C2 } from "../vo_c2"; import { VO_C3 } from "../vo_c3"; import { VO_C4 } from "../vo_c4";

const blue = "#a8d0ff", warm = "#ffb060";
// ================= C1 — cold open =================
const bl = (c: Ctx, cam: number[][], eli: any, mam = 0, vis = 0.2, ex?: React.ReactNode) => <S cam={mv(c, cam[0], cam[1])}><Blizzard f={c.f} vis={vis}
  behind={mam > 0 ? <g transform={`translate(${lerp(1900, 1350, mam)} 860) scale(${0.55 + 0.25 * mam})`}><Mammoth ph={c.f * 0.05} trunk={Math.sin(c.f * 0.04)} /></g> : undefined}>
  {P(ELI_PACK, { facing: 1, ...shiver(c.f), mouth: "worried", brow: 0, browIn: 0.8, ...eli }, eli.x ?? 760, 900, 1.0, c.f, 1)}{ex}</Blizzard></S>;
const c1: Shot[] = [
  { at: ["open"], r: c => bl(c, [[0, -40, 1.0], [0, -40, 1.08]], { look: [0.4, -0.2] }) },
  { at: ["n1"], r: c => bl(c, [onHead(760, 900, 1, 2.0, 60, 40), onHead(760, 900, 1, 2.2, 60, 40)], { look: [0.7, 0], eyes: 0.8 }) },
  { at: ["n2"], r: c => <S cam={mv(c, [-60, -40, 1.1], [0, -40, 1.12])}><Museum f={c.f}>{P(ELI, { facing: 1, hold: "mop", aR: [20, 30], ...walk(c.f, 1, 0.5), mouth: "flat" }, 760 + c.t * 2, 1000, 1.05, c.f, 1)}</Museum></S> },
  { at: ["n2b"], r: c => bl(c, [[-300, -60, 1.0], [200, -60, 1.0]], { x: 760 + c.t * 0.5, ...walk(c.f, 1, 0.6) }, 0, 0.1) },
  { at: ["eli1"], r: c => bl(c, [onHead(760, 900, 1, 2.1, 30, 30), onHead(760, 900, 1, 2.3, 30, 30)], { talk: c.talk("eli1"), mouth: "shout", aR: [40, 60], look: [0.9, -0.3], eyes: 1.2, brow: 0.6, browIn: 0 }) },
  { at: ["n3"], r: c => bl(c, [[200, -60, 1.05], [240, -80, 1.15]], { facing: 1, look: [0.9, -0.5], mouth: "o", eyes: 1.3, brow: 0.8, browIn: 0 }, sat(c.t / (c.d * 0.8)), 0.15) },
  { at: ["n3", 0.62], r: c => <S cam={mv(c, [540, -80, 2.6], [560, -90, 2.9])}><Blizzard f={c.f} vis={0.5}><g transform="translate(1200 900) scale(1.0)"><Mammoth ph={c.f * 0.03} eye={1.2} angry={0.6} /></g></Blizzard></S> },
  { at: ["n4"], r: c => bl(c, [[60, -60, 1.0], [60, -120, 1.25]], { facing: 1, look: [0.9, -0.6], mouth: "o", eyes: 1.4, brow: 0.9, browIn: 0, aR: [40, 70], aL: [35, 75], lean: -6 }, 1, 0.3) },
  { at: ["title"], r: c => <TitleCard f={c.t} /> },
];
export const C1: React.FC = () => <ChapterPlayer ch="c1" vo={VO_C1} shots={c1} />;
export const C1_LEN = chLen("c1", VO_C1);

// ================= C2 — the night shift =================
const mus = (c: Ctx, cam: number[][], eli: any, glow = 0, flick = false, ex = 760) => <S cam={mv(c, cam[0], cam[1])}><Museum f={c.f} glow={glow} flicker={flick}>
  {P(ELI, { facing: 1, hold: "mop", aR: [20, 30], mouth: "flat", ...eli }, ex, 1000, 1.05, c.f, 1, glow > 0 ? "#ffd86a" : undefined)}</Museum></S>;
const c2: Shot[] = [
  { at: ["n1"], r: c => mus(c, [[-100, -30, 1.05], [60, -30, 1.1]], { ...walk(c.f, 1, 0.4) }, 0, false, 560 + c.t * 2) },
  { at: ["eli1"], r: c => mus(c, [onHead(760, 1000, 1.05, 2.2, 40, 40), onHead(760, 1000, 1.05, 2.35, 40, 40)], { talk: c.talk("eli1"), eyes: 0.6, look: [0.6, 0.3] }) },
  { at: ["n2"], r: c => <S cam={mv(c, [340, -10, 2.4], [340, -20, 2.7])}><Museum f={c.f} /></S> },
  { at: ["n2b"], r: c => <BoneTally f={c.f} n={44} bg="#1a2030" label="THE OLDEST CALENDAR?" /> },
  { at: ["n3"], r: c => <S cam={mv(c, [340, -20, 2.7], [340, -30, 3.1])}><Museum f={c.f} glow={0.35 + 0.15 * Math.sin(c.f * 0.3)} /></S> },
  { at: ["eli2"], r: c => mus(c, [onHead(1060, 1000, 1.05, 2.3, -40, 40), onHead(1060, 1000, 1.05, 2.45, -40, 40)], { talk: c.talk("eli2"), mouth: "o", eyes: 1.3, brow: 0.7, look: [0.9, -0.2] }, 0.4, false, 1060) },
  { at: ["n4"], r: c => mus(c, [[180, -40, 1.4], [220, -40, 1.6]], { aR: [80 + 10 * sat(c.t / 40), 6], hold: null, look: [0.9, -0.2], mouth: "o" }, 0.4 + 0.5 * sat(c.t / c.d), true, 1110) },
  { at: ["flash"], r: c => <><S cam={mv(c, [200, -40, 1.6], [200, -40, 1.8])}><Museum f={c.f} glow={1.0 + sat(c.t / 10)} /></S><AbsoluteFill style={{ background: "#fff", opacity: sat(c.t / 8) * (1 - sat((c.t - 24) / 14)) }} /></> },
];
export const C2: React.FC = () => <ChapterPlayer ch="c2" vo={VO_C2} shots={c2} />;
export const C2_LEN = chLen("c2", VO_C2);

// ================= C3 — the first hour =================
const Mound: React.FC<{ k: number }> = ({ k }) => <g><path d={`M${960 - 260 * k} 920 Q960 ${920 - 260 * k} ${960 + 260 * k} 920 Z`} fill="#f4f8fc" /><path d={`M${960 - 90 * k} 920 Q960 ${920 - 130 * k} ${960 + 90 * k} 920 Z`} fill="#3a5a7a" opacity={sat(k * 2 - 1)} /></g>;
const c3: Shot[] = [
  { at: ["n1"], r: c => bl(c, [[-200, -60, 1.0], [0, -60, 1.05]], { x: 500 + c.t * 2.5, ...walk(c.f, 1, 0.7), ...shiver(c.f), lL: walk(c.f).lL, lR: walk(c.f).lR }, 0, 0.1) },
  { at: ["fact1"], r: c => <Frost f={c.f} k={sat(c.t / (c.d * 0.8))} /> },
  { at: ["eli1"], r: c => <PhoneShot f={c.f} pct={12} lines={["NO SERVICE", "12%", "??:??"]} /> },
  { at: ["eli2"], r: c => bl(c, [onHead(760, 900, 1, 2.2, 30, 30), onHead(760, 900, 1, 2.35, 30, 30)], { talk: c.talk("eli2"), look: [0.5, 0.2] }) },
  { at: ["n2"], r: c => <S cam={mv(c, [0, -20, 1.2], [0, -20, 1.25])}><Blizzard f={c.f} vis={0.1}><Mound k={sat(c.t / c.d)} />{P(ELI_PACK, { facing: 1, lean: 30, aR: [60 + 30 * Math.sin(c.f * 0.5), 30], aL: [50 - 30 * Math.sin(c.f * 0.5), 30], mouth: "flat", brow: -0.3 }, 700, 930, 1.0, c.f, 1)}</Blizzard></S> },
  { at: ["fact2"], r: c => <S cam={mv(c, [0, 0, 1.0], [0, -20, 1.15])}><SnowCave f={c.f}><rect x={560} y={830} width={360} height={80} rx={30} fill="#9ab8d4" />{P(ELI_PACK, { ...SIT, seat: false, facing: 1, ...shiver(c.f), lL: SIT.lL, lR: SIT.lR, mouth: "flat", eyes: 0.7, look: [0.6, 0.2] }, 760, 960, 1.05, c.f, 1, blue)}
    {Array.from({ length: 4 }, (_, i) => { const t = ((c.f * 0.02 + i / 4) % 1); return <ellipse key={i} cx={860 + t * 60} cy={560 - t * 80} rx={20 + t * 30} ry={12 + t * 14} fill="#fff" opacity={(1 - t) * 0.35} />; })}</SnowCave></S> },
  { at: ["n3"], r: c => <><S cam={mv(c, [0, -20, 1.15], [0, -20, 1.25])}><SnowCave f={c.f}><rect x={560} y={830} width={360} height={80} rx={30} fill="#9ab8d4" />{P(ELI_PACK, { ...SIT, seat: false, facing: 1, eyes: 0.1, mouth: "flat", head: 8 }, 760, 960, 1.05, c.f, 1, blue)}</SnowCave></S><AbsoluteFill style={{ background: "#000", opacity: sat((c.t - c.d + 24) / 24) }} /></> },
];
export const C3: React.FC = () => <ChapterPlayer ch="c3" vo={VO_C3} shots={c3}
  facts={[["fact1", "At −25 °C with strong wind, bare skin can get frostbite in under 30 minutes. The body pulls blood from the fingers to protect the heart."],
    ["fact2", "Snow is full of trapped air. Inside a small snow cave, body heat keeps the air near 0 °C, even at −30 °C outside.", "right"]]} />;
export const C3_LEN = chLen("c3", VO_C3);

// ================= C4 — the world without us =================
const val = (c: Ctx, cam: number[][], kids: React.ReactNode, time: any = "dawn", herd = true) => <S cam={mv(c, cam[0], cam[1])}><Valley f={c.f} time={time} herd={herd}>{kids}</Valley></S>;
const c4: Shot[] = [
  { at: ["n1"], r: c => val(c, [[-200, -40, 1.25], [0, -40, 1.0]], <>{P(ELI_PACK, { facing: 1, look: [0.8, -0.2], mouth: "o", eyes: 1.2 }, 360, 1060, 1.15, c.f, 1, warm)}</>) },
  { at: ["fact1"], r: c => <EuropeMap f={c.f} k={sat(c.t / (c.d * 0.6))} /> },
  { at: ["n2"], r: c => val(c, [[-300, -60, 1.1], [300, -60, 1.1]], null) },
  { at: ["fact2"], r: c => val(c, [[0, 160, 2.0], [140, 160, 2.1]], null) },
  { at: ["n3"], r: c => val(c, [[-100, 0, 1.2], [-60, 0, 1.3]], <>{Array.from({ length: 10 }, (_, i) => <ellipse key={i} cx={300 + i * 110} cy={1000 - (i % 2) * 20} rx={18} ry={9} fill="#9ab0c4" />)}
    <g transform={`translate(${1500 - sat(c.t / 60) * 80} 1010) scale(-0.9 0.9)`}><CaveLion ph={c.f * 0.12} /></g><path d="M1300 1010 Q1420 900 1560 1010 Z" fill="#7a808a" /></>) },
  { at: ["fact3"], r: c => <>{val(c, [[-160, -40, 1.0], [160, -60, 1.18]], null, "day")}<Big text="−6 °C" k={sat(c.t / 10)} size={200} color="#a8d8ff" y={420} /></> },
  { at: ["eli1"], r: c => val(c, [onHead(560, 1060, 1.15, 2.1, -40, 40), onHead(560, 1060, 1.15, 2.25, -40, 40)], <>{P(ELI_PACK, { facing: 1, talk: c.talk("eli1"), mouth: "smile", eyes: 1.25, brow: 0.6, look: [0.6, -0.3] }, 560, 1060, 1.15, c.f, 1, warm)}</>) },
];
export const C4: React.FC = () => <ChapterPlayer ch="c4" vo={VO_C4} shots={c4}
  facts={[["fact1", "30,000 years ago, ice up to 3 km thick covered northern Europe. The sea was so low you could walk from France to Britain.", "right"],
    ["fact2", "A woolly mammoth could weigh 6 tonnes. Cave lions were even bigger than today's lions."],
    ["fact3", "On average the whole planet was about 6 °C colder than today."]]} />;
export const C4_LEN = chLen("c4", VO_C4);
