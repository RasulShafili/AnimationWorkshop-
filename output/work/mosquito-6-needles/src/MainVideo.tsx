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
  drawMicroscopeHeader,
  drawDetailedSkinCrossSection,
  drawMosquitoAndSixNeedles,
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

    // 1. Night Sky & Electron-Microscope Header Arch
    drawMicroscopeHeader(ctx, frame);

    // 2. Multi-Layered Anatomical Human Skin Cross-Section (Epidermis + Dermis + Capillary + RBCs + Mast Cells)
    drawDetailedSkinCrossSection(ctx, frame);

    // 3. Hyper-Detailed Perched Mosquito + Bowing Labium Sheath + 6 Surgical Needles + SEM Zoom HUD
    drawMosquitoAndSixNeedles(ctx, frame);
  }, [frame]);

  const activeBanners = timingData.bubbles.filter(
    (b: any) => frame >= b.startFrame && frame < b.endFrame
  );

  // Dynamic Surgical Tool Status Badge at Bottom
  let toolStatus = "SCANNING PROBOSCIS: 6 MICRO-BLADES";
  let toolColor = "#5CE1E6";
  if (frame >= 240 && frame < 360) {
    toolStatus = "ACTIVE: #1 & #2 MAXILLAE SAWS";
    toolColor = "#5CE1E6";
  } else if (frame >= 360 && frame < 480) {
    toolStatus = "ACTIVE: #3 & #4 MANDIBLE CLAMPS";
    toolColor = "#FFD54F";
  } else if (frame >= 480 && frame < 600) {
    toolStatus = "ACTIVE: #5 ANTI-CLOT SALIVA TUBE";
    toolColor = "#55EFC4";
  } else if (frame >= 600 && frame < 720) {
    toolStatus = "ACTIVE: #6 LABRUM BLOOD SEEKER";
    toolColor = "#FF6B6B";
  } else if (frame >= 720) {
    toolStatus = "SIPHONING RBCs + HISTAMINE SWELL!";
    toolColor = "#FF5252";
  }

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#101426",
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

        {/* Subtle Channel Watermark on the Microscope Bezel Arch */}
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: 520,
            textAlign: "center",
            fontFamily: FONT_PIXEL,
            fontSize: 18,
            color: "rgba(190, 220, 255, 0.42)",
            letterSpacing: "2px",
            pointerEvents: "none",
          }}
        >
          LEARN WITH 8-BIT
        </div>

        {/* SEM Zoom Scope Label */}
        <div
          style={{
            position: "absolute",
            left: 142,
            top: 792,
            fontFamily: FONT_PIXEL,
            fontSize: 14,
            color: "#5CE1E6",
            textShadow: "2px 2px 0 #0A0D18",
            pointerEvents: "none",
          }}
        >
          6-BLADE SCOPE
        </div>

        {/* Anatomical Layer Micro-Labels with Semi-Transparent Pixel Badges */}
        <div
          style={{
            position: "absolute",
            right: 24,
            top: 890,
            fontFamily: FONT_PIXEL,
            fontSize: 14,
            color: "#FFE0B2",
            backgroundColor: "rgba(20, 10, 20, 0.75)",
            padding: "4px 8px",
            border: "2px solid #C87A60",
            pointerEvents: "none",
          }}
        >
          EPIDERMIS
        </div>
        <div
          style={{
            position: "absolute",
            right: 24,
            top: 1110,
            fontFamily: FONT_PIXEL,
            fontSize: 14,
            color: "#FFCDD2",
            backgroundColor: "rgba(20, 10, 20, 0.75)",
            padding: "4px 8px",
            border: "2px solid #B84862",
            pointerEvents: "none",
          }}
        >
          DERMIS
        </div>
        <div
          style={{
            position: "absolute",
            right: 24,
            top: 1435,
            fontFamily: FONT_PIXEL,
            fontSize: 14,
            color: "#FF8A80",
            backgroundColor: "rgba(20, 10, 20, 0.75)",
            padding: "4px 8px",
            border: "2px solid #E53935",
            pointerEvents: "none",
          }}
        >
          CAPILLARY
        </div>

        {/* Dynamic Surgical Status Bar below Capillary */}
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: 1715,
            textAlign: "center",
            fontFamily: FONT_PIXEL,
            fontSize: 21,
            color: toolColor,
            textShadow: "4px 4px 0 #0D060A",
            pointerEvents: "none",
          }}
        >
          {toolStatus}
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
                  fontSize: 40,
                  color: banner.highlightLine === 1 ? hiColor : "#FFFFFF",
                  textShadow:
                    "6px 6px 0 #0A0D18, -4px -4px 0 #0A0D18, 4px -4px 0 #0A0D18, -4px 4px 0 #0A0D18",
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
                    fontSize: banner.bigLine2 ? 74 : 44,
                    color: banner.highlightLine === 2 ? hiColor : "#FFFFFF",
                    textShadow:
                      "6px 6px 0 #0A0D18, -4px -4px 0 #0A0D18, 4px -4px 0 #0A0D18, -4px 4px 0 #0A0D18",
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
