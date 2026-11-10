// A warm loft gym at sunset: big factory windows with a city skyline outside (so every part of the frame is filled),
// brick wall, rubber floor with mats, dumbbell rack, bench press, squat rack, kettlebells, punching bag, plants, pendant lamps.
import React, { useLayoutEffect, useMemo, useRef } from "react";
import * as THREE from "three";

const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };
type V3 = [number, number, number];
const M: React.FC<{ c: string | THREE.Color; r?: number; m?: number; e?: string; ei?: number }> = ({ c, r = 0.8, m = 0, e = "#000", ei = 0 }) => <meshStandardMaterial color={c} roughness={r} metalness={m} emissive={e} emissiveIntensity={ei} flatShading />;
const B: React.FC<{ p: V3; s: V3; c: string; r?: number; m?: number; rot?: V3; e?: string; ei?: number }> = ({ p, s, c, r, m, rot = [0, 0, 0], e, ei }) =>
  <mesh position={p} rotation={rot} castShadow receiveShadow><boxGeometry args={s} /><M c={c} r={r} m={m} e={e} ei={ei} /></mesh>;
const Cyl: React.FC<{ p: V3; r: number; h: number; c: string; rot?: V3; seg?: number; m?: number; rr?: number }> = ({ p, r, h, c, rot = [0, 0, 0], seg = 10, m = 0, rr = 0.6 }) =>
  <mesh position={p} rotation={rot} castShadow receiveShadow><cylinderGeometry args={[r, r, h, seg]} /><M c={c} m={m} r={rr} /></mesh>;

const Dumbbell: React.FC<{ p: V3; s: number; c?: string }> = ({ p, s, c = "#2a2a30" }) => (
  <group position={p} rotation={[0, 0, Math.PI / 2]}>
    <Cyl p={[0, 0, 0]} r={0.016 * s} h={0.22 * s} c="#9a9aa0" m={0.6} rr={0.3} />
    {[-1, 1].map(k => <Cyl key={k} p={[0, k * 0.1 * s, 0]} r={0.05 * s} h={0.06 * s} c={c} seg={8} />)}
  </group>
);

// sunset skyline outside the windows, instanced
const Skyline: React.FC<{ glow: number }> = ({ glow }) => {
  const ref = useRef<THREE.InstancedMesh>(null), wref = useRef<THREE.InstancedMesh>(null);
  const { towers, wins } = useMemo(() => {
    const towers: THREE.Matrix4[] = [], wins: THREE.Matrix4[] = [];
    for (let i = 0; i < 70; i++) {
      const x = (rnd(i, 1) - 0.5) * 120, z = -22 - rnd(i, 2) * 60, h = 6 + rnd(i, 3) * 30 * (1 - Math.abs(x) / 90), w = 3 + rnd(i, 4) * 5;
      towers.push(new THREE.Matrix4().compose(new THREE.Vector3(x, h / 2 - 2, z), new THREE.Quaternion(), new THREE.Vector3(w, h, w)));
      for (let k = 0; k < 10; k++) if (rnd(i, 10 + k) > 0.45) wins.push(new THREE.Matrix4().compose(new THREE.Vector3(x + (rnd(i, 30 + k) - 0.5) * w * 0.8, rnd(i, 50 + k) * h * 0.9, z + w / 2 + 0.05), new THREE.Quaternion(), new THREE.Vector3(0.5, 0.6, 0.1)));
    }
    return { towers, wins };
  }, []);
  const res = useMemo(() => ({ box: new THREE.BoxGeometry(1, 1, 1), tm: new THREE.MeshStandardMaterial({ color: "#5a4a6a", flatShading: true, roughness: 0.9 }), wm: new THREE.MeshBasicMaterial({ color: new THREE.Color(1.6 * glow + 0.6, 1.2 * glow + 0.45, 0.5 * glow + 0.25), toneMapped: false }) }), [glow]);
  useLayoutEffect(() => {
    towers.forEach((m, i) => ref.current!.setMatrixAt(i, m)); ref.current!.instanceMatrix.needsUpdate = true;
    wins.forEach((m, i) => wref.current!.setMatrixAt(i, m)); wref.current!.instanceMatrix.needsUpdate = true;
  });
  return (
    <group>
      <instancedMesh ref={ref} args={[res.box, res.tm, towers.length]} frustumCulled={false} />
      <instancedMesh ref={wref} args={[res.box, res.wm, wins.length]} frustumCulled={false} />
    </group>
  );
};

const SkyDome: React.FC = () => {
  const geo = useMemo(() => {
    const g = new THREE.SphereGeometry(200, 24, 16), p = g.attributes.position, col = new Float32Array(p.count * 3);
    const top = new THREE.Color("#5a5a9a"), mid = new THREE.Color("#f08a5a"), bot = new THREE.Color("#ffcf8a");
    for (let i = 0; i < p.count; i++) { const u = Math.max(0, p.getY(i) / 200); const c = u < 0.15 ? bot.clone().lerp(mid, u / 0.15) : mid.clone().lerp(top, Math.min(1, (u - 0.15) / 0.5)); col.set([c.r, c.g, c.b], i * 3); }
    g.setAttribute("color", new THREE.BufferAttribute(col, 3)); return g;
  }, []);
  return <mesh geometry={geo}><meshBasicMaterial vertexColors side={THREE.BackSide} fog={false} toneMapped={false} /></mesh>;
};

export const Gym: React.FC<{ f: number; dropT: number }> = ({ f, dropT }) => {
  const brick = useMemo(() => {
    const items: { p: V3; c: string }[] = [];
    for (let y = 0; y < 22; y++) for (let x = 0; x < 30; x++) items.push({ p: [-5.95, 0.08 + y * 0.18, -4.6 + x * 0.32 + (y % 2) * 0.16], c: ["#9a4a36", "#a8553c", "#8a4232", "#b0603f"][Math.floor(rnd(x * 31 + y, 2) * 4)] });
    return items;
  }, []);
  const bref = useRef<THREE.InstancedMesh>(null);
  const bres = useMemo(() => ({ g: new THREE.BoxGeometry(0.1, 0.16, 0.3), m: new THREE.MeshStandardMaterial({ flatShading: true, roughness: 0.95 }) }), []);
  useLayoutEffect(() => {
    brick.forEach((b, i) => { bref.current!.setMatrixAt(i, new THREE.Matrix4().makeTranslation(...b.p)); bref.current!.setColorAt(i, new THREE.Color(b.c)); });
    bref.current!.instanceMatrix.needsUpdate = true; if (bref.current!.instanceColor) bref.current!.instanceColor.needsUpdate = true;
  });
  // dumbbell dropped by the hero: falls, bounces, rolls
  const dt = dropT, dropY = dt < 0 ? null : dt < 9 ? 1.0 - 0.012 * dt * dt : dt < 15 ? Math.max(0.06, 0.06 + Math.sin((dt - 9) / 6 * Math.PI) * 0.08) : 0.06;
  const swing = Math.sin(f * 0.05) * 0.04;
  return (
    <group>
      <SkyDome />
      <Skyline glow={0.6} />
      {/* floor: rubber + mats */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow><planeGeometry args={[14, 12]} /><M c="#2c2a30" r={0.95} /></mesh>
      {[[-1.5, 0.8], [1.5, 0.8], [0, -1.4], [-3, -1.4], [3, -1.4]].map(([x, z], i) => <mesh key={i} rotation={[-Math.PI / 2, 0, 0]} position={[x, 0.004, z]} receiveShadow><planeGeometry args={[1.45, 1.45]} /><M c={i % 2 ? "#3a3640" : "#34303a"} r={0.95} /></mesh>)}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.006, 3.4]} receiveShadow><planeGeometry args={[14, 0.08]} /><M c="#e8b84a" /></mesh>
      {/* brick wall (left) */}
      <instancedMesh ref={bref} args={[bres.g, bres.m, brick.length]} castShadow receiveShadow frustumCulled={false} />
      <B p={[-6.02, 2, -0.1]} s={[0.05, 4, 9.6]} c="#d8c8b0" />
      {/* back wall with three tall factory windows */}
      {[-4.7, 4.7].map(x => <B key={x} p={[x, 2, -5]} s={[2.6, 4, 0.25]} c="#d8c8b0" />)}
      {[-1.7, 1.7].map(x => <B key={x} p={[x, 2, -5]} s={[0.4, 4, 0.25]} c="#d8c8b0" />)}
      <B p={[0, 0.3, -5]} s={[6.8, 0.6, 0.25]} c="#d8c8b0" /><B p={[0, 3.85, -5]} s={[6.8, 0.3, 0.25]} c="#d8c8b0" />
      {[-3.25, 0, 3.25].map(cx => (
        <group key={cx}>
          {[-0.95, -0.32, 0.32, 0.95].map(dx => <B key={dx} p={[cx + dx, 2.05, -4.98]} s={[0.05, 3.2, 0.08]} c="#2a2a30" m={0.5} r={0.4} />)}
          {[0.95, 1.8, 2.65].map(y => <B key={y} p={[cx, y, -4.98]} s={[2.9, 0.05, 0.08]} c="#2a2a30" m={0.5} r={0.4} />)}
        </group>
      ))}
      {/* right wall (dark) with a long mirror strip */}
      <B p={[6, 2, -0.5]} s={[0.2, 4, 9]} c="#3a3842" />
      <mesh position={[5.88, 1.5, -0.6]} rotation={[0, -Math.PI / 2, 0]}><planeGeometry args={[6, 1.8]} /><meshStandardMaterial color="#8aa0b8" metalness={0.9} roughness={0.08} /></mesh>
      {/* dumbbell rack */}
      <group position={[-4.2, 0, -2.6]} rotation={[0, 0.5, 0]}>
        {[-0.9, 0.9].map(x => <B key={x} p={[x, 0.45, 0]} s={[0.06, 0.9, 0.5]} c="#2a2a30" m={0.5} r={0.4} />)}
        {[0.35, 0.7].map(y => <B key={y} p={[0, y, 0]} s={[1.9, 0.04, 0.42]} c="#3a3a44" m={0.5} r={0.4} />)}
        {Array.from({ length: 6 }, (_, i) => <Dumbbell key={i} p={[-0.75 + i * 0.3, 0.42, 0]} s={0.8 + i * 0.12} c={["#2a2a30", "#c84a3a", "#2a2a30", "#3a6ab8", "#2a2a30", "#e8b84a"][i]} />)}
        {Array.from({ length: 6 }, (_, i) => <Dumbbell key={i} p={[-0.75 + i * 0.3, 0.77, 0]} s={0.7 + i * 0.1} />)}
      </group>
      {/* bench press */}
      <group position={[2.6, 0, -2.4]} rotation={[0, -0.4, 0]}>
        <B p={[0, 0.42, 0]} s={[0.32, 0.1, 1.2]} c="#c84a3a" r={0.6} />
        <B p={[0, 0.2, 0.4]} s={[0.08, 0.4, 0.08]} c="#2a2a30" m={0.5} /><B p={[0, 0.2, -0.4]} s={[0.08, 0.4, 0.08]} c="#2a2a30" m={0.5} />
        {[-0.45, 0.45].map(x => <B key={x} p={[x, 0.6, -0.4]} s={[0.06, 1.2, 0.06]} c="#2a2a30" m={0.5} />)}
        <Cyl p={[0, 1.08, -0.42]} r={0.018} h={1.9} c="#b0b0b8" rot={[0, 0, Math.PI / 2]} m={0.8} rr={0.25} />
        {[-0.75, 0.75].map(x => <Cyl key={x} p={[x, 1.08, -0.42]} r={0.2} h={0.07} c="#2a2a30" rot={[0, 0, Math.PI / 2]} seg={12} />)}
      </group>
      {/* squat rack */}
      <group position={[4.4, 0, -3.6]}>
        {[[-0.6, -0.5], [0.6, -0.5], [-0.6, 0.5], [0.6, 0.5]].map(([x, z], i) => <B key={i} p={[x, 1.15, z]} s={[0.07, 2.3, 0.07]} c="#e8b84a" m={0.3} r={0.5} />)}
        <B p={[0, 2.28, 0]} s={[1.3, 0.07, 1.07]} c="#e8b84a" m={0.3} r={0.5} />
        <Cyl p={[0, 1.4, 0.5]} r={0.018} h={2.0} c="#b0b0b8" rot={[0, 0, Math.PI / 2]} m={0.8} rr={0.25} />
        {[-0.8, 0.8].map(x => <Cyl key={x} p={[x, 1.4, 0.5]} r={0.24} h={0.08} c="#3a6ab8" rot={[0, 0, Math.PI / 2]} seg={12} />)}
      </group>
      {/* kettlebells */}
      {[[-2.6, -3.9, "#2a2a30"], [-2.2, -3.95, "#c84a3a"], [-1.8, -3.9, "#2a2a30"]].map(([x, z, c], i) => (
        <group key={i} position={[x as number, 0, z as number]}>
          <mesh position={[0, 0.12, 0]} castShadow><icosahedronGeometry args={[0.13, 1]} /><M c={c as string} r={0.5} /></mesh>
          <mesh position={[0, 0.26, 0]}><torusGeometry args={[0.07, 0.02, 6, 10, Math.PI]} /><M c={c as string} r={0.5} /></mesh>
        </group>
      ))}
      {/* punching bag */}
      <group position={[-3.4, 0, 0.9]} rotation={[swing, 0, swing * 0.6]}>
        <Cyl p={[0, 3.3, 0]} r={0.01} h={1.4} c="#8a8a90" m={0.7} />
        <mesh position={[0, 1.85, 0]} castShadow><cylinderGeometry args={[0.22, 0.22, 1.1, 12]} /><M c="#c84a3a" r={0.55} /></mesh>
        <Cyl p={[0, 2.42, 0]} r={0.225} h={0.06} c="#2a2a30" />
      </group>
      {/* plants */}
      {[[-5.4, -4.4], [5.3, -4.4], [5.3, 2.6]].map(([x, z], i) => (
        <group key={i} position={[x, 0, z]}>
          <mesh position={[0, 0.2, 0]} castShadow><cylinderGeometry args={[0.2, 0.15, 0.4, 8]} /><M c="#e8e0d0" /></mesh>
          {[0, 1, 2, 3, 4].map(k => <mesh key={k} position={[Math.cos(k * 1.3) * 0.12, 0.6 + k * 0.12, Math.sin(k * 1.3) * 0.12]} rotation={[Math.cos(k) * 0.6, k, Math.sin(k) * 0.6]} castShadow><coneGeometry args={[0.14, 0.6, 4]} /><M c={k % 2 ? "#4a8a3a" : "#5aa04a"} /></mesh>)}
        </group>
      ))}
      {/* pendant lamps */}
      {[-2.5, 0, 2.5].map(x => (
        <group key={x} position={[x, 3.6, -0.8]}>
          <Cyl p={[0, 0.5, 0]} r={0.006} h={1} c="#2a2a30" />
          <mesh castShadow><coneGeometry args={[0.22, 0.2, 10, 1, true]} /><meshStandardMaterial color="#2a2a30" side={THREE.DoubleSide} flatShading /></mesh>
          <mesh position={[0, -0.07, 0]}><sphereGeometry args={[0.07, 8, 6]} /><meshBasicMaterial color={new THREE.Color(3, 2.4, 1.5)} toneMapped={false} /></mesh>
        </group>
      ))}
      {/* the dumbbell the hero drops */}
      {dropY !== null && <group position={[0.42 + Math.min(dt, 40) * 0.006, 0, 0.3 + Math.min(dt, 40) * 0.004]}><Dumbbell p={[0, dropY, 0]} s={1.25} /></group>}
    </group>
  );
};
