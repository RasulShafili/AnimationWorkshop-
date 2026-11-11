// The arena seen from outside at night: a big hall with a dome in the middle of the city.
// launch: frames since the opponent left through the roof (flies away at 45°).
import React from "react";
import * as THREE from "three";
import { Surroundings } from "./env";
import { Glow, sat } from "./Scenes";
import { Boxer } from "./Boxer";
import { GLTF } from "three/examples/jsm/loaders/GLTFLoader.js";

const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };

export const Hall: React.FC<{ hole?: number }> = ({ hole = 0 }) => (
  <group>
    <mesh position={[0, 5, 0]} castShadow receiveShadow><boxGeometry args={[26, 10, 20]} /><meshStandardMaterial color="#3a4058" roughness={0.7} flatShading /></mesh>
    <mesh position={[0, 10, 0]} scale={[13, 5, 10]}><sphereGeometry args={[1, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2]} /><meshStandardMaterial color="#c8ccd8" metalness={0.5} roughness={0.35} flatShading /></mesh>
    {/* lit window band and the name sign */}
    <mesh position={[0, 7.5, 10.02]}><planeGeometry args={[24, 1.2]} /><meshBasicMaterial color={new THREE.Color(2.2, 1.8, 1.2)} toneMapped={false} /></mesh>
    <mesh position={[0, 3, 10.03]}><planeGeometry args={[8, 1.6]} /><meshBasicMaterial color={new THREE.Color(2.8, 0.4, 0.3)} toneMapped={false} /></mesh>
    {hole > 0 && <mesh position={[2, 14.6, 0]} rotation={[-Math.PI / 2, 0, 0]}><circleGeometry args={[1.6 * hole, 16]} /><meshBasicMaterial color={new THREE.Color(3, 2.6, 2)} toneMapped={false} /></mesh>}
  </group>
);

export const Exterior: React.FC<{ f: number; g: GLTF; launch: number }> = ({ f, g, launch }) => {
  const k = launch, x = 2 + k * 0.9, y = 15 + k * 0.9 - k * k * 0.004;
  return (
    <group>
      <color attach="background" args={["#141c3a"]} />
      <fog attach="fog" args={["#141c3a", 90, 380]} />
      <Surroundings f={f} glow={0.9} day={0.25} sunDir={new THREE.Vector3(-10, -2, -20)} />
      <Hall hole={k >= 0 ? 1 : 0} />
      {k >= 0 && <group>
        <group position={[x, y, 0]} rotation={[0, 0, -k * 0.25]}><Boxer g={g} pose={{ clip: "Death", t: 1.0 }} pos={[0, -0.9, 0]} ry={0} shorts="#2a5ad8" glove="#2a5ad8" skin="#a87050" /></group>
        <Glow size={6} color="#ffd8a0" opacity={0.5} pos={[x, y, 0]} />
        {/* streak from the roof to the flying man */}
        <mesh position={[(2 + x) / 2, (15 + y) / 2, 0]} rotation={[0, 0, Math.atan2(y - 15, x - 2) - Math.PI / 2]}><cylinderGeometry args={[0.15, 0.6, Math.hypot(x - 2, y - 15), 8]} /><meshBasicMaterial color={new THREE.Color(2.5, 2.2, 1.8)} toneMapped={false} transparent opacity={0.35} /></mesh>
        {Array.from({ length: 40 }, (_, i) => { const a = rnd(i, 1) * 6.283, sp = 0.2 + rnd(i, 2) * 0.5, u = k * sp; return <mesh key={i} position={[2 + Math.cos(a) * u * 0.5 + u * 0.4, 15 + u * (0.6 + rnd(i, 3)) - u * u * 0.01, Math.sin(a) * u * 0.5]} rotation={[k * 0.2, k * 0.3, 0]}><boxGeometry args={[0.6, 0.15, 0.6]} /><meshStandardMaterial color="#c8ccd8" metalness={0.5} roughness={0.4} /></mesh>; })}
      </group>}
      <hemisphereLight args={["#5a6ab8", "#1a1424", 0.7]} />
      <directionalLight position={[-20, 30, 20]} intensity={0.8} color="#a8b8ff" />
    </group>
  );
};

// a beam of light from the glove: along +x from origin, grows to `len`
export const Beam: React.FC<{ len: number; w: number; pos: [number, number, number]; rot?: [number, number, number]; o?: number }> = ({ len, w, pos, rot = [0, 0, 0], o = 1 }) => (
  <group position={pos} rotation={rot}>
    <mesh position={[len / 2, 0, 0]} rotation={[0, 0, Math.PI / 2]}><cylinderGeometry args={[w, w, len, 16, 1, true]} /><meshBasicMaterial color={new THREE.Color(3.5, 3.2, 4)} toneMapped={false} transparent opacity={o} /></mesh>
    <mesh position={[len / 2, 0, 0]} rotation={[0, 0, Math.PI / 2]}><cylinderGeometry args={[w * 2.6, w * 2.6, len, 16, 1, true]} /><meshBasicMaterial color={new THREE.Color(1.2, 1.6, 3.5)} toneMapped={false} transparent opacity={0.3 * o} depthWrite={false} blending={THREE.AdditiveBlending} /></mesh>
  </group>
);
