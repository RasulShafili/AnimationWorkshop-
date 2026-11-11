import React from "react";
import * as THREE from "three";
import { useThree } from "@react-three/fiber";
import T from "./timeline.json";
import { BlastCity, EarthBlast, Glow, sat, lerp, ease } from "./Scenes";
import { Arena } from "./Arena";
import { Planet } from "./Planet";
import { Boxer, Pose } from "./Boxer";
import { Exterior, Hall, Beam } from "./Exterior";
import { GLTF } from "three/examples/jsm/loaders/GLTFLoader.js";

const B = T.beats, H = T.hits;
export const beatOf = (f: number) => { let i = 0; while (i < B.length - 2 && f >= B[i + 1]) i++; return i; };
const V = (x: number, y: number, z: number) => new THREE.Vector3(x, y, z);
const HIT = 12; // frames from punch start to impact
const punchPose = (f: number, hit: number, glow = 0): Pose => (f >= hit - HIT && f < hit + 16 ? { clip: "Punch", t: (f - hit + HIT) / 30, glow } : { clip: "Idle", t: f / 30, glow });
const OPP = { shorts: "#2a5ad8", glove: "#2a5ad8", skin: "#a87050" };
const top = 1.0, BX = -0.6, OX = 0.6;

export const World: React.FC<{ f: number; glb: Record<string, GLTF> | null }> = ({ f, glb }) => {
  const { camera, scene } = useThree();
  const pc = camera as THREE.PerspectiveCamera, b = beatOf(f);
  const set = (pos: THREE.Vector3, look: THREE.Vector3, fov: number, shake = 0) => {
    pc.position.set(pos.x + Math.sin(f * 2.3) * shake, pos.y + Math.cos(f * 1.9) * shake, pos.z); pc.up.set(0, 1, 0); pc.lookAt(look); pc.fov = fov; pc.near = 0.05; pc.far = 900; pc.updateProjectionMatrix();
  };
  scene.fog = null;
  if (!glb) return null;
  const g = glb["man.glb"], h = H[Math.min(b, H.length - 1)], k = f - h;
  const hitShake = (amp: number, len = 10) => (k >= 0 && k < len ? (1 - k / len) * amp : 0);
  const impact = (pos: [number, number, number], size: number) => k >= 0 && k < 8 ? <Glow size={size * (1 - k / 8)} color="#fff4e0" opacity={1 - k / 8} pos={pos} /> : null;
  const boxer = (glow: number) => <Boxer g={g} pose={punchPose(f, h, glow)} pos={[BX, top, 0]} ry={Math.PI / 2} />;

  // ---- 1-3: in the ring, close range
  if (b <= 2) {
    let opp;
    if (b === 0) opp = <Boxer g={g} pose={{ clip: "Idle", t: f / 30 + 1.3, lean: k >= 0 ? Math.exp(-k / 7) * 0.7 : 0 }} pos={[OX, top, 0]} ry={-Math.PI / 2} {...OPP} />;
    else if (b === 1) opp = k >= 0 ? <Boxer g={g} pose={{ clip: "Death", t: k / 30 * 1.3 }} pos={[OX + Math.min(k, 10) * 0.03, top, 0]} ry={-Math.PI / 2} {...OPP} /> : <Boxer g={g} pose={{ clip: "Idle", t: f / 30 + 1.3 }} pos={[OX, top, 0]} ry={-Math.PI / 2} {...OPP} />;
    else {
      const x = OX + Math.max(0, k) * 0.16, inRing = x < 3.4, y = k < 0 ? top : Math.max(inRing ? top : 0, top + k * 0.12 - k * k * 0.0018);
      opp = k < 0 ? <Boxer g={g} pose={{ clip: "Idle", t: f / 30 + 1.3 }} pos={[OX, top, 0]} ry={-Math.PI / 2} {...OPP} /> : <Boxer g={g} pose={{ clip: "Death", t: Math.min(k / 30 * 1.6, 1.2) + (y <= 0.01 ? 1 : 0) }} pos={[x, y, 0]} ry={-Math.PI / 2} rz={-Math.min(k, 30) * 0.03} {...OPP} />;
    }
    const u = (f - B[b]) / (B[b + 1] - B[b]);
    if (b === 0) set(V(lerp(-0.4, 0.4, u), 2.0, lerp(4.4, 3.8, u)), V(0, 1.75, 0), 40, hitShake(0.02));
    if (b === 1) set(V(lerp(1.6, 1.0, u), 1.3, lerp(3.6, 3.2, u)), V(0, 1.4, 0), 42, hitShake(0.04));
    if (b === 2) set(V(1.5 + sat(k / 40) * 2, 2.3, 5.2 + sat(k / 40) * 3), k < 0 ? V(0, 1.7, 0) : V((OX + k * 0.16) * 0.8, Math.max(1.6, top + k * 0.12 - k * k * 0.0018), 0), 42, hitShake(0.08));
    return <group><Arena f={f} />{boxer(b * 0.4)}{opp}{impact([0.1, 2.2, 0], 0.6 + b * 0.5)}</group>;
  }
  // ---- 4: launched at 45° up through the roof, then seen from outside
  if (b === 3) {
    if (f < T.outside) {
      const x = OX + Math.max(0, k) * 0.28, y = top + Math.max(0, k) * 0.28;
      const opp = k < 0 ? <Boxer g={g} pose={{ clip: "Idle", t: f / 30 + 1.3 }} pos={[OX, top, 0]} ry={-Math.PI / 2} {...OPP} /> : <Boxer g={g} pose={{ clip: "Death", t: 0.9 }} pos={[x, y, 0]} ry={-Math.PI / 2} rz={-0.8} {...OPP} />;
      set(V(k < 0 ? -0.5 : -1.5, k < 0 ? 1.8 : 1.4, k < 0 ? 4.6 : 7), V(k < 0 ? 0 : x * 0.6, k < 0 ? 1.7 : 1.7 + y * 0.6, 0), k < 0 ? 40 : 55, hitShake(0.12));
      return <group><Arena f={f} blast={k > 0 ? 0.05 : 0} />{boxer(1.4)}{opp}{impact([0.1, 2.2, 0], 2.5)}</group>;
    }
    const l = f - T.outside;
    set(V(lerp(-40, -50, l / 55), lerp(14, 22, l / 55), lerp(55, 65, l / 55)), V(lerp(8, 30, sat(l / 50)), lerp(18, 34, sat(l / 50)), 0), 50);
    return <Exterior f={f} g={g} launch={l + 4} />;
  }
  // ---- 5: the punch becomes a beam; the arena explodes
  if (b === 4) {
    if (f < T.beamOut) {
      const len = k < 0 ? 0 : Math.min(60, k * 6);
      set(V(k < 0 ? 1.8 : 2.6, 1.9, k < 0 ? 3.0 : 5), V(k < 0 ? -0.2 : 2, 2.0, 0), 44, hitShake(0.1, 20));
      return <group><Arena f={f} blast={k > 0 ? sat(k / 20) : 0} />{boxer(2)}{k >= 0 && <Beam len={len} w={0.12} pos={[0.2, 2.25, 0]} />}{impact([0.2, 2.25, 0], 2)}</group>;
    }
    const l = f - T.beamOut, boom = T.beamOut + 6;
    set(V(lerp(60, 75, sat(l / 60)), lerp(20, 28, sat(l / 60)), lerp(70, 90, sat(l / 60))), V(0, lerp(8, 20, sat(l / 50)), 0), 50, l >= 6 && l < 30 ? (1 - (l - 6) / 24) * 1.5 : 0);
    return <group>
      <BlastCity f={f} boom={boom} spoonIn={1e9} />
      {l < 14 && <Hall />}
      {l < 30 && <Beam len={Math.min(400, l * 40)} w={0.5} pos={[13, 7, 0]} o={sat(1 - (l - 10) / 20)} />}
    </group>;
  }
  // ---- 6-10: a short shot of the punch in the burnt ring, then the planet from space
  if (f < h + 3) {
    const glow = 2 + (b - 5) * 1.2;
    const cams: [THREE.Vector3, THREE.Vector3][] = [[V(2.4, 1.6, 0.8), V(BX, 1.75, 0)], [V(0.3, 1.9, 3.4), V(0, 1.8, 0)], [V(1.6, 0.9, 1.8), V(BX, 2.0, 0)], [V(1.5, 1.85, 0.3), V(BX, 1.8, 0)], [V(3.2, 2.6, 4.2), V(0, 1.8, 0)]];
    const [cp, cl] = cams[b - 5];
    set(cp, cl, 42, f > h - 4 ? 0.03 : 0);
    return <group><Arena f={f} ruin={1} />{boxer(glow)}</group>;
  }
  if (b === 5) { set(V(0, 1.6, lerp(15, 19, sat(k / 70))), V(0, 1.0, 0), 42, hitShake(0.3, 15)); return <EarthBlast f={f} t={k * 0.6} beam={Math.min(14, k * 0.6)} />; }
  if (b === 6) { set(V(0, 1.2, lerp(14, 16, sat(k / 70))), V(0, 0.4, 0), 42, hitShake(0.4, 15)); return <EarthBlast f={f} t={60 + k * 1.5} />; }
  const planet = (boil: number, crack: number, shatter: number, d: number) => {
    set(V(0, 1.0, d), V(0, 0.2, 0), 42, hitShake(0.4, 15));
    return <group><color attach="background" args={["#020208"]} /><Planet f={f} boil={boil} crack={crack} shatter={shatter} spin={-0.3 + f * 0.001} />{impact([0.3, 0.9, 3.1], 5)}<ambientLight intensity={0.3} /><directionalLight position={[-5, 3, 6]} intensity={2.4} /></group>;
  };
  if (b === 7) return planet(ease(k / 45), 0, -1, lerp(16, 14.5, sat(k / 80)));
  if (b === 8) return planet(1, 0.25 + 0.35 * ease(k / 40), -1, lerp(15, 14, sat(k / 80)));
  const s = f - (H[9] + 6);
  return planet(1, sat(0.6 + k / 15), s, lerp(15, 26, ease(sat((s + 10) / 150))));
};
