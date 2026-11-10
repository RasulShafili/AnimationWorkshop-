// A detailed low-poly man (metres, feet at y=0, facing +z) whose body responds to the hormone:
// muscle (1 → ~1.9), beard, acne, receding hairline, flushed skin, softer/larger chest, a tank top that rips.
import React, { useMemo } from "react";
import * as THREE from "three";

const sat = (v: number) => Math.min(1, Math.max(0, v));
const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
const C = (h: string) => new THREE.Color(h);
const mix = (a: string, b: string, t: number) => C(a).lerp(C(b), sat(t));
const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };
const S: React.FC<{ c: THREE.Color | string; r?: number; e?: string; ei?: number; side?: THREE.Side }> = ({ c, r = 0.75, e = "#000", ei = 0, side }) =>
  <meshStandardMaterial color={c} flatShading roughness={r} emissive={e} emissiveIntensity={ei} side={side} />;
const Cap: React.FC<{ a: THREE.Vector3; b: THREE.Vector3; r: number; c: THREE.Color | string; seg?: number }> = ({ a, b, r, c, seg = 7 }) => {
  const mid = a.clone().add(b).multiplyScalar(0.5), len = Math.max(0.001, a.distanceTo(b));
  const q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), b.clone().sub(a).normalize());
  return <mesh position={mid} quaternion={q} castShadow receiveShadow><capsuleGeometry args={[r, len, 3, seg]} /><S c={c} /></mesh>;
};
const V = (x: number, y: number, z: number) => new THREE.Vector3(x, y, z);

export type Look = {
  m: number;        // muscle factor 1..1.9
  beard: number; acne: number; hair: number; flush: number; chest: number; sweat: number;
  rip: number;      // frames since the shirt ripped (<0: intact)
  flex: number;     // 0 idle .. 1 double-biceps pose
  curl: number;     // dumbbell curl angle 0..1
  holding: boolean; // dumbbell in right hand
  lookDown: number; slump: number; brow: number;
  f: number;
};

// torso shape as a lathe: waist → chest → shoulders → neck base
const torsoGeo = (m: number, scale = 1) => {
  const w = 1 + (m - 1) * 0.55, pts = [
    [0.13, 0.92], [0.135, 1.0], [0.15 * w, 1.12], [0.175 * w, 1.24], [0.19 * w, 1.33], [0.185 * w, 1.41], [0.12 * w, 1.47], [0.06, 1.5],
  ].map(([r, y]) => new THREE.Vector2(r * scale, y));
  const g = new THREE.LatheGeometry(pts, 12); g.scale(1.25, 1, 0.78); return g;
};

export const Man: React.FC<{ L: Look }> = ({ L }) => {
  const { m, f } = L, w = 1 + (m - 1) * 0.55;
  const skin = mix(mix("#e2a27c", "#e88470", L.flush * 0.8).getStyle(), "#c8907a", 0).getStyle();
  const skinC = C(skin);
  const torso = useMemo(() => torsoGeo(m), [Math.round(m * 50)]);
  const shirt = useMemo(() => torsoGeo(m, 1.05), [Math.round(m * 50)]);
  const halfL = useMemo(() => { const g = new THREE.LatheGeometry(torsoGeoPts(1.32, 1.06), 12, 0, Math.PI); g.scale(1.25, 1, 0.78); return g; }, []);
  const halfR = useMemo(() => { const g = new THREE.LatheGeometry(torsoGeoPts(1.32, 1.06), 12, Math.PI, Math.PI); g.scale(1.25, 1, 0.78); return g; }, []);
  const breath = Math.sin(f * 0.12) * 0.006 * (1 + L.slump * 2);
  const slumpY = -L.slump * 0.06;

  // arms: shoulder angle (frontal plane, 0 = hanging), elbow angle (relative), curl (sagittal)
  const arm = (side: 1 | -1) => {
    const flex = L.flex;
    const aU = lerp(0.14 + L.slump * 0.05, 1.5, flex), aF = lerp(0.1, 1.95, flex);
    const curlX = side === 1 ? -L.curl * 2.2 * (1 - flex) : 0;
    const sh = V(side * 0.235 * w, 1.4 + slumpY, 0);
    const up = 0.28, fo = 0.26, rU = 0.048 * (1 + (m - 1) * 0.8), rF = 0.04 * (1 + (m - 1) * 0.6);
    const bic = 0.05 * Math.pow(m, 1.7) * (0.8 + flex * 0.5);
    return (
      <group position={sh} rotation={[side === 1 ? 0 : 0, 0, side * aU]}>
        <mesh position={[0, 0.0, 0]} castShadow><icosahedronGeometry args={[0.072 * (1 + (m - 1) * 0.7), 1]} /><S c={skinC} /></mesh>
        <mesh position={[0, -up / 2, 0]} castShadow><capsuleGeometry args={[rU, up - rU, 3, 7]} /><S c={skinC} /></mesh>
        <mesh position={[side * 0.0, -up * 0.55, 0.03]} scale={[1, 1.25, 1.1]} castShadow><icosahedronGeometry args={[bic, 1]} /><S c={skinC} /></mesh>
        <group position={[0, -up, 0]} rotation={[curlX, 0, side * aF]}>
          <mesh position={[0, -fo / 2, 0]} castShadow><capsuleGeometry args={[rF, fo - rF, 3, 7]} /><S c={skinC} /></mesh>
          <mesh position={[0, -fo - 0.03, 0]} castShadow><icosahedronGeometry args={[0.048, 1]} /><S c={skinC} /></mesh>
          {side === 1 && L.holding && (
            <group position={[0, -fo - 0.03, 0]} rotation={[Math.PI / 2, 0, 0]}>
              <mesh><cylinderGeometry args={[0.015, 0.015, 0.2, 6]} /><S c="#8a8a90" r={0.3} /></mesh>
              {[-1, 1].map(s => <mesh key={s} position={[0, s * 0.11, 0]} castShadow><cylinderGeometry args={[0.055, 0.055, 0.06, 8]} /><S c="#2a2a30" r={0.4} /></mesh>)}
            </group>
          )}
        </group>
      </group>
    );
  };

  // hair cap recedes: shorter and tilted back as `hair` grows
  const hairLen = lerp(1.25, 0.55, L.hair), hairTilt = lerp(-0.3, -1.0, L.hair);
  const acneSpots = useMemo(() => Array.from({ length: 12 }, (_, i) => { const th = (rnd(i, 1) - 0.5) * 1.9, ph = (rnd(i, 2) - 0.2) * 1.2; return V(Math.sin(th) * Math.cos(ph) * 0.112, Math.sin(ph) * 0.11 - 0.01, Math.cos(th) * Math.cos(ph) * 0.112); }).filter(p => p.z > 0.05 && Math.abs(p.x) > 0.03), []);
  const head = (
    <group position={[0, 1.67 + slumpY, 0.005 + L.slump * 0.04]} rotation={[L.lookDown * 0.55 + L.slump * 0.25, 0, 0]}>
      <mesh scale={[0.93, 1.06, 1]} castShadow><icosahedronGeometry args={[0.115, 2]} /><S c={skinC} /></mesh>
      {/* jaw widens with the hormone */}
      <mesh position={[0, -0.07, 0.015]} scale={[1 + (m - 1) * 0.35, 1, 1]} castShadow><boxGeometry args={[0.14, 0.07, 0.15]} /><S c={skinC} /></mesh>
      {[-1, 1].map(s => <mesh key={s} position={[s * 0.108, 0, -0.005]} scale={[0.5, 1, 0.8]}><icosahedronGeometry args={[0.03, 1]} /><S c={skinC} /></mesh>)}
      <mesh position={[0, -0.005, 0.118]} rotation={[Math.PI / 2 + 0.25, 0, 0]}><coneGeometry args={[0.018, 0.05, 5]} /><S c={mix(skin, "#c06050", 0.2)} /></mesh>
      {[-1, 1].map(s => (
        <group key={s} position={[s * 0.042, 0.022, 0.1]}>
          <mesh scale={[1, 0.72, 0.5]}><icosahedronGeometry args={[0.0145, 1]} /><S c="#ffffff" r={0.3} /></mesh>
          <mesh position={[0, -0.001, 0.006]}><icosahedronGeometry args={[0.0075, 1]} /><S c="#2a1a14" r={0.2} /></mesh>
          <mesh position={[0, 0.03, 0.006]} rotation={[0, 0, -s * L.brow * 0.35]}><boxGeometry args={[0.045, 0.011, 0.012]} /><S c="#3a2418" /></mesh>
        </group>
      ))}
      <mesh position={[0, -0.062, 0.112]} rotation={[0, 0, 0]} scale={[1, 1 + L.slump * 1.5, 1]}><boxGeometry args={[0.05, 0.009, 0.01]} /><S c="#8a3a34" /></mesh>
      {/* hair */}
      <mesh rotation={[hairTilt, 0, 0]} scale={[0.96, 1.08, 1.04]} castShadow><sphereGeometry args={[0.12, 14, 8, 0, Math.PI * 2, 0, hairLen]} /><S c="#3a2418" side={THREE.DoubleSide} /></mesh>
      {/* beard: stubble → full beard */}
      {L.beard > 0.03 && (
        <group>
          <mesh rotation={[0.05, 0, 0]} scale={[lerp(1.0, 1.12, L.beard), lerp(1.0, 1.1, L.beard), lerp(1.0, 1.16, L.beard)]}>
            <sphereGeometry args={[0.118, 14, 8, -Math.PI * 0.08, Math.PI * 1.16, Math.PI * 0.64, Math.PI * 0.3]} /><S c={mix(skin, "#5a3a26", 0.3 + L.beard * 0.6)} side={THREE.DoubleSide} r={0.95} />
          </mesh>
          <mesh position={[0, -0.08, 0.015]} scale={[1 + (m - 1) * 0.35, 1, 1]}><boxGeometry args={[0.146, 0.062 + L.beard * 0.012, 0.14]} /><S c={mix(skin, "#5a3a26", 0.3 + L.beard * 0.6)} r={0.95} /></mesh>
          <mesh position={[0, -0.042, 0.112]}><boxGeometry args={[0.07, 0.014 * L.beard + 0.002, 0.018]} /><S c="#3a2418" /></mesh>
        </group>
      )}
      {acneSpots.map((p, i) => L.acne > i / acneSpots.length && <mesh key={i} position={p}><icosahedronGeometry args={[0.0075, 0]} /><S c="#c8384a" r={0.4} /></mesh>)}
      {L.sweat > 0 && [0, 1, 2].map(i => { const u = ((f * 0.02 + i / 3) % 1); return <mesh key={i} position={[(i - 1) * 0.06, 0.07 - u * 0.12, 0.112]}><icosahedronGeometry args={[0.008, 0]} /><meshStandardMaterial color="#cfefff" roughness={0.05} metalness={0.2} transparent opacity={L.sweat} /></mesh>; })}
    </group>
  );

  const ripT = L.rip; // frames since rip
  return (
    <group position={[0, breath, 0]}>
      {/* legs + shoes */}
      {[-1, 1].map(s => (
        <group key={s}>
          <Cap a={V(s * 0.1, 0.92, 0)} b={V(s * 0.11, 0.5, 0.01)} r={0.075 * (1 + (m - 1) * 0.35)} c={skinC} />
          <Cap a={V(s * 0.11, 0.5, 0.01)} b={V(s * 0.11, 0.1, -0.01)} r={0.055 * (1 + (m - 1) * 0.3)} c={skinC} />
          <mesh position={[s * 0.11, 0.045, 0.035]} castShadow><boxGeometry args={[0.11, 0.08, 0.26]} /><S c="#f2f2f2" /></mesh>
          <mesh position={[s * 0.11, 0.008, 0.035]}><boxGeometry args={[0.115, 0.018, 0.27]} /><S c="#e8603a" /></mesh>
        </group>
      ))}
      {/* shorts */}
      <mesh position={[0, 0.83, 0]} scale={[1.28, 1, 0.82]} castShadow><cylinderGeometry args={[0.15, 0.17, 0.26, 10]} /><S c="#2a3a6a" /></mesh>
      {[-1, 1].map(s => <mesh key={s} position={[s * 0.1, 0.7, 0]} castShadow><cylinderGeometry args={[0.095 * (1 + (m - 1) * 0.3), 0.09 * (1 + (m - 1) * 0.3), 0.14, 8]} /><S c="#2a3a6a" /></mesh>)}
      {/* torso, pecs (chest softens/enlarges with estrogen), abs once the shirt is gone */}
      <group position={[0, slumpY, L.slump * 0.03]} rotation={[L.slump * 0.18, 0, 0]}>
        <mesh geometry={torso} castShadow receiveShadow><S c={skinC} /></mesh>
        {[-1, 1].map(s => <mesh key={s} position={[s * 0.078 * w, lerp(1.31, 1.275, L.chest), 0.1 * (1 + (m - 1) * 0.25)]} scale={[1.15, lerp(0.72, 1.05, L.chest), lerp(0.42, 0.72, L.chest)]} castShadow><icosahedronGeometry args={[0.085 * (1 + (m - 1) * 0.45), 1]} /><S c={skinC} /></mesh>)}
        {ripT >= 0 && m > 1.3 && [0, 1, 2].map(r => [-1, 1].map(s => <mesh key={`${r}${s}`} position={[s * 0.035, 1.18 - r * 0.07, 0.1 + 0.01 * (m - 1)]} scale={[1, 0.8, 0.4]}><icosahedronGeometry args={[0.03, 0]} /><S c={skinC} /></mesh>))}
        {/* traps + neck */}
        <mesh position={[0, 1.47, -0.025]} scale={[1.7, 0.6, 0.9]} castShadow><icosahedronGeometry args={[0.07 * (1 + (m - 1) * 0.8), 1]} /><S c={skinC} /></mesh>
        <mesh position={[0, 1.54, 0]} castShadow><cylinderGeometry args={[0.05 * (1 + (m - 1) * 0.45), 0.06 * (1 + (m - 1) * 0.5), 0.12, 8]} /><S c={skinC} /></mesh>
        {/* tank top: intact until the rip, then two halves fly off */}
        {ripT < 0 && <mesh geometry={shirt} castShadow><S c="#2fb3a3" /></mesh>}
        {ripT >= 0 && ripT < 50 && [halfL, halfR].map((g, i) => {
          const s = i ? 1 : -1, t = ripT / 30;
          return <mesh key={i} geometry={g} position={[s * (0.15 + t * 0.8), -t * t * 1.2 + t * 0.4, t * 0.5]} rotation={[t * 1.2, s * t * 1.5, s * t * 2]} castShadow><S c="#2fb3a3" side={THREE.DoubleSide} /></mesh>;
        })}
        {arm(1)}{arm(-1)}
        {head}
      </group>
    </group>
  );
};
const torsoGeoPts = (m: number, scale: number) => { const w = 1 + (m - 1) * 0.55; return [[0.13, 0.92], [0.135, 1.0], [0.15 * w, 1.12], [0.175 * w, 1.24], [0.19 * w, 1.33], [0.185 * w, 1.41], [0.12 * w, 1.47], [0.06, 1.5]].map(([r, y]) => new THREE.Vector2(r * scale, y)); };
