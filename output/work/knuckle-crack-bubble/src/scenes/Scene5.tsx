import React, { useRef, useEffect } from "react";
import { useCurrentFrame } from "remotion";
import {
  drawJointRoom,
  drawBone,
  drawSynovialCapsule,
  drawMythBusterBadge,
  rect
} from "../pixelEngine";

export const Scene5: React.FC<{ startFrame: number; endFrame: number; globalFrame: number }> = ({ startFrame, globalFrame }) => {
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

    drawSynovialCapsule(ctx, cx, cy, gap, false, 0, 0, localFrame);

    // Bone with pixel sunglasses ("cool") and happy lower bone
    drawBone(ctx, cx, cy - 10, true, stretchOffset, "cool", localFrame);
    drawBone(ctx, cx, cy + 10, false, stretchOffset, "happy", localFrame);

    // Green checkmark badge: NO ARTHRITIS
    drawMythBusterBadge(ctx, 60, 105, localFrame);

    // Festive celebratory pixel confetti falling
    const colors = ["#ffe600", "#ff7675", "#00f0ff", "#55efc4", "#a29bfe"];
    for (let i = 0; i < 24; i++) {
      const confX = (i * 37 + (i % 3) * 17) % 270;
      const confY = ((localFrame * 2 + i * 23) % 400);
      rect(ctx, confX, confY, 3, 3, colors[i % colors.length]);
    }

    // Call to action prompt at bottom above subtitles
    if (localFrame > 150) {
      rect(ctx, 40, 360, 190, 24, "rgba(14, 13, 24, 0.95)");
      ctx.fillStyle = "#ffe600";
      ctx.font = "7px 'Press Start 2P', monospace";
      ctx.fillText("DO YOU CRACK YOURS?", 48, 376);
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
