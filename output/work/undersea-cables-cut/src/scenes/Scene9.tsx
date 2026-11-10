import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { theme } from "../theme";
import { BgMesh } from "../components/BgMesh";
import { HUDHeader } from "../components/HUDHeader";
import { pixelRect, pixelCircle, drawMicroSpark } from "../microPixel";

export const Scene9: React.FC<{ durationInFrames: number }> = ({ durationInFrames }) => {
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

    const cx = 270;
    const cy = 410;

    // Glowing Cyber Radar Rings
    const pulse1 = (frame * 0.04) % 1;
    const pulse2 = (frame * 0.04 + 0.5) % 1;

    ctx.strokeStyle = `rgba(34, 211, 238, ${0.7 - pulse1 * 0.6})`;
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.arc(cx, cy, 70 + pulse1 * 75, 0, Math.PI * 2);
    ctx.stroke();

    ctx.strokeStyle = `rgba(245, 158, 11, ${0.7 - pulse2 * 0.6})`;
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.arc(cx, cy, 70 + pulse2 * 75, 0, Math.PI * 2);
    ctx.stroke();

    // Central Hexagonal Cyber Shield
    ctx.fillStyle = "#090d16";
    ctx.strokeStyle = theme.colors.heroCyan;
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    for (let i = 0; i < 6; i++) {
      const angle = (i * Math.PI) / 3 - Math.PI / 6;
      const hx = cx + Math.cos(angle) * 72;
      const hy = cy + Math.sin(angle) * 72;
      if (i === 0) ctx.moveTo(hx, hy);
      else ctx.lineTo(hx, hy);
    }
    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    // Inner Glowing Fiber Optic Loop
    ctx.strokeStyle = "#38bdf8";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(cx, cy, 45, 0, Math.PI * 2);
    ctx.stroke();

    // Earth icon inside shield
    pixelCircle(ctx, cx, cy, 28, "#0284c7", "#38bdf8");
    // Miniature continent pixel shapes
    pixelRect(ctx, cx - 18, cy - 14, 12, 10, "#16a34a");
    pixelRect(ctx, cx + 4, cy - 10, 16, 12, "#16a34a");
    pixelRect(ctx, cx - 10, cy + 4, 10, 14, "#16a34a");

    // Orbiting photon dots around the badge
    for (let d = 0; d < 4; d++) {
      const dotAngle = (frame * 0.05 + (d * Math.PI) / 2);
      const dx = cx + Math.cos(dotAngle) * 45;
      const dy = cy + Math.sin(dotAngle) * 45;
      drawMicroSpark(ctx, dx, dy, 4, "#facc15");
    }
  }, [frame]);

  return (
    <AbsoluteFill style={{ backgroundColor: "#020617" }}>
      <BgMesh />

      <HUDHeader
        badge="GLOBAL REALITY // 09"
        title="THE FRAGILE THREADS OF HUMANITY"
        metrics={[
          { label: "SUBSEA CABLES", value: "550 ACTIVE SYSTEMS" },
          { label: "TOTAL LENGTH", value: "1,400,000 KILOMETERS" },
          { label: "PROTECTION", value: "SURVEILLANCE & REPAIR FLEETS" }
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

      {/* Interactive Outro Prompt Box */}
      <div
        style={{
          position: "absolute",
          top: "64%",
          left: 40,
          right: 40,
          background: "rgba(15, 23, 42, 0.94)",
          border: `2px solid ${theme.colors.accentGold}`,
          boxShadow: `0 0 35px ${theme.colors.accentGoldGlow}`,
          borderRadius: 18,
          padding: "24px 28px",
          textAlign: "center"
        }}
      >
        <div style={{ fontFamily: theme.fonts.display, fontSize: 24, fontWeight: 900, color: theme.colors.accentGold, letterSpacing: "0.04em" }}>
          COULD THE GLOBAL INTERNET EVER SHUT DOWN?
        </div>
        <div style={{ fontFamily: theme.fonts.display, fontSize: 18, fontWeight: 600, color: "#ffffff", marginTop: 8 }}>
          Drop your thoughts in the comments! 👇
        </div>
        <div style={{ display: "flex", justifyContent: "center", gap: 12, marginTop: 14 }}>
          <span style={{ background: "rgba(34, 211, 238, 0.15)", border: "1px solid #22d3ee", padding: "6px 14px", borderRadius: 8, fontSize: 13, color: "#22d3ee", fontFamily: theme.fonts.mono }}>
            #internetcable
          </span>
          <span style={{ background: "rgba(34, 211, 238, 0.15)", border: "1px solid #22d3ee", padding: "6px 14px", borderRadius: 8, fontSize: 13, color: "#22d3ee", fontFamily: theme.fonts.mono }}>
            #technology
          </span>
          <span style={{ background: "rgba(34, 211, 238, 0.15)", border: "1px solid #22d3ee", padding: "6px 14px", borderRadius: 8, fontSize: 13, color: "#22d3ee", fontFamily: theme.fonts.mono }}>
            #cybersecurity
          </span>
          <span style={{ background: "rgba(34, 211, 238, 0.15)", border: "1px solid #22d3ee", padding: "6px 14px", borderRadius: 8, fontSize: 13, color: "#22d3ee", fontFamily: theme.fonts.mono }}>
            #deepsea
          </span>
          <span style={{ background: "rgba(34, 211, 238, 0.15)", border: "1px solid #22d3ee", padding: "6px 14px", borderRadius: 8, fontSize: 13, color: "#22d3ee", fontFamily: theme.fonts.mono }}>
            #science
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
