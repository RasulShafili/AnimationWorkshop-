import React from "react";
import * as THREE from "three";
import { useThree } from "@react-three/fiber";
import T from "./timeline.json";
import { BlastCity, EarthBlast, Glow, sat, lerp, ease } from "./Scenes";
import { Arena } from "./Arena";
import { Planet } from "./Planet";
import { Boxer, Pose } from "./Boxer";
import { GLTF } from "three/examples/jsm/loaders/GLTFLoader.js";

const B = T.beats;
export const beatOf = (f: number) => { let i = 0; while (i < B.length - 2 && f >= B[i + 1]) i++; return i; };
const V = (x: number, y: number, z: number) => new THREE.Vector3(x, y, z);
export const sceneFrame = (f: number) => (f >= B[1] && f < B[2] ? Math.max(0, 96 - (f - B[1]) * 3.2) : f);
const HIT = 12; // frames from punch start to impact
const punchPose = (f: number, hits: number[]): Pose => { for (const j of hits) if (f >= j - HIT && f < j + 16) return { clip: "Punch", t: (f - j + HIT) / 30 }; return { clip: "Idle", t: f / 30 }; };

export const World: React.FC<{ f: number; glb: Record<string, GLTF> | null }> = ({ f: f0, glb }) => {
  const { camera, scene } = useThree();
  const pc = camera as THREE.PerspectiveCamera, f = sceneFrame(f0), b = beatOf(f0);
  const set = (pos: THREE.Vector3, look: THREE.Vector3, fov: number, shake = 0) => {
    pc.position.set(pos.x + Math.sin(f * 2.3) * shake, pos.y + Math.cos(f * 1.9) * shake, pos.z); pc.up.set(0, 1, 0); pc.lookAt(look); pc.fov = fov; pc.near = 0.05; pc.far = 900; pc.updateProjectionMatrix();
  };
  scene.fog = null;
  const planetShot = (crackAt: number, breakAt: number, boil: number, d0: number, d1: number, span: number) => {
    const crack = sat((f - crackAt) / (breakAt - crackAt)), s = f >= breakAt ? f - breakAt : -1;
    const sh = s >= 0 && s < 30 ? (1 - s / 30) * 0.5 : crack > 0 && s < 0 ? crack * 0.08 : 0;
    set(V(0, 1.0, lerp(d0, d1, ease(sat((f - breakAt + 20) / span)))), V(0, 0.2, 0), 42, sh);
    // the punch landing: a bright streak and impact flare on the face of the planet
    const hit = sat(1 - Math.abs(f - crackAt) / 6);
    return <group>
      <color attach="background" args={["#020208"]} />
      <Planet f={f} boil={boil} crack={crack} shatter={s} spin={-0.3 + f * 0.001} />
      {hit > 0 && <Glow size={6 * hit} color="#ffffff" opacity={hit} pos={[0.3, 0.9, 3.1]} />}
      {f >= crackAt - 6 && f < crackAt + 2 && <mesh position={[3, 4, 6]} rotation={[0, 0, 0.9]}><cylinderGeometry args={[0.05, 0.4, 9, 6]} /><meshBasicMaterial color={new THREE.Color(4, 3, 2)} toneMapped={false} transparent opacity={0.8} /></mesh>}
      <ambientLight intensity={0.3} /><directionalLight position={[-5, 3, 6]} intensity={2.4} />
    </group>;
  };
  if (b <= 1) return planetShot(T.crack, T.shatter, 0.25, 15, 19, 60);
  if (!glb) return null;
  const g = glb["man.glb"], top = 1.0;
  if (b === 2 || b === 3) {
    const pose = punchPose(f, [...T.jabs, T.ko]);
    const lastHit = [...T.jabs].reverse().find(j => f >= j);
    const lean = lastHit !== undefined ? Math.exp(-(f - lastHit) / 6) * 0.6 : 0;
    const k = f - T.ko;
    let opp = <Boxer g={g} pose={{ clip: "Idle", t: f / 30 + 1.3, lean }} pos={[0.78, top, 0]} ry={-Math.PI / 2} shorts="#2a5ad8" glove="#2a5ad8" skin="#a87050" />;
    if (k >= 0) opp = <Boxer g={g} pose={{ clip: "Death", t: k / 30 * 1.6 }} pos={[0.78 + k * 0.13, top + Math.max(-top, k * 0.1 - k * k * 0.0018), 0]} ry={-Math.PI / 2} rz={-k * 0.06} shorts="#2a5ad8" glove="#2a5ad8" skin="#a87050" />;
    if (b === 2) set(V(lerp(-0.8, 0.8, (f - B[2]) / 200), 2.2, lerp(6.2, 5.4, (f - B[2]) / 200)), V(0, 1.85, 0), 40, lastHit !== undefined && f - lastHit < 5 ? 0.02 : 0);
    else set(V(0.8 + sat(k / 40) * 1.5, 2.4, 6.0 + sat(k / 40) * 3), V(lerp(0, 2.6, sat(k / 45)), lerp(1.8, 2.0, sat(k / 45)), 0), 42, k >= 0 && k < 8 ? 0.08 : 0);
    return <group><Arena f={f} /><Boxer g={g} pose={pose} pos={[-0.78, top, 0]} ry={Math.PI / 2} />{opp}</group>;
  }
  if (b === 4) {
    const t = f - T.tnt, R = t < 0 ? 0 : 0.6 + Math.pow(sat(t / 40), 0.5) * 3.2;
    set(V(lerp(-1, 1, (f - B[4]) / 90), 3.2, lerp(9.5, 13, sat(t / 60))), V(0, 2.4, 0), 46, t >= 0 && t < 25 ? (1 - t / 25) * 0.35 : 0);
    return <group>
      <Arena f={f} blast={t > 0 ? sat(t / 40) : 0} />
      <Boxer g={g} pose={{ ...punchPose(f, [T.tnt]), glow: sat((f - T.tnt + 30) / 30) * 2.5 }} pos={[-0.78, top, 0]} ry={Math.PI / 2} />
      {t >= 0 && <group position={[0.4, 2.3, 0]}>
        <mesh scale={R}><icosahedronGeometry args={[1, 2]} /><meshBasicMaterial color={new THREE.Color(2.0, 0.9, 0.3).lerp(new THREE.Color(0.8, 0.22, 0.08), sat(t / 40))} toneMapped={false} transparent opacity={sat(1 - (t - 30) / 40)} /></mesh>
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -1.2, 0]}><ringGeometry args={[Math.max(0.1, t * 0.35 - 0.6), t * 0.35, 48]} /><meshBasicMaterial color={new THREE.Color(3, 2.4, 1.6)} toneMapped={false} transparent opacity={sat(1 - t / 50)} side={THREE.DoubleSide} /></mesh>
        <pointLight intensity={80 * sat(1 - t / 60)} distance={40} color="#ffa060" />
      </group>}
    </group>;
  }
  if (b === 5) {
    const t = f - T.hiro, sh = t >= 0 && t < 30 ? (1 - t / 30) * 2 : 0;
    set(V(lerp(70, 85, sat((f - B[5]) / 80)), 22, lerp(80, 100, sat((f - B[5]) / 80))), V(0, lerp(10, 30, sat(t / 60)), 0), 50, sh);
    return <BlastCity f={f} boom={T.hiro} spoonIn={1e9} mush />;
  }
  if (b === 6) { const t = f - T.astro; set(V(0, 1.2, lerp(14, 16, sat(t / 90))), V(0, 0.4, 0), 42, t >= 0 && t < 20 ? (1 - t / 20) * 0.3 : 0); return <EarthBlast f={f} t={t} />; }
  if (b === 7) { set(V(0, 1.0, lerp(16, 14, (f - B[7]) / 80)), V(0, 0.2, 0), 42); return <group><color attach="background" args={["#020208"]} /><Planet f={f} boil={ease((f - B[7] - 5) / 55)} spin={-0.3 + f * 0.001} /><ambientLight intensity={0.3} /><directionalLight position={[-5, 3, 6]} intensity={2.4} /></group>; }
  if (b === 8 && f < T.last + 19) {
    const charge = sat((f - T.bell) / (T.last - T.bell));
    set(V(lerp(1.4, 0.4, (f - B[8]) / 125), lerp(1.6, 1.9, charge), lerp(4.6, 3.2, ease(charge))), V(-0.4, 1.8, 0), 40, charge * 0.03);
    return <group><Arena f={f} ruin={1} /><Boxer g={g} pose={{ ...punchPose(f, [T.last]), glow: charge * 4 }} pos={[-0.78, top, 0]} ry={Math.PI / 2 - 0.5} /></group>;
  }
  return planetShot(T.last + 19, T.shatter2, 1, 16, 26, 160);
};
