import React, { useEffect, useRef } from "react";
import {
  AbsoluteFill,
  Audio,
  staticFile,
  useCurrentFrame,
} from "remotion";
import "@fontsource/press-start-2p";
import timingData from "./timing.json";
import {
  PW,
  PH,
  drawVisionStudioBackground,
  drawEyesNoseAndBrainScene,
} from "./pixelEngine";

const FONT_PIXEL = "'Press Start 2P', monospace";

export const MainVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.imageSmoothingEnabled = false;

    // 1. Neural Vision Studio Background & Optical Bezel Arch
    drawVisionStudioBackground(ctx, frame);

    // 2. Hero Two Eyes + Overlapping Vision Cones + Giant Center Nose + Brain Editor
    drawEyesNoseAndBrainScene(ctx, frame);
  }, [frame]);

  const activeBanners = timingData.bubbles.filter(
    (b: any) => frame >= b.startFrame && frame < b.endFrame
  );
  const isErased = frame >= 240 && frame < 700;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#18142C",
        overflow: "hidden",
        userSelect: "none",
      }}
    >
      <div
        style={{
          position: "relative",
          width: "100%",
          height: "100%",
        }}
      >
        <canvas
          ref={canvasRef}
          width={PW}
          height={PH}
          style={{
            width: "100%",
            height: "100%",
            imageRendering: "pixelated",
            display: "block",
          }}
        />

        {/* Subtle Channel Watermark on the Optical Bezel Arch */}
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: 520,
            textAlign: "center",
            fontFamily: FONT_PIXEL,
            fontSize: 18,
            color: "rgba(210, 195, 255, 0.40)",
            letterSpacing: "2px",
            pointerEvents: "none",
          }}
        >
          LEARN WITH 8-BIT
        </div>

        {/* Status Badge below Brain Editor */}
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: 1515,
            textAlign: "center",
            fontFamily: FONT_PIXEL,
            fontSize: 22,
            color: isErased ? "#55EFC4" : "#FF6B6B",
            textShadow: "4px 4px 0 #100A1E",
            pointerEvents: "none",
          }}
        >
          {isErased
            ? "BRAIN FILTER: AUTO-ERASE ON"
            : "MANUAL VIEW: NOSE VISIBLE!"}
        </div>

        {/* SINGLE-FOCUS CENTER TEXT */}
        {activeBanners.map((banner: any) => {
          const elapsed = frame - banner.startFrame;
          const progress = Math.min(1, elapsed / banner.typeFrames);
          const l1 = banner.line1 || "";
          const l2 = banner.line2 || "";
          const totalChars = l1.length + l2.length;
          const revealed = Math.floor(totalChars * progress);

          const s1 = l1.slice(0, Math.min(l1.length, revealed));
          const s2 =
            revealed > l1.length ? l2.slice(0, revealed - l1.length) : "";
          const hiColor = banner.highlightColor || "#FFD54F";

          return (
            <div
              key={banner.id}
              style={{
                position: "absolute",
                top: 340,
                left: 32,
                right: 32,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 18,
                pointerEvents: "none",
              }}
            >
              <div
                style={{
                  fontFamily: FONT_PIXEL,
                  fontSize: 42,
                  color: banner.highlightLine === 1 ? hiColor : "#FFFFFF",
                  textShadow:
                    "6px 6px 0 #100A1E, -4px -4px 0 #100A1E, 4px -4px 0 #100A1E, -4px 4px 0 #100A1E",
                  textAlign: "center",
                  lineHeight: 1.25,
                }}
              >
                {s1}
              </div>
              {s2.length > 0 && (
                <div
                  style={{
                    fontFamily: FONT_PIXEL,
                    fontSize: banner.bigLine2 ? 76 : 46,
                    color: banner.highlightLine === 2 ? hiColor : "#FFFFFF",
                    textShadow:
                      "6px 6px 0 #100A1E, -4px -4px 0 #100A1E, 4px -4px 0 #100A1E, -4px 4px 0 #100A1E",
                    textAlign: "center",
                    lineHeight: 1.2,
                  }}
                >
                  {s2}
                </div>
              )}
            </div>
          );
        })}
      </div>

      <Audio src={staticFile("mix.wav")} />
    </AbsoluteFill>
  );
};
