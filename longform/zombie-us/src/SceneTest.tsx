import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Stage, Layer } from "./engine/core";
import { StoreAisle, StoreFront, StaffRoom, DockDoor, P } from "./scenes/Store";
import { KAI, MIRA, RUIZ, DANA } from "./chars/cast";
import { useFonts } from "./ui";
import { Phone, Clipboard, RulesBoard, BrainBoard, AntFungus, RatCat, RadioBench, Doubling, Density, Threes, Sleeve, ER, Notebook, TitleCard, Part2, EndCard, Badge } from "./scenes/Inserts";
import { Street, Highway, RoofView, BoxTruck, Lot, Cab, Crossroads, Landscape, Checkpoint, TentCity } from "./scenes/Outdoor";
import { HOLT as HOLT2 } from "./chars/cast";
import { Kitchen, KitchenTable, Ranch, Bat, NerveMicro, Terminal, DepBoard, PlaneSky, USMap } from "./scenes/World";
import { MOM, RANCHER, KAI_PACK } from "./chars/cast";
export const SCENES: ((f: number) => React.ReactNode)[] = [
  f => <Stage cam={{ x: 0, y: 0, zoom: 1 }}><Layer depth={1}><StoreAisle f={f} light="night">{P(KAI, { hold: "bat", aR: [20, 20] }, 800, 900, 1.1, f, 1, "#8ad0ff")}{P(MIRA, { hold: "torch", beam: 1, aR: [70, 10] }, 1050, 900, 1.1, f, 2)}</StoreAisle></Layer></Stage>,
  f => <Stage cam={{ x: 0, y: 0, zoom: 1 }}><Layer depth={1}><StoreFront f={f} crowd={40} hands={9} inside={<>{P(KAI, { facing: -1, aR: [70, 20] }, 520, 1060, 1.2, f, 1, "#8ad0ff")}</>} /></Layer></Stage>,
  f => <Stage cam={{ x: 0, y: 0, zoom: 1 }}><Layer depth={1}><StaffRoom f={f} board={<text x={40} y={90} fontFamily="Permanent Marker" fontSize={60} fill="#1a3a8a">RULES</text>}>{P(DANA, { aR: [120, 30] }, 500, 900, 1.1, f)}{P(RUIZ, { facing: -1 }, 1500, 900, 1.1, f)}</StaffRoom></Layer></Stage>,
  f => <Stage cam={{ x: 0, y: 0, zoom: 1 }}><Layer depth={1}><DockDoor f={f} knock={1} />{P(RUIZ, { hold: "mop", aR: [10, 20] }, 600, 900, 1.1, f)}</Layer></Stage>,
  f => <Stage cam={{ x: 0, y: 0, zoom: 1 }}><Layer depth={1}><Kitchen f={f}><KitchenTable x={700} y={900} />{P(MOM, { hold: "keys", aR: [30, 40], mouth: "smile" }, 1300, 950, 1.1, f)}{P(KAI, { facing: 1, mouth: "flat", eyes: 0.6 }, 400, 950, 1.1, f)}{P(MIRA, { hold: "walkie", aR: [40, 70], mouth: "smile", facing: -1 }, 900, 960, 1.1, f)}</Kitchen></Layer></Stage>,
  f => <Stage cam={{ x: 0, y: 0, zoom: 1 }}><Layer depth={1}><Ranch f={f}>{P(RANCHER, { facing: -1 }, 1500, 880, 1.0, f)}</Ranch></Layer></Stage>,
  f => <Stage cam={{ x: 0, y: 0, zoom: 1 }}><Layer depth={1}><Ranch f={f} inside><Bat x={900} y={240} f={f} s={1.4} />{P(RANCHER, { facing: -1, aR: [160, 10] }, 1000, 900, 1.1, f)}</Ranch></Layer></Stage>,
  f => <NerveMicro f={f} />,
  f => <Stage cam={{ x: 0, y: 0, zoom: 1 }}><Layer depth={1}><Terminal f={f} /></Layer></Stage>,
  f => <DepBoard f={f} hi={1} rows={[["14:05", "DENVER", "DL 1182", "B10", "ON TIME"], ["14:20", "ATLANTA", "DL 2207", "C3", "BOARDING"], ["14:35", "CHICAGO", "AA 302", "A7", "DELAYED"]]} />,
  f => <PlaneSky f={f + 40} />,
  f => <USMap f={f} spread={0.5} routes={1} safe={1} path={1} />,
  f => <Stage cam={{ x: 0, y: 0, zoom: 1 }}><Layer depth={1}><Street f={f}>{P(MIRA, { facing: 1 }, 960, 700, 1.0, f)}{P(KAI, { facing: -1 }, 1300, 980, 1.0, f)}</Street></Layer></Stage>,
  f => <Stage cam={{ x: 0, y: 0, zoom: 1 }}><Layer depth={1}><Highway f={f} /></Layer></Stage>,
  f => <Stage cam={{ x: 0, y: 0, zoom: 1 }}><Layer depth={1}><RoofView f={f} turn={1} canT={10}>{P(KAI_PACK, { facing: 1, hold: "binoculars", aR: [150, 20], aL: [150, 20] }, 400, 1000, 1.0, f)}</RoofView></Layer></Stage>,
  f => <Stage cam={{ x: 0, y: 0, zoom: 1 }}><Layer depth={1}><Lot f={f} moon><g transform="translate(1200 960)"><BoxTruck /></g></Lot></Layer></Stage>,
  f => <Stage cam={{ x: 0, y: 0, zoom: 1 }}><Layer depth={1}><Cab f={f} outside="dawn">{P(DANA, { facing: 1, aR: [60, 60], aL: [60, 60] }, 560, 1180, 1.25, f)}{P(KAI, { facing: -1 }, 1050, 1180, 1.25, f)}{P(MIRA, { facing: -1 }, 1400, 1100, 1.25, f)}</Cab></Layer></Stage>,
  f => <Stage cam={{ x: 0, y: 0, zoom: 1 }}><Layer depth={1}><Crossroads f={f}>{P(RUIZ, { facing: -1 }, 1000, 760, 0.6, f)}</Crossroads></Layer></Stage>,
  f => <Stage cam={{ x: 0, y: 0, zoom: 1 }}><Layer depth={1}><Landscape f={f} kind="mountains"><g transform="translate(500 880) scale(0.7)"><BoxTruck wheelRot={f * 10} /></g></Landscape></Layer></Stage>,
  f => <Stage cam={{ x: 0, y: 0, zoom: 1 }}><Layer depth={1}><Checkpoint f={f}>{P(HOLT2, { facing: -1, hold: "rifle", aR: [50, 70], aL: [40, 60] }, 1100, 1000, 1.0, f)}{P(KAI_PACK, { facing: 1, aR: [150, 10], aL: [150, 10] }, 800, 1000, 1.0, f)}</Checkpoint></Layer></Stage>,
  f => <Stage cam={{ x: 0, y: 0, zoom: 1 }}><Layer depth={1}><TentCity f={f}>{P(MIRA, { facing: 1, aR: [120, 20] }, 600, 1020, 1.0, f)}</TentCity></Layer></Stage>,
  f => <Phone f={f} mode={{ kind: "notifs", n: 4, items: [["NEWS", "Attacks reported at ATL airport"], ["MOM", "Are you at work??"], ["X", "#AtlantaAttacks trending"], ["ALERT", "Police: avoid Hartsfield"]] }} />,
  f => <Phone f={f} mode={{ kind: "alert" }} />,
  f => <Clipboard f={f} items={["WATER", "CANNED FOOD", "BATTERIES", "FIRST AID"]} ticks={3.5} />,
  f => <Stage cam={{ x: 0, y: 0, zoom: 1 }}><Layer depth={1}><StaffRoom f={f} board={<RulesBoard n={3} />} /></Layer></Stage>,
  f => <Stage cam={{ x: 0, y: 0, zoom: 1 }}><Layer depth={1}><StaffRoom f={f} board={<BrainBoard k={1} />} /></Layer></Stage>,
  f => <AntFungus f={f + 160} />,
  f => <RatCat f={f + 60} />,
  f => <Stage cam={{ x: 0, y: 0, zoom: 1 }}><Layer depth={1}><RadioBench f={f} on={1}>{P(KAI, { facing: 1, aR: [70, 40], aL: [60, 40], look: [0.6, 0.4] }, 760, 1000, 1.2, f, 1, "#ffd86a")}</RadioBench></Layer></Stage>,
  f => <Doubling f={f} k={0.7} />,
  f => <Density f={f} k={1} />,
  f => <Threes f={f} k={1} />,
  f => <Sleeve f={f} />,
  f => <ER f={f} talk={0.5} />,
  f => <Notebook f={f} k={1} />,
  f => <TitleCard f={f + 30} />,
  f => <EndCard f={f} />,
  f => <svg width={1920} height={1080}><rect width={1920} height={1080} fill="#8a6a44" /><Badge x={960} y={540} s={1.6} note="ARRIVED DAY 12 · TENT 48" /></svg>,
  f => <Phone f={f} mode={{ kind: "call", name: "MOM", t: 200 }} />,
];
export const SceneTest: React.FC<{ which: number }> = ({ which }) => { useFonts(); const f = useCurrentFrame(); return <AbsoluteFill>{SCENES[which](f)}</AbsoluteFill>; };
