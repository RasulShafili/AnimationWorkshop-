import React, { useRef, useEffect } from "react";
import { useCurrentFrame } from "remotion";
import {
  drawJointRoom,
  drawBone,
  drawSynovialCapsule,
  drawVacuumGauge
} from "../pixelEngine";

export const Scene3: React.FC<{ startFrame: number; endFrame: number; globalFrame: number }> = ({ startFrame, globalFrame }) => {
  const frame = useCurrentFrame();
  const localFrame = frame;
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    drawJointRoom(ctx, 270, 480, localFrame);

    const cy = 250;
    const cx = 135;
    const gap = 42;
    const stretchOffset = 40;

    // Bubble lifecycle:
    // 0-40 frames: rapidly grows from 0 to 14px radius
    // 40-70 frames: oscillates then violently collapses at frame 70!
    // 70-130 frames: shockwave ripples outward!
    let bubbleR = 0;
    let showBubble = false;
    let shockProg = 0;

    if (localFrame < 70) {
      showBubble = true;
      const growProg = Math.min(1.0, localFrame / 35);
      bubbleR = growProg * 14 + Math.sin(localFrame * 0.4) * 1.5;
    } else {
      showBubble = false;
      shockProg = (localFrame - 70) / 45;
    }

    drawSynovialCapsule(ctx, cx, cy, gap, showBubble, bubbleR, shockProg, localFrame);

    const expr = localFrame >= 70 ? "shock" : "strain";
    drawBone(ctx, cx, cy - 10, true, stretchOffset, expr, localFrame);
    drawBone(ctx, cx, cy + 10, false, stretchOffset, expr, localFrame);

    drawVacuumGauge(ctx, 15, 110, localFrame >= 70 ? 0.7 : 0.05, localFrame);
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
