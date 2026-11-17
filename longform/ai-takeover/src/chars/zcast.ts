import { Look } from "./Rig2";
// zombie-us cast — original designs. Accents: Kai = orange hoodie, Mira = yellow raincoat, Mom = navy scrubs,
// Ruiz = green FRESHWAY vest, Dana = teal paramedic, Holt = olive army. Infected = grey-green, pale glowing eyes.
export const KAI_PACK: Look = { top: "#e8742a", topDark: "#a84e18", pants: "#2c3046", shoes: "#f0ece2", style: "hoodie", hair: "messy", hairColor: "#17141c", skin: "#2a2532", backpack: "#3a4a3a" };
export const KAI: Look = { top: "#e8742a", topDark: "#a84e18", pants: "#2c3046", shoes: "#f0ece2", style: "hoodie", hair: "messy", hairColor: "#17141c", skin: "#2a2532" };
export const MIRA: Look = { top: "#f4c430", topDark: "#c8961a", pants: "#3a4a8a", shoes: "#d8423a", style: "raincoat", hair: "pigtails", hairColor: "#17141c", blush: true, lashes: true, skin: "#2a2532", scale: 0.68 };
export const MOM: Look = { top: "#2e4a7a", topDark: "#1e3254", pants: "#2e4a7a", shoes: "#f2f2f4", style: "scrubs", badge: true, hair: "bun", hairColor: "#17141c", lashes: true, skin: "#2a2532", scale: 1.02 };
export const RUIZ: Look = { top: "#e8e4da", topDark: "#b8b2a4", pants: "#2c2e38", shoes: "#2a1e18", style: "vest", vest: "#2f8a4e", hair: "short", hairColor: "#8e8e96", mustache: true, skin: "#2a2532", scale: 1.06 };
export const DANA: Look = { top: "#1f8a8a", topDark: "#136262", pants: "#1e2a36", shoes: "#141418", style: "uniform", hair: "ponytail", hairColor: "#3a2418", lashes: true, skin: "#2a2532", scale: 1.0 };
export const HOLT: Look = { top: "#5a6a3a", topDark: "#3e4a28", pants: "#4a5432", shoes: "#2a2418", style: "uniform", hair: "helmet", hatColor: "#4e5c32", skin: "#2a2532", scale: 1.1 };
export const RANCHER: Look = { top: "#7a4a8a", topDark: "#563266", pants: "#3a4a6a", shoes: "#5a3a22", style: "shirt", hair: "cowboy", hatColor: "#b8864a", mustache: true, hairColor: "#6a5a4a", skin: "#2a2532", scale: 1.08 };
export const GUARD: Look = { top: "#2a3448", topDark: "#1c2232", pants: "#1e2230", style: "shirt", tie: "#1a1e2a", hair: "cap", hatColor: "#1e2638", skin: "#2a2532", scale: 1.12 };
export const EXTRAS: Look[] = [
  { top: "#4f8fd8", pants: "#2a2a3a", style: "hoodie", hair: "short" }, { top: "#e7c34a", pants: "#3a3a4a", style: "jacket", hair: "long", hairColor: "#2a1a14", lashes: true },
  { top: "#59b07a", pants: "#2e2a3a", style: "hoodie", hair: "curly" }, { top: "#c66ab4", pants: "#2a2a3a", style: "cardigan", hair: "bun", hairColor: "#1a1418", lashes: true },
  { top: "#ef8c4a", pants: "#2b2e40", style: "jacket", hair: "cap", hatColor: "#2a4a8a" }, { top: "#7ac4d0", pants: "#3a3040", style: "shirt", hair: "short" },
  { top: "#8a6ac8", pants: "#2a2a3a", style: "coat", hair: "ponytail", hairColor: "#5a3a2a", lashes: true }, { top: "#d8d4ca", pants: "#3a3a4a", style: "suit", tie: "#a8323a", hair: "short" },
];
// professions for the infected crowd (learned from outlier zombie channels: a varied crowd reads as "everyone got it")
const JOBS: Look[] = [
  { top: "#d8c23a", pants: "#c8b030", shoes: "#2a2a24", style: "shirt", outfit: "hazmat", hair: "none" },
  { top: "#2a3a5a", pants: "#1e2638", style: "shirt", outfit: "police", hair: "cap", hatColor: "#1a2238" },
  { top: "#eef0f4", pants: "#1a2238", style: "shirt", outfit: "pilot", hair: "cap", hatColor: "#1a2238" },
  { top: "#5a6a7a", pants: "#3a3a2a", style: "shirt", outfit: "hivis", hair: "helmet", hatColor: "#f2c43a" },
  { top: "#b03a32", pants: "#3a4a6a", style: "shirt", outfit: "flannel", hair: "short" },
  { top: "#8ab8d8", pants: "#8ab8d8", style: "shirt", outfit: "nurse", hair: "bun", hairColor: "#3a2a20", lashes: true },
];
// infected: same clothes palette but desaturated, zombie skin/eyes
export const ZOMBIES: Look[] = [...EXTRAS.slice(0, 4), ...JOBS, ...EXTRAS.slice(4)].map((e, i) => ({ ...e, zombie: true, skin: ["#6b8068", "#728a6c", "#62786a", "#7a8a70"][i % 4], top: desat(e.top), topDark: undefined, scale: 0.95 + (i % 3) * 0.06 }));
function desat(hex: string) { const n = parseInt(hex.slice(1), 16); const r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255, m = (r + g + b) / 3;
  const c = (v: number) => Math.round(m * 0.55 + v * 0.45 * 0.8).toString(16).padStart(2, "0"); return `#${c(r)}${c(g)}${c(b)}`; }
export const zombiePose = (f: number, seed = 1, run = 0) => { const ph = f * (run ? 0.42 : 0.12) + seed * 1.7, s = Math.sin(ph), c = Math.cos(ph);
  return run ? { lean: 14, aL: [96 + 8 * s, 6], aR: [104 - 8 * s, 4], lL: [40 * s, 20 + 60 * Math.max(0, -c)], lR: [-40 * s, 20 + 60 * Math.max(0, c)], bob: -Math.abs(c) * 10, head: 8, mouth: "open" as const, brow: -0.6 }
    : { lean: 6 + 3 * s, aL: [84 + 6 * s, 10], aR: [90 - 6 * c, 6], lL: [16 * s, 6 + 14 * Math.max(0, -c)], lR: [-16 * s, 6 + 14 * Math.max(0, c)], bob: -Math.abs(c) * 3, head: 10 * Math.sin(ph * 0.5) + 6, mouth: "open" as const, brow: -0.6 }; };
