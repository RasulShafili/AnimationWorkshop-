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
export const DAD: Look = { top: "#4a5a3a", topDark: "#34402a", pants: "#2a2a34", hair: "none", glasses: true, scale: 1.08 };
export const UNCLE: Look = { top: "#b83a3a", topDark: "#882a2a", pants: "#2a2a34", hair: "grey", mustache: true, scale: 1.1 };
export const AUNT: Look = { top: "#6a4aa8", topDark: "#4a3480", pants: "#2a2a34", hair: "tuft", scale: 1.0 };
export const FRIEND: Look = { top: "#3a7ab8", topDark: "#2a5a88", pants: "#2a2a34", hair: "none", scale: 1.02 };
export const RESCUER: Look = { top: "#d8762a", topDark: "#a85a1e", pants: "#2a2e3a", vest: "#e8d23a", helmet: "#f0c020", hair: "none", shoes: "#1a1a1a" };
export const CHIEF: Look = { top: "#2a3a5a", topDark: "#1e2a44", pants: "#2a2e3a", helmet: "#f4f4f4", hair: "none", mustache: true, scale: 1.08 };
export const GIRL: Look = { top: "#e86aa8", topDark: "#b84a80", pants: "#3a3a5a", hair: "tuft", scale: 0.7 };
export const LEO: Look = { top: "#3a8ad8", topDark: "#2a6aa8", pants: "#2a2a3a", helmet: "#e84a4a", hair: "none", scale: 0.62 };
export const MIA_SNOW: Look = { ...MIA, top: "#7a3ab8", helmet: "#f0c040" };
export const HERO_SNOW: Look = { ...HERO, top: "#d8962c", headphones: "head" };
