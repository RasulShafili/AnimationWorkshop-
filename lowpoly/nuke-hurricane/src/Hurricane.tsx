// A hurricane over the ocean: ~3000 low-poly cloud puffs in a log-spiral with a clear eye and a towering eyewall,
// rotating counter-clockwise (northern hemisphere). Coast + city to the east (+x). Optional nuke and green fallout.
import React, { useEffect, useMemo, useRef } from "react";
import { useThree } from "@react-three/fiber";
import * as THREE from "three";
import { Glow, sat } from "./Scenes";

const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };
export const SPIN = 0.0045;   // rad per frame
const N = 3000;
const EYE = 6.5;
const puffs = (() => Array.from({ length: N }, (_, i) => {
  if (i < 800) { // eyewall: a stadium from the sea up to the top
    const r = EYE + Math.pow(rnd(i, 1), 1.5) * 3.2, a = rnd(i, 2) * 6.283, y = rnd(i, 3) * 13 * (1 - (r - EYE) / 6);
    return { r: r + y * 0.12, a, y, s: 1.1 + rnd(i, 4) * 0.9 };
  }
  if (i < 2800) { // four spiral bands
    const arm = i % 4, r = EYE + 3 + Math.pow(rnd(i, 1), 0.9) * 46;
    const a = arm * Math.PI / 2 - 1.25 * Math.log(r / EYE) + (rnd(i, 2) - 0.5) * (0.4 + r / 90);
    return { r, a, y: 3 + rnd(i, 3) * 5 * (1 - r / 60), s: 0.9 + rnd(i, 4) * 1.6 * (1.15 - r / 60) };
  }
  const r = EYE + 4 + rnd(i, 1) * 40, a = rnd(i, 2) * 6.283; // a few loose puffs between the bands
  return { r, a, y: 2.4 + rnd(i, 3) * 1.2, s: 0.7 + rnd(i, 4) * 0.8 };
}))();

export const Storm: React.FC<{ f: number; push?: number; dim?: number }> = ({ f, push = 0, dim = 0 }) => {
  // built imperatively and updated during render: Remotion captures before useEffect would run
  const m = useMemo(() => { const im = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(1, 1), new THREE.MeshStandardMaterial({ flatShading: true, roughness: 1 }), N); im.castShadow = true; im.frustumCulled = false; return im; }, []);
  {
    const o = new THREE.Object3D(), c = new THREE.Color();
    puffs.forEach((p, i) => {
      const r = p.r * (1 + push * Math.exp(-p.r / 8) * 0.6);
      o.position.set(Math.cos(p.a) * r, p.y, Math.sin(p.a) * r); o.scale.set(p.s * 1.25, p.s * 0.8, p.s * 1.25); o.rotation.set(rnd(i, 5) * 3, rnd(i, 6) * 3, 0); o.updateMatrix(); m.setMatrixAt(i, o.matrix);
      const k = 0.6 + p.y * 0.03 + rnd(i, 7) * 0.12 - dim * 0.3; c.setRGB(k * 0.97, k, k * 1.04); m.setColorAt(i, c);
    });
    m.instanceMatrix.needsUpdate = true; m.instanceColor!.needsUpdate = true;
  }
  return <group rotation={[0, f * SPIN, 0]}><primitive object={m} /></group>;
};

export const Ocean: React.FC<{ tint?: string }> = ({ tint = "#1d3d5e" }) => {
  const geo = useMemo(() => { const g = new THREE.PlaneGeometry(900, 900, 140, 140); const p = g.attributes.position; for (let i = 0; i < p.count; i++) p.setZ(i, (rnd(i, 1) - 0.5) * 0.5); g.computeVertexNormals(); return g; }, []);
  return <mesh geometry={geo} rotation={[-Math.PI / 2, 0, 0]} receiveShadow><meshStandardMaterial color={tint} flatShading roughness={0.5} metalness={0.1} /></mesh>;
};

export const Coast: React.FC<{ lit?: number }> = ({ lit = 0.4 }) => {
  const m = useMemo(() => {
    const im = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshStandardMaterial({ flatShading: true, roughness: 0.7 }), 260); im.castShadow = true; im.frustumCulled = false;
    const o = new THREE.Object3D(), c = new THREE.Color(), m = im;
    for (let i = 0; i < 260; i++) { const x = 64 + rnd(i, 1) * 26, z = (rnd(i, 2) - 0.5) * 70, h = 0.6 + Math.pow(rnd(i, 3), 3) * 7 * (1 - Math.abs(z) / 45);
      o.position.set(x, h / 2 + 0.3, z); o.scale.set(1 + rnd(i, 4) * 1.4, Math.max(0.4, h), 1 + rnd(i, 5) * 1.4); o.updateMatrix(); m.setMatrixAt(i, o.matrix);
      c.set(rnd(i, 6) > 0.5 ? "#c8ccd4" : "#9aa2b0"); m.setColorAt(i, c); }
    return im;
  }, []);
  return <group>
    <mesh position={[230, 0.15, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow><planeGeometry args={[340, 900]} /><meshStandardMaterial color="#5a7a4a" flatShading /></mesh>
    <mesh position={[61, 0.12, 0]} rotation={[-Math.PI / 2, 0, 0]}><planeGeometry args={[3, 900]} /><meshStandardMaterial color="#e0d0a0" /></mesh>
    <primitive object={m} />
    {Array.from({ length: 40 }, (_, i) => <mesh key={i} position={[64 + rnd(i, 8) * 26, 0.5 + rnd(i, 9) * 3, (rnd(i, 10) - 0.5) * 60]}><boxGeometry args={[0.3, 0.3, 0.3]} /><meshBasicMaterial color={new THREE.Color(2.2, 1.8, 1.0).multiplyScalar(lit)} toneMapped={false} /></mesh>)}
  </group>;
};

// the nuke at the centre of the eye: fireball, mushroom stem + cap, shock ring on the water, condensation dome
export const Nuke: React.FC<{ t: number }> = ({ t }) => {
  if (t < 0) return null;
  const fire = sat(t / 40), R = 0.6 + Math.pow(fire, 0.5) * 2.8, rise = Math.min(13, t * 0.16), fade = sat(1 - (t - 140) / 120);
  return <group>
    <mesh position={[0, R * 0.6 + rise * 0.6, 0]} scale={[R * (1 + rise * 0.05), R * 0.75, R * (1 + rise * 0.05)]}><icosahedronGeometry args={[1, 2]} /><meshBasicMaterial color={new THREE.Color(4, 2.4, 0.9).lerp(new THREE.Color(0.9, 0.35, 0.2), fire)} toneMapped={false} transparent opacity={fade} /></mesh>
    {t > 10 && <mesh position={[0, rise * 0.3, 0]}><cylinderGeometry args={[0.5, 1.1, Math.max(0.1, rise * 0.6), 12]} /><meshStandardMaterial color="#b89a88" emissive="#ff6a2a" emissiveIntensity={sat(1 - t / 60) * 2} transparent opacity={fade} /></mesh>}
    {t < 50 && <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.2, 0]}><ringGeometry args={[Math.max(0.1, t * 0.3 - 0.8), t * 0.3, 64]} /><meshBasicMaterial color={new THREE.Color(3, 3, 3)} toneMapped={false} transparent opacity={sat(1 - t / 50)} side={THREE.DoubleSide} /></mesh>}
    {t < 30 && <mesh scale={t * 0.35}><sphereGeometry args={[1, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2]} /><meshStandardMaterial color="#ffffff" transparent opacity={0.35 * (1 - t / 30)} depthWrite={false} /></mesh>}
    <Glow size={20 * sat(1 - t / 40) + 4} color="#fff0c8" opacity={sat(1 - t / 60)} pos={[0, 2, 0]} />
    <pointLight position={[0, 3, 0]} intensity={900 * sat(1 - t / 50)} distance={120} decay={1.2} color="#ffd8a0" />
  </group>;
};

// green fallout: motes caught by the spiral winds, drifting out of the storm toward the coast (+x)
export const Fallout: React.FC<{ t: number }> = ({ t }) => {
  const n = 700;
  const geo = useMemo(() => { const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.BufferAttribute(new Float32Array(n * 3), 3)); return g; }, []);
  const p = geo.attributes.position as THREE.BufferAttribute;
  for (let i = 0; i < n; i++) {
    const tt = Math.max(0, t - rnd(i, 1) * 40), r0 = 0.5 + rnd(i, 2) * 3, r = r0 + tt * (0.06 + rnd(i, 3) * 0.1);
    const a = rnd(i, 4) * 6.283 + tt * 0.04 * (8 / (r + 4)) * 4, drift = Math.max(0, tt - 30) * 0.22;
    p.setXYZ(i, Math.cos(a) * r + drift, 1.5 + rnd(i, 5) * 7 - Math.max(0, tt - 80) * 0.02, Math.sin(a) * r);
  }
  p.needsUpdate = true;
  return <points geometry={geo}><pointsMaterial color={new THREE.Color(0.6, 2.4, 0.5)} size={0.55} toneMapped={false} transparent opacity={sat(t / 20)} blending={THREE.AdditiveBlending} depthWrite={false} /></points>;
};

export const SceneSky: React.FC<{ sky: string; near: number; far: number }> = ({ sky, near, far }) => {
  // background/fog must be set on the scene itself (attach inside a <group> lands on the group)
  const { scene } = useThree(); const c = new THREE.Color(sky);
  scene.background = c; scene.fog = new THREE.Fog(c, near, far); return null;
};
export const StormWorld: React.FC<{ f: number; nukeT?: number; falloutT?: number; push?: number; sky?: string }> = ({ f, nukeT = -1, falloutT = -1, push = 0, sky = "#8aa0b8" }) => (
  <group>
    <SceneSky sky={sky} near={140} far={520} />
    <Ocean />
    <Coast />
    <Storm f={f} push={push} />
    <Nuke t={nukeT} />
    {falloutT >= 0 && <group rotation={[0, f * SPIN * 0.3, 0]}><Fallout t={falloutT} /></group>}
    <hemisphereLight args={["#dfe8f4", "#2a3a4a", 0.9]} />
    <directionalLight position={[-60, 120, 40]} intensity={2.2} color="#fff4e4" castShadow shadow-mapSize={[2048, 2048]} shadow-camera-left={-60} shadow-camera-right={60} shadow-camera-top={60} shadow-camera-bottom={-60} shadow-camera-far={400} />
  </group>
);
