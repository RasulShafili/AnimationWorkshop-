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
  drawRibcageBackground,
  drawLiverAndGallbladder,
} from "./pixelEngine";

const FONT_PIXEL = "'Press Start 2P', monospace";

export const MainVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  // Laser Regeneration Sweep:
  // Frames 0 - 360: scanBaseX = 134 (left 70% is cyan wireframe hologram, right 30% is solid liver)
  // Frames 360 - 600: laser sweeps left from 134 to 18 (regenerating 100% of the liver!)
  // Frames 600 - 960: scanBaseX = 18 (100% solid regrown liver!)
  let scanBaseX = 134;
  if (frame >= 360 && frame < 600) {
    const t = (frame - 360) / 240;
    scanBaseX = Math.round(134 - t * 116);
  } else if (frame >= 600) {
    scanBaseX = 18;
  }

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.imageSmoothingEnabled = false;

    // 1. Burgundy-Violet Body Cavity, Amber Halo, Curved Ribs & Diaphragm Arch
    drawRibcageBackground(ctx, frame);

    // 2. Hero Cute Liver (with 70% Cyan Wireframe & Laser Regrowth) + Green Gallbladder Buddy
    drawLiverAndGallbladder(ctx, frame, scanBaseX);
  }, [frame, scanBaseX]);

  // Single-Focus Center Text Beat (Right above the liver in the center cavity!)
  const activeBanners = timingData.bubbles.filter(
    (b: any) => frame >= b.startFrame && frame < b.endFrame
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#2C1638",
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

        {/* Subtle Channel Watermark on the Maroon Diaphragm Arch (Matches Reference!) */}
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: 520,
            textAlign: "center",
            fontFamily: FONT_PIXEL,
            fontSize: 18,
            color: "rgba(255, 210, 220, 0.38)",
            letterSpacing: "2px",
            pointerEvents: "none",
          }}
        >
          LEARN WITH 8-BIT
        </div>

        {/* SINGLE-FOCUS CENTER TEXT (Positioned right above the central liver & laser scan!) */}
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
                    "6px 6px 0 #120818, -4px -4px 0 #120818, 4px -4px 0 #120818, -4px 4px 0 #120818",
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
                    fontSize: banner.bigLine2 ? 82 : 46,
                    color: banner.highlightLine === 2 ? hiColor : "#FFFFFF",
                    textShadow:
                      "6px 6px 0 #120818, -4px -4px 0 #120818, 4px -4px 0 #120818, -4px 4px 0 #120818",
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
