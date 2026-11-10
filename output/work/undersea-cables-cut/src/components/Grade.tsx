import React from "react";
import { AbsoluteFill } from "remotion";
import { theme } from "../theme";

export const Grade: React.FC<{ alert?: boolean }> = ({ alert = false }) => (
  <AbsoluteFill style={{ pointerEvents: "none" }}>
    <AbsoluteFill
      style={{
        backgroundColor: alert ? theme.colors.alertRed : theme.colors.primary,
        mixBlendMode: "soft-light",
        opacity: alert ? 0.22 : 0.16
      }}
    />
    <AbsoluteFill
      style={{
        background:
          "linear-gradient(180deg, rgba(0,0,0,0.18) 0%, transparent 22%, transparent 78%, rgba(0,0,0,0.35) 100%)"
      }}
    />
  </AbsoluteFill>
);
