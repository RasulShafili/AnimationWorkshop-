// "What if oxygen doubled?" — a floating low-poly town at golden hour.
import React, { useMemo } from "react";
import * as THREE from "three";
import { useThree } from "@react-three/fiber";
import T from "./timeline.json";
import { rnd, sat, lerp, ease, C, mixC, Mat, Box, House, HouseSpec, Apartment, Tree, Car, Lamp, Bench, Bin, Person } from "./kit";
import { Surroundings } from "./env";

const B = T.beats;
type V3 = [number, number, number];
const V = (x: number, y: number, z: number) => new THREE.Vector3(x, y, z);

// ---------------- layout ----------------
const HOUSES: HouseSpec[] = [
  { p: [1.6, -2.2], ry: 0, w: 2.4, d: 2.0, floors: 2, wall: "#f0d6a4", roof: "#d9542f", trim: "#a83a2a", seed: 1 },
  { p: [4.9, -2.3], ry: 0, w: 2.0, d: 2.0, floors: 1, wall: "#ecd0a0", roof: "#4f9a8c", trim: "#7a4a3a", seed: 2 },
  { p: [8.4, -2.4], ry: 0, w: 2.6, d: 2.2, floors: 2, wall: "#f2dcb0", roof: "#4f9a8c", trim: "#7a4a3a", seed: 3 },
  { p: [0.9, -6.6], ry: 0.1, w: 2.2, d: 2.0, floors: 1, wall: "#e8c898", roof: "#d9542f", trim: "#a83a2a", seed: 4 },
  { p: [9.2, -7.0], ry: -0.1, w: 2.4, d: 2.2, floors: 2, wall: "#f0d6a4", roof: "#e0643a", trim: "#a83a2a", seed: 5 },
  { p: [1.8, 5.3], ry: 0, w: 2.6, d: 2.2, floors: 2, wall: "#f0d6a4", roof: "#d9542f", trim: "#a83a2a", seed: 6 },
  { p: [5.4, 5.1], ry: 0, w: 2.2, d: 2.0, floors: 1, wall: "#ecd0a0", roof: "#4f9a8c", trim: "#7a4a3a", seed: 7 },
  { p: [9.0, 5.4], ry: 0, w: 2.6, d: 2.2, floors: 2, wall: "#f2dcb0", roof: "#d9542f", trim: "#a83a2a", seed: 8 },
  { p: [3.0, 9.6], ry: 0, w: 2.2, d: 2.0, floors: 1, wall: "#e8c898", roof: "#4f9a8c", trim: "#7a4a3a", seed: 9 },
  { p: [7.4, 9.8], ry: 0, w: 2.4, d: 2.0, floors: 2, wall: "#f0d6a4", roof: "#e0643a", trim: "#a83a2a", seed: 10 },
];
// forest in the back-left block: this is what burns
const FOREST: { p: [number, number]; s: number }[] = [];
for (let i = 0; FOREST.length < 26 && i < 400; i++) {
  const x = -11.3 + rnd(i, 1) * 7.6, z = -11.3 + rnd(i, 2) * 9.8;
  if (FOREST.every(t => Math.hypot(t.p[0] - x, t.p[1] - z) > 1.25)) FOREST.push({ p: [x, z], s: 0.9 + rnd(i, 3) * 0.5 });
}
const STRIKE_TREE = FOREST.reduce((b, t, i) => (Math.hypot(t.p[0] + 7, t.p[1] + 6) < Math.hypot(FOREST[b].p[0] + 7, FOREST[b].p[1] + 6) ? i : b), 0);
const IGNITE = FOREST.map(t => T.strike + 4 + Math.hypot(t.p[0] - FOREST[STRIKE_TREE].p[0], t.p[1] - FOREST[STRIKE_TREE].p[1]) * 16);
const burnRaw = (i: number, f: number) => (f - IGNITE[i]) / 55;
const TOWN_TREES: { p: [number, number]; s: number }[] = [[3.3, -4.4], [6.7, -4.6], [11, -4], [0, 3.6], [3.7, 3.4], [7.2, 3.5], [10.8, 7.8], [-0.2, 10.8], [5.2, 11.2], [11, 11]].map(([x, z], i) => ({ p: [x, z] as [number, number], s: 0.85 + rnd(i, 7) * 0.35 }));
const PARK = { c: [-7.4, 7.0] as [number, number], r: 2.9 };
const LAMPS: [number, number][] = [[-10, 0.2], [-5.2, 0.2], [0.6, 0.2], [5.4, 0.2], [10, 0.2]];
const PARKED: { p: V3; ry: number; c: string }[] = [{ p: [3.4, 0, 0.75], ry: 0, c: "#6a4a8a" }, { p: [5.4, 0, 0.75], ry: 0, c: "#3a4a9a" }, { p: [7.4, 0, 0.75], ry: Math.PI, c: "#8a4a7a" }];

// ---------------- story state ----------------
const runnerAt = (f: number): { p: V3; ry: number } => {
  const a = f * 0.03, x = PARK.c[0] + Math.cos(a) * PARK.r, z = PARK.c[1] + Math.sin(a) * PARK.r;
  return { p: [x, 0.02, z], ry: -a - Math.PI / 2 };
};
// time of day: golden hour, a dusk dip during the fire, two fast day/night cycles during the rust time-lapse
const sunAt = (f: number) => {
  if (f >= T.rust[0] && f < T.rust[1]) {
    const ph = 0.35 + (f - T.rust[0]) / (T.rust[1] - T.rust[0]) * Math.PI * 4; // two days
    const el = Math.sin(ph);
    return { dir: V(Math.cos(ph) * 18, Math.max(-6, el * 16), 8), day: sat(el * 2.2 + 0.1) };
  }
  const dusk = f >= B[2] && f < B[3] ? 0.55 * ease((f - B[2]) / 60) : 0;
  return { dir: V(14, 9 - dusk * 6, 11), day: 1 - dusk };
};

const Road: React.FC<{ along: "x" | "z"; at: number; from: number; to: number }> = ({ along, at, from, to }) => {
  const len = to - from, mid = (from + to) / 2, w = 1.9, dashes = Math.floor(len / 1.3);
  const P = (u: number, v: number, y: number): V3 => (along === "x" ? [u, y, v] : [v, y, u]);
  const S = (lu: number, lv: number, h: number): V3 => (along === "x" ? [lu, h, lv] : [lv, h, lu]);
  return (
    <group>
      <Box p={P(mid, at, 0.015)} s={S(len, w, 0.03)} c="#34303a" shadow={false} />
      {Array.from({ length: dashes }, (_, i) => <Box key={i} p={P(from + 0.65 + i * 1.3, at, 0.035)} s={S(0.55, 0.08, 0.01)} c="#e8dcc0" shadow={false} />)}
      {[-1, 1].map(s => <Box key={s} p={P(mid, at + s * (w / 2 + 0.28), 0.04)} s={S(len, 0.56, 0.08)} c="#cdb995" />)}
    </group>
  );
};

const Flames: React.FC<{ p: V3; k: number; f: number; seed: number; size?: number }> = ({ p, k, f, seed, size = 1 }) => {
  if (k <= 0.01) return null;
  return (
    <group position={p} scale={k * size}>
      {[0, 1, 2, 3].map(i => {
        const fl = 0.75 + 0.35 * Math.sin(f * (0.9 + i * 0.23) + seed * 3 + i), a = i * 1.7 + seed;
        const col = i % 2 ? new THREE.Color(2.4, 0.75, 0.12) : new THREE.Color(2.8, 1.5, 0.3);
        return <mesh key={i} position={[Math.cos(a) * 0.16 * (i > 0 ? 1 : 0), 0.32 * fl, Math.sin(a) * 0.16 * (i > 0 ? 1 : 0)]} scale={[1, fl, 1]} rotation={[0, a, 0]}><coneGeometry args={[i ? 0.17 : 0.24, i ? 0.6 : 0.8, 5]} /><meshBasicMaterial color={col} toneMapped={false} /></mesh>;
      })}
    </group>
  );
};
const Smoke: React.FC<{ p: V3; k: number; f: number; seed: number }> = ({ p, k, f, seed }) => {
  if (k <= 0.01) return null;
  return (
    <group position={p}>
      {[0, 1, 2, 3].map(i => {
        const u = ((f * 0.012 + i / 4 + seed * 0.37) % 1);
        return <mesh key={i} position={[Math.sin(u * 6 + seed) * 0.3 + u * 1.2, 0.6 + u * 3.6, u * 0.5]} scale={0.3 + u * 0.9}><icosahedronGeometry args={[0.5, 0]} /><meshStandardMaterial color="#5a5458" flatShading transparent opacity={k * 0.55 * (1 - u)} depthWrite={false} /></mesh>;
      })}
    </group>
  );
};

const Bolt: React.FC<{ to: V3; f: number }> = ({ to, f }) => {
  const pts = useMemo(() => { const a: THREE.Vector3[] = []; for (let i = 0; i <= 10; i++) { const u = i / 10; a.push(V(to[0] + (i && i < 10 ? (rnd(i, 31) - 0.5) * 1.6 : 0) + (1 - u) * 3, lerp(18, to[1], u), to[2] + (i && i < 10 ? (rnd(i, 32) - 0.5) * 1.2 : 0))); } return a; }, [to]);
  const on = f >= T.strike && f < T.strike + 6 && (f - T.strike) % 2 === 0 ? 1 : f >= T.strike && f < T.strike + 6 ? 0.4 : 0;
  if (!on) return null;
  return (
    <group>
      {pts.slice(1).map((b, i) => { const a = pts[i], m = a.clone().add(b).multiplyScalar(0.5), len = a.distanceTo(b); const q = new THREE.Quaternion().setFromUnitVectors(V(0, 1, 0), b.clone().sub(a).normalize());
        return <mesh key={i} position={m} quaternion={q}><cylinderGeometry args={[0.06, 0.06, len, 4]} /><meshBasicMaterial color={new THREE.Color(7 * on, 7 * on, 9 * on)} toneMapped={false} /></mesh>; })}
    </group>
  );
};

const Dragonfly: React.FC<{ p: V3; ry: number; f: number }> = ({ p, ry, f }) => {
  const flap = Math.sin(f * 2.6) * 0.5;
  return (
    <group position={p} rotation={[0, ry, 0]}>
      <mesh position={[0.06, 0, 0]} scale={[1.3, 1, 1]}><icosahedronGeometry args={[0.05, 1]} /><Mat c="#2a7a8a" r={0.35} m={0.3} /></mesh>
      <mesh position={[0.15, 0.01, 0]}><icosahedronGeometry args={[0.04, 1]} /><Mat c="#3ac06a" r={0.3} /></mesh>
      {[-1, 1].map(s => <mesh key={s} position={[0.17, 0.02, s * 0.025]}><icosahedronGeometry args={[0.022, 1]} /><Mat c="#1a5a3a" r={0.2} /></mesh>)}
      <mesh position={[-0.2, 0, 0]} rotation={[0, 0, Math.PI / 2]}><cylinderGeometry args={[0.018, 0.012, 0.36, 6]} /><Mat c="#2a8a9a" r={0.35} m={0.3} /></mesh>
      {[-1, 1].map(s => [0.06, -0.03].map((x, k) => (
        <group key={`${s}${k}`} position={[x, 0.03, s * 0.03]} rotation={[s * (flap + (k ? 0.35 : 0)), 0, 0]}>
          <mesh position={[0, 0, s * 0.11]} rotation={[-Math.PI / 2, 0, 0]}><planeGeometry args={[0.07, 0.22]} /><meshStandardMaterial color="#d8f0ff" transparent opacity={0.45} side={THREE.DoubleSide} roughness={0.2} depthWrite={false} /></mesh>
        </group>
      )))}
    </group>
  );
};

// ---------------- sky + fog ----------------
const Sky: React.FC<{ day: number; fire: number }> = ({ day, fire }) => {
  const geo = useMemo(() => new THREE.SphereGeometry(420, 32, 20), []);
  const top = mixC(mixC("#22264a", "#8fb0d8", day), "#5a3a3a", fire * 0.35), bot = mixC(mixC("#3a3050", "#f6c79e", day), "#c8643a", fire * 0.4);
  const col = useMemo(() => new Float32Array(geo.attributes.position.count * 3), [geo]);
  const p = geo.attributes.position;
  for (let i = 0; i < p.count; i++) { const u = sat((p.getY(i) / 420 - 0.0) / 0.6); const c = bot.clone().lerp(top, u); col.set([c.r, c.g, c.b], i * 3); }
  geo.setAttribute("color", new THREE.BufferAttribute(col, 3));
  return <mesh geometry={geo}><meshBasicMaterial vertexColors side={THREE.BackSide} fog={false} toneMapped={false} /></mesh>;
};

// ---------------- cameras ----------------
type Shot = { pos: THREE.Vector3; look: THREE.Vector3; fov: number };
const FIRE_C = V(-7.5, 0.8, -6.5);
const shotAt = (f: number): Shot => {
  const camp = V(PARK.c[0], 0.5, PARK.c[1]);
  const s0: Shot = { pos: camp.clone().add(V(4.4, 2.9, 5.8).multiplyScalar(lerp(0.7, 1.0, ease(f / 70)))), look: camp.clone().add(V(0, 0.4, 0)), fov: 34 };
  const r = runnerAt(f), rp = V(...r.p), a = f * 0.03;
  const s1: Shot = { pos: rp.clone().add(V(Math.cos(a + 0.9) * 6.2, 2.9, Math.sin(a + 0.9) * 6.2)), look: rp.clone().add(V(0, 1.25, 0)), fov: 34 };
  const u2 = (f - B[2]) / (B[3] - B[2]);
  const s2: Shot = { pos: V(lerp(13, 9, u2), lerp(14, 11, u2), lerp(15, 17, u2)), look: V(lerp(-2.5, -4.5, u2), 0, lerp(-3.5, -4.5, u2)), fov: 38 };
  const u3 = (f - B[3]) / (B[4] - B[3]);
  const s3: Shot = { pos: V(lerp(11.6, 10.4, u3), lerp(1.9, 1.7, u3), lerp(3.4, 3.0, u3)), look: V(4.6, 0.55, 0.8), fov: 34 };
  const dp = V(-5.15, 1.05, 4.7), u4 = (f - B[4]) / (B[5] - B[4]);
  const s4: Shot = { pos: dp.clone().add(V(lerp(2.7, 2.2, u4), lerp(0.55, 0.4, u4), lerp(2.9, 2.4, u4))), look: dp.clone().add(V(-0.3, -0.3, 0)), fov: 34 };
  const u5 = ease((f - B[5]) / 70);
  const s5: Shot = { pos: V(lerp(18, 42, u5), lerp(12, 34, u5), lerp(20, 48, u5)), look: V(0, lerp(0, -2, u5), lerp(0, -10, u5)), fov: 40 };
  const mix = (p: Shot, q: Shot, t: number): Shot => ({ pos: p.pos.clone().lerp(q.pos, ease(t)), look: p.look.clone().lerp(q.look, ease(t)), fov: lerp(p.fov, q.fov, ease(t)) });
  const end0: Shot = { pos: camp.clone().add(V(4.4, 2.9, 5.8).multiplyScalar(0.7)), look: camp.clone().add(V(0, 0.4, 0)), fov: 34 };
  if (f < B[1] - 12) return s0;
  if (f < B[1] + 14) return mix(s0, s1, (f - (B[1] - 12)) / 26);
  if (f < B[2] - 12) return s1;
  if (f < B[2] + 20) return mix(s1, s2, (f - (B[2] - 12)) / 32);
  if (f < B[3] - 10) return s2;
  if (f < B[3] + 16) return mix(s2, s3, (f - (B[3] - 10)) / 26);
  if (f < B[4] - 10) return s3;
  if (f < B[4] + 16) return mix(s3, s4, (f - (B[4] - 10)) / 26);
  if (f < B[5] - 10) return s4;
  if (f < B[5] + 20) return mix(s4, s5, (f - (B[5] - 10)) / 30);
  if (f < B[6] - 36) return s5;
  return mix(s5, end0, (f - (B[6] - 36)) / 36);
};

export const World: React.FC<{ f: number }> = ({ f }) => {
  const { camera, scene } = useThree();
  const sh = shotAt(f);
  const shake = f >= T.flare && f < T.flare + 10 ? (1 - (f - T.flare) / 10) * 0.05 : f >= T.strike && f < T.strike + 12 ? (1 - (f - T.strike) / 12) * 0.12 : 0;
  camera.position.set(sh.pos.x + Math.sin(f * 2.3) * shake, sh.pos.y + Math.cos(f * 1.9) * shake, sh.pos.z);
  camera.lookAt(sh.look);
  const pc = camera as THREE.PerspectiveCamera; pc.fov = sh.fov; pc.near = 0.1; pc.far = 500; pc.updateProjectionMatrix();

  const sun = sunAt(f), day = sun.day;
  const burning = FOREST.map((_, i) => burnRaw(i, f));
  const flameK = burning.map(b => sat(b * 3) * (1 - sat((b - 1) * 1.4)));
  const fireNow = flameK.reduce((a, b) => a + b, 0), fireGlow = sat(fireNow / 8) * (f < B[3] ? 1 : 0);
  const flash = f >= T.strike && f < T.strike + 6 ? (f - T.strike) % 2 === 0 ? 1 : 0.4 : 0;
  const rust = ease((f - T.rust[0]) / (T.rust[1] - T.rust[0]));
  const night = 1 - day, glow = sat(night * 1.4 + fireGlow * 0.5 + (f >= B[2] && f < B[3] ? 0.35 : 0));
  const o2 = f >= T.gauge[1] ? 1 : 0;
  const campK = f < T.flare ? 1 : lerp(3.2, 1.7, ease((f - T.flare) / 40));
  const gust = f >= T.flare && f < T.flare + 50 ? Math.sin((f - T.flare) / 50 * Math.PI) : 0;
  const fogC = mixC(mixC("#3a3050", "#f6c79e", day), "#c8643a", fireGlow * 0.4);
  scene.fog = new THREE.Fog(fogC, 70, 360);
  // fire light follows the burning trees
  let fx = 0, fz = 0, fw = 0; burning.forEach((_, i) => { fx += FOREST[i].p[0] * flameK[i]; fz += FOREST[i].p[1] * flameK[i]; fw += flameK[i]; });
  const fireP: V3 = fw > 0 ? [fx / fw, 2, fz / fw] : [-7, 2, -6];
  const carX = ((f * 0.06 + 14) % 28) - 14;
  const fly = f >= T.fly[0] - 10 && f < T.fly[1] + 10;
  const fa = (f - T.fly[0]) * 0.05, dfp: V3 = [-4.98 + Math.sin(fa) * 0.3, 1.0 + Math.sin(f * 0.11) * 0.07, 4.82 + Math.sin(fa * 2) * 0.14];

  return (
    <>
      <Sky day={day} fire={fireGlow} />
      <hemisphereLight args={[mixC("#4a5080", "#ffe6c8", day), mixC("#1a1424", "#6a5070", day), 0.55 + day * 0.35 + flash * 2]} />
      <directionalLight position={sun.dir} intensity={day * 3.2} color="#ffcf98" castShadow shadow-mapSize={[4096, 4096]} shadow-camera-left={-34} shadow-camera-right={34} shadow-camera-top={34} shadow-camera-bottom={-34} shadow-camera-near={1} shadow-camera-far={140} shadow-bias={-0.0004} shadow-normalBias={0.03} />
      <ambientLight intensity={0.12 + night * 0.15} color="#8a90c8" />
      {fireGlow > 0.02 && <pointLight position={fireP} intensity={fireGlow * 60} distance={22} decay={1.6} color="#ff8a3a" />}
      <pointLight position={[PARK.c[0], 0.9, PARK.c[1]]} intensity={(4 + campK * 4) * (0.8 + 0.2 * Math.sin(f * 0.7))} distance={6} decay={1.5} color="#ffa04a" />
      {night > 0.4 && LAMPS.slice(1, 4).map((l, i) => <pointLight key={i} position={[l[0], 1.7, l[1]]} intensity={night * 6} distance={5} decay={1.5} color="#ffd08a" />)}

      <Surroundings f={f} glow={glow} day={day} sunDir={sun.dir} />
      {/* scorched ground under the forest */}
      {FOREST.map((t, i) => burning[i] > 0 && <mesh key={i} rotation={[-Math.PI / 2, 0, 0]} position={[t.p[0], 0.012 + i * 0.0003, t.p[1]]} receiveShadow><circleGeometry args={[sat(burning[i]) * 1.3, 9]} /><Mat c="#2e2620" /></mesh>)}
      <Road along="x" at={1.5} from={-12} to={12} />
      <Road along="z" at={-2} from={-12} to={12} />
      {[0, 1, 2, 3, 4].map(i => <Box key={i} p={[-3.5 - i * 0.0, 0.045, 1.5 - 0.7 + i * 0.35]} s={[0.5, 0.01, 0.2]} c="#e8dcc0" shadow={false} />)}
      {/* park: lighter lawn, sand running track, campfire, benches, bushes */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[PARK.c[0], 0.012, PARK.c[1]]} receiveShadow><circleGeometry args={[4.4, 28]} /><Mat c="#8aae46" /></mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[PARK.c[0], 0.02, PARK.c[1]]} receiveShadow><ringGeometry args={[PARK.r - 0.35, PARK.r + 0.35, 40]} /><Mat c="#d8b88a" /></mesh>
      <group position={[PARK.c[0], 0, PARK.c[1]]}>
        {Array.from({ length: 8 }, (_, i) => <mesh key={i} position={[Math.cos(i / 8 * 6.28) * 0.5, 0.08, Math.sin(i / 8 * 6.28) * 0.5]} castShadow><icosahedronGeometry args={[0.13, 0]} /><Mat c="#8a8478" /></mesh>)}
        {[0.4, -0.4].map(r => <mesh key={r} position={[0, 0.1, 0]} rotation={[0, r, Math.PI / 2]} castShadow><cylinderGeometry args={[0.07, 0.07, 0.8, 6]} /><Mat c="#6a3a24" /></mesh>)}
        <Flames p={[0, 0.12, 0]} k={1} size={campK * 0.38} f={f} seed={1} />
      </group>
      <Bench p={[-5.2, 3.6]} ry={0.3} /><Bench p={[-9.8, 9.4]} ry={-2.4} />
      {[[-10.6, 4.2], [-4.4, 9.8], [-11, 10.8], [-4.2, 4.1]].map(([x, z], i) => <mesh key={i} position={[x, 0.25, z]} castShadow><icosahedronGeometry args={[0.38, 0]} /><Mat c="#6a8a2a" /></mesh>)}
      <Bin p={[-4.1, 3.4]} /><Bin p={[2.8, 0.25]} />

      {HOUSES.map((h, i) => <House key={i} h={h} glow={glow * (0.6 + 0.4 * rnd(i, 9))} />)}
      <Apartment p={[4.8, -9.6]} w={5} d={2.6} floors={6} glow={glow} />
      {TOWN_TREES.map((t, i) => <Tree key={i} p={t.p} s={t.s} seed={i} sway={f * 0.04 + gust * 2} />)}
      {FOREST.map((t, i) => <Tree key={i} p={t.p} s={t.s} seed={i + 40} sway={f * 0.04 + gust * 2 + flameK[i] * f * 0.3} burn={sat(burning[i])} tone={rnd(i, 5) > 0.5 ? "#a8c03a" : "#c4c43c"} />)}
      {FOREST.map((t, i) => <Flames key={i} p={[t.p[0], 0.4 * t.s, t.p[1]]} k={flameK[i]} size={t.s * 2.2} f={f} seed={i} />)}
      {FOREST.map((t, i) => <Smoke key={i} p={[t.p[0], 1.2, t.p[1]]} k={i % 2 ? 0 : sat(burning[i] * 2) * (1 - sat((burning[i] - 2.2) * 0.8))} f={f} seed={i} />)}
      <Bolt to={[FOREST[STRIKE_TREE].p[0], 1.6, FOREST[STRIKE_TREE].p[1]]} f={f} />

      {LAMPS.map((l, i) => <Lamp key={i} p={l} on={sat(night * 1.6)} rust={rust} />)}
      {PARKED.map((c, i) => <Car key={i} p={c.p} ry={c.ry} c={c.c} rust={rust} lights={night} />)}
      {(f < T.rust[0] || f > T.rust[1]) && <Car p={[carX, 0, 2.05]} ry={0} c="#3a3a8a" lights={night} rust={f > T.rust[1] ? 1 : 0} />}

      {(f < B[4] || f >= B[5]) && f < B[6] && <Person {...runnerAt(f)} shirt="#e8603a" run={1} f={f} />}
      {f >= B[4] - 12 && f < B[5] && <Person p={[-5.6, 0.02, 4.3]} ry={-0.7} shirt="#e8603a" run={0} f={f} />}
      {fly && <Dragonfly p={dfp} ry={-0.7 + Math.PI + Math.cos(fa) * 0.5} f={f} />}
      {/* O2 doubling: a soft breath of wind sweeping the island */}
      {gust > 0.02 && Array.from({ length: 10 }, (_, i) => <mesh key={i} position={[lerp(-14, 14, ((f - T.flare) / 50 + rnd(i, 1) * 0.3) % 1.2), 1 + rnd(i, 2) * 3, -10 + rnd(i, 3) * 20]} rotation={[0, 0, Math.PI / 2]}><cylinderGeometry args={[0.015, 0.015, 2.5, 4]} /><meshBasicMaterial color="#ffffff" transparent opacity={gust * 0.5} /></mesh>)}

    </>
  );
};
