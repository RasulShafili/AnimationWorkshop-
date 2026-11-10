import { Easing } from "remotion";

export const theme = {
  colors: {
    bgDark: "#020617",
    bgNavy: "#081b33",
    surfaceCard: "rgba(8, 20, 40, 0.82)",
    primary: "#0284c7",
    heroCyan: "#22d3ee",
    heroCyanGlow: "rgba(34, 211, 238, 0.35)",
    accentGold: "#facc15",
    accentGoldGlow: "rgba(250, 204, 21, 0.35)",
    alertRed: "#ef4444",
    alertRedGlow: "rgba(239, 68, 68, 0.4)",
    successGreen: "#10b981",
    copper: "#d97706",
    steel: "#94a3b8",
    steelDark: "#475569",
    textWhite: "#f8fafc",
    textMuted: "#94a3b8",
    borderSubtle: "rgba(56, 189, 248, 0.25)"
  },
  fonts: {
    display: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    mono: "'JetBrains Mono', 'Fira Code', 'Courier New', monospace"
  },
  spring: {
    smooth: { damping: 18, stiffness: 90, mass: 0.8 },
    snappy: { damping: 14, stiffness: 140, mass: 0.6 },
    bouncy: { damping: 10, stiffness: 100, mass: 0.7 }
  },
  ease: {
    out: Easing.bezier(0.16, 1, 0.3, 1),
    inOut: Easing.bezier(0.65, 0, 0.35, 1),
    in: Easing.bezier(0.7, 0, 0.84, 0)
  }
};
