import React from "react";
import * as THREE from "three";
import { useThree } from "@react-three/fiber";
import T from "./timeline.json";
import { Look } from "./Man";
import { Hero } from "./Hero";
import { GLTF } from "three/examples/jsm/loaders/GLTFLoader.js";
import { Gym } from "./Gym";
import { Vessel, Heart, Molecules } from "./Inside";

const B = T.beats;
const sat = (v: number) => Math.min(1, Math.max(0, v));
const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const ease = (t: number) => { t = sat(t); return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
const V = (x: number, y: number, z: number) => new THREE.Vector3(x, y, z);
const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };
const span = (f: number, a: number[]) => ease((f - a[0]) / (a[1] - a[0]));

export const sceneOf = (f: number) => (f >= B[3] && f < T.heart ? "vessel" : f >= T.heart && f < B[4] ? "heart" : f >= T.molecules[0] && f < T.molecules[1] ? "molecules" : "gym");
export const bpmAt = (f: number) => Math.round(lerp(72, 168, sat((f - T.heart) / (B[4] - T.heart))));

const lookAt = (f: number): Look => ({
  f,
  m: 1 + 0.9 * span(f, T.muscle),
  beard: span(f, T.beard), acne: span(f, T.acne), hair: span(f, T.hair),
  flush: sat((f - 330) / 140) * 0.9, chest: span(f, T.chest), sweat: f > 690 ? sat((f - 690) / 20) : 0,
  rip: f >= T.rip ? f - T.rip : -1,
  flex: f < 125 ? 0 : f < B[2] ? ease((f - 125) / 12) : 1 - ease((f - B[2]) / 16),
  curl: f < T.drop ? 0.5 + 0.5 * Math.sin(f * 0.16 - 1.2) : 0,
  holding: f < T.drop,
  lookDown: f >= 618 && f < B[5] + 10 ? ease((f - 618) / 14) : 0,
  slump: f >= B[5] ? ease((f - B[5] - 10) / 40) * (1 - ease((f - 872) / 26)) : 0,
  brow: sat((1 + 0.9 * span(f, T.muscle) - 1) * 1.2) * (f > B[5] ? 0.3 : 1),
});

type Shot = { pos: THREE.Vector3; look: THREE.Vector3; fov: number };
const gymShot = (f: number): Shot => {
  const s0: Shot = { pos: V(lerp(1.4, 0.9, ease(f / 90)), lerp(1.05, 1.15, ease(f / 90)), lerp(5.6, 4.7, ease(f / 90))), look: V(0, 1.27, 0), fov: 34 };
  const a = lerp(0.55, -0.35, (f - B[1]) / (B[2] - B[1]));
  const s1: Shot = { pos: V(Math.sin(a) * 3.4, 0.95, Math.cos(a) * 3.4), look: V(0, 1.47, 0), fov: 36 };
  const u2 = (f - B[2]) / (B[3] - B[2]);
  const s2: Shot = { pos: V(lerp(0.5, 0.3, u2), lerp(1.8, 1.76, u2), lerp(1.55, 1.3, u2)), look: V(0, 1.72, 0), fov: 34 };
  const u4 = (f - 600) / (B[5] - 600);
  const s4: Shot = { pos: V(lerp(0.8, 0.55, u4), lerp(1.55, 1.5, u4), lerp(2.45, 2.15, u4)), look: V(0, 1.56, 0), fov: 34 };
  const u5 = ease((f - B[5]) / 120);
  const s5: Shot = { pos: V(lerp(1.0, 2.2, u5), lerp(1.45, 1.4, u5), lerp(2.8, 5.4, u5)), look: V(0, lerp(1.5, 1.3, u5), 0), fov: 36 };
  const end0: Shot = { pos: V(1.4, 1.05, 5.6), look: V(0, 1.27, 0), fov: 34 };
  const mix = (p: Shot, q: Shot, t: number): Shot => ({ pos: p.pos.clone().lerp(q.pos, ease(t)), look: p.look.clone().lerp(q.look, ease(t)), fov: lerp(p.fov, q.fov, ease(t)) });
  if (f < B[1] - 10) return s0;
  if (f < B[1] + 14) return mix(s0, s1, (f - (B[1] - 10)) / 24);
  if (f < B[2] - 8) return s1;
  if (f < B[2] + 16) return mix(s1, s2, (f - (B[2] - 8)) / 24);
  if (f < B[3]) return s2;
  if (f < B[5]) return s4;
  if (f < 872) return s5;
  return mix(s5, end0, (f - 872) / 28);
};

export const World: React.FC<{ f: number; g: GLTF }> = ({ f, g }) => {
  const { camera, scene } = useThree();
  const sc = sceneOf(f);
  const pc = camera as THREE.PerspectiveCamera;
  const set = (s: Shot, shake = 0) => { pc.position.set(s.pos.x + Math.sin(f * 2.3) * shake, s.pos.y + Math.cos(f * 1.9) * shake, s.pos.z); pc.up.set(0, 1, 0); pc.lookAt(s.look); pc.fov = s.fov; pc.near = 0.02; pc.far = 400; pc.updateProjectionMatrix(); };
  if (sc !== "gym") scene.fog = null;
  if (sc === "vessel") { set({ pos: V(Math.sin(f * 0.03) * 0.08, Math.cos(f * 0.025) * 0.08, 2.2), look: V(0, 0, -10), fov: 55 }); return <Vessel f={f} t0={B[3]} t1={T.heart} />; }
  if (sc === "heart") { const ph = (f / 30) * (bpmAt(f) / 60); set({ pos: V(0.3, 0.25, lerp(4.6, 3.9, (f - T.heart) / 45)), look: V(0, 0.1, 0), fov: 40 }, Math.pow(Math.max(0, Math.sin(ph * Math.PI * 2)), 8) * 0.03); return <Heart f={f} bpm={bpmAt(f)} />; }
  if (sc === "molecules") { set({ pos: V(Math.sin(f * 0.01) * 0.6, 0, 9.5), look: V(0, 0, 0), fov: 50 }); return <Molecules f={f} t0={T.molecules[0]} />; }

  const L = lookAt(f);
  const pulse = (f % T.every) < 6 && f > 10 ? (1 - (f % T.every) / 6) * 0.012 * (1 + f / 400) : 0;
  set(gymShot(f), pulse);
  scene.fog = new THREE.Fog("#e8a070", 30, 140);
  const hairFall = f >= T.hair[0] && f < B[3] + 10;
  return (
    <>
      <Gym f={f} dropT={f >= T.drop ? f - T.drop : -1} />
      <hemisphereLight args={["#ffe2c8", "#4a3a4a", 0.7]} />
      {/* sunset through the factory windows: long warm shadows of the window grid on the floor */}
      <directionalLight position={[-3, 5.5, -12]} intensity={4.2} color="#ffb070" castShadow shadow-mapSize={[4096, 4096]} shadow-camera-left={-7} shadow-camera-right={7} shadow-camera-top={7} shadow-camera-bottom={-7} shadow-camera-near={1} shadow-camera-far={40} shadow-bias={-0.0003} shadow-normalBias={0.02} />
      {/* soft key from the camera side and the pendant lamps */}
      <directionalLight position={[2.5, 3, 5]} intensity={1.3} color="#ffe8d8" />
      {[-2.5, 0, 2.5].map(x => <pointLight key={x} position={[x, 3.45, -0.8]} intensity={7} distance={6} decay={1.6} color="#ffcf98" />)}
      <pointLight position={[-1.5, 1.8, -2]} intensity={5} distance={5} decay={1.5} color="#ff9a5a" />
      <Hero g={g} L={L} />
      {hairFall && Array.from({ length: 14 }, (_, i) => {
        const st = T.hair[0] + i * 5, u = (f - st) / 40;
        if (u < 0 || u > 1) return null;
        return <mesh key={i} position={[(rnd(i, 1) - 0.5) * 0.18 + u * (rnd(i, 2) - 0.5) * 0.2, 1.8 - u * 1.6, 0.04 + (rnd(i, 3) - 0.3) * 0.12]} rotation={[u * 6, u * 4, u * 5]}><boxGeometry args={[0.03, 0.004, 0.004]} /><meshStandardMaterial color="#3a2418" /></mesh>;
      })}
    </>
  );
};
