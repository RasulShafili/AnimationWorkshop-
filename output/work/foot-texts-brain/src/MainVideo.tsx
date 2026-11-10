import React, { useRef, useEffect } from "react";
import { useCurrentFrame, staticFile, Audio } from "remotion";
import "@fontsource/press-start-2p";

import timingData from "./timing.json";
import {
  drawNeuralBackdrop,
  drawNervePipelines,
  drawCuteFoot,
  drawWeightAndRadar
} from "./pixelEngine";

export const MainVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  let footState: "happy" | "bonked" | "confused" | "screaming" = "happy";
  if (frame >= 55 && frame < 360) {
    footState = "bonked";
  } else if (frame >= 360 && frame < 720) {
    footState = "confused";
  } else if (frame >= 720 && frame < 860) {
    footState = "screaming";
  } else if (frame >= 860) {
    footState = "bonked";
  }

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    drawNeuralBackdrop(ctx, 270, 480, frame);
    drawNervePipelines(ctx, frame);
    drawCuteFoot(ctx, frame, footState);
    drawWeightAndRadar(ctx, frame);
  }, [frame, footState]);

  // Weight position for crisp 'YOU' & '@PIXEL_FACT.8BIT' text overlay
  let wx = 130;
  let wy = 34;
  if (frame >= 35 && frame < 55) {
    const p = (frame - 35) / 20.0;
    wx = 130 + p * 18;
    wy = 34 + p * p * 256;
  } else if (frame >= 55 && frame < 78) {
    const p = (frame - 55) / 23.0;
    wx = 148 - p * 18;
    wy = 290 - p * 256;
  }

  // Digital Radar Speed display value
  let radarSpeed = "0";
  let radarColor = "#FFE600";
  if (frame >= 55 && frame < 480) {
    const ramp = Math.min(180, Math.floor(((frame - 55) / 18) * 180));
    radarSpeed = String(ramp);
    radarColor = "#FFE600";
  } else if (frame >= 480 && frame < 720) {
    radarSpeed = "2";
    radarColor = "#FF5252";
  } else if (frame >= 720) {
    radarSpeed = "180";
    radarColor = "#FFE600";
  }

  // Single-Focus Center Text Beat (positioned right above the central nerve highway!)
  const activeCenterText = (timingData.bubbles as any[]).find(
    (b) => frame >= b.startFrame && frame < b.endFrame
  );

  let shownLine1 = "";
  let shownLine2 = "";
  if (activeCenterText) {
    const age = frame - activeCenterText.startFrame;
    const totalChars = activeCenterText.line1.length + activeCenterText.line2.length;
    const visible = Math.floor(
      totalChars * Math.min(1.0, age / Math.max(1, activeCenterText.typeFrames))
    );
    shownLine1 = activeCenterText.line1.slice(0, Math.min(visible, activeCenterText.line1.length));
    if (visible > activeCenterText.line1.length) {
      shownLine2 = activeCenterText.line2.slice(0, visible - activeCenterText.line1.length);
    }
  }

  return (
    <div
      style={{
        position: "relative",
        width: 1080,
        height: 1920,
        backgroundColor: "#191E48",
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

      {/* Crisp 'YOU' & '@PIXEL_FACT.8BIT' Etched on the Falling Iron Weight */}
      <div
        style={{
          position: "absolute",
          left: Math.floor((wx - 36) * 4),
          top: Math.floor((wy + 8) * 4),
          width: 288,
          textAlign: "center",
          pointerEvents: "none",
          zIndex: 25
        }}
      >
        <div
          style={{
            fontSize: "42px",
            color: "#D2DAE2",
            textShadow: "-3px -3px 0 #1E272E, 3px 3px 0 #1E272E"
          }}
        >
          YOU
        </div>
        <div
          style={{
            fontSize: "13px",
            color: "#A4B0BE",
            marginTop: "22px",
            letterSpacing: "1px"
          }}
        >
          LEARN WITH 8-BIT
        </div>
      </div>

      {/* Digital LED Radar Speed Sign on Right Pole (YOUR SPEED: 180 KM/H) */}
      <div
        style={{
          position: "absolute",
          left: 716,
          top: 936,
          width: 236,
          backgroundColor: "#0D1124",
          border: "6px solid #2F3542",
          boxShadow: "0 0 0 4px #070914, 10px 10px 0 rgba(0,0,0,0.6)",
          padding: "14px 10px",
          textAlign: "center",
          zIndex: 30
        }}
      >
        <div style={{ fontSize: "16px", color: "#FFFFFF", marginBottom: "12px" }}>
          YOUR SPEED
        </div>
        <div
          style={{
            fontSize: "48px",
            color: radarColor,
            textShadow: `0 0 12px ${radarColor}, 3px 3px 0 #000`,
            letterSpacing: "2px",
            marginBottom: "10px"
          }}
        >
          {radarSpeed}
        </div>
        <div style={{ fontSize: "18px", color: "#FDCB6E" }}>KM/H</div>
      </div>

      {/* SINGLE-FOCUS CENTER TEXT (Right near the central nerve pipeline & foot action!) */}
      {activeCenterText && (
        <div
          style={{
            position: "absolute",
            top: 430,
            left: 32,
            right: 32,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            pointerEvents: "none",
            zIndex: 40,
            textAlign: "center"
          }}
        >
          <div
            style={{
              fontSize: "44px",
              lineHeight: 1.35,
              color:
                activeCenterText.highlightLine === 1
                  ? activeCenterText.highlightColor || "#FFE600"
                  : "#FFFFFF",
              textShadow:
                "-5px -5px 0 #0B0E24, 5px -5px 0 #0B0E24, -5px 5px 0 #0B0E24, 5px 5px 0 #0B0E24, 0 8px 0 #0B0E24"
            }}
          >
            {shownLine1}
          </div>
          {shownLine2 && (
            <div
              style={{
                fontSize: "48px",
                lineHeight: 1.35,
                marginTop: "14px",
                color:
                  activeCenterText.highlightLine === 2
                    ? activeCenterText.highlightColor || "#FFE600"
                    : "#FFFFFF",
                textShadow:
                  "-5px -5px 0 #0B0E24, 5px -5px 0 #0B0E24, -5px 5px 0 #0B0E24, 5px 5px 0 #0B0E24, 0 8px 0 #0B0E24"
              }}
            >
              {shownLine2}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
