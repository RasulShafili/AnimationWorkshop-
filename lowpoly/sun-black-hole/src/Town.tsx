// Ground level: a small low-poly seaside town at noon, the moment the sunlight stops, and the months after.
// Units: roughly metres / 2 (a house is ~2 units tall). Sea for z < -6.
import React, { useMemo } from "react";
import * as THREE from "three";
import { useThree } from "@react-three/fiber";
import T from "./timeline.json";
import { Glow, Stars, sat, lerp, ease } from "./Space";

const B = T.beats, DARK = T.dark;
const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };
const C = (h: string) => new THREE.Color(h);
const mixC = (a: string, b: string, t: number) => C(a).lerp(C(b), sat(t));
const M: React.FC<{ c: THREE.Color | string; e?: THREE.Color | string; ei?: number }> = ({ c, e = "#000000", ei = 0 }) => <meshStandardMaterial color={c} emissive={e} emissiveIntensity={ei} flatShading roughness={0.9} metalness={0} />;

export const wiltAt = (f: number) => ease((f - T.wilt[0]) / (T.wilt[1] - T.wilt[0]));
export const snowAt = (f: number) => sat((f - T.snow) / 160);
export const iceAt = (f: number) => ease((f - T.freeze[0]) / (T.freeze[1] - T.freeze[0]));

const HOUSES: [number, number, number, string, string][] = [
  [-4.6, -0.4, 0.15, "#e8d0a8", "#c0503a"], [-1.4, 0.1, -0.08, "#a8c8e8", "#5a4a8a"], [1.9, -0.5, 0.12, "#f0e0c0", "#3a7a5a"],
  [5.2, 0.2, -0.15, "#e8b8a0", "#8a3a3a"], [-7.8, -0.2, 0.3, "#d8d8c8", "#4a5a8a"], [8.4, -0.4, -0.3, "#c8e0c8", "#6a3a6a"],
];
// park between the houses and the camera
const TREES: [number, number, number][] = [[-5, 4.6, 1], [-2.3, 6.0, 0.8], [1.4, 6.4, 1.1], [4.8, 4.9, 0.9], [-7.2, 6.8, 1.2], [7, 7, 1], [-0.4, 8.6, 0.9]];
const LAMPS: [number, number][] = [[-5.6, 2.6], [-1.9, 2.6], [1.9, 2.6], [5.6, 2.6]];
// people: start in the park looking up; later they run to a door
const PEOPLE: [number, number, string, number][] = [[-3.4, 3.7, "#e84a4a", 0], [-0.7, 4.1, "#3a8ae8", 1], [0.8, 3.5, "#f0c040", 2], [3.2, 4.0, "#55c08a", 3], [4.4, 3.6, "#c060e0", 3]];

const House: React.FC<{ h: (typeof HOUSES)[number]; i: number; f: number; snow: number }> = ({ h, i, f, snow }) => {
  const [x, z, r, wall, roof] = h, lit = f >= DARK + 6 + i * 5 ? 1 : 0;
  return (
    <group position={[x, 0, z]} rotation={[0, r, 0]}>
      <mesh position={[0, 1, 0]}><boxGeometry args={[2.2, 2, 1.9]} /><M c={wall} /></mesh>
      <mesh position={[0, 2.55, 0]} rotation={[0, Math.PI / 4, 0]}><coneGeometry args={[1.85, 1.1, 4]} /><M c={mixC(roof, "#f4f8ff", snow)} /></mesh>
      <mesh position={[0, 0.55, 0.96]}><boxGeometry args={[0.45, 1.1, 0.04]} /><M c="#5a3a2a" /></mesh>
      {[-0.65, 0.65].map(wx => <mesh key={wx} position={[wx, 1.25, 0.96]}><boxGeometry args={[0.45, 0.45, 0.04]} /><M c={lit ? "#ffd27a" : "#8ab8d8"} e="#ffc860" ei={lit * 2.2} /></mesh>)}
      {lit > 0 && <Glow size={1.6} color="#ffb84a" opacity={0.35} pos={[0, 1.25, 1.1]} />}
    </group>
  );
};

const Tree: React.FC<{ t: (typeof TREES)[number]; i: number; f: number; wilt: number; snow: number }> = ({ t, i, f, wilt, snow }) => {
  const [x, z, s] = t, sway = Math.sin(f * 0.05 + i) * 0.03 * (1 + snowAt(f) * 2);
  const leaf = wilt < 0.5 ? mixC("#3fa04a", "#b89a3a", wilt * 2) : mixC("#b89a3a", "#6a4a2a", (wilt - 0.5) * 2);
  const crown = 1 - wilt * 0.45 - (rnd(i, 3) * 0.15) * wilt;
  return (
    <group position={[x, 0, z]} scale={s} rotation={[sway, 0, sway]}>
      <mesh position={[0, 0.6, 0]}><cylinderGeometry args={[0.1, 0.16, 1.2, 5]} /><M c="#6a4a2a" /></mesh>
      <mesh position={[0, 1.55, 0]} scale={crown}><icosahedronGeometry args={[0.75, 0]} /><M c={leaf} /></mesh>
      {snow > 0.05 && <mesh position={[0, 1.55 + 0.35 * crown, 0]} scale={[crown * 0.95, crown * 0.45 * snow, crown * 0.95]}><icosahedronGeometry args={[0.75, 0]} /><M c="#f4f8ff" /></mesh>}
    </group>
  );
};

const Person: React.FC<{ p: (typeof PEOPLE)[number]; i: number; f: number }> = ({ p, i, f }) => {
  const [x, z, c, door] = p;
  const [hx, hz] = [HOUSES[door][0], HOUSES[door][1] + 1.0];
  const run = sat((f - T.run[0] - i * 6) / (T.run[1] - T.run[0]));
  if (run >= 1) return null;
  const px = lerp(x, hx, ease(run)), pz = lerp(z, hz, ease(run));
  const look = f >= DARK && run === 0 ? 0.5 : 0, bob = run > 0 ? Math.abs(Math.sin(f * 0.9 + i)) * 0.12 : 0;
  const face = run > 0 ? Math.atan2(hx - x, hz - z) : 0.3 * Math.sin(i);
  const shiver = f > T.snow && run === 0 ? Math.sin(f * 2.2 + i) * 0.02 : 0;
  return (
    <group position={[px + shiver, bob, pz]} rotation={[0, face, 0]}>
      <mesh position={[0, 0.42, 0]}><boxGeometry args={[0.32, 0.5, 0.2]} /><M c={c} /></mesh>
      {[-0.08, 0.08].map((lx, k) => <mesh key={lx} position={[lx, 0.1, 0]} rotation={[run > 0 ? Math.sin(f * 0.9 + k * Math.PI) * 0.7 : 0, 0, 0]}><boxGeometry args={[0.1, 0.26, 0.1]} /><M c="#2a2a4a" /></mesh>)}
      <mesh position={[0, 0.82, 0]} rotation={[-look, 0, 0]}><icosahedronGeometry args={[0.15, 0]} /><M c="#f2b48a" /></mesh>
    </group>
  );
};

const Snow: React.FC<{ f: number }> = ({ f }) => {
  const geo = useMemo(() => { const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.BufferAttribute(new Float32Array(900 * 3), 3)); return g; }, []);
  const s = snowAt(f); if (s <= 0) return null;
  const p = geo.attributes.position as THREE.BufferAttribute, n = Math.floor(900 * s);
  for (let i = 0; i < 900; i++) {
    if (i >= n) { p.setXYZ(i, 0, -99, 0); continue; }
    const fall = (rnd(i, 1) * 8 + f * (0.03 + rnd(i, 2) * 0.03)) % 8;
    p.setXYZ(i, (rnd(i, 3) - 0.5) * 22 + Math.sin(f * 0.04 + i) * 0.4 + f * 0.01, 8 - fall, (rnd(i, 4) - 0.5) * 22);
  }
  p.needsUpdate = true;
  return <points geometry={geo}><pointsMaterial color="#ffffff" size={1.6} sizeAttenuation={false} /></points>;
};

const Sea: React.FC<{ f: number }> = ({ f }) => {
  const geo = useMemo(() => { const g = new THREE.PlaneGeometry(80, 70, 40, 34); g.rotateX(-Math.PI / 2); g.translate(0, 0, -41); return g.toNonIndexed(); }, []);
  const base = useMemo(() => Float32Array.from(geo.attributes.position.array as Float32Array), [geo]);
  const ice = iceAt(f), p = geo.attributes.position as THREE.BufferAttribute;
  for (let i = 0; i < p.count; i++) {
    const x = base[i * 3], z = base[i * 3 + 2], front = sat(ice * 1.6 - (-z - 6) / 50); // ice grows out from the shore
    const a = 0.12 * (1 - front) * (1 - ice * 0.5);
    p.setY(i, Math.sin(x * 0.5 + f * 0.06) * a + Math.cos(z * 0.6 + x * 0.2 + f * 0.05) * a - 0.05);
  }
  p.needsUpdate = true; geo.computeVertexNormals();
  return <mesh geometry={geo}><meshStandardMaterial color={mixC("#2a7ad8", "#dfefff", ice)} flatShading roughness={lerp(0.35, 0.8, ice)} metalness={0.05} /></mesh>;
};

const Boat: React.FC<{ f: number }> = ({ f }) => {
  const ice = iceAt(f), bob = (1 - ice) * Math.sin(f * 0.07) * 0.08, tilt = (1 - ice) * Math.sin(f * 0.05) * 0.06 + ice * 0.12;
  return (
    <group position={[-2.5, bob, -11]} rotation={[0, 0.6, tilt]}>
      <mesh position={[0, 0.2, 0]}><boxGeometry args={[2.4, 0.5, 0.9]} /><M c="#c84a3a" /></mesh>
      <mesh position={[-0.3, 0.7, 0]}><boxGeometry args={[0.9, 0.5, 0.7]} /><M c="#f0f0f0" /></mesh>
      <mesh position={[0.5, 1.3, 0]}><cylinderGeometry args={[0.04, 0.04, 1.8, 4]} /><M c="#5a4a3a" /></mesh>
      {ice > 0.5 && <mesh position={[0, 0.48, 0]} scale={[1, ice, 1]}><boxGeometry args={[2.3, 0.06, 0.85]} /><M c="#f4f8ff" /></mesh>}
    </group>
  );
};

// camera per beat: street at noon -> trees and people -> over the sea
type Shot = { pos: THREE.Vector3; look: THREE.Vector3 };
const V = (x: number, y: number, z: number) => new THREE.Vector3(x, y, z);
const shot = (f: number): Shot => {
  const u = ease((f - B[3]) / 150), lookUp = sat((f - DARK) / 30);
  const a: Shot = { pos: V(lerp(3.2, 2.2, u), lerp(4.4, 3.8, u), lerp(16.5, 13.5, u)), look: V(0, lerp(2.0, 3.4, lookUp), 0) };
  const v = (f - B[4]) / 150;
  const b: Shot = { pos: V(lerp(-3.2, -1.0, v), 1.7, lerp(10.5, 9.2, v)), look: V(lerp(-1.2, 1.4, v), 1.0, 3.6) };
  const w = (f - B[5]) / 150;
  const c: Shot = { pos: V(lerp(2.6, 1.8, w), lerp(6.6, 7.4, w), lerp(3.2, 1.6, w)), look: V(-2.2, 0, -12) };
  const mix = (p: Shot, q: Shot, t: number): Shot => ({ pos: p.pos.clone().lerp(q.pos, ease(t)), look: p.look.clone().lerp(q.look, ease(t)) });
  if (f < B[4] - 10) return a;
  if (f < B[4] + 16) return mix(a, b, (f - (B[4] - 10)) / 26);
  if (f < B[5] - 10) return b;
  if (f < B[5] + 16) return mix(b, c, (f - (B[5] - 10)) / 26);
  return c;
};

export const Town: React.FC<{ f: number }> = ({ f }) => {
  const { camera } = useThree();
  const sh = shot(f), jolt = f >= DARK && f < DARK + 8 ? (1 - (f - DARK) / 8) * 0.06 : 0;
  camera.up.set(0, 1, 0);
  camera.position.set(sh.pos.x + Math.sin(f * 2.1) * jolt, sh.pos.y + Math.cos(f * 1.7) * jolt, sh.pos.z);
  camera.lookAt(sh.look);
  const pc = camera as THREE.PerspectiveCamera; pc.fov = 50; pc.near = 0.05; pc.far = 300; pc.updateProjectionMatrix();
  const day = f < DARK ? 1 : 0, wilt = wiltAt(f), snow = snowAt(f), ice = iceAt(f);
  const ground = wilt < 1 && snow < 0.3 ? mixC("#5ab04a", "#8a7a3a", wilt) : mixC("#8a7a3a", "#eef4ff", (snow - 0.3) / 0.7);
  return (
    <>
      <color attach="background" args={[day ? "#6ab8ff" : "#03040c"]} />
      {!day && <Stars f={f} />}
      {day > 0 && <><Glow size={14} color="#fff2c0" opacity={0.9} pos={[-14, 18, -40]} /><mesh position={[-14, 18, -40]}><sphereGeometry args={[2.2, 12, 8]} /><meshBasicMaterial color="#fff8e0" /></mesh></>}
      <hemisphereLight args={[day ? "#cfe8ff" : "#2a3a6a", day ? "#8a7a5a" : "#0a0a14", day ? 1.1 : 0.8]} />
      <directionalLight position={[-14, 18, -10]} intensity={day * 2.4} color="#fff0d8" />
      <ambientLight intensity={day ? 0 : 0.38} color="#7a90d0" />
      {!day && LAMPS.slice(0, 3).map(([x, z], i) => f >= DARK + 4 + i * 4 && <pointLight key={i} position={[x, 2.3, z]} intensity={6} distance={7} decay={1.5} color="#ffc070" />)}
      {/* ground, road, shore */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 18]}><planeGeometry args={[80, 48]} /><M c={ground} /></mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.01, -2.4]}><planeGeometry args={[40, 1.4]} /><M c={mixC("#4a4a5a", "#dde6f4", (snow - 0.5) * 2)} /></mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.005, -5]}><planeGeometry args={[80, 2.2]} /><M c={mixC("#e0cf98", "#eef4ff", snow)} /></mesh>
      {HOUSES.map((h, i) => <House key={i} h={h} i={i} f={f} snow={snow} />)}
      {TREES.map((t, i) => <Tree key={i} t={t} i={i} f={f} wilt={wilt} snow={snow} />)}
      {LAMPS.map(([x, z], i) => {
        const on = !day && f >= DARK + 4 + i * 4;
        return (
          <group key={i} position={[x, 0, z]}>
            <mesh position={[0, 1.2, 0]}><cylinderGeometry args={[0.05, 0.06, 2.4, 5]} /><M c="#3a3a4a" /></mesh>
            <mesh position={[0, 2.45, 0]}><icosahedronGeometry args={[0.16, 0]} /><M c={on ? "#fff0c0" : "#c8c8d0"} e="#ffd080" ei={on ? 3 : 0} /></mesh>
            {on && <Glow size={2.4} color="#ffc070" opacity={0.55} pos={[0, 2.45, 0]} />}
          </group>
        );
      })}
      {PEOPLE.map((p, i) => <Person key={i} p={p} i={i} f={f} />)}
      <Sea f={f} />
      <Boat f={f} />
      <Snow f={f} />
      {ice > 0.2 && <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.02, -6.4]}><planeGeometry args={[80, 1]} /><M c="#f4f8ff" /></mesh>}
    </>
  );
};
