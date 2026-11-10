// Inside the body: a blood vessel clogging with red cells, a racing heart, and aromatase turning testosterone into estrogen.
import React, { useLayoutEffect, useMemo, useRef } from "react";
import * as THREE from "three";

const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };
const sat = (v: number) => Math.min(1, Math.max(0, v));

// biconcave red blood cell
const rbcGeo = (() => {
  const pts: THREE.Vector2[] = [];
  for (let i = 0; i <= 10; i++) { const r = i / 10 * 0.1; const h = 0.012 + 0.03 * Math.pow(i / 10, 2) * (1 - Math.pow(i / 10, 6)); pts.push(new THREE.Vector2(r, h)); }
  for (let i = 10; i >= 0; i--) { const r = i / 10 * 0.1; const h = 0.012 + 0.03 * Math.pow(i / 10, 2) * (1 - Math.pow(i / 10, 6)); pts.push(new THREE.Vector2(r, -h)); }
  return new THREE.LatheGeometry(pts, 14);
})();

export const Vessel: React.FC<{ f: number; t0: number; t1: number }> = ({ f, t0, t1 }) => {
  const u = sat((f - t0) / (t1 - t0));
  const N = 520, ref = useRef<THREE.InstancedMesh>(null);
  const wall = useMemo(() => {
    const g = new THREE.CylinderGeometry(1, 1, 60, 18, 30, true).toNonIndexed(); g.rotateX(Math.PI / 2);
    const p = g.attributes.position, col = new Float32Array(p.count * 3);
    for (let i = 0; i < p.count; i++) { const k = 1 + (rnd(i, 1) - 0.5) * 0.06; p.setX(i, p.getX(i) * k); p.setY(i, p.getY(i) * k); }
    for (let i = 0; i < p.count; i += 3) { const c = new THREE.Color("#a8243a").lerp(new THREE.Color("#e86a7a"), rnd(i, 2) * 0.5); for (let k = 0; k < 3; k++) col.set([c.r, c.g, c.b], (i + k) * 3); }
    g.setAttribute("color", new THREE.BufferAttribute(col, 3)); g.computeVertexNormals(); return g;
  }, []);
  const visible = Math.floor(lerpN(90, N, Math.pow(u, 0.8)));
  const speed = lerpN(0.09, 0.012, u); // the flow slows as it thickens
  useLayoutEffect(() => {
    const m = new THREE.Matrix4(), q = new THREE.Quaternion(), s = new THREE.Vector3();
    for (let i = 0; i < N; i++) {
      if (i >= visible) { m.makeScale(0, 0, 0); ref.current!.setMatrixAt(i, m); continue; }
      const a = rnd(i, 3) * Math.PI * 2, r = Math.sqrt(rnd(i, 4)) * 0.82;
      const z = ((rnd(i, 5) * 30 + (f - t0) * speed * (0.8 + rnd(i, 6) * 0.4)) % 30) - 26;
      q.setFromEuler(new THREE.Euler(rnd(i, 7) * 6 + f * 0.02 * rnd(i, 8), rnd(i, 9) * 6, 0)); s.setScalar(1.4 + rnd(i, 10) * 0.3);
      m.compose(new THREE.Vector3(Math.cos(a) * r, Math.sin(a) * r, z), q, s); ref.current!.setMatrixAt(i, m);
    }
    ref.current!.instanceMatrix.needsUpdate = true;
  });
  return (
    <group>
      <color attach="background" args={["#2a0610"]} />
      <fog attach="fog" args={["#3a0814", 2, 22]} />
      <ambientLight intensity={0.5} color="#ff9090" />
      <pointLight position={[0, 0.3, 1.2]} intensity={14} distance={14} decay={1.4} color="#ffd0c0" />
      <mesh geometry={wall}><meshStandardMaterial vertexColors side={THREE.BackSide} flatShading roughness={0.6} /></mesh>
      <instancedMesh ref={ref} args={[rbcGeo, RBC_MAT, N]} frustumCulled={false} />
    </group>
  );
};
const RBC_MAT = new THREE.MeshStandardMaterial({ color: "#d8202e", roughness: 0.35, flatShading: true });
const lerpN = (a: number, b: number, t: number) => a + (b - a) * t;

// low-poly heart: two lobes, a tapered bottom, aorta and vessels; beats faster and faster
export const Heart: React.FC<{ f: number; bpm: number }> = ({ f, bpm }) => {
  const ph = (f / 30) * (bpm / 60), beat = Math.pow(Math.max(0, Math.sin(ph * Math.PI * 2)), 6) + 0.6 * Math.pow(Math.max(0, Math.sin(ph * Math.PI * 2 - 0.9)), 8);
  const s = 1 + beat * 0.09;
  return (
    <group>
      <color attach="background" args={["#14060c"]} />
      <ambientLight intensity={0.4} color="#ff8a8a" />
      <directionalLight position={[2, 3, 4]} intensity={2.4} color="#ffe0d0" />
      <pointLight position={[-2, -1, 2]} intensity={6} distance={10} color="#ff4a6a" />
      <group scale={[s, s, s]} rotation={[0.1, -0.4, 0.25]}>
        {[-1, 1].map(k => <mesh key={k} position={[k * 0.32, 0.25, 0]} castShadow><icosahedronGeometry args={[0.5, 1]} /><meshStandardMaterial color="#c8283a" flatShading roughness={0.45} /></mesh>)}
        <mesh position={[0, -0.35, 0]} rotation={[Math.PI, 0, 0]}><coneGeometry args={[0.72, 1.1, 8]} /><meshStandardMaterial color="#b8202e" flatShading roughness={0.45} /></mesh>
        <mesh position={[0.15, 0.85, -0.05]} rotation={[0, 0, -0.3]}><cylinderGeometry args={[0.16, 0.2, 0.6, 8]} /><meshStandardMaterial color="#d8606a" flatShading roughness={0.5} /></mesh>
        <mesh position={[0.32, 1.15, -0.05]} rotation={[0, 0, Math.PI / 2]}><torusGeometry args={[0.2, 0.12, 6, 10, Math.PI]} /><meshStandardMaterial color="#d8606a" flatShading roughness={0.5} /></mesh>
        <mesh position={[-0.25, 0.8, -0.15]} rotation={[0, 0, 0.3]}><cylinderGeometry args={[0.12, 0.15, 0.5, 8]} /><meshStandardMaterial color="#5a6ab8" flatShading roughness={0.5} /></mesh>
        {[0, 1, 2].map(i => <mesh key={i} position={[-0.3 + i * 0.25, 0.1 - i * 0.25, 0.47]} rotation={[0, 0, 0.6 + i * 0.3]}><cylinderGeometry args={[0.025, 0.025, 0.5, 5]} /><meshStandardMaterial color="#e8d050" flatShading /></mesh>)}
      </group>
    </group>
  );
};

// steroid skeleton: three hexagons + a pentagon, atoms as balls; T = blue, E = pink (with an aromatic A ring)
const steroidPts = (() => {
  const hex = (cx: number, cy: number) => Array.from({ length: 6 }, (_, i) => new THREE.Vector2(cx + Math.cos(i * Math.PI / 3 + Math.PI / 6) * 0.3, cy + Math.sin(i * Math.PI / 3 + Math.PI / 6) * 0.3));
  const rings = [hex(-0.52, -0.15), hex(0, 0.15), hex(0.52, -0.15)];
  const pent = Array.from({ length: 5 }, (_, i) => new THREE.Vector2(0.98 + Math.cos(i * 2 * Math.PI / 5 + Math.PI) * 0.27, 0.12 + Math.sin(i * 2 * Math.PI / 5 + Math.PI) * 0.27));
  return [...rings, pent];
})();
const Molecule: React.FC<{ p: THREE.Vector3; rot: number; e: number }> = ({ p, rot, e }) => {
  const col = new THREE.Color("#4aa8ff").lerp(new THREE.Color("#ff6ab8"), e), atom = new THREE.Color("#d8ecff").lerp(new THREE.Color("#ffd8ec"), e);
  return (
    <group position={p} rotation={[0.3, rot, 0.1]} scale={0.8}>
      {steroidPts.map((ring, ri) => ring.map((a, i) => {
        const b = ring[(i + 1) % ring.length], mid = a.clone().add(b).multiplyScalar(0.5), ang = Math.atan2(b.y - a.y, b.x - a.x);
        return <mesh key={`${ri}-${i}`} position={[mid.x, mid.y, 0]} rotation={[0, 0, ang - Math.PI / 2]}><cylinderGeometry args={[0.035, 0.035, a.distanceTo(b), 5]} /><meshStandardMaterial color={col} flatShading roughness={0.4} emissive={col} emissiveIntensity={0.25} /></mesh>;
      }))}
      {steroidPts.flat().map((a, i) => <mesh key={i} position={[a.x, a.y, 0]}><icosahedronGeometry args={[0.065, 1]} /><meshStandardMaterial color={atom} flatShading roughness={0.3} /></mesh>)}
      {e > 0.5 && <mesh position={[-0.52, -0.15, 0]} rotation={[Math.PI / 2, 0, 0]}><torusGeometry args={[0.17, 0.025, 5, 16]} /><meshStandardMaterial color="#ffffff" emissive="#ff9ad0" emissiveIntensity={1.5} /></mesh>}
    </group>
  );
};

export const Molecules: React.FC<{ f: number; t0: number }> = ({ f, t0 }) => {
  const l = f - t0, mouth = 0.35 + 0.25 * Math.abs(Math.sin(l * 0.18));
  const blob = useMemo(() => { const g = new THREE.IcosahedronGeometry(0.9, 2); const p = g.attributes.position; for (let i = 0; i < p.count; i++) { const v = new THREE.Vector3(p.getX(i), p.getY(i), p.getZ(i)); v.multiplyScalar(1 + (rnd(i, 3) - 0.5) * 0.12); p.setXYZ(i, v.x, v.y, v.z); } g.computeVertexNormals(); return g; }, []);
  const count = Math.min(14, 3 + Math.floor(l / 10));
  return (
    <group>
      <color attach="background" args={["#0c0a24"]} />
      <ambientLight intensity={0.5} color="#8a8aff" />
      <directionalLight position={[2, 3, 5]} intensity={2.2} />
      <pointLight position={[0, 0, 2]} intensity={10} distance={8} color="#c86aff" />
      {/* bokeh specks */}
      {Array.from({ length: 40 }, (_, i) => <mesh key={i} position={[(rnd(i, 1) - 0.5) * 12, (rnd(i, 2) - 0.5) * 18, -6 - rnd(i, 3) * 6]}><sphereGeometry args={[0.05 + rnd(i, 4) * 0.1, 6, 4]} /><meshBasicMaterial color={new THREE.Color(rnd(i, 5) > 0.5 ? "#6a8aff" : "#ff6ab8").multiplyScalar(1.5)} toneMapped={false} /></mesh>)}
      {/* aromatase enzyme: a purple blob with a chomping mouth */}
      <group rotation={[0, 0, 0]}>
        <mesh geometry={blob} scale={[1, 1 - mouth * 0.25, 0.9]}><meshStandardMaterial color="#8a4ad8" flatShading roughness={0.5} /></mesh>
        <mesh position={[0, 0, 0.62]} scale={[1, mouth, 1]}><sphereGeometry args={[0.32, 10, 6]} /><meshStandardMaterial color="#2a0a3a" flatShading /></mesh>
        {[-1, 1].map(k => <mesh key={k} position={[k * 0.3, 0.42, 0.7]}><icosahedronGeometry args={[0.09, 1]} /><meshStandardMaterial color="#ffffff" /></mesh>)}
      </group>
      {/* conveyor: blue T from above → into the enzyme → pink E out below */}
      {Array.from({ length: count }, (_, i) => {
        const u = ((l * 0.012 + i / count) % 1);
        const y = 4.2 - u * 8.4, e = y < 0 ? 1 : 0, x = Math.sin(u * 7 + i) * 0.9 * Math.min(1, Math.abs(y) / 1.5);
        const shrink = Math.min(1, Math.abs(y) / 0.9);
        return <Molecule key={i} p={new THREE.Vector3(x, y, 0.2 + rnd(i, 9) * 0.4)} rot={l * 0.03 + i} e={e} />;
      }).map((el, i) => <group key={i} scale={1}>{el}</group>)}
    </group>
  );
};
