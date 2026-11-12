// Loads the precomputed simulation (public/snaps.bin, stars.bin, meta.json) once, outside the canvas.
import { useEffect, useState } from "react";
import { staticFile, delayRender, continueRender } from "remotion";
export type Sim = { N: number; S: number; QSCALE: number; dtSnap: number; times: number[]; cores: number[][][]; sep: number[]; sun: number; snaps: Int16Array; stars: Float32Array };
let cache: Promise<Sim> | null = null;
const load = () => cache ??= (async () => {
  const meta = await (await fetch(staticFile("meta.json"))).json();
  const snaps = new Int16Array(await (await fetch(staticFile("snaps.bin"))).arrayBuffer());
  const stars = new Float32Array(await (await fetch(staticFile("stars.bin"))).arrayBuffer());
  return { ...meta, snaps, stars } as Sim;
})();
export const useSim = () => {
  const [sim, setSim] = useState<Sim | null>(null);
  const [h] = useState(() => delayRender("sim data"));
  useEffect(() => { load().then(s => { setSim(s); continueRender(h); }); }, []);
  return sim;
};
// interpolated position of star i (or all stars into out) at sim time t
export const snapIndex = (sim: Sim, t: number) => { const x = Math.max(0, Math.min(sim.S - 1.001, t / sim.dtSnap)); const i = Math.floor(x); return [i, x - i] as const; };
export const coreAt = (sim: Sim, t: number, k: number) => { const [i, u] = snapIndex(sim, t); const a = sim.cores[i][k], b = sim.cores[i + 1][k]; return [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u]; };
export const starAt = (sim: Sim, t: number, s: number) => { const [i, u] = snapIndex(sim, t); const q = sim.QSCALE, o0 = (i * sim.N + s) * 3, o1 = ((i + 1) * sim.N + s) * 3; return [0, 1, 2].map(c => (sim.snaps[o0 + c] + (sim.snaps[o1 + c] - sim.snaps[o0 + c]) * u) / q); };
