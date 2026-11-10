// The twist: "local sleep". A low-poly brain made of cells; patches switch off (go dark blue) while the rest stays active.
import React, { useLayoutEffect, useMemo, useRef } from "react";
import * as THREE from "three";

const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };
const CELLS = (() => {
  const out: THREE.Vector3[] = [];
  for (const side of [-1, 1]) for (let i = 0; i < 150; i++) {   // two hemispheres (fibonacci points on ellipsoids)
    const y = 1 - (i + 0.5) / 150 * 2, r = Math.sqrt(1 - y * y), a = i * 2.39996;
    const p = new THREE.Vector3(Math.cos(a) * r * 0.52, y * 0.62, Math.sin(a) * r * 0.85).multiplyScalar(1 + (rnd(i, 3) - 0.5) * 0.1);
    if (side * p.x < -0.2) continue;              // flatten the inner face
    p.x += side * 0.43; if (p.y < -0.42) continue; out.push(p);
  }
  for (let i = 0; i < 26; i++) { const y = 1 - (i + 0.5) / 26 * 2, r = Math.sqrt(1 - y * y), a = i * 2.39996; out.push(new THREE.Vector3(Math.cos(a) * r * 0.42, y * 0.26 - 0.62, Math.sin(a) * r * 0.36 - 0.5)); }  // cerebellum
  for (let i = 0; i < 6; i++) out.push(new THREE.Vector3(0, -0.6 - i * 0.12, -0.12 + i * 0.02));   // stem
  return out;
})();
// sleep patches: centre, start (0..1 of the scene), final radius
const PATCH: [THREE.Vector3, number, number][] = [
  [new THREE.Vector3(-0.7, 0.35, 0.45), 0.12, 0.42], [new THREE.Vector3(0.75, 0.1, -0.5), 0.3, 0.46], [new THREE.Vector3(0.5, 0.5, 0.6), 0.48, 0.4],
  [new THREE.Vector3(-0.6, -0.1, -0.6), 0.62, 0.5], [new THREE.Vector3(0, 0.6, 0), 0.78, 0.45],
];
export const asleepFraction = (u: number) => CELLS.filter(p => PATCH.some(([c, s, r]) => u > s && p.distanceTo(c) < r * Math.min(1, (u - s) / 0.1))).length / CELLS.length;

export const Brain: React.FC<{ f: number; u: number }> = ({ f, u }) => {
  const ref = useRef<THREE.InstancedMesh>(null);
  const res = useMemo(() => ({ geo: new THREE.IcosahedronGeometry(0.105, 0), mat: new THREE.MeshStandardMaterial({ flatShading: true, roughness: 0.5 }) }), []);
  useLayoutEffect(() => {
    const im = ref.current!, m = new THREE.Matrix4(), q = new THREE.Quaternion(), c = new THREE.Color();
    CELLS.forEach((p, i) => {
      let sl = 0; for (const [pc, s, r] of PATCH) if (u > s) sl = Math.max(sl, THREE.MathUtils.clamp((r * Math.min(1, (u - s) / 0.1) - p.distanceTo(pc)) / 0.08 + 0.5, 0, 1));
      const act = 0.75 + 0.25 * Math.sin(f * 0.35 + i * 1.7) * (rnd(i, 5) > 0.5 ? 1 : 0.4);
      c.setRGB(1.5 * act, 0.55 * act, 0.7 * act).lerp(new THREE.Color(0.05, 0.08, 0.3), sl);
      q.setFromEuler(new THREE.Euler(rnd(i, 6) * 6, rnd(i, 7) * 6, 0));
      m.compose(p, q, new THREE.Vector3(1, 1, 1).multiplyScalar(1 - sl * 0.18)); im.setMatrixAt(i, m); im.setColorAt(i, c);
    });
    im.instanceMatrix.needsUpdate = true; if (im.instanceColor) im.instanceColor.needsUpdate = true;
  });
  return (
    <group>
      <color attach="background" args={["#07061a"]} />
      <ambientLight intensity={0.9} color="#b0a0ff" />
      <directionalLight position={[2, 3, 4]} intensity={2.4} color="#fff0f0" />
      <pointLight position={[-2, -1, 2]} intensity={8} distance={8} color="#6a5aff" />
      {Array.from({ length: 50 }, (_, i) => <mesh key={i} position={[(rnd(i, 1) - 0.5) * 9, (rnd(i, 2) - 0.5) * 14, -4 - rnd(i, 3) * 5]}><sphereGeometry args={[0.03 + rnd(i, 4) * 0.05, 6, 4]} /><meshBasicMaterial color={new THREE.Color(rnd(i, 5) > 0.5 ? "#6a8aff" : "#ff8ab8").multiplyScalar(1.3)} toneMapped={false} /></mesh>)}
      <group rotation={[0.15, f * 0.012 - 0.6, 0]} scale={1.25}>
        <instancedMesh ref={ref} args={[res.geo, res.mat, CELLS.length]} frustumCulled={false} />
      </group>
    </group>
  );
};
