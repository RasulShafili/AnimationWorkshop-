// "What if the Sun became a black hole?" — low-poly space scene, not to scale.
// Units: Sun radius 1.2 at the origin, Earth radius 0.5 on an orbit of radius 6.
import React, { useMemo } from "react";
import * as THREE from "three";
import { useThree } from "@react-three/fiber";
import T from "./timeline.json";
import { Town } from "./Town";

export const sat = (v: number) => Math.min(1, Math.max(0, v));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const ease = (t: number) => { t = sat(t); return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
const easeIn = (t: number) => Math.pow(sat(t), 3);
const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };
const B = T.beats;
export const ORBIT = 6;
export const LIGHT_OFF = Math.round(T.shellStart + (T.shellEnd - T.shellStart) * ORBIT / 6.6);
export const shellR = (f: number) => 6.6 * (f - T.shellStart) / (T.shellEnd - T.shellStart);
export const earthAngle = (f: number) => -Math.PI / 2 + (f - 75) * 0.003;
export const earthPos = (f: number): THREE.Vector3 => { const a = earthAngle(f); return new THREE.Vector3(Math.cos(a) * ORBIT, 0, -Math.sin(a) * ORBIT); };
export const freezeAt = (f: number) => (f >= B[6] ? 1 : 0);

// ---------- radial glow texture shared by the sun, the photon ring halo and the light shell ----------
export const glowTex = (() => {
  let tex: THREE.CanvasTexture | null = null;
  return () => {
    if (tex) return tex;
    const c = document.createElement("canvas"); c.width = c.height = 128;
    const g = c.getContext("2d")!, gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
    gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(0.25, "rgba(255,255,255,0.55)"); gr.addColorStop(1, "rgba(255,255,255,0)");
    g.fillStyle = gr; g.fillRect(0, 0, 128, 128);
    tex = new THREE.CanvasTexture(c); return tex;
  };
})();
export const Glow: React.FC<{ size: number; color: string; opacity: number; pos?: THREE.Vector3 | [number, number, number] }> = ({ size, color, opacity, pos = [0, 0, 0] }) => (
  <sprite position={pos as any} scale={[size, size, 1]}>
    <spriteMaterial map={glowTex()} color={color} transparent opacity={opacity} blending={THREE.AdditiveBlending} depthWrite={false} />
  </sprite>
);

export const Stars: React.FC<{ f: number }> = ({ f }) => {
  const geo = useMemo(() => {
    const n = 1400, p = new Float32Array(n * 3), c = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) {
      const u = rnd(i, 1) * 2 - 1, th = rnd(i, 2) * Math.PI * 2, r = 80, s = Math.sqrt(1 - u * u);
      p.set([Math.cos(th) * s * r, u * r, Math.sin(th) * s * r], i * 3);
      const w = 0.5 + rnd(i, 3) * 0.5, tint = rnd(i, 4);
      c.set(tint < 0.2 ? [w, w * 0.8, w * 0.6] : tint > 0.85 ? [w * 0.7, w * 0.85, w] : [w, w, w], i * 3);
    }
    const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.BufferAttribute(p, 3)); g.setAttribute("color", new THREE.BufferAttribute(c, 3)); return g;
  }, []);
  return <points geometry={geo} rotation={[0, f * 0.0004, 0]}><pointsMaterial size={1.6} sizeAttenuation={false} vertexColors transparent opacity={0.95} /></points>;
};

// ---------- the Sun: boiling low-poly ball that implodes ----------
const Sun: React.FC<{ f: number }> = ({ f }) => {
  const geo = useMemo(() => new THREE.IcosahedronGeometry(1.2, 2), []);
  const base = useMemo(() => Float32Array.from(geo.attributes.position.array as Float32Array), [geo]);
  const k = 1 - easeIn((f - 16) / (T.collapse - 16));
  if (k <= 0.001) return null;
  const pos = geo.attributes.position as THREE.BufferAttribute;
  for (let i = 0; i < pos.count; i++) {
    const x = base[i * 3], y = base[i * 3 + 1], z = base[i * 3 + 2];
    const n = 1 + 0.06 * Math.sin(x * 3.1 + f * 0.31) * Math.sin(y * 2.7 - f * 0.23) * Math.sin(z * 3.3 + f * 0.17) + (f > 16 ? 0.05 * Math.sin(f * 1.7 + i) : 0);
    pos.setXYZ(i, x * n, y * n, z * n);
  }
  pos.needsUpdate = true; geo.computeVertexNormals();
  const hot = sat((f - 16) / 18);
  return (
    <group scale={k}>
      <mesh geometry={geo}><meshBasicMaterial color={new THREE.Color("#ff7a12").lerp(new THREE.Color("#ffe8a0"), hot)} /></mesh>
      <mesh scale={0.985} rotation={[f * 0.01, f * 0.013, 0]}><icosahedronGeometry args={[1.2, 1]} /><meshBasicMaterial color="#ffd060" wireframe transparent opacity={0.35} /></mesh>
      <Glow size={4.6} color="#ff7a10" opacity={0.5} />
    </group>
  );
};

// ---------- the black hole: black ball, bright photon ring facing the camera, faint halo ----------
const BlackHole: React.FC<{ f: number; cam: THREE.Vector3 }> = ({ f, cam }) => {
  const born = sat((f - T.collapse) / 10);
  if (born <= 0) return null;
  const q = new THREE.Quaternion().setFromRotationMatrix(new THREE.Matrix4().lookAt(cam, new THREE.Vector3(), new THREE.Vector3(0, 1, 0)));
  const pulse = 1 + 0.06 * Math.sin(f * 0.25);
  return (
    <group scale={born}>
      <Glow size={2.2 * pulse} color="#ff7a3a" opacity={0.45} />
      <group quaternion={q}>
        <mesh><torusGeometry args={[0.3, 0.03, 6, 40]} /><meshBasicMaterial color="#ffe0a0" /></mesh>
        <mesh rotation={[0, 0, f * 0.02]}><ringGeometry args={[0.33, 0.55, 40, 1]} /><meshBasicMaterial color="#ff8a3a" transparent opacity={0.25} side={THREE.DoubleSide} blending={THREE.AdditiveBlending} depthWrite={false} /></mesh>
      </group>
      <mesh><sphereGeometry args={[0.24, 20, 14]} /><meshBasicMaterial color="#000000" /></mesh>
    </group>
  );
};

// ---------- Earth: faceted globe whose oceans ice over ----------
const fbm = (x: number, y: number, z: number) => {
  let s = 0, a = 0.5, fr = 1.6;
  for (let o = 0; o < 4; o++) { s += a * (Math.sin(x * fr + 1.3 * o) * Math.sin(y * fr * 1.1 + 2.1 * o) * Math.sin(z * fr * 0.9 + 0.7 * o) * 0.5 + 0.5); fr *= 2.1; a *= 0.5; }
  return s;
};
const Earth: React.FC<{ f: number }> = ({ f }) => {
  const { geo, faces } = useMemo(() => {
    const g = new THREE.IcosahedronGeometry(0.5, 4); // non-indexed: one colour per face
    const p = g.attributes.position.array as Float32Array, n = p.length / 9, faces: { land: number; lat: number; n: number }[] = [];
    for (let i = 0; i < n; i++) {
      const cx = (p[i * 9] + p[i * 9 + 3] + p[i * 9 + 6]) / 3, cy = (p[i * 9 + 1] + p[i * 9 + 4] + p[i * 9 + 7]) / 3, cz = (p[i * 9 + 2] + p[i * 9 + 5] + p[i * 9 + 8]) / 3;
      const l = Math.hypot(cx, cy, cz);
      faces.push({ land: fbm(cx / l * 2.2, cy / l * 2.2, cz / l * 2.2), lat: Math.abs(cy / l), n: rnd(i, 9) });
    }
    g.setAttribute("color", new THREE.BufferAttribute(new Float32Array(p.length), 3));
    return { geo: g, faces };
  }, []);
  const fr = freezeAt(f), col = geo.attributes.color as THREE.BufferAttribute;
  const ocean = new THREE.Color("#2a72e0"), deep = new THREE.Color("#1c52b8"), land = new THREE.Color("#3f9a4a"), dry = new THREE.Color("#b8a060"), ice = new THREE.Color("#e8f6ff"), snow = new THREE.Color("#ffffff");
  faces.forEach((fc, i) => {
    const isLand = fc.land > 0.56;
    let c = isLand ? land.clone().lerp(dry, sat((fc.land - 0.62) * 6)) : ocean.clone().lerp(deep, fc.n * 0.5);
    if (fc.lat > 0.88) c = snow.clone();
    // ice creeps from the poles to the equator as the planet cools
    const line = 0.88 - fr * 1.05 + (fc.n - 0.5) * 0.12;
    if (fc.lat > line) c = (isLand ? snow : ice).clone().lerp(new THREE.Color("#bcd8f0"), fc.n * 0.3);
    for (let k = 0; k < 3; k++) col.setXYZ(i * 3 + k, c.r, c.g, c.b);
  });
  col.needsUpdate = true;
  const cities = useMemo(() => {
    const pts: number[] = [];
    for (let i = 0; pts.length < 260 * 3 && i < 9000; i++) {
      const u = rnd(i, 21) * 2 - 1, th = rnd(i, 22) * Math.PI * 2, s = Math.sqrt(1 - u * u), x = Math.cos(th) * s, y = u * 0.9, z = Math.sin(th) * s;
      if (fbm(x * 2.2, y * 2.2, z * 2.2) > 0.6 && Math.abs(y) < 0.7) pts.push(x * 0.508, y * 0.508, z * 0.508);
    }
    const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.BufferAttribute(new Float32Array(pts), 3)); return g;
  }, []);
  const p = earthPos(f), dark = f >= LIGHT_OFF;
  return (
    <group position={p} scale={f < B[6] ? 1.6 : 1}>
      <group rotation={[0.41, f * 0.012, 0]}>
        <mesh geometry={geo}><meshStandardMaterial vertexColors flatShading roughness={0.85} metalness={0} /></mesh>
        {dark && <points geometry={cities}><pointsMaterial color="#ffcf6a" size={1.4} sizeAttenuation={false} transparent opacity={0.9 * (1 - fr * 0.6)} /></points>}
      </group>
      <mesh scale={1.07}><sphereGeometry args={[0.5, 24, 16]} /><meshBasicMaterial color="#6ac8ff" transparent opacity={0.1 * (1 - fr)} side={THREE.BackSide} /></mesh>
    </group>
  );
};

const OrbitDots: React.FC<{ opacity: number }> = ({ opacity }) => {
  const geo = useMemo(() => {
    const n = 140, p = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) { const a = i / n * Math.PI * 2; p.set([Math.cos(a) * ORBIT, 0, Math.sin(a) * ORBIT], i * 3); }
    const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.BufferAttribute(p, 3)); return g;
  }, []);
  if (opacity <= 0.01) return null;
  return <points geometry={geo}><pointsMaterial color="#7ad8ff" size={1.4} sizeAttenuation={false} transparent opacity={opacity} /></points>;
};

// the last sunlight, still travelling outward as an expanding ring
const LightShell: React.FC<{ f: number }> = ({ f }) => {
  const R = shellR(f);
  if (f < T.shellStart || R > 9) return null;
  return (
    <group rotation={[-Math.PI / 2, 0, 0]}>
      <mesh><torusGeometry args={[Math.max(0.01, R), 0.04, 6, 120]} /><meshBasicMaterial color="#fff2a0" /></mesh>
      <mesh><ringGeometry args={[Math.max(0, R - 0.9), Math.max(0.01, R), 120, 1]} /><meshBasicMaterial color="#ffc860" transparent opacity={0.18} side={THREE.DoubleSide} blending={THREE.AdditiveBlending} depthWrite={false} /></mesh>
    </group>
  );
};

// ---------- camera path ----------
type Shot = { pos: THREE.Vector3; look: THREE.Vector3; up: THREE.Vector3; fov: number };
const V = (x: number, y: number, z: number) => new THREE.Vector3(x, y, z);
const Y = V(0, 1, 0);
const shotAt = (f: number): Shot => {
  const e = earthPos(f), toHole = e.clone().multiplyScalar(-1).normalize();
  const s0: Shot = { pos: V(0.4, 0.3, lerp(6.2, 4.6, sat(f / T.collapse))), look: V(0, 0, 0), up: Y, fov: 46 };
  // top-down: the hole at the top of the frame, Earth at the bottom, the orbit as a big arc
  const mid = e.clone().multiplyScalar(0.45);
  const s1: Shot = { pos: mid.clone().add(V(0, 12.5, 0)).addScaledVector(toHole, -2.2), look: mid, up: toHole, fov: 58 };
  const s2: Shot = { pos: mid.clone().add(V(0, 10.5 - (f - B[2]) * 0.006, 0)).addScaledVector(toHole, -1.6), look: mid, up: toHole, fov: 56 };
  const s3: Shot = { pos: e.clone().add(V(-1.0 + (f - B[6]) * 0.004, 0.7, 2.1)), look: e.clone(), up: Y, fov: 46 };
  const k = (f - 920) / 70;
  const s4: Shot = { pos: V(lerp(1.4, 0.05, ease(k)), lerp(0.8, 0.03, ease(k)), lerp(3.2, 0.42, easeIn(k))), look: V(0, 0, 0), up: Y, fov: 46 };
  const mixS = (a: Shot, b: Shot, t: number): Shot => ({ pos: a.pos.clone().lerp(b.pos, ease(t)), look: a.look.clone().lerp(b.look, ease(t)), up: a.up.clone().lerp(b.up, ease(t)).normalize(), fov: lerp(a.fov, b.fov, ease(t)) });
  if (f < B[1] - 20) return s0;
  if (f < B[1] + 30) return mixS(s0, s1, (f - (B[1] - 20)) / 50);
  if (f < B[2]) return s1;
  if (f < B[2] + 22) return mixS(s1, s2, (f - B[2]) / 22);
  if (f < B[6]) return s2;
  if (f < 868) return s3;
  if (f < 904) return mixS(s3, s4, (f - 868) / 36);
  return s4;
};

export const Scene: React.FC<{ f: number }> = ({ f }) => {
  const { camera } = useThree();
  if (f >= B[3] && f < B[6]) return <Town f={f} />;
  const sh = shotAt(f);
  const quake = f >= T.collapse && f < T.collapse + 14 ? (1 - (f - T.collapse) / 14) * 0.12 : f < T.collapse && f > 16 ? 0.02 : 0;
  camera.position.set(sh.pos.x + Math.sin(f * 2.3) * quake, sh.pos.y + Math.cos(f * 1.9) * quake, sh.pos.z);
  camera.up.copy(sh.up); camera.lookAt(sh.look);
  const pc = camera as THREE.PerspectiveCamera; pc.near = 0.01; pc.far = 400; pc.fov = sh.fov; pc.updateProjectionMatrix();
  const sunOn = f < LIGHT_OFF ? 1 : 0;
  const coldLight = f >= LIGHT_OFF ? 0.55 : 0;
  return (
    <>
      <color attach="background" args={["#02030a"]} />
      <Stars f={f} />
      <ambientLight intensity={0.06 + coldLight * 0.2} color="#8aa8ff" />
      <pointLight position={[0, 0, 0]} intensity={sunOn * 4.2} decay={0} distance={0} color="#fff0d8" />
      <directionalLight position={[camera.position.x + 2, camera.position.y + 3, camera.position.z + 2]} intensity={coldLight} color="#9ab8ff" />
      <Sun f={f} />
      <BlackHole f={f} cam={camera.position.clone()} />
      <OrbitDots opacity={sat((f - B[1]) / 20) * (1 - sat((f - B[3] + 15) / 15)) * 0.7} />
      <LightShell f={f} />
      <Earth f={f} />
    </>
  );
};
