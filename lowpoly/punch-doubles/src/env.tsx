// The world beyond the hero block, so nothing on screen is empty:
// an outer town on a street grid, fields and hills, forested slopes, snowy mountains, clouds and a sun disc.
// Everything far away is instanced to stay cheap.
import React, { useLayoutEffect, useMemo, useRef } from "react";
import * as THREE from "three";
import { rnd, sat, mixC } from "./kit";

const GRID = 14, OX = -2, OZ = 1.5, CITY = 60, CORE = 12.6;
const sstep = (a: number, b: number, x: number) => { const t = sat((x - a) / (b - a)); return t * t * (3 - 2 * t); };
const vnoise = (x: number, z: number) => {
  const xi = Math.floor(x), zi = Math.floor(z), xf = x - xi, zf = z - zi, u = xf * xf * (3 - 2 * xf), v = zf * zf * (3 - 2 * zf);
  const h = (a: number, b: number) => rnd(a * 7919 + b * 104729 + 1000003, 77);
  return (h(xi, zi) * (1 - u) + h(xi + 1, zi) * u) * (1 - v) + (h(xi, zi + 1) * (1 - u) + h(xi + 1, zi + 1) * u) * v;
};
const fbm = (x: number, z: number) => vnoise(x, z) * 0.55 + vnoise(x * 2.1, z * 2.1) * 0.3 + vnoise(x * 4.3, z * 4.3) * 0.15;
// terrain height: flat under the town, rolling hills beyond, higher ridges far out
export const groundY = (x: number, z: number) => {
  const r = Math.max(Math.abs(x), Math.abs(z));
  return sstep(CITY + 2, CITY + 30, r) * (fbm(x * 0.03, z * 0.03) * 9 - 1.5) + sstep(110, 220, r) * fbm(x * 0.012 + 5, z * 0.012) * 26;
};

const Terrain: React.FC = () => {
  const geo = useMemo(() => {
    const g = new THREE.PlaneGeometry(640, 640, 150, 150).toNonIndexed(); g.rotateX(-Math.PI / 2);
    const p = g.attributes.position, col = new Float32Array(p.count * 3);
    for (let i = 0; i < p.count; i++) p.setY(i, groundY(p.getX(i), p.getZ(i)) - 0.02);
    const grass = [mixC("#7a9a3a", "#86a640", 0), mixC("#9aa848", "#9aa848", 0), mixC("#c8b860", "#c8b860", 0), mixC("#6a8a34", "#6a8a34", 0), mixC("#b0884a", "#b0884a", 0)];
    for (let i = 0; i < p.count; i += 3) {
      const cx = (p.getX(i) + p.getX(i + 1) + p.getX(i + 2)) / 3, cz = (p.getZ(i) + p.getZ(i + 1) + p.getZ(i + 2)) / 3, cy = (p.getY(i) + p.getY(i + 1) + p.getY(i + 2)) / 3;
      const r = Math.max(Math.abs(cx), Math.abs(cz));
      let c: THREE.Color;
      if (r < CITY + 1) c = grass[0].clone().lerp(grass[1], fbm(cx * 0.2, cz * 0.2) * 0.5);
      else {
        const field = Math.floor((cx + 1000) / 18) * 31 + Math.floor((cz + 1000) / 14) * 17; // patchwork farmland
        c = grass[Math.floor(rnd(field, 3) * 5)].clone().lerp(grass[0], sstep(10, 30, cy) * 0.8);
        if (cy > 22) c = c.lerp(new THREE.Color("#8a7a8a"), sstep(22, 34, cy));
      }
      c.multiplyScalar(0.92 + rnd(i, 5) * 0.12);
      for (let k = 0; k < 3; k++) col.set([c.r, c.g, c.b], (i + k) * 3);
    }
    g.setAttribute("color", new THREE.BufferAttribute(col, 3)); g.computeVertexNormals(); return g;
  }, []);
  return <mesh geometry={geo} receiveShadow><meshStandardMaterial vertexColors flatShading roughness={0.95} /></mesh>;
};

type Inst = { m: THREE.Matrix4; c: THREE.Color };
const Instanced: React.FC<{ geo: THREE.BufferGeometry; items: Inst[]; mat: THREE.Material; shadow?: boolean }> = ({ geo, items, mat, shadow = true }) => {
  const ref = useRef<THREE.InstancedMesh>(null);
  useLayoutEffect(() => {
    const im = ref.current!; items.forEach((it, i) => { im.setMatrixAt(i, it.m); im.setColorAt(i, it.c); });
    im.instanceMatrix.needsUpdate = true; if (im.instanceColor) im.instanceColor.needsUpdate = true;
  }, [items]);
  return <instancedMesh ref={ref} args={[geo, mat, items.length]} castShadow={shadow} receiveShadow frustumCulled={false} />;
};
const M4 = (x: number, y: number, z: number, ry: number, sx: number, sy: number, sz: number) =>
  new THREE.Matrix4().compose(new THREE.Vector3(x, y, z), new THREE.Quaternion().setFromEuler(new THREE.Euler(0, ry, 0)), new THREE.Vector3(sx, sy, sz));

const unitBox = new THREE.BoxGeometry(1, 1, 1);
const unitRoof = (() => { const s = new THREE.Shape(); s.moveTo(-0.5, 0); s.lineTo(0.5, 0); s.lineTo(0, 1); s.closePath(); const g = new THREE.ExtrudeGeometry(s, { depth: 1, bevelEnabled: false }); g.translate(0, 0, -0.5); return g; })();
const crownGeo = new THREE.IcosahedronGeometry(1, 0), trunkGeo = new THREE.CylinderGeometry(0.07, 0.11, 1, 5); trunkGeo.translate(0, 0.5, 0);
const WALLS = ["#f0d6a4", "#ecd0a0", "#f2dcb0", "#e8c898", "#e9c3a0", "#dcd2b8"], ROOFS = ["#d9542f", "#4f9a8c", "#e0643a", "#c0503a", "#5a8a9a", "#b8483a"];
const TREE_C = ["#c4c43c", "#a8c03a", "#8aa83a", "#b8b03a"];

const buildCity = () => {
  const walls: Inst[] = [], roofs: Inst[] = [], chim: Inst[] = [], winOn: Inst[] = [], winOff: Inst[] = [], roads: Inst[] = [], dashes: Inst[] = [], walks: Inst[] = [], trunks: Inst[] = [], crowns: Inst[] = [], towers: Inst[] = [], bands: Inst[] = [];
  const C = (h: string) => new THREE.Color(h);
  // street grid aligned with the hero block's two roads
  for (let k = -4; k <= 4; k++) {
    const zl = OZ + k * GRID, xl = OX + k * GRID;
    const segs = (line: number, isCore: boolean): [number, number][] => (isCore ? [[-CITY, -CORE], [CORE, CITY]] : Math.abs(line) < CORE ? [[-CITY, -CORE], [CORE, CITY]] : [[-CITY, CITY]]);
    for (const [a, b] of segs(zl, k === 0)) { roads.push({ m: M4((a + b) / 2, 0.015, zl, 0, b - a, 0.03, 1.9), c: C("#34303a") }); walks.push({ m: M4((a + b) / 2, 0.04, zl - 1.23, 0, b - a, 0.08, 0.56), c: C("#cdb995") }, { m: M4((a + b) / 2, 0.04, zl + 1.23, 0, b - a, 0.08, 0.56), c: C("#cdb995") });
      for (let x = a + 0.7; x < b; x += 1.3) dashes.push({ m: M4(x, 0.035, zl, 0, 0.55, 0.01, 0.08), c: C("#e8dcc0") }); }
    for (const [a, b] of segs(xl, k === 0)) { roads.push({ m: M4(xl, 0.016, (a + b) / 2, 0, 1.9, 0.03, b - a), c: C("#34303a") }); walks.push({ m: M4(xl - 1.23, 0.041, (a + b) / 2, 0, 0.56, 0.08, b - a), c: C("#cdb995") }, { m: M4(xl + 1.23, 0.041, (a + b) / 2, 0, 0.56, 0.08, b - a), c: C("#cdb995") });
      for (let z = a + 0.7; z < b; z += 1.3) dashes.push({ m: M4(xl, 0.036, z, 0, 0.08, 0.01, 0.55), c: C("#e8dcc0") }); }
  }
  // blocks: four houses each, some parks and a few towers near the core for a skyline
  let seed = 0;
  for (let bx = -4; bx < 4; bx++) for (let bz = -4; bz < 4; bz++) {
    const x0 = OX + bx * GRID + 1.6, z0 = OZ + bz * GRID + 1.6, size = GRID - 3.2, cx = x0 + size / 2, cz = z0 + size / 2;
    if (Math.abs(cx) < CORE + 4 && Math.abs(cz) < CORE + 4 && x0 < CORE && x0 + size > -CORE && z0 < CORE && z0 + size > -CORE) continue; // hero block
    const kind = rnd(bx * 31 + bz, 11);
    if (kind < 0.16) { // park: trees only
      for (let i = 0; i < 9; i++) { const x = x0 + 1 + rnd(seed, i) * (size - 2), z = z0 + 1 + rnd(seed, i + 20) * (size - 2), s = 0.9 + rnd(seed, i + 40) * 0.6; trunks.push({ m: M4(x, 0, z, 0, s, s * 1.1, s), c: C("#b2462a") }); crowns.push({ m: M4(x, 1.45 * s, z, rnd(seed, i), 0.6 * s, 0.68 * s, 0.6 * s), c: C(TREE_C[i % 4]) }); }
      seed++; continue;
    }
    if (kind > 0.88 && Math.hypot(cx, cz) < 34) { // tower block
      const fl = 5 + Math.floor(rnd(seed, 2) * 6), w = 5, d = 4;
      towers.push({ m: M4(cx, fl / 2, cz, 0, w, fl, d), c: C(["#d9733f", "#c8603a", "#e08a50"][seed % 3]) });
      for (let f = 1; f < fl; f++) bands.push({ m: M4(cx, f + 0.45, cz + d / 2 + 0.03, 0, w * 0.86, 0.5, 0.05), c: C(rnd(seed, f) > 0.45 ? "#ffcf73" : "#c8d0a0") });
      seed++; continue;
    }
    for (let i = 0; i < 4; i++) {
      const hx = x0 + (i % 2 ? size * 0.72 : size * 0.28), hz = z0 + (i < 2 ? size * 0.3 : size * 0.74), ry = i < 2 ? Math.PI : 0;
      const w = 2.2 + rnd(seed, 1) * 0.6, d = 2.0 + rnd(seed, 2) * 0.3, fl = rnd(seed, 3) > 0.5 ? 2 : 1, H = fl * 1.25, rh = w * 0.42;
      walls.push({ m: M4(hx, H / 2 + 0.1, hz, ry, w, H, d), c: C(WALLS[Math.floor(rnd(seed, 4) * 6)]) });
      roofs.push({ m: M4(hx, H + 0.1, hz, ry, w + 0.5, rh, d + 0.5), c: C(ROOFS[Math.floor(rnd(seed, 5) * 6)]) });
      chim.push({ m: M4(hx + Math.cos(ry) * w * 0.22, H + 0.1 + rh * 0.6, hz, ry, 0.32, rh * 0.9, 0.32), c: C("#c98a4a") });
      const fz = d / 2 + 0.03, dir = ry ? -1 : 1;
      for (let f = 0; f < fl; f++) for (let j = 0; j < 3; j++) {
        if (f === 0 && j === 2) continue;
        const wx = hx + (j - 1) * w * 0.3 * dir, wz = hz + fz * dir;
        (rnd(seed, 30 + f * 3 + j) > 0.4 ? winOn : winOff).push({ m: M4(wx, 0.72 + f * 1.25, wz, ry, 0.42, 0.5, 0.06), c: C("#ffffff") });
      }
      // a garden tree beside most houses
      if (rnd(seed, 6) > 0.3) { const tx = hx + (rnd(seed, 7) > 0.5 ? 1 : -1) * (w / 2 + 0.9), tz = hz + (rnd(seed, 8) - 0.5) * 1.5, s = 0.8 + rnd(seed, 9) * 0.5; trunks.push({ m: M4(tx, 0, tz, 0, s, s * 1.1, s), c: C("#b2462a") }); crowns.push({ m: M4(tx, 1.45 * s, tz, rnd(seed, 10), 0.58 * s, 0.66 * s, 0.58 * s), c: C(TREE_C[seed % 4]) }); }
      seed++;
    }
  }
  // forests on the hills and lone trees in the fields
  for (let i = 0; i < 2600; i++) {
    const a = rnd(i, 51) * Math.PI * 2, r = CITY + 4 + Math.pow(rnd(i, 52), 0.8) * 190, x = Math.cos(a) * r, z = Math.sin(a) * r;
    if (fbm(x * 0.02 + 9, z * 0.02) < 0.5 && rnd(i, 53) > 0.08) continue; // clustered woods
    const y = groundY(x, z), s = 1.2 + rnd(i, 54) * 1.4;
    trunks.push({ m: M4(x, y, z, 0, s, s * 1.1, s), c: C("#8a3a24") });
    crowns.push({ m: M4(x, y + 1.45 * s, z, rnd(i, 55), 0.62 * s, 0.75 * s, 0.62 * s), c: C(["#6a8a2a", "#7a9a30", "#5a7a28", "#8aa038"][i % 4]) });
  }
  return { walls, roofs, chim, winOn, winOff, roads, dashes, walks, trunks, crowns, towers, bands };
};

const Mountains: React.FC = () => {
  const items = useMemo(() => {
    const out: { p: [number, number, number]; r: number; h: number; ry: number; snow: boolean }[] = [];
    for (let i = 0; i < 26; i++) { const a = i / 26 * Math.PI * 2 + rnd(i, 61) * 0.2, d = 230 + rnd(i, 62) * 70; out.push({ p: [Math.cos(a) * d, -2, Math.sin(a) * d], r: 35 + rnd(i, 63) * 35, h: 45 + rnd(i, 64) * 55, ry: rnd(i, 65) * 3, snow: rnd(i, 66) > 0.25 }); }
    return out;
  }, []);
  return (
    <>
      {items.map((m, i) => (
        <group key={i} position={m.p} rotation={[0, m.ry, 0]}>
          <mesh position={[0, m.h / 2, 0]}><coneGeometry args={[m.r, m.h, 6, 1]} /><meshStandardMaterial color={["#7a6a8a", "#6a6a8a", "#8a7a8a"][i % 3]} flatShading roughness={1} /></mesh>
          {m.snow && <mesh position={[0, m.h * 0.86, 0]}><coneGeometry args={[m.r * 0.28 + 0.5, m.h * 0.28, 6, 1]} /><meshStandardMaterial color="#f4f0f4" flatShading roughness={0.9} /></mesh>}
        </group>
      ))}
    </>
  );
};

const Clouds: React.FC<{ f: number; tint: THREE.Color }> = ({ f, tint }) => {
  const items = useMemo(() => Array.from({ length: 16 }, (_, i) => ({ x: (rnd(i, 71) - 0.5) * 420, y: 45 + rnd(i, 72) * 35, z: (rnd(i, 73) - 0.5) * 420, s: 6 + rnd(i, 74) * 8 })), []);
  return (
    <>
      {items.map((c, i) => (
        <group key={i} position={[((c.x + f * 0.05 + 210) % 420) - 210, c.y, c.z]} scale={[c.s, c.s * 0.45, c.s * 0.8]}>
          {[0, 1, 2, 3].map(k => <mesh key={k} position={[(k - 1.5) * 0.9, rnd(i, k) * 0.4, (rnd(i, k + 4) - 0.5) * 0.8]} scale={0.7 + rnd(i, k + 8) * 0.5}><icosahedronGeometry args={[1, 0]} /><meshStandardMaterial color={tint} flatShading roughness={1} emissive={tint} emissiveIntensity={0.25} /></mesh>)}
        </group>
      ))}
    </>
  );
};

/** glow: window light 0..1; day: 0..1; sunDir: direction to the sun */
export const Surroundings: React.FC<{ f: number; glow: number; day: number; sunDir: THREE.Vector3 }> = ({ f, glow, day, sunDir }) => {
  const city = useMemo(buildCity, []);
  const mats = useMemo(() => ({
    std: new THREE.MeshStandardMaterial({ flatShading: true, roughness: 0.85 }),
    winOn: new THREE.MeshStandardMaterial({ color: "#ffcf73", emissive: "#ffcf73", emissiveIntensity: 0, flatShading: true, roughness: 0.3 }),
    winOff: new THREE.MeshStandardMaterial({ color: "#9cc2c8", flatShading: true, roughness: 0.3 }),
    band: new THREE.MeshStandardMaterial({ emissive: "#ffcf73", emissiveIntensity: 0, flatShading: true, roughness: 0.4 }),
  }), []);
  mats.winOn.emissiveIntensity = glow * 2.4; mats.winOn.color.set(glow > 0.05 ? "#ffcf73" : "#9cc2c8");
  mats.band.emissiveIntensity = glow * 1.6;
  const sunPos = sunDir.clone().normalize().multiplyScalar(300);
  return (
    <group>
      <Terrain />
      <Instanced geo={unitBox} items={city.roads} mat={mats.std} shadow={false} />
      <Instanced geo={unitBox} items={city.dashes} mat={mats.std} shadow={false} />
      <Instanced geo={unitBox} items={city.walks} mat={mats.std} />
      <Instanced geo={unitBox} items={city.walls} mat={mats.std} />
      <Instanced geo={unitRoof} items={city.roofs} mat={mats.std} />
      <Instanced geo={unitBox} items={city.chim} mat={mats.std} />
      <Instanced geo={unitBox} items={city.winOn} mat={mats.winOn} shadow={false} />
      <Instanced geo={unitBox} items={city.winOff} mat={mats.winOff} shadow={false} />
      <Instanced geo={unitBox} items={city.towers} mat={mats.std} />
      <Instanced geo={unitBox} items={city.bands} mat={mats.band} shadow={false} />
      <Instanced geo={trunkGeo} items={city.trunks} mat={mats.std} />
      <Instanced geo={crownGeo} items={city.crowns} mat={mats.std} />
      <Mountains />
      <Clouds f={f} tint={mixC("#4a4a6a", "#fff0e4", day)} />
      {day > 0.05 && sunDir.y > -2 && (
        <mesh position={sunPos}><sphereGeometry args={[9, 16, 10]} /><meshBasicMaterial color={new THREE.Color(3.2, 2.6, 1.8).multiplyScalar(day)} toneMapped={false} fog={false} /></mesh>
      )}
    </group>
  );
};
