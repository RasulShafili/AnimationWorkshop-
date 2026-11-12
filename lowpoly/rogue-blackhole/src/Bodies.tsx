// Planets, asteroids and Kuiper objects as glowing points; planet trails; the Sun.
import React, { useMemo } from "react";
import * as THREE from "three";
import { Sim, idx, coreAt, bodyAt } from "./data";
import { Glow } from "./Scenes";

const vert = `
attribute vec3 aColor; attribute float aSize; attribute float aKind;
uniform float uScale, uStar, uMax, uPlanet;
varying vec3 vColor; varying float vI;
void main() {
  vec4 mv = modelViewMatrix * vec4(position, 1.0);
  float d = -mv.z;
  bool planet = aKind < 7.5;
  float ps = planet ? aSize * uPlanet : aSize * uStar * uScale / max(d, 0.001);
  vI = planet ? 1.0 : clamp(ps / 1.4, aKind > 8.5 ? 0.85 : 0.45, 1.0) * (aKind > 8.5 ? 1.5 : 1.0);
  gl_PointSize = planet ? ps : clamp(ps, 1.0, uMax);
  vColor = aColor * (planet ? 2.2 : 1.0);
  gl_Position = projectionMatrix * mv;
}`;
const frag = `varying vec3 vColor; varying float vI; void main(){ vec2 c = gl_PointCoord - .5; float r2 = dot(c, c); float a = exp(-r2 * 18.0) + 0.6 * exp(-r2 * 120.0); gl_FragColor = vec4(vColor * vI * a, 1.0); }`;

export const Bodies: React.FC<{ sim: Sim; t: number; fov: number; star?: number; planetPx?: number; trail?: number; sunGlow?: number; orbits?: number }> = ({ sim, t, fov, star = 0.004, planetPx = 22, trail = 40, sunGlow = 2, orbits = 0 }) => {
  const { geo, mat, trails } = useMemo(() => {
    const g = new THREE.BufferGeometry(); const N = sim.N;
    g.setAttribute("position", new THREE.BufferAttribute(new Float32Array(N * 3), 3));
    const col = new Float32Array(N * 3), size = new Float32Array(N), kind = new Float32Array(N);
    for (let i = 0; i < N; i++) { col.set([sim.bodies[i * 5], sim.bodies[i * 5 + 1], sim.bodies[i * 5 + 2]], i * 3); size[i] = sim.bodies[i * 5 + 3]; kind[i] = sim.bodies[i * 5 + 4]; }
    g.setAttribute("aColor", new THREE.BufferAttribute(col, 3)); g.setAttribute("aSize", new THREE.BufferAttribute(size, 1)); g.setAttribute("aKind", new THREE.BufferAttribute(kind, 1));
    const m = new THREE.ShaderMaterial({ vertexShader: vert, fragmentShader: frag, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, uniforms: { uScale: { value: 1 }, uStar: { value: 1 }, uMax: { value: 4 }, uPlanet: { value: 22 } } });
    const tr = Array.from({ length: 8 }, (_, k) => { const lg = new THREE.BufferGeometry(); lg.setAttribute("position", new THREE.BufferAttribute(new Float32Array(120 * 3), 3)); const c = new THREE.Color(sim.bodies[k * 5], sim.bodies[k * 5 + 1], sim.bodies[k * 5 + 2]); return new THREE.Line(lg, new THREE.LineBasicMaterial({ color: c, transparent: true, opacity: 0.55, blending: THREE.AdditiveBlending, depthWrite: false })); });
    return { geo: g, mat: m, trails: tr };
  }, [sim]);
  const [i, u] = idx(sim, t), N = sim.N, s = sim.snaps, p = geo.attributes.position.array as Float32Array, q = sim.Q;
  const o0 = i * N * 3, o1 = (i + 1) * N * 3;
  for (let k = 24; k < N * 3; k++) p[k] = (s[o0 + k] + (s[o1 + k] - s[o0 + k]) * u) / q;
  for (let k = 0; k < 8; k++) { const b = bodyAt(sim, t, k); p[k * 3] = b[0]; p[k * 3 + 1] = b[1]; p[k * 3 + 2] = b[2]; }
  geo.attributes.position.needsUpdate = true;
  mat.uniforms.uScale.value = 1920 / (2 * Math.tan((fov * Math.PI) / 360)); mat.uniforms.uStar.value = star; mat.uniforms.uPlanet.value = planetPx;
  // trails: the last `trail` years of each planet, 120 samples
  trails.forEach((ln, k) => { const a = ln.geometry.attributes.position.array as Float32Array; for (let j = 0; j < 120; j++) { const tt = Math.max(0, t - trail * (1 - j / 119)); const b = bodyAt(sim, tt, k); a[j * 3] = b[0]; a[j * 3 + 1] = b[1]; a[j * 3 + 2] = b[2]; } ln.geometry.attributes.position.needsUpdate = true; ln.geometry.computeBoundingSphere(); });
  const sun = coreAt(sim, t, 0);
  return <group>
    <points geometry={geo} material={mat} frustumCulled={false} />
    {trails.map((l, k) => <primitive key={k} object={l} />)}
    {sunGlow > 0 && <mesh position={sun as any} scale={sunGlow * 0.06}><sphereGeometry args={[1, 24, 16]} /><meshBasicMaterial color={new THREE.Color(3.2, 2.6, 1.6)} toneMapped={false} /></mesh>}
    {sunGlow > 0 && <Glow size={sunGlow} color="#ffd890" opacity={0.85} pos={sun as any} />}
    {orbits > 0 && [.387, .723, 1, 1.524, 5.2, 9.58, 19.2, 30.1].map((r, k) => <mesh key={k} position={sun as any}><ringGeometry args={[r - r * 0.004 - 0.02, r + r * 0.004 + 0.02, 160]} /><meshBasicMaterial color={new THREE.Color(sim.bodies[k * 5], sim.bodies[k * 5 + 1], sim.bodies[k * 5 + 2])} transparent opacity={0.35 * orbits} side={THREE.DoubleSide} depthWrite={false} blending={THREE.AdditiveBlending} /></mesh>)}
  </group>;
};

const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };
export const Backdrop: React.FC<{ center: number[]; dim?: number; n?: number }> = ({ center, dim = 1, n = 9000 }) => {
  const geo = useMemo(() => { const p = new Float32Array(n * 3), c = new Float32Array(n * 3); for (let i = 0; i < n; i++) { const uu = rnd(i, 1) * 2 - 1, th = rnd(i, 2) * 6.283, s = Math.sqrt(1 - uu * uu), b = 0.2 + Math.pow(rnd(i, 3), 7) * 1.6; p.set([Math.cos(th) * s * 900, uu * 900, Math.sin(th) * s * 900], i * 3); const w = rnd(i, 4); c.set([b * (0.85 + w * 0.2), b * 0.9, b * (1.1 - w * 0.25)], i * 3); } const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.BufferAttribute(p, 3)); g.setAttribute("color", new THREE.BufferAttribute(c, 3)); return g; }, [n]);
  return <points geometry={geo} position={center as any}><pointsMaterial vertexColors size={1.7} sizeAttenuation={false} transparent opacity={dim} depthWrite={false} /></points>;
};

// the crowded star field toward the galactic bulge (where Hubble/OGLE look) for the microlensing shot
export const DenseField: React.FC = () => {
  const geo = useMemo(() => { const n = 60000, p = new Float32Array(n * 3), c = new Float32Array(n * 3); // bulge field
    for (let i = 0; i < n; i++) { const a = (rnd(i, 1) - 0.5) * 0.9, e = (rnd(i, 2) - 0.5) * 1.5 + 0.12, w = rnd(i, 4), b = 0.15 + Math.pow(rnd(i, 3), 5) * 1.8;
      p.set([Math.cos(e) * Math.cos(a) * 600, Math.cos(e) * Math.sin(a) * 600, Math.sin(e) * 600], i * 3); c.set([b * (1.0 - w * 0.25), b * (0.85 + w * 0.05), b * (0.6 + w * 0.5)], i * 3); }
    const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.BufferAttribute(p, 3)); g.setAttribute("color", new THREE.BufferAttribute(c, 3)); return g; }, []);
  return <group>
    <points geometry={geo}><pointsMaterial vertexColors size={2.0} sizeAttenuation={false} transparent depthWrite={false} blending={THREE.AdditiveBlending} /></points>
    <Glow size={520} color="#c89060" opacity={0.18} pos={[600, 40, 90]} />
    <Glow size={300} color="#8a6aa0" opacity={0.12} pos={[600, -160, -40]} />
  </group>;
};

// the Milky Way as seen from the Solar System: a band of stars + soft glow on a big sphere around the camera
export const SkyBand: React.FC<{ center: number[]; dim?: number }> = ({ center, dim = 1 }) => {
  const geo = useMemo(() => { const n = 45000, p = new Float32Array(n * 3), c = new Float32Array(n * 3);
    // band plane tilted ~60° to the ecliptic (z-up world)
    const tilt = 1.05, ct = Math.cos(tilt), st = Math.sin(tilt);
    for (let i = 0; i < n; i++) { const lon = rnd(i, 11) * 6.283, lat = (rnd(i, 12) + rnd(i, 13) + rnd(i, 14) - 1.5) * 0.28 * (1 + 0.6 * Math.exp(-Math.pow((lon - 3.4) / 0.6, 2)));
      const x = Math.cos(lat) * Math.cos(lon), y = Math.cos(lat) * Math.sin(lon), z = Math.sin(lat);
      const w = rnd(i, 15), b = (0.12 + Math.pow(rnd(i, 16), 6) * 1.4) * (1 + 1.2 * Math.exp(-Math.pow((lon - 3.4) / 0.5, 2)));
      p.set([x * 850, (y * ct - z * st) * 850, (y * st + z * ct) * 850], i * 3); c.set([b * (1.0 - w * 0.2), b * 0.9, b * (0.75 + w * 0.4)], i * 3); }
    const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.BufferAttribute(p, 3)); g.setAttribute("color", new THREE.BufferAttribute(c, 3)); return g; }, []);
  return <group position={center as any}><points geometry={geo}><pointsMaterial vertexColors size={1.9} sizeAttenuation={false} transparent opacity={dim} depthWrite={false} blending={THREE.AdditiveBlending} /></points></group>;
};
