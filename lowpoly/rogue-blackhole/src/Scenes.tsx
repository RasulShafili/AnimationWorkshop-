import React from "react";
import * as THREE from "three";
export const sat = (v: number) => Math.min(1, Math.max(0, v));
const glowTex = (() => { let t: THREE.CanvasTexture | null = null; return () => { if (t) return t; const c = document.createElement("canvas"); c.width = c.height = 128; const g = c.getContext("2d")!, gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(0.3, "rgba(255,255,255,.45)"); gr.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); t = new THREE.CanvasTexture(c); return t; }; })();
export const Glow: React.FC<{ size: number; color: THREE.Color | string; opacity: number; pos?: [number, number, number] }> = ({ size, color, opacity, pos = [0, 0, 0] }) =>
  <sprite position={pos} scale={[size, size, 1]}><spriteMaterial map={glowTex()} color={color} transparent opacity={opacity} blending={THREE.AdditiveBlending} depthWrite={false} toneMapped={false} /></sprite>;

