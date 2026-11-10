import React, { useRef, useEffect } from "react";
import { useCurrentFrame, staticFile, Audio } from "remotion";
import "@fontsource/press-start-2p";

import timingData from "./timing.json";
import {
  drawAnatomicalBackdrop,
  drawDetailedSynovialCapsule,
  drawDetailedBones,
  drawCavitationPhysics,
  BubbleEvent
} from "./pixelEngine";

export const MainVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Continuous joint stretch curve across 840 frames:
  let stretchPx = 0;
  if (frame < 175) {
    stretchPx = Math.sin(frame * 0.08) * 1.5;
  } else if (frame < 320) {
    const p = (frame - 175) / 145.0;
    stretchPx = p * 38.0;
  } else if (frame < 480) {
    const tremor = frame > 430 ? Math.sin(frame * 1.6) * 2.0 : Math.sin(frame * 0.4) * 0.8;
    stretchPx = 38.0 + tremor;
  } else if (frame < 525) {
    const p = (frame - 480) / 45.0;
    stretchPx = 38.0 - p * 22.0 + Math.sin(p * Math.PI * 3) * 3.0 * (1 - p);
  } else {
    stretchPx = 14.0 + Math.sin(frame * 0.07) * 1.5;
  }

  // Facial expression state machine
  let expression: "sleepy" | "strain" | "shock" | "relief" = "sleepy";
  if (frame >= 185 && frame < 480) {
    expression = "strain";
  } else if (frame >= 480 && frame < 528) {
    expression = "shock";
  } else if (frame >= 528) {
    expression = "relief";
  }

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const cx = 135;
    const cy = 236;

    // 1. Deep navy anatomical cellular backdrop
    drawAnatomicalBackdrop(ctx, 270, 480, frame);

    // 2. Glowing orange-coral synovial capsule
    drawDetailedSynovialCapsule(ctx, cx, cy, stretchPx, frame);

    // 3. Full-height cylindrical textured finger bones with faces & watermark
    drawDetailedBones(ctx, cx, cy, stretchPx, expression, frame);

    // 4. Dissolved gas particles, bubble formation & 310ms POP shockwave (in front of joint gap!)
    drawCavitationPhysics(ctx, cx, cy, frame);
  }, [frame, stretchPx, expression]);

  // Active Top Arcade Hook Banner (Typewriter reveal, no bottom subtitles!)
  const activeTopBanner = (timingData.bubbles as any[]).find(
    (b) => b.type === "top_banner" && frame >= b.startFrame && frame < b.endFrame
  );

  let shownLine1 = "";
  let shownLine2 = "";
  if (activeTopBanner) {
    const age = frame - activeTopBanner.startFrame;
    const totalChars = activeTopBanner.line1.length + activeTopBanner.line2.length;
    const visible = Math.floor(
      totalChars * Math.min(1.0, age / Math.max(1, activeTopBanner.typeFrames))
    );
    shownLine1 = activeTopBanner.line1.slice(0, Math.min(visible, activeTopBanner.line1.length));
    if (visible > activeTopBanner.line1.length) {
      shownLine2 = activeTopBanner.line2.slice(0, visible - activeTopBanner.line1.length);
    }
  }

  // Active spatial RPG speech bubbles & callout boxes (rendered at crisp 1080p pixel grid!)
  const activeDialogBubbles = (timingData.bubbles as BubbleEvent[]).filter(
    (b) => b.type !== "top_banner" && frame >= b.startFrame && frame < b.endFrame
  );

  // Vacuum Gauge state (Frames 260..479)
  const showVacuumGauge = frame >= 260 && frame < 480;
  const dropProg = showVacuumGauge ? Math.min(1.0, (frame - 260) / 65) : 0;

  // 20-Minute Cooldown Stopwatch state (Frames 635..840)
  const showCooldownTimer = frame >= 635;
  const remSec = showCooldownTimer ? Math.max(0, 1200 - (frame - 635) * 5.8) : 1200;
  const cdMins = Math.floor(remSec / 60);
  const cdSecs = Math.floor(remSec % 60);
  const cdTimeStr = `${String(cdMins).padStart(2, "0")}:${String(cdSecs).padStart(2, "0")}`;

  return (
    <div
      style={{
        position: "relative",
        width: 1080,
        height: 1920,
        backgroundColor: "#141736",
        overflow: "hidden",
        fontFamily: "'Press Start 2P', monospace"
      }}
    >
      <Audio src={staticFile("mix.wav")} />

      <canvas
        ref={canvasRef}
        width={270}
        height={480}
        style={{
          width: "1080px",
          height: "1920px",
          imageRendering: "pixelated"
        }}
      />

      {/* Etched Bone Watermark (Moves with lower bone shaft, razor-sharp pixel font) */}
      <div
        style={{
          position: "absolute",
          top: Math.floor((236 + 8 + stretchPx * 0.55 + 95) * 4),
          left: 0,
          right: 0,
          textAlign: "center",
          fontSize: "15px",
          lineHeight: 1.4,
          color: "rgba(95, 65, 30, 0.72)",
          pointerEvents: "none",
          zIndex: 25
        }}
      >
        <div>PIXEL_FACT</div>
        <div>.8BIT</div>
      </div>

      {/* Crisp Top Arcade Hook Typography (Typewriter Reveal) */}
      {activeTopBanner && (
        <div
          style={{
            position: "absolute",
            top: 230,
            left: 0,
            right: 0,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            pointerEvents: "none",
            zIndex: 40,
            textAlign: "center",
            padding: "0 36px"
          }}
        >
          <div
            style={{
              fontSize: "38px",
              lineHeight: 1.4,
              letterSpacing: "1px",
              color: activeTopBanner.highlightLine === 1 ? "#FFE600" : "#FFFFFF",
              textShadow:
                "-4px -4px 0 #000, 4px -4px 0 #000, -4px 4px 0 #000, 4px 4px 0 #000, 0 6px 0 #000"
            }}
          >
            {shownLine1}
          </div>
          {shownLine2 && (
            <div
              style={{
                fontSize: "40px",
                lineHeight: 1.4,
                marginTop: "10px",
                letterSpacing: "1px",
                color: activeTopBanner.highlightLine === 2 ? "#FFE600" : "#FFFFFF",
                textShadow:
                  "-4px -4px 0 #000, 4px -4px 0 #000, -4px 4px 0 #000, 4px 4px 0 #000, 0 6px 0 #000"
              }}
            >
              {shownLine2}
            </div>
          )}
        </div>
      )}

      {/* Left Vacuum Pressure Barometer HUD (Frames 260..479) */}
      {showVacuumGauge && (
        <div
          style={{
            position: "absolute",
            left: 44,
            top: 740,
            width: 224,
            backgroundColor: "#161B3D",
            border: "6px solid #5CE1E6",
            boxShadow: "0 0 0 6px #0B0D1F, 12px 12px 0 rgba(0,0,0,0.65)",
            padding: "16px 14px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            zIndex: 35
          }}
        >
          <div style={{ fontSize: "18px", color: "#FFE600", marginBottom: "14px", textShadow: "2px 2px 0 #000" }}>
            PRESSURE
          </div>
          <div
            style={{
              width: 56,
              height: 170,
              backgroundColor: "#080A17",
              border: "4px solid #2C356E",
              display: "flex",
              flexDirection: "column",
              justifyContent: "flex-end",
              padding: 4
            }}
          >
            <div
              style={{
                width: "100%",
                height: `${Math.max(12, Math.floor((1.0 - dropProg * 0.86) * 100))}%`,
                backgroundColor: dropProg < 0.5 ? "#55EFC4" : dropProg < 0.8 ? "#FDCB6E" : "#FF5252"
              }}
            />
          </div>
          <div
            style={{
              fontSize: "17px",
              color: dropProg >= 0.8 ? "#FF5252" : "#A8FFFA",
              marginTop: "14px",
              textShadow: "2px 2px 0 #000"
            }}
          >
            {dropProg >= 0.8 ? "VACUUM!" : "-0.2 ATM"}
          </div>
        </div>
      )}

      {/* Left 20-Minute Cooldown Stopwatch HUD (Frames 635..840) */}
      {showCooldownTimer && (
        <div
          style={{
            position: "absolute",
            left: 40,
            top: 660,
            width: 356,
            backgroundColor: "#161B3D",
            border: "6px solid #FFE600",
            boxShadow: "0 0 0 6px #0B0D1F, 12px 12px 0 rgba(0,0,0,0.65)",
            padding: "18px 18px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            zIndex: 35
          }}
        >
          <div style={{ fontSize: "17px", color: "#5CE1E6", marginBottom: "12px", textShadow: "2px 2px 0 #000" }}>
            RECHARGE TIMER
          </div>
          <div
            style={{
              width: "100%",
              backgroundColor: "#070914",
              border: "4px solid #2B3570",
              padding: "14px 10px",
              textAlign: "center",
              fontSize: "38px",
              color: "#FFE600",
              letterSpacing: "2px"
            }}
          >
            {cdTimeStr}
          </div>
          <div style={{ fontSize: "16px", color: "#FFFFFF", marginTop: "12px", textShadow: "2px 2px 0 #000" }}>
            GAS DISSOLVING...
          </div>
        </div>
      )}

      {/* Crisp 8-Bit RPG Speech Bubbles & Callout Boxes (Paced Typewriter Reveal) */}
      {activeDialogBubbles.map((ev) => {
        const age = frame - ev.startFrame;
        const bounceY = age < 5 ? (5 - age) * 6 : 0;
        const bx = (ev.x || 14) * 4;
        const by = (ev.y || 150) * 4 + bounceY;
        const bw = (ev.w || 116) * 4;

        const bg = ev.color || "#FFF8E7";
        const border = ev.borderColor || "#FFE600";
        const isLight = bg.toUpperCase().startsWith("#FFF");
        const textColor = isLight ? "#181426" : "#FFFFFF";

        const fullText = ev.text || "";
        const charProgress = Math.min(1.0, age / Math.max(1, ev.typeFrames));
        const visibleChars = Math.floor(fullText.length * charProgress);
        const shownText = fullText.slice(0, visibleChars);
        const lines = shownText.split("\n");

        return (
          <div
            key={ev.id}
            style={{
              position: "absolute",
              left: bx,
              top: by,
              width: bw,
              backgroundColor: bg,
              border: `6px solid ${border}`,
              boxShadow: "0 0 0 6px #121020, 12px 12px 0 rgba(8, 8, 18, 0.78)",
              padding: "22px 20px 18px 20px",
              zIndex: 45,
              pointerEvents: "none"
            }}
          >
            {/* Speaker Mini-Tag */}
            {ev.speaker && (
              <div
                style={{
                  position: "absolute",
                  top: -22,
                  left: 16,
                  backgroundColor: border,
                  border: "4px solid #121020",
                  padding: "4px 10px",
                  fontSize: "15px",
                  color: "#121020",
                  fontWeight: "bold"
                }}
              >
                {ev.speaker}
              </div>
            )}

            {/* Speech Bubble Pointer Tail */}
            {ev.tailDir?.startsWith("right") && (
              <div
                style={{
                  position: "absolute",
                  right: -22,
                  top: ev.tailDir === "right_up" ? 18 : undefined,
                  bottom: ev.tailDir === "right_down" ? 18 : undefined,
                  width: 22,
                  height: 16,
                  backgroundColor: border,
                  borderTop: "4px solid #121020",
                  borderRight: "4px solid #121020",
                  borderBottom: "4px solid #121020"
                }}
              />
            )}
            {ev.tailDir?.startsWith("left") && (
              <div
                style={{
                  position: "absolute",
                  left: -22,
                  top: ev.tailDir === "left_up" ? 18 : undefined,
                  bottom: ev.tailDir === "left_down" ? 18 : undefined,
                  width: 22,
                  height: 16,
                  backgroundColor: border,
                  borderTop: "4px solid #121020",
                  borderLeft: "4px solid #121020",
                  borderBottom: "4px solid #121020"
                }}
              />
            )}

            {/* Typewriter Lines */}
            {lines.map((line, lIdx) => (
              <div
                key={lIdx}
                style={{
                  fontSize: "21px",
                  lineHeight: 1.55,
                  color: textColor,
                  textShadow: isLight ? "none" : "2px 2px 0 #000",
                  whiteSpace: "pre-wrap"
                }}
              >
                {line}
              </div>
            ))}
          </div>
        );
      })}
    </div>
  );
};
