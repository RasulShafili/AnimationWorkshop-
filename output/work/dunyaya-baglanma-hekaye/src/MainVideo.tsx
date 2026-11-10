import React, { useEffect, useRef } from "react";
import {
  AbsoluteFill,
  Audio,
  staticFile,
  useCurrentFrame,
} from "remotion";
import timingData from "./timing.json";
import {
  PW,
  PH,
  drawIslamicOasisBackdrop,
  drawOasisTreeAndTravelers,
  drawHourglassOfLife,
} from "./pixelEngine";
import { PixelTextAz } from "./pixelFontAz";

export const MainVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.imageSmoothingEnabled = false;

    // 1. Starry Desert Twilight Sky, Crescent Moon (Hilal), Distant Masjid & Dunes
    drawIslamicOasisBackdrop(ctx, frame);

    // 2. Oasis Shade Tree, Wise Traveler, Greedy Traveler & Transforming Dunya Gold
    drawOasisTreeAndTravelers(ctx, frame, );

    // 3. Ornate Hourglass of Life ("ÖMÜR SAATI")
    drawHourglassOfLife(ctx, frame);
  }, [frame]);

  // Remaining life sand percentage (100% -> 0% at Frame 550)
  const sandPercent = Math.max(0, Math.round((1 - frame / 550) * 100));

  // Camera rumble when the Hourglass hits 0% and Gold crumbles to dust at Frame 550!
  let shakeX = 0;
  let shakeY = 0;
  if (frame >= 550 && frame <= 568) {
    const decay = (569 - frame) / 19;
    shakeX = Math.round(Math.sin(frame * 2.7) * 14 * decay);
    shakeY = Math.round(Math.cos(frame * 3.1) * 14 * decay);
  }

  const activeBanners = timingData.bubbles.filter(
    (b: any) =>
      b.type === "top_banner" && frame >= b.startFrame && frame <= b.endFrame
  );
  const activeBoxes = timingData.bubbles.filter(
    (b: any) =>
      b.type !== "top_banner" && frame >= b.startFrame && frame <= b.endFrame
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0E152B",
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

        {/* Subtle Channel Watermark on Desert Dune */}
        <div
          style={{
            position: "absolute",
            left: 56,
            top: 1090,
            opacity: 0.55,
            pointerEvents: "none",
          }}
        >
          <PixelTextAz
            text="PIXEL-FACT.8BIT"
            pixelSize={3}
            color="#FFE082"
            shadowColor="#2A1608"
          />
        </div>

        {/* Hourglass Status HUD Bar at Bottom ("ÖMÜR QUMU" & "ƏBƏDİ QAZANC") */}
        <div
          style={{
            position: "absolute",
            left: 56,
            right: 56,
            top: 1545,
            backgroundColor: "#141A2E",
            border: "6px solid #FFE082",
            boxShadow: "10px 10px 0 #090C16",
            padding: "18px 22px",
            display: "flex",
            flexDirection: "column",
            gap: 14,
            pointerEvents: "none",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <PixelTextAz
              text={
                frame >= 720
                  ? "QALAN MİRAS: SALEH ƏMƏL"
                  : `ÖMÜR QUMU: ${sandPercent}%`
              }
              pixelSize={3.5}
              color={
                frame >= 720
                  ? "#55EFC4"
                  : sandPercent === 0
                  ? "#FF5252"
                  : "#FFE082"
              }
              shadowColor="#090C16"
            />
            <PixelTextAz
              text={
                frame >= 550 ? "DÜNYA MALI: KÜL" : "DÜNYA MALI: QIZIL"
              }
              pixelSize={3.5}
              color={frame >= 550 ? "#90A4AE" : "#FFD54F"}
              shadowColor="#090C16"
            />
          </div>

          <div
            style={{
              width: "100%",
              height: 24,
              backgroundColor: "#090C16",
              border: "4px solid #323E64",
              padding: 3,
            }}
          >
            <div
              style={{
                width: `${frame >= 720 ? 100 : sandPercent}%`,
                height: "100%",
                backgroundColor:
                  frame >= 720
                    ? "#55EFC4"
                    : sandPercent > 25
                    ? "#FFD54F"
                    : "#FF5252",
              }}
            />
          </div>
        </div>

        {/* 1. TOP HOOK HEADLINES IN AZERBAIJANI (8-Bit Pixel Bitmap Reveal!) */}
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

          return (
            <div
              key={banner.id}
              style={{
                position: "absolute",
                top: 236,
                left: 24,
                right: 24,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 20,
                pointerEvents: "none",
              }}
            >
              {s1.length > 0 && (
                <PixelTextAz
                  text={s1}
                  pixelSize={8}
                  color={banner.highlightLine === 1 ? "#FFD54F" : "#FFFFFF"}
                  outlineColor="#0B0E1D"
                />
              )}
              {s2.length > 0 && (
                <PixelTextAz
                  text={s2}
                  pixelSize={8}
                  color={banner.highlightLine === 2 ? "#FFD54F" : "#FFFFFF"}
                  outlineColor="#0B0E1D"
                />
              )}
            </div>
          );
        })}

        {/* 2. PACED SPATIAL RPG SPEECH BUBBLES IN AZERBAIJANI */}
        {activeBoxes.map((box: any) => {
          const elapsed = frame - box.startFrame;
          if (elapsed < 2) return null;

          const popScale = elapsed < 5 ? 0.92 : 1.0;
          const progress = Math.min(1, elapsed / box.typeFrames);
          const fullText: string = box.text;
          const revealedChars = Math.floor(fullText.length * progress);
          const visibleText = fullText.slice(0, revealedChars);
          const lines = visibleText.split("\n");

          const isLightBg = box.color === "#FFF8E7";
          const textColor = isLightBg ? "#12121C" : "#FFFFFF";

          const leftPx = box.x * 4;
          const topPx = box.y * 4;
          const widthPx = box.w * 4;
          const minHeightPx = box.h * 4;

          return (
            <div
              key={box.id}
              style={{
                position: "absolute",
                left: leftPx,
                top: topPx,
                width: widthPx,
                minHeight: minHeightPx,
                backgroundColor: box.color,
                border: `6px solid ${box.borderColor}`,
                boxShadow: "10px 10px 0 #090C16, 0 0 0 4px #090C16",
                padding: "30px 24px 20px 24px",
                transform: `scale(${popScale})`,
                transformOrigin: "center top",
                pointerEvents: "none",
                zIndex: 20,
              }}
            >
              {/* Speaker Name Tag */}
              {box.speaker && (
                <div
                  style={{
                    position: "absolute",
                    top: -22,
                    left: 16,
                    backgroundColor: box.borderColor,
                    border: "4px solid #090C16",
                    padding: "6px 12px",
                  }}
                >
                  <PixelTextAz
                    text={box.speaker}
                    pixelSize={3.2}
                    color="#090C16"
                  />
                </div>
              )}

              {/* Typewriter Dialog Lines in Azerbaijani */}
              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  gap: 14,
                }}
              >
                {lines.map((line: string, idx: number) => (
                  <div
                    key={idx}
                    style={{
                      display: "flex",
                      alignItems: "center",
                    }}
                  >
                    {line.length > 0 && (
                      <PixelTextAz
                        text={line}
                        pixelSize={4.5}
                        color={textColor}
                        shadowColor={isLightBg ? undefined : "#090C16"}
                      />
                    )}
                    {idx === lines.length - 1 &&
                      progress < 1 &&
                      frame % 4 < 2 && (
                        <span
                          style={{
                            display: "inline-block",
                            width: 14,
                            height: 26,
                            backgroundColor: box.borderColor,
                            marginLeft: 8,
                          }}
                        />
                      )}
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      <Audio src={staticFile("mix.wav")} />
    </AbsoluteFill>
  );
};
