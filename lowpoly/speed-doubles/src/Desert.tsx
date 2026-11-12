// Endless desert highway at sunrise. The runner stays at x=0; everything scrolls by `dist` (metres).
// `v` is the visual speed in m/frame: scenery stretches into streaks when it gets fast.
import React, { useMemo } from "react";
import * as THREE from "three";
import { Car } from "./kit";
import { Glow, sat } from "./Scenes";

const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };
const L = 260; const wrap = (x: number, l = L) => ((x % l) + l) % l - l / 2;

const Sky: React.FC<{ hot: number }> = ({ hot }) => {
  const geo = useMemo(() => {
    const g = new THREE.SphereGeometry(500, 32, 16), p = g.attributes.position, c = new Float32Array(p.count * 3);
    const top = new THREE.Color("#3a5aa8"), mid = new THREE.Color("#f0a868"), low = new THREE.Color("#ffd8a0");
    for (let i = 0; i < p.count; i++) { const y = p.getY(i) / 500; const col = y > 0.15 ? mid.clone().lerp(top, Math.min(1, (y - 0.15) / 0.5)) : low.clone().lerp(mid, Math.max(0, (y + 0.05) / 0.2)); c.set([col.r, col.g, col.b], i * 3); }
    g.setAttribute("color", new THREE.BufferAttribute(c, 3)); return g;
  }, []);
  return <mesh geometry={geo}><meshBasicMaterial vertexColors side={THREE.BackSide} fog={false} color={new THREE.Color(1, 1, 1).lerp(new THREE.Color(1.2, 0.7, 0.5), hot)} /></mesh>;
};
const Cactus: React.FC<{ s: number }> = ({ s }) => (
  <group scale={s}>
    <mesh position={[0, 1.2, 0]} castShadow><cylinderGeometry args={[0.22, 0.26, 2.4, 7]} /><meshStandardMaterial color="#4a8a4a" flatShading /></mesh>
    <mesh position={[0.35, 1.4, 0]} castShadow><cylinderGeometry args={[0.13, 0.13, 0.9, 6]} /><meshStandardMaterial color="#4a8a4a" flatShading /></mesh>
    <mesh position={[-0.33, 1.0, 0]} castShadow><cylinderGeometry args={[0.12, 0.12, 0.7, 6]} /><meshStandardMaterial color="#4a8a4a" flatShading /></mesh>
  </group>
);

export const Desert: React.FC<{ f: number; dist: number; v: number; carXs?: number[]; boom?: number; hot?: number; melt?: number }> =
  ({ f, dist, v, carXs = [], boom = -1, hot = 0, melt = 0 }) => {
  const stretch = 1 + Math.min(14, Math.max(0, v - 1.5) * 1.2);
  const props = useMemo(() => Array.from({ length: 60 }, (_, i) => ({ x0: rnd(i, 1) * L, z: (rnd(i, 2) > 0.5 ? 1 : -1) * (7 + rnd(i, 3) * 40), kind: rnd(i, 4) > 0.45 ? 0 : 1, s: 0.7 + rnd(i, 5) * 0.9, ry: rnd(i, 6) * 6 })), []);
  const mesas = useMemo(() => Array.from({ length: 9 }, (_, i) => ({ x0: i * 150 + rnd(i, 1) * 60, z: -170 - rnd(i, 2) * 80, w: 30 + rnd(i, 3) * 40, h: 18 + rnd(i, 4) * 26 })), []);
  const signs = [0, 1, 2, 3].map(i => i * 65);
  const b = boom >= 0 ? boom : -1;
  return (
    <group>
      <Sky hot={hot} />
      <fog attach="fog" args={[new THREE.Color("#f0b880").lerp(new THREE.Color("#ff8a50"), hot), 60, 420]} />
      <Glow size={70} color="#fff0c0" opacity={0.9} pos={[260, 18, -380]} />
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow><planeGeometry args={[1400, 1400]} /><meshStandardMaterial color="#d8a068" roughness={1} /></mesh>
      {/* road */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.02, 0]} receiveShadow><planeGeometry args={[1400, 7.5]} /><meshStandardMaterial color="#3a3a44" roughness={0.9} /></mesh>
      {[-3.5, 3.5].map(z => <mesh key={z} rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.03, z]}><planeGeometry args={[1400, 0.18]} /><meshStandardMaterial color="#f0f0f0" /></mesh>)}
      {Array.from({ length: 30 }, (_, i) => <mesh key={i} rotation={[-Math.PI / 2, 0, 0]} position={[wrap(i * 9 - dist, 270), 0.03, 0]} scale={[Math.min(stretch, 3), 1, 1]}><planeGeometry args={[3.5, 0.18]} /><meshStandardMaterial color="#ffd040" /></mesh>)}
      {melt > 0 && <mesh rotation={[-Math.PI / 2, 0, 0]} position={[-200, 0.04, -1.5]}><planeGeometry args={[400, 1.2]} /><meshBasicMaterial color={new THREE.Color(3, 1.2, 0.3)} toneMapped={false} transparent opacity={melt * 0.8} /></mesh>}
      {props.map((p, i) => { const x = wrap(p.x0 - dist); const knock = b >= 0 && x < 0 && Math.abs(p.z) < 25 ? Math.min(1.3, b * 0.05) : 0; return (
        <group key={i} position={[x, 0, p.z]} rotation={[0, p.ry, -knock * (p.kind === 0 ? 1 : 0)]} scale={[stretch, 1, 1]}>
          {p.kind === 0 ? <Cactus s={p.s} /> : <mesh position={[0, 0.4 * p.s, 0]} castShadow><dodecahedronGeometry args={[0.8 * p.s, 0]} /><meshStandardMaterial color="#b8784a" flatShading /></mesh>}
        </group>); })}
      {signs.map((x0, i) => { const x = wrap(x0 - dist); const knock = b >= 0 && x < 0 ? Math.min(1.4, b * 0.06) : 0; return (
        <group key={i} position={[x, 0, -5]} rotation={[0, 0, knock]} scale={[Math.min(stretch, 4), 1, 1]}>
          <mesh position={[0, 1.4, 0]}><cylinderGeometry args={[0.05, 0.05, 2.8, 6]} /><meshStandardMaterial color="#9aa0aa" metalness={0.6} /></mesh>
          <mesh position={[0, 2.6, 0.04]}><boxGeometry args={[1.4, 0.8, 0.05]} /><meshStandardMaterial color="#2a8a4a" /></mesh>
        </group>); })}
      {mesas.map((m, i) => <mesh key={i} position={[wrap(m.x0 - dist * 0.05, 1350), m.h / 2, m.z]}><cylinderGeometry args={[m.w * 0.42, m.w * 0.55, m.h, 7]} /><meshStandardMaterial color="#b85a3a" flatShading /></mesh>)}
      {/* cars on the other lane: driving +x at highway speed; the runner overtakes them */}
      {carXs.map((x, i) => <group key={i} position={[x, 0, 1.8]} scale={3}><Car p={[0, 0, 0]} ry={0} c={["#d83a3a", "#3a7ad8", "#f0c040", "#f0f0f0", "#2a2a30"][i % 5]} lights={0.3} /></group>)}
      {/* speed lines in the air */}
      {v > 2 && Array.from({ length: 40 }, (_, i) => <mesh key={i} position={[wrap(rnd(i, 1) * 200 - dist * 1.3, 200), 0.4 + rnd(i, 2) * 4, -1.5 + (rnd(i, 3) - 0.5) * 10]}><boxGeometry args={[Math.min(30, v * 2), 0.02, 0.02]} /><meshBasicMaterial color="#ffffff" transparent opacity={0.5} /></mesh>)}
      <hemisphereLight args={["#ffd8b0", "#8a5a3a", 0.8]} />
      <directionalLight position={[60, 25, -60]} intensity={2.6} color="#ffd0a0" castShadow shadow-mapSize={[2048, 2048]} shadow-camera-left={-12} shadow-camera-right={12} shadow-camera-top={12} shadow-camera-bottom={-12} />
      <ambientLight intensity={0.25} />
    </group>
  );
};
