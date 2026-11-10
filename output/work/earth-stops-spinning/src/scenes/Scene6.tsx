import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { renderEarthQuakeFaults } from "../pixelGlobe";
import { HUDHeader } from "../components/HUDHeader";
import { theme } from "../theme";

export const Scene6: React.FC = () => {
  const frame = useCurrentFrame();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Earth spins again, causing intense tectonic friction
  const rotDeg = 120 + frame * 0.9;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const W = canvas.width;
    const H = canvas.height;
    ctx.clearRect(0, 0, W, H);

    // 1. Render globe with glowing red tectonic fault lines
    renderEarthQuakeFaults(ctx, 270, 460, 185, rotDeg, frame);

    // 2. Real-Time Seismograph Oscilloscope at Bottom
    const seismoY = 720;
    const seismoH = 80;
    const seismoW = 460;
    const seismoX = (W - seismoW) / 2;

    ctx.save();
    ctx.fillStyle = "rgba(3, 8, 20, 0.9)";
    ctx.strokeStyle = "#ef4444";
    ctx.lineWidth = 1.5;
    ctx.fillRect(seismoX, seismoY, seismoW, seismoH);
    ctx.strokeRect(seismoX, seismoY, seismoW, seismoH);

    // Seismograph grid lines
    ctx.strokeStyle = "rgba(239, 68, 68, 0.2)";
    ctx.lineWidth = 1;
    for (let gy = seismoY + 15; gy < seismoY + seismoH; gy += 18) {
      ctx.beginPath();
      ctx.moveTo(seismoX, gy);
      ctx.lineTo(seismoX + seismoW, gy);
      ctx.stroke();
    }

    // Needle seismic trace
    ctx.strokeStyle = "#ef4444";
    ctx.lineWidth = 2;
    ctx.shadowColor = "#ef4444";
    ctx.shadowBlur = 8;
    ctx.beginPath();
    for (let x = 0; x < seismoW; x += 3) {
      const t = (frame * 6 + x * 0.8);
      // High-frequency chaos oscillation mimicking M12 quake
      const wave =
        Math.sin(t * 0.2) * 22 +
        Math.cos(t * 0.55) * 14 +
        Math.sin(t * 1.3) * 6;
      const y = seismoY + seismoH / 2 + wave;
      if (x === 0) ctx.moveTo(seismoX + x, y);
      else ctx.lineTo(seismoX + x, y);
    }
    ctx.stroke();

    // Seismograph HUD readout
    ctx.fillStyle = "#ef4444";
    ctx.font = "bold 12px 'JetBrains Mono', monospace";
    ctx.fillText("SEISMOGRAPH: GLOBAL FAULT RUPTURE", seismoX + 16, seismoY - 8);
    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 16px 'JetBrains Mono', monospace";
    ctx.fillText("MAGNITUDE 12.0+", seismoX + seismoW - 160, seismoY - 8);
    ctx.restore();
  }, [frame, rotDeg]);

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <HUDHeader
        badge="TECTONIC FRICTION RESTART"
        title="MAGNITUDE 12+ HYPER-QUAKES"
        alert={true}
        metrics={[
          { label: "MOMENT MAGNITUDE", value: "M12.0+ GLOBAL", alert: true },
          { label: "FAULT CRACKING", value: "RING OF FIRE & MID-ATLANTIC", alert: true },
          { label: "ENERGY RELEASED", value: "100× TOTAL TSUNAMIS" }
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
