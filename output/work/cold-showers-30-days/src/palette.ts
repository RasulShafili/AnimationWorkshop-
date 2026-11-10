export const PALETTE = {
  dark: "#1a1226",      // dark outline
  white: "#ffffff",     // white
  skinLight: "#f4d3b5", // skin light
  skinShade: "#e8a77c", // skin shade
  hotPink: "#ff5d8f",   // hot pink (brain)
  cyan: "#2ee6ff",      // cyan (accent, sweat, energy)
  yellow: "#ffd93b",    // yellow (highlight, aura)
  orange: "#ff8a3d",    // orange
  brown: "#7a4a2b",     // brown (shoes, hair)
  red: "#c94a4a",       // red (urges, danger)
  greyPurple: "#5b4a7a",// grey-purple
  peach: "#ffcfa3",     // peach
  brightGreen: "#b9f27c", // bright green (focus, boost)
  green: "#3fa35a",     // green
  blue: "#3b86ff",      // blue (hoodie)
  darkPurple: "#44395a" // dark purple (vignette, bg)
} as const;

export type Color = typeof PALETTE[keyof typeof PALETTE] | string;
