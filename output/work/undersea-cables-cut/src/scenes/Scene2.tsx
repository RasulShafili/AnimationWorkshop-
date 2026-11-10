import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { theme } from "../theme";
import { BgMesh } from "../components/BgMesh";
import { HUDHeader } from "../components/HUDHeader";
import { pixelCircle, drawMetallicWire, drawMicroSpark } from "../microPixel";

export const Scene2: React.FC<{ durationInFrames: number }> = ({ durationInFrames }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  const entrance = spring({
    frame,
    fps,
    config: theme.spring.smooth
  });

  const scale = interpolate(entrance, [0, 1], [0.88, 1]);
  const opacity = entrance;
  const floatY = Math.sin(frame * 0.09) * 6;

  // Staggered callout lines
  const c1 = spring({ frame: frame - 8, fps, config: theme.spring.snappy });
  const c2 = spring({ frame: frame - 16, fps, config: theme.spring.snappy });
  const c3 = spring({ frame: frame - 24, fps, config: theme.spring.snappy });
  const c4 = spring({ frame: frame - 32, fps, config: theme.spring.snappy });

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const cx = 270;
    const cy = 420;

    // Outer Polyethylene Jacket (Radius 165px)
    pixelCircle(ctx, cx, cy, 165, "#0f172a", "#334155");
    // Outer rim highlight
    ctx.strokeStyle = "rgba(148, 163, 184, 0.3)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(cx, cy, 163, -Math.PI * 0.8, -Math.PI * 0.2);
    ctx.stroke();

    // Mylar tape layer (Radius 150px)
    pixelCircle(ctx, cx, cy, 150, "#1e293b", "#475569");

    // 24 High-Tensile Galvanized Steel Armor Wires (Radius ring ~136px, wire radius 11px)
    const numWires = 24;
    const wireRingR = 136;
    const wireR = 11;
    for (let i = 0; i < numWires; i++) {
      const angle = (i * 2 * Math.PI) / numWires + frame * 0.003;
      const wx = cx + Math.cos(angle) * wireRingR;
      const wy = cy + Math.sin(angle) * wireRingR;
      drawMetallicWire(ctx, wx, wy, wireR, "#94a3b8", "#f8fafc", "#334155");
    }

    // Aluminum Water-Blocking Barrier (Radius 120px)
    pixelCircle(ctx, cx, cy, 120, "#cbd5e1", "#64748b");

    // Solid Copper Conductor Tube (10,000V DC bus) (Radius 112px to 84px)
    pixelCircle(ctx, cx, cy, 112, "#b45309", "#78350f");
    pixelCircle(ctx, cx, cy, 84, "#1e293b", "#451a03");
    // Burnished copper sheen
    ctx.strokeStyle = "rgba(253, 230, 138, 0.4)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(cx, cy, 106, -Math.PI * 0.75, -Math.PI * 0.25);
    ctx.stroke();

    // Polycarbonate Dielectric Insulator (Radius 84px to 62px)
    pixelCircle(ctx, cx, cy, 84, "#1e293b", "#0f172a");

    // Central Stainless Steel Loose Tube with Hydrophobic Gel (Radius 62px to 0)
    pixelCircle(ctx, cx, cy, 62, "#475569", "#94a3b8");
    // Thixotropic Petroleum Jelly Core (Radius 54px)
    pixelCircle(ctx, cx, cy, 54, "#ca8a04", "#854d0e");

    // 8 Silica Optical Fiber Hair Strands (Radius ring ~28px, fiber radius 5px)
    const numFibers = 8;
    const fiberRingR = 28;
    for (let f = 0; f < numFibers; f++) {
      const fAngle = (f * 2 * Math.PI) / numFibers + frame * -0.01;
      const fx = cx + Math.cos(fAngle) * fiberRingR;
      const fy = cy + Math.sin(fAngle) * fiberRingR;

      // Fiber glass cladding
      pixelCircle(ctx, fx, fy, 6, "#e2e8f0", "#94a3b8");
      // Glowing single-mode laser core
      const coreColor = f % 2 === 0 ? "#22d3ee" : "#ec4899";
      pixelCircle(ctx, fx, fy, 2, "#ffffff", coreColor);
      drawMicroSpark(ctx, fx, fy, 3, coreColor);
    }

    // Central steel strength wire
    drawMetallicWire(ctx, cx, cy, 8, "#cbd5e1", "#ffffff", "#475569");

    // Micro-pixel subtle voltage electricity pulse around copper tube
    if (frame % 4 < 2) {
      const sparkAngle = (frame * 0.15) % (Math.PI * 2);
      const sx = cx + Math.cos(sparkAngle) * 98;
      const sy = cy + Math.sin(sparkAngle) * 98;
      drawMicroSpark(ctx, sx, sy, 5, "#facc15");
    }
  }, [frame]);

  return (
    <AbsoluteFill style={{ backgroundColor: "#020617" }}>
      <BgMesh />

      <HUDHeader
        badge="ENGINEERING SCHEMATIC // 02"
        title="SUBSEA ARMORED CABLE ANATOMY"
        metrics={[
          { label: "CABLE DIAMETER", value: "38 MM (COASTAL) / 17 MM (DEEP)" },
          { label: "ARMOR TENSILE", value: "250,000 N BREAK LOAD" },
          { label: "VOLTAGE BUS", value: "10,000V DC REPEATERS" }
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
          transform: `translateY(${floatY}px) scale(${scale})`,
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

      {/* Micro-Pixel Engineering Callouts */}
      <div
        style={{
          position: "absolute",
          top: "35%",
          left: 40,
          opacity: c1,
          transform: `translateX(${interpolate(c1, [0, 1], [-20, 0])}px)`,
          borderLeft: `3px solid ${theme.colors.heroCyan}`,
          paddingLeft: 14
        }}
      >
        <div style={{ fontFamily: theme.fonts.mono, fontSize: 13, color: theme.colors.heroCyan, letterSpacing: "0.1em" }}>
          LAYER 01 // OUTER ARMOR
        </div>
        <div style={{ fontFamily: theme.fonts.display, fontSize: 20, fontWeight: 800, color: "#ffffff" }}>
          24× GALVANIZED STEEL WIRES
        </div>
        <div style={{ fontFamily: theme.fonts.mono, fontSize: 13, color: "#94a3b8" }}>
          250 kN Breaking Strain • Shark/Trawler Shield
        </div>
      </div>

      <div
        style={{
          position: "absolute",
          top: "43%",
          right: 40,
          textAlign: "right",
          opacity: c2,
          transform: `translateX(${interpolate(c2, [0, 1], [20, 0])}px)`,
          borderRight: `3px solid ${theme.colors.accentGold}`,
          paddingRight: 14
        }}
      >
        <div style={{ fontFamily: theme.fonts.mono, fontSize: 13, color: theme.colors.accentGold, letterSpacing: "0.1em" }}>
          LAYER 02 // POWER CONDUCTOR
        </div>
        <div style={{ fontFamily: theme.fonts.display, fontSize: 20, fontWeight: 800, color: "#ffffff" }}>
          SOLID COPPER TUBE
        </div>
        <div style={{ fontFamily: theme.fonts.mono, fontSize: 13, color: "#94a3b8" }}>
          Carries 10,000V DC • Powers Optical Repeaters
        </div>
      </div>

      <div
        style={{
          position: "absolute",
          top: "57%",
          left: 40,
          opacity: c3,
          transform: `translateX(${interpolate(c3, [0, 1], [-20, 0])}px)`,
          borderLeft: `3px solid ${theme.colors.accentGold}`,
          paddingLeft: 14
        }}
      >
        <div style={{ fontFamily: theme.fonts.mono, fontSize: 13, color: theme.colors.accentGold, letterSpacing: "0.1em" }}>
          LAYER 03 // BARRIER GEL
        </div>
        <div style={{ fontFamily: theme.fonts.display, fontSize: 20, fontWeight: 800, color: "#ffffff" }}>
          THIXOTROPIC PETROLEUM JELLY
        </div>
        <div style={{ fontFamily: theme.fonts.mono, fontSize: 13, color: "#94a3b8" }}>
          Hermetic Water Seal at 600 Atmospheres
        </div>
      </div>

      <div
        style={{
          position: "absolute",
          top: "65%",
          right: 40,
          textAlign: "right",
          opacity: c4,
          transform: `translateX(${interpolate(c4, [0, 1], [20, 0])}px)`,
          borderRight: `3px solid ${theme.colors.heroCyan}`,
          paddingRight: 14
        }}
      >
        <div style={{ fontFamily: theme.fonts.mono, fontSize: 13, color: theme.colors.heroCyan, letterSpacing: "0.1em" }}>
          LAYER 04 // DATA CORE
        </div>
        <div style={{ fontFamily: theme.fonts.display, fontSize: 20, fontWeight: 800, color: "#ffffff" }}>
          8× SILICA OPTICAL FIBERS
        </div>
        <div style={{ fontFamily: theme.fonts.mono, fontSize: 13, color: "#94a3b8" }}>
          Hair-Thin Pure Glass • 250+ Terabits/sec
        </div>
      </div>
    </AbsoluteFill>
  );
};
