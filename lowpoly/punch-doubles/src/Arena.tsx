// Boxing arena: ring with ropes and corner posts, tiered crowd, light rig with spotlight beams, camera flashes.
import React, { useEffect, useMemo, useRef } from "react";
import * as THREE from "three";
import { Glow, sat } from "./Scenes";

const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };
const RING = 3.2, H = 1.0;

const Crowd: React.FC<{ f: number; gone: number }> = ({ f, gone }) => {
  const N = 900, ref = useRef<THREE.InstancedMesh>(null);
  const geo = useMemo(() => new THREE.CapsuleGeometry(0.18, 0.45, 2, 6), []);
  const mat = useMemo(() => new THREE.MeshStandardMaterial({ roughness: 0.9, flatShading: true }), []);
  const seats = useMemo(() => Array.from({ length: N }, (_, i) => {
    const side = i % 4, row = Math.floor(rnd(i, 1) * 9), u = (rnd(i, 2) * 2 - 1) * (7 + row * 0.9), d = 7 + row * 1.0;
    const p = side === 0 ? [u, d] : side === 1 ? [u, -d] : side === 2 ? [d, u] : [-d, u];
    return { x: p[0], z: p[1], y: 0.6 + row * 0.55, c: new THREE.Color().setHSL(rnd(i, 3), 0.35, 0.25 + rnd(i, 4) * 0.25), ph: rnd(i, 5) * 6 };
  }), []);
  useEffect(() => { const m = ref.current!; seats.forEach((s, i) => m.setColorAt(i, s.c)); m.instanceColor!.needsUpdate = true; });
  useEffect(() => {
    const m = ref.current!, o = new THREE.Object3D();
    seats.forEach((s, i) => {
      const k = gone > 0 ? Math.max(0, 1 - gone * (0.6 + rnd(i, 6))) : 1;
      o.position.set(s.x, s.y + Math.abs(Math.sin(f * 0.25 + s.ph)) * 0.12 * (f % 200 < 120 ? 1 : 0.3), s.z); o.scale.setScalar(Math.max(0.001, k)); o.updateMatrix(); m.setMatrixAt(i, o.matrix);
    });
    m.instanceMatrix.needsUpdate = true;
  });
  return <instancedMesh ref={ref} args={[geo, mat, N]} />;
};

export const Arena: React.FC<{ f: number; blast?: number; ruin?: number }> = ({ f, blast = 0, ruin = 0 }) => {
  const ropeMat = useMemo(() => new THREE.MeshStandardMaterial({ color: "#e8e8f0", roughness: 0.4 }), []);
  const posts: [number, number, string][] = [[RING, RING, "#d81e2a"], [-RING, -RING, "#2a5ad8"], [RING, -RING, "#f0f0f0"], [-RING, RING, "#f0f0f0"]];
  const ropes = useMemo(() => { const out: { p: [number, number, number]; r: number; len: number }[] = []; for (const h of [0.45, 0.85, 1.25]) for (let s = 0; s < 4; s++) out.push({ p: s < 2 ? [0, H + h, s ? RING : -RING] : [s === 2 ? RING : -RING, H + h, 0], r: s < 2 ? 0 : Math.PI / 2, len: RING * 2 }); return out; }, []);
  const scorch = new THREE.Color("#7a8098").lerp(new THREE.Color("#1a1212"), ruin);
  return (
    <group>
      <color attach="background" args={[new THREE.Color("#07060c").lerp(new THREE.Color("#3a0c06"), ruin)]} />
      <fog attach="fog" args={[new THREE.Color("#07060c").lerp(new THREE.Color("#5a1808"), ruin), 14, 40]} />
      {/* floor of the hall */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow><planeGeometry args={[80, 80]} /><meshStandardMaterial color={ruin ? "#2a0e08" : "#14121c"} emissive={ruin ? "#ff4a10" : "#000"} emissiveIntensity={ruin * 0.08} /></mesh>
      {/* ring: base, apron skirt, canvas */}
      <mesh position={[0, H / 2, 0]} castShadow receiveShadow><boxGeometry args={[RING * 2 + 0.6, H, RING * 2 + 0.6]} /><meshStandardMaterial color="#1a1a28" roughness={0.8} /></mesh>
      <mesh position={[0, H + 0.01, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow><planeGeometry args={[RING * 2 + 0.6, RING * 2 + 0.6]} /><meshStandardMaterial color={scorch} roughness={0.9} /></mesh>
      <mesh position={[0, H + 0.015, 0]} rotation={[-Math.PI / 2, 0, 0]}><ringGeometry args={[0.9, 1.0, 40]} /><meshStandardMaterial color="#d81e2a" transparent opacity={1 - ruin} /></mesh>
      {posts.map(([x, z, c], i) => (
        <group key={i} position={[x, H, z]}>
          <mesh position={[0, 0.75, 0]} castShadow><cylinderGeometry args={[0.07, 0.07, 1.5, 8]} /><meshStandardMaterial color="#b8b8c8" metalness={0.7} roughness={0.3} /></mesh>
          <mesh position={[0, 0.85, 0]}><boxGeometry args={[0.22, 1.0, 0.22]} /><meshStandardMaterial color={c} roughness={0.5} /></mesh>
        </group>
      ))}
      {ruin < 0.5 && ropes.map((r, i) => <mesh key={i} position={r.p} rotation={[0, r.r, Math.PI / 2]} material={ropeMat}><cylinderGeometry args={[0.03, 0.03, r.len, 6]} /></mesh>)}
      {ruin < 0.5 && <Crowd f={f} gone={blast} />}
      {/* light rig */}
      {ruin < 0.5 && <group position={[0, 9, 0]}>
        <mesh><boxGeometry args={[7, 0.3, 7]} /><meshStandardMaterial color="#20202a" metalness={0.6} roughness={0.4} /></mesh>
        {[-2.5, 0, 2.5].flatMap(x => [-2.5, 2.5].map(z => <mesh key={x + "_" + z} position={[x, -0.2, z]}><boxGeometry args={[0.5, 0.15, 0.5]} /><meshBasicMaterial color={new THREE.Color(3, 2.8, 2.4)} toneMapped={false} /></mesh>))}
      </group>}
      {ruin < 0.5 && <mesh position={[0, 5, 0]}><coneGeometry args={[3.0, 8, 32, 1, true]} /><meshBasicMaterial color="#fff4dc" transparent opacity={0.025} depthWrite={false} side={THREE.DoubleSide} blending={THREE.AdditiveBlending} /></mesh>}
      {/* camera flashes in the crowd */}
      {ruin < 0.5 && blast < 0.2 && Array.from({ length: 14 }, (_, i) => { const on = (f + Math.floor(rnd(i, 1) * 60)) % 60 < 2; const a = rnd(i, 2) * 6.283, d = 8 + rnd(i, 3) * 7; return on ? <Glow key={i} size={0.9} color="#ffffff" opacity={0.9} pos={[Math.cos(a) * d, 1.5 + rnd(i, 4) * 4, Math.sin(a) * d]} /> : null; })}
      {/* embers in the ruined world */}
      {ruin > 0 && Array.from({ length: 70 }, (_, i) => { const y = ((rnd(i, 1) * 8 + f * (0.02 + rnd(i, 2) * 0.04)) % 8); return <mesh key={i} position={[(rnd(i, 3) - 0.5) * 16, y, (rnd(i, 4) - 0.5) * 16]}><boxGeometry args={[0.05, 0.05, 0.05]} /><meshBasicMaterial color={new THREE.Color(3, 1.2, 0.3)} toneMapped={false} /></mesh>; })}
      <ambientLight intensity={ruin ? 0.25 : 0.25} color={ruin ? "#ffa080" : "#8890c0"} />
      <spotLight position={[0, 9, 0]} angle={0.55} penumbra={0.5} intensity={ruin ? 20 : 45} distance={30} decay={1.2} castShadow shadow-mapSize={[1024, 1024]} color="#fff2dc" />
      <directionalLight position={[-6, 8, 6]} intensity={ruin ? 1.3 : 0.6} color={ruin ? "#ffc0a0" : "#a0b0ff"} />
      {ruin < 0.5 && <directionalLight position={[0, 3, 9]} intensity={0.9} color="#fff0e0" />}
      <directionalLight position={[6, 4, -6]} intensity={ruin ? 1.2 : 0.4} color="#80a0ff" />
      {ruin > 0 && <hemisphereLight args={["#ff9a70", "#200804", 0.35]} />}
    </group>
  );
};
