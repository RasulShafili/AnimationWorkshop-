import React from "react";
import * as THREE from "three";
import { useThree } from "@react-three/fiber";
import T from "./timeline.json";
import { Sim, coreAt, starAt } from "./data";
import { Galaxy, Backdrop } from "./Galaxy";

const B = T.beats;
export const beatOf = (f: number) => { let i = 0; while (i < B.length - 2 && f >= B[i + 1]) i++; return i; };
const sat = (v: number) => Math.min(1, Math.max(0, v));
const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
const ease = (t: number) => { t = sat(t); return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
const V = (a: number[]) => new THREE.Vector3(a[0], a[1], a[2]);
export const SKY_T = 8.3, FAR = 17;

// what each beat shows: sky (from the Sun's position) or space, at which sim time
export const shotAt = (f: number) => {
  const b = beatOf(f), lf = f - B[b];
  if (b === 0) return { mode: "sky", t: SKY_T - 0.15 + lf * 0.002, shift: 0 };
  if (b === 1) return { mode: "sky", t: 0, shift: FAR, dim: 0.55 };
  if (b === 2) { const u = ease(lf / (B[3] - B[2])); return { mode: "sky", t: lerp(0, SKY_T, u), shift: lerp(FAR, 0, u), dim: lerp(0.55, 1, u) }; }
  if (b === 3) return { mode: "space", t: lerp(6.6, 11.6, lf / (B[4] - B[3])) };
  if (b === 4 && f < T.skyIn) return { mode: "space", t: lerp(11.6, 14.0, (f - B[4]) / (T.skyIn - B[4])), burst: sat((f - B[4]) / 30) };
  if (b === 4) return { mode: "sky", t: lerp(14.0, 15.2, (f - T.skyIn) / (B[5] - T.skyIn)), burst: 1, shift: 0 };
  if (b === 5) return { mode: "space", t: lerp(15.2, 33.5, ease(lf / (B[6] - B[5]))), burst: lerp(1, 0.3, lf / 120) };
  if (b === 6) return { mode: "space", t: 0.6 + lf * 0.004, shift: 0, wide: true };
  return { mode: "sky", t: SKY_T + lf * 0.002, shift: 0 };
};

// camera for a frame: shared by World (applies it) and Video (projects points for the HTML overlays)
export const cameraFor = (f: number, sim: Sim, pc: THREE.PerspectiveCamera) => {
  const b = beatOf(f), lf = f - B[b], s = shotAt(f) as any;
  if (s.mode === "sky") {
    const sun = V(starAt(sim, s.t, sim.sun)), m31 = V(coreAt(sim, s.t, 1)), mw = V(coreAt(sim, s.t, 0));
    const dir = m31.clone().sub(mw).normalize();
    const look = m31.clone().addScaledVector(dir, s.shift ?? 0);
    const fov = b === 1 ? 60 : 78;
    pc.position.copy(sun); pc.up.set(0, 0, 1); pc.lookAt(look);
    pc.rotateZ(0.45);            // tilt so the Milky Way band crosses the sky diagonally
    pc.rotateX(-0.2);            // look a bit below the target: Andromeda sits high in the sky
    pc.fov = fov; pc.near = 0.0005; pc.far = 2000;
  } else {
    const c0 = V(coreAt(sim, s.t, 0)), c1 = V(coreAt(sim, s.t, 1));
    const com = c0.clone().multiplyScalar(1 / 2.3).add(c1.clone().multiplyScalar(1.3 / 2.3));
    const a = 0.9 + f * 0.0016, el = 0.55, dist = s.wide ? 15 : b === 5 ? lerp(4.6, 5.6, lf / 120) : 5.2;
    pc.position.set(com.x + Math.cos(a) * dist * Math.cos(el), com.y + Math.sin(a) * dist * Math.cos(el), com.z + dist * Math.sin(el));
    pc.up.set(0, 0, 1); pc.lookAt(s.wide ? c0.clone().lerp(c1, 0.5) : com); pc.fov = 50; pc.near = 0.01; pc.far = 2000;
  }
  pc.updateProjectionMatrix(); pc.updateMatrixWorld();
  return s;
};
// screen position (px) of a world point for this camera
export const toScreen = (pc: THREE.PerspectiveCamera, p: number[]) => { const v = V(p).project(pc); return [(v.x + 1) * 540, (1 - v.y) * 960, v.z] as const; };

export const World: React.FC<{ f: number; sim: Sim }> = ({ f, sim }) => {
  const { camera, scene } = useThree();
  const pc = camera as THREE.PerspectiveCamera;
  scene.background = new THREE.Color("#010106"); scene.fog = null;
  const s = cameraFor(f, sim, pc);
  if (s.mode === "sky") return <group>
    <Backdrop center={pc.position.clone()} dim={0.8} />
    <Galaxy sim={sim} t={s.t} shiftM31={s.shift ?? 0} fov={pc.fov} star={0.0042} maxPx={3.4} near={0.006} exp={1.5} burst={s.burst ?? 0} m31Dim={s.dim ?? 1} />
  </group>;
  return <group>
    <Backdrop center={pc.position.clone()} dim={0.9} />
    <Galaxy sim={sim} t={s.t} shiftM31={s.shift ?? 0} fov={pc.fov} star={0.0072} maxPx={6} exp={b5(f) ? 1.15 : 0.95} burst={s.burst ?? 0} />
  </group>;
};
const b5 = (f: number) => beatOf(f) === 5;
