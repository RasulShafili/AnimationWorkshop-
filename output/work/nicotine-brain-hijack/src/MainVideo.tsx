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
  drawCityStreetBackground,
  drawAlexCharacter,
  drawCartoonBrainCharacter,
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

    // 1. City Street Night Background
    drawCityStreetBackground(ctx, frame);

    // S C E N E   M A N A G E R   (Smooth Cartoon Transitions)

    // SCENE 1: Alex smoking/vaping under street lamp (f0 - f180)
    if (frame < 185) {
      const alpha = frame < 170 ? 1 : Math.max(0, 1 - (frame - 170) / 15);
      ctx.save();
      ctx.globalAlpha = alpha;
      drawAlexCharacter(ctx, frame, "smoking");
      ctx.restore();
    }

    // SCENE 2: The Cartoon Brain Dopamine Jackpot Party! (f170 - f365)
    if (frame >= 170 && frame < 365) {
      const fadeIn = Math.min(1, (frame - 170) / 15);
      const fadeOut = frame < 350 ? 1 : Math.max(0, 1 - (frame - 350) / 15);
      ctx.save();
      ctx.globalAlpha = fadeIn * fadeOut;
      drawCartoonBrainCharacter(ctx, frame, "jackpotParty");
      ctx.restore();
    }

    // SCENE 3: Alex Superhero High & 95 BPM Pumping Heart (f350 - f545)
    if (frame >= 350 && frame < 545) {
      const fadeIn = Math.min(1, (frame - 350) / 15);
      const fadeOut = frame < 530 ? 1 : Math.max(0, 1 - (frame - 530) / 15);
      ctx.save();
      ctx.globalAlpha = fadeIn * fadeOut;
      drawAlexCharacter(ctx, frame, "superhero");
      ctx.restore();
    }

    // SCENE 4: The Brain Mutates - Hungry Monster Jaws (f530 - f725)
    if (frame >= 530 && frame < 725) {
      const fadeIn = Math.min(1, (frame - 530) / 15);
      const fadeOut = frame < 710 ? 1 : Math.max(0, 1 - (frame - 710) / 15);
      ctx.save();
      ctx.globalAlpha = fadeIn * fadeOut;
      drawCartoonBrainCharacter(ctx, frame, "hungryMonster");
      ctx.restore();
    }

    // SCENE 5: 30 Mins Later - Alex Craving Zombie (f710 - f960)
    if (frame >= 710) {
      const fadeIn = Math.min(1, (frame - 710) / 15);
      ctx.save();
      ctx.globalAlpha = fadeIn;
      drawAlexCharacter(ctx, frame, "cravingZombie");
      ctx.restore();
    }

    // Vignette & Scanlines
    drawVignetteAndScanlines(ctx);
  }, [frame]);

  const activeBanners = timingData.bubbles.filter(
    (b: any) => frame >= b.startFrame && frame < b.endFrame
  );

  // Dynamic Cartoon Telemetry Status Header
  let statusText = "WHAT DOES NICOTINE DO TO YOUR BRAIN? 🧠";
  let statusColor = "#FFD54F";
  if (frame >= 120 && frame < 240) {
    statusText = "PUFF TAKEN: 10s TO BRAIN! ⏱️";
    statusColor = "#76FF03";
  } else if (frame >= 240 && frame < 360) {
    statusText = "BRAIN REWARD: DOPAMINE JACKPOT! 🎰";
    statusColor = "#FFD54F";
  } else if (frame >= 360 && frame < 540) {
    statusText = "SUPERHERO HIGH: PULSE SPIKES TO 95 BPM! ⚡";
    statusColor = "#FF6B6B";
  } else if (frame >= 540 && frame < 720) {
    statusText = "TOLERANCE: BRAIN GROWS HUNGRY MOUTHS! 👾";
    statusColor = "#5CE1E6";
  } else if (frame >= 720) {
    statusText = "30 MINS LATER: THE CRAVING TRAP! 😫";
    statusColor = "#FF1744";
  }

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#080614",
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
            color: "rgba(255, 213, 79, 0.40)",
            letterSpacing: "3px",
            pointerEvents: "none",
          }}
        >
          LEARN WITH 8-BIT
        </div>

        {/* Dynamic Cartoon Telemetry Status Header */}
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
              backgroundColor: "rgba(10, 8, 24, 0.92)",
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
                backgroundColor: "rgba(10, 8, 24, 0.95)",
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

        {/* Audio Layer - Engaging Cartoon Sound Effects (LOUD & AUDIBLE, ZERO MUSIC) */}
        <Audio src={staticFile("mix.wav")} />
      </div>
    </AbsoluteFill>
  );
};
