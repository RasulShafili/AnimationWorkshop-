import React, { useRef, useEffect } from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { drawFalloutMap } from "../nycPixelEngine";
import { HUDHeader } from "../components/HUDHeader";
import { theme } from "../theme";

export const Scene7: React.FC = () => {
  const frame = useCurrentFrame();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawFalloutMap(ctx, frame);
  }, [frame]);

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <HUDHeader
        badge="RADIOLOGICAL HAZARD"
        title="EASTWARD FALLOUT PLUME"
        alert={true}
        metrics={[
          { label: "LETHAL DOSE (>1000R)", value: "LONG ISLAND & QUEENS", alert: true },
          { label: "WIND DIRECTION", value: "45 KM/H EAST-NORTHEAST" },
          { label: "FATALITY HORIZON", value: "HOURS TO DAYS" }
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
