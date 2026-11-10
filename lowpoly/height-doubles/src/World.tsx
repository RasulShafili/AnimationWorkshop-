// Low-poly world. The hero is always 1 unit tall at the origin; the world (built in metres)
// is scaled by 1/height, so the camera never has to travel 3 million km and float precision stays sane.
import React, { useMemo } from "react";
import * as THREE from "three";
import { useThree } from "@react-three/fiber";

const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };
const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
const sat = (v: number) => Math.min(1, Math.max(0, v));
const sstep = (a: number, b: number, x: number) => { const t = sat((x - a) / (b - a)); return t * t * (3 - 2 * t); };
const col = (h: string) => new THREE.Color(h);
const M = (c: string, extra: Partial<THREE.MeshStandardMaterialParameters> = {}) => <meshStandardMaterial color={c} flatShading roughness={0.9} metalness={0} {...extra} />;

// ---------- hero ----------
export const Hero: React.FC<{ t: number; lookUp: number; wave: number; mouthO: boolean }> = ({ t, lookUp, wave, mouthO }) => {
  const s = 1 / 1.7; // model authored in metres for a 1.7 m person
  const sway = Math.sin(t * 2.1) * 0.02, blink = (t * 30 + 20) % 110 < 4;
  const armR = -0.15 - wave * (2.6 + Math.sin(t * 9) * 0.25);
  return (
    <group scale={s} rotation={[0, sway, 0]}>
      {[-1, 1].map(sd => (
        <group key={sd}>
          <mesh position={[sd * 0.11, 0.42, 0]} castShadow><boxGeometry args={[0.15, 0.84, 0.17]} />{M("#2a3a8a")}</mesh>
          <mesh position={[sd * 0.11, 0.04, 0.04]} castShadow><boxGeometry args={[0.17, 0.09, 0.27]} />{M("#ffc94e")}</mesh>
        </group>
      ))}
      <mesh position={[0, 1.08, 0]} castShadow><boxGeometry args={[0.44, 0.52, 0.24]} />{M("#17a58f")}</mesh>
      <mesh position={[0.07, 1.16, 0.122]}><boxGeometry args={[0.1, 0.1, 0.01]} />{M("#62e8c0")}</mesh>
      <group position={[-0.27, 1.3, 0]} rotation={[0, 0, 0.12]}>
        <mesh position={[0, -0.25, 0]} castShadow><boxGeometry args={[0.11, 0.5, 0.12]} />{M("#17a58f")}</mesh>
        <mesh position={[0, -0.53, 0]}><icosahedronGeometry args={[0.065, 0]} />{M("#f2b48a")}</mesh>
      </group>
      <group position={[0.27, 1.3, 0]} rotation={[0, 0, -armR]}>
        <mesh position={[0, -0.25, 0]} castShadow><boxGeometry args={[0.11, 0.5, 0.12]} />{M("#17a58f")}</mesh>
        <mesh position={[0, -0.53, 0]}><icosahedronGeometry args={[0.065, 0]} />{M("#f2b48a")}</mesh>
      </group>
      <mesh position={[0, 1.38, 0]}><cylinderGeometry args={[0.06, 0.07, 0.1, 6]} />{M("#f2b48a")}</mesh>
      <group position={[0, 1.55, 0]} rotation={[-lookUp * 0.32, 0, 0]}>
        <mesh castShadow><icosahedronGeometry args={[0.2, 1]} />{M("#f2b48a")}</mesh>
        <mesh position={[0, 0.01, -0.01]} rotation={[-0.12, 0, 0]}><sphereGeometry args={[0.218, 9, 6, 0, Math.PI * 2, 0, 1.45]} />{M("#e0702e")}</mesh>
        <mesh position={[0.03, 0.24, 0]} rotation={[0, 0, -0.4]}><coneGeometry args={[0.05, 0.14, 4]} />{M("#e0702e")}</mesh>
        {[-1, 1].map(sd => (
          <group key={sd} position={[sd * 0.075, -0.015, 0.172]}>
            <mesh scale={[1, blink ? 0.15 : 1, 0.5]}><icosahedronGeometry args={[0.045, 1]} />{M("#ffffff", { roughness: 0.4 })}</mesh>
            {!blink && <mesh position={[0, -0.005, 0.02]}><icosahedronGeometry args={[0.026, 1]} />{M("#2a1450")}</mesh>}
          </group>
        ))}
        <mesh position={[0, -0.105, 0.175]} scale={mouthO ? [0.6, 0.8, 0.4] : [1, 0.35, 0.4]}><icosahedronGeometry args={[0.035, 1]} />{M("#7a2a3a")}</mesh>
      </group>
    </group>
  );
};

// ---------- neighbourhood (metres) ----------
const House: React.FC<{ p: [number, number]; r: number; c: string; roof: string; s?: number }> = ({ p, r, c, roof, s = 1 }) => (
  <group position={[p[0], 0, p[1]]} rotation={[0, r, 0]} scale={s}>
    <mesh position={[0, 2.6, 0]} castShadow receiveShadow><boxGeometry args={[8, 5.2, 7]} />{M(c)}</mesh>
    <mesh position={[0, 6.4, 0]} rotation={[0, Math.PI / 4, 0]} castShadow><coneGeometry args={[6.4, 2.8, 4]} />{M(roof)}</mesh>
    <mesh position={[0, 1.2, 3.52]}><boxGeometry args={[1.4, 2.4, 0.1]} />{M("#7a4a2a")}</mesh>
    {[-2.4, 2.4].map(x => <mesh key={x} position={[x, 3.2, 3.52]}><boxGeometry args={[1.4, 1.2, 0.1]} />{M("#bfe8ff", { emissive: "#3a6a8a", emissiveIntensity: 0.3 })}</mesh>)}
  </group>
);
const Tree: React.FC<{ p: [number, number]; s: number }> = ({ p, s }) => (
  <group position={[p[0], 0, p[1]]} scale={s}>
    <mesh position={[0, 1.6, 0]} castShadow><cylinderGeometry args={[0.25, 0.35, 3.2, 5]} />{M("#7a4a2a")}</mesh>
    <mesh position={[0, 5.2, 0]} castShadow><icosahedronGeometry args={[2.6, 0]} />{M("#3aa860")}</mesh>
    <mesh position={[0.9, 6.6, 0.3]} castShadow><icosahedronGeometry args={[1.7, 0]} />{M("#4cc070")}</mesh>
  </group>
);
const Car: React.FC<{ x: number; z: number; c: string }> = ({ x, z, c }) => (
  <group position={[x, 0, z]}>
    <mesh position={[0, 0.6, 0]} castShadow><boxGeometry args={[4.2, 0.8, 1.8]} />{M(c)}</mesh>
    <mesh position={[-0.2, 1.25, 0]} castShadow><boxGeometry args={[2.2, 0.6, 1.6]} />{M("#bfe8ff")}</mesh>
    {[-1.4, 1.4].map(wx => [-0.9, 0.9].map(wz => <mesh key={`${wx}${wz}`} position={[wx, 0.32, wz]} rotation={[Math.PI / 2, 0, 0]}><cylinderGeometry args={[0.34, 0.34, 0.2, 8]} />{M("#222233")}</mesh>))}
  </group>
);
const Hoop: React.FC = () => (
  <group position={[2.6, 0, -1.6]} rotation={[0, -0.5, 0]}>
    <mesh position={[0, 1.6, 0]}><cylinderGeometry args={[0.06, 0.08, 3.2, 6]} />{M("#5a6a8a")}</mesh>
    <mesh position={[0, 3.3, 0.25]}><boxGeometry args={[1.4, 0.9, 0.06]} />{M("#ffffff")}</mesh>
    <mesh position={[0, 3.05, 0.55]} rotation={[Math.PI / 2, 0, 0]}><torusGeometry args={[0.23, 0.025, 4, 12]} />{M("#ff6a2a")}</mesh>
  </group>
);

export const Neighbourhood: React.FC<{ t: number }> = ({ t }) => {
  const houses = useMemo(() => Array.from({ length: 26 }, (_, i) => {
    const a = rnd(i, 1) * Math.PI * 2, r = 14 + rnd(i, 2) * 110;
    return { p: [Math.cos(a) * r, Math.sin(a) * r - 6] as [number, number], r: rnd(i, 3) * 6, c: ["#f2d2a0", "#ffb0a0", "#a8d8f0", "#f0f0e0", "#c8e8a8"][i % 5], roof: ["#c8403a", "#5a4a8a", "#2a6a8a"][i % 3] };
  }), []);
  const trees = useMemo(() => Array.from({ length: 40 }, (_, i) => {
    const a = rnd(i, 11) * Math.PI * 2, r = 6 + rnd(i, 12) * 140;
    return { p: [Math.cos(a) * r, Math.sin(a) * r] as [number, number], s: 0.8 + rnd(i, 13) * 0.6 };
  }), []);
  const drive = (t * 6) % 120;
  return (
    <group>
      {houses.map((h, i) => <House key={i} {...h} />)}
      <House p={[-9, -9]} r={0.3} c="#f2d2a0" roof="#c8403a" />
      {trees.map((tr, i) => <Tree key={i} {...tr} />)}
      <Tree p={[5, -6]} s={1.25} />
      <mesh position={[0, 0.02, 9]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow><planeGeometry args={[400, 7]} />{M("#4a4a5a")}</mesh>
      <Car x={-60 + drive} z={7.6} c="#e83a3a" /><Car x={50 - drive} z={10.4} c="#3a7ae8" /><Car x={-110 + drive * 1.3} z={7.6} c="#ffc94e" />
      <Hoop />
    </group>
  );
};

// ---------- city, landmarks, terrain (metres) ----------
const BoxCity: React.FC = () => {
  const mesh = useMemo(() => {
    const n = 900, g = new THREE.BoxGeometry(1, 1, 1); g.translate(0, 0.5, 0);
    const m = new THREE.InstancedMesh(g, new THREE.MeshStandardMaterial({ flatShading: true, roughness: 0.85 }), n);
    const o = new THREE.Object3D(), c = new THREE.Color(), pal = ["#e8e0d0", "#c8d8e8", "#f0c8a8", "#a8b8d8", "#d8d0f0", "#b8e0d0"];
    for (let i = 0; i < n; i++) {
      const a = Math.PI * (1.05 + rnd(i, 21) * 0.9), r = 420 + Math.pow(rnd(i, 22), 0.7) * 3800;
      const w = 18 + rnd(i, 23) * 30, hgt = (15 + Math.pow(rnd(i, 24), 3) * 190) * (r < 1500 ? 1.3 : 0.7);
      o.position.set(Math.cos(a) * r, 0, Math.sin(a) * r - 300); o.scale.set(w, hgt, w * (0.7 + rnd(i, 25) * 0.6)); o.rotation.y = rnd(i, 26);
      o.updateMatrix(); m.setMatrixAt(i, o.matrix); m.setColorAt(i, c.set(pal[i % pal.length]));
    }
    m.castShadow = true; m.receiveShadow = true;
    return m;
  }, []);
  return <primitive object={mesh} />;
};

const Tower: React.FC = () => ( // generic 828 m supertall
  <group position={[640, 0, -820]}>
    {[0, 1, 2, 3, 4, 5, 6].map(i => <mesh key={i} position={[0, 60 + i * 95, 0]} castShadow><cylinderGeometry args={[70 - i * 9, 78 - i * 9, 120, 6]} />{M("#d8e8ff", { metalness: 0.2, roughness: 0.35, emissive: "#3a5a8a", emissiveIntensity: 0.25 })}</mesh>)}
    <mesh position={[0, 760, 0]}><cylinderGeometry args={[2, 8, 140, 5]} />{M("#e0e8ff")}</mesh>
  </group>
);

const Statue: React.FC = () => ( // 93 m: pedestal + green figure with a torch
  <group position={[70, 0, -30]} rotation={[0, -0.9, 0]}>
    <mesh position={[0, 23, 0]} castShadow><boxGeometry args={[30, 46, 30]} />{M("#c8b898")}</mesh>
    <mesh position={[0, 66, 0]} castShadow><cylinderGeometry args={[6, 10, 40, 6]} />{M("#5ab8a0")}</mesh>
    <mesh position={[0, 90, 0]} castShadow><icosahedronGeometry args={[5, 0]} />{M("#5ab8a0")}</mesh>
    <mesh position={[6, 92, 0]} rotation={[0, 0, -0.2]}><cylinderGeometry args={[1.2, 1.2, 18, 5]} />{M("#5ab8a0")}</mesh>
    <mesh position={[8, 102, 0]}><coneGeometry args={[2.4, 5, 5]} />{M("#ffc94e", { emissive: "#ff9a3a", emissiveIntensity: 0.8 })}</mesh>
  </group>
);

const Mountains: React.FC = () => {
  const geo = useMemo(() => {
    const g = new THREE.ConeGeometry(1, 1, 7, 3); g.translate(0, 0.5, 0);
    const pos = g.attributes.position, cols: number[] = [];
    for (let i = 0; i < pos.count; i++) {
      const y = pos.getY(i); if (y > 0.02 && y < 0.98) { pos.setX(i, pos.getX(i) * (0.85 + rnd(i, 31) * 0.3)); pos.setZ(i, pos.getZ(i) * (0.85 + rnd(i, 32) * 0.3)); }
      const c = y > 0.62 ? col("#ffffff") : y > 0.3 ? col("#8a7a8a") : col("#5a8a5a"); cols.push(c.r, c.g, c.b);
    }
    g.setAttribute("color", new THREE.Float32BufferAttribute(cols, 3)); g.computeVertexNormals();
    return g;
  }, []);
  const list = useMemo(() => [
    { x: -9000, z: -26000, h: 8850, r: 9000 }, // the tallest: Everest's height
    ...Array.from({ length: 16 }, (_, i) => ({ x: -40000 + i * 5200 + rnd(i, 41) * 2000, z: -30000 - rnd(i, 42) * 12000, h: 2500 + rnd(i, 43) * 4500, r: 5000 + rnd(i, 44) * 5000 })),
  ], []);
  return <group>{list.map((m, i) => <mesh key={i} geometry={geo} position={[m.x, 0, m.z]} scale={[m.r, m.h, m.r]} castShadow><meshStandardMaterial vertexColors flatShading roughness={1} /></mesh>)}</group>;
};

export const Clouds: React.FC<{ t: number }> = ({ t }) => {
  const mesh = useMemo(() => {
    const n = 260, g = new THREE.IcosahedronGeometry(1, 0);
    const m = new THREE.InstancedMesh(g, new THREE.MeshStandardMaterial({ color: "#ffffff", flatShading: true, roughness: 1 }), n);
    const o = new THREE.Object3D();
    for (let i = 0; i < n; i++) {
      const a = rnd(i, 51) * Math.PI * 2, r = 600 + Math.sqrt(rnd(i, 52)) * 40000;
      o.position.set(Math.cos(a) * r, 800 + rnd(i, 53) * 300, Math.sin(a) * r);
      const s = 300 + rnd(i, 54) * 700; o.scale.set(s * 1.8, s * 0.6, s); o.rotation.set(0, rnd(i, 55) * 6, 0);
      o.updateMatrix(); m.setMatrixAt(i, o.matrix);
    }
    return m;
  }, []);
  return <primitive object={mesh} position={[t * 30, 0, 0]} />;
};

export const Plane: React.FC<{ t: number }> = ({ t }) => {
  const x = -60000 + (t - 13.2) * 30000; // a jet crossing at 11 km during second 14, with a long contrail
  return (
    <group position={[x, 11000, 6000]}>
      <mesh rotation={[0, 0, Math.PI / 2]}><cylinderGeometry args={[180, 140, 2400, 6]} />{M("#ffffff")}</mesh>
      <mesh><boxGeometry args={[700, 60, 3200]} />{M("#d8e0f0")}</mesh>
      <mesh position={[-1100, 300, 0]}><boxGeometry args={[400, 600, 60]} />{M("#e83a5a")}</mesh>
      <mesh position={[-25000, 0, 0]}><boxGeometry args={[48000, 260, 260]} /><meshBasicMaterial color="#ffffff" transparent opacity={0.75} /></mesh>
    </group>
  );
};

// ---------- planet scale ----------
const R_EARTH = 6371000;
export const Earth: React.FC<{ opacity: number }> = ({ opacity }) => {
  const geo = useMemo(() => {
    const g = new THREE.IcosahedronGeometry(1, 6).toNonIndexed(); const pos = g.attributes.position, cols: number[] = [];
    const n3 = (x: number, y: number, z: number) => Math.sin(x * 3.1 + Math.sin(y * 2.3) * 1.7) * Math.cos(z * 2.7 + Math.sin(x * 1.9)) + 0.5 * Math.sin(x * 7.1 + z * 5.3 + y * 3.7);
    for (let i = 0; i < pos.count; i += 3) {
      const cx = (pos.getX(i) + pos.getX(i + 1) + pos.getX(i + 2)) / 3, cy = (pos.getY(i) + pos.getY(i + 1) + pos.getY(i + 2)) / 3, cz = (pos.getZ(i) + pos.getZ(i + 1) + pos.getZ(i + 2)) / 3;
      const v = cy > 0.985 ? 0.7 : n3(cx, cy, cz); // the hero stands on green land
      let c = v > 0.35 ? (v > 1.15 ? col("#c8b070") : col(v > 0.8 ? "#3a9a50" : "#4cb860")) : col(v > 0.15 ? "#2a8ae0" : "#1a5ac8");
      if (Math.abs(cx) > 0.9) c = col("#f4f8ff"); // ice caps on a pole off to the side
      for (let k = 0; k < 3; k++) cols.push(c.r, c.g, c.b);
    }
    g.setAttribute("color", new THREE.Float32BufferAttribute(cols, 3)); return g;
  }, []);
  return (
    <group position={[0, -R_EARTH, 0]}>
      <mesh geometry={geo} scale={R_EARTH} receiveShadow><meshStandardMaterial vertexColors flatShading roughness={0.95} transparent={opacity < 1} opacity={opacity} /></mesh>
      <mesh scale={R_EARTH * 1.035}><icosahedronGeometry args={[1, 3]} /><meshBasicMaterial color="#6ab8ff" transparent opacity={0.22 * opacity} side={THREE.BackSide} /></mesh>
    </group>
  );
};

// small things at huge scale get drawn as markers (sizes in hero units, not to scale)
export const Marker: React.FC<{ pos: [number, number, number]; size: number; kind: "iss" | "sat" | "moon"; h: number; spin: number }> = ({ pos, size, kind, h, spin }) => {
  const p: [number, number, number] = [pos[0] / h, pos[1] / h, pos[2] / h];
  if (kind === "moon") return (
    <group position={p}>
      <mesh rotation={[0, spin, 0]}><icosahedronGeometry args={[size, 1]} />{M("#cfcfd8")}</mesh>
      <mesh rotation={[0.3, spin, 0]} position={[size * 0.35, size * 0.3, size * 0.8]}><icosahedronGeometry args={[size * 0.22, 0]} />{M("#9a9aa8")}</mesh>
      <mesh position={[-size * 0.4, -size * 0.2, size * 0.8]}><icosahedronGeometry args={[size * 0.16, 0]} />{M("#9a9aa8")}</mesh>
    </group>
  );
  return (
    <group position={p} rotation={[0.2, spin, 0.1]} scale={size}>
      <mesh><boxGeometry args={[0.6, 0.3, 0.3]} />{M("#e8e8f0", { metalness: 0.4, roughness: 0.4 })}</mesh>
      {[-1, 1].map(sd => <mesh key={sd} position={[sd * (kind === "iss" ? 1.3 : 0.9), 0, 0]}><boxGeometry args={[kind === "iss" ? 1.6 : 1, 0.04, 0.55]} />{M("#2a4ab8", { emissive: "#1a2a8a", emissiveIntensity: 0.4, metalness: 0.5 })}</mesh>)}
    </group>
  );
};

export const Stars: React.FC<{ opacity: number }> = ({ opacity }) => {
  const geo = useMemo(() => {
    const n = 1400, a = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) { const u = rnd(i, 61) * 2 - 1, th = rnd(i, 62) * Math.PI * 2, r = Math.sqrt(1 - u * u); a.set([r * Math.cos(th) * 800, u * 800, r * Math.sin(th) * 800], i * 3); }
    const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.BufferAttribute(a, 3)); return g;
  }, []);
  return <points geometry={geo}><pointsMaterial color="#ffffff" size={2.2} sizeAttenuation={false} transparent opacity={opacity} /></points>;
};

export const Meteors: React.FC<{ t: number; h: number }> = ({ t, h }) => (
  <group>{Array.from({ length: 7 }, (_, i) => {
    const ph = ((t - 17) * 1.4 + i * 0.37) % 1, x = (rnd(i, 71) - 0.5) * 2.4 + ph * 0.6, y = (90000 + rnd(i, 72) * 30000) / h, z = 0.6 + rnd(i, 73) * 0.5;
    return <mesh key={i} position={[x, y, z]} rotation={[0, 0, -0.5]}><boxGeometry args={[0.18, 0.006, 0.006]} /><meshBasicMaterial color="#ffb05a" transparent opacity={Math.sin(ph * Math.PI)} /></mesh>;
  })}</group>
);

export const Cracks: React.FC<{ a: number }> = ({ a }) => (
  <group position={[0, 0.002, 0]}>{Array.from({ length: 9 }, (_, i) => {
    const ang = (i / 9) * Math.PI * 2 + rnd(i, 81), len = (0.25 + rnd(i, 82) * 0.6) * a;
    return <mesh key={i} position={[Math.cos(ang) * len / 2, 0, Math.sin(ang) * len / 2]} rotation={[-Math.PI / 2, 0, -ang]}><planeGeometry args={[len, 0.012]} /><meshBasicMaterial color="#2a1a1a" /></mesh>;
  })}</group>
);

// ---------- the whole scene ----------
export const Scene: React.FC<{ t: number; h: number; n: number }> = ({ t, h, n }) => {
  const { camera } = useThree();
  const alt = Math.log10(h);
  // camera: hero-relative orbit, pulling slightly wider in space
  // intro: start on the face and fly back so frame 0 is already moving
  const intro = 1 - Math.pow(1 - sat(t / 0.75), 3);
  const frac = t - Math.floor(t), drift = 1 + 0.045 * frac; // keep easing out between ticks: never a frozen frame
  const yaw = -0.35 + Math.sin(t * 0.18) * 0.25 + t * 0.012 + (1 - intro) * 0.5;
  const dist = lerp(0.75, (3.5 + sstep(4.8, 7.5, alt) * 0.6) * drift, intro);
  const shake = t > 0.9 && frac < 0.13 ? (rnd(Math.floor(t * 30), 91) - 0.5) * 0.05 * (1 - frac / 0.13) : 0;
  camera.position.set(Math.sin(yaw) * dist + shake, lerp(0.95, 0.42 + sstep(3, 6, alt) * 0.25, intro) + shake * 0.6, Math.cos(yaw) * dist);
  camera.lookAt(0, lerp(0.9, 0.8 - sstep(5.5, 7.5, alt) * 0.08, intro), 0);
  (camera as THREE.PerspectiveCamera).near = 0.002; (camera as THREE.PerspectiveCamera).far = 4e6;
  camera.updateProjectionMatrix();
  // sky: blue -> navy -> black with altitude (log10 metres of the hero's head)
  const day = col("#8ad0ff"), dusk = col("#1a2a7a"), space = col("#03040e");
  const sky = alt < 4 ? day.clone().lerp(dusk, sstep(3.6, 4.5, alt)) : dusk.clone().lerp(space, sstep(4.3, 5.1, alt));
  const ground = 1 - sstep(4.4, 5.0, alt), earthO = sstep(3.9, 4.4, alt);
  const s = 1 / h;
  return (
    <>
      <color attach="background" args={[sky]} />
      {alt < 4.6 && <fog attach="fog" args={[sky, 6, 60 + sstep(2, 4.5, alt) * 200]} />}
      <hemisphereLight args={["#cfe8ff", "#a89888", 1.0]} />
      <directionalLight position={[camera.position.x, 1.2, camera.position.z]} intensity={0.7} />
      <directionalLight position={[2.2, 3.2, 2.0]} intensity={2.4} castShadow shadow-mapSize={[2048, 2048]} shadow-camera-left={-2.5} shadow-camera-right={2.5} shadow-camera-top={2.5} shadow-camera-bottom={-2.5} shadow-camera-near={0.1} shadow-camera-far={12} shadow-bias={-0.0005} />
      <Stars opacity={sstep(4.2, 5.0, alt)} />
      <Hero t={t} lookUp={sstep(15.5, 16.5, t) - sstep(26, 27, t) + sstep(27.6, 28.2, t) * 0.8} wave={sstep(0.35, 0.55, t) * (1 - sstep(0.85, 1.0, t)) + sstep(17.6, 18.0, t) * (1 - sstep(19.2, 19.6, t))} mouthO={(t > 7.8 && t < 9) || (t > 15.8 && t < 17)} />
      {n >= 8 && ground > 0.01 && <Cracks a={sstep(8, 8.4, t) * 1.0} />}
      <group scale={s}>
        {ground > 0.01 && (
          <>
            <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow><circleGeometry args={[400000, 48]} />{M("#5aa85a")}</mesh>
            <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.01, 0]} receiveShadow><circleGeometry args={[30, 24]} />{M("#7ac870")}</mesh>
            {alt < 4.2 && <Neighbourhood t={t} />}
            {alt < 5.2 && <><BoxCity /><Tower /><Statue /></>}
            <Mountains />
          </>
        )}
        {alt > 2.4 && alt < 5.4 && <Clouds t={t} />}
        {t > 13 && t < 15.5 && <Plane t={t} />}
        {earthO > 0.01 && <Earth opacity={earthO} />}
      </group>
      {t > 16.6 && t < 18.2 && <Meteors t={t} h={h} />}
      {/* markers: iss 408 km, low sats 550 km, gps 20,200 km, geo 35,786 km, moon 384,400 km */}
      {t > 16.5 && t < 21 && <Marker kind="iss" pos={[-150000, 408000, 220000]} size={0.06} h={h} spin={t * 0.3} />}
      {t > 18 && t < 22 && [0, 1, 2, 3].map(i => <Marker key={i} kind="sat" pos={[Math.cos(t * 0.8 + i * 1.6) * 900000, 550000, Math.sin(t * 0.8 + i * 1.6) * 900000]} size={0.012} h={h} spin={t} />)}
      {t > 22.5 && t < 26 && [0, 1].map(i => <Marker key={i} kind="sat" pos={[Math.cos(t * 0.4 + i * 3) * 26000000, 20200000, Math.sin(t * 0.4 + i * 3) * 26000000]} size={0.012} h={h} spin={t} />)}
      {t > 23.5 && t < 27 && [0, 1, 2].map(i => <Marker key={i} kind="sat" pos={[Math.cos(i * 2.1) * 42164000, 35786000 * 0.1, Math.sin(i * 2.1) * 42164000]} size={0.01} h={h} spin={t} />)}
      {t > 25 && <><Marker kind="moon" pos={[150000000, 384400000, 90000000]} size={0.07} h={h} spin={t * 0.1} /><mesh position={[150000000 / h, 384400000 / h, 90000000 / h]}><sphereGeometry args={[0.11, 12, 8]} /><meshBasicMaterial color="#cfe0ff" transparent opacity={0.12} /></mesh></>}
    </>
  );
};
