import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { theme } from "../theme";
import { BgMesh } from "../components/BgMesh";
import { HUDHeader } from "../components/HUDHeader";
import { pixelRect, pixelCircle, drawMicroSpark } from "../microPixel";

export const Scene7: React.FC<{ durationInFrames: number }> = ({ durationInFrames }) => {
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
    const h = canvas.height;

    // Top Section: Surface Cable Repair Ship (y = 230 to 330)
    const seaLevelY = 280;
    // Stormy ocean waves at surface
    ctx.strokeStyle = "rgba(56, 189, 248, 0.4)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    for (let x = 0; x < w; x += 4) {
      const wy = seaLevelY + Math.sin(x * 0.04 + frame * 0.1) * 5;
      if (x === 0) ctx.moveTo(x, wy);
      else ctx.lineTo(x, wy);
    }
    ctx.stroke();

    // 140m Specialized Cable Repair Ship (C.S. Reliance)
    const shipX = 170 + Math.sin(frame * 0.04) * 6;
    const shipY = seaLevelY - 26 + Math.cos(frame * 0.05) * 3;
    // Hull (Dark Blue / White superstructure)
    ctx.fillStyle = "#1e293b";
    ctx.beginPath();
    ctx.moveTo(shipX - 90, shipY + 12);
    ctx.lineTo(shipX + 110, shipY + 12);
    ctx.lineTo(shipX + 85, shipY + 28);
    ctx.lineTo(shipX - 75, shipY + 28);
    ctx.closePath();
    ctx.fill();
    ctx.strokeStyle = "#475569";
    ctx.lineWidth = 1;
    ctx.stroke();

    // Red water line
    pixelRect(ctx, shipX - 75, shipY + 26, 160, 2, "#ef4444");

    // Superstructure & Bridge
    pixelRect(ctx, shipX - 50, shipY - 14, 55, 26, "#f8fafc", "#cbd5e1");
    // Bridge windows
    pixelRect(ctx, shipX - 45, shipY - 8, 45, 6, "#0284c7");
    // Stern Cable Gantry & Crane
    ctx.strokeStyle = "#eab308";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(shipX + 75, shipY + 12);
    ctx.lineTo(shipX + 85, shipY - 18);
    ctx.lineTo(shipX + 95, shipY + 12);
    ctx.stroke();

    // Umbilical Tether cable dropping from ship to ROV in deep abyss
    ctx.strokeStyle = "rgba(234, 179, 8, 0.5)";
    ctx.lineWidth = 2;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(shipX + 85, shipY - 18);
    ctx.bezierCurveTo(shipX + 120, 360, 310, 380, 290, 420);
    ctx.stroke();
    ctx.setLineDash([]);

    // Bottom Section: Heavy Work-Class ROV Submarine at 4,000m depth
    const rovX = 270 + Math.sin(frame * 0.05) * 8;
    const rovY = 460 + Math.cos(frame * 0.06) * 5;

    // Dual LED Volumetric Floodlight Beams cutting through abyssal dark
    const leftBeamGrad = ctx.createRadialGradient(rovX - 35, rovY + 10, 4, rovX - 70, rovY + 110, 100);
    leftBeamGrad.addColorStop(0, "rgba(56, 189, 248, 0.45)");
    leftBeamGrad.addColorStop(1, "rgba(56, 189, 248, 0)");
    ctx.fillStyle = leftBeamGrad;
    ctx.beginPath();
    ctx.moveTo(rovX - 35, rovY + 10);
    ctx.lineTo(rovX - 110, rovY + 130);
    ctx.lineTo(rovX - 20, rovY + 130);
    ctx.closePath();
    ctx.fill();

    const rightBeamGrad = ctx.createRadialGradient(rovX + 35, rovY + 10, 4, rovX + 70, rovY + 110, 100);
    rightBeamGrad.addColorStop(0, "rgba(56, 189, 248, 0.45)");
    rightBeamGrad.addColorStop(1, "rgba(56, 189, 248, 0)");
    ctx.fillStyle = rightBeamGrad;
    ctx.beginPath();
    ctx.moveTo(rovX + 35, rovY + 10);
    ctx.lineTo(rovX + 20, rovY + 130);
    ctx.lineTo(rovX + 110, rovY + 130);
    ctx.closePath();
    ctx.fill();

    // Heavy Industrial ROV Chassis (Yellow Syntactic Foam)
    const rw = 110;
    const rh = 65;
    pixelRect(ctx, rovX - rw / 2, rovY - rh / 2, rw, rh, "#eab308", "#ca8a04");
    // ROV Frame & Hardware Ribs
    pixelRect(ctx, rovX - rw / 2 + 6, rovY - rh / 2 + 6, rw - 12, rh - 12, "#1e293b", "#475569");
    // Electronics Canisters & Cameras
    pixelCircle(ctx, rovX, rovY, 14, "#0f172a", "#38bdf8");
    pixelCircle(ctx, rovX, rovY, 5, "#22d3ee");

    // Dual Thrusters on sides
    pixelRect(ctx, rovX - rw / 2 - 14, rovY - 14, 14, 28, "#334155", "#64748b");
    pixelRect(ctx, rovX + rw / 2, rovY - 14, 14, 28, "#334155", "#64748b");

    // Dual LED Headlamps
    pixelCircle(ctx, rovX - 35, rovY + 10, 7, "#f8fafc", "#38bdf8");
    pixelCircle(ctx, rovX + 35, rovY + 10, 7, "#f8fafc", "#38bdf8");

    // Articulated Hydraulic Manipulator Arm holding the severed cable
    const armX = rovX - 25;
    const armY = rovY + rh / 2;
    ctx.strokeStyle = "#cbd5e1";
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(armX, armY);
    ctx.lineTo(armX - 20, armY + 28);
    ctx.lineTo(armX + 10, armY + 54);
    ctx.stroke();

    // Titanium Claw Gripper clamped onto subsea cable
    const clawX = armX + 10;
    const clawY = armY + 54;
    pixelCircle(ctx, clawX, clawY, 6, "#64748b", "#f8fafc");

    // Subsea Cable retrieved and held by claw
    ctx.strokeStyle = "#1e293b";
    ctx.lineWidth = 8;
    ctx.beginPath();
    ctx.moveTo(clawX - 80, clawY + 25);
    ctx.quadraticCurveTo(clawX, clawY, clawX + 60, clawY + 10);
    ctx.stroke();
    ctx.strokeStyle = "#d97706";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(clawX - 80, clawY + 25);
    ctx.quadraticCurveTo(clawX, clawY, clawX + 60, clawY + 10);
    ctx.stroke();

    // Floating marine snow sediment particles
    for (let p = 0; p < 18; p++) {
      const px = ((frame * 0.4 + p * 31) % w);
      const py = 340 + ((frame * 0.3 + p * 19) % 220);
      pixelCircle(ctx, px, py, 1.5, "rgba(226, 232, 240, 0.4)");
    }
  }, [frame]);

  return (
    <AbsoluteFill style={{ backgroundColor: "#020617" }}>
      <BgMesh />

      <HUDHeader
        badge="DEEP-SEA SALVAGE // 07"
        title="HEAVY WORK-CLASS ROV AT 4,000M"
        metrics={[
          { label: "ROV DEPTH", value: "4,180 METERS" },
          { label: "HYDRAULIC PRESSURE", value: "420 BAR" },
          { label: "POSITIONING SYSTEM", value: "DP2 GPS DYNAMIC LOCK" }
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

      {/* Technical Spec Box */}
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
          AUTONOMOUS ROBOTIC CABLE RECOVERY
        </div>
        <div style={{ fontFamily: theme.fonts.mono, fontSize: 14, color: "#e2e8f0", marginTop: 4 }}>
          Heavy ROV locates the severed cable in total darkness, attaches an acoustic beacon, and brings the fiber ends to the surface ship for cleanroom micro-splicing.
        </div>
      </div>
    </AbsoluteFill>
  );
};
