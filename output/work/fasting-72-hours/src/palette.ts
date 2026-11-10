export const PALETTE = {
  dark: "#1a1226",      // dark outline
  white: "#ffffff",     // white
  skinLight: "#f4d3b5", // skin light
  skinShade: "#e8a77c", // skin shade
  hotPink: "#ff5d8f",   // hot pink (cells / organs)
  cyan: "#2ee6ff",      // cyan (scavenger, energy)
  yellow: "#ffd93b",    // yellow (ketones, stem cells)
  orange: "#ff8a3d",    // orange (furnace, glycogen)
  brown: "#7a4a2b",     // brown (liver, furniture)
  red: "#c94a4a",       // red (blood, hunger)
  greyPurple: "#5b4a7a",// grey-purple
  peach: "#ffcfa3",     // peach
  brightGreen: "#b9f27c", // bright acid green / autophagy
  green: "#3fa35a",     // green
  blue: "#3b86ff",      // blue (hoodie)
  darkPurple: "#44395a" // dark purple
} as const;

export type Color = typeof PALETTE[keyof typeof PALETTE] | string;
