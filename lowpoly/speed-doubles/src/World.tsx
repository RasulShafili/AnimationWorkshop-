import React from "react";
import * as THREE from "three";
import { useThree } from "@react-three/fiber";
import T from "./timeline.json";
import { Glow, sat, lerp, ease } from "./Scenes";
import { Runner } from "./Runner";
import { Desert } from "./Desert";
import { EarthLeave, MoonPass, Warp, Streak } from "./Space";
import { GLTF } from "three/examples/jsm/loaders/GLTFLoader.js";

const B = T.beats;
export const beatOf = (f: number) => { let i = 0; while (i < B.length - 2 && f >= B[i + 1]) i++; return i; };
const V = (x: number, y: number, z: number) => new THREE.Vector3(x, y, z);
// visual scroll speed (m/frame) per level; real speeds are far beyond what a camera could show
const VIS = [0.17, 0.67, 1.33, 3.0, 5.0, 7.0, 9.0, 10.0, 10.0, 10.0, 10.0];
const visAt = (f: number) => { const b = beatOf(f); return lerp(VIS[Math.max(0, b - 1)], VIS[b], ease((f - B[b]) / 12)); };
const DIST: number[] = [], PHASE: number[] = [];
{ let d = 0, p = 0; for (let f = 0; f <= T.total; f++) { DIST.push(d); PHASE.push(p); const v = visAt(f); d += v; p += Math.min(2.4, 1 + v * 0.45) / 30; } }
const RZ = -1.5;

export const World: React.FC<{ f: number; glb: Record<string, GLTF> | null }> = ({ f, glb }) => {
  const { camera, scene } = useThree();
  const pc = camera as THREE.PerspectiveCamera, b = beatOf(f), lf = f - B[b];
  const kick = lf < 18 && b >= 1 ? (2 + b * 0.6) * Math.exp(-lf / 4) : 0;
  const set = (pos: THREE.Vector3, look: THREE.Vector3, fov: number, shake = 0) => {
    pc.position.set(pos.x + Math.sin(f * 2.3) * shake, pos.y + Math.cos(f * 1.9) * shake, pos.z); pc.up.set(0, 1, 0); pc.lookAt(look); pc.fov = fov - kick; pc.near = 0.05; pc.far = 1200; pc.updateProjectionMatrix();
  };
  scene.fog = null;
  if (!glb) return null;
  const g = glb["man.glb"], v = visAt(f), dist = DIST[f] ?? 0, ph = PHASE[f] ?? 0;
  const run = (heat = 0, y = 0, rz = 0) => <Runner g={g} t={ph} heat={heat} pos={[0, y, RZ]} ry={Math.PI / 2} rz={rz} />;
  const vib = Math.min(0.06, v * 0.006);
  if (b <= 6) {
    let extra: React.ReactNode = null, heat = 0, carXs: number[] = [], boom = -1, hot = 0, melt = 0;
    if (b === 0) set(V(lerp(0.2, 0.8, lf / 90), 1.5, 4.2), V(0.3, 1.05, RZ), 40);
    if (b === 1) set(V(4.6, 0.7, -0.4), V(0, 1.1, RZ), 42, vib);
    if (b === 2) { carXs = [0, 1, 2, 3].map(i => 10 + i * 16 + (1.11 - v) * lf); set(V(-4.5 + lf * 0.02, 2.4, -10.5), V(2.5, 1.0, 0), 44, vib); }
    if (b === 3) {
      set(V(-6.5, 2.4, RZ + 0.6), V(6, 1.0, RZ), 46, vib);
      extra = Array.from({ length: 12 }, (_, i) => <Glow key={i} size={1.5 + i * 0.5} color="#e8c090" opacity={0.35 - i * 0.025} pos={[-1 - i * 1.4, 0.4 + i * 0.12, RZ + Math.sin(f * 0.3 + i) * 0.3]} />);
    }
    if (b === 4) {
      const k = f - T.boom; boom = k;
      set(V(1.5, 3.4, 13), V(-2.5, 1.2, RZ), 46, k >= 0 && k < 20 ? (1 - k / 20) * 0.3 : vib);
      const Lc = 11, rad = Lc * Math.tan(32 * Math.PI / 180);
      extra = <group>
        {k >= -4 && <mesh position={[0.5 - Lc / 2, 1.0, RZ]} rotation={[0, 0, -Math.PI / 2]}><coneGeometry args={[rad, Lc, 40, 1, true]} /><meshStandardMaterial color="#ffffff" transparent opacity={0.13} side={THREE.DoubleSide} depthWrite={false} /></mesh>}
        {k >= 0 && k < 26 && <mesh position={[-0.2, 1.0, RZ]} rotation={[0, 0, Math.PI / 2]} scale={[1, 1 + k * 0.08, 1 + k * 0.08]}><cylinderGeometry args={[1.6, 2.4, 0.9, 32, 1, true]} /><meshStandardMaterial color="#ffffff" transparent opacity={0.55 * (1 - k / 26)} side={THREE.DoubleSide} depthWrite={false} /></mesh>}
        {k >= 0 && <mesh rotation={[-Math.PI / 2, 0, 0]} position={[-k * 0.6, 0.06, RZ]}><ringGeometry args={[Math.max(0.1, k * 0.9 - 1), k * 0.9, 48]} /><meshBasicMaterial color="#fff4e0" transparent opacity={sat(1 - k / 40) * 0.7} side={THREE.DoubleSide} /></mesh>}
        {k >= 0 && Array.from({ length: 30 }, (_, i) => <Glow key={i} size={3 + (i % 5)} color="#e8c8a0" opacity={sat(0.5 - k / 80)} pos={[-k * 0.4 - (i % 10) * 2, 0.5 + (i % 3), RZ + ((i * 7) % 11 - 5) * (0.5 + k * 0.05)]} />)}
      </group>;
    }
    if (b === 5) {
      heat = lerp(0.15, 0.5, ease(lf / 50)); hot = 0.2; melt = sat(lf / 40) * 0.5;
      set(V(1.7, 0.5, RZ + 2.2), V(0, 0.55, RZ), 40, vib);
      extra = Array.from({ length: 14 }, (_, i) => <Glow key={i} size={0.6 + i * 0.12} color={i < 4 ? "#ffd070" : "#ff6a1a"} opacity={0.8 - i * 0.05} pos={[-0.2 - i * 0.35, 0.15 + Math.abs(Math.sin(f * 0.9 + i)) * 0.25, RZ + Math.sin(f * 1.3 + i * 2) * 0.12]} />);
    }
    if (b === 6) {
      heat = lerp(0.5, 1, ease(lf / 30)); hot = 0.6; melt = 1;
      set(V(-9, 4, 9), V(2, 1.2, RZ), 46, vib);
      extra = <group><Glow size={3 + Math.sin(f) * 0.3} color="#ffb060" opacity={0.7} pos={[0.2, 1.0, RZ]} />
        <Streak head={V(-0.4, 1.0, RZ)} dir={V(1, 0, 0)} len={26} w={0.3} /></group>;
    }
    return <group><Desert f={f} dist={dist} v={v} carXs={carXs} boom={boom} hot={hot} melt={melt} />{run(heat)}{extra}</group>;
  }
  if (b === 7 && f < T.orbit) {
    const k = Math.max(0, f - T.lift), y = k * k * 0.006 + k * 0.05;
    set(V(-14, 3 + y * 0.4, 12), V(2, 1 + y * 0.8, RZ), 48, 0.04);
    return <group><Desert f={f} dist={dist} v={v} hot={0.6} melt={1} />
      <group position={[0, y, 0]}>{run(1, 0, k * 0.008)}<Glow size={3} color="#ffb060" opacity={0.7} pos={[0.2, 1.0, RZ]} /><Streak head={V(-0.4, 1.0, RZ)} dir={V(1, y > 0 ? 0.25 : 0, 0)} len={26} w={0.3} /></group>
    </group>;
  }
  if (b === 7) { const t = f - T.orbit; set(V(0, 1.2, lerp(13, 15, sat(t / 60))), V(0.6, 0.8, 0), 42); return <EarthLeave f={f} t={t} />; }
  if (b === 8) { const t = f - B[8]; set(V(0, 1.5, 12), V(0, 0.6, 0), 44, 0); return <MoonPass f={f} t={t} />; }
  const k = b === 9 ? ease((f - B[9]) / 70) : 1;
  set(V(0, 0.25, 0), V(0, 0.1, -10), 58 + k * 12, k * 0.02);
  return <group><Warp f={f} k={k} /><Runner g={g} t={ph} heat={1} pos={[0, -0.9, -3.4]} ry={Math.PI} /><ambientLight intensity={0.5} /></group>;
};
