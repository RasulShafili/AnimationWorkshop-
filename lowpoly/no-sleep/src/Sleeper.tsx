// The CC0 rigged man (public/man.glb) as a sleep-deprived guy: clip playback + eyelids, eye bags, head nod, pale skin.
import React, { useMemo } from "react";
import * as THREE from "three";
import { GLTF } from "three/examples/jsm/loaders/GLTFLoader.js";
import * as SkeletonUtils from "three/examples/jsm/utils/SkeletonUtils.js";

export const SCALE = 1.8 / 4.82;
export type Pose = { clip: "Idle" | "Walk" | "Sitting" | "Death"; t: number; lids?: number; bags?: number; nod?: number; pale?: number; turn?: number };
const SKIN = new THREE.Color("#d79a72"), PALE = new THREE.Color("#c8b0a8");

const build = (g: GLTF) => {
  const root = SkeletonUtils.clone(g.scene); root.updateMatrixWorld(true);
  const bones: Record<string, THREE.Bone> = {}, mats: Record<string, THREE.MeshStandardMaterial> = {};
  root.traverse((o: any) => {
    if (o.isBone) { bones[o.name] = o; o.userData.q = o.quaternion.clone(); o.userData.p = o.position.clone(); }
    if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; o.frustumCulled = false; const m = o.material.clone(); m.flatShading = true; m.roughness = 0.75; o.material = m; mats[m.name] = m; }
  });
  mats.Shirt.color.set("#6a5ab0"); mats.Pants.color.set("#2c2c3a"); mats.Socks.color.set("#e8e8e8"); mats.Hair.color.set("#2e2420");
  const mixer = new THREE.AnimationMixer(root), actions: Record<string, THREE.AnimationAction> = {}, durs: Record<string, number> = {};
  for (const n of ["Idle", "Walk", "Sitting", "Death"]) { const c = g.animations.find(a => a.name.endsWith("Man_" + n))!; actions[n] = mixer.clipAction(c); durs[n] = c.duration; }
  // attachments in model units on the head bone (the armature is scaled, so cancel that scale)
  const head = bones.Head, ws = new THREE.Vector3(); head.getWorldScale(ws);
  const hold = new THREE.Group(); hold.scale.set(1 / ws.x, 1 / ws.y, 1 / ws.z); head.add(hold);
  const lids: THREE.Mesh[] = [], bags: THREE.Mesh[] = [];
  const bagMat = new THREE.MeshStandardMaterial({ color: "#6a4060", transparent: true, opacity: 0, roughness: 0.9 });
  for (const s of [-1, 1]) {
    const lid = new THREE.Mesh(new THREE.BoxGeometry(0.105, 0.07, 0.04), mats.Skin); lid.position.set(s * 0.105, 0.3, 0.325); hold.add(lid); lids.push(lid);
    const bag = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.02, 0.02), bagMat); bag.position.set(s * 0.105, 0.215, 0.335); hold.add(bag); bags.push(bag);
  }
  return { root, bones, mats, mixer, actions, durs, lids, bags, bagMat };
};

export const Sleeper: React.FC<{ g: GLTF; pose: Pose; pos: [number, number, number]; ry: number; rz?: number }> = ({ g, pose, pos, ry, rz = 0 }) => {
  const r = useMemo(() => build(g), [g]);
  Object.values(r.bones).forEach(b => { b.quaternion.copy(b.userData.q); b.position.copy(b.userData.p); });
  r.mixer.stopAllAction(); const a = r.actions[pose.clip]; a.play();
  const d = r.durs[pose.clip]; r.mixer.setTime(pose.clip === "Death" ? Math.min(Math.max(0, pose.t), d - 0.01) : ((pose.t % d) + d) % d);
  const nod = pose.nod ?? 0; if (nod) { r.bones.Head.rotateX(nod * 0.75); r.bones.Neck.rotateX(nod * 0.35); r.bones.Torso.rotateX(nod * 0.12); }
  if (pose.turn) { r.bones.Head.rotateY(pose.turn * 0.7); r.bones.Torso.rotateY(pose.turn * 0.3); }
  const lids = pose.lids ?? 0;
  r.lids.forEach(l => { l.visible = lids > 0.2; l.scale.y = Math.max(0.05, lids); l.position.y = 0.31 - 0.035 * lids; });
  r.bagMat.opacity = (pose.bags ?? 0) * 0.85; r.bags.forEach(b => (b.visible = (pose.bags ?? 0) > 0.03));
  r.mats.Skin.color.copy(SKIN).lerp(PALE, pose.pale ?? 0);
  return <primitive object={r.root} position={pos} rotation={[0, ry, rz]} scale={SCALE} />;
};
