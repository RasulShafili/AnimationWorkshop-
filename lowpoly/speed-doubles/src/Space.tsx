// Space shots: Earth with the glowing runner leaving it, the Moon fly-by, and the light-speed warp.
import React, { useMemo } from "react";
import * as THREE from "three";
import { Planet } from "./Planet";
import { Glow, sat } from "./Scenes";

const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };
export const Stars: React.FC<{ n?: number }> = ({ n = 1200 }) => {
  const geo = useMemo(() => { const p = new Float32Array(n * 3); for (let i = 0; i < n; i++) { const u = rnd(i, 1) * 2 - 1, th = rnd(i, 2) * 6.283, s = Math.sqrt(1 - u * u); p.set([Math.cos(th) * s * 300, u * 300, Math.sin(th) * s * 300], i * 3); } const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.BufferAttribute(p, 3)); return g; }, [n]);
  return <points geometry={geo}><pointsMaterial color="#ffffff" size={1.8} sizeAttenuation={false} /></points>;
};
// a glowing streak whose head is at `head`, pointing back along -dir
export const Streak: React.FC<{ head: THREE.Vector3; dir: THREE.Vector3; len: number; w: number }> = ({ head, dir, len, w }) => {
  const q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.clone().normalize());
  const mid = head.clone().addScaledVector(dir.clone().normalize(), -len / 2);
  return <group>
    <mesh position={mid} quaternion={q}><cylinderGeometry args={[w, w * 0.1, len, 10, 1, true]} /><meshBasicMaterial color={new THREE.Color(3, 1.6, 0.6)} toneMapped={false} transparent opacity={0.85} /></mesh>
    <Glow size={w * 14} color="#ffd8a0" opacity={1} pos={[head.x, head.y, head.z]} />
  </group>;
};
export const EarthLeave: React.FC<{ f: number; t: number }> = ({ f, t }) => {
  // the runner skims the surface then flies off tangentially, accelerating
  const R = 3, a0 = 0.9, start = new THREE.Vector3(Math.cos(a0) * R * 1.01, Math.sin(a0) * R * 1.01, 0.6);
  const tang = new THREE.Vector3(-Math.sin(a0), Math.cos(a0), 0).normalize();
  const d = 0.04 * t + 0.0009 * t * t, head = start.clone().addScaledVector(tang, d).add(new THREE.Vector3(0, 0, d * 0.25));
  return <group>
    <color attach="background" args={["#020208"]} /><Stars />
    <Planet f={f} spin={-0.4 + f * 0.0012} />
    <Streak head={head} dir={tang.clone().add(new THREE.Vector3(0, 0, 0.25))} len={Math.min(5, 0.6 + d)} w={0.06} />
    <ambientLight intensity={0.3} /><directionalLight position={[-5, 3, 6]} intensity={2.4} />
  </group>;
};
const moonGeo = () => { const g = new THREE.IcosahedronGeometry(1, 4).toNonIndexed(), p = g.attributes.position, c = new Float32Array(p.count * 3);
  const craters = Array.from({ length: 26 }, (_, i) => { const u = rnd(i, 1) * 2 - 1, a = rnd(i, 2) * 6.283, s = Math.sqrt(1 - u * u); return { d: new THREE.Vector3(Math.cos(a) * s, u, Math.sin(a) * s), r: 0.08 + rnd(i, 3) * 0.2 }; });
  for (let i = 0; i < p.count; i += 3) { const v = new THREE.Vector3(p.getX(i), p.getY(i), p.getZ(i)).normalize(); let k = 0.72 + rnd(i, 7) * 0.08; for (const cr of craters) if (v.distanceTo(cr.d) < cr.r) k -= 0.2; for (let j = 0; j < 3; j++) c.set([k, k, k * 1.02], (i + j) * 3); }
  g.setAttribute("color", new THREE.BufferAttribute(c, 3)); return g; };
export const MoonPass: React.FC<{ f: number; t: number }> = ({ f, t }) => {
  const geo = useMemo(moonGeo, []);
  const x = 14 - t * 0.32;
  return <group>
    <color attach="background" args={["#020208"]} /><Stars />
    <mesh geometry={geo} scale={3.2} position={[-1.2, -0.6, -2]} rotation={[0.2, f * 0.002, 0]}><meshStandardMaterial vertexColors flatShading roughness={1} /></mesh>
    <mesh position={[6, 5, -40]} scale={2}><sphereGeometry args={[1, 24, 16]} /><meshStandardMaterial color="#3a7ad8" /></mesh>
    <Streak head={new THREE.Vector3(x, 2.6 - t * 0.012, 2.5)} dir={new THREE.Vector3(-1, -0.04, 0)} len={Math.min(10, 2 + t * 0.2)} w={0.07} />
    <ambientLight intensity={0.08} /><directionalLight position={[8, 3, 2]} intensity={1.7} />
  </group>;
};
// light-speed warp: star lines rushing past; `k` 0..1 how close to c
export const Warp: React.FC<{ f: number; k: number }> = ({ f, k }) => {
  const lines = useMemo(() => Array.from({ length: 260 }, (_, i) => ({ a: rnd(i, 1) * 6.283, r: 0.6 + rnd(i, 2) * 9, z0: rnd(i, 3) * 120, hue: rnd(i, 4) })), []);
  return <group>
    <color attach="background" args={["#020210"]} />
    {lines.map((l, i) => { const z = ((l.z0 + f * (0.6 + k * 6)) % 120) - 110; const len = 0.2 + k * 14;
      return <mesh key={i} position={[Math.cos(l.a) * l.r, Math.sin(l.a) * l.r, z]} rotation={[Math.PI / 2, 0, 0]}><cylinderGeometry args={[0.02, 0.02, len, 4]} /><meshBasicMaterial color={new THREE.Color().setHSL(0.58 + l.hue * 0.15, 0.6, 0.8).multiplyScalar(1.5)} toneMapped={false} /></mesh>; })}
    <Glow size={6 + k * 8} color="#c8d8ff" opacity={0.6 + k * 0.4} pos={[0, 0, -30]} />
  </group>;
};
