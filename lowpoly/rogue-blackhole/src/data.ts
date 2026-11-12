// Loads the precomputed solar-system simulation once, outside the canvas.
import { useEffect, useState } from "react";
import { staticFile, delayRender, continueRender } from "remotion";
export type Sim = { N: number; S: number; Q: number; dtSnap: number; F: number; dtFine: number; cores: number[][][]; fates: any[]; snaps: Int16Array; bodies: Float32Array; fine: Float32Array };
let cache: Promise<Sim> | null = null;
const load = () => cache ??= (async () => {
  const meta = await (await fetch(staticFile("meta.json"))).json();
  const snaps = new Int16Array(await (await fetch(staticFile("snaps.bin"))).arrayBuffer());
  const bodies = new Float32Array(await (await fetch(staticFile("bodies.bin"))).arrayBuffer());
  const fine = new Float32Array(await (await fetch(staticFile("fine.bin"))).arrayBuffer());
  return { ...meta, snaps, bodies, fine } as Sim;
})();
export const useSim = () => {
  const [sim, setSim] = useState<Sim | null>(null);
  const [h] = useState(() => delayRender("sim data"));
  useEffect(() => { load().then(s => { setSim(s); continueRender(h); }); }, []);
  return sim;
};
export const idx = (sim: Sim, t: number) => { const x = Math.max(0, Math.min(sim.S - 1.001, t / sim.dtSnap)); const i = Math.floor(x); return [i, x - i] as const; };
// fine track: 8 planets (0-7), sun (8), black hole (9), sampled every dtFine years
const fineAt = (sim: Sim, t: number, k: number) => { const x = Math.max(0, Math.min(sim.F - 1.001, t / sim.dtFine)); const i = Math.floor(x), u = x - i; const o0 = (i * 10 + k) * 3, o1 = ((i + 1) * 10 + k) * 3; return [0, 1, 2].map(c => sim.fine[o0 + c] + (sim.fine[o1 + c] - sim.fine[o0 + c]) * u); };
export const coreAt = (sim: Sim, t: number, k: number) => fineAt(sim, t, 8 + k);
export const bodyAt = (sim: Sim, t: number, s: number) => s < 8 ? fineAt(sim, t, s) : (() => { const [i, u] = idx(sim, t); const o0 = (i * sim.N + s) * 3, o1 = ((i + 1) * sim.N + s) * 3; return [0, 1, 2].map(c => (sim.snaps[o0 + c] + (sim.snaps[o1 + c] - sim.snaps[o0 + c]) * u) / sim.Q); })();
