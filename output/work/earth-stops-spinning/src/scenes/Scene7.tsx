import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { renderEarthAftermath } from "../pixelGlobe";
import { HUDHeader } from "../components/HUDHeader";
import { theme } from "../theme";

export const Scene7: React.FC = () => {
  const frame = useCurrentFrame();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const rotDeg = 180 + frame * 0.4;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    renderEarthAftermath(ctx, 270, 480, 185, rotDeg, frame);
  }, [frame, rotDeg]);

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <HUDHeader
        badge="PLANETARY AFTERMATH"
        title="TRANSFORMED BIOSPHERE"
        metrics={[
          { label: "OCEAN REDISTRIBUTION", value: "POLES CONCENTRATION" },
          { label: "EQUATORIAL BULGE", value: "FLATTENED TO DESERT" },
          { label: "BIOSPHERE SURVIVAL", value: "< 0.01% CASUALTY RATE", alert: true }
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

      {/* Science Explanation Box */}
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
            border: "2px solid #38bdf8",
            boxShadow: "0 0 25px rgba(56, 189, 248, 0.35)",
            borderRadius: 16,
            padding: "16px 24px",
            textAlign: "center"
          }}
        >
          <span
            style={{
              fontFamily: theme.fonts.mono,
              fontSize: 14,
              color: "#38bdf8",
              letterSpacing: "0.14em",
              textTransform: "uppercase",
              display: "block",
              marginBottom: 4
            }}
          >
            GEODESIC RECONFIGURATION
          </span>
          <span
            style={{
              fontFamily: theme.fonts.display,
              fontSize: 24,
              fontWeight: 800,
              color: "#ffffff",
              lineHeight: 1.25
            }}
          >
            NO CENTRIFUGAL FORCE = 2 POLAR OCEANS
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
