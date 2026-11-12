import React from "react";
import * as THREE from "three";
import { useThree } from "@react-three/fiber";
import T from "./timeline.json";
import { Glow, sat, lerp, ease } from "./Scenes";
import { StormWorld, SPIN } from "./Hurricane";
import { RainCity } from "./RainCity";

const B = T.beats;
export const beatOf = (f: number) => { let i = 0; while (i < B.length - 2 && f >= B[i + 1]) i++; return i; };
const V = (x: number, y: number, z: number) => new THREE.Vector3(x, y, z);

const Bomb: React.FC<{ y: number }> = ({ y }) => (
  <group position={[0, y, 0]} rotation={[0, 0, 0.08]}>
    <mesh><capsuleGeometry args={[0.32, 1.6, 4, 12]} /><meshStandardMaterial color="#4a5a3a" metalness={0.5} roughness={0.4} /></mesh>
    {[0, 1, 2, 3].map(k => <mesh key={k} position={[0, 1.15, 0]} rotation={[0, k * Math.PI / 2, 0]}><boxGeometry args={[0.9, 0.5, 0.04]} /><meshStandardMaterial color="#3a4a2a" /></mesh>)}
    <mesh position={[0, -0.1, 0.33]}><boxGeometry args={[0.25, 0.25, 0.01]} /><meshBasicMaterial color="#ffd040" /></mesh>
    <mesh position={[0, 4, 0]}><cylinderGeometry args={[0.05, 0.3, 6, 8, 1, true]} /><meshBasicMaterial color="#ffffff" transparent opacity={0.25} depthWrite={false} /></mesh>
  </group>
);

export const World: React.FC<{ f: number }> = ({ f }) => {
  const { camera, scene } = useThree();
  const pc = camera as THREE.PerspectiveCamera, b = beatOf(f), lf = f - B[b];
  const set = (pos: THREE.Vector3, look: THREE.Vector3, fov: number, shake = 0) => {
    pc.position.set(pos.x + Math.sin(f * 2.3) * shake, pos.y + Math.cos(f * 1.9) * shake, pos.z); pc.up.set(0, 1, 0); pc.lookAt(look); pc.fov = fov; pc.near = 0.1; pc.far = 1500; pc.updateProjectionMatrix();
  };
  scene.fog = null;
  const nt = f - T.boom;
  if (b === 0) { set(V(0, lerp(120, 95, ease(lf / 90)), lerp(34, 26, lf / 90)), V(0, 0, 0), 46); return <StormWorld f={f} />; }
  if (b === 1) { const u = lf / 100; set(V(lerp(96, 86, u), lerp(5, 6, u), lerp(40, 26, u)), V(0, 8, -5), 46); return <StormWorld f={f} />; }
  if (b === 2) {
    const y = lerp(46, 1.5, sat((f - T.drop) / (T.boom - T.drop)) ** 1.6);
    set(V(2.2, 0.8, 2.2), V(-1, lerp(18, 7, sat((f - T.drop) / 95)), -1), 66, f > T.boom - 12 ? 0.05 : 0);
    return <group><StormWorld f={f} sky="#5a8ac8" /><Bomb y={y} /></group>;
  }
  if (b === 3) { set(V(0, 40, lerp(52, 60, sat(nt / 80))), V(0, 5, 0), 50, nt < 25 ? (1 - nt / 25) * 1.2 : 0); return <StormWorld f={f} nukeT={nt} push={sat(nt / 20) * sat(1 - (nt - 30) / 60)} />; }
  if (b === 4) { const a = 0.6 + lf * 0.004; set(V(Math.sin(a) * 75, 58, Math.cos(a) * 75), V(0, 2, 0), 48); return <StormWorld f={f} nukeT={nt} />; }
  if (b === 5) { set(V(lerp(10, 26, lf / 160), 125, 55), V(lerp(14, 30, lf / 160), 0, 0), 50); return <StormWorld f={f} nukeT={nt} falloutT={f - B[5] + 30} />; }
  if (b === 6 || (b === 7 && f < T.finalAerial)) {
    const u = (f - T.rainCut) / 200;
    set(V(lerp(70, 50, u), lerp(22, 14, u), lerp(80, 60, u)), V(0, lerp(10, 8, u), 0), 50);
    return <RainCity f={f} green={sat((f - T.rainCut) / 20)} />;
  }
  set(V(0, lerp(110, 120, sat((f - T.finalAerial) / 150)), lerp(30, 34, sat((f - T.finalAerial) / 150))), V(0, 0, 0), 46);
  return <StormWorld f={f} />;
};
