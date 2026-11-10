import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import * as THREE from "three";
import { GLTF } from "three/examples/jsm/loaders/GLTFLoader.js";
import { useGLBs } from "./glb";
import { Post } from "./Post";

const Model: React.FC<{ g: GLTF; x: number; clip: string; t: number }> = ({ g, x, clip, t }) => {
  const mixer = React.useMemo(() => new THREE.AnimationMixer(g.scene), [g]);
  const a = g.animations.find(c => c.name.includes(clip)) || g.animations[0];
  mixer.stopAllAction(); mixer.clipAction(a).play(); mixer.setTime(t);
  g.scene.updateMatrixWorld(true);
  const box = new THREE.Box3().setFromObject(g.scene, true), h = Math.max(0.01, box.max.y - box.min.y);
  g.scene.traverse((o: any) => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; o.frustumCulled = false; } });
  return <primitive object={g.scene} position={[x, -box.min.y * 1.8 / h, 0]} scale={1.8 / h} />;
};
export const Preview: React.FC = () => {
  const f = useCurrentFrame();
  const d = useGLBs(["man.glb", "animated_human.glb"]);
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {d && (
        <ThreeCanvas width={1080} height={1920} shadows camera={{ fov: 34, position: [0, 1.1, 6.5] }} gl={{ antialias: true }}>
          <color attach="background" args={["#d8a080"]} />
          <hemisphereLight args={["#ffe2c8", "#4a3a4a", 1.0]} />
          <directionalLight position={[2.5, 4, 5]} intensity={2.5} castShadow />
          <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow><planeGeometry args={[20, 20]} /><meshStandardMaterial color="#3a3640" /></mesh>
          <Model g={d["man.glb"]} x={-0.9} clip="Idle" t={f / 30} />
          <Model g={d["animated_human.glb"]} x={0.9} clip="Idle" t={f / 30} />
          <Post />
        </ThreeCanvas>
      )}
    </AbsoluteFill>
  );
};
