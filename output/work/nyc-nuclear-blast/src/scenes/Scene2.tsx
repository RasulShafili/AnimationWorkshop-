import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { drawManhattanSkyline, drawThermalFireball } from "../nycPixelEngine";
import { HUDHeader } from "../components/HUDHeader";
import { theme } from "../theme";

export const Scene2: React.FC = () => {
  const frame = useCurrentFrame();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Fireball rapidly expands over first 30 frames and pulses
  const fireballProgress = interpolate(frame, [0, 35], [0.15, 1.0], { extrapolateRight: "clamp" });
  const vapR = interpolate(frame, [5, 45], [0, 140], { extrapolateRight: "clamp" });

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // Draw background skyline with Midtown vaporizing
    drawManhattanSkyline(ctx, frame, {
      vaporizeRadius: vapR,
      detonationY: 380
    });
    // Draw expanding thermal fireball
    drawThermalFireball(ctx, frame, fireballProgress);
  }, [frame, fireballProgress, vapR]);

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <HUDHeader
        badge="THERMAL RADIATION PHASE"
        title="100,000,000°C FIREBALL"
        alert={true}
        metrics={[
          { label: "CORE TEMPERATURE", value: "100 MILLION °C", alert: true },
          { label: "SOLAR COMPARISON", value: "4× HOTTER THAN SUN CORE" },
          { label: "GROUND ZERO", value: "VAPORIZED TO PLASMA", alert: true }
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

      {/* Physics Callout */}
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
            border: "2px solid #facc15",
            boxShadow: "0 0 35px rgba(250, 204, 21, 0.4)",
            borderRadius: 16,
            padding: "16px 24px",
            textAlign: "center"
          }}
        >
          <span
            style={{
              fontFamily: theme.fonts.mono,
              fontSize: 14,
              color: "#fde047",
              letterSpacing: "0.14em",
              textTransform: "uppercase",
              display: "block",
              marginBottom: 4
            }}
          >
            FIRST MILLISECOND OF DETONATION
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
            MIDTOWN STEEL & CONCRETE INSTANTLY VAPORIZED
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
