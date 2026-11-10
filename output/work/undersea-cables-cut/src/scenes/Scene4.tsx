import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { theme } from "../theme";
import { BgMesh } from "../components/BgMesh";
import { HUDHeader } from "../components/HUDHeader";
import { pixelRect, pixelCircle, drawMicroSpark } from "../microPixel";

export const Scene4: React.FC<{ durationInFrames: number }> = ({ durationInFrames }) => {
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

  // Sever impact timing: anchor drags across from frame 25 to 60
  const impactProgress = interpolate(frame, [15, 45], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp"
  });
  const isCut = frame >= 40;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const w = canvas.width;
    const h = canvas.height;

    // Abyssal Seabed Ground (Basalt rocks and sediment at y = 520)
    const groundY = 520;
    pixelRect(ctx, 0, groundY, w, h - groundY, "#090d16");

    // Rock contours and sediment dithering
    for (let x = 0; x < w; x += 12) {
      const rockH = (Math.sin(x * 0.05) + Math.cos(x * 0.12)) * 8;
      pixelRect(ctx, x, groundY + rockH, 12, 6, "#1e293b");
    }

    // Hydrothermal smoker vent on left (x = 60)
    pixelRect(ctx, 50, groundY - 40, 30, 40, "#1f2937", "#374151");
    // Micro-pixel smoke particles rising
    for (let i = 0; i < 8; i++) {
      const spY = (groundY - 40) - ((frame * 1.5 + i * 20) % 140);
      const spX = 65 + Math.sin(frame * 0.1 + i) * 14;
      pixelCircle(ctx, spX, spY, 3 + (i % 3), "rgba(100, 116, 139, 0.45)");
    }

    // Bioluminescent deep sea creature (Anglerfish with lantern)
    const fishX = (w - (frame * 1.2) % (w + 100)) + 50;
    const fishY = 320 + Math.sin(frame * 0.08) * 15;
    if (fishX > -40 && fishX < w + 40) {
      // Fish body
      pixelCircle(ctx, fishX, fishY, 14, "#0f172a", "#1e293b");
      // Eye
      pixelCircle(ctx, fishX - 6, fishY - 3, 2, "#38bdf8");
      // Tail
      ctx.fillStyle = "#1e293b";
      ctx.beginPath();
      ctx.moveTo(fishX + 12, fishY);
      ctx.lineTo(fishX + 24, fishY - 8);
      ctx.lineTo(fishX + 24, fishY + 8);
      ctx.closePath();
      ctx.fill();
      // Lure & Bioluminescent bulb
      ctx.strokeStyle = "#475569";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(fishX - 8, fishY - 10);
      ctx.quadraticCurveTo(fishX - 22, fishY - 26, fishX - 20, fishY - 12);
      ctx.stroke();
      drawMicroSpark(ctx, fishX - 20, fishY - 12, 5, "#22d3ee");
    }

    // Undersea Armored Cable resting on seabed (y = 510)
    const cableY = 510;
    const cutX = 270;

    if (!isCut) {
      // Intact armored cable across entire screen
      pixelRect(ctx, 0, cableY - 7, w, 14, "#1e293b", "#475569");
      // Copper core line
      pixelRect(ctx, 0, cableY - 2, w, 4, "#d97706");
      // Pulsing fiber laser core
      pixelRect(ctx, 0, cableY, w, 1, "#22d3ee");
    } else {
      // Left severed cable section (snapped and bent downwards)
      pixelRect(ctx, 0, cableY - 7, cutX - 25, 14, "#1e293b", "#475569");
      pixelRect(ctx, 0, cableY - 2, cutX - 25, 4, "#d97706");
      // Right severed cable section
      pixelRect(ctx, cutX + 25, cableY - 7, w - (cutX + 25), 14, "#1e293b", "#475569");
      pixelRect(ctx, cutX + 25, cableY - 2, w - (cutX + 25), 4, "#d97706");

      // Frayed steel armor wires sticking out
      ctx.strokeStyle = "#94a3b8";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(cutX - 25, cableY - 5);
      ctx.lineTo(cutX - 10, cableY - 15);
      ctx.moveTo(cutX - 25, cableY + 5);
      ctx.lineTo(cutX - 12, cableY + 12);
      ctx.moveTo(cutX + 25, cableY - 5);
      ctx.lineTo(cutX + 12, cableY - 16);
      ctx.moveTo(cutX + 25, cableY + 5);
      ctx.lineTo(cutX + 14, cableY + 14);
      ctx.stroke();
    }

    // 15-Ton Ship Anchor dragging across seabed
    const anchorStartX = 140;
    const anchorEndX = 280;
    const anchorX = anchorStartX + impactProgress * (anchorEndX - anchorStartX);
    const anchorY = cableY - 25 + Math.sin(frame * 0.2) * 3;

    // Anchor chain links extending upwards to surface
    ctx.strokeStyle = "#64748b";
    ctx.lineWidth = 3;
    for (let link = 0; link < 10; link++) {
      const lx = anchorX + link * 18;
      const ly = anchorY - link * 32;
      pixelCircle(ctx, lx, ly, 6, "#334155", "#94a3b8");
    }

    // Massive forged iron anchor
    // Shank
    pixelRect(ctx, anchorX - 5, anchorY - 60, 10, 60, "#334155", "#94a3b8");
    // Stock / Crossbar
    pixelRect(ctx, anchorX - 24, anchorY - 50, 48, 6, "#1e293b", "#64748b");
    // Curved Flukes / Arms
    ctx.strokeStyle = "#475569";
    ctx.lineWidth = 8;
    ctx.beginPath();
    ctx.arc(anchorX, anchorY - 10, 28, 0, Math.PI);
    ctx.stroke();
    // Anchor flukes (sharp triangular blades digging in)
    ctx.fillStyle = "#94a3b8";
    ctx.beginPath();
    ctx.moveTo(anchorX - 28, anchorY - 10);
    ctx.lineTo(anchorX - 38, anchorY - 24);
    ctx.lineTo(anchorX - 20, anchorY - 18);
    ctx.closePath();
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(anchorX + 28, anchorY - 10);
    ctx.lineTo(anchorX + 38, anchorY - 24);
    ctx.lineTo(anchorX + 20, anchorY - 18);
    ctx.closePath();
    ctx.fill();

    // Catastrophic 10,000V DC Arc Flash & Short Circuit Explosion!
    if (isCut) {
      const arcFlash = Math.sin(frame * 0.8) > -0.2;
      if (arcFlash) {
        // High-voltage plasma explosion
        drawMicroSpark(ctx, cutX, cableY, 28, "#38bdf8");
        drawMicroSpark(ctx, cutX, cableY, 18, "#ffffff");

        // Branching electrical lightning bolts
        ctx.strokeStyle = "#67e8f9";
        ctx.lineWidth = 2;
        ctx.beginPath();
        for (let b = 0; b < 6; b++) {
          const boltAngle = (b * Math.PI) / 3 + (frame % 3) * 0.2;
          const dist = 35 + ((frame * 7 + b * 13) % 25);
          ctx.moveTo(cutX, cableY);
          ctx.lineTo(
            cutX + Math.cos(boltAngle) * (dist * 0.5) + ((b % 2) * 8 - 4),
            cableY + Math.sin(boltAngle) * (dist * 0.5) + ((b % 3) * 8 - 4)
          );
          ctx.lineTo(
            cutX + Math.cos(boltAngle) * dist,
            cableY + Math.sin(boltAngle) * dist
          );
        }
        ctx.stroke();

        // Shower of fiery micro-pixel copper sparks
        for (let s = 0; s < 16; s++) {
          const sparkAngle = Math.random() * Math.PI * 2;
          const sparkDist = Math.random() * 45;
          const sx = cutX + Math.cos(sparkAngle) * sparkDist;
          const sy = cableY + Math.sin(sparkAngle) * sparkDist;
          ctx.fillStyle = s % 2 === 0 ? "#facc15" : "#f97316";
          ctx.fillRect(Math.floor(sx), Math.floor(sy), 2, 2);
        }
      }
    }
  }, [frame, impactProgress, isCut]);

  return (
    <AbsoluteFill style={{ backgroundColor: "#020617" }}>
      <BgMesh />

      <HUDHeader
        badge="ABYSSAL INCIDENT // 04"
        title="4,200M DEPTH // ANCHOR SEVER"
        metrics={[
          { label: "PRESSURE", value: "420 ATMOSPHERES" },
          { label: "CONDUCTOR FAULT", value: "10,000V SHORT CIRCUIT" },
          { label: "PRIMARY CAUSE", value: "MERCHANT SHIP ANCHOR DRAG" }
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

      {/* Flashing Emergency Alarm Banner */}
      {isCut && (
        <div
          style={{
            position: "absolute",
            top: "66%",
            left: 40,
            right: 40,
            background: "rgba(220, 38, 38, 0.92)",
            border: "2px solid #f87171",
            boxShadow: "0 0 35px rgba(239, 68, 68, 0.7)",
            borderRadius: 14,
            padding: "16px 24px",
            textAlign: "center"
          }}
        >
          <div style={{ fontFamily: theme.fonts.display, fontSize: 24, fontWeight: 900, color: "#ffffff", letterSpacing: "0.06em" }}>
            ⚠️ CRITICAL FIBER CUT DETECTED
          </div>
          <div style={{ fontFamily: theme.fonts.mono, fontSize: 14, color: "#fef2f2", marginTop: 4 }}>
            LOCATION: SUEZ / RED SEA STRAIT • 10kV ARC FAULT • TOTAL DARK FIBER SHUTDOWN
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};
