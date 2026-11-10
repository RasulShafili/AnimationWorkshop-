import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { drawOverpressureShockwave } from "../nycPixelEngine";
import { HUDHeader } from "../components/HUDHeader";
import { theme } from "../theme";

export const Scene3: React.FC = () => {
  const frame = useCurrentFrame();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const shockProgress = interpolate(frame, [0, 60], [0.1, 1.0], { extrapolateRight: "clamp" });

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawOverpressureShockwave(ctx, frame, shockProgress);
  }, [frame, shockProgress]);

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <HUDHeader
        badge="SUPERSONIC AIR BLAST"
        title="30 PSI OVERPRESSURE WAVE"
        alert={true}
        metrics={[
          { label: "PEAK OVERPRESSURE", value: "30+ PSI (200 KPA)", alert: true },
          { label: "BLAST VELOCITY", value: "750 MPH (SUPERSONIC)", alert: true },
          { label: "STRUCTURAL DAMAGE", value: "REINFORCED CONCRETE SHEAR" }
        ]}
      />

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
            background: "rgba(15, 23, 42, 0.94)",
            border: "2px solid #ef4444",
            boxShadow: "0 0 35px rgba(239, 68, 68, 0.4)",
            borderRadius: 16,
            padding: "16px 24px",
            textAlign: "center"
          }}
        >
          <span
            style={{
              fontFamily: theme.fonts.mono,
              fontSize: 14,
              color: "#f87171",
              letterSpacing: "0.14em",
              textTransform: "uppercase",
              display: "block",
              marginBottom: 4
            }}
          >
            KINETIC HYDRODYNAMICS
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
            SKYSCRAPERS TOPPLE LIKE DRY KINDLING
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
