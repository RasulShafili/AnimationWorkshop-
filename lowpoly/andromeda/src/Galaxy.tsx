// All simulated stars as soft additive points. Positions interpolated between snapshots each frame.
// shiftM31 pushes Andromeda's stars further away along the MW->M31 line (for "today" views: 2.5 Mly away).
import React, { useMemo } from "react";
import * as THREE from "three";
import { Sim, snapIndex, coreAt } from "./data";

const vert = `
attribute vec3 aColor; attribute float aSize; attribute float aKind;
uniform float uScale, uStar, uMax, uNear, uBurst, uM31Dim;
varying vec3 vColor; varying float vI;
void main() {
  vec4 mv = modelViewMatrix * vec4(position, 1.0);
  float d = -mv.z;
  float boost = aKind > 3.5 ? 1.0 + uBurst * 3.5 : 1.0;
  float ps = aSize * boost * uStar * uScale / max(d, 0.0001);
  vI = clamp(ps / 1.6, 0.0, 1.0) * (aKind > 1.5 && aKind < 3.5 ? uM31Dim : 1.0) * (aKind > 3.5 ? 0.6 + uBurst * 2.2 : 1.0);
  ps = clamp(ps, 1.2, uMax);
  if (d < uNear) { ps = 0.0; }
  gl_PointSize = ps;
  vColor = aColor;
  gl_Position = projectionMatrix * mv;
}`;
const frag = `
uniform float uExp; varying vec3 vColor; varying float vI;
void main() {
  vec2 c = gl_PointCoord - 0.5; float r2 = dot(c, c);
  float a = exp(-r2 * 22.0);
  gl_FragColor = vec4(vColor * vI * a * uExp, 1.0);
}`;

export const Galaxy: React.FC<{ sim: Sim; t: number; shiftM31?: number; exp?: number; star?: number; maxPx?: number; near?: number; burst?: number; m31Dim?: number; fov: number }> =
  ({ sim, t, shiftM31 = 0, exp = 1, star = 0.006, maxPx = 7, near = 0.0, burst = 0, m31Dim = 1, fov }) => {
  const { geo, mat } = useMemo(() => {
    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.BufferAttribute(new Float32Array(sim.N * 3), 3));
    const col = new Float32Array(sim.N * 3), size = new Float32Array(sim.N), kind = new Float32Array(sim.N);
    for (let i = 0; i < sim.N; i++) { col[i * 3] = sim.stars[i * 5]; col[i * 3 + 1] = sim.stars[i * 5 + 1]; col[i * 3 + 2] = sim.stars[i * 5 + 2]; size[i] = sim.stars[i * 5 + 3]; kind[i] = sim.stars[i * 5 + 4]; }
    g.setAttribute("aColor", new THREE.BufferAttribute(col, 3)); g.setAttribute("aSize", new THREE.BufferAttribute(size, 1)); g.setAttribute("aKind", new THREE.BufferAttribute(kind, 1));
    const m = new THREE.ShaderMaterial({ vertexShader: vert, fragmentShader: frag, transparent: true, depthWrite: false, depthTest: false, blending: THREE.AdditiveBlending,
      uniforms: { uScale: { value: 1 }, uStar: { value: 1 }, uMax: { value: 7 }, uNear: { value: 0 }, uBurst: { value: 0 }, uM31Dim: { value: 1 }, uExp: { value: 1 } } });
    return { geo: g, mat: m };
  }, [sim]);
  // positions for this frame
  const [i, u] = snapIndex(sim, t), q = sim.QSCALE, N = sim.N, s = sim.snaps, p = geo.attributes.position.array as Float32Array;
  const c0 = coreAt(sim, t, 0), c1 = coreAt(sim, t, 1);
  let dx = c1[0] - c0[0], dy = c1[1] - c0[1], dz = c1[2] - c0[2]; const dl = Math.hypot(dx, dy, dz) || 1; dx /= dl; dy /= dl; dz /= dl;
  const o0 = i * N * 3, o1 = (i + 1) * N * 3, m31From = 30000;
  for (let k = 0; k < N * 3; k += 3) {
    const sh = (k / 3) >= m31From ? shiftM31 : 0;
    p[k] = (s[o0 + k] + (s[o1 + k] - s[o0 + k]) * u) / q + dx * sh;
    p[k + 1] = (s[o0 + k + 1] + (s[o1 + k + 1] - s[o0 + k + 1]) * u) / q + dy * sh;
    p[k + 2] = (s[o0 + k + 2] + (s[o1 + k + 2] - s[o0 + k + 2]) * u) / q + dz * sh;
  }
  geo.attributes.position.needsUpdate = true;
  const U = mat.uniforms; U.uScale.value = 1920 / (2 * Math.tan((fov * Math.PI) / 360)); U.uStar.value = star; U.uMax.value = maxPx; U.uNear.value = near; U.uBurst.value = burst; U.uM31Dim.value = m31Dim; U.uExp.value = exp;
  return <points geometry={geo} material={mat} frustumCulled={false} />;
};

// distant background stars + faint nebula haze, fixed on a big sphere around the camera
const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };
export const Backdrop: React.FC<{ center: THREE.Vector3; dim?: number }> = ({ center, dim = 1 }) => {
  const geo = useMemo(() => { const n = 5000, p = new Float32Array(n * 3), c = new Float32Array(n * 3); for (let i = 0; i < n; i++) { const u = rnd(i, 1) * 2 - 1, th = rnd(i, 2) * 6.283, s = Math.sqrt(1 - u * u), b = 0.25 + Math.pow(rnd(i, 3), 6) * 1.2; p.set([Math.cos(th) * s * 300, u * 300, Math.sin(th) * s * 300], i * 3); const w = rnd(i, 4); c.set([b * (0.85 + w * 0.15), b * 0.9, b * (1.05 - w * 0.2)], i * 3); } const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.BufferAttribute(p, 3)); g.setAttribute("color", new THREE.BufferAttribute(c, 3)); return g; }, []);
  return <points geometry={geo} position={center}><pointsMaterial vertexColors size={1.6} sizeAttenuation={false} transparent opacity={dim} depthWrite={false} /></points>;
};
