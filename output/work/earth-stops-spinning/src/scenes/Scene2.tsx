import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { renderEarthInertia } from "../pixelGlobe";
import { HUDHeader } from "../components/HUDHeader";
import { theme } from "../theme";

export const Scene2: React.FC = () => {
  const frame = useCurrentFrame();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // In Scene 2, the Earth abruptly halts!
  // Slow down rotation to a sudden dead stop over first 25 frames
  const stopProgress = interpolate(frame, [0, 25], [0, 1], { extrapolateRight: "clamp" });
  const rotDeg = 45 + (1 - stopProgress) * 5;

  const alertProgress = interpolate(frame, [10, 35], [0, 1], { extrapolateRight: "clamp" });

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // Draw micro-pixel inertia Earth
    renderEarthInertia(ctx, 270, 480, 185, rotDeg, frame, alertProgress);
  }, [frame, rotDeg, alertProgress]);

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      {/* HUD Header */}
      <HUDHeader
        badge="PHYSICS INERTIA ANALYSIS"
        title="MOMENTUM CONSERVATION"
        alert={true}
        metrics={[
          { label: "EQUATORIAL INERTIA", value: "1,670 KM/H", alert: true },
          { label: "45° LATITUDE", value: "1,180 KM/H" },
          { label: "PLANET ROTATION", value: "0.0 KM/H [FROZEN]", alert: true }
        ]}
      />

      {/* Micro-Pixel Canvas (540x960 native space, scaled 2x to 1080x1920) */}
      <canvas
        ref={canvasRef}
        width={540}
        height={960}
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: 1080,
          height: 1920,
          imageRendering: "pixelated"
        }}
      />

      {/* Physics Principle Callout */}
      <div
        style={{
          position: "absolute",
          top: 350,
          left: 60,
          right: 60,
          display: "flex",
          justifyContent: "center",
          zIndex: 30
        }}
      >
        <div
          style={{
            background: "rgba(15, 23, 42, 0.92)",
            border: "2px solid #ef4444",
            boxShadow: "0 0 30px rgba(239, 68, 68, 0.4)",
            borderRadius: 16,
            padding: "16px 24px",
            textAlign: "center"
          }}
        >
          <span
            style={{
              fontFamily: theme.fonts.mono,
              fontSize: 15,
              color: "#f87171",
              letterSpacing: "0.14em",
              textTransform: "uppercase",
              display: "block",
              marginBottom: 4
            }}
          >
            NEWTON'S FIRST LAW
          </span>
          <span
            style={{
              fontFamily: theme.fonts.display,
              fontSize: 26,
              fontWeight: 800,
              color: "#ffffff",
              lineHeight: 1.25
            }}
          >
            UNANCHORED MASS FLIES EASTWARD AT 465 M/S
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
