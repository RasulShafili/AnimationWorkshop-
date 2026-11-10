import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { theme } from "../theme";
import { BgMesh } from "../components/BgMesh";
import { HUDHeader } from "../components/HUDHeader";
import { pixelRect, pixelCircle, drawMicroSpark } from "../microPixel";

export const Scene5: React.FC<{ durationInFrames: number }> = ({ durationInFrames }) => {
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

  // Latency spike: jump from 24ms to 999ms
  const latency = Math.floor(
    interpolate(frame, [10, 45], [24, 999], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp"
    })
  );

  // Bandwidth plunge: drop from 100% to 18%
  const bandwidth = Math.floor(
    interpolate(frame, [10, 45], [100, 18], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp"
    })
  );

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const w = canvas.width;
    const h = canvas.height;

    // Mission Control NOC Panoramic Monitor (y = 280, height = 240)
    const monY = 280;
    const monH = 240;
    pixelRect(ctx, 30, monY, w - 60, monH, "#090d16", "#ef4444");

    // Monitor Header
    pixelRect(ctx, 30, monY, w - 60, 24, "#7f1d1d");
    ctx.font = "bold 11px monospace";
    ctx.fillStyle = "#fecaca";
    ctx.fillText("NOC GLOBAL TELEMETRY // SEVER ALERT ACTIVE", 42, monY + 16);

    // World map outline on monitor (simplified micro-pixel grid)
    ctx.strokeStyle = "rgba(239, 68, 68, 0.25)";
    ctx.lineWidth = 1;
    for (let gx = 50; gx < w - 60; gx += 30) {
      ctx.beginPath();
      ctx.moveTo(gx, monY + 28);
      ctx.lineTo(gx, monY + monH - 10);
      ctx.stroke();
    }
    for (let gy = monY + 40; gy < monY + monH; gy += 25) {
      ctx.beginPath();
      ctx.moveTo(40, gy);
      ctx.lineTo(w - 70, gy);
      ctx.stroke();
    }

    // Red Sever Alarm Beacons on Map (Suez/Red Sea: x = 290, y = monY + 90)
    const cutX = 290;
    const cutY = monY + 95;
    const pulse = (Math.sin(frame * 0.3) + 1) * 0.5;

    ctx.strokeStyle = `rgba(239, 68, 68, ${0.9 - pulse * 0.5})`;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(cutX, cutY, 10 + pulse * 18, 0, Math.PI * 2);
    ctx.stroke();

    drawMicroSpark(ctx, cutX, cutY, 7, "#ef4444");
    drawMicroSpark(ctx, cutX, cutY, 3, "#ffffff");

    // Telemetry Graph 1: Latency Curve (Skyrocketing in red)
    const graph1X = 50;
    const graph1Y = monY + 130;
    const graph1W = 200;
    const graph1H = 80;
    pixelRect(ctx, graph1X, graph1Y, graph1W, graph1H, "#030712", "#374151");

    ctx.strokeStyle = "#ef4444";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(graph1X + 10, graph1Y + graph1H - 15);
    ctx.lineTo(graph1X + 70, graph1Y + graph1H - 18);
    ctx.lineTo(graph1X + 110, graph1Y + 15); // Sudden spike!
    ctx.lineTo(graph1X + graph1W - 10, graph1Y + 15);
    ctx.stroke();

    ctx.font = "bold 10px monospace";
    ctx.fillStyle = "#f87171";
    ctx.fillText("PING: " + latency + " ms [FATAL]", graph1X + 10, graph1Y + 22);

    // Telemetry Graph 2: Bandwidth Throughput (Plunging down)
    const graph2X = 280;
    const graph2Y = monY + 130;
    const graph2W = 210;
    const graph2H = 80;
    pixelRect(ctx, graph2X, graph2Y, graph2W, graph2H, "#030712", "#374151");

    ctx.strokeStyle = "#f59e0b";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(graph2X + 10, graph2Y + 20);
    ctx.lineTo(graph2X + 70, graph2Y + 22);
    ctx.lineTo(graph2X + 110, graph2Y + graph2H - 15); // Sudden plunge!
    ctx.lineTo(graph2X + graph2W - 10, graph2Y + graph2H - 15);
    ctx.stroke();

    ctx.font = "bold 10px monospace";
    ctx.fillStyle = "#fbbf24";
    ctx.fillText("THROUGHPUT: " + bandwidth + "%", graph2X + 10, graph2Y + 22);

    // Operator Desk Console & Silhouettes at bottom (y = 540 to 620)
    pixelRect(ctx, 40, 540, w - 80, 50, "#1e293b", "#334155");
    // Operator keyboard & control screens
    for (let c = 0; c < 3; c++) {
      const cx = 90 + c * 140;
      pixelRect(ctx, cx, 515, 70, 35, "#0f172a", "#38bdf8");
      // Console lines
      for (let l = 0; l < 4; l++) {
        pixelRect(ctx, cx + 8, 522 + l * 6, 54, 2, l % 2 === 0 ? "#38bdf8" : "#94a3b8");
      }
      // Operator head & shoulders silhouette
      pixelCircle(ctx, cx + 35, 575, 14, "#020617");
      pixelRect(ctx, cx + 18, 590, 34, 25, "#020617");
    }

    // Emergency Flashing Red Room Ambient Sweep
    const roomAlert = (Math.sin(frame * 0.4) + 1) * 0.5;
    ctx.fillStyle = `rgba(239, 68, 68, ${roomAlert * 0.12})`;
    ctx.fillRect(0, 0, w, h);
  }, [frame, latency, bandwidth]);

  return (
    <AbsoluteFill style={{ backgroundColor: "#020617" }}>
      <BgMesh />

      <HUDHeader
        badge="NOC EMERGENCY // 05"
        title="GLOBAL TELEMETRY CRASH"
        metrics={[
          { label: "PACKET LOSS", value: "82% ACROSS CONTINENTS" },
          { label: "LATENCY PEAK", value: `${latency} MS` },
          { label: "BGP ANOMALIES", value: "14,800 ROUTE COLLAPSES" }
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

      {/* Live Terminal Log Stream */}
      <div
        style={{
          position: "absolute",
          top: "66%",
          left: 40,
          right: 40,
          background: "rgba(15, 23, 42, 0.94)",
          border: "1.5px solid #ef4444",
          boxShadow: "0 0 25px rgba(239, 68, 68, 0.4)",
          borderRadius: 14,
          padding: "16px 24px",
          fontFamily: theme.fonts.mono
        }}
      >
        <div style={{ fontSize: 13, color: "#f87171", fontWeight: 700, marginBottom: 6 }}>
          [BGP_ROUTER_CORE_01] FATAL: AS-PATH WITHDRAWAL // 14 COUNTRIES UNREACHABLE
        </div>
        <div style={{ fontSize: 13, color: "#ffffff" }}>
          ► RED SEA SEA-ME-WE-5 DOWN // TRANSATLANTIC TAT-14 OVERLOAD (142% CAPACITY)
        </div>
        <div style={{ fontSize: 13, color: theme.colors.accentGold, marginTop: 4 }}>
          ► ESTIMATED ECONOMIC IMPACT: $10,000,000,000 PER HOUR
        </div>
      </div>
    </AbsoluteFill>
  );
};
