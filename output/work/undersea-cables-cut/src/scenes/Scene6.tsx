import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { theme } from "../theme";
import { BgMesh } from "../components/BgMesh";
import { HUDHeader } from "../components/HUDHeader";
import { pixelRect, pixelCircle } from "../microPixel";

export const Scene6: React.FC<{ durationInFrames: number }> = ({ durationInFrames }) => {
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

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const w = canvas.width;
    const cy = 410;

    // Panel 1: Wall Street Stock Exchange Freeze (Left: x = 20 to 175)
    const p1X = 25;
    const p1Y = cy - 130;
    const p1W = 150;
    const p1H = 260;
    pixelRect(ctx, p1X, p1Y, p1W, p1H, "#090d16", "#ef4444");
    pixelRect(ctx, p1X, p1Y, p1W, 22, "#7f1d1d");
    ctx.font = "bold 9px monospace";
    ctx.fillStyle = "#ffffff";
    ctx.fillText("NASDAQ / SWIFT", p1X + 8, p1Y + 15);

    // Falling stock indices in red
    const stocks = [
      { name: "S&P 500", val: "-14.8%", down: true },
      { name: "SWIFT", val: "FROZEN", down: true },
      { name: "BTC/USD", val: "OFFLINE", down: true },
      { name: "FOREX", val: "HALTED", down: true },
      { name: "OIL / WTI", val: "-18.2%", down: true }
    ];
    stocks.forEach((s, idx) => {
      const sy = p1Y + 40 + idx * 40;
      ctx.fillStyle = "#94a3b8";
      ctx.font = "bold 10px monospace";
      ctx.fillText(s.name, p1X + 10, sy);
      ctx.fillStyle = "#ef4444";
      ctx.fillText(`▼ ${s.val}`, p1X + 10, sy + 16);
      pixelRect(ctx, p1X + 10, sy + 22, p1W - 20, 1, "rgba(239, 68, 68, 0.2)");
    });

    // Panel 2: Cloud Datacenter Server Racks (Center: x = 195 to 345)
    const p2X = 195;
    const p2Y = cy - 130;
    const p2W = 150;
    const p2H = 260;
    pixelRect(ctx, p2X, p2Y, p2W, p2H, "#090d16", "#f59e0b");
    pixelRect(ctx, p2X, p2Y, p2W, 22, "#78350f");
    ctx.fillStyle = "#ffffff";
    ctx.fillText("AWS / CLOUD RACKS", p2X + 8, p2Y + 15);

    // Datacenter Rack Units with blinking fault LEDs
    for (let u = 0; u < 7; u++) {
      const uy = p2Y + 34 + u * 31;
      pixelRect(ctx, p2X + 8, uy, p2W - 16, 26, "#1e293b", "#334155");
      // Status LEDs: green shifting to blinking red/amber
      for (let led = 0; led < 6; led++) {
        const lx = p2X + 16 + led * 18;
        const ly = uy + 13;
        const isBlinkingRed = (frame + led + u) % 4 < 2;
        pixelCircle(ctx, lx, ly, 3, isBlinkingRed ? "#ef4444" : "#451a03");
      }
    }

    // Panel 3: Smartphone "No Internet" (Right: x = 365 to 515)
    const p3X = 365;
    const p3Y = cy - 130;
    const p3W = 150;
    const p3H = 260;
    // Phone chassis
    pixelRect(ctx, p3X, p3Y, p3W, p3H, "#0f172a", "#38bdf8");
    // Phone screen
    pixelRect(ctx, p3X + 8, p3Y + 14, p3W - 16, p3H - 28, "#020617");
    // Phone camera notch
    pixelRect(ctx, p3X + p3W / 2 - 16, p3Y + 16, 32, 6, "#1e293b");

    // No signal icon on phone screen
    const phoneMidX = p3X + p3W / 2;
    ctx.strokeStyle = "#ef4444";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.arc(phoneMidX, p3Y + 80, 22, 0, Math.PI * 2);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(phoneMidX - 15, p3Y + 65);
    ctx.lineTo(phoneMidX + 15, p3Y + 95);
    ctx.stroke();

    ctx.font = "bold 10px monospace";
    ctx.fillStyle = "#f87171";
    ctx.textAlign = "center";
    ctx.fillText("NO INTERNET", phoneMidX, p3Y + 125);
    ctx.font = "9px monospace";
    ctx.fillStyle = "#94a3b8";
    ctx.fillText("SAT OVERLOAD", phoneMidX, p3Y + 145);
    ctx.fillText("< 1% SATELLITE", phoneMidX, p3Y + 162);
    ctx.fillText("CAPACITY FAILED", phoneMidX, p3Y + 178);
    ctx.textAlign = "left";
  }, [frame]);

  return (
    <AbsoluteFill style={{ backgroundColor: "#020617" }}>
      <BgMesh />

      <HUDHeader
        badge="CIVILIZATION SHOCKWAVE // 06"
        title="GLOBAL FINANCIAL & CLOUD COLLAPSE"
        metrics={[
          { label: "FINANCIAL SYSTEM", value: "$10 TRILLION AT RISK" },
          { label: "SATELLITE FALLBACK", value: "OVERLOADED (<1%)" },
          { label: "DATACENTERS", value: "MULTI-REGION OUTAGE" }
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

      {/* Warning Callout Box */}
      <div
        style={{
          position: "absolute",
          top: "66%",
          left: 40,
          right: 40,
          background: "rgba(15, 23, 42, 0.92)",
          border: `1.5px solid ${theme.colors.accentGold}`,
          boxShadow: `0 0 25px ${theme.colors.accentGoldGlow}`,
          borderRadius: 14,
          padding: "16px 24px",
          textAlign: "center"
        }}
      >
        <div style={{ fontFamily: theme.fonts.display, fontSize: 20, fontWeight: 800, color: theme.colors.accentGold }}>
          SATELLITES CANNOT REPLACE SUBSEA FIBER
        </div>
        <div style={{ fontFamily: theme.fonts.mono, fontSize: 14, color: "#e2e8f0", marginTop: 4 }}>
          All global communications satellites combined handle less than 1% of international internet bandwidth.
        </div>
      </div>
    </AbsoluteFill>
  );
};
