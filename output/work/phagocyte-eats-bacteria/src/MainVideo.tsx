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
  drawMicroscopicBloodArena,
  drawPhagocytosisBattle,
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

    // 1. Dark-Field Microscopic Blood Arena & Aperture Arch
    drawMicroscopicBloodArena(ctx, frame);

    // 2. Living Macrophage + Extending Pseudopodia + Bacteria + Lysosome Digestion
    drawPhagocytosisBattle(ctx, frame);
  }, [frame]);

  const activeBanners = timingData.bubbles.filter(
    (b: any) => frame >= b.startFrame && frame < b.endFrame
  );

  // Dynamic Microscopic Battle Status Badge
  let statusText = "CHEMOTAXIS: DETECTING PATHOGEN";
  let statusColor = "#5CE1E6";
  if (frame >= 240 && frame < 480) {
    statusText = "EXTENDING PSEUDOPODIA (CELL ARMS)";
    statusColor = "#55EFC4";
  } else if (frame >= 480 && frame < 600) {
    statusText = "PHAGOSOME VACUOLE TRAP SEALED!";
    statusColor = "#5CE1E6";
  } else if (frame >= 600 && frame < 720) {
    statusText = "LYSOSOMES FUSING: ACID HYDROLASES";
    statusColor = "#FFD54F";
  } else if (frame >= 720) {
    statusText = "PATHOGEN DIGESTED & NEUTRALIZED!";
    statusColor = "#55EFC4";
  }

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#120A20",
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

        {/* Subtle Channel Watermark on the Aperture Arch */}
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: 520,
            textAlign: "center",
            fontFamily: FONT_PIXEL,
            fontSize: 18,
            color: "rgba(200, 180, 255, 0.40)",
            letterSpacing: "2px",
            pointerEvents: "none",
          }}
        >
          LEARN WITH 8-BIT
        </div>

        {/* Reticle Label on Microscope Scope */}
        <div
          style={{
            position: "absolute",
            left: 120,
            top: 792,
            fontFamily: FONT_PIXEL,
            fontSize: 14,
            color: "#5CE1E6",
            textShadow: "2px 2px 0 #0E061A",
            pointerEvents: "none",
          }}
        >
          10,000x ZOOM
        </div>

        {/* Cellular Structure Micro-Labels */}
        <div
          style={{
            position: "absolute",
            left: 54,
            top: 1420,
            fontFamily: FONT_PIXEL,
            fontSize: 14,
            color: "#B39DDB",
            backgroundColor: "rgba(18, 10, 32, 0.75)",
            padding: "4px 8px",
            border: "2px solid #512DA8",
            pointerEvents: "none",
          }}
        >
          MACROPHAGE (WBC)
        </div>
        <div
          style={{
            position: "absolute",
            right: 48,
            top: 1420,
            fontFamily: FONT_PIXEL,
            fontSize: 14,
            color: "#A5D6A7",
            backgroundColor: "rgba(18, 10, 32, 0.75)",
            padding: "4px 8px",
            border: "2px solid #2E7D32",
            pointerEvents: "none",
          }}
        >
          BACTERIA TARGET
        </div>

        {/* Dynamic Microscopic Status Bar at Bottom */}
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: 1680,
            textAlign: "center",
            fontFamily: FONT_PIXEL,
            fontSize: 21,
            color: statusColor,
            textShadow: "4px 4px 0 #080310",
            pointerEvents: "none",
          }}
        >
          {statusText}
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
                    "6px 6px 0 #0E061A, -4px -4px 0 #0E061A, 4px -4px 0 #0E061A, -4px 4px 0 #0E061A",
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
                      "6px 6px 0 #0E061A, -4px -4px 0 #0E061A, 4px -4px 0 #0E061A, -4px 4px 0 #0E061A",
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
