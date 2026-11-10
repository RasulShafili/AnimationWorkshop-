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
  drawCellularBackground,
  drawMacroMitochondria,
  drawLipidBilayer,
  drawAtpSynthase,
  drawProtonStream,
  drawAtpSynthesisEvents,
  drawTachometerHud,
  drawVignetteAndScanlines,
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

    // 1. Deep Mitochondrial Matrix & Cytoplasm Atmosphere
    drawCellularBackground(ctx, frame);

    // 2. Early Macro Mitochondria Overview (Fade out by frame 120)
    const macroAlpha = Math.max(0, 1 - frame / 110);
    if (macroAlpha > 0) {
      drawMacroMitochondria(ctx, frame, macroAlpha);
    }

    // 3. Zoomed 100,000x Nanomotor Scene (Fades in from frame 80)
    const nanoAlpha = Math.min(1, Math.max(0, (frame - 80) / 40));
    if (nanoAlpha > 0) {
      ctx.save();
      ctx.globalAlpha = nanoAlpha;

      // Inner membrane lipid bilayer
      drawLipidBilayer(ctx, frame);

      // Flowing stream of positive H+ protons
      drawProtonStream(ctx, frame);

      // The 9,000 RPM ATP Synthase Rotary Motor
      drawAtpSynthase(ctx, frame);

      // ADP + Pi binding and ATP batteries launching
      drawAtpSynthesisEvents(ctx, frame);

      // 9,000 RPM Tachometer & Daily Recycled KG counter HUD (Positioned in bottom matrix!)
      drawTachometerHud(ctx, frame);

      ctx.restore();
    }

    // 4. Subtle Vignette & CRT Scanlines
    drawVignetteAndScanlines(ctx);
  }, [frame]);

  const activeBanners = timingData.bubbles.filter(
    (b: any) => frame >= b.startFrame && frame < b.endFrame
  );

  // Dynamic Telemetry Status Badge
  let statusText = "SCANNING MUSCLE CELL: MITOCHONDRIA";
  let statusColor = "#5CE1E6";
  if (frame >= 120 && frame < 240) {
    statusText = "ZOOM 100,000x: ATP SYNTHASE ROTOR";
    statusColor = "#00E5FF";
  } else if (frame >= 240 && frame < 360) {
    statusText = "TACHOMETER PINNED: 9,000 RPM ROTATION";
    statusColor = "#FFD54F";
  } else if (frame >= 360 && frame < 480) {
    statusText = "PROTON-MOTIVE FORCE: 180mV GRADIENT";
    statusColor = "#55EFC4";
  } else if (frame >= 480 && frame < 600) {
    statusText = "C-RING ROTOR: PROTON TRANSLOCATION";
    statusColor = "#00E5FF";
  } else if (frame >= 600 && frame < 720) {
    statusText = "F1 CATALYTIC HEAD: FORGING COVALENT BOND";
    statusColor = "#FFD54F";
  } else if (frame >= 720 && frame < 840) {
    statusText = "ATP CHARGE RELEASE: 3 BATTERIES / REVOLUTION";
    statusColor = "#55EFC4";
  } else if (frame >= 840) {
    statusText = "CELLULAR RECYCLER: ~70 KG OUTPUT PER DAY!";
    statusColor = "#FF5252";
  }

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0A0914",
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

        {/* Channel Branding Watermark */}
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: 175,
            textAlign: "center",
            fontFamily: FONT_PIXEL,
            fontSize: 18,
            color: "rgba(180, 220, 255, 0.40)",
            letterSpacing: "3px",
            pointerEvents: "none",
          }}
        >
          LEARN WITH 8-BIT
        </div>

        {/* Dynamic Telemetry Status Header */}
        <div
          style={{
            position: "absolute",
            left: "5%",
            right: "5%",
            top: 220,
            display: "flex",
            justifyContent: "center",
            pointerEvents: "none",
          }}
        >
          <div
            style={{
              padding: "8px 20px",
              backgroundColor: "rgba(10, 15, 28, 0.88)",
              border: `2px solid ${statusColor}`,
              borderRadius: 6,
              boxShadow: `0 0 16px ${statusColor}44`,
              fontFamily: FONT_PIXEL,
              fontSize: 20,
              color: statusColor,
              letterSpacing: "1px",
              textAlign: "center",
            }}
          >
            {statusText}
          </div>
        </div>

        {/* Single-Focus Center Text Standard (Big, Clear, Gold Border) */}
        {activeBanners.map((banner: any) => {
          const elapsed = frame - banner.startFrame;
          const charProg1 = Math.min(
            1,
            Math.max(0, elapsed / (banner.typeFrames * 0.5))
          );
          const charProg2 = Math.min(
            1,
            Math.max(
              0,
              (elapsed - banner.typeFrames * 0.4) / (banner.typeFrames * 0.6)
            )
          );

          const l1Len = Math.floor(charProg1 * banner.line1.length);
          const l2Len = Math.floor(charProg2 * banner.line2.length);

          const dispL1 = banner.line1.slice(0, l1Len);
          const dispL2 = banner.line2.slice(0, l2Len);

          return (
            <div
              key={banner.id}
              style={{
                position: "absolute",
                top: 295,
                left: "4%",
                right: "4%",
                backgroundColor: "rgba(8, 12, 24, 0.94)",
                border: "4px solid #FFD54F",
                borderRadius: 12,
                boxShadow:
                  "0 12px 36px rgba(0,0,0,0.8), 0 0 24px rgba(255, 213, 79, 0.35)",
                padding: "24px 28px",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                gap: 14,
                zIndex: 50,
              }}
            >
              <div
                style={{
                  fontFamily: FONT_PIXEL,
                  fontSize: 38,
                  color: "#FFFFFF",
                  textAlign: "center",
                  lineHeight: 1.4,
                  textShadow: "2px 2px 0 #000, -2px -2px 0 #000",
                }}
              >
                {dispL1}
              </div>
              <div
                style={{
                  fontFamily: FONT_PIXEL,
                  fontSize: 42,
                  color: banner.highlightColor || "#5CE1E6",
                  textAlign: "center",
                  lineHeight: 1.4,
                  textShadow: `0 0 16px ${banner.highlightColor || "#5CE1E6"}88, 2px 2px 0 #000`,
                }}
              >
                {dispL2}
              </div>
            </div>
          );
        })}

        {/* Audio Layer - Relaxing Non-Brain-Fatiguing Cellular ASMR (ZERO MUSIC) */}
        <Audio src={staticFile("mix.wav")} />
      </div>
    </AbsoluteFill>
  );
};
