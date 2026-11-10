import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";
import { renderEarthSpinning } from "../pixelGlobe";
import { HUDHeader } from "../components/HUDHeader";
import { theme } from "../theme";

export const Scene1: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Rotation speed: 0.6 degrees per frame
  const rotDeg = frame * 0.7;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // Draw micro-pixel spinning Earth
    renderEarthSpinning(ctx, 270, 480, 185, rotDeg, frame, {
      showEquatorSpeed: true,
      showCoordinates: true
    });
  }, [frame, rotDeg]);

  const pop = spring({
    frame,
    fps,
    config: theme.spring.smooth
  });

  const questionOpacity = interpolate(pop, [0, 1], [0, 1]);
  const questionY = interpolate(pop, [0, 1], [30, 0]);

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      {/* HUD Header */}
      <HUDHeader
        badge="PLANETARY DYNAMICS"
        title="EARTH ROTATIONAL INERTIA"
        metrics={[
          { label: "EQUATOR VELOCITY", value: "1,670 KM/H" },
          { label: "ANGULAR SPEED", value: "465.1 M/S" },
          { label: "STATE", value: "STABLE ROTATION" }
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

      {/* Prominent Question Badge */}
      <div
        style={{
          position: "absolute",
          top: 360,
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
            background: "rgba(3, 8, 20, 0.9)",
            border: "2px solid #22d3ee",
            boxShadow: "0 0 25px rgba(34, 211, 238, 0.4)",
            borderRadius: 16,
            padding: "16px 28px",
            textAlign: "center"
          }}
        >
          <span
            style={{
              fontFamily: theme.fonts.mono,
              fontSize: 16,
              color: "#38bdf8",
              letterSpacing: "0.15em",
              textTransform: "uppercase",
              display: "block",
              marginBottom: 6
            }}
          >
            HYPOTHETICAL CATACLYSM
          </span>
          <span
            style={{
              fontFamily: theme.fonts.display,
              fontSize: 32,
              fontWeight: 800,
              color: "#f8fafc",
              letterSpacing: "-0.01em",
              lineHeight: 1.2
            }}
          >
            WHAT IF EARTH STOPPED FOR 1 SECOND?
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
