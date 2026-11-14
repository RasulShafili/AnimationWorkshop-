import { Look } from "./Rig2";
// never-forget cast — original designs. Accent: Lina = gold (beanie, earring, memory eyes).
export const LINA: Look = { top: "#1f6f78", topDark: "#134a52", pants: "#2b2d44", shoes: "#efe9dc", style: "jacket", hair: "beanie", hatColor: "#e3a83b", earring: "#ffcc4d", lashes: true, blush: true, skin: "#2a2536" };
export const LINA_ADULT: Look = { ...LINA, hair: "long", hairColor: "#1a1622", scale: 1.06 };
export const AYLA: Look = { top: "#a58bc9", topDark: "#76619a", pants: "#4a4458", shoes: "#5a4a44", style: "cardigan", hair: "bun", hairColor: "#d8d6e2", glasses: true, lashes: true, blush: true, skin: "#2e2a38", scale: 0.95 };
export const OKAFOR: Look = { top: "#7a5a3e", topDark: "#54402c", pants: "#2c2a32", shoes: "#1a1614", style: "coat", hair: "short", beard: true, skin: "#221f2b", scale: 1.1 };
export const SAM: Look = { top: "#d2453e", topDark: "#9a2e2a", pants: "#34364a", shoes: "#f4f4f4", style: "hoodie", hair: "curly", skin: "#26232f", scale: 1.0 };
export const MANAGER: Look = { top: "#1b1a22", topDark: "#0e0d12", pants: "#1b1a22", shoes: "#0c0b0e", style: "suit", tie: "#d4a93a", hair: "short", skin: "#25222e", scale: 1.08 };
export const HALE: Look = { top: "#f2f2f4", topDark: "#c8ccd6", pants: "#3a4052", style: "labcoat", hair: "long", hairColor: "#2a1e1a", glasses: true, lashes: true, skin: "#2a2634", scale: 1.02 };
export const GUARD: Look = { top: "#24232c", pants: "#1c1b22", style: "suit", tie: "#24232c", hair: "bald", skin: "#211e29", scale: 1.22 };
export const COP: Look = { top: "#2d4266", topDark: "#1e2d48", pants: "#1e2436", style: "shirt", tie: "#1a2234", hair: "cap", hatColor: "#1e2a44", skin: "#24212e" };
export const EXTRAS: Look[] = [
  { top: "#4f8fd8", pants: "#2a2a3a", style: "hoodie", hair: "short" }, { top: "#e7c34a", pants: "#3a3a4a", style: "jacket", hair: "long", hairColor: "#2a1a14", lashes: true },
  { top: "#59b07a", pants: "#2e2a3a", style: "hoodie", hair: "curly" }, { top: "#c66ab4", pants: "#2a2a3a", style: "cardigan", hair: "bun", hairColor: "#1a1418", lashes: true },
  { top: "#ef8c4a", pants: "#2b2e40", style: "jacket", hair: "cap", hatColor: "#2a4a8a" }, { top: "#7ac4d0", pants: "#3a3040", style: "shirt", hair: "short" },
];
