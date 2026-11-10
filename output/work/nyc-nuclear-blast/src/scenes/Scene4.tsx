import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { drawHurricaneFirestorm } from "../nycPixelEngine";
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

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawHurricaneFirestorm(ctx, frame);
  }, [frame]);

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <HUDHeader
        badge="THERMAL INFERNO PHASE"
        title="HURRICANE FIRESTORM"
        alert={true}
        metrics={[
          { label: "INRUSH WIND SPEED", value: "150+ MPH", alert: true },
          { label: "OXYGEN CONCENTRATION", value: "0% (CONSUMED)", alert: true },
          { label: "FIRE AREA", value: "SELF-FEEDING VORTEX" }
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
            background: "rgba(15, 23, 42, 0.94)",
            border: "2px solid #ea580c",
            boxShadow: "0 0 35px rgba(234, 88, 12, 0.45)",
            borderRadius: 16,
            padding: "16px 24px",
            textAlign: "center"
          }}
        >
          <span
            style={{
              fontFamily: theme.fonts.mono,
              fontSize: 14,
              color: "#fb923c",
              letterSpacing: "0.14em",
              textTransform: "uppercase",
              display: "block",
              marginBottom: 4
            }}
          >
            ATMOSPHERIC ASPHYXIATION
          </span>
          <span
            style={{
              fontFamily: theme.fonts.display,
              fontSize: 26,
              fontWeight: 800,
              color: "#ffffff",
              lineHeight: 1.25
            }}
          >
            150 MPH WINDS VACUUM ALL REMAINING OXYGEN
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
