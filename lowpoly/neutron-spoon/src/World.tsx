import React from "react";
import * as THREE from "three";
import { useThree } from "@react-three/fiber";
import T from "./timeline.json";
import { BlastCity, StarCollapse, Seesaw, EarthCut, EarthBlast, sat, lerp, ease } from "./Scenes";

const B = T.beats;
export const beatOf = (f: number) => { let i = 0; while (i < B.length - 2 && f >= B[i + 1]) i++; return i; };
const V = (x: number, y: number, z: number) => new THREE.Vector3(x, y, z);
// the rewind: frames 100-130 play the cold open backwards, fast
export const sceneFrame = (f: number) => (f >= B[1] && f < B[2] ? Math.max(0, 96 - (f - B[1]) * 3.2) : f);

export const World: React.FC<{ f: number }> = ({ f: f0 }) => {
  const { camera, scene } = useThree();
  const pc = camera as THREE.PerspectiveCamera, f = sceneFrame(f0), b = beatOf(f0);
  const set = (pos: THREE.Vector3, look: THREE.Vector3, fov: number, shake = 0) => {
    pc.position.set(pos.x + Math.sin(f * 2.3) * shake, pos.y + Math.cos(f * 1.9) * shake, pos.z); pc.up.set(0, 1, 0); pc.lookAt(look); pc.fov = fov; pc.near = 0.05; pc.far = 900; pc.updateProjectionMatrix();
  };
  if (b <= 1) {
    const t = f - T.boom, sh = t >= 0 && t < 30 ? (1 - t / 30) * 2.5 : 0;
    set(V(lerp(55, 70, sat(f / 100)), lerp(26, 34, sat(f / 100)), lerp(75, 95, sat(f / 100))), V(0, lerp(14, 24, sat((f - T.boom) / 60)), 0), 50, sh);
    return <BlastCity f={f} boom={T.boom} spoonIn={T.spoonIn} />;
  }
  scene.fog = null;
  if (b === 2) { const u = (f - B[2]) / (B[3] - B[2]); set(V(lerp(0, 0.6, u), lerp(0.5, 0.3, u), lerp(26, f > T.collapse + 10 ? 4.2 : 24, ease((f - T.collapse - 10) / 40))), V(f > T.collapse + 40 ? 0.5 * ease((f - T.collapse - 40) / 30) : 0, 0, 0), 42); return <StarCollapse f={f} collapse={T.collapse} />; }
  if (b === 3) { const l = f - B[3]; set(V(lerp(-1.5, 0.5, l / 125), 2.6, lerp(16.5, 15, l / 125)), V(0, 0.3, 0), 46); return <Seesaw f={f} l={l} />; }
  if (b === 4) { const l = f - B[4]; set(V(lerp(-9.5, -8.3, l / 125), 5, lerp(10.5, 9.2, l / 125)), V(0, 0.2, 0), 44); return <EarthCut f={f} l={l} />; }
  if (b === 5) {
    const l = f - B[5];
    if (f < T.boom2 + 90) {
      const t = f - T.boom2, sh = t >= 0 && t < 40 ? (1 - t / 40) * 3 : 0;
      set(V(lerp(-60, -80, sat(l / 160)), lerp(18, 40, sat((f - T.boom2) / 80)), lerp(70, 110, sat(l / 160))), V(0, lerp(16, 30, sat((f - T.boom2) / 60)), 0), 50, sh);
      return <BlastCity f={f} boom={T.boom2} spoonIn={B[5] + 8} />;
    }
    const t = f - T.boom2; set(V(0, 1.2, lerp(14, 16, sat((t - 90) / 120))), V(0, 0.4, 0), 42); return <EarthBlast f={f} t={t - 90} />;
  }
  const t = f - T.boom2; set(V(0, 1.2, lerp(16, 17, sat((f - B[6]) / 100))), V(0, 0.4, 0), 42); return <EarthBlast f={f} t={t - 90} />;
};
