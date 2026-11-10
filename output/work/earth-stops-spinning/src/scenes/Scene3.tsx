import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { HUDHeader } from "../components/HUDHeader";
import { theme } from "../theme";

export const Scene3: React.FC = () => {
  const frame = useCurrentFrame();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const W = canvas.width;
    const H = canvas.height;
    ctx.clearRect(0, 0, W, H);

    // 1. Dark stormy sky gradient
    const skyGrad = ctx.createLinearGradient(0, 0, 0, H);
    skyGrad.addColorStop(0, "#020617");
    skyGrad.addColorStop(0.5, "#0f172a");
    skyGrad.addColorStop(1, "#1e1b4b");
    ctx.fillStyle = skyGrad;
    ctx.fillRect(0, 0, W, H);

    // 2. Supersonic Mach Cones and Horizontal Wind Shock Streams
    const numShockStreams = 12;
    for (let s = 0; s < numShockStreams; s++) {
      const y = 180 + s * 38;
      const xOffset = ((frame * 24 + s * 95) % (W + 200)) - 100;
      const streamLen = 220 + (s % 4) * 60;

      ctx.save();
      const streamGrad = ctx.createLinearGradient(xOffset, y, xOffset + streamLen, y);
      streamGrad.addColorStop(0, "rgba(255, 255, 255, 0)");
      streamGrad.addColorStop(0.3, "rgba(56, 189, 248, 0.45)");
      streamGrad.addColorStop(1, "rgba(255, 255, 255, 0.95)");

      ctx.strokeStyle = streamGrad;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(xOffset, y);
      ctx.lineTo(xOffset + streamLen, y);
      ctx.stroke();

      // Shock wave angled cone
      ctx.strokeStyle = "rgba(255, 255, 255, 0.35)";
      ctx.beginPath();
      ctx.moveTo(xOffset + streamLen, y);
      ctx.lineTo(xOffset + streamLen - 45, y - 18);
      ctx.moveTo(xOffset + streamLen, y);
      ctx.lineTo(xOffset + streamLen - 45, y + 18);
      ctx.stroke();
      ctx.restore();
    }

    // 3. Bedrock Foundation & Stripped Soil
    const groundY = 680;
    // Bedrock base
    ctx.fillStyle = "#1e293b";
    ctx.fillRect(0, groundY + 40, W, H - (groundY + 40));
    // Stripped fractured bedrock top
    ctx.fillStyle = "#334155";
    ctx.fillRect(0, groundY + 15, W, 25);
    // Soil layer actively tearing away
    ctx.fillStyle = "#78350f";
    ctx.fillRect(0, groundY, W, 15);

    // 4. Micro-Pixel Skyscrapers being ripped and shattered sideways
    const buildings = [
      { x: 35, w: 55, h: 260, color: "#475569", winColor: "#38bdf8", shear: 28 },
      { x: 110, w: 75, h: 360, color: "#334155", winColor: "#facc15", shear: 42 },
      { x: 210, w: 90, h: 440, color: "#1e293b", winColor: "#22d3ee", shear: 58 },
      { x: 325, w: 65, h: 320, color: "#475569", winColor: "#f8fafc", shear: 36 },
      { x: 415, w: 80, h: 280, color: "#334155", winColor: "#38bdf8", shear: 32 }
    ];

    buildings.forEach((bld, bIdx) => {
      ctx.save();
      const topY = groundY - bld.h;
      // Shear distortion to show supersonic aerodynamic drag tearing the structure
      const currentShear = Math.min(bld.shear, (frame * 1.5 + bIdx * 5));

      // Building pillar silhouette
      ctx.fillStyle = bld.color;
      ctx.beginPath();
      ctx.moveTo(bld.x, groundY);
      ctx.lineTo(bld.x + bld.w, groundY);
      ctx.lineTo(bld.x + bld.w + currentShear, topY);
      ctx.lineTo(bld.x + currentShear, topY);
      ctx.closePath();
      ctx.fill();

      // Micro-pixel windows
      ctx.fillStyle = bld.winColor;
      for (let wy = topY + 15; wy < groundY - 20; wy += 22) {
        for (let wx = 6; wx < bld.w - 12; wx += 14) {
          const progress = (wy - topY) / bld.h;
          const shearX = currentShear * (1 - progress);
          ctx.fillRect(bld.x + wx + shearX, wy, 6, 9);
        }
      }

      // Fracture cracks across the building in micro-pixels
      ctx.strokeStyle = "#ef4444";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(bld.x + currentShear * 0.5, groundY - bld.h * 0.5);
      ctx.lineTo(bld.x + bld.w + currentShear * 0.7, groundY - bld.h * 0.3);
      ctx.lineTo(bld.x + bld.w + currentShear, groundY - bld.h * 0.15);
      ctx.stroke();

      ctx.restore();
    });

    // 5. High-Density Micro-Pixel Flying Debris Cloud (thousands of particles traveling East)
    const particleCount = 280;
    for (let p = 0; p < particleCount; p++) {
      const seed = p * 1337;
      const speed = 18 + (seed % 22);
      const px = ((frame * speed + seed) % (W + 300)) - 100;
      const py = 240 + (seed % 460) + Math.sin(frame * 0.3 + p) * 12;
      const pSize = 1 + (seed % 4);

      let pColor = "#cbd5e1";
      if (p % 4 === 0) pColor = "#ef4444"; // glowing structural spark
      else if (p % 4 === 1) pColor = "#facc15"; // shattered glass glint
      else if (p % 4 === 2) pColor = "#78350f"; // flying topsoil chunk

      ctx.fillStyle = pColor;
      ctx.fillRect(Math.floor(px), Math.floor(py), pSize, pSize);
    }

    // 6. Supersonic Wind Metric Callout
    ctx.save();
    ctx.fillStyle = "rgba(3, 8, 20, 0.88)";
    ctx.strokeStyle = "#ef4444";
    ctx.lineWidth = 2;
    ctx.fillRect(W / 2 - 190, 240, 380, 75);
    ctx.strokeRect(W / 2 - 190, 240, 380, 75);

    ctx.fillStyle = "#ef4444";
    ctx.font = "bold 13px 'JetBrains Mono', monospace";
    ctx.fillText("ATMOSPHERIC SHEAR VELOCITY", W / 2 - 170, 264);

    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 24px 'JetBrains Mono', monospace";
    ctx.fillText("465 M/S (MACH 1.35)", W / 2 - 170, 298);
    ctx.restore();
  }, [frame]);

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <HUDHeader
        badge="SUPERSONIC ATMOSPHERE"
        title="MACH 1.35 SURFACE SHEAR"
        alert={true}
        metrics={[
          { label: "WIND VELOCITY", value: "MACH 1.35 (1,670 KM/H)", alert: true },
          { label: "DYNAMIC PRESSURE", value: "350+ PSI", alert: true },
          { label: "STRUCTURAL DAMAGE", value: "TOTAL LEVELING" }
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
    </AbsoluteFill>
  );
};
