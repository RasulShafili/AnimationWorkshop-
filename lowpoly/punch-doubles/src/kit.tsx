// Low-poly prop kit in the style of the references: gable roofs with chimneys, framed windows with warm panes,
// trim bands, red-trunk trees with faceted crowns, cars, lamps, a floating diorama island with soil layers.
import React, { useMemo } from "react";
import * as THREE from "three";

export const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };
export const sat = (v: number) => Math.min(1, Math.max(0, v));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const ease = (t: number) => { t = sat(t); return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
export const C = (h: string) => new THREE.Color(h);
export const mixC = (a: string | THREE.Color, b: string | THREE.Color, t: number) => (typeof a === "string" ? C(a) : a.clone()).lerp(typeof b === "string" ? C(b) : b, sat(t));

type V3 = [number, number, number];
// flat-shaded standard material
export const Mat: React.FC<{ c: string | THREE.Color; e?: string | THREE.Color; ei?: number; r?: number; m?: number; o?: number }> = ({ c, e = "#000000", ei = 0, r = 0.85, m = 0, o = 1 }) =>
  <meshStandardMaterial color={c} emissive={e} emissiveIntensity={ei} flatShading roughness={r} metalness={m} transparent={o < 1} opacity={o} />;
export const Box: React.FC<{ p: V3; s: V3; c: string | THREE.Color; rot?: V3; e?: string; ei?: number; shadow?: boolean }> = ({ p, s, c, rot = [0, 0, 0], e, ei, shadow = true }) => (
  <mesh position={p} rotation={rot} castShadow={shadow} receiveShadow><boxGeometry args={s} /><Mat c={c} e={e} ei={ei} /></mesh>
);

// gable roof prism, ridge along z
const roofGeo = (w: number, h: number, d: number) => {
  const sh = new THREE.Shape(); sh.moveTo(-w / 2, 0); sh.lineTo(w / 2, 0); sh.lineTo(0, h); sh.closePath();
  const g = new THREE.ExtrudeGeometry(sh, { depth: d, bevelEnabled: false }); g.translate(0, 0, -d / 2); return g;
};

export const WIN_LIT = "#ffcf73";
const Window: React.FC<{ p: V3; ry: number; glow: number; trim: string; w?: number; h?: number }> = ({ p, ry, glow, trim, w = 0.42, h = 0.5 }) => (
  <group position={p} rotation={[0, ry, 0]}>
    <mesh castShadow><boxGeometry args={[w + 0.1, h + 0.1, 0.05]} /><Mat c={trim} /></mesh>
    <mesh position={[0, 0, 0.02]}><boxGeometry args={[w, h, 0.04]} /><Mat c={glow > 0.05 ? WIN_LIT : "#9cc2c8"} e={WIN_LIT} ei={glow * 2.6} r={0.3} /></mesh>
    <mesh position={[0, 0, 0.045]}><boxGeometry args={[0.035, h, 0.02]} /><Mat c={trim} /></mesh>
    <mesh position={[0, 0, 0.045]}><boxGeometry args={[w, 0.035, 0.02]} /><Mat c={trim} /></mesh>
  </group>
);

export type HouseSpec = { p: [number, number]; ry: number; w: number; d: number; floors: 1 | 2; wall: string; roof: string; trim: string; seed: number };
/** glow: 0..1 how lit the windows are (night / fire) */
export const House: React.FC<{ h: HouseSpec; glow: number }> = ({ h, glow }) => {
  const H = h.floors * 1.25, roofH = h.w * 0.42;
  const roof = useMemo(() => roofGeo(h.w + 0.5, roofH, h.d + 0.5), [h.w, h.d, roofH]);
  const wins: { p: V3; ry: number }[] = [];
  const nf = Math.max(1, Math.floor(h.w / 0.95));
  for (let f = 0; f < h.floors; f++) for (let i = 0; i < nf; i++) {
    const x = -h.w / 2 + (i + 0.5) * h.w / nf;
    if (f === 0 && Math.abs(x - h.w * 0.18) < 0.45) continue; // door
    wins.push({ p: [x, 0.72 + f * 1.25, h.d / 2 + 0.02], ry: 0 });
  }
  for (let f = 0; f < h.floors; f++) for (const s of [-1, 1]) wins.push({ p: [s * (h.w / 2 + 0.02), 0.72 + f * 1.25, 0], ry: s * Math.PI / 2 });
  return (
    <group position={[h.p[0], 0, h.p[1]]} rotation={[0, h.ry, 0]}>
      <Box p={[0, 0.06, 0]} s={[h.w + 0.3, 0.12, h.d + 0.3]} c="#b9a58a" />
      <Box p={[0, H / 2 + 0.1, 0]} s={[h.w, H, h.d]} c={h.wall} />
      {h.floors === 2 && <Box p={[0, 1.36, 0]} s={[h.w + 0.06, 0.1, h.d + 0.06]} c={h.trim} />}
      <mesh geometry={roof} position={[0, H + 0.1, 0]} castShadow receiveShadow><Mat c={h.roof} /></mesh>
      <Box p={[h.w * 0.22, H + 0.1 + roofH * 0.55, -h.d * 0.15]} s={[0.32, roofH * 0.9, 0.32]} c="#c98a4a" />
      <Box p={[h.w * 0.22, H + 0.1 + roofH * 1.02, -h.d * 0.15]} s={[0.4, 0.08, 0.4]} c="#7a4a3a" />
      {/* door with frame and step */}
      <Box p={[h.w * 0.18, 0.58, h.d / 2 + 0.03]} s={[0.56, 1.0, 0.05]} c={h.trim} />
      <Box p={[h.w * 0.18, 0.56, h.d / 2 + 0.06]} s={[0.42, 0.9, 0.04]} c="#8fae8a" />
      <Box p={[h.w * 0.18, 0.08, h.d / 2 + 0.28]} s={[0.7, 0.12, 0.35]} c="#a89a8a" />
      {/* round attic window on the gable */}
      <mesh position={[0, H + 0.1 + roofH * 0.38, h.d / 2 + 0.26]}><torusGeometry args={[0.2, 0.04, 6, 14]} /><Mat c={h.trim} /></mesh>
      <mesh position={[0, H + 0.1 + roofH * 0.38, h.d / 2 + 0.25]}><circleGeometry args={[0.18, 12]} /><Mat c={glow > 0.05 ? WIN_LIT : "#9cc2c8"} e={WIN_LIT} ei={glow * 2} /></mesh>
      {wins.map((w, i) => <Window key={i} p={w.p} ry={w.ry} trim={h.trim} glow={glow * (rnd(h.seed, i) > 0.35 ? 1 : 0.15)} />)}
    </group>
  );
};

export const Apartment: React.FC<{ p: [number, number]; w: number; d: number; floors: number; glow: number }> = ({ p, w, d, floors, glow }) => {
  const H = floors * 1.0;
  return (
    <group position={[p[0], 0, p[1]]}>
      <Box p={[0, H / 2, 0]} s={[w, H, d]} c="#d9733f" />
      <Box p={[0, H + 0.08, 0]} s={[w + 0.2, 0.16, d + 0.2]} c="#a8452a" />
      {Array.from({ length: floors - 1 }, (_, f) => (
        <group key={f}>
          <Box p={[0, 1.0 + f, d / 2 + 0.05]} s={[w + 0.04, 0.12, 0.12]} c="#a8452a" />
          <Box p={[0, 1.45 + f, d / 2 + 0.03]} s={[w * 0.86, 0.5, 0.05]} c={glow > 0.05 ? mixC("#c8d0a0", WIN_LIT, glow) : "#c8d0a0"} e={WIN_LIT} ei={glow * (rnd(f, 3) > 0.4 ? 2.2 : 0.3)} />
        </group>
      ))}
      <Box p={[0, 0.5, d / 2 + 0.6]} s={[w * 0.5, 0.08, 1.2]} c="#e0c8a0" />
      {[-1, 1].map(s => <Box key={s} p={[s * w * 0.22, 0.25, d / 2 + 1.1]} s={[0.1, 0.5, 0.1]} c="#e0c8a0" />)}
    </group>
  );
};

/** burn 0..1 chars the crown; fire flames are drawn separately */
export const Tree: React.FC<{ p: [number, number]; s: number; seed: number; sway: number; burn?: number; tone?: string }> = ({ p, s, seed, sway, burn = 0, tone = "#c4c43c" }) => {
  const crown = mixC(mixC(tone, "#d9a03a", burn * 1.6), "#2a2220", (burn - 0.4) / 0.5), k = 1 - sat((burn - 0.5) * 1.6) * 0.45;
  const lean = Math.sin(sway + seed) * 0.03;
  return (
    <group position={[p[0], 0, p[1]]} scale={s} rotation={[lean, rnd(seed, 1) * 6, lean * 0.6]}>
      <mesh position={[0, 0.55, 0]} castShadow><cylinderGeometry args={[0.07, 0.11, 1.1, 5]} /><Mat c={mixC("#b2462a", "#2a1a14", burn)} /></mesh>
      <mesh position={[0.18, 0.95, 0]} rotation={[0, 0, -0.7]} castShadow><cylinderGeometry args={[0.035, 0.05, 0.45, 4]} /><Mat c={mixC("#b2462a", "#2a1a14", burn)} /></mesh>
      <mesh position={[0, 1.45, 0]} scale={[k, k * 1.15, k]} castShadow><icosahedronGeometry args={[0.55, 0]} /><Mat c={crown} /></mesh>
      <mesh position={[0.32, 1.1, 0.05]} scale={k} castShadow><icosahedronGeometry args={[0.28, 0]} /><Mat c={mixC(crown, "#000000", 0.08)} /></mesh>
    </group>
  );
};

export const Car: React.FC<{ p: V3; ry: number; c: string; rust?: number; lights?: number }> = ({ p, ry, c, rust = 0, lights = 0 }) => {
  const body = mixC(c, "#8a4a26", rust * 0.85);
  return (
    <group position={p} rotation={[0, ry, 0]}>
      <Box p={[0, 0.3, 0]} s={[1.5, 0.34, 0.72]} c={body} />
      <Box p={[-0.08, 0.6, 0]} s={[0.85, 0.3, 0.64]} c={body} />
      <Box p={[-0.08, 0.6, 0]} s={[0.87, 0.22, 0.6]} c={mixC("#7fb8a8", "#5a4a3a", rust * 0.6)} />
      {rust > 0.2 && [0, 1, 2].map(i => <Box key={i} p={[-0.5 + i * 0.45, 0.3 + rnd(i, 4) * 0.08, 0.365]} s={[0.22 * rust, 0.12 * rust, 0.01]} c="#5a2a14" shadow={false} />)}
      {[-0.48, 0.48].map(x => [-0.37, 0.37].map(z => <mesh key={`${x}${z}`} position={[x, 0.15, z]} rotation={[Math.PI / 2, 0, 0]} castShadow><cylinderGeometry args={[0.15, 0.15, 0.1, 8]} /><Mat c="#2a2a30" /></mesh>))}
      {[-0.22, 0.22].map(z => <mesh key={z} position={[0.76, 0.32, z]}><boxGeometry args={[0.02, 0.08, 0.12]} /><Mat c="#fff4d0" e="#fff0c0" ei={0.4 + lights * 3} /></mesh>)}
    </group>
  );
};

export const Lamp: React.FC<{ p: [number, number]; on: number; rust?: number }> = ({ p, on, rust = 0 }) => (
  <group position={[p[0], 0, p[1]]}>
    <mesh position={[0, 0.9, 0]} castShadow><cylinderGeometry args={[0.04, 0.05, 1.8, 6]} /><Mat c={mixC("#2a2a34", "#7a3a1a", rust)} r={0.6} /></mesh>
    <Box p={[0, 1.85, 0]} s={[0.22, 0.18, 0.22]} c={mixC("#2a2a34", "#7a3a1a", rust)} />
    <mesh position={[0, 1.76, 0]}><boxGeometry args={[0.15, 0.08, 0.15]} /><Mat c="#fff0c0" e="#ffd27a" ei={on * 4} /></mesh>
  </group>
);

export const Bench: React.FC<{ p: [number, number]; ry: number }> = ({ p, ry }) => (
  <group position={[p[0], 0, p[1]]} rotation={[0, ry, 0]}>
    <Box p={[0, 0.3, 0]} s={[1.0, 0.07, 0.34]} c="#a0522d" />
    <Box p={[0, 0.52, -0.15]} s={[1.0, 0.25, 0.05]} c="#a0522d" />
    {[-0.42, 0.42].map(x => <Box key={x} p={[x, 0.15, 0]} s={[0.07, 0.3, 0.3]} c="#3a3a40" />)}
  </group>
);

export const Bin: React.FC<{ p: [number, number] }> = ({ p }) => (
  <mesh position={[p[0], 0.22, p[1]]} castShadow><cylinderGeometry args={[0.14, 0.12, 0.44, 7]} /><Mat c="#5a5a50" /></mesh>
);

export const Person: React.FC<{ p: V3; ry: number; shirt: string; run: number; f: number; pants?: string }> = ({ p, ry, shirt, run, f, pants = "#33334a" }) => {
  const sw = Math.sin(f * 0.55) * 0.9 * run;
  return (
    <group position={p} rotation={[0, ry, 0]}>
      {[-1, 1].map(s => <group key={s} position={[0, 0.42, s * 0.07]} rotation={[0, 0, s * sw]}><Box p={[0, -0.2, 0]} s={[0.1, 0.42, 0.1]} c={pants} /></group>)}
      <Box p={[0, 0.62, 0]} s={[0.2, 0.36, 0.3]} c={shirt} />
      {[-1, 1].map(s => <group key={s} position={[0, 0.78, s * 0.19]} rotation={[0, 0, -s * sw * 0.8]}><Box p={[0, -0.16, 0]} s={[0.08, 0.32, 0.08]} c={shirt} /></group>)}
      <mesh position={[0, 0.94, 0]} castShadow><icosahedronGeometry args={[0.13, 1]} /><Mat c="#e8b088" /></mesh>
      <mesh position={[-0.04, 1.0, 0]} castShadow><icosahedronGeometry args={[0.13, 0]} /><Mat c="#3a2418" /></mesh>
      {[-1, 1].map(z => <mesh key={z} position={[0.115, 0.96, z * 0.05]}><boxGeometry args={[0.03, 0.04, 0.03]} /><Mat c="#1a1420" /></mesh>)}
      <mesh position={[0.13, 0.91, 0]}><boxGeometry args={[0.03, 0.04, 0.035]} /><Mat c="#d8987a" /></mesh>
    </group>
  );
};

// floating diorama: grass slab, red soil layer, purple rock that tapers to a point
export const Island: React.FC<{ size: number; grass: string }> = ({ size, grass }) => {
  const rock = useMemo(() => { const g = new THREE.CylinderGeometry(size * 0.68, size * 0.12, size * 0.5, 4, 3); g.rotateY(Math.PI / 4); const p = g.attributes.position; for (let i = 0; i < p.count; i++) { const y = p.getY(i); if (y < size * 0.24) { p.setX(i, p.getX(i) * (0.9 + rnd(i, 2) * 0.2)); p.setZ(i, p.getZ(i) * (0.9 + rnd(i, 3) * 0.2)); } } g.computeVertexNormals(); return g; }, [size]);
  return (
    <group>
      <Box p={[0, -0.15, 0]} s={[size, 0.3, size]} c={grass} />
      <Box p={[0, -0.95, 0]} s={[size - 0.02, 1.3, size - 0.02]} c="#c4553a" />
      <Box p={[0, -1.72, 0]} s={[size - 0.3, 0.25, size - 0.3]} c="#8a3a2e" />
      <mesh geometry={rock} position={[0, -1.85 - size * 0.25, 0]} castShadow receiveShadow><Mat c="#6a4a7a" /></mesh>
    </group>
  );
};

export const Crystals: React.FC<{ p: V3; s: number; f: number; seed: number }> = ({ p, s, f, seed }) => (
  <group position={[p[0], p[1] + Math.sin(f * 0.03 + seed) * 0.25, p[2]]} scale={s} rotation={[0, f * 0.004 + seed, 0]}>
    {[0, 1, 2].map(i => <mesh key={i} position={[(rnd(seed, i) - 0.5) * 1.4, (rnd(seed, i + 5) - 0.5) * 0.8, (rnd(seed, i + 9) - 0.5) * 1.4]} scale={0.6 + rnd(seed, i + 3) * 0.6}><icosahedronGeometry args={[0.6, 0]} /><Mat c="#e8a8c8" /></mesh>)}
  </group>
);
