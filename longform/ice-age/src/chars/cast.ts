import { Look } from "./Rig2";
// ice-age cast — original designs. Eli = grey hoodie + red beanie (the modern contrast); the band in warm hides.
export const ELI: Look = { top: "#8a909c", topDark: "#5e6470", pants: "#2c3a5a", shoes: "#f0ece2", style: "hoodie", hair: "beanie", hatColor: "#c8322a", skin: "#f2c8a8" };
export const ELI_PACK: Look = { ...ELI, backpack: "#2f4a6a" };
export const ELI_FUR: Look = { top: "#8a6a4a", topDark: "#5a4430", pants: "#5a4430", shoes: "#4a3426", style: "fur", hair: "beanie", hatColor: "#c8322a", skin: "#f2c8a8", necklace: "#efe6d6" };
export const NIA: Look = { top: "#a87a52", topDark: "#7a5636", pants: "#6a4a30", shoes: "#4a3426", style: "fur", hair: "braid", hairColor: "#3a2214", lashes: true, blush: true, paint: true, necklace: "#f4efe2", skin: "#c8946a" };
export const TOR: Look = { top: "#6a4a32", topDark: "#4a3222", pants: "#5a3e2a", shoes: "#3a2a1e", style: "fur", hair: "wild", hairColor: "#2a1a10", beard: true, scar: true, necklace: "#efe6d6", furTrim: "#5a4636", skin: "#e0b090", scale: 1.12 };
export const PIP: Look = { top: "#b08a60", topDark: "#806040", pants: "#6a4a30", shoes: "#4a3426", style: "fur", hair: "hood", hatColor: "#9a7450", blush: true, skin: "#f0c4a0", scale: 0.66 };
export const AMA: Look = { top: "#7a6a5a", topDark: "#54483c", pants: "#5a4a3a", shoes: "#3a2a1e", style: "fur", hair: "wild", hairColor: "#d8d6d0", lashes: true, necklace: "#e8c88a", skin: "#8a5a3e", scale: 0.94 };
export const BAND: Look[] = [
  { top: "#9a7a58", pants: "#5a4030", style: "fur", hair: "wild", hairColor: "#2a1a10", beard: true, skin: "#e8bc98", paint: true },
  { top: "#8a6448", pants: "#5a4030", style: "fur", hair: "braid", hairColor: "#1a120c", lashes: true, skin: "#5a3a2a", necklace: "#efe6d6" },
  { top: "#a88a64", pants: "#6a4a30", style: "fur", hair: "short", hairColor: "#2a1a10", skin: "#d8a07a", furTrim: "#8a7a64" },
  { top: "#7a5a40", pants: "#4a3424", style: "fur", hair: "wild", hairColor: "#3a2414", lashes: true, skin: "#7a4e34" },
  { top: "#b09070", pants: "#6a4a30", style: "fur", hair: "hood", hatColor: "#8a6a4a", skin: "#f0c8a8", scale: 0.7 },
];
export const VOSS: Look = { top: "#e8742a", topDark: "#a84e18", pants: "#3a3e4a", shoes: "#2a2a2a", style: "jacket", hair: "helmet", hatColor: "#f2f2f2", glasses: true, lashes: true, skin: "#f4d0b4", scale: 1.0 };
export const SCIENTIST: Look = { top: "#3a6ad8", pants: "#2a2e3a", style: "jacket", hair: "helmet", hatColor: "#f2c43a", skin: "#6a4430" };
