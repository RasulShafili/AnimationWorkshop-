import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { theme } from "../theme";

export const BgMesh: React.FC<{ alert?: boolean }> = ({ alert = false }) => {
  const frame = useCurrentFrame();
  const d1 = Math.sin(frame / 45) * 60;
  const d2 = Math.cos(frame / 60) * 50;

  const primaryGlow = alert ? theme.colors.alertRed : theme.colors.primary;
  const secondaryGlow = alert ? theme.colors.copper : theme.colors.heroCyan;

  return (
    <AbsoluteFill style={{ backgroundColor: theme.colors.bgDark, overflow: "hidden" }}>
      {/* Deep gradient foundation */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: `radial-gradient(ellipse at 50% 25%, ${alert ? "#1a050b" : "#071b34"} 0%, #020617 75%)`
        }}
      />

      {/* Primary ambient light orb */}
      <div
        style={{
          position: "absolute",
          width: 800,
          height: 800,
          borderRadius: "50%",
          top: -200,
          left: -150 + d1,
          filter: "blur(90px)",
          background: `radial-gradient(circle, ${primaryGlow}28, transparent 65%)`
        }}
      />

      {/* Secondary accent orb */}
      <div
        style={{
          position: "absolute",
          width: 700,
          height: 700,
          borderRadius: "50%",
          bottom: 100,
          right: -150 - d2,
          filter: "blur(100px)",
          background: `radial-gradient(circle, ${secondaryGlow}18, transparent 65%)`
        }}
      />

      {/* Subtle subsea grid lines */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: `linear-gradient(to right, rgba(56, 189, 248, 0.03) 1px, transparent 1px),
                            linear-gradient(to bottom, rgba(56, 189, 248, 0.03) 1px, transparent 1px)`,
          backgroundSize: "60px 60px",
          opacity: 0.7
        }}
      />
    </AbsoluteFill>
  );
};
