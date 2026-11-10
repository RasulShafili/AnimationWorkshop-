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
  drawMeadowNight,
  drawCricketAndFrog,
  drawWoodenThermometer,
} from "./pixelEngine";

const FONT_PIXEL = "'Press Start 2P', monospace";

export const MainVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  // Check if the cricket is currently rubbing its wings (within 8 frames after any chirpFrame)
  const chirpFrames: number[] = (timingData as any).chirpFrames || [];
  const isChirping = chirpFrames.some(
    (cf) => frame >= cf && frame <= cf + 8
  );
  const isFrogCroaking =
    (frame >= 485 && frame <= 520) || (frame >= 725 && frame <= 760);

  // Calculate live chirp count (scales smoothly from 1 up to 32 chirps across 960 frames!)
  let chirpCount = 1;
  if (frame < 240) {
    chirpCount = 1 + Math.floor((frame / 240) * 5);
  } else if (frame < 660) {
    chirpCount = 6 + Math.floor(((frame - 240) / 420) * 26);
  } else {
    chirpCount = 32;
  }

  // Temperature on the wooden thermometer: Dolbear's Law -> Chirps + 40 = °F!
  const currentTempF = 40 + chirpCount;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.imageSmoothingEnabled = false;

    // 1. Starry Night Sky, Moon, Distant Hills, Lush Grass & Circular Timer Ring
    drawMeadowNight(ctx, frame);

    // 2. Hero Cricket on Giant Leaf + Cute Frog Buddy on Lily Pad
    drawCricketAndFrog(ctx, frame, isChirping, isFrogCroaking);

    // 3. Tall Wooden Mercury Thermometer on the Right
    drawWoodenThermometer(ctx, currentTempF);
  }, [frame, isChirping, isFrogCroaking, currentTempF]);

  // Single-Focus Center Text Beat (Right above the central CHIRPS ring & cricket!)
  const activeBanners = timingData.bubbles.filter(
    (b: any) => frame >= b.startFrame && frame < b.endFrame
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#141834",
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

        {/* 1. Circular Timer Ring Center Number + "CHIRPS" Label (Exact Match to Reference!) */}
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: 536,
            textAlign: "center",
            fontFamily: FONT_PIXEL,
            fontSize: 56,
            color: "#FFD54F",
            textShadow:
              "6px 6px 0 #101224, -4px -4px 0 #101224, 4px -4px 0 #101224, -4px 4px 0 #101224",
            pointerEvents: "none",
          }}
        >
          {chirpCount}
        </div>
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: 668,
            textAlign: "center",
            fontFamily: FONT_PIXEL,
            fontSize: 30,
            color: "#FFFFFF",
            textShadow:
              "4px 4px 0 #101224, -3px -3px 0 #101224, 3px -3px 0 #101224, -3px 3px 0 #101224",
            pointerEvents: "none",
          }}
        >
          CHIRPS
        </div>

        {/* 2. Thermometer Degree Numbers & Vertical @PIXEL_FACT.8BIT Wood Engraving */}
        {[
          { label: "90", top: 656 },
          { label: "80", top: 736 },
          { label: "70", top: 816 },
          { label: "60", top: 896 },
          { label: "50", top: 976 },
          { label: "40", top: 1056 },
        ].map((tick) => (
          <div
            key={tick.label}
            style={{
              position: "absolute",
              left: 822,
              top: tick.top,
              fontFamily: FONT_PIXEL,
              fontSize: 13,
              color: "#2A180C",
              pointerEvents: "none",
            }}
          >
            {tick.label}
          </div>
        ))}

        {/* Vertical LEARN WITH 8-BIT Watermark on Wooden Post */}
        <div
          style={{
            position: "absolute",
            left: 856,
            top: 1310,
            transform: "rotate(90deg)",
            transformOrigin: "left top",
            fontFamily: FONT_PIXEL,
            fontSize: 15,
            color: "rgba(255, 240, 210, 0.65)",
            textShadow: "2px 2px 0 #2A180C",
            letterSpacing: "2px",
            pointerEvents: "none",
            whiteSpace: "nowrap",
          }}
        >
          LEARN WITH 8-BIT
        </div>

        {/* 3. SINGLE-FOCUS CENTER TEXT (Positioned right above the CHIRPS ring & cricket!) */}
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
                top: 324,
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
                    "6px 6px 0 #0B0D1E, -4px -4px 0 #0B0D1E, 4px -4px 0 #0B0D1E, -4px 4px 0 #0B0D1E",
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
                      "6px 6px 0 #0B0D1E, -4px -4px 0 #0B0D1E, 4px -4px 0 #0B0D1E, -4px 4px 0 #0B0D1E",
                    textAlign: "center",
                    lineHeight: 1.25,
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
