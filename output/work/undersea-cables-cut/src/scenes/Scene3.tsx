import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { theme } from "../theme";
import { BgMesh } from "../components/BgMesh";
import { HUDHeader } from "../components/HUDHeader";
import { pixelRect, drawMicroSpark } from "../microPixel";

export const Scene3: React.FC<{ durationInFrames: number }> = ({ durationInFrames }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  const entrance = spring({
    frame,
    fps,
    config: theme.spring.smooth
  });

  const scale = interpolate(entrance, [0, 1], [0.9, 1]);
  const opacity = entrance;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const cx = 270;
    const cy = 430;

    // Outer Glass Cladding (125 Microns) - Longitudinal channel
    // Cladding Top & Bottom blocks
    pixelRect(ctx, 30, cy - 140, 480, 70, "#0f172a", "#1e293b");
    pixelRect(ctx, 30, cy + 70, 480, 70, "#0f172a", "#1e293b");

    // Cladding grid texture (subtle micro-pixel lattice)
    for (let x = 30; x < 510; x += 16) {
      ctx.strokeStyle = "rgba(56, 189, 248, 0.08)";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(x, cy - 140);
      ctx.lineTo(x, cy - 70);
      ctx.moveTo(x, cy + 70);
      ctx.lineTo(x, cy + 140);
      ctx.stroke();
    }

    // Boundary interface lines (Critical Angle Total Reflection Boundary)
    ctx.strokeStyle = "rgba(34, 211, 238, 0.7)";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(30, cy - 70);
    ctx.lineTo(510, cy - 70);
    ctx.moveTo(30, cy + 70);
    ctx.lineTo(510, cy + 70);
    ctx.stroke();

    // Core glass medium (9 Microns Single-Mode Core)
    pixelRect(ctx, 30, cy - 70, 480, 140, "#082f49");

    // Total Internal Reflection - Laser Beam 1 (Electric Cyan)
    const bouncePeriod = 90;
    const offset1 = (frame * 3.5) % bouncePeriod;
    ctx.strokeStyle = "#22d3ee";
    ctx.lineWidth = 3;
    ctx.shadowColor = "rgba(34, 211, 238, 0.8)";
    ctx.shadowBlur = 10;
    ctx.beginPath();
    for (let x = 30; x <= 510; x += 2) {
      const phase = (x + offset1) / bouncePeriod;
      const triangleWave = Math.abs((phase % 2) - 1) * 2 - 1; // -1 to 1
      const y = cy + triangleWave * 60;
      if (x === 30) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Laser Beam 2 (WDM Frequency 2 - Fluorescent Magenta)
    const offset2 = (frame * 3.2 + 45) % bouncePeriod;
    ctx.strokeStyle = "#ec4899";
    ctx.lineWidth = 2.5;
    ctx.shadowColor = "rgba(236, 72, 153, 0.8)";
    ctx.shadowBlur = 8;
    ctx.beginPath();
    for (let x = 30; x <= 510; x += 2) {
      const phase = (x + offset2) / bouncePeriod;
      const triangleWave = Math.abs((phase % 2) - 1) * 2 - 1;
      const y = cy - triangleWave * 56;
      if (x === 30) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    ctx.shadowBlur = 0;

    // Traveling Binary Photon Packets along Core
    const bits = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1];
    ctx.font = "bold 14px monospace";
    for (let i = 0; i < bits.length; i++) {
      const bitX = ((frame * 4 + i * 42) % 460) + 36;
      const bitY = cy - 4;
      ctx.fillStyle = bits[i] === 1 ? "#facc15" : "#67e8f9";
      ctx.fillText(`${bits[i]}`, bitX, bitY);

      // Micro-spark above 1s
      if (bits[i] === 1 && (frame + i) % 3 === 0) {
        drawMicroSpark(ctx, bitX + 4, bitY - 8, 3, "#fef08a");
      }
    }

    // Critical reflection contact point sparks
    for (let x = 30; x <= 510; x += bouncePeriod) {
      const hitX1 = (x - offset1 + bouncePeriod * 10) % 480 + 30;
      drawMicroSpark(ctx, hitX1, cy - 68, 4, "#22d3ee");
      drawMicroSpark(ctx, (hitX1 + bouncePeriod * 0.5) % 480 + 30, cy + 68, 4, "#22d3ee");
    }
  }, [frame]);

  return (
    <AbsoluteFill style={{ backgroundColor: "#020617" }}>
      <BgMesh />

      <HUDHeader
        badge="NANOSCALE TRANSMISSION // 03"
        title="TOTAL INTERNAL REFLECTION & SPEED"
        metrics={[
          { label: "SPEED IN GLASS", value: "204,000 KM/S (2/3 C)" },
          { label: "WDM CHANNELS", value: "96 WAVELENGTHS" },
          { label: "TRANSIT NYC-LON", value: "32 MILLISECONDS" }
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

      {/* High-Frequency Live Financial & Data Ticker */}
      <div
        style={{
          position: "absolute",
          top: "65%",
          left: 40,
          right: 40,
          background: "rgba(15, 23, 42, 0.92)",
          border: `1.5px solid ${theme.colors.heroCyan}`,
          boxShadow: `0 0 25px ${theme.colors.heroCyanGlow}`,
          borderRadius: 14,
          padding: "16px 24px"
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
          <span style={{ fontFamily: theme.fonts.mono, fontSize: 13, color: theme.colors.accentGold, fontWeight: 700 }}>
            LIVE TRANSOCEANIC DATASTREAM // LATENCY: 31.8 ms
          </span>
          <span style={{ fontFamily: theme.fonts.mono, fontSize: 13, color: theme.colors.heroCyan }}>
            DWDM: 48.2 Tbps
          </span>
        </div>
        <div style={{ fontFamily: theme.fonts.mono, fontSize: 16, color: "#ffffff", letterSpacing: "0.04em" }}>
          ► SWIFT WIRE: $420,000,000 [NYC → LON / VERIFIED]
        </div>
        <div style={{ fontFamily: theme.fonts.mono, fontSize: 14, color: "#94a3b8", marginTop: 4 }}>
          ► NYSE / LSE HIGH-FREQUENCY ARBITRAGE EXECUTED IN 0.0014 SEC
        </div>
      </div>
    </AbsoluteFill>
  );
};
