import React, { useMemo } from "react";
import * as THREE from "three";
import { Surroundings } from "./env";

const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };
export const sat = (v: number) => Math.min(1, Math.max(0, v));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const ease = (t: number) => { t = sat(t); return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };

const glowTex = (() => { let t: THREE.CanvasTexture | null = null; return () => { if (t) return t; const c = document.createElement("canvas"); c.width = c.height = 128; const g = c.getContext("2d")!, gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(0.3, "rgba(255,255,255,.45)"); gr.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); t = new THREE.CanvasTexture(c); return t; }; })();
export const Glow: React.FC<{ size: number; color: THREE.Color | string; opacity: number; pos?: [number, number, number] }> = ({ size, color, opacity, pos = [0, 0, 0] }) =>
  <sprite position={pos} scale={[size, size, 1]}><spriteMaterial map={glowTex()} color={color} transparent opacity={opacity} blending={THREE.AdditiveBlending} depthWrite={false} toneMapped={false} /></sprite>;

const Stars: React.FC<{ n?: number }> = ({ n = 900 }) => {
  const geo = useMemo(() => { const p = new Float32Array(n * 3); for (let i = 0; i < n; i++) { const u = rnd(i, 1) * 2 - 1, th = rnd(i, 2) * 6.283, s = Math.sqrt(1 - u * u); p.set([Math.cos(th) * s * 150, u * 150, Math.sin(th) * s * 150], i * 3); } const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.BufferAttribute(p, 3)); return g; }, [n]);
  return <points geometry={geo}><pointsMaterial color="#ffffff" size={1.8} sizeAttenuation={false} /></points>;
};

// the teaspoon: silver spoon with a scoop of blinding neutron matter
export const Spoon: React.FC<{ pos: [number, number, number]; s: number; f: number; heat?: number }> = ({ pos, s, f, heat = 1 }) => (
  <group position={pos} scale={s} rotation={[0.35, f * 0.03, 0.2]}>
    <mesh position={[0, 0, -0.55]} rotation={[Math.PI / 2, 0, 0]}><cylinderGeometry args={[0.035, 0.05, 0.9, 6]} /><meshStandardMaterial color="#d8dce8" metalness={0.8} roughness={0.25} flatShading /></mesh>
    <mesh scale={[1, 0.38, 1.35]}><sphereGeometry args={[0.2, 12, 8, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2]} /><meshStandardMaterial color="#d8dce8" metalness={0.8} roughness={0.25} flatShading side={THREE.DoubleSide} /></mesh>
    <mesh position={[0, 0.02, 0]} scale={[1, 0.35, 1.3]}><icosahedronGeometry args={[0.16, 1]} /><meshBasicMaterial color={new THREE.Color(2.2, 2.6, 4).multiplyScalar(heat)} toneMapped={false} /></mesh>
    <Glow size={1.6 * heat} color="#8ab8ff" opacity={0.9} pos={[0, 0.05, 0]} />
  </group>
);

// ---------- the city at blue hour, with the blast ----------
export const BlastCity: React.FC<{ f: number; boom: number; spoonIn: number }> = ({ f, boom, spoonIn }) => {
  const t = f - boom, fire = sat(t / 50), shock = t > 0 ? t * 1.6 : -1;
  const fb = useMemo(() => { const g = new THREE.IcosahedronGeometry(1, 3); const p = g.attributes.position; for (let i = 0; i < p.count; i++) { const v = new THREE.Vector3(p.getX(i), p.getY(i), p.getZ(i)); v.multiplyScalar(1 + (rnd(i, 4) - 0.5) * 0.18); p.setXYZ(i, v.x, v.y, v.z); } g.computeVertexNormals(); return g; }, []);
  const R = t < 0 ? 0 : 4 + Math.pow(fire, 0.6) * 18;
  const sky = new THREE.Color("#1a2a5a").lerp(new THREE.Color("#ff8a4a"), t > 0 ? sat(1 - (t - 10) / 120) * 0.8 : 0);
  return (
    <group>
      <color attach="background" args={[sky]} />
      <fog attach="fog" args={[sky, 80, 380]} />
      <Surroundings f={f} glow={0.9} day={0.25} sunDir={new THREE.Vector3(-10, -2, -20)} />
      {f >= spoonIn && t < 4 && <Spoon pos={[0, lerp(40, 14, ease((f - spoonIn) / (boom - spoonIn))), 0]} s={6} f={f} heat={1 + Math.max(0, f - boom + 8) * 0.4} />}
      {t >= 0 && (
        <group>
          <mesh geometry={fb} position={[0, R * 0.55, 0]} scale={[R, R * 0.92, R]} rotation={[0, t * 0.01, 0]}>
            <meshBasicMaterial color={new THREE.Color(3.2, 1.7, 0.6).lerp(new THREE.Color(1.1, 0.3, 0.1), fire)} toneMapped={false} transparent opacity={0.95} />
          </mesh>
          <mesh geometry={fb} position={[0, R * 0.55, 0]} scale={[R * 1.15, R * 1.05, R * 1.15]}>
            <meshBasicMaterial color={new THREE.Color(3, 1.2, 0.4)} toneMapped={false} transparent opacity={0.25} depthWrite={false} />
          </mesh>
          <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.4, 0]}><ringGeometry args={[Math.max(0.1, shock - 3), shock, 64]} /><meshBasicMaterial color={new THREE.Color(3.5, 2.6, 1.6)} toneMapped={false} transparent opacity={sat(1 - t / 90)} side={THREE.DoubleSide} depthWrite={false} /></mesh>
          {Array.from({ length: 50 }, (_, i) => { const a = rnd(i, 1) * 6.283, sp = 0.5 + rnd(i, 2), u = t * sp; return <mesh key={i} position={[Math.cos(a) * u * 0.9, Math.max(0, u * (0.8 + rnd(i, 3)) - u * u * 0.004), Math.sin(a) * u * 0.9]}><boxGeometry args={[0.8, 0.8, 0.8]} /><meshBasicMaterial color={new THREE.Color(2.5, 1.0, 0.3)} toneMapped={false} /></mesh>; })}
          <pointLight position={[0, R * 0.5, 0]} intensity={700 * sat(1 - t / 160)} distance={600} decay={1.2} color="#ffb070" />
        </group>
      )}
      <hemisphereLight args={["#5a6ab8", "#1a1424", 0.6]} />
      <directionalLight position={[-20, 30, 20]} intensity={0.6} color="#a8b8ff" />
    </group>
  );
};

// ---------- a giant star collapses into a city-sized neutron star ----------
export const StarCollapse: React.FC<{ f: number; collapse: number }> = ({ f, collapse }) => {
  const t = f - collapse, shrink = sat(t / 10), post = t > 10;
  const R = lerp(6, 0.35, ease(shrink));
  const geo = useMemo(() => { const g = new THREE.IcosahedronGeometry(1, 4).toNonIndexed(); const p = g.attributes.position, col = new Float32Array(p.count * 3); for (let i = 0; i < p.count; i += 3) { const x = p.getX(i), y = p.getY(i), z = p.getZ(i); const n = 0.5 + 0.5 * Math.sin(x * 7 + Math.sin(y * 5) * 2) * Math.cos(z * 6 + x * 3); const k = 0.55 + n * 0.6 + rnd(i, 9) * 0.15; for (let j = 0; j < 3; j++) col.set([k, k, k], (i + j) * 3); } g.setAttribute("color", new THREE.BufferAttribute(col, 3)); return g; }, []);
  const city = useMemo(() => Array.from({ length: 70 }, (_, i) => { const a = rnd(i, 1) * 6.283, r = Math.sqrt(rnd(i, 2)) * 0.33; return [Math.cos(a) * r, rnd(i, 3) * 0.06 + 0.01, Math.sin(a) * r] as [number, number, number]; }), []);
  const cityIn = ease((t - 40) / 20);
  return (
    <group>
      <color attach="background" args={["#04030c"]} />
      <Stars />
      {!post && <mesh geometry={geo} scale={R} rotation={[f * 0.004, f * 0.006, 0]}><meshBasicMaterial vertexColors color={new THREE.Color(1.25, 0.24, 0.05).lerp(new THREE.Color(3.5, 3.0, 2.5), shrink)} toneMapped={false} /></mesh>}
      {!post && <Glow size={R * 2.4} color="#ff5a2a" opacity={0.35} />}
      {t >= 8 && t < 40 && <mesh scale={(t - 8) * 0.9}><sphereGeometry args={[1, 24, 16]} /><meshBasicMaterial color={new THREE.Color(3, 3, 4)} toneMapped={false} transparent opacity={sat(1 - (t - 8) / 30) * 0.6} side={THREE.BackSide} depthWrite={false} /></mesh>}
      {post && <group>
        <mesh scale={0.35}><sphereGeometry args={[1, 24, 16]} /><meshBasicMaterial color={new THREE.Color(2.6, 3.0, 4.2)} toneMapped={false} /></mesh>
        <Glow size={2.2} color="#8ab8ff" opacity={0.9} />
        {[0, 1].map(k => <mesh key={k} rotation={[0.3 + k * 1.3, f * 0.05 * (k ? -1 : 1), 0]}><torusGeometry args={[0.6 + k * 0.25, 0.008, 4, 64]} /><meshBasicMaterial color={new THREE.Color(1.5, 2.2, 4)} toneMapped={false} transparent opacity={0.6} /></mesh>)}
      </group>}
      {post && cityIn > 0 && <group position={[1.15, -0.25, 0]} scale={cityIn}>
        <mesh rotation={[-Math.PI / 2, 0, 0]}><circleGeometry args={[0.36, 28]} /><meshStandardMaterial color="#3a4a6a" /></mesh>
        {city.map((p, i) => <mesh key={i} position={[p[0], p[1] / 2, p[2]]}><boxGeometry args={[0.035, p[1], 0.035]} /><meshStandardMaterial color="#c8d0e8" emissive="#ffd890" emissiveIntensity={rnd(i, 5) > 0.5 ? 0.8 : 0} /></mesh>)}
      </group>}
      <ambientLight intensity={0.6} /><directionalLight position={[2, 3, 4]} intensity={1.5} />
    </group>
  );
};

// ---------- the scale: one teaspoon balances a mountain of 8 billion people ----------
export const Seesaw: React.FC<{ f: number; l: number }> = ({ f, l }) => {
  const people = useMemo(() => { const out: [number, number, number, string][] = []; for (let i = 0; i < 420; i++) { const r = Math.pow(rnd(i, 1), 0.7) * 1.7, a = rnd(i, 2) * 6.283, h = Math.max(0, 1.9 * (1 - r / 1.75)) * rnd(i, 3); out.push([Math.cos(a) * r, h, Math.sin(a) * r * 0.6, ["#e8603a", "#3a8ae8", "#e8c83a", "#3ac08a", "#c060e0", "#f0f0f0"][i % 6]]); } return out; }, []);
  const n = Math.floor(lerp(20, 420, ease(l / 70)));
  const tilt = lerp(0.3, 0, ease((l - 30) / 50)) + Math.sin(l * 0.2) * 0.01 * sat((l - 70) / 10);
  return (
    <group>
      <color attach="background" args={["#14102a"]} />
      <Stars n={400} />
            <mesh position={[0, -0.9, 0]}><coneGeometry args={[0.6, 1.4, 4]} /><meshStandardMaterial color="#6a6a8a" flatShading /></mesh>
      <group position={[0, -0.2, 0]} rotation={[0, 0, tilt]}>
        <mesh><boxGeometry args={[6.6, 0.12, 1.0]} /><meshStandardMaterial color="#b88a5a" flatShading /></mesh>
        <Spoon pos={[-2.7, 0.3, 0]} s={2.2} f={0} />
        <group position={[2.2, 0.06, 0]} scale={0.75}>
          {people.slice(0, n).map((p, i) => <mesh key={i} position={[p[0], p[1] + 0.12, p[2]]} rotation={[0, rnd(i, 7) * 6, rnd(i, 8) * 0.6 - 0.3]}><capsuleGeometry args={[0.055, 0.12, 2, 5]} /><meshStandardMaterial color={p[3]} flatShading /></mesh>)}
        </group>
      </group>
      <ambientLight intensity={0.7} /><directionalLight position={[3, 6, 5]} intensity={2.2} /><pointLight position={[-2.7, 1, 1]} intensity={8} distance={5} color="#8ab8ff" />
    </group>
  );
};

// ---------- Earth with a wedge cut out: the "it would sink to the core" myth ----------
export const EarthCut: React.FC<{ f: number; l: number }> = ({ f, l }) => {
  const layers: [number, string][] = [[3, "#3a7ad8"], [2.75, "#d8603a"], [1.6, "#ff9a3a"], [0.75, "#fff0a0"]];
  const sink = ease((l - 20) / 70), y = lerp(3.1, 0, sink) + (l > 90 ? Math.sin((l - 90) * 0.15) * 0.25 : 0);
  return (
    <group>
      <color attach="background" args={["#04030c"]} />
      <Stars />
      <group>
        {layers.map(([r, c], i) => (
          <mesh key={i}><sphereGeometry args={[r, 32, 20, Math.PI * 0.5, Math.PI * 1.5]} /><meshStandardMaterial color={c} emissive={i > 1 ? c : "#000"} emissiveIntensity={i > 1 ? 0.6 : 0} flatShading side={THREE.DoubleSide} /></mesh>
        ))}
        <mesh><sphereGeometry args={[3.01, 32, 20, Math.PI * 0.5, Math.PI * 1.5]} /><meshStandardMaterial color="#3aa04a" transparent opacity={0.35} flatShading /></mesh>
        <group position={[0, y, 0]}><mesh scale={0.07}><sphereGeometry args={[1, 10, 8]} /><meshBasicMaterial color={new THREE.Color(2.6, 3, 4)} toneMapped={false} /></mesh><Glow size={0.7} color="#8ab8ff" opacity={1} /></group>
        {l > 20 && <mesh position={[0, (3.1 + y) / 2, 0]}><cylinderGeometry args={[0.02, 0.02, Math.max(0.01, 3.1 - y), 6]} /><meshBasicMaterial color={new THREE.Color(1.5, 2, 3)} toneMapped={false} transparent opacity={0.6} /></mesh>}
      </group>
      <ambientLight intensity={0.6} /><directionalLight position={[4, 5, 6]} intensity={2.2} />
    </group>
  );
};

// ---------- Earth from orbit with the blast spreading ----------
export const EarthBlast: React.FC<{ f: number; t: number }> = ({ f, t }) => {
  const geo = useMemo(() => { const g = new THREE.IcosahedronGeometry(3, 4).toNonIndexed(); const p = g.attributes.position, col = new Float32Array(p.count * 3); for (let i = 0; i < p.count; i += 3) { const x = p.getX(i), y = p.getY(i), z = p.getZ(i); const land = Math.sin(x * 1.3 + Math.sin(z * 0.9) * 2) * Math.cos(y * 1.5 + x * 0.4) > 0.15; const c = new THREE.Color(Math.abs(y) > 2.6 ? "#f0f4ff" : land ? "#4aa04a" : "#2a6ad8"); for (let k = 0; k < 3; k++) col.set([c.r, c.g, c.b], (i + k) * 3); } g.setAttribute("color", new THREE.BufferAttribute(col, 3)); return g; }, []);
  const spot = new THREE.Vector3(0.4, 1.2, 2.7).normalize().multiplyScalar(3.02), q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 0, 1), spot.clone().normalize());
  const r = 0.15 + Math.pow(sat(t / 140), 0.6) * 1.5;
  return (
    <group>
      <color attach="background" args={["#020208"]} />
      <Stars />
      <group rotation={[0.25, -0.12 - Math.max(0, t) * 0.0009, 0]}>
        <mesh geometry={geo}><meshStandardMaterial vertexColors flatShading roughness={0.9} /></mesh>
        <mesh scale={1.04}><sphereGeometry args={[3, 32, 20]} /><meshBasicMaterial color="#6ab8ff" transparent opacity={0.12} side={THREE.BackSide} /></mesh>
        <group position={spot} quaternion={q}>
          <mesh position={[0, 0, 0.02]}><circleGeometry args={[r * 0.55, 32]} /><meshBasicMaterial color={new THREE.Color(2.2, 0.9, 0.25)} toneMapped={false} transparent opacity={0.85} /></mesh>
          <mesh position={[0, 0, 0.03]}><ringGeometry args={[r * 0.9, r, 48]} /><meshBasicMaterial color={new THREE.Color(1.8, 1.4, 1.1)} toneMapped={false} transparent opacity={0.55} side={THREE.DoubleSide} /></mesh>
          <Glow size={r * 2} color="#ff7a2a" opacity={0.35} pos={[0, 0, 0.2]} />
        </group>
      </group>
      <ambientLight intensity={0.35} /><directionalLight position={[-5, 3, 6]} intensity={2.4} />
    </group>
  );
};
