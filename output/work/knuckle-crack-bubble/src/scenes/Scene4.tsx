import React, { useRef, useEffect } from "react";
import { useCurrentFrame } from "remotion";
import {
  drawJointRoom,
  drawBone,
  drawSynovialCapsule,
  drawRechargeTimer,
  rect
} from "../pixelEngine";

export const Scene4: React.FC<{ startFrame: number; endFrame: number; globalFrame: number }> = ({ startFrame, globalFrame }) => {
  const frame = useCurrentFrame();
  const localFrame = frame;
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    drawJointRoom(ctx, 270, 480, localFrame);

    const cy = 270;
    const cx = 135;
    const gap = 16;
    const stretchOffset = 26;

    // Joint is back together, trying to crack again
    drawSynovialCapsule(ctx, cx, cy, gap, false, 0, 0, localFrame);

    // Bone tries to stretch slightly, question mark pops up
    const tryProg = Math.sin(localFrame * 0.15);
    drawBone(ctx, cx, cy - 10, true, stretchOffset + (tryProg > 0 ? tryProg * 4 : 0), "normal", localFrame);
    drawBone(ctx, cx, cy + 10, false, stretchOffset, "normal", localFrame);

    if (localFrame < 80) {
      // Question mark over bone
      rect(ctx, cx + 22, cy - 65, 18, 20, "rgba(14, 13, 24, 0.85)");
      ctx.fillStyle = "#ffe600";
      ctx.font = "14px 'Press Start 2P', monospace";
      ctx.fillText("?", cx + 26, cy - 50);
    }

    // 20-Minute Digital Timer counting down from 20:00.00 down to 00:00.00
    // Total duration of Scene 4 is 195 frames (~6.5 sec)
    const countdownSec = Math.max(0, 1200 - (localFrame / 195) * 1200);
    drawRechargeTimer(ctx, 70, 105, countdownSec, localFrame);
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
