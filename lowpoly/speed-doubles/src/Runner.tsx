// CC0 rigged man (public/man.glb) as a runner: teal top, black shorts, white shoes. heat 0..1 makes him glow
// (shoes first, then the whole body) — air friction at hypersonic speed.
import React, { useMemo } from "react";
import * as THREE from "three";
import { GLTF } from "three/examples/jsm/loaders/GLTFLoader.js";
import * as SkeletonUtils from "three/examples/jsm/utils/SkeletonUtils.js";

export const SCALE = 1.8 / 4.82;
const build = (g: GLTF) => {
  const root = SkeletonUtils.clone(g.scene); root.updateMatrixWorld(true);
  const bones: Record<string, THREE.Bone> = {}, mats: Record<string, THREE.MeshStandardMaterial> = {};
  root.traverse((o: any) => {
    if (o.isBone) { bones[o.name] = o; o.userData.q = o.quaternion.clone(); o.userData.p = o.position.clone(); }
    if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; o.frustumCulled = false; const m = o.material.clone(); m.flatShading = true; m.roughness = 0.6; o.material = m; mats[m.name] = m; }
  });
  mats.Skin.color.set("#c98a62"); mats.Shirt.color.set("#18c8a0"); mats.Pants.color.set("#1a1a26"); mats.Socks.color.set("#f4f4f4"); mats.Hair.color.set("#1e1814");
  const mixer = new THREE.AnimationMixer(root), actions: Record<string, THREE.AnimationAction> = {}, durs: Record<string, number> = {};
  for (const n of ["Run", "Idle", "RunningJump"]) { const c = g.animations.find(a => a.name.endsWith("Man_" + n))!; actions[n] = mixer.clipAction(c); durs[n] = c.duration; }
  return { root, bones, mats, mixer, actions, durs };
};
const HOT = new THREE.Color("#ff6a1a"), WHITE = new THREE.Color("#fff2d8");
export const Runner: React.FC<{ g: GLTF; clip?: "Run" | "Idle" | "RunningJump"; t: number; heat?: number; pos: [number, number, number]; ry: number; rz?: number }> =
  ({ g, clip = "Run", t, heat = 0, pos, ry, rz = 0 }) => {
  const r = useMemo(() => build(g), [g]);
  Object.values(r.bones).forEach(b => { b.quaternion.copy(b.userData.q); b.position.copy(b.userData.p); });
  r.mixer.stopAllAction(); r.actions[clip].play(); const d = r.durs[clip]; r.mixer.setTime(((t % d) + d) % d);
  const shoe = Math.min(1, heat * 2), body = Math.max(0, heat * 2 - 1);
  const col = HOT.clone().lerp(WHITE, body);
  r.mats.Socks.emissive.copy(col); r.mats.Socks.emissiveIntensity = shoe * 3;
  for (const n of ["Skin", "Shirt", "Pants", "Hair"]) { r.mats[n].emissive.copy(col); r.mats[n].emissiveIntensity = body * 2.5; }
  return <primitive object={r.root} position={pos} rotation={[0, ry, rz]} scale={SCALE} />;
};
