import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { drawSubwayCrossSection } from "../nycPixelEngine";
import { HUDHeader } from "../components/HUDHeader";
import { theme } from "../theme";

export const Scene5: React.FC = () => {
  const frame = useCurrentFrame();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawSubwayCrossSection(ctx, frame);
  }, [frame]);

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <HUDHeader
        badge="GEOLOGICAL SURVIVAL ANALYSIS"
        title="SUBWAY BEDROCK SHIELDING"
        alert={false}
        metrics={[
          { label: "BEDROCK DEPTH", value: "30 METERS (SCHIST)" },
          { label: "RADIATION SHIELD", value: "99.9% ATTENUATION" },
          { label: "VENTILATION THREAT", value: "SMOKE & CO SUFFOCATION", alert: true }
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
