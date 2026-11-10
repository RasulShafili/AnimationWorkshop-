import React, { useLayoutEffect, useRef } from "react";
import { AbsoluteFill, Audio, staticFile, useCurrentFrame } from "remotion";
import { renderFrame } from "./scenes";
import { W, H } from "./gfx";

export const MainVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const ref = useRef<HTMLCanvasElement>(null);
  useLayoutEffect(() => {
    const ctx = ref.current!.getContext("2d")!;
    const img = ctx.createImageData(W, H);
    renderFrame(frame, img.data);
    ctx.putImageData(img, 0, 0);
  }, [frame]);
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <canvas ref={ref} width={W} height={H} style={{ width: 1080, height: 1920, imageRendering: "pixelated" }} />
      <Audio src={staticFile("mix.wav")} />
    </AbsoluteFill>
  );
};
