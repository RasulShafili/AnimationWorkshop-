import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { drawMushroomCloud } from "../nycPixelEngine";
import { HUDHeader } from "../components/HUDHeader";
import { theme } from "../theme";

export const Scene6: React.FC = () => {
  const frame = useCurrentFrame();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawMushroomCloud(ctx, frame);
  }, [frame]);

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <HUDHeader
        badge="ATMOSPHERIC CONVECTION"
        title="20-KM MUSHROOM CLOUD"
        alert={true}
        metrics={[
          { label: "CLOUD ALTITUDE", value: "20 KM (STRATOSPHERE)", alert: true },
          { label: "RADIOACTIVE DEBRIS", value: "MILLIONS OF TONS" },
          { label: "ELECTROSTATIC STATE", value: "LIGHTNING IN PLUME" }
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
