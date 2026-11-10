// Bedroom at night: bed, desk with a glowing monitor, window onto a city, wall clock, lamp, rug, shelf, plant.
import React, { useLayoutEffect, useMemo, useRef } from "react";
import * as THREE from "three";

const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };
type V3 = [number, number, number];
const M: React.FC<{ c: string | THREE.Color; e?: string | THREE.Color; ei?: number; r?: number }> = ({ c, e = "#000", ei = 0, r = 0.85 }) => <meshStandardMaterial color={c} emissive={e} emissiveIntensity={ei} roughness={r} flatShading />;
const B: React.FC<{ p: V3; s: V3; c: string | THREE.Color; rot?: V3; e?: string; ei?: number }> = ({ p, s, c, rot = [0, 0, 0], e, ei }) =>
  <mesh position={p} rotation={rot} castShadow receiveShadow><boxGeometry args={s} /><M c={c} e={e} ei={ei} /></mesh>;

const Skyline: React.FC<{ night: number }> = ({ night }) => {
  const tr = useRef<THREE.InstancedMesh>(null), wr = useRef<THREE.InstancedMesh>(null);
  const data = useMemo(() => {
    const t: THREE.Matrix4[] = [], w: THREE.Matrix4[] = [];
    for (let i = 0; i < 40; i++) {
      const x = (rnd(i, 1) - 0.5) * 60, z = -14 - rnd(i, 2) * 30, h = 5 + rnd(i, 3) * 16, wd = 2.5 + rnd(i, 4) * 3;
      t.push(new THREE.Matrix4().compose(new THREE.Vector3(x, h / 2 - 4, z), new THREE.Quaternion(), new THREE.Vector3(wd, h, wd)));
      for (let k = 0; k < 9; k++) if (rnd(i, 10 + k) > 0.45) w.push(new THREE.Matrix4().compose(new THREE.Vector3(x + (rnd(i, 30 + k) - 0.5) * wd * 0.8, rnd(i, 50 + k) * h * 0.9 - 4, z + wd / 2 + 0.05), new THREE.Quaternion(), new THREE.Vector3(0.4, 0.5, 0.1)));
    }
    return { t, w, box: new THREE.BoxGeometry(1, 1, 1), tm: new THREE.MeshBasicMaterial({ color: "#2a2a4a" }), wm: new THREE.MeshBasicMaterial({ color: "#ffd890", toneMapped: false }) };
  }, []);
  useLayoutEffect(() => {
    data.t.forEach((m, i) => tr.current!.setMatrixAt(i, m)); tr.current!.instanceMatrix.needsUpdate = true;
    data.w.forEach((m, i) => wr.current!.setMatrixAt(i, m)); wr.current!.instanceMatrix.needsUpdate = true;
  });
  data.tm.color.set("#2a2a4a").lerp(new THREE.Color("#8a9ab8"), 1 - night);
  data.wm.color.setRGB(1.8 * night + 0.5, 1.4 * night + 0.5, 0.7 * night + 0.5);
  return <group><instancedMesh ref={tr} args={[data.box, data.tm, data.t.length]} frustumCulled={false} /><instancedMesh ref={wr} args={[data.box, data.wm, data.w.length]} frustumCulled={false} /></group>;
};

/** hours: time awake (drives the wall clock and day/night in the window); hall: 0..1 hallucination strength */
export const Room: React.FC<{ f: number; hours: number; hall: number; dim: number }> = ({ f, hours, hall, dim }) => {
  const tod = ((hours + 23) % 24), night = THREE.MathUtils.clamp(-Math.cos((tod - 12) / 12 * Math.PI) * 1.6 + 0.5, 0, 1);  // starts at 11 pm
  const sky = new THREE.Color("#0a1030").lerp(new THREE.Color("#7ab8f0"), 1 - night);
  const wob = (k: number) => Math.sin(f * 0.13 + k) * 0.07 * hall;
  const ha = (hours / 12) * Math.PI * 2, ma = hours * Math.PI * 2;
  const lit = (1 - dim);
  return (
    <group>
      <mesh position={[0, 6, -30]}><planeGeometry args={[120, 60]} /><meshBasicMaterial color={sky} /></mesh>
      <mesh position={[5, 9, -29]}><circleGeometry args={[1.6, 20]} /><meshBasicMaterial color={new THREE.Color(night * 2.2 + 0.6, night * 2.1 + 0.6, night * 1.6 + 0.5)} toneMapped={false} /></mesh>
      <Skyline night={night} />
      {/* floor + rug */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow><planeGeometry args={[7, 8]} /><M c="#7a5a44" /></mesh>
      {Array.from({ length: 9 }, (_, i) => <B key={i} p={[-3.5 + i * 0.875, 0.002, 0]} s={[0.02, 0.004, 8]} c="#5a4030" />)}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0.2, 0.01, 0.6]} receiveShadow><circleGeometry args={[1.25, 24]} /><M c="#b8504a" /></mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0.2, 0.012, 0.6]}><ringGeometry args={[0.75, 0.9, 24]} /><M c="#e8c880" /></mesh>
      {/* walls: back wall with a window, side walls */}
      <B p={[-2.4, 1.5, -3]} s={[2.2, 3, 0.2]} c="#5a5a82" /><B p={[2.45, 1.5, -3]} s={[2.1, 3, 0.2]} c="#5a5a82" />
      <B p={[0.05, 0.5, -3]} s={[2.7, 1.0, 0.2]} c="#5a5a82" /><B p={[0.05, 2.75, -3]} s={[2.7, 0.5, 0.2]} c="#5a5a82" />
      <B p={[0.05, 1.75, -2.95]} s={[0.06, 1.5, 0.08]} c="#e8e0d0" /><B p={[0.05, 1.75, -2.95]} s={[2.7, 0.06, 0.08]} c="#e8e0d0" /><B p={[0.05, 0.98, -2.9]} s={[2.9, 0.08, 0.25]} c="#e8e0d0" />
      <B p={[-3.5, 1.5, 0]} s={[0.2, 3, 8]} c="#50507a" /><B p={[3.5, 1.5, 0]} s={[0.2, 3, 8]} c="#50507a" />
      {/* curtains */}
      {[-1.45, 1.55].map((x, i) => <B key={i} p={[x, 1.75, -2.82]} s={[0.4, 1.9, 0.08]} c="#3a7a8a" rot={[0, 0, wob(i) * 0.5]} />)}
      {/* wall clock */}
      <group position={[2.5, 2.25, -2.88]}>
        <mesh><cylinderGeometry args={[0.3, 0.3, 0.05, 20]} /><M c="#f4f0e8" /></mesh>
        <mesh rotation={[Math.PI / 2, 0, 0]}><torusGeometry args={[0.3, 0.03, 6, 20]} /><M c="#2a2a34" /></mesh>
        <group rotation={[0, 0, -ha]}><B p={[0, 0.07, 0.04]} s={[0.035, 0.16, 0.01]} c="#1a1a24" /></group>
        <group rotation={[0, 0, -ma]}><B p={[0, 0.11, 0.05]} s={[0.022, 0.24, 0.01]} c="#c83a3a" /></group>
      </group>
      {/* bed (left) */}
      <group rotation={[0, 0, wob(1) * 0.4]}>
        <B p={[-1.85, 0.12, -1.2]} s={[2.2, 0.24, 2.9]} c="#6a4a3a" /><B p={[-1.85, 0.3, -1.2]} s={[2.1, 0.16, 2.8]} c="#e8e4f0" />
        <B p={[-1.85, 0.39, -0.7]} s={[2.12, 0.08, 1.8]} c="#4a6ab8" /><B p={[-1.85, 0.6, -2.72]} s={[2.2, 1.0, 0.14]} c="#6a4a3a" />
        {[-2.35, -1.35].map(x => <mesh key={x} position={[x, 0.45, -2.2]} scale={[1, 0.45, 0.7]} castShadow><icosahedronGeometry args={[0.36, 1]} /><M c="#f4f0f8" /></mesh>)}
      </group>
      {/* nightstand + lamp */}
      <B p={[-0.45, 0.25, -2.5]} s={[0.5, 0.5, 0.5]} c="#6a4a3a" />
      <mesh position={[-0.45, 0.62, -2.5]}><cylinderGeometry args={[0.03, 0.08, 0.24, 8]} /><M c="#2a2a34" /></mesh>
      <mesh position={[-0.45, 0.84, -2.5]}><coneGeometry args={[0.2, 0.26, 10, 1, true]} /><meshStandardMaterial color="#ffd8a0" emissive="#ffb060" emissiveIntensity={1.6 * lit} side={THREE.DoubleSide} flatShading /></mesh>
      {/* desk (right wall), monitor, chair, mug */}
      <group rotation={[0, 0, wob(2) * 0.3]}>
        <B p={[2.9, 0.72, -0.8]} s={[0.8, 0.06, 1.8]} c="#8a6a4a" />
        {[-1.6, 0].map(z => <B key={z} p={[2.9, 0.36, z]} s={[0.7, 0.72, 0.06]} c="#6a4a3a" />)}
        <B p={[3.12, 1.12, -0.8]} s={[0.05, 0.5, 0.86]} c="#1a1a24" /><B p={[3.1, 0.82, -0.8]} s={[0.12, 0.14, 0.12]} c="#1a1a24" />
        <mesh position={[3.09, 1.12, -0.8]} rotation={[0, -Math.PI / 2, 0]}><planeGeometry args={[0.8, 0.44]} /><meshBasicMaterial color={new THREE.Color(0.7, 1.5, 2.2).multiplyScalar(lit * (0.9 + 0.1 * Math.sin(f * 0.6)))} toneMapped={false} /></mesh>
        <B p={[2.75, 0.76, -0.8]} s={[0.16, 0.02, 0.46]} c="#2a2a34" />
        <mesh position={[2.8, 0.81, -0.2]} castShadow><cylinderGeometry args={[0.045, 0.04, 0.11, 8]} /><M c="#e8603a" /></mesh>
        {[0, 1, 2].map(i => <mesh key={i} position={[2.72 + i * 0.07, 0.8, -1.45 + i * 0.06]} castShadow><cylinderGeometry args={[0.033, 0.033, 0.12, 8]} /><M c={["#3ac06a", "#3a8ae8", "#e8c83a"][i]} r={0.3} /></mesh>)}
      </group>
      <group position={[2.05, 0, -0.8]}>
        <B p={[0, 0.44, 0]} s={[0.5, 0.06, 0.5]} c="#2a2a34" /><B p={[-0.24, 0.8, 0]} s={[0.06, 0.7, 0.5]} c="#2a2a34" />
        <mesh position={[0, 0.22, 0]}><cylinderGeometry args={[0.03, 0.03, 0.44, 6]} /><M c="#8a8a90" /></mesh>
        <mesh position={[0, 0.03, 0]}><cylinderGeometry args={[0.28, 0.28, 0.04, 5]} /><M c="#2a2a34" /></mesh>
      </group>
      {/* shelf with books + plant + poster */}
      <B p={[-3.32, 1.9, 0.8]} s={[0.25, 0.05, 1.4]} c="#8a6a4a" />
      {Array.from({ length: 7 }, (_, i) => <B key={i} p={[-3.3, 2.08 + (i % 2) * 0.02, 0.25 + i * 0.17]} s={[0.18, 0.3 + (i % 3) * 0.04, 0.12]} c={["#c84a3a", "#3a8ae8", "#e8c83a", "#3ac06a", "#b05ac8", "#e8603a", "#4ab8c8"][i]} rot={[i === 6 ? 0.3 : 0, 0, 0]} />)}
      <mesh position={[3.0, 0.22, 1.9]} castShadow><cylinderGeometry args={[0.22, 0.16, 0.44, 8]} /><M c="#e8e0d0" /></mesh>
      {[0, 1, 2, 3, 4].map(k => <mesh key={k} position={[3.0 + Math.cos(k * 1.3) * 0.12, 0.7 + k * 0.1, 1.9 + Math.sin(k * 1.3) * 0.12]} rotation={[Math.cos(k) * 0.6 + wob(k), k, Math.sin(k) * 0.6]} castShadow><coneGeometry args={[0.13, 0.6, 4]} /><M c={k % 2 ? "#4a8a3a" : "#5aa04a"} /></mesh>)}
      <B p={[-3.38, 1.75, -1.4]} s={[0.03, 0.9, 0.65]} c="#e8c880" /><B p={[-3.36, 1.75, -1.4]} s={[0.03, 0.74, 0.5]} c="#3a4a8a" />
      {/* hallucinations: shadow people with glowing eyes, eyes in the window */}
      {hall > 0.05 && [[-3.0, 1.6, 1], [0.9, -2.6, 2], [3.05, 2.6, 3]].map(([x, z, k], i) => (
        <group key={i} position={[x, 0, z]} scale={[1, 0.6 + 0.5 * Math.min(1, hall * 1.4 - i * 0.25) + Math.sin(f * 0.1 + k) * 0.04, 1]} visible={hall * 1.4 - i * 0.25 > 0.05}>
          <mesh position={[0, 1.0, 0]}><capsuleGeometry args={[0.24, 1.5, 3, 7]} /><meshBasicMaterial color="#05040c" transparent opacity={Math.min(0.92, hall * 1.2)} /></mesh>
          {[-0.09, 0.09].map(ex => <mesh key={ex} position={[ex, 1.82, 0.22]}><sphereGeometry args={[0.035, 6, 5]} /><meshBasicMaterial color={new THREE.Color(3.5, 0.5, 0.4).multiplyScalar(hall)} toneMapped={false} /></mesh>)}
        </group>
      ))}
      {hall > 0.3 && Array.from({ length: 6 }, (_, i) => <mesh key={i} position={[-1.0 + rnd(i, 71) * 2.2, 1.2 + rnd(i, 72) * 1.0, -3.3]}><sphereGeometry args={[0.05, 6, 5]} /><meshBasicMaterial color={new THREE.Color(3, 2.6, 0.6).multiplyScalar(((f + i * 9) % 40 < 34 ? 1 : 0) * hall)} toneMapped={false} /></mesh>)}
    </group>
  );
};
