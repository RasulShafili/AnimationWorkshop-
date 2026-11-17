import React from "react";
import { AbsoluteFill } from "remotion";
import { Character, AIM, PORT, COVER, muzzle } from "./chars/Rig2";
import { Robot, robotAim } from "./chars/Robot";
import { WALT, LEO, SOLDIERS, HUNTER, ZARA } from "./chars/cast";
import { Pickup, BED_Y, Muzzle, NetShot, Humvee } from "./scenes/Gear";
// pose + scale QA: aim, port, cover, robot aiming a net at Leo, the real-scale truck next to people
export const PoseTest: React.FC = () => { const ra = robotAim(1500, 960, 1.12, -1, 1180, 700);
  const [mx, my] = muzzle(200, 960, 1.04, 1);
  return <AbsoluteFill style={{ background: "#c8d4e0" }}><svg width={1920} height={1080}><rect y={960} width={1920} height={120} fill="#7a8290" />
    <Character look={WALT} pose={{ facing: 1, ...AIM, mouth: "shout" }} x={200} y={960} s={1} f={3} seed={2} /><Muzzle x={mx} y={my} k={1} />
    <Character look={SOLDIERS[1]} pose={{ facing: 1, ...PORT }} x={560} y={960} s={1} f={3} seed={3} />
    <Character look={LEO} pose={{ facing: 1, ...COVER, bob: 95, lL: [70, 130], lR: [60, 120], mouth: "shout" }} x={1180} y={960} s={1} f={3} seed={1} />
    <Robot look={HUNTER} pose={{ facing: -1, aR: ra.aR }} x={1500} y={960} s={1} f={3} seed={5} />
    <NetShot x0={ra.tip[0]} y0={ra.tip[1]} x1={1180} y1={700} k={0.5} />
    <g transform="translate(-1200 0)" />
  </svg>
  <svg width={1920} height={1080} style={{ position: "absolute", top: 0 }} viewBox="0 0 1920 1080"><g transform="translate(1000 1960) scale(1)" /></svg></AbsoluteFill>; };
export const ScaleTest: React.FC = () => <AbsoluteFill style={{ background: "#c8d4e0" }}><svg width={1920} height={1080}><rect y={960} width={1920} height={120} fill="#7a8290" />
  <g transform="translate(700 960)"><Character look={WALT} pose={{ facing: -1, ...AIM }} x={-108} y={BED_Y} s={0.95} f={3} seed={2} /><Pickup lights /></g>
  <Character look={LEO} pose={{ facing: 1 }} x={1400} y={960} s={1} f={3} seed={1} /><Character look={ZARA} pose={{ facing: -1 }} x={1550} y={960} s={1} f={3} seed={2} />
  <g transform="translate(1720 960) scale(0.35)"><Humvee f={0} /></g></svg></AbsoluteFill>;
