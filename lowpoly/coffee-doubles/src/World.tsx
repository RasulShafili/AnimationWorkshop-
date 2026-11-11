import React from "react";
import * as THREE from "three";
import { useThree } from "@react-three/fiber";
import T from "./timeline.json";
import { Cafe } from "./Cafe";
import { Synapse } from "./Synapse";

const B = T.beats;
export const sat = (v: number) => Math.min(1, Math.max(0, v));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const ease = (t: number) => { t = sat(t); return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
export const beatOf = (f: number) => { let i = 0; while (i < B.length - 2 && f >= B[i + 1]) i++; return i; };
export const cupsAt = (f: number) => T.cupsAt.filter(a => f >= a).length;
export const bpmAt = (f: number) => { const c = Math.max(1, cupsAt(f)); return Math.round(Math.min(185, 72 + Math.log2(c) * 27)); };
// stage drives jitter and the laptop: 0 calm .. 4 danger
export const stageAt = (f: number) => { const b = beatOf(f); return b <= 4 ? b : 5; };
const V = (x: number, y: number, z: number) => new THREE.Vector3(x, y, z);

export const World: React.FC<{ f: number }> = ({ f }) => {
  const { camera, scene } = useThree();
  const pc = camera as THREE.PerspectiveCamera, b = beatOf(f);
  scene.fog = null;
  if (f >= B[5] && f < T.crash) {
    pc.position.set(Math.sin(f * 0.01) * 0.3, 0.55, 4.2); pc.up.set(0, 1, 0); pc.lookAt(0, 0.4, 0); pc.fov = 42; pc.updateProjectionMatrix();
    return <Synapse l={f - B[5]} release={T.release - B[5]} total={T.crash - B[5]} />;
  }
  const stage = stageAt(f), bpm = bpmAt(f);
  // POV: seated at the table; heartbeat pulse and tremor grow with the cups
  const beatPh = (f / 30) * (bpm / 60), pulse = Math.pow(Math.max(0, Math.sin(beatPh * Math.PI * 2)), 10);
  const tremor = [0, 0.0006, 0.003, 0.009, 0.018, 0, 0][stage] ?? 0;
  const hook = ease(f / 22);
  const hk = ease((f - 26) / 40);
  let pos = V(lerp(0.56, 0.16, hk) + Math.sin(f * 0.031) * 0.015, lerp(0.98, 1.42, hk), lerp(0.36, 1.3, hk));
  let look = V(lerp(0.34, 0.24, hk), lerp(0.86, 0.95, hk), lerp(0.02, -0.35, hk)), roll = 0;
  const crash = sat((f - T.crash) / 20), fallen = ease((f - T.crash - 6) / 18), dim = ease((f - T.crash) / 30) * 0.65;
  if (f >= T.crash) {                       // head drops onto the table and rolls sideways
    pos = V(lerp(0.05, -0.55, crash), lerp(1.42, 0.86, ease(crash)), lerp(1.3, 0.2, crash));
    look = V(lerp(0.12, 0.45, crash), lerp(0.95, 0.85, crash), lerp(-0.35, -0.1, crash)); roll = -1.1 * ease(crash);
  }
  pos.x += Math.sin(f * 3.1) * tremor + Math.sin(f * 1.7) * tremor * 0.6; pos.y += Math.cos(f * 2.7) * tremor;
  pc.position.copy(pos); pc.up.set(Math.sin(roll), Math.cos(roll), 0); pc.lookAt(look);
  pc.fov = 58 - pulse * (stage >= 3 ? 2.2 : stage === 2 ? 0.8 : 0); pc.near = 0.02; pc.far = 120; pc.updateProjectionMatrix();
  const lit = 1 - dim, danger = stage === 4 && Math.floor(f / 6) % 2 === 0 ? 1 : 0;
  return (
    <>
      <Cafe f={f} cups={cupsAt(f)} stage={f >= T.crash ? 5 : stage} fallen={fallen} dim={dim} />
      <hemisphereLight args={[new THREE.Color("#fff0e0").lerp(new THREE.Color("#ff8a8a"), stage >= 3 ? 0.25 : 0), "#5a4030", (0.55 + 0.1 * Math.sin(f * 0.02)) * (1 - dim * 0.7)]} />
      <directionalLight position={[1.5, 4, -6]} intensity={2.0 * lit} color="#fff4e0" castShadow shadow-mapSize={[2048, 2048]} shadow-camera-left={-4} shadow-camera-right={4} shadow-camera-top={4} shadow-camera-bottom={-4} shadow-camera-near={1} shadow-camera-far={20} shadow-bias={-0.0004} shadow-normalBias={0.02} />
      <directionalLight position={[0.5, 2, 2]} intensity={0.5 * lit} color="#ffe8d0" />
      {[-1.4, 1.4].map(x => <pointLight key={x} position={[x, 2.5, -0.8]} intensity={3 * lit} distance={4} decay={1.5} color="#ffc890" />)}
      <pointLight position={[0, 1.05, -0.05]} intensity={(danger ? 4 : 1.2) * lit} distance={1.2} decay={1.5} color={danger ? "#ff3a3a" : "#8ab0ff"} />
    </>
  );
};
