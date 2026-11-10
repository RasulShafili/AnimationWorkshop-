import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { theme } from "../theme";
import { BgMesh } from "../components/BgMesh";
import { HUDHeader } from "../components/HUDHeader";
import { pixelRect, pixelCircle, drawMicroSpark } from "../microPixel";

export const Scene8: React.FC<{ durationInFrames: number }> = ({ durationInFrames }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  const entrance = spring({
    frame,
    fps,
    config: theme.spring.smooth
  });

  const scale = interpolate(entrance, [0, 1], [0.92, 1]);
  const opacity = entrance;

  // Arc discharge timing: occurs at frame 35-70
  const isArcFiring = frame >= 30 && frame <= 75;
  const isFused = frame > 75;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const w = canvas.width;
    const cy = 410;
    const cx = 270;

    // Microscope Chamber Frame (380x240)
    const cw = 380;
    const ch = 240;
    pixelRect(ctx, cx - cw / 2, cy - ch / 2, cw, ch, "#020617", "#0ea5e9");

    // Microscope Crosshairs & Nanometer Graticule
    ctx.strokeStyle = "rgba(14, 165, 233, 0.25)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(cx - cw / 2 + 10, cy);
    ctx.lineTo(cx + cw / 2 - 10, cy);
    ctx.moveTo(cx, cy - ch / 2 + 10);
    ctx.lineTo(cx, cy + ch / 2 - 10);
    ctx.stroke();

    // Tungsten Electrodes (Top & Bottom)
    // Top Electrode (needle pointing down)
    ctx.fillStyle = "#94a3b8";
    ctx.beginPath();
    ctx.moveTo(cx - 8, cy - ch / 2);
    ctx.lineTo(cx + 8, cy - ch / 2);
    ctx.lineTo(cx + 2, cy - 36);
    ctx.lineTo(cx - 2, cy - 36);
    ctx.closePath();
    ctx.fill();
    pixelCircle(ctx, cx, cy - 35, 3, "#f8fafc");

    // Bottom Electrode (needle pointing up)
    ctx.fillStyle = "#94a3b8";
    ctx.beginPath();
    ctx.moveTo(cx - 8, cy + ch / 2);
    ctx.lineTo(cx + 8, cy + ch / 2);
    ctx.lineTo(cx + 2, cy + 36);
    ctx.lineTo(cx - 2, cy + 36);
    ctx.closePath();
    ctx.fill();
    pixelCircle(ctx, cx, cy + 35, 3, "#f8fafc");

    // Left Optical Fiber Strand (125 Microns)
    const gap = isFused ? 0 : interpolate(frame, [0, 30], [28, 6], { extrapolateRight: "clamp" });
    const leftFiberEnd = cx - gap;
    pixelRect(ctx, cx - cw / 2 + 20, cy - 14, leftFiberEnd - (cx - cw / 2 + 20), 28, "#1e293b", "#38bdf8");
    // Left Core (9 Microns)
    pixelRect(ctx, cx - cw / 2 + 20, cy - 3, leftFiberEnd - (cx - cw / 2 + 20), 6, "#67e8f9");

    // Right Optical Fiber Strand (125 Microns)
    const rightFiberStart = cx + gap;
    pixelRect(ctx, rightFiberStart, cy - 14, (cx + cw / 2 - 20) - rightFiberStart, 28, "#1e293b", "#38bdf8");
    // Right Core (9 Microns)
    pixelRect(ctx, rightFiberStart, cy - 3, (cx + cw / 2 - 20) - rightFiberStart, 6, "#67e8f9");

    // Precision V-Groove Alignment Blocks
    pixelRect(ctx, cx - 140, cy + 24, 70, 20, "#334155", "#64748b");
    pixelRect(ctx, cx + 70, cy + 24, 70, 20, "#334155", "#64748b");

    // High-Voltage Plasma Arc Discharge during Fusion!
    if (isArcFiring) {
      // Intense plasma flare between electrodes
      const arcWidth = 24 + (frame % 3) * 6;
      ctx.strokeStyle = "#ffffff";
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(cx, cy - 35);
      ctx.lineTo(cx + ((frame % 2) * 6 - 3), cy);
      ctx.lineTo(cx, cy + 35);
      ctx.stroke();

      // Cyan plasma cloud
      pixelCircle(ctx, cx, cy, arcWidth * 0.7, "rgba(56, 189, 248, 0.45)");
      drawMicroSpark(ctx, cx, cy, 18, "#ffffff");
      drawMicroSpark(ctx, cx, cy - 15, 8, "#38bdf8");
      drawMicroSpark(ctx, cx, cy + 15, 8, "#38bdf8");
    }

    // If Fused: Glowing unbroken laser line across the splice
    if (isFused) {
      pixelRect(ctx, cx - 6, cy - 3, 12, 6, "#ffffff");
      drawMicroSpark(ctx, cx, cy, 6, "#facc15");
    }

    // Microscope HUD Overlay text
    ctx.font = "bold 11px monospace";
    ctx.fillStyle = "#38bdf8";
    ctx.fillText("AXIAL OFFSET: 0.01 µm", cx - cw / 2 + 16, cy - ch / 2 + 24);
    ctx.fillText("CORE DIAMETER: 9.0 µm", cx - cw / 2 + 16, cy - ch / 2 + 40);

    ctx.fillStyle = isFused ? "#22c55e" : "#f59e0b";
    ctx.fillText(
      isFused ? "SPLICE STATUS: PASSED (0.02 dB)" : isArcFiring ? "ARC DISCHARGE IN PROGRESS..." : "ALIGNING CORES...",
      cx - cw / 2 + 16,
      cy + ch / 2 - 16
    );
  }, [frame, isArcFiring, isFused]);

  return (
    <AbsoluteFill style={{ backgroundColor: "#020617" }}>
      <BgMesh />

      <HUDHeader
        badge="OPTICAL MICROSURGERY // 08"
        title="0.01 MICRON LASER FUSION SPLICING"
        metrics={[
          { label: "GLASS TOLERANCE", value: "0.01 MICRONS" },
          { label: "ARC TEMPERATURE", value: "2,000°C PLASMA" },
          { label: "SPLICE LOSS", value: isFused ? "0.02 dB [PERFECT]" : "CALIBRATING..." }
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
          transform: `scale(${scale})`,
          opacity,
          transformOrigin: "540px 840px"
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

      {/* Microscope Callout Box */}
      <div
        style={{
          position: "absolute",
          top: "66%",
          left: 40,
          right: 40,
          background: "rgba(15, 23, 42, 0.92)",
          border: `1.5px solid ${theme.colors.heroCyan}`,
          boxShadow: `0 0 25px ${theme.colors.heroCyanGlow}`,
          borderRadius: 14,
          padding: "16px 24px"
        }}
      >
        <div style={{ fontFamily: theme.fonts.display, fontSize: 20, fontWeight: 800, color: theme.colors.accentGold }}>
          HAIR-THIN GLASS FUSED BY 2000°C PLASMA ARC
        </div>
        <div style={{ fontFamily: theme.fonts.mono, fontSize: 14, color: "#e2e8f0", marginTop: 4 }}>
          Each individual hair-thin fiber is welded under a shipboard microscope. Once all fibers are spliced and hermetically resealed, the global network springs back to life.
        </div>
      </div>
    </AbsoluteFill>
  );
};
