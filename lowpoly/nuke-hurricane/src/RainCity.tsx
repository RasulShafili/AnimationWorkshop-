// The coastal city at night under green radioactive rain: rain streaks, glowing puddles, lightning.
import React, { useEffect, useMemo, useRef } from "react";
import * as THREE from "three";
import { Surroundings } from "./env";
import { Glow } from "./Scenes";
import { SceneSky } from "./Hurricane";

const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };
export const RainCity: React.FC<{ f: number; green: number }> = ({ f, green }) => {
  const N = 2200;
  const m = useMemo(() => { const im = new THREE.InstancedMesh(new THREE.BoxGeometry(0.06, 2.2, 0.06), new THREE.MeshBasicMaterial({ transparent: true, opacity: 0.55, toneMapped: false }), N); im.frustumCulled = false; return im; }, []);
  const mat = m.material as THREE.MeshBasicMaterial;
  mat.color.setRGB(0.7 - green * 0.2, 0.8 + green * 1.4, 0.8 - green * 0.3);
  {
    const o = new THREE.Object3D();
    for (let i = 0; i < N; i++) {
      const y = 40 - ((rnd(i, 1) * 40 + f * (1.6 + rnd(i, 2) * 0.6)) % 40);
      o.position.set((rnd(i, 3) - 0.5) * 160, y, (rnd(i, 4) - 0.5) * 160 + 20); o.rotation.set(0, 0, 0.18); o.updateMatrix(); m.setMatrixAt(i, o.matrix);
    }
    m.instanceMatrix.needsUpdate = true;
  }
  const flash = [37, 101].some(p => (f % p) < 3) ? 1 : 0;
  const sky = new THREE.Color("#141a20").lerp(new THREE.Color("#16301a"), green).lerp(new THREE.Color("#a8c8b0"), flash * 0.5);
  return (
    <group>
      <SceneSky sky={"#" + sky.getHexString()} near={50} far={260} />
      <Surroundings f={f} glow={0.9} day={0.12} sunDir={new THREE.Vector3(-10, -2, -20)} />
      <primitive object={m} />
      {/* glowing puddles */}
      {Array.from({ length: 26 }, (_, i) => <mesh key={i} rotation={[-Math.PI / 2, 0, 0]} position={[(rnd(i, 5) - 0.5) * 90, 0.35, (rnd(i, 6) - 0.5) * 90]}><circleGeometry args={[1 + rnd(i, 7) * 2.5, 16]} /><meshBasicMaterial color={new THREE.Color(0.3, 1.6, 0.35).multiplyScalar(green * (0.6 + 0.4 * Math.sin(f * 0.1 + i)))} toneMapped={false} transparent opacity={0.8} /></mesh>)}
      <Glow size={140} color="#5aff6a" opacity={0.12 * green} pos={[0, 30, -40]} />
      <hemisphereLight args={["#6a8a7a", "#101418", 0.5 + flash]} />
      <directionalLight position={[-20, 30, 20]} intensity={0.5 + flash * 3} color="#c8e8d0" />
    </group>
  );
};
