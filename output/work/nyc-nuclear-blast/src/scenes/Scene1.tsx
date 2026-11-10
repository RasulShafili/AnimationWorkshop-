import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";
import { drawManhattanSkyline } from "../nycPixelEngine";
import { HUDHeader } from "../components/HUDHeader";
import { theme } from "../theme";

export const Scene1: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawManhattanSkyline(ctx, frame);
  }, [frame]);

  const pop = spring({
    frame,
    fps,
    config: theme.spring.smooth
  });

  const questionOpacity = interpolate(pop, [0, 1], [0, 1]);
  const questionY = interpolate(pop, [0, 1], [30, 0]);

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <HUDHeader
        badge="URBAN GEOPOLITICS SIMULATION"
        title="NEW YORK METROPOLITAN GRID"
        metrics={[
          { label: "TARGET WARHEAD", value: "800 KILOTONS (W88)" },
          { label: "POPULATION DENSITY", value: "8.4 MILLION" },
          { label: "GRID STATE", value: "PRE-DETONATION" }
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

      {/* Title Badge */}
      <div
        style={{
          position: "absolute",
          top: 350,
          left: 60,
          right: 60,
          display: "flex",
          justifyContent: "center",
          opacity: questionOpacity,
          transform: `translateY(${questionY}px)`,
          zIndex: 30
        }}
      >
        <div
          style={{
            background: "rgba(3, 8, 20, 0.92)",
            border: "2px solid #ef4444",
            boxShadow: "0 0 30px rgba(239, 68, 68, 0.4)",
            borderRadius: 16,
            padding: "18px 28px",
            textAlign: "center"
          }}
        >
          <span
            style={{
              fontFamily: theme.fonts.mono,
              fontSize: 15,
              color: "#f87171",
              letterSpacing: "0.15em",
              textTransform: "uppercase",
              display: "block",
              marginBottom: 6
            }}
          >
            HYPOTHETICAL NUCLEAR DETONATION
          </span>
          <span
            style={{
              fontFamily: theme.fonts.display,
              fontSize: 30,
              fontWeight: 800,
              color: "#f8fafc",
              lineHeight: 1.2
            }}
          >
            WHAT IF AN ATOM BOMB HIT NEW YORK?
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
