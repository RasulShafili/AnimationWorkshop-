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
  drawNightCityWindow,
  drawTableAndPlate,
  drawWhiteSugarBuddy,
  drawSpoonAndGoldenCube,
  drawAtomicHologram,
} from "./pixelEngine";

const FONT_PIXEL = "'Press Start 2P', monospace";

export const MainVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  // Porcelain plate crack state:
  // In Beat 1 (frames 0-240), show the iconic shattered plate from the reference hook!
  // In Beats 3-6 (frames 240-724), intact plate while explaining the atomic compression,
  // then at Frame 725, MASSIVE 500-MILLION-TON SHATTER IMPACT!
  let crackProgress = 0;
  if (frame < 240) {
    crackProgress = 1.0;
  } else if (frame >= 725) {
    crackProgress = Math.min(1.0, (frame - 725) / 10);
  }

  // Spoon heavy drop offset at Frame 725
  let heavyDropOffset = 0;
  if (frame >= 725 && frame < 755) {
    heavyDropOffset = Math.max(0, 6 - (frame - 725) * 0.2);
  }

  // Sugar Buddy mood
  let mood: "curious" | "shocked" | "amazed" = "curious";
  if (frame >= 720 && frame < 840) {
    mood = "shocked";
  } else if (frame >= 840) {
    mood = "amazed";
  }

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.imageSmoothingEnabled = false;

    // 1. Night City Window Backdrop
    drawNightCityWindow(ctx, frame);

    // 2. Wooden Table & Giant Porcelain Plate
    drawTableAndPlate(ctx, frame, crackProgress);

    // 3. Cute White Sugar Cube Character ("SUGAR BUDDY")
    drawWhiteSugarBuddy(ctx, frame, mood);

    // 4. Silver Spoon & Glowing Golden Compressed Humanity Sugar Cube
    drawSpoonAndGoldenCube(ctx, frame, heavyDropOffset);

    // 5. Quantum Atomic Empty-Space Hologram (Frames 240 - 715)
    drawAtomicHologram(ctx, frame);
  }, [frame, crackProgress, heavyDropOffset, mood]);

  // Camera shake on the 500-Million-Ton impact at Frame 725!
  let shakeX = 0;
  let shakeY = 0;
  if (frame >= 725 && frame <= 745) {
    const decay = (746 - frame) / 21;
    shakeX = Math.round(Math.sin(frame * 2.9) * 18 * decay);
    shakeY = Math.round(Math.cos(frame * 3.4) * 18 * decay);
  }

  // Single-Focus Center Text Beat (Right above the central spoon & sugar cubes!)
  const activeBanners = timingData.bubbles.filter(
    (b: any) => frame >= b.startFrame && frame < b.endFrame
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#10172A",
        overflow: "hidden",
        userSelect: "none",
      }}
    >
      <div
        style={{
          position: "relative",
          width: "100%",
          height: "100%",
          transform: `translate(${shakeX}px, ${shakeY}px)`,
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

        {/* Subtle Channel Watermark on the Porcelain Plate Rim */}
        <div
          style={{
            position: "absolute",
            left: 36,
            top: 1368,
            fontFamily: FONT_PIXEL,
            fontSize: 16,
            color: "rgba(255, 255, 255, 0.55)",
            textShadow: "2px 2px 0 #1A2232",
            letterSpacing: "1px",
            pointerEvents: "none",
          }}
        >
          LEARN WITH 8-BIT
        </div>

        {/* SINGLE-FOCUS CENTER TEXT (Positioned right above the spoon & sugar cubes!) */}
        {activeBanners.map((banner: any) => {
          const elapsed = frame - banner.startFrame;
          const progress = Math.min(1, elapsed / banner.typeFrames);
          const l1 = banner.line1 || "";
          const l2 = banner.line2 || "";
          const l3 = banner.line3 || "";
          const totalChars = l1.length + l2.length + l3.length;
          const revealed = Math.floor(totalChars * progress);

          const s1 = l1.slice(0, Math.min(l1.length, revealed));
          const rem1 = Math.max(0, revealed - l1.length);
          const s2 = l2.slice(0, Math.min(l2.length, rem1));
          const rem2 = Math.max(0, rem1 - l2.length);
          const s3 = l3.slice(0, Math.min(l3.length, rem2));
          const hiColor = banner.highlightColor || "#FFD54F";

          return (
            <div
              key={banner.id}
              style={{
                position: "absolute",
                top: 390,
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
                  fontSize: 44,
                  color: banner.highlightLine === 1 ? hiColor : "#FFFFFF",
                  textShadow:
                    "6px 6px 0 #090C15, -4px -4px 0 #090C15, 4px -4px 0 #090C15, -4px 4px 0 #090C15",
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
                    fontSize: 46,
                    color: banner.highlightLine === 2 ? hiColor : "#FFFFFF",
                    textShadow:
                      "6px 6px 0 #090C15, -4px -4px 0 #090C15, 4px -4px 0 #090C15, -4px 4px 0 #090C15",
                    textAlign: "center",
                    lineHeight: 1.25,
                  }}
                >
                  {s2}
                </div>
              )}
              {s3.length > 0 && (
                <div
                  style={{
                    fontFamily: FONT_PIXEL,
                    fontSize: 46,
                    color: banner.highlightLine === 3 ? hiColor : "#FFFFFF",
                    textShadow:
                      "6px 6px 0 #090C15, -4px -4px 0 #090C15, 4px -4px 0 #090C15, -4px 4px 0 #090C15",
                    textAlign: "center",
                    lineHeight: 1.25,
                  }}
                >
                  {s3}
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
