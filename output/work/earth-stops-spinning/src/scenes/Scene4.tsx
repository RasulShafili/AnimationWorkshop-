import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { HUDHeader } from "../components/HUDHeader";
import { theme } from "../theme";

export const Scene4: React.FC = () => {
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

    // 1. Dark turbulent storm sky
    const skyGrad = ctx.createLinearGradient(0, 0, 0, H);
    skyGrad.addColorStop(0, "#020617");
    skyGrad.addColorStop(0.5, "#0b1528");
    skyGrad.addColorStop(1, "#082f49");
    ctx.fillStyle = skyGrad;
    ctx.fillRect(0, 0, W, H);

    // 2. Continental Shelf Topography & Mountain Silhouette in Micro-Pixels
    const terrainY = 660;
    ctx.fillStyle = "#1e293b";
    ctx.beginPath();
    ctx.moveTo(0, terrainY + 120);
    ctx.lineTo(160, terrainY + 90);
    ctx.lineTo(280, terrainY + 40); // Continental slope
    ctx.lineTo(390, terrainY - 60); // Coastal Mountain 1
    ctx.lineTo(440, terrainY - 20); // Mountain valley
    ctx.lineTo(510, terrainY - 110); // Mountain Peak 2
    ctx.lineTo(W, terrainY - 80);
    ctx.lineTo(W, H);
    ctx.lineTo(0, H);
    ctx.closePath();
    ctx.fill();

    // 3. Eastward Surging Mega-Tsunami Wall
    // Water surges from left to right with frame
    const surgeProgress = Math.min(1.0, frame / 180);
    const waveFrontX = 80 + surgeProgress * 420;
    const wavePeakY = 320 - Math.sin(frame * 0.08) * 20;

    // Deep water body
    const waterGrad = ctx.createLinearGradient(0, wavePeakY, 0, H);
    waterGrad.addColorStop(0, "rgba(56, 189, 248, 0.95)"); // Bright cyan crest
    waterGrad.addColorStop(0.2, "rgba(14, 116, 144, 0.95)"); // Emerald ocean body
    waterGrad.addColorStop(0.6, "rgba(8, 47, 73, 0.98)");   // Abyss
    waterGrad.addColorStop(1, "rgba(2, 6, 23, 1)");

    ctx.fillStyle = waterGrad;
    ctx.beginPath();
    ctx.moveTo(0, H);
    ctx.lineTo(0, wavePeakY + 40);
    // Huge curved tsunami wall leading to breaking curl
    ctx.quadraticCurveTo(
      waveFrontX * 0.6,
      wavePeakY - 40,
      waveFrontX,
      wavePeakY
    );
    // Breaking curl falling forward
    ctx.quadraticCurveTo(
      waveFrontX + 45,
      wavePeakY + 30,
      waveFrontX + 30,
      wavePeakY + 90
    );
    ctx.lineTo(waveFrontX - 20, terrainY + 80);
    ctx.lineTo(0, terrainY + 120);
    ctx.closePath();
    ctx.fill();

    // 4. Multi-Layer Micro-Pixel Foam & Whitecaps
    ctx.fillStyle = "#ffffff";
    for (let f = 0; f < 180; f++) {
      const foamProg = f / 180;
      const fx = waveFrontX - 80 + foamProg * 110 + Math.sin(frame * 0.2 + f) * 8;
      const fy = wavePeakY - 10 + foamProg * 80 + Math.cos(frame * 0.2 + f) * 12;
      ctx.fillRect(Math.floor(fx), Math.floor(fy), 2, 2);
    }

    // 5. Water Spray & Turbulent Mist Particles
    const sprayCount = 140;
    for (let s = 0; s < sprayCount; s++) {
      const seed = s * 733;
      const spx = waveFrontX + (seed % 120) + (frame * 6) % 180 - 40;
      const spy = wavePeakY - 60 + (seed % 140) + Math.sin(frame * 0.3 + s) * 15;
      ctx.fillStyle = s % 2 === 0 ? "#e0f2fe" : "#38bdf8";
      ctx.fillRect(Math.floor(spx), Math.floor(spy), 2, 2);
    }

    // 6. Hydrodynamic Surge Vector Arrows in Ocean Abyss
    ctx.save();
    ctx.strokeStyle = "rgba(34, 211, 238, 0.65)";
    ctx.lineWidth = 2;
    for (let a = 0; a < 5; a++) {
      const arrowY = 560 + a * 55;
      const arrowX = 40 + ((frame * 8 + a * 80) % 220);
      ctx.beginPath();
      ctx.moveTo(arrowX, arrowY);
      ctx.lineTo(arrowX + 45, arrowY);
      ctx.stroke();

      ctx.fillStyle = "#22d3ee";
      ctx.beginPath();
      ctx.moveTo(arrowX + 50, arrowY);
      ctx.lineTo(arrowX + 40, arrowY - 4);
      ctx.lineTo(arrowX + 40, arrowY + 4);
      ctx.closePath();
      ctx.fill();
    }
    ctx.restore();

    // 7. Mega-Tsunami Metric Badge
    ctx.save();
    ctx.fillStyle = "rgba(3, 8, 20, 0.9)";
    ctx.strokeStyle = "#38bdf8";
    ctx.lineWidth = 2;
    ctx.fillRect(W / 2 - 200, 220, 400, 72);
    ctx.strokeRect(W / 2 - 200, 220, 400, 72);

    ctx.fillStyle = "#38bdf8";
    ctx.font = "bold 13px 'JetBrains Mono', monospace";
    ctx.fillText("EASTWARD OCEAN KINETIC BULGE", W / 2 - 180, 244);

    ctx.fillStyle = "#f8fafc";
    ctx.font = "bold 22px 'JetBrains Mono', monospace";
    ctx.fillText("WAVE HEIGHT: 5,000+ METERS", W / 2 - 180, 276);
    ctx.restore();
  }, [frame]);

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <HUDHeader
        badge="HYDRODYNAMIC SURGE"
        title="GLOBAL MEGA-TSUNAMI WALL"
        alert={true}
        metrics={[
          { label: "OCEAN MASS", value: "1.4×10^18 TONS" },
          { label: "SURGE VELOCITY", value: "1,670 KM/H EAST", alert: true },
          { label: "COASTAL INUNDATION", value: "CONTINENT-SCALE" }
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
