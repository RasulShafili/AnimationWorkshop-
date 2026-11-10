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
  drawKitchenScene,
  drawSugarAndFly,
  drawGreenSwatter,
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

    // 1. Kitchen Wallpaper, Sleepy Wall Clock, Spice Jars, Night Window, Wooden Plank Table & Pink Sugar Box
    drawKitchenScene(ctx, frame);

    // 2. White Granulated Sugar Cube & Detailed Housefly (with Supersonic Dodge!)
    drawSugarAndFly(ctx, frame);

    // 3. Giant Green Mesh Fly-Swatter with Big Goofy Eyes (Moving in Slow-Motion!)
    drawGreenSwatter(ctx, frame);
  }, [frame]);

  // Camera shake when the swatter finally smacks the table at Frame 620!
  let shakeX = 0;
  let shakeY = 0;
  if (frame >= 620 && frame <= 638) {
    const decay = (639 - frame) / 19;
    shakeX = Math.round(Math.sin(frame * 2.8) * 14 * decay);
    shakeY = Math.round(Math.cos(frame * 3.2) * 14 * decay);
  }

  // Single-Focus Center Text Beat (Positioned right below the central sugar cube & fly!)
  const activeBanners = timingData.bubbles.filter(
    (b: any) => frame >= b.startFrame && frame < b.endFrame
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#1E265E",
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

        {/* Sleepy Wall Clock "Z" (Matches Reference!) */}
        <div
          style={{
            position: "absolute",
            left: 178,
            top: 204 - (frame % 30),
            fontFamily: FONT_PIXEL,
            fontSize: 18,
            color: "rgba(210, 225, 255, 0.75)",
            pointerEvents: "none",
          }}
        >
          Z
        </div>

        {/* Pink Sugar Box Label & @PIXEL_FACT.8BIT Watermark (Matches Reference!) */}
        <div
          style={{
            position: "absolute",
            left: 6,
            top: 538,
            fontFamily: FONT_PIXEL,
            fontSize: 38,
            color: "#BC427C",
            pointerEvents: "none",
          }}
        >
          R
        </div>
        <div
          style={{
            position: "absolute",
            left: 6,
            top: 632,
            fontFamily: FONT_PIXEL,
            fontSize: 14,
            color: "rgba(255, 225, 240, 0.85)",
            lineHeight: 1.5,
            pointerEvents: "none",
          }}
        >
          LEARN
          <br />
          8-BIT
        </div>

        {/* Subtle Channel Watermark on Wooden Table */}
        <div
          style={{
            position: "absolute",
            left: 36,
            top: 1760,
            fontFamily: FONT_PIXEL,
            fontSize: 16,
            color: "rgba(255, 235, 210, 0.45)",
            textShadow: "2px 2px 0 #22140B",
            letterSpacing: "1px",
            pointerEvents: "none",
          }}
        >
          LEARN WITH 8-BIT
        </div>

        {/* SINGLE-FOCUS CENTER TEXT (Positioned right below the sugar cube & fly in the center of the table!) */}
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
                top: 1276,
                left: 32,
                right: 32,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 18,
                pointerEvents: "none",
                zIndex: 30,
              }}
            >
              <div
                style={{
                  fontFamily: FONT_PIXEL,
                  fontSize: 42,
                  color: banner.highlightLine === 1 ? hiColor : "#FFFFFF",
                  textShadow:
                    "6px 6px 0 #120B06, -4px -4px 0 #120B06, 4px -4px 0 #120B06, -4px 4px 0 #120B06",
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
                    fontSize: 44,
                    color: banner.highlightLine === 2 ? hiColor : "#FFFFFF",
                    textShadow:
                      "6px 6px 0 #120B06, -4px -4px 0 #120B06, 4px -4px 0 #120B06, -4px 4px 0 #120B06",
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
