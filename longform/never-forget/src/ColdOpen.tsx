// Cold open: "Plate 7KR-419". All cut/voice frames are derived from the real voice lengths (src/vo_c1.ts).
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Stage, camAt, sat, ease, easeOut, lerp } from "./engine/core";
import { Vignette, Grain, Grade } from "./engine/fx";
import { PoliceRoom } from "./scenes/Police";
import { PhotoInsert, CoffeeSpill, Screen } from "./scenes/Inserts";
import { StreetPast, PlateInsert, MemoryFX, MEMORY_FILTER, carPt, CAR_PTS } from "./scenes/Memory";
import { TitleCard, Loftus, Exterior } from "./scenes/Title";
import { FactCard, Stamp, useFonts } from "./ui";
import { VO_C1, talkAt } from "./vo_c1";

const D = (k: string) => VO_C1[k]?.dur ?? 60;
// timeline (frames)
const T: Record<string, number> = {};
T.okafor1 = 48; T.photo = T.okafor1 + 76;
T.okafor2 = T.okafor1 + D("c1_okafor1") + 10;
T.n1 = T.okafor2 + D("c1_okafor2") + 12;
T.n2 = T.n1 + D("c1_n1") + 6;
T.flash = T.n2 + D("c1_n2") + 4;
T.rew = T.flash + 12;
T.lina1 = T.rew + 26; T.plate = T.lina1 + 34;
T.lina2 = T.lina1 + D("c1_lina1") + 10; T.fresh = T.lina2 + Math.round(D("c1_lina2") * 0.55);
T.lina3 = T.lina2 + D("c1_lina2") + 10;
T.tip = T.lina3 + D("c1_lina3") + 14;
T.knock = T.tip; T.spillCU = T.tip + 26; T.screen = T.tip + 66;
T.n3 = T.screen + 66; T.two = T.screen + 84;
T.loftus = T.n3 + D("c1_n3") + 10;
T.ext = T.loftus + 135;
T.n4 = T.ext + 10;
T.title = T.n4 + D("c1_n4") + 20;
T.n5 = T.title + 10;
T.end = T.n5 + D("c1_n5") + 45;
export const C1 = T;
export const C1_LEN = T.end;

const Flash: React.FC<{ f: number; at: number; color?: string; len?: number }> = ({ f, at, color = "255,210,110", len = 14 }) => {
  const u = (f - at) / len; if (u < 0 || u > 1) return null;
  return <div style={{ position: "absolute", inset: 0, background: `radial-gradient(circle at 50% 45%, rgba(${color},${1 - u}) 0%, rgba(${color},${(1 - u) * 0.6}) 50%, rgba(0,0,0,0) 100%)`, mixBlendMode: "screen" }} />;
};

export const ColdOpen: React.FC = () => {
  useFonts();
  const f = useCurrentFrame();
  const tk = (k: string) => talkAt(VO_C1[k], f, T[k.replace("c1_", "")]);
  // police room. Close-ups hide the other character (cheat cut) so no half faces sit on the frame edge.
  // Okafor CU: him on the right third looking left; Lina CU: her on the left third looking right.
  const OKCU = [47, -34, 2.2], LICU = [-130, 69, 2.1];
  const roomCam = camAt(f, [[42, -20, 40, 1.0], [T.photo, 40, 30, 1.2], [T.okafor2 - 1, 40, 30, 1.2], [T.okafor2, OKCU[0], OKCU[1], OKCU[2]], [T.n1 - 1, OKCU[0] + 10, OKCU[1], OKCU[2] + 0.12],
    [T.n1, LICU[0], LICU[1], LICU[2]], [T.n2 - 1, LICU[0] + 8, LICU[1], LICU[2] + 0.12], [T.n2, -243, 38, 4.2], [T.flash + 12, -243, 38, 5.0]]);
  const twoCam = camAt(f, [[T.two, OKCU[0], OKCU[1], OKCU[2]], [T.two + 44, OKCU[0] + 8, OKCU[1], OKCU[2] + 0.1], [T.two + 45, LICU[0], LICU[1], LICU[2]], [T.two + 92, LICU[0] + 8, LICU[1], LICU[2] + 0.1], [T.two + 93, 0, 50, 1.1], [T.loftus, 20, 50, 1.2]]);
  const roomHide = (f >= T.okafor2 && f < T.n1) || (f >= T.two && f < T.two + 45) ? "lina" : (f >= T.n1 && f < T.rew) || (f >= T.two + 45 && f < T.two + 93) ? "ok" : null;
  // memory: the car drives in from the right and FREEZES; the whole memory freezes with it (tf stops)
  const tStop = T.lina1 + 30, tf = Math.min(f, tStop) - T.rew;
  const carX = f < tStop ? lerp(2900, 1400, easeOut((f - T.rew) / (tStop - T.rew))) : 1400;
  const wheel = (2900 - carX) * 0.6;
  const marks = [sat((f - T.plate) / 14), sat((f - T.lina2 - 10) / 14), sat((f - T.fresh) / 14)];
  const DENT = carPt(1400, 1.15, -1, CAR_PTS.dent), FRESH = carPt(1400, 1.15, -1, CAR_PTS.fresh);
  const streetCam = camAt(f, [[T.rew, 60, 40, 1.0], [T.plate, 30, 50, 1.06], [T.lina2, DENT[0] - 960, DENT[1] - 540, 2.3], [T.fresh - 1, DENT[0] - 950, DENT[1] - 540, 2.45],
    [T.fresh, FRESH[0] - 960, FRESH[1] - 540, 2.9], [T.lina3 - 1, FRESH[0] - 960, FRESH[1] - 540, 3.1], [T.lina3, 60, 40, 1.0], [T.tip, 80, 40, 1.08]]);
  const closeStreet = f >= T.lina2 && f < T.lina3;
  const okRoom = { mouth: (f > T.screen ? "o" : "frown") as any, brow: f > T.screen ? 0.8 : -0.5, look: [0.6, 0.25], talk: tk("c1_okafor1") || tk("c1_okafor2"), eyes: f > T.screen ? 1.2 : 1 };
  const linaRoom = { noBlink: f >= T.n1 && f < T.rew, eyes: f >= T.n2 && f < T.rew ? 1.15 : 1, look: [0.7, -0.15], mouth: (f > T.two ? "smirk" : "flat") as any, gold: f >= T.n2 + 18 ? sat((f - T.n2 - 18) / 6) : 0, brow: f > T.two ? 0.3 : 0 };
  const extX = lerp(960, 1340, easeOut((f - T.ext) / 150));

  let shot: React.ReactNode = null, grade = "room", mem = 0;
  // 0) Okafor slams his coffee down (his own rig hand holds the cup; arm angles solved so the cup base lands on the table)
  const slamU = Math.min(1, (f / 8) ** 2), slamA = f < 8 ? [lerp(90, 12, slamU), lerp(134, 54, slamU)] : f < 24 ? [12, 54] : [lerp(12, 42, ease((f - 24) / 12)), lerp(54, 16, ease((f - 24) / 12))];
  const slamOk = { ...okRoom, aR: slamA, hold: (f < 24 ? "cup" : null) as any, mouth: "frown" as any, brow: -0.7, look: [0.7, 0.3] };
  // knock: Okafor startles at the plate, his hand jerks back and hits the cup (contact at +7), the cup tips right
  const kf = f - T.knock, knA = kf < 4 ? [42, 16] : kf < 9 ? [lerp(42, 2, ease((kf - 4) / 5)), lerp(16, 58, ease((kf - 4) / 5))] : [lerp(2, -7, ease((kf - 9) / 8)), lerp(58, 64, ease((kf - 9) / 8))];
  const cupTipK = f >= T.knock + 5 ? Math.min(1, ((f - T.knock - 5) / 8) ** 1.6) : 0;
  const spillK = f >= T.knock + 16 ? 1 : 0;
  if (f < 42) { shot = <Stage cam={camAt(f, [[0, 154, 60, 2.2], [42, 150, 60, 2.35]])}><PoliceRoom f={f} lina={linaRoom} ok={slamOk} cupHeld={f < 24} splash={f >= 8 ? f - 8 : -1} hide="lina" /></Stage>; }
  else if (f < T.photo) shot = <Stage cam={roomCam}><PoliceRoom f={f} lina={linaRoom} ok={okRoom} /></Stage>;
  else if (f < T.okafor2) shot = <PhotoInsert f={f - T.photo} />;
  else if (f < T.rew) shot = <Stage cam={roomCam}><PoliceRoom f={f} lina={linaRoom} ok={okRoom} hide={roomHide as any} /></Stage>;
  else if (f < T.tip) { mem = sat((f - T.rew) / 8); grade = "mem";
    shot = <div style={{ position: "absolute", inset: 0, filter: MEMORY_FILTER(mem) }}>{f >= T.plate && f < T.lina2 ? <PlateInsert f={f - T.plate} k={marks[0]} />
      : <Stage cam={streetCam} bg="#9ec6e8"><StreetPast f={f} tf={tf} carX={carX} wheel={wheel} marks={marks} active={closeStreet ? (f >= T.fresh ? 2 : 1) : -1} crowd={!closeStreet} /></Stage>}</div>; }
  else if (f < T.spillCU) shot = <Stage cam={camAt(f, [[T.knock, 170, 40, 2.1], [T.spillCU, 175, 45, 2.2]])}><PoliceRoom f={f} lina={linaRoom} ok={{ ...okRoom, mouth: "o", brow: 0.9, eyes: 1.25, look: [0.7, -0.2], aR: knA }} cupTip={cupTipK} spill={spillK * 0.3} hide="lina" /></Stage>;
  else if (f < T.screen) shot = <CoffeeSpill f={f - T.spillCU} />;
  else if (f < T.two) shot = <Screen f={f - T.screen} />;
  else if (f < T.loftus) shot = <Stage cam={twoCam}><PoliceRoom f={f} lina={linaRoom} ok={{ ...okRoom, aR: [30, 40], aL: [40, 30], lean: 4 }} cupTip={1} spill={1} hide={roomHide as any} /></Stage>;
  else if (f < T.ext) { shot = <Loftus f={f - T.loftus} />; grade = "none"; }
  else if (f < T.title) { shot = <Stage cam={camAt(f, [[T.ext, 0, 0, 1.0], [T.title, 230, -20, 1.12]])}><Exterior f={f} linaX={extX} walking={f < T.ext + 140} frames={sat((f - T.ext - 80) / 20)} /></Stage>; grade = "ext"; }
  else { shot = <TitleCard f={f - T.title} />; grade = "none"; }

  const dateK = f >= T.rew && f < T.tip ? sat((f - T.rew - 6) / 8) : 0;
  return <AbsoluteFill style={{ background: "#000" }}>
    {shot}
    {grade === "room" && <Grade top="rgba(120,170,255,1)" bottom="rgba(20,30,60,1)" o={0.22} />}
    {grade === "ext" && <Grade top="rgba(80,120,255,1)" bottom="rgba(255,150,80,1)" o={0.15} />}
    <MemoryFX f={f} k={mem} />
    <Stamp text={f >= T.lina3 ? "TUE 03 MAR 2023  16:17:09" : "03 MAR 2023  16:17:0" + Math.min(9, Math.floor((f - T.rew) / 12) % 10)} k={dateK} f={f} />
    <FactCard text="Memory is easy to rewrite: in a 1974 study, changing ONE word in a question changed how fast people remembered a car going." k={easeOut((f - T.loftus - 20) / 15) * (1 - sat((f - T.ext + 8) / 8))} />
    <Flash f={f} at={T.flash} />
    <Flash f={f} at={T.knock - 2} color="200,230,255" len={8} />
    {grade !== "none" && <Vignette o={0.8} />}
    <Grain f={f} o={0.06} />
  </AbsoluteFill>;
};
