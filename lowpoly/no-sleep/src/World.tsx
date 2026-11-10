import React from "react";
import * as THREE from "three";
import { useThree } from "@react-three/fiber";
import { GLTF } from "three/examples/jsm/loaders/GLTFLoader.js";
import T from "./timeline.json";
import { Room } from "./Room";
import { Sleeper, Pose } from "./Sleeper";
import { Brain } from "./Brain";

const B = T.beats, H = T.hours;
export const sat = (v: number) => Math.min(1, Math.max(0, v));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const ease = (t: number) => { t = sat(t); return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
const V = (x: number, y: number, z: number) => new THREE.Vector3(x, y, z);
export const beatOf = (f: number) => { let i = 0; while (i < B.length - 2 && f >= B[i + 1]) i++; return i; };
// hours awake: races 0 -> 24 during the hook, then jumps per beat; in the brain scene it runs 96 -> 264
export const hoursAt = (f: number) => {
  const b = beatOf(f);
  if (b === 0) return lerp(0, 24, ease(f / (B[1] - 6)));
  if (b === 4) return lerp(96, 264, ease((f - B[4]) / (B[5] - B[4] - 20)));
  return H[b];
};
// eyelids: 0 open .. 1 shut, with the two microsleeps in beat 2
export const lidsAt = (f: number) => {
  let v = 0;
  for (const [a, b] of T.micro) v = Math.max(v, f < a - 14 ? 0 : f < a ? lerp(0.35, 1, (f - a + 14) / 14) : f < b ? 1 : f < b + 4 ? lerp(1, 0.1, (f - b) / 4) : 0);
  return v;
};
export const blackoutAt = (f: number) => Math.max(...T.micro.map(([a, b]) => (f < a ? 0 : f < a + 5 ? (f - a) / 5 : f < b - 2 ? 1 : f < b + 2 ? 1 - (f - b + 2) / 4 : 0)));

type Shot = { pos: THREE.Vector3; look: THREE.Vector3; fov: number; roll?: number };

export const World: React.FC<{ f: number; g: GLTF }> = ({ f, g }) => {
  const { camera, scene } = useThree();
  const b = beatOf(f), l = f - B[b], hours = hoursAt(f);
  const pc = camera as THREE.PerspectiveCamera;
  const set = (s: Shot) => { pc.position.copy(s.pos); pc.up.set(Math.sin(s.roll ?? 0), Math.cos(s.roll ?? 0), 0); pc.lookAt(s.look); pc.fov = s.fov; pc.near = 0.05; pc.far = 200; pc.updateProjectionMatrix(); };
  if (b === 4) {
    scene.fog = null;
    set({ pos: V(0, 0.9, lerp(7.4, 6.6, l / (B[5] - B[4]))), look: V(0, 0.9, 0), fov: 40 });
    return <Brain f={f} u={sat(l / (B[5] - B[4] - 20))} />;
  }
  let pose: Pose, pos: [number, number, number], ry = 0, rz = 0, hall = 0, dim = 0, shot: Shot;
  if (b === 0) {                                                  // at the desk, the clock racing
    pose = { clip: "Sitting", t: f / 30, bags: sat(f / 75) * 0.4, lids: 0.1 };
    pos = [2.05, 0, -0.8]; ry = Math.PI / 2;
    const u = ease(f / 75); shot = { pos: V(lerp(0.2, 0.9, u), lerp(2.1, 1.7, u), lerp(3.4, 2.3, u)), look: V(2.3, 1.75, -0.9), fov: 44 };
  } else if (b === 1) {                                           // 24 h: staggering across the room
    const u = l / (B[2] - B[1]), x = lerp(1.6, -1.3, u), z = 0.5 + Math.sin(l * 0.09) * 0.45;
    pose = { clip: "Walk", t: l / 30 * 0.8, bags: 0.5, lids: 0.3, nod: 0.15 };
    pos = [x, 0, z]; ry = -Math.PI / 2 + Math.cos(l * 0.09) * 0.45; rz = Math.sin(l * 0.16) * 0.13;
    shot = { pos: V(x * 0.5 + 0.3, 1.5, 5.6), look: V(x, 1.75, z), fov: 40, roll: Math.sin(l * 0.07) * 0.1 };
  } else if (b === 2) {                                           // 48 h: microsleeps, close on the face
    const lids = lidsAt(f), shut = sat((lids - 0.6) / 0.4);
    pose = { clip: "Idle", t: f / 30, bags: 0.8, lids, nod: shut * 0.9 + 0.08, pale: 0.4 };
    pos = [0.2, 0, 0.6]; ry = 0.15;
    shot = { pos: V(0.6, 1.66, 2.5), look: V(0.2, 1.86 - shut * 0.06, 0.6), fov: 30 };
  } else if (b === 3) {                                           // 72 h: the room turns on him
    hall = ease(l / 50);
    pose = { clip: "Idle", t: f / 30, bags: 1, lids: 0.15, pale: 0.7, turn: Math.sin(l * 0.14) * 0.9 };
    pos = [0.2, 0, 0.6]; ry = Math.sin(l * 0.07) * 0.5;
    const a = 0.25 + l * 0.004; shot = { pos: V(Math.sin(a) * 5.2, 1.7, Math.cos(a) * 5.2 + 0.4), look: V(0, 1.7, -0.4), fov: 46, roll: Math.sin(l * 0.06) * 0.12 * hall };
  } else {                                                        // the crash: face-first onto the bed
    const t = (f - T.fall) / 30, down = sat((f - T.fall - 22) / 26);
    pose = { clip: t < 0 ? "Idle" : "Death", t: t < 0 ? f / 30 : t, bags: 1, lids: t < 0 ? 0.7 : 1, pale: 0.6, nod: t < 0 ? 0.5 : 0 };
    pos = [-0.72, down * 0.4, -1.0]; ry = -Math.PI / 2; dim = ease((f - T.fall - 40) / 40) * 0.75;
    const u = ease(l / 150); shot = { pos: V(lerp(1.9, 2.6, u), lerp(1.5, 2.3, u), lerp(2.6, 3.8, u)), look: V(-1.1, 1.3, -1.0), fov: 42 };
  }
  set(shot);
  scene.fog = new THREE.Fog("#0a1030", 30, 90);
  const tod = (hours + 23) % 24, day = THREE.MathUtils.clamp(Math.cos((tod - 12) / 12 * Math.PI) * 1.6 + 0.5, 0, 1);
  const hc = new THREE.Color().setHSL((0.75 + Math.sin(f * 0.05) * 0.2) % 1, 0.9, 0.55);
  const lit = 1 - dim;
  return (
    <>
      <Room f={f} hours={hours} hall={hall} dim={dim} />
      <hemisphereLight args={[new THREE.Color("#8a90d8").lerp(hc, hall * 0.8), "#2a2030", (0.55 + day * 0.7) * (1 - dim * 0.6)]} />
      <directionalLight position={[1, 4, -9]} intensity={day * 3.2} color="#fff0d8" castShadow shadow-mapSize={[2048, 2048]} shadow-camera-left={-6} shadow-camera-right={6} shadow-camera-top={6} shadow-camera-bottom={-6} shadow-camera-near={1} shadow-camera-far={30} shadow-bias={-0.0004} shadow-normalBias={0.02} />
      <directionalLight position={[2, 3, 6]} intensity={0.9 * lit} color={new THREE.Color("#c8d0ff").lerp(hc, hall)} castShadow shadow-mapSize={[2048, 2048]} shadow-camera-left={-6} shadow-camera-right={6} shadow-camera-top={6} shadow-camera-bottom={-6} shadow-bias={-0.0004} shadow-normalBias={0.02} />
      <pointLight position={[2.7, 1.2, -0.8]} intensity={9 * lit} distance={5} decay={1.5} color="#7ac8ff" />
      <pointLight position={[-0.45, 0.95, -2.3]} intensity={7 * lit} distance={5} decay={1.5} color="#ffb060" />
      {hall > 0 && <pointLight position={[0, 2.4, 0.5]} intensity={10 * hall} distance={7} color={hc} />}
      {b === 2 && <pointLight position={[0.9, 1.9, 2.4]} intensity={9} distance={6} decay={1.4} color="#cfe0ff" />}
      <Sleeper g={g} pose={pose} pos={pos} ry={ry} rz={rz} />
    </>
  );
};
