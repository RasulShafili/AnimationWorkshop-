// First-person café table: laptop, a growing tower of mugs, window onto a sunny street, counter with an espresso machine.
import React, { useLayoutEffect, useMemo, useRef } from "react";
import * as THREE from "three";
import T from "./timeline.json";

const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };
const sat = (v: number) => Math.min(1, Math.max(0, v));
type V3 = [number, number, number];
const M: React.FC<{ c: string | THREE.Color; e?: string | THREE.Color; ei?: number; r?: number; m?: number }> = ({ c, e = "#000", ei = 0, r = 0.8, m = 0 }) => <meshStandardMaterial color={c} emissive={e} emissiveIntensity={ei} roughness={r} metalness={m} flatShading />;
const B: React.FC<{ p: V3; s: V3; c: string | THREE.Color; rot?: V3; r?: number; m?: number }> = ({ p, s, c, rot = [0, 0, 0], r, m }) =>
  <mesh position={p} rotation={rot} castShadow receiveShadow><boxGeometry args={s} /><M c={c} r={r} m={m} /></mesh>;

// mug slots: a pyramid that grows to the right of the laptop
const SLOTS: V3[] = (() => {
  const out: V3[] = [], d = 0.115, h = 0.105, base: [number, number][] = [[0.28, 0.02], [0.4, 0.02], [0.52, 0.02], [0.28, -0.1], [0.4, -0.1], [0.52, -0.1]];
  base.forEach(([x, z]) => out.push([x, 0, z]));
  [[0.34, 0.02], [0.46, 0.02], [0.34, -0.1], [0.46, -0.1], [0.4, -0.04]].forEach(([x, z]) => out.push([x, h, z]));
  [[0.34, -0.04], [0.46, -0.04], [0.4, 0.02]].forEach(([x, z]) => out.push([x, h * 2, z]));
  [[0.4, -0.04], [0.4, -0.04]].forEach(([x, z], i) => out.push([x, h * (3 + i), z]));
  return out.map(([x, y, z]) => [x + 0.06, y, z] as V3);
})();
const MUGC = ["#f4f0e8", "#e8603a", "#3a8ae8", "#f4f0e8", "#3ac08a", "#e8c83a", "#f4f0e8", "#c84a6a", "#f4f0e8", "#6a5ab0", "#e8603a", "#f4f0e8", "#3a8ae8", "#e8c83a", "#f4f0e8", "#c84a6a"];

const Mug: React.FC<{ p: V3; c: string; k: number; f: number; arrive: number; fallen: number }> = ({ p, c, k, f, arrive, fallen }) => {
  const t = (f - arrive) / 10;
  if (t < 0) return null;
  const drop = Math.max(0, 1 - Math.min(1, t)) * 0.35, bounce = t > 1 && t < 1.6 ? Math.sin((t - 1) / 0.6 * Math.PI) * 0.012 : 0;
  const fx = fallen > 0 ? (rnd(k, 3) - 0.3) * 0.5 * fallen : 0, fz = fallen > 0 ? rnd(k, 4) * 0.25 * fallen : 0;
  const ry = fallen * (rnd(k, 5) * 2 - 1) * 2, rz = fallen * (rnd(k, 6) > 0.5 ? 1.57 : -1.57) * (p[1] > 0.05 ? 1 : 0.0);
  const y = p[1] * (1 - fallen) + drop + bounce;
  const steam = k < 16 && fallen < 0.2;
  return (
    <group position={[p[0] + fx, 0.776 + y + (fallen > 0 && p[1] > 0.05 ? 0.04 : 0), p[2] + fz]} rotation={[0, ry + rnd(k, 1) * 6, rz]}>
      <mesh position={[0, 0.05, 0]} castShadow receiveShadow><cylinderGeometry args={[0.048, 0.042, 0.1, 12]} /><M c={c} r={0.4} /></mesh>
      <mesh position={[0, 0.098, 0]}><cylinderGeometry args={[0.041, 0.041, 0.006, 12]} /><M c="#3a2010" r={0.2} /></mesh>
      <mesh position={[0.052, 0.05, 0]} rotation={[0, 0, Math.PI / 2]} castShadow><torusGeometry args={[0.024, 0.008, 6, 10, Math.PI]} /><M c={c} r={0.4} /></mesh>
      {steam && [0, 1, 2].map(i => { const u = ((f * 0.02 + i / 3 + k * 0.13) % 1); return <mesh key={i} position={[Math.sin(u * 6 + k) * 0.012, 0.11 + u * 0.12, 0]} scale={0.006 + u * 0.012}><icosahedronGeometry args={[1, 1]} /><meshStandardMaterial color="#ffffff" transparent opacity={0.3 * (1 - u)} depthWrite={false} /></mesh>; })}
    </group>
  );
};

// laptop screen lines: typing speed / garble / alarm per stage
const CodeLines: React.FC<{ f: number; stage: number }> = ({ f, stage }) => {
  const rows = 11, speed = [0.25, 0.9, 1.6, 2.4, 3.2, 0, 0][stage] ?? 0, alarm = stage === 4 && Math.floor(f / 6) % 2 === 0;
  const prog = f * speed * 0.02;
  return (
    <group position={[0, 1.02, -0.205]} rotation={[-0.18, 0, 0]}>
      <mesh><planeGeometry args={[0.44, 0.27]} /><meshBasicMaterial color={alarm ? new THREE.Color(1.3, 0.15, 0.15) : new THREE.Color(0.05, 0.06, 0.12)} toneMapped={false} /></mesh>
      {Array.from({ length: rows }, (_, r) => {
        const done = sat(prog - r * 0.35 + Math.floor(prog / (rows * 0.35)) * rows * 0.35), w = (0.12 + rnd(r + Math.floor(prog / (rows * 0.35)) * 13, 2) * 0.24) * Math.min(1, done * 2);
        const garble = stage >= 3 ? (rnd(r, Math.floor(f / 3)) - 0.5) * 0.06 : 0;
        const col = stage >= 3 ? new THREE.Color(1.0, 0.35, 0.3) : [new THREE.Color(0.3, 0.95, 0.6), new THREE.Color(0.9, 0.75, 0.3), new THREE.Color(0.4, 0.6, 1.0)][r % 3];
        return w > 0.005 ? <mesh key={r} position={[-0.2 + w / 2 + (r % 4) * 0.015 + garble, 0.115 - r * 0.021, 0.001]}><planeGeometry args={[w, 0.009]} /><meshBasicMaterial color={col} toneMapped={false} /></mesh> : null;
      })}
    </group>
  );
};

const Street: React.FC = () => {
  const ref = useRef<THREE.InstancedMesh>(null);
  const data = useMemo(() => {
    const ms: THREE.Matrix4[] = [], cs: THREE.Color[] = [];
    for (let i = 0; i < 14; i++) { const h = 4 + rnd(i, 2) * 6, w = 2.5 + rnd(i, 3) * 2; ms.push(new THREE.Matrix4().compose(new THREE.Vector3(-14 + i * 2.4, h / 2, -12 - rnd(i, 4) * 3), new THREE.Quaternion(), new THREE.Vector3(w, h, 2))); cs.push(new THREE.Color(["#e8c8a0", "#d8907a", "#c8d0e0", "#e0b070", "#a8c8b8"][i % 5])); }
    return { ms, cs, geo: new THREE.BoxGeometry(1, 1, 1), mat: new THREE.MeshStandardMaterial({ flatShading: true, roughness: 0.9 }) };
  }, []);
  useLayoutEffect(() => { data.ms.forEach((m, i) => { ref.current!.setMatrixAt(i, m); ref.current!.setColorAt(i, data.cs[i]); }); ref.current!.instanceMatrix.needsUpdate = true; if (ref.current!.instanceColor) ref.current!.instanceColor.needsUpdate = true; });
  return (
    <group>
      <instancedMesh ref={ref} args={[data.geo, data.mat, data.ms.length]} frustumCulled={false} />
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.01, -8]}><planeGeometry args={[60, 14]} /><M c="#8a8a90" /></mesh>
      {[-6, -2, 2, 6].map((x, i) => <group key={i} position={[x, 0, -7]}><mesh position={[0, 1, 0]}><cylinderGeometry args={[0.12, 0.16, 2, 5]} /><M c="#7a4a2a" /></mesh><mesh position={[0, 2.6, 0]}><icosahedronGeometry args={[1.1, 0]} /><M c={i % 2 ? "#6ab04a" : "#8ac04a"} /></mesh></group>)}
    </group>
  );
};

export const Cafe: React.FC<{ f: number; cups: number; stage: number; fallen: number; dim: number }> = ({ f, cups, stage, fallen, dim }) => {
  const lit = 1 - dim;
  return (
    <group>
      <color attach="background" args={["#8ac0ec"]} />
      <mesh position={[0, 8, -20]}><planeGeometry args={[80, 40]} /><meshBasicMaterial color="#7ab4e8" /></mesh>
      <group position={[0, -0.0, 0]}><Street /></group>
      {/* floor, walls, the big window behind the table */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow><planeGeometry args={[10, 10]} /><M c="#8a5a3a" /></mesh>
      {Array.from({ length: 12 }, (_, i) => <B key={i} p={[-5 + i * 0.85, 0.002, 0]} s={[0.015, 0.004, 10]} c="#6a4028" />)}
      <B p={[-2.6, 1.6, -2.2]} s={[2.8, 3.2, 0.15]} c="#e8d8c0" /><B p={[2.6, 1.6, -2.2]} s={[2.8, 3.2, 0.15]} c="#e8d8c0" />
      <B p={[0, 0.35, -2.2]} s={[2.4, 0.7, 0.15]} c="#e8d8c0" /><B p={[0, 2.95, -2.2]} s={[2.4, 0.5, 0.15]} c="#e8d8c0" />
      {[-1.18, 0, 1.18].map(x => <B key={x} p={[x, 1.7, -2.16]} s={[0.07, 2.0, 0.1]} c="#2a2a30" m={0.4} r={0.4} />)}
      <B p={[0, 1.7, -2.16]} s={[2.4, 0.06, 0.1]} c="#2a2a30" m={0.4} r={0.4} />
      <B p={[-4.0, 1.6, 0]} s={[0.15, 3.2, 8]} c="#c86a4a" /><B p={[4.0, 1.6, 0]} s={[0.15, 3.2, 8]} c="#c86a4a" />
      {/* menu board + shelf with jars on the side walls */}
      <B p={[3.9, 2.0, -1.0]} s={[0.04, 0.9, 1.3]} c="#1a2a24" />
      {[0, 1, 2, 3].map(i => <B key={i} p={[3.87, 2.25 - i * 0.16, -1.0]} s={[0.01, 0.03, 0.9 - (i % 2) * 0.3]} c="#f0e8d0" />)}
      <B p={[-3.88, 1.9, -0.6]} s={[0.25, 0.04, 1.6]} c="#6a4028" />
      {Array.from({ length: 6 }, (_, i) => <mesh key={i} position={[-3.82, 2.02, -1.25 + i * 0.26]} castShadow><cylinderGeometry args={[0.07, 0.07, 0.2, 8]} /><M c={["#c8903a", "#7a4a2a", "#e8d8a0", "#5a3020", "#c8903a", "#7a4a2a"][i]} r={0.3} /></mesh>)}
      {/* counter + espresso machine (left background) */}
      <group position={[-2.6, 0, -1.5]}>
        <B p={[0, 0.5, 0]} s={[1.6, 1.0, 0.6]} c="#3a2a24" /><B p={[0, 1.02, 0]} s={[1.7, 0.05, 0.7]} c="#d8d0c0" />
        <B p={[0.2, 1.25, 0]} s={[0.6, 0.4, 0.4]} c="#c0c4cc" m={0.7} r={0.25} /><B p={[0.2, 1.48, 0]} s={[0.62, 0.05, 0.42]} c="#2a2a30" />
        {[0, 0.25].map(x => <mesh key={x} position={[0.08 + x, 1.08, 0.12]}><cylinderGeometry args={[0.03, 0.03, 0.08, 8]} /><M c="#2a2a30" /></mesh>)}
      </group>
      {/* pendant lamps */}
      {[-1.4, 1.4].map(x => (
        <group key={x} position={[x, 2.6, -0.8]}>
          <mesh position={[0, 0.5, 0]}><cylinderGeometry args={[0.005, 0.005, 1, 4]} /><M c="#2a2a30" /></mesh>
          <mesh><coneGeometry args={[0.18, 0.18, 10, 1, true]} /><meshStandardMaterial color="#2a5a4a" side={THREE.DoubleSide} flatShading /></mesh>
          <mesh position={[0, -0.06, 0]}><sphereGeometry args={[0.05, 8, 6]} /><meshBasicMaterial color={new THREE.Color(3, 2.3, 1.4).multiplyScalar(lit)} toneMapped={false} /></mesh>
        </group>
      ))}
      {/* plants */}
      {[[-3.4, -1.9], [3.4, -1.9]].map(([x, z], i) => (
        <group key={i} position={[x, 0, z]}>
          <mesh position={[0, 0.25, 0]} castShadow><cylinderGeometry args={[0.22, 0.17, 0.5, 8]} /><M c="#e8e0d0" /></mesh>
          {[0, 1, 2, 3, 4, 5].map(k => <mesh key={k} position={[Math.cos(k * 1.1) * 0.14, 0.75 + k * 0.12, Math.sin(k * 1.1) * 0.14]} rotation={[Math.cos(k) * 0.6, k, Math.sin(k) * 0.6]} castShadow><coneGeometry args={[0.16, 0.7, 4]} /><M c={k % 2 ? "#4a8a3a" : "#5aa04a"} /></mesh>)}
        </group>
      ))}
      {/* empty tables in the background */}
      {[[-1.6, -1.5], [1.7, -1.4]].map(([x, z], i) => (
        <group key={i} position={[x, 0, z]}>
          <mesh position={[0, 0.74, 0]} castShadow><cylinderGeometry args={[0.35, 0.35, 0.04, 14]} /><M c="#e8d8c0" /></mesh>
          <mesh position={[0, 0.37, 0]}><cylinderGeometry args={[0.03, 0.03, 0.74, 6]} /><M c="#2a2a30" /></mesh>
          {[-1, 1].map(s => <group key={s} position={[s * 0.5, 0, 0.1]}><B p={[0, 0.45, 0]} s={[0.32, 0.04, 0.32]} c="#7a4a2a" /><B p={[0, 0.22, 0]} s={[0.04, 0.44, 0.04]} c="#2a2a30" /></group>)}
        </group>
      ))}
      {/* our table */}
      <B p={[0, 0.75, -0.1]} s={[1.5, 0.05, 0.85]} c="#a8703a" r={0.6} />
      <B p={[0, 0.37, -0.1]} s={[0.08, 0.74, 0.08]} c="#2a2a30" />
      {/* laptop */}
      <B p={[0, 0.785, -0.05]} s={[0.48, 0.016, 0.32]} c="#b8bcc8" m={0.6} r={0.3} />
      <B p={[0, 0.79, 0.0]} s={[0.4, 0.004, 0.14]} c="#2a2a34" />
      <group position={[0, 0.79, -0.21]} rotation={[-0.18, 0, 0]}><B p={[0, 0.17, -0.006]} s={[0.48, 0.32, 0.012]} c="#b8bcc8" m={0.6} r={0.3} /></group>
      <CodeLines f={f} stage={stage} />
      {/* phone + croissant plate */}
      <B p={[-0.5, 0.783, 0.05]} s={[0.08, 0.01, 0.15]} c="#1a1a24" />
      <mesh position={[-0.45, 0.79, -0.25]} receiveShadow><cylinderGeometry args={[0.1, 0.09, 0.015, 14]} /><M c="#f4f4f8" /></mesh>
      <mesh position={[-0.45, 0.815, -0.25]} rotation={[0, 0.5, Math.PI / 2]} scale={[1, 1.9, 1]} castShadow><capsuleGeometry args={[0.025, 0.04, 3, 6]} /><M c="#d8903a" /></mesh>
      {/* the mugs */}
      {SLOTS.map((p, k) => k < cups && <Mug key={k} p={p} c={MUGC[k]} k={k} f={f} arrive={T.cupsAt[k]} fallen={fallen} />)}
    </group>
  );
};
