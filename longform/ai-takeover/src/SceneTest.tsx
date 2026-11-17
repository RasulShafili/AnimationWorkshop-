import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Stage, Layer } from "./engine/core";
import { SmartRoom, Shop, NightStreet, CityWide, DataCenter, ServerHall, Tunnel } from "./scenes/City";
import { Pickup, Humvee, Drone, Muzzle, Sparks, NetShot, Dart, LaserDot, Boom } from "./scenes/Gear";
import { Ranch } from "./scenes/z/World";
import { Landscape } from "./scenes/z/Outdoor";
import { P, RB } from "./chapters/H";
import { LEO, LEO_RAIN, WALT, ZARA, REYES, SOLDIERS, BOLT, BOLT_1ARM, HELPERS, HUNTER } from "./chars/cast";
const L = [
  (f: number) => <SmartRoom f={f}>{P(LEO, { facing: 1, mouth: "smile" }, 600, 960, 1, f, 1)}</SmartRoom>,
  (f: number) => <Shop f={f} tv={<rect width={396} height={226} fill="#2a4a6a" />}>{P(LEO, { facing: 1, mouth: "smile", aR: [60, 40] }, 900, 960, 1, f, 1)}{P(ZARA, { facing: -1, mouth: "flat" }, 1500, 960, 1, f, 2)}<g>{RB(BOLT, { facing: -1, lL: [90, 90], lR: [84, 84], bob: 82 }, 1200, 760, 0.8, f, 3)}</g></Shop>,
  (f: number) => <NightStreet f={f} alley={1}>{P(LEO_RAIN, { facing: 1, aR: [-40, 80], aL: [40, 80], lean: 10 }, 400, 960, 1, f, 1)}{RB({ ...HUNTER, dark: 0.7 }, { facing: -1 }, 1110, 900, 1, f, 4)}{RB({ ...HUNTER, dark: 0.8 }, { facing: -1 }, 1300, 900, 0.95, f, 5)}</NightStreet>,
  (f: number) => <CityWide f={f} mode="day" drones={1} />,
  (f: number) => <CityWide f={f} mode="locked" drones={1} />,
  (f: number) => <CityWide f={f} mode="dark" />,
  (f: number) => <DataCenter f={f} fight={1}>{SOLDIERS.slice(0, 3).map((s, i) => <g key={i}>{P(s, { facing: 1, hold: "rifle", aR: [80, 10], aL: [70, 40] }, -420 + i * 160, 960, 0.9, f, i)}</g>)}<Muzzle x={-300} y={760} k={1} />{RB({ ...HUNTER, dark: 0.5 }, { facing: -1, aR: [70, 20] }, 1300, 900, 0.8, f, 6)}<Sparks x={1300} y={700} t={4} /><Boom x={1700} y={760} t={6} /></DataCenter>,
  (f: number) => <ServerHall f={f} handle={0}>{P(LEO, { facing: 1, aR: [150, 10] }, 760, 1000, 1, f, 1)}{RB(BOLT_1ARM, { facing: 1 }, 1100, 1000, 1, f, 3)}</ServerHall>,
  (f: number) => <Tunnel f={f}>{P(REYES, { facing: 1, hold: "rifle", aR: [30, 40] }, 700, 1000, 1, f, 1)}{P(WALT, { facing: -1, mouth: "smirk" }, 1200, 1000, 1, f, 2)}</Tunnel>,
  (f: number) => <Ranch f={f}>{P(WALT, { facing: 1, hold: "rifle", aR: [80, 10], aL: [70, 40] }, 300, 960, 1, f, 2)}<Muzzle x={470} y={720} k={1} />{RB({ ...HELPERS, shell: 0.4, mode: "hostile", gun: true }, { facing: -1, aR: [80, 20] }, 1300, 960, 1, f, 7)}<NetShot x0={1240} y0={760} x1={500} y1={800} k={0.5} /><Dart x0={1240} y0={760} x1={700} y1={760} k={0.7} f={f} /></Ranch>,
  (f: number) => <Landscape f={f} kind="plains"><g transform="translate(900 960)"><Pickup wheelRot={f * 8} lights /></g><Drone x={1500} y={400} f={f} kind="search" red beam={1} /><Drone x={300} y={300} f={f} /></Landscape>,
  (f: number) => <Landscape f={f} kind="plains"><g transform="translate(900 960)"><Humvee f={f} firing /></g>{RB(HUNTER, { facing: -1 }, 1600, 960, 1, f, 8)}<LaserDot x0={1560} y0={600} x={1000} y={700} f={f} /></Landscape>,
];
export const SceneTest: React.FC<{ which: number }> = ({ which }) => { const f = useCurrentFrame();
  return <AbsoluteFill style={{ background: "#000" }}><Stage cam={{ x: 0, y: 0, zoom: 1 }}><Layer depth={1}>{L[which](f)}</Layer></Stage></AbsoluteFill>; };
