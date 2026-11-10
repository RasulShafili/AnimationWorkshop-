import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { renderEarthCoreSlice } from "../pixelGlobe";
import { HUDHeader } from "../components/HUDHeader";
import { theme } from "../theme";

export const Scene5: React.FC = () => {
  const frame = useCurrentFrame();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Sloshing offset driven by planetary inertia
  const sloshOffset = 18 + Math.sin(frame * 0.18) * 8;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    renderEarthCoreSlice(ctx, 270, 480, 190, frame, sloshOffset);
  }, [frame, sloshOffset]);

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <HUDHeader
        badge="GEODYNAMO COLLAPSE"
        title="MOLTEN CORE SLOSH & RADIATION"
        alert={true}
        metrics={[
          { label: "CORE SLIP VELOCITY", value: "400+ M/S", alert: true },
          { label: "MAGNETOSPHERE", value: "COLLAPSED (0%)", alert: true },
          { label: "SOLAR WIND IMPACT", value: "UNFILTERED LETHAL" }
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

      {/* Geophysics Callout */}
      <div
        style={{
          position: "absolute",
          top: 350,
          left: 60,
          right: 60,
          display: "flex",
          justifyContent: "center",
          zIndex: 30
        }}
      >
        <div
          style={{
            background: "rgba(15, 23, 42, 0.92)",
            border: "2px solid #facc15",
            boxShadow: "0 0 25px rgba(250, 204, 21, 0.35)",
            borderRadius: 16,
            padding: "16px 24px",
            textAlign: "center"
          }}
        >
          <span
            style={{
              fontFamily: theme.fonts.mono,
              fontSize: 14,
              color: "#fde047",
              letterSpacing: "0.14em",
              textTransform: "uppercase",
              display: "block",
              marginBottom: 4
            }}
          >
            MAGNETIC SHIELD DESTABILIZATION
          </span>
          <span
            style={{
              fontFamily: theme.fonts.display,
              fontSize: 24,
              fontWeight: 800,
              color: "#ffffff",
              lineHeight: 1.25
            }}
          >
            LIQUID IRON CORE SLOSHES OUT OF SYNC
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
