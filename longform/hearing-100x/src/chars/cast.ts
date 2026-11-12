import { Look } from "./Rig";
// our cast — original designs
export const HERO_PJ: Look = { top: "#5a7ab8", topDark: "#3a5288", pants: "#4a6aa4", stripes: "#a8c0ec", shoes: "#d8d4cc", hair: "tuft", headphones: "neck", hpColor: "#f0a83a" };
export const HERO: Look = { top: "#e2a63c", topDark: "#a8741e", pants: "#2c3046", shoes: "#e8e4dc", hair: "tuft", headphones: "neck", hpColor: "#f05a3a" };
export const NEIGHBOUR: Look = { top: "#7a6a5a", topDark: "#54483c", pants: "#3c3a44", hair: "grey", glasses: true, mustache: true, scale: 1.04 };
export const MEDIC: Look = { top: "#2a3a5a", pants: "#2a3a5a", vest: "#e8d23a", hair: "none", shoes: "#111" };
export const MIA: Look = { top: "#8a4ac8", topDark: "#5e2e92", pants: "#2a2a3a", hair: "tuft", shoes: "#f0f0f0" };
export const HERO_HP: Look = { ...HERO, headphones: "head" };
export const TEACHER1: Look = { top: "#3a6a6a", topDark: "#244a4a", pants: "#3a3240", hair: "grey", glasses: true, scale: 1.05 };
export const TEACHER2: Look = { top: "#c8c0b0", topDark: "#9a9284", pants: "#2a2a38", hair: "none", mustache: true, scale: 1.08 };
export const STUDENTS: Look[] = [
  { top: "#d84a4a", pants: "#2a2a3a", hair: "tuft" }, { top: "#4aa86a", pants: "#3a3040", hair: "none" },
  { top: "#4a6ad8", pants: "#2a2a3a", hair: "tuft" }, { top: "#e8c84a", pants: "#3a3a4a", hair: "none" },
  { top: "#c86ab8", pants: "#2a2a3a", hair: "tuft" }, { top: "#6ac8d8", pants: "#3a3040", hair: "none" },
];
