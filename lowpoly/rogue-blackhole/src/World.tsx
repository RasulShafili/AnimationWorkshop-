import React from "react";
import * as THREE from "three";
import { useThree } from "@react-three/fiber";
import T from "./timeline.json";
import { Sim, coreAt, bodyAt } from "./data";
import { Bodies, Backdrop, DenseField, SkyBand } from "./Bodies";
import { LENS } from "./LensPost";

const B = T.beats;
export const beatOf = (f: number) => { let i = 0; while (i < B.length - 2 && f >= B[i + 1]) i++; return i; };
const sat = (v: number) => Math.min(1, Math.max(0, v));
const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
const ease = (t: number) => { t = sat(t); return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
const V = (a: number[]) => new THREE.Vector3(a[0], a[1], a[2]);
const EARTH = 2, JUPITER = 4;

export type Shot = { mode: "space" | "deep" | "ground"; t: number; re: number; frozen?: boolean };
export const shotAt = (f: number): Shot => {
  const b = beatOf(f), lf = f - B[b], L = B[b + 1] - B[b];
  if (b === 0) return { mode: "space", t: 22.6 + lf * 0.006, re: 1 };
  if (b === 1) return { mode: "deep", t: 0, re: 1 };
  if (b === 2) return { mode: "ground", t: 2 + lf * 0.01, re: 1 };
  if (b === 3) return { mode: "space", t: lerp(0, 21.2, ease(lf / L) * 0.4 + lf / L * 0.6), re: 1 };
  if (b === 4) return { mode: "space", t: lerp(21.2, 24.6, lf / L), re: 1 };
  if (b === 5) return { mode: "space", t: lerp(24.6, 28.5, lf / L), re: 1 };
  if (b === 6 && f < T.frozenIn) return { mode: "space", t: lerp(28.5, 38, (f - B[6]) / (T.frozenIn - B[6])), re: 1 };
  if (b === 6) return { mode: "ground", t: 40 + (f - T.frozenIn) * 0.02, re: 1, frozen: true };
  return { mode: "space", t: lerp(38, 47, lf / L), re: 1 };
};

// camera for a frame (shared with Video for label/lens projection)
export const cameraFor = (f: number, sim: Sim, pc: THREE.PerspectiveCamera) => {
  const b = beatOf(f), lf = f - B[b], s = shotAt(f);
  const sun = V(coreAt(sim, s.t, 0)), bh = V(coreAt(sim, s.t, 1)), earth = V(bodyAt(sim, s.t, EARTH));
  pc.up.set(0, 0, 1);
  if (s.mode === "deep") { pc.position.set(0, 0, 0); pc.lookAt(1, 0, 0.12); pc.fov = 40; }
  else if (s.mode === "ground") {
    pc.position.copy(earth);
    const target = s.frozen ? sun : bh;                       // today: look toward the incoming (invisible) hole
    pc.lookAt(target); pc.rotateX(-0.22); pc.fov = 70;
  } else {
    let look: THREE.Vector3, dist: number, el = 0.85, az = -1.9 + f * 0.0012;
    if (b === 0) { look = bh.clone().lerp(sun, 0.25); dist = 6; el = 0.7; }
    else if (b === 3) { const u = lf / (B[4] - B[3]), sep = sun.distanceTo(bh); look = sun.clone().lerp(bh, 0.45 * sat((120 - sep) / 60)); dist = Math.min(170, Math.max(16, sep * 2.3 + 10)); el = lerp(1.1, 0.85, u); }
    else if (b === 4) { const sep = sun.distanceTo(bh); look = sun.clone().lerp(bh, 0.45); dist = Math.max(7.5, sep * 2.3 + 4); }
    else if (b === 5) { look = bh.clone().lerp(earth, 0.3); dist = 6.5; el = 0.9; }
    else if (b === 6) { const u = (f - B[6]) / (T.frozenIn - B[6]); look = bh.clone().lerp(earth, 0.3); dist = lerp(9, 16, u); }
    else { look = bh.clone().lerp(earth, 0.3); dist = lerp(10, 13, lf / 120); }
    pc.position.set(look.x + Math.cos(az) * dist * Math.cos(el), look.y + Math.sin(az) * dist * Math.cos(el), look.z + dist * Math.sin(el));
    pc.lookAt(look); pc.fov = 48;
  }
  pc.near = 0.001; pc.far = 5000; pc.updateProjectionMatrix(); pc.updateMatrixWorld();
  return s;
};
export const toScreen = (pc: THREE.PerspectiveCamera, p: number[] | THREE.Vector3) => { const v = (p instanceof THREE.Vector3 ? p.clone() : V(p)).project(pc); return [(v.x + 1) * 540, (1 - v.y) * 960, v.z] as const; };

export const World: React.FC<{ f: number; sim: Sim }> = ({ f, sim }) => {
  const { camera, scene } = useThree();
  const pc = camera as THREE.PerspectiveCamera;
  scene.background = new THREE.Color("#010104"); scene.fog = null;
  const s = cameraFor(f, sim, pc), b = beatOf(f), lf = f - B[b];
  // the lens: where the black hole is on screen and how big its Einstein ring looks (artistic scale ~ 1/distance)
  if (s.mode === "deep") { const u = lf / (B[2] - B[1]); LENS.on = 1; LENS.x = lerp(1180, -100, u); LENS.y = 820 + Math.sin(u * 3) * 40; LENS.re = 95; }
  else {
    const bh = V(coreAt(sim, s.t, 1)), sc = toScreen(pc, bh), d = pc.position.distanceTo(bh);
    LENS.on = sc[2] < 1 && sc[2] > -1 ? 1 : 0; LENS.x = sc[0]; LENS.y = sc[1];
    LENS.re = s.mode === "ground" ? (s.frozen ? 0 : 80) : Math.max(70, Math.min(300, 1000 / Math.max(d, 0.5)));
    if (s.mode === "ground" && s.frozen) LENS.on = 0;
  }
  const eye = [pc.position.x, pc.position.y, pc.position.z];
  const sunD = pc.position.distanceTo(V(coreAt(sim, s.t, 0)));
  if (s.mode === "deep") return <group><Backdrop center={eye} n={14000} /><DenseField /></group>;
  return <group>
    <Backdrop center={eye} dim={s.frozen ? 1.1 : 0.85} />
    <SkyBand center={eye} dim={s.frozen ? 1.2 : 1} />
    <Bodies sim={sim} t={s.t} fov={pc.fov} star={s.mode === "ground" ? 0.002 : 0.016} planetPx={s.mode === "ground" ? 0 : b === 3 ? 16 : 24}
      orbits={b === 3 ? 1 : b === 4 ? sat(1 - lf / 12) * 0.5 : 0} trail={b === 3 ? 6 : 3} sunGlow={s.mode === "ground" ? (s.frozen ? sunD * 0.03 : 0) : sunD * 0.07} />
  </group>;
};
