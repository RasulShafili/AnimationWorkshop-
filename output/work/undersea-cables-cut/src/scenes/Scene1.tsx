import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { theme } from "../theme";
import { BgMesh } from "../components/BgMesh";
import { HUDHeader } from "../components/HUDHeader";
import { renderMicroPixelGlobe } from "../pixelGlobe";

export const Scene1: React.FC<{ durationInFrames: number }> = ({ durationInFrames }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  // Smooth entrance
  const entrance = spring({
    frame,
    fps,
    config: theme.spring.smooth
  });

  const globeScale = interpolate(entrance, [0, 1], [0.88, 1]);
  const globeOpacity = entrance;

  // Rotation angle for Earth: smooth orbit around globe
  const rotDeg = -40 + frame * 0.45;

  // Floating bob
  const floatY = Math.sin(frame * 0.08) * 8;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Clear background
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Render high-precision authentic micro-pixel globe
    // Globe center at cx = 270, cy = 410, R = 175
    renderMicroPixelGlobe(ctx, 270, 410, 175, rotDeg, frame, {
      highlightCut: false
    });
  }, [frame, rotDeg]);

  return (
    <AbsoluteFill style={{ backgroundColor: "#020617" }}>
      <BgMesh />

      {/* Top HUD */}
      <HUDHeader
        badge="GLOBAL INFRASTRUCTURE // 01"
        title="WHERE IS THE INTERNET?"
        metrics={[
          { label: "UNDERSEA CABLES", value: "99.1% OF TRAFFIC" },
          { label: "SATELLITES", value: "0.9% ONLY" },
          { label: "GLOBAL RUNS", value: "1,400,000 KM" }
        ]}
      />

      {/* Center Micro-Pixel Canvas (540x960 rendered pixel-crisp at 1080x1920) */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: 1080,
          height: 1920,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          pointerEvents: "none",
          transform: `translateY(${floatY}px) scale(${globeScale})`,
          opacity: globeOpacity,
          transformOrigin: "540px 820px"
        }}
      >
        <canvas
          ref={canvasRef}
          width={540}
          height={960}
          style={{
            width: 1080,
            height: 1920,
            imageRendering: "pixelated"
          }}
        />
      </div>

      {/* Center Callout Badge */}
      <div
        style={{
          position: "absolute",
          top: "66%",
          left: "50%",
          transform: "translateX(-50%)",
          background: "rgba(15, 23, 42, 0.9)",
          border: `1.5px solid ${theme.colors.heroCyan}`,
          boxShadow: `0 0 25px ${theme.colors.heroCyanGlow}`,
          borderRadius: 14,
          padding: "12px 28px",
          fontFamily: theme.fonts.display,
          fontSize: 24,
          fontWeight: 800,
          letterSpacing: "0.08em",
          color: theme.colors.accentGold,
          textTransform: "uppercase",
          pointerEvents: "none"
        }}
      >
        ⚡ 99% OF INTERNET ON OCEAN FLOOR
      </div>
    </AbsoluteFill>
  );
};
