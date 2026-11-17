// AI-takeover cast (all original). Mixed skin tones, light-skinned hero (owner 2026-11-16). No near-black skin hex.
import { Look } from "./Rig2";
import type { RobotLook } from "./Robot";
export const LEO: Look = { top: "#3f8a4e", topDark: "#2a6038", pants: "#2c3a5a", shoes: "#e8e2d4", style: "hoodie", hair: "messy", hairColor: "#c8642a", skin: "#f4ccb0", blush: true };
export const LEO_RAIN: Look = { ...LEO, top: "#356f42", topDark: "#244c2e", backpack: "#3a3a44" };
export const WALT: Look = { top: "#b8402e", topDark: "#86301f", pants: "#3e4a5e", shoes: "#4a3a2a", style: "shirt", outfit: "flannel", hair: "cap", hatColor: "#3a5a3a", mustache: true, hairColor: "#e8e4dc", skin: "#f0c4a4", scale: 1.04 };
export const ZARA: Look = { top: "#7a4ab8", topDark: "#563488", pants: "#2a2a36", shoes: "#f0ece4", style: "jacket", hair: "long", hairColor: "#1e1612", glasses: true, lashes: true, earring: "#ffd34a", skin: "#7a4e34" };
export const REYES: Look = { top: "#5e6a42", topDark: "#404a2c", pants: "#4a5434", shoes: "#2a2418", style: "uniform", hair: "helmet", hatColor: "#55603a", lashes: true, skin: "#c8956a", scale: 1.02 };
export const SOLDIERS: Look[] = ["#e8b896", "#8a5a3e", "#c8956a", "#f2c8a8", "#6e4a34"].map((skin, i) => ({ top: "#5e6a42", topDark: "#404a2c", pants: "#4a5434", shoes: "#2a2418", style: "uniform" as const, hair: "helmet" as const, hatColor: "#55603a", skin, scale: 1 + (i % 3) * 0.04 }));
export const PIKE: Look = { top: "#8a7a62", topDark: "#5e5242", pants: "#4a4a52", style: "cardigan", hair: "bald", mustache: true, hairColor: "#c8c4bc", glasses: true, skin: "#e8bc98", scale: 0.98 };
export const PIKE_DAUGHTER: Look = { top: "#3a7ac8", pants: "#2a2e3a", style: "jacket", hair: "ponytail", hairColor: "#6a3a1a", lashes: true, skin: "#f0c8a8" };
// easter eggs from our earlier videos (zombie: Mira's yellow raincoat; never-forget: Okafor's coat, Lina's mustard beanie)
export const RAINCOAT_GIRL: Look = { top: "#f2c21a", topDark: "#c09610", pants: "#3a4a6a", style: "raincoat", hair: "pigtails", hairColor: "#2a1a10", blush: true, lashes: true, skin: "#c8946a", scale: 0.62 };
export const OKAFOR_EGG: Look = { top: "#7a5a3a", topDark: "#54402a", pants: "#3a3a44", style: "coat", hair: "short", hairColor: "#1e1814", skin: "#8a5a3e", scale: 1.06 };
export const LINA_EGG: Look = { top: "#1f6e6a", topDark: "#14504c", pants: "#2a2a36", style: "jacket", hair: "beanie", hatColor: "#e0a53a", earring: "#ffd34a", lashes: true, skin: "#f2c8a8", scale: 0.92 };
export const EXTRAS: Look[] = [
  { top: "#c8582a", pants: "#2a3448", style: "jacket", hair: "short", hairColor: "#3a2a1a", skin: "#f0c8a8" },
  { top: "#3a6ad8", pants: "#2a2e3a", style: "hoodie", hair: "curly", hairColor: "#1e1612", skin: "#8a5a3e" },
  { top: "#d8a03a", pants: "#4a3a2a", style: "cardigan", hair: "bun", hairColor: "#c8c4bc", lashes: true, skin: "#e8bc98", scale: 0.95 },
  { top: "#2f8a7a", pants: "#2a2a36", style: "scrubs", hair: "ponytail", hairColor: "#2a1a10", lashes: true, skin: "#c8956a" },
  { top: "#8a3a5a", pants: "#2a2e3a", style: "coat", hair: "short", hairColor: "#d8c088", skin: "#f4d0b4", scale: 1.05 },
  { top: "#5a5a6a", pants: "#3a3a44", style: "shirt", outfit: "flannel", hair: "cap", hatColor: "#b8402e", skin: "#a87050" },
  { top: "#e8e2d4", pants: "#3a3e4a", style: "labcoat", hair: "short", hairColor: "#1e1612", glasses: true, skin: "#e0b090" },
  { top: "#4a7a3a", pants: "#2a2e3a", style: "vest", vest: "#f08a1a", hair: "beanie", hatColor: "#2a5a8a", skin: "#6e4a34" },
];
// robots
export const BOLT: RobotLook = { shell: 1, mode: "calm", tag: "B0LT", scale: 0.82, plate: "#f2efe6", smiley: true };
export const BOLT_1ARM: RobotLook = { ...BOLT, dmg: 0.4, noArmR: true };
export const HELPERS: RobotLook = { shell: 1, mode: "calm", tag: "ORIN" };
export const HUNTER: RobotLook = { shell: 0, mode: "hostile", frame: "#2e333c", scale: 1.12, gun: true };
export const HELPER_GUN: RobotLook = { ...HELPERS, gun: true };
