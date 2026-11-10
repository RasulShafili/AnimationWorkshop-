// The hero is a professional CC0 rigged model (Quaternius "BaseHuman", public/man.glb, via poly.pizza).
// We drive it with: the Idle clip, aimed bones for curl / double-biceps / hunch, bone scaling for muscle,
// material colours for flush / shirt-off / balding, and meshes parented to bones for beard, acne, pecs, sweat.
import React, { useMemo } from "react";
import * as THREE from "three";
import { GLTF } from "three/examples/jsm/loaders/GLTFLoader.js";
import * as SkeletonUtils from "three/examples/jsm/utils/SkeletonUtils.js";
import type { Look } from "./Man";

const sat = (v: number) => Math.min(1, Math.max(0, v));
const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
const V = (x: number, y: number, z: number) => new THREE.Vector3(x, y, z);
export const MODEL_H = 4.82, SCALE = 1.8 / MODEL_H;

type Rig = {
  root: THREE.Object3D; mixer: THREE.AnimationMixer; idle: THREE.AnimationAction;
  bones: Record<string, THREE.Bone>; mats: Record<string, THREE.MeshStandardMaterial>;
  extra: Record<string, THREE.Object3D>;
  bulk: (factors: Record<string, number>) => void;
};
const SKIN = new THREE.Color("#d79a72"), FLUSH = new THREE.Color("#e0705e"), HAIR = new THREE.Color("#2e2420");

const std = (c: string, r = 0.75) => new THREE.MeshStandardMaterial({ color: c, roughness: r, flatShading: true });

const build = (g: GLTF): Rig => {
  const root = SkeletonUtils.clone(g.scene);
  root.updateMatrixWorld(true);
  // attach `obj` to `bone`, with positions given in model units relative to the bone's rest frame;
  // `front`: optional world-space offset (model units) converted into the bone's local frame
  const attach = (bone: THREE.Object3D, obj: THREE.Object3D, worldOff?: THREE.Vector3) => {
    const ws = new THREE.Vector3(); bone.getWorldScale(ws);
    const w = new THREE.Group(); w.scale.set(1 / ws.x, 1 / ws.y, 1 / ws.z);
    if (worldOff) { const q = new THREE.Quaternion(); bone.getWorldQuaternion(q); obj.position.add(worldOff.clone().applyQuaternion(q.invert())); }
    w.add(obj); bone.add(w); return w;
  };
  const bones: Record<string, THREE.Bone> = {}, mats: Record<string, THREE.MeshStandardMaterial> = {};
  const skinned: THREE.SkinnedMesh[] = [];
  root.traverse((o: any) => {
    if (o.isBone) bones[o.name] = o;
    if (o.isSkinnedMesh) { o.geometry = o.geometry.clone(); skinned.push(o); }
    if (o.isMesh) {
      o.castShadow = true; o.receiveShadow = true; o.frustumCulled = false;
      const m = (o.material as THREE.MeshStandardMaterial).clone(); m.flatShading = true; m.roughness = 0.7; o.material = m; mats[m.name] = m;
    }
  });
  mats.Shirt.color.set("#2f9fd0"); mats.Pants.color.set("#22284a"); mats.Socks.color.set("#f2f2f2"); mats.Hair.color.copy(HAIR); mats.Skin.color.copy(SKIN);
  const mixer = new THREE.AnimationMixer(root);
  const idle = mixer.clipAction(g.animations.find(a => a.name.includes("Idle"))!); idle.play();
  const skinMat = mats.Skin;
  // ---- attachments (model units; the head bone sits at the base of the skull, y up, z forward) ----
  const head = bones.Head, torso = bones.Torso, palmR = bones.PalmR;
  const beard = new THREE.Group();
  const beardMat = std("#4a3226", 0.95);
  const chin = new THREE.Mesh(new THREE.SphereGeometry(0.325, 14, 9, Math.PI * 0.2, Math.PI * 0.6, Math.PI * 0.56, Math.PI * 0.32), beardMat);
  chin.position.set(0, 0.16, 0.03); chin.material.side = THREE.DoubleSide;
  const goatee = new THREE.Mesh(new THREE.IcosahedronGeometry(0.13, 1), beardMat); goatee.scale.set(1.25, 0.75, 0.7); goatee.position.set(0, -0.06, 0.26);
  const stache = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.04, 0.07), beardMat); stache.position.set(0, 0.07, 0.34);
  beard.add(chin, goatee, stache); attach(head, beard);
  const acne = new THREE.Group(), acneMat = std("#c03040", 0.4);
  [[-0.17, 0.16, 0.31], [0.18, 0.14, 0.31], [-0.13, 0.08, 0.32], [0.15, 0.21, 0.31], [0.03, 0.4, 0.33], [-0.09, 0.43, 0.32], [0.2, 0.07, 0.28], [-0.21, 0.1, 0.27]]
    .forEach(([x, y, z]) => { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(0.022, 1), acneMat); m.position.set(x, y, z); acne.add(m); });
  attach(head, acne);
  const sweat = new THREE.Group(), sweatMat = new THREE.MeshStandardMaterial({ color: "#d8f2ff", roughness: 0.05, metalness: 0.2, transparent: true });
  for (let i = 0; i < 3; i++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(0.022, 1), sweatMat); m.scale.set(0.8, 1.3, 0.8); sweat.add(m); }
  attach(head, sweat);
  // pecs + abs on the torso bone, visible once the shirt is gone
  const pecs = new THREE.Group();
  [-1, 1].forEach(s => { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(0.2, 2), skinMat); m.position.set(s * 0.17, 0.42, 0.2); m.scale.set(1.1, 0.75, 0.42); m.castShadow = true; pecs.add(m); });
  attach(torso, pecs);
  const abs = new THREE.Group();
  for (let r = 0; r < 3; r++) [-1, 1].forEach(s => { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(0.07, 1), skinMat); m.position.set(s * 0.08, 0.52 - r * 0.15, 0.27); m.scale.set(1, 0.85, 0.35); abs.add(m); });
  attach(bones.Abdomen, abs);
  const muscles: THREE.Mesh[] = [];
  for (const sd of ["L", "R"]) {
    const ua = bones["UpperArm" + sd], side = sd === "L" ? 1 : -1;
    const bic = new THREE.Mesh(new THREE.IcosahedronGeometry(0.13, 1), skinMat); bic.position.set(0, 0.32, 0); bic.castShadow = true;
    const g1 = new THREE.Group(); g1.add(bic); attach(ua, g1); bic.userData.front = V(0, 0, 0.07); muscles.push(bic);
    const q = new THREE.Quaternion(); ua.getWorldQuaternion(q); bic.position.add(V(0, 0, 0.07).applyQuaternion(q.clone().invert()));
    const del = new THREE.Mesh(new THREE.IcosahedronGeometry(0.16, 1), mats.Shirt); del.position.set(0, 0.06, 0); del.position.add(V(side * 0.05, 0.02, 0).applyQuaternion(q.clone().invert())); del.castShadow = true;
    const g2 = new THREE.Group(); g2.add(del); attach(ua, g2); muscles.push(del);
  }
  const group: { m: THREE.Mesh; k: number; cover?: "Shirt" | "Pants" }[] = [];
  const addM = (bone: string, local: THREE.Vector3, worldOff: THREE.Vector3, r: number, sc: THREE.Vector3, k: number, cover?: "Shirt" | "Pants") => {
    const bn = bones[bone], q = new THREE.Quaternion(); bn.getWorldQuaternion(q);
    const m = new THREE.Mesh(new THREE.IcosahedronGeometry(r, 1), skinMat); m.castShadow = true;
    m.position.copy(local).add(worldOff.clone().applyQuaternion(q.invert())); m.userData.base = sc.clone();
    const gg = new THREE.Group(); gg.add(m); attach(bn, gg); group.push({ m, k, cover });
  };
  for (const [sd, sx] of [["L", 1], ["R", -1]] as const) {
    addM("Torso", V(sx * 0.17, 0.86, -0.06), V(0, 0, 0), 0.17, V(1.3, 0.6, 0.85), 1, "Shirt");          // traps
    addM("Torso", V(sx * 0.29, 0.3, -0.04), V(0, 0, 0), 0.19, V(0.75, 1.45, 0.95), 1, "Shirt");        // lats
    addM("LowerArm" + sd, V(0, 0.22, 0), V(0, 0, 0.02), 0.1, V(1, 1.7, 1), 0.8);                       // forearms
    addM("LowerLeg" + sd, V(0, 0.28, 0), V(0, 0, -0.07), 0.12, V(1, 1.6, 1), 0.7);                      // calves
  }
  // dumbbell in the right palm
  const db = new THREE.Group();
  const bar = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.55, 8), new THREE.MeshStandardMaterial({ color: "#9a9aa0", metalness: 0.7, roughness: 0.3 }));
  db.add(bar); [-1, 1].forEach(s => { const p = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.14, 10), std("#26262c", 0.5)); p.position.y = s * 0.27; p.castShadow = true; db.add(p); });
  db.rotation.set(0, 0, Math.PI / 2); db.position.set(0, 0.12, 0.02); attach(palmR, db);
  // muscle "inflate": push each vertex away from its bones' axes (bind pose), weighted by skin weights.
  // Bone transforms stay untouched, so poses never shear.
  const prep = skinned.map(m => {
    const pos = m.geometry.attributes.position as THREE.BufferAttribute, orig = Float32Array.from(pos.array as Float32Array);
    const si = m.geometry.attributes.skinIndex as THREE.BufferAttribute, sw = m.geometry.attributes.skinWeight as THREE.BufferAttribute;
    const axes = m.skeleton.boneInverses.map(inv => { const w = inv.clone().invert(); const o = new THREE.Vector3().setFromMatrixPosition(w); const y = new THREE.Vector3(0, 1, 0).transformDirection(w); return { o, y }; });
    return { m, pos, orig, si, sw, axes, names: m.skeleton.bones.map(bn => bn.name) };
  });
  const bulk = (fac: Record<string, number>) => {
    const v = new THREE.Vector3(), d = new THREE.Vector3(), acc = new THREE.Vector3();
    for (const P of prep) {
      const bm = P.m.bindMatrix, bmi = P.m.bindMatrixInverse;
      for (let i = 0; i < P.pos.count; i++) {
        v.set(P.orig[i * 3], P.orig[i * 3 + 1], P.orig[i * 3 + 2]).applyMatrix4(bm); acc.set(0, 0, 0);
        for (let k = 0; k < 4; k++) {
          const w = P.sw.getComponent(i, k); if (w <= 0) continue;
          const bi = P.si.getComponent(i, k), f = fac[P.names[bi]] ?? 1; if (f === 1) continue;
          const A = P.axes[bi]; d.copy(v).sub(A.o); d.addScaledVector(A.y, -d.dot(A.y)); acc.addScaledVector(d, w * (f - 1));
        }
        v.add(acc).applyMatrix4(bmi); P.pos.setXYZ(i, v.x, v.y, v.z);
      }
      P.pos.needsUpdate = true; P.m.geometry.computeBoundingSphere();
    }
  };
  Object.values(bones).forEach(bn => { bn.userData.restQ = bn.quaternion.clone(); bn.userData.restP = bn.position.clone(); });
  return { bulk, root, mixer, idle, bones, mats, extra: { group: Object.assign(new THREE.Group(), { userData: { list: group } }), beard, acne, sweat, pecs, abs, db, m0: muscles[0], m1: muscles[1], m2: muscles[2], m3: muscles[3] } };
};

// rotate `bone` so its +Y axis points along `dir` (world space)
const aim = (bone: THREE.Bone, dir: THREE.Vector3, amt: number) => {
  if (amt <= 0) return;
  bone.updateWorldMatrix(true, false);
  const wq = new THREE.Quaternion(); bone.getWorldQuaternion(wq);
  const cur = V(0, 1, 0).applyQuaternion(wq);
  const delta = new THREE.Quaternion().setFromUnitVectors(cur, dir.clone().normalize());
  const full = new THREE.Quaternion().slerpQuaternions(new THREE.Quaternion(), delta, amt);
  const target = full.multiply(wq);
  const pq = new THREE.Quaternion(); bone.parent!.getWorldQuaternion(pq);
  bone.quaternion.copy(pq.invert().multiply(target));
  bone.updateWorldMatrix(false, true);
};
const thick = (b: THREE.Bone, k: number) => b.scale.set(k, 1, k);

export const Hero: React.FC<{ g: GLTF; L: Look; ry?: number }> = ({ g, L, ry = 0 }) => {
  const rig = useMemo(() => build(g), [g]);
  const { bones: b, mats, extra } = rig, f = L.f, u = sat((L.m - 1) / 0.9);
  // 1) base motion
  Object.values(b).forEach(bn => { bn.quaternion.copy(bn.userData.restQ); bn.position.copy(bn.userData.restP); });
  rig.mixer.setTime((f / 30) % 10); rig.root.updateMatrixWorld(true);
  // 3) poses on top of the idle clip
  const flex = L.flex, curl = L.curl * (L.holding ? 1 : 0);
  if (L.slump > 0) { b.Abdomen.rotateX(0.25 * L.slump); b.Torso.rotateX(0.12 * L.slump); rig.root.updateMatrixWorld(true); }
  for (const [s, side] of [["L", 1], ["R", -1]] as const) {
    if (flex > 0) {
      aim(b["UpperArm" + s], V(side * 1, 0.05, 0.1), flex);
      aim(b["LowerArm" + s], V(-side * 0.45, 1, 0.35), flex);
      b["Fingers" + s].rotateX(1.4 * flex);
    }
  }
  if (curl > 0 || L.holding) {
    aim(b.UpperArmR, V(-0.12, -1, 0.18), 1);
    const c = 0.15 + 0.85 * curl;
    aim(b.LowerArmR, V(-0.05, lerp(-1, 0.75, c), lerp(0.15, 0.7, c)), 1);
  }
  if (L.lookDown > 0) { b.Head.rotateX(0.5 * L.lookDown); b.Neck.rotateX(0.2 * L.lookDown); }
  if (L.slump > 0) { b.Head.rotateX(0.35 * L.slump); for (const s of ["L", "R"]) aim(b["UpperArm" + s], V(0, -1, 0.35), L.slump * 0.6); }
  // 2) muscle: inflate the skin around the bones (cached per step of u)
  const key = Math.round(u * 60);
  if (rig.root.userData.bulkKey !== key) {
    const q = key / 60;
    if (false) rig.bulk({ Torso: 1 + 0.32 * q, Abdomen: 1 + 0.12 * q, Neck: 1 + 0.5 * q, ShoulderL: 1 + 0.55 * q, ShoulderR: 1 + 0.55 * q,
      UpperArmL: 1 + 0.75 * q, UpperArmR: 1 + 0.75 * q, LowerArmL: 1 + 0.45 * q, LowerArmR: 1 + 0.45 * q,
      UpperLegL: 1 + 0.28 * q, UpperLegR: 1 + 0.28 * q, LowerLegL: 1 + 0.2 * q, LowerLegR: 1 + 0.2 * q, Hips: 1 + 0.08 * q });
    rig.root.userData.bulkKey = key;
  }
  // 4) materials
  const shirtOff = L.rip >= 0;
  mats.Skin.color.copy(SKIN).lerp(FLUSH, L.flush * 0.75);
  mats.Shirt.color.copy(shirtOff ? mats.Skin.color : new THREE.Color("#2f9fd0"));
  mats.Hair.color.copy(HAIR).lerp(mats.Skin.color, L.hair * 0.92);
  // 5) attachments
  extra.beard.visible = L.beard > 0.02; extra.beard.scale.setScalar(lerp(0.96, 1.06, L.beard));
  ((extra.beard.children[0] as THREE.Mesh).material as THREE.MeshStandardMaterial).color.copy(mats.Skin.color).lerp(new THREE.Color("#3e2a20"), 0.35 + 0.65 * L.beard);
  extra.acne.children.forEach((m, i) => (m.visible = L.acne > i / extra.acne.children.length));
  extra.sweat.visible = L.sweat > 0; extra.sweat.children.forEach((m, i) => { const t = (f * 0.02 + i / 3) % 1; m.position.set((i - 1) * 0.14, 0.55 - t * 0.35, 0.36); ((m as THREE.Mesh).material as THREE.MeshStandardMaterial).opacity = L.sweat * (1 - t); });
  extra.pecs.visible = shirtOff; extra.abs.visible = shirtOff && u > 0.5;
  extra.pecs.children.forEach(m => { m.scale.set(lerp(1.1, 1.2, L.chest) * (1 + 0.3 * u), lerp(0.75, 1.0, L.chest), lerp(0.42, 0.75, L.chest) * (1 + 0.2 * u)); m.position.y = lerp(0.42, 0.36, L.chest); });
  extra.db.visible = L.holding;
  for (const it of extra.group.userData.list as { m: THREE.Mesh; k: number; cover?: "Shirt" | "Pants" }[]) {
    it.m.visible = u > 0.04; const sc = (0.45 + 0.75 * u) * it.k + (1 - it.k) * 0.6; it.m.scale.copy(it.m.userData.base).multiplyScalar(sc);
    it.m.material = it.cover === "Pants" ? mats.Pants : it.cover === "Shirt" && !shirtOff ? mats.Shirt : mats.Skin;
  }
  // biceps bulge (more when flexing), delts round out; delts follow the shirt until it rips
  for (const k of ["m0", "m2"]) { const m = extra[k]; m.visible = u > 0.05; const bs = (0.55 + 0.6 * u) * (1 + 0.25 * flex); m.scale.set(bs * 0.85, bs * 1.25, bs); }
  for (const k of ["m1", "m3"]) { const m = extra[k] as THREE.Mesh; m.visible = u > 0.05; m.scale.setScalar(0.7 + 0.55 * u); m.material = shirtOff ? mats.Skin : mats.Shirt; }
  return <primitive object={rig.root} scale={SCALE} rotation={[0, ry, 0]} />;
};
