// Earth as ~45 fracture chunks around a lava core: oceans can boil (boil 0..1), cracks glow (crack 0..1),
// and the chunks fly apart (shatter = frames since the break).
import React, { useMemo } from "react";
import * as THREE from "three";
import { Glow, sat } from "./Scenes";

const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };
const R = 3, K = 46;

const buildChunks = () => {
  const seeds = Array.from({ length: K }, (_, i) => { const u = rnd(i, 1) * 2 - 1, a = rnd(i, 2) * 6.283, s = Math.sqrt(1 - u * u); return new THREE.Vector3(Math.cos(a) * s, u, Math.sin(a) * s); });
  const g = new THREE.IcosahedronGeometry(R, 5).toNonIndexed(), p = g.attributes.position;
  const buckets: number[][] = Array.from({ length: K }, () => []);
  for (let i = 0; i < p.count; i += 3) {
    const c = new THREE.Vector3(p.getX(i) + p.getX(i + 1) + p.getX(i + 2), p.getY(i) + p.getY(i + 1) + p.getY(i + 2), p.getZ(i) + p.getZ(i + 1) + p.getZ(i + 2)).normalize();
    let best = 0, bd = -2; seeds.forEach((s, k) => { const d = s.dot(c); if (d > bd) { bd = d; best = k; } });
    buckets[best].push(i);
  }
  return buckets.map((tris, k) => {
    const pos: number[] = [], land: number[] = [];
    for (const i of tris) {
      const v = [0, 1, 2].map(j => new THREE.Vector3(p.getX(i + j), p.getY(i + j), p.getZ(i + j)));
      const c = v[0].clone().add(v[1]).add(v[2]).divideScalar(3);
      const isLand = Math.sin(c.x * 1.3 + Math.sin(c.z * 0.9) * 2) * Math.cos(c.y * 1.5 + c.x * 0.4) > 0.15 ? 1 : Math.abs(c.y) > 2.6 ? 2 : 0;
      for (const w of v) { pos.push(w.x, w.y, w.z); land.push(isLand); }
      // a wedge down to the core so a flying chunk has a molten inside
      const inner = v.map(w => w.clone().multiplyScalar(0.55));
      for (const [a, b] of [[0, 1], [1, 2], [2, 0]]) { for (const w of [v[b], v[a], inner[a], v[b], inner[a], inner[b]]) { pos.push(w.x, w.y, w.z); land.push(3); } }
    }
    const geo = new THREE.BufferGeometry(); geo.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3)); geo.setAttribute("kind", new THREE.Float32BufferAttribute(land, 1));
    geo.computeVertexNormals();
    const col = new Float32Array(land.length * 3); geo.setAttribute("color", new THREE.BufferAttribute(col, 3));
    return { geo, dir: seeds[k], spin: new THREE.Vector3(rnd(k, 3) - 0.5, rnd(k, 4) - 0.5, rnd(k, 5) - 0.5).normalize(), sp: 0.6 + rnd(k, 6) * 0.8 };
  });
};

const C = { ocean: new THREE.Color("#2a6ad8"), land: new THREE.Color("#4aa04a"), ice: new THREE.Color("#f0f4ff"), lava: new THREE.Color("#ff5a10"), steam: new THREE.Color("#8a8c94"), burnt: new THREE.Color("#3a2418") };

export const Planet: React.FC<{ f: number; boil?: number; crack?: number; shatter?: number; spin?: number }> = ({ f, boil = 0, crack = 0, shatter = -1, spin = 0 }) => {
  const chunks = useMemo(buildChunks, []);
  const mat = useMemo(() => new THREE.MeshStandardMaterial({ vertexColors: true, flatShading: true, roughness: 0.85, side: THREE.DoubleSide }), []);
  const lavaMat = useMemo(() => new THREE.MeshBasicMaterial({ color: new THREE.Color(3, 1.1, 0.25), toneMapped: false }), []);
  // recolour (cheap: only depends on boil)
  const oc = C.ocean.clone().lerp(C.steam, boil), ld = C.land.clone().lerp(C.burnt, boil);
  useMemo(() => chunks.forEach(ch => { const k = ch.geo.attributes.kind, c = ch.geo.attributes.color as THREE.BufferAttribute; for (let i = 0; i < k.count; i++) { const kind = k.getX(i), cc = kind === 0 ? oc : kind === 1 ? ld : kind === 2 ? C.ice.clone().lerp(C.steam, boil) : C.lava; c.setXYZ(i, cc.r, cc.g, cc.b); } c.needsUpdate = true; }), [chunks, Math.round(boil * 40)]);
  const s = Math.max(0, shatter);
  const gap = crack * 0.06;
  return (
    <group rotation={[0.25, spin, 0]}>
      {chunks.map((ch, i) => {
        const d = gap + (shatter >= 0 ? s * 0.02 * ch.sp + s * s * 0.00012 : 0);
        const q = new THREE.Quaternion().setFromAxisAngle(ch.spin, shatter >= 0 ? s * 0.012 * ch.sp : 0);
        return <mesh key={i} geometry={ch.geo} material={mat} position={ch.dir.clone().multiplyScalar(d * R)} quaternion={q} />;
      })}
      {/* molten core: visible through cracks, flares when it breaks */}
      <mesh scale={Math.max(0.001, R * 0.96 * (shatter >= 0 ? sat(1 - s / 45) : 1))} material={lavaMat}><icosahedronGeometry args={[1, 3]} /></mesh>
      <Glow size={R * (2.4 + crack * 1.5 + (shatter >= 0 ? Math.min(3, s * 0.12) : 0))} color="#ff7a2a" opacity={(0.25 + crack * 0.4) * (shatter >= 0 ? sat(1 - s / 50) : 1) + (shatter >= 0 ? sat(1 - s / 40) * 0.5 : 0)} />
      {boil > 0 && shatter < 0 && <mesh scale={1.06}><sphereGeometry args={[R, 32, 20]} /><meshStandardMaterial color="#f4f0ec" transparent opacity={boil * 0.22} depthWrite={false} /></mesh>}
      <mesh scale={1.04}><sphereGeometry args={[R, 32, 20]} /><meshBasicMaterial color={boil > 0.5 ? "#ff7a3a" : "#6ab8ff"} transparent opacity={shatter >= 0 ? 0 : 0.12 + boil * 0.12} side={THREE.BackSide} /></mesh>
    </group>
  );
};
