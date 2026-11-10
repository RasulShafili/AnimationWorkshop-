import React, { useRef, useEffect } from "react";
import { useCurrentFrame } from "remotion";
import { ART_WIDTH, ART_HEIGHT } from "./pixel";
import { drawCaptions } from "./captions";

export const CaptionOverlay: React.FC = () => {
  const globalFrame = useCurrentFrame();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, ART_WIDTH, ART_HEIGHT);
    drawCaptions(ctx, globalFrame);
  }, [globalFrame]);

  return (
    <canvas
      ref={canvasRef}
      width={ART_WIDTH}
      height={ART_HEIGHT}
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "1080px",
        height: "1920px",
        imageRendering: "pixelated",
        pointerEvents: "none",
        zIndex: 10
      }}
    />
  );
};
