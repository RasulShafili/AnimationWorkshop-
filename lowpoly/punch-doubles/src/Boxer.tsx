// CC0 rigged man (public/man.glb) as a boxer: shirtless, coloured shorts, boots, gloves on the palm bones.
import React, { useMemo } from "react";
import * as THREE from "three";
import { GLTF } from "three/examples/jsm/loaders/GLTFLoader.js";
import * as SkeletonUtils from "three/examples/jsm/utils/SkeletonUtils.js";

export const SCALE = 1.8 / 4.82;
export type Pose = { clip: "Idle" | "Punch" | "Death" | "Clapping" | "Standing"; t: number; lean?: number; glow?: number };

const build = (g: GLTF, shorts: string, glove: string, skin: string) => {
  const root = SkeletonUtils.clone(g.scene); root.updateMatrixWorld(true);
  const bones: Record<string, THREE.Bone> = {}, mats: Record<string, THREE.MeshStandardMaterial> = {};
  root.traverse((o: any) => {
    if (o.isBone) { bones[o.name] = o; o.userData.q = o.quaternion.clone(); o.userData.p = o.position.clone(); }
    if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; o.frustumCulled = false; const m = o.material.clone(); m.flatShading = true; m.roughness = 0.6; o.material = m; mats[m.name] = m; }
  });
  mats.Skin.color.set(skin); mats.Shirt.color.set(skin); mats.Pants.color.set(shorts); mats.Socks.color.set("#1a1a22"); mats.Hair.color.set("#1e1814");
  const mixer = new THREE.AnimationMixer(root), actions: Record<string, THREE.AnimationAction> = {}, durs: Record<string, number> = {};
  for (const n of ["Idle", "Punch", "Death", "Clapping", "Standing"]) { const c = g.animations.find(a => a.name.endsWith("Man_" + n))!; actions[n] = mixer.clipAction(c); durs[n] = c.duration; }
  const gloveMat = new THREE.MeshStandardMaterial({ color: glove, roughness: 0.35, metalness: 0.05, emissive: glove, emissiveIntensity: 0 });
  const gloves: THREE.Group[] = [];
  for (const side of ["L", "R"]) {
    const palm = bones["Palm." + side] ?? bones["Palm" + side], ws = new THREE.Vector3(); palm.getWorldScale(ws);
    const hold = new THREE.Group(); hold.scale.set(1 / ws.x, 1 / ws.y, 1 / ws.z); palm.add(hold);
    const gl = new THREE.Group(); gl.position.set(0, 0.16, 0.02); hold.add(gl);
    const ball = new THREE.Mesh(new THREE.SphereGeometry(0.2, 14, 10), gloveMat); ball.scale.set(1, 1.25, 1.1); ball.castShadow = true; gl.add(ball);
    const cuff = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.12, 0.16, 10), new THREE.MeshStandardMaterial({ color: "#f2f2f2", roughness: 0.6 })); cuff.position.y = -0.2; gl.add(cuff);
    gloves.push(gl);
  }
  return { root, bones, mats, mixer, actions, durs, gloveMat, gloves };
};

export const Boxer: React.FC<{ g: GLTF; pose: Pose; pos: [number, number, number]; ry: number; rz?: number; shorts?: string; glove?: string; skin?: string }> =
  ({ g, pose, pos, ry, rz = 0, shorts = "#c0262e", glove = "#d81e2a", skin = "#c98a62" }) => {
  const r = useMemo(() => build(g, shorts, glove, skin), [g, shorts, glove, skin]);
  Object.values(r.bones).forEach(b => { b.quaternion.copy(b.userData.q); b.position.copy(b.userData.p); });
  r.mixer.stopAllAction(); const a = r.actions[pose.clip]; a.play();
  const d = r.durs[pose.clip];
  r.mixer.setTime(pose.clip === "Death" ? Math.min(Math.max(0, pose.t), d - 0.01) : ((pose.t % d) + d) % d);
  if (pose.lean) { r.bones.Torso.rotateX(-pose.lean * 0.5); r.bones.Head.rotateX(-pose.lean * 0.6); }
  r.gloveMat.emissiveIntensity = pose.glow ?? 0;
  return <primitive object={r.root} position={pos} rotation={[0, ry, rz]} scale={SCALE} />;
};
