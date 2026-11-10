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
  drawOpticalScannerBackground,
  drawBlindSpotExperiment,
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

    // 1. Cosmic Optical Lab Background & Scanner Bezel Arch
    drawOpticalScannerBackground(ctx, frame);

    // 2. Interactive Blind-Spot Test Strip + Eye & Optic Nerve Cross-Section
    drawBlindSpotExperiment(ctx, frame);
  }, [frame]);

  // Single-Focus Center Text Beat (Positioned directly above the interactive test chamber!)
  const activeBanners = timingData.bubbles.filter(
    (b: any) => frame >= b.startFrame && frame < b.endFrame
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#141026",
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
            color: "rgba(180, 210, 255, 0.42)",
            letterSpacing: "2px",
            pointerEvents: "none",
          }}
        >
          LEARN WITH 8-BIT
        </div>

        {/* Micro Labels inside the Interactive Blind-Spot Chamber */}
        <div
          style={{
            position: "absolute",
            left: 86,
            top: 882,
            fontFamily: FONT_PIXEL,
            fontSize: 18,
            color: "#5CE1E6",
            textShadow: "3px 3px 0 #0A0814",
            pointerEvents: "none",
          }}
        >
          STARE AT (+)
        </div>
        <div
          style={{
            position: "absolute",
            right: 88,
            top: 882,
            fontFamily: FONT_PIXEL,
            fontSize: 18,
            color: "#FFD54F",
            textShadow: "3px 3px 0 #0A0814",
            pointerEvents: "none",
          }}
        >
          STAR VANISHES!
        </div>

        {/* Micro Labels on Eye & Optic Nerve Diagram */}
        <div
          style={{
            position: "absolute",
            left: 195,
            top: 1515,
            fontFamily: FONT_PIXEL,
            fontSize: 18,
            color: "#FF6B6B",
            textShadow: "3px 3px 0 #0A0814",
            pointerEvents: "none",
          }}
        >
          OPTIC NERVE PLUG (0 PIXELS)
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
                    "6px 6px 0 #0A0814, -4px -4px 0 #0A0814, 4px -4px 0 #0A0814, -4px 4px 0 #0A0814",
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
                    fontSize: banner.bigLine2 ? 74 : 46,
                    color: banner.highlightLine === 2 ? hiColor : "#FFFFFF",
                    textShadow:
                      "6px 6px 0 #0A0814, -4px -4px 0 #0A0814, 4px -4px 0 #0A0814, -4px 4px 0 #0A0814",
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
