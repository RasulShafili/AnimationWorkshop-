import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Character } from "./chars/Rig2";
import { ELI, ELI_PACK, NIA, TOR, PIP, AMA, BAND, VOSS } from "./chars/cast";
import { Mammoth, CaveLion, Wolf, Reindeer, Rhino } from "./scenes/Animals";
import { useFonts } from "./ui";
import { Stage, Layer } from "./engine/core";
import { Blizzard, Valley, SnowCave, Riverbank, Camp, TentIn, PaintedCave, Museum, ResearchCave } from "./scenes/Ice";
const S1 = (n: React.ReactNode) => <Stage cam={{ x: 0, y: 0, zoom: 1 }}><Layer depth={1}>{n}</Layer></Stage>;
export const SCENES: ((f: number) => React.ReactNode)[] = [
  f => <svg width={1920} height={1080}><rect width={1920} height={1080} fill="#9aa8b8" />
    {[[ELI_PACK, {}], [NIA, { hold: "can" }], [TOR, {}], [PIP, { mouth: "grin" }], [AMA, {}], [BAND[0], {}], [BAND[1], {}], [BAND[3], {}], [VOSS, {}]].map(([l, p]: any, i) => <Character key={i} look={l} pose={{ facing: 1, ...p }} x={110 + i * 210} y={480} s={0.95} f={f} seed={i} />)}
    <g transform="translate(400 1040) scale(0.55)"><Mammoth ph={f * 0.1} /></g>
    <g transform="translate(900 1040) scale(0.8)"><CaveLion ph={f * 0.2} roar={0.6} /></g>
    <g transform="translate(1250 1040) scale(0.8)"><Wolf ph={f * 0.2} /></g>
    <g transform="translate(1500 1040) scale(0.8)"><Reindeer ph={f * 0.2} /></g>
    <g transform="translate(1720 1040) scale(0.45)"><Rhino ph={f * 0.1} /></g></svg>,
  f => S1(<Blizzard f={f} behind={<g transform="translate(1300 800) scale(0.6)"><Mammoth ph={f * 0.05} /></g>}><Character look={ELI} pose={{ facing: 1, aR: [20, 120], aL: [20, 120], mouth: "worried" }} x={700} y={900} s={1.0} f={f} /></Blizzard>),
  f => S1(<Valley f={f} />),
  f => S1(<SnowCave f={f} />),
  f => S1(<Riverbank f={f} glint={1} />),
  f => S1(<Camp f={f} />),
  f => S1(<Camp f={f} night />),
  f => S1(<TentIn f={f} />),
  f => S1(<PaintedCave f={f} />),
  f => S1(<Museum f={f} glow={0.5} />),
  f => S1(<ResearchCave f={f} />),
];
export const SceneTest: React.FC<{ which: number }> = ({ which }) => { useFonts(); const f = useCurrentFrame(); return <AbsoluteFill>{SCENES[which](f)}</AbsoluteFill>; };
