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
  drawNeuroCortexBackground,
  drawSynapticJunction,
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

    // 1. Deep Neuro-Cortex Atmosphere & Aperture Arch
    drawNeuroCortexBackground(ctx, frame);

    // 2. Hyper-Detailed Synaptic Junction (Axon + 20nm Cleft + Dopamine + Dendrite)
    drawSynapticJunction(ctx, frame);
  }, [frame]);

  const activeBanners = timingData.bubbles.filter(
    (b: any) => frame >= b.startFrame && frame < b.endFrame
  );

  // Dynamic Synaptic Status Badge
  let statusText = "SCANNING SYNAPSE: 20nm GAP";
  let statusColor = "#5CE1E6";
  if (frame >= 240 && frame < 460) {
    statusText = "ACTION POTENTIAL RACING DOWN AXON";
    statusColor = "#00E5FF";
  } else if (frame >= 460 && frame < 600) {
    statusText = "VESICLES DOCKING: EXOCYTOSIS FLOOD";
    statusColor = "#FFD54F";
  } else if (frame >= 600 && frame < 740) {
    statusText = "DOPAMINE BINDING: D1/D2 RECEPTORS";
    statusColor = "#55EFC4";
  } else if (frame >= 740) {
    statusText = "NEW SIGNAL IGNITED: PLEASURE & FOCUS!";
    statusColor = "#FFD54F";
  }

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0E0C1E",
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
            color: "rgba(180, 160, 255, 0.40)",
            letterSpacing: "2px",
            pointerEvents: "none",
          }}
        >
          LEARN WITH 8-BIT
        </div>

        {/* 20nm Gap Scale Tag */}
        <div
          style={{
            position: "absolute",
            right: 28,
            top: 1115,
            fontFamily: FONT_PIXEL,
            fontSize: 13,
            color: "#5CE1E6",
            textShadow: "2px 2px 0 #0E061A",
            pointerEvents: "none",
          }}
        >
          20nm CLEFT
        </div>

        {/* Anatomical Structure Micro-Badges */}
        <div
          style={{
            position: "absolute",
            left: 32,
            top: 730,
            fontFamily: FONT_PIXEL,
            fontSize: 14,
            color: "#B39DDB",
            backgroundColor: "rgba(14, 12, 30, 0.75)",
            padding: "4px 8px",
            border: "2px solid #512DA8",
            pointerEvents: "none",
          }}
        >
          PRESYNAPTIC AXON
        </div>
        <div
          style={{
            position: "absolute",
            left: 32,
            top: 1460,
            fontFamily: FONT_PIXEL,
            fontSize: 14,
            color: "#A5D6A7",
            backgroundColor: "rgba(14, 12, 30, 0.75)",
            padding: "4px 8px",
            border: "2px solid #2E7D32",
            pointerEvents: "none",
          }}
        >
          POSTSYNAPTIC DENDRITE
        </div>

        {/* Dynamic Synaptic Status Bar at Bottom */}
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: 1715,
            textAlign: "center",
            fontFamily: FONT_PIXEL,
            fontSize: 21,
            color: statusColor,
            textShadow: "4px 4px 0 #06040C",
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
                    "6px 6px 0 #080612, -4px -4px 0 #080612, 4px -4px 0 #080612, -4px 4px 0 #080612",
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
                      "6px 6px 0 #080612, -4px -4px 0 #080612, 4px -4px 0 #080612, -4px 4px 0 #080612",
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
