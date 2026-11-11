// The twist: caffeine (brown beans) plugs the adenosine receptors while adenosine (the "tired" signal, sleepy blue blobs) piles up;
// then the caffeine wears off and the whole pile floods in at once.
import React from "react";
import * as THREE from "three";

const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };
const sat = (v: number) => Math.min(1, Math.max(0, v));
const ease = (t: number) => { t = sat(t); return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
const SLOTS = Array.from({ length: 7 }, (_, i) => -1.5 + i * 0.5);

export const Synapse: React.FC<{ l: number; release: number; total: number }> = ({ l, release, total }) => {
  const pile = Math.min(60, Math.floor(8 + l * 0.55)), rel = sat((l - release) / 12), flood = ease((l - release - 8) / 22);
  return (
    <group>
      <color attach="background" args={["#160a12"]} />
      <ambientLight intensity={0.8} color="#ffc0a0" />
      <directionalLight position={[2, 4, 5]} intensity={2.2} color="#fff0e0" />
      <pointLight position={[0, 1.5, 2]} intensity={10 * (1 - flood * 0.5)} distance={8} color="#ff9a6a" />
      <pointLight position={[0, -0.2, 1.5]} intensity={14 * flood} distance={6} color="#5a8aff" />
      {/* membrane */}
      <mesh position={[0, -1.25, -0.3]} rotation={[0, 0, Math.PI / 2]}><cylinderGeometry args={[1, 1, 5, 20, 1, false, 0, Math.PI]} /><meshStandardMaterial color="#e88a6a" flatShading roughness={0.6} side={THREE.DoubleSide} /></mesh>
      {SLOTS.map((x, i) => (
        <group key={i} position={[x, -0.32, 0.25]}>
          <mesh><cylinderGeometry args={[0.17, 0.13, 0.22, 10, 1, true]} /><meshStandardMaterial color={new THREE.Color("#3ac0b0").lerp(new THREE.Color("#5a8aff"), flood)} emissive="#3a6aff" emissiveIntensity={flood * 1.2} flatShading side={THREE.DoubleSide} /></mesh>
          <mesh position={[0, -0.11, 0]}><cylinderGeometry args={[0.13, 0.13, 0.02, 10]} /><meshStandardMaterial color="#2a8a80" flatShading /></mesh>
          {/* caffeine bean: sits in the slot, then pops out and flies away */}
          {rel < 1 && (
            <group position={[rel * (rnd(i, 1) - 0.5) * 3, 0.08 + rel * (1.2 + rnd(i, 2)), rel * 1.4]} rotation={[0.4 + rel * 4, i, 0]}>
              <mesh scale={[1, 0.62, 0.72]}><icosahedronGeometry args={[0.13, 1]} /><meshStandardMaterial color="#6a3a1a" flatShading roughness={0.5} /></mesh>
              <mesh rotation={[Math.PI / 2, 0, 0]} scale={[1, 0.75, 1]}><torusGeometry args={[0.09, 0.012, 4, 12, Math.PI]} /><meshStandardMaterial color="#2a1408" /></mesh>
            </group>
          )}
        </group>
      ))}
      {/* adenosine pile: grows while blocked, then rains into the slots */}
      {Array.from({ length: pile }, (_, i) => {
        const hx = (rnd(i, 3) - 0.5) * 3.4, hy = 0.5 + rnd(i, 4) * 1.6 + Math.sin(l * 0.07 + i) * 0.06, hz = 0.2 + (rnd(i, 5) - 0.5) * 0.6;
        const slot = SLOTS[i % SLOTS.length], target = new THREE.Vector3(slot + (rnd(i, 6) - 0.5) * 0.25, -0.2 + Math.floor(i / SLOTS.length) * 0.05, 0.28);
        const p = new THREE.Vector3(hx, hy, hz).lerp(target, flood);
        return (
          <group key={i} position={p}>
            <mesh><icosahedronGeometry args={[0.075, 1]} /><meshStandardMaterial color="#7aa8ff" emissive="#3a5aff" emissiveIntensity={0.3 + flood * 0.8} flatShading roughness={0.4} /></mesh>
            {[-1, 1].map(s => <mesh key={s} position={[s * 0.025, 0.01, 0.068]}><boxGeometry args={[0.022, 0.006, 0.004]} /><meshBasicMaterial color="#1a1a40" /></mesh>)}
          </group>
        );
      })}
    </group>
  );
};
