import React, { useRef, useEffect } from "react";
import { useCurrentFrame } from "remotion";
import {
  drawJointRoom,
  drawBone,
  drawSynovialCapsule,
  rect
} from "../pixelEngine";

export const Scene1: React.FC<{ startFrame: number; endFrame: number; globalFrame: number }> = ({ startFrame, globalFrame }) => {
  const frame = useCurrentFrame();
  const localFrame = frame;
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Room background
    drawJointRoom(ctx, 270, 480, localFrame);

    // Two finger bones resting peacefully together in the joint
    const cy = 250;
    const cx = 135;
    const gap = 14 + Math.sin(localFrame * 0.1) * 2;

    drawSynovialCapsule(ctx, cx, cy, gap, false, 0, 0, localFrame);
    drawBone(ctx, cx, cy - 10, true, 26, "happy", localFrame);
    drawBone(ctx, cx, cy + 10, false, 26, "normal", localFrame);

    // "NO BONE GRINDING" red prohibition badge
    if (localFrame > 40) {
      rect(ctx, 45, 120, 180, 36, "rgba(14, 13, 24, 0.95)");
      rect(ctx, 47, 122, 176, 32, "#c0392b");
      ctx.fillStyle = "#ffffff";
      ctx.font = "8px 'Press Start 2P', monospace";
      ctx.fillText("NOT BONES GRINDING!", 55, 142);
    }
  }, [localFrame]);

  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <canvas
        ref={canvasRef}
        width={270}
        height={480}
        style={{
          width: "1080px",
          height: "1920px",
          imageRendering: "pixelated"
        }}
      />
    </div>
  );
};
