// shared shot helpers
import React from "react";
import { AbsoluteFill } from "remotion";
import { Stage, Layer, camAt } from "../engine/core";
import { Ctx } from "../Player";
import { Character, Pose, Look } from "../chars/Rig2";
import { Robot, RobotLook } from "../chars/Robot";
export const mv = (c: Ctx, a: number[], b: number[]) => camAt(c.t, [[0, ...a], [c.d, ...b]]);
export const S: React.FC<{ cam: any; children: React.ReactNode; bg?: string }> = ({ cam, children, bg = "#000" }) => <Stage cam={cam} bg={bg}><Layer depth={1}>{children}</Layer></Stage>;
export const onHead = (x: number, y: number, s: number, z: number, dx = 0, dy = 0) => [x - 960 + dx, y - 362 * s - 540 + dy, z];
// seated poses (bob 82) get a log/rock under them automatically: seat top = rootY − 86·s·scale
export const P = (look: Look, pose: Pose, x: number, y: number, s: number, f: number, seed = 1, rim?: string) => { const k = s * (look.scale ?? 1), top = y - 86 * k;
  return <g>{pose.bob === 82 && pose.seat !== false && <g><path d={`M${x - 78 * k} ${y + 4} Q${x - 84 * k} ${top} ${x} ${top - 4 * k} Q${x + 84 * k} ${top} ${x + 78 * k} ${y + 4} Z`} fill="#6a5a4e" /><path d={`M${x - 64 * k} ${top + 8 * k} Q${x} ${top - 6 * k} ${x + 64 * k} ${top + 8 * k}`} stroke="#fff" strokeOpacity={0.25} strokeWidth={5 * k} fill="none" /></g>}
    <Character look={look} pose={pose} x={x} y={y} s={s} f={f} seed={seed} rim={rim ? { dx: 4, dy: -3, color: rim } : null} /></g>; };
export const Big: React.FC<{ text: string; k: number; color?: string; y?: number; size?: number }> = ({ text, k, color = "#fff", y = 540, size = 120 }) => k <= 0 ? null :
  <AbsoluteFill><div style={{ position: "absolute", top: y - size * 0.6, width: "100%", textAlign: "center", fontFamily: "Inter", fontWeight: 900, fontSize: size, color, opacity: Math.min(1, k), textShadow: "0 6px 0 rgba(0,0,0,.5), 0 0 40px rgba(0,0,0,.6)", transform: `scale(${0.92 + 0.08 * Math.min(1, k)})` }}>{text}</div></AbsoluteFill>;
export const walk = (f: number, dir = 1, amp = 1) => { const ph = f * 0.14 * dir, s = Math.sin(ph), c = Math.cos(ph);
  return { lean: 3, aL: [-22 * s * amp, 14], aR: [22 * s * amp, 14], lL: [24 * s * amp, 6 + 22 * Math.max(0, -c) * amp], lR: [-24 * s * amp, 6 + 22 * Math.max(0, c) * amp], bob: -Math.abs(c) * 4 * amp }; };
export const run = (f: number, dir = 1) => { const ph = f * 0.38 * dir, s = Math.sin(ph), c = Math.cos(ph);
  return { lean: 10, aL: [-50 * s, 80], aR: [50 * s, 80], lL: [40 * s, 20 + 60 * Math.max(0, -c)], lR: [-40 * s, 20 + 60 * Math.max(0, c)], bob: -Math.abs(c) * 10 }; };
export const shiver = (f: number) => ({ aR: [18, 128], aL: [14, 128], lean: 4 + Math.sin(f * 2.1) * 1.2, head: Math.sin(f * 1.7) * 2 });
export const SIT = { bob: 82, lL: [90, 90], lR: [84, 84] };
// robots drop into the same scenes/cameras as people
export const RB = (look: RobotLook, pose: Pose, x: number, y: number, s: number, f: number, seed = 1, rim?: string) =>
  <Robot look={look} pose={pose} x={x} y={y} s={s} f={f} seed={seed} rim={rim ? { dx: 4, dy: -3, color: rim } : null} />;
