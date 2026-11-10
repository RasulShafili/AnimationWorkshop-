import React from "react";
import { useCurrentFrame, staticFile, Audio, Sequence } from "remotion";
import "@fontsource/press-start-2p";

import timingData from "./timing.json";
import captionsData from "./captions.json";

import { Scene1 } from "./scenes/Scene1";
import { Scene2 } from "./scenes/Scene2";
import { Scene3 } from "./scenes/Scene3";
import { Scene4 } from "./scenes/Scene4";
import { Scene5 } from "./scenes/Scene5";

export const MainVideo: React.FC = () => {
  const frame = useCurrentFrame();

  const activeScene = timingData.scenes.find(
    (s) => frame >= s.startFrame && frame < s.endFrame
  ) || timingData.scenes[0];

  const activeCaption = captionsData.find(
    (c) => frame >= c.startFrame && frame < c.endFrame
  );

  return (
    <div
      style={{
        position: "relative",
        width: 1080,
        height: 1920,
        backgroundColor: "#1a182e",
        overflow: "hidden",
        fontFamily: "'Press Start 2P', monospace"
      }}
    >
      <Audio src={staticFile("mix.wav")} />

      <Sequence from={timingData.scenes[0].startFrame} durationInFrames={timingData.scenes[0].endFrame - timingData.scenes[0].startFrame}>
        <Scene1 startFrame={timingData.scenes[0].startFrame} endFrame={timingData.scenes[0].endFrame} globalFrame={frame} />
      </Sequence>

      <Sequence from={timingData.scenes[1].startFrame} durationInFrames={timingData.scenes[1].endFrame - timingData.scenes[1].startFrame}>
        <Scene2 startFrame={timingData.scenes[1].startFrame} endFrame={timingData.scenes[1].endFrame} globalFrame={frame} />
      </Sequence>

      <Sequence from={timingData.scenes[2].startFrame} durationInFrames={timingData.scenes[2].endFrame - timingData.scenes[2].startFrame}>
        <Scene3 startFrame={timingData.scenes[2].startFrame} endFrame={timingData.scenes[2].endFrame} globalFrame={frame} />
      </Sequence>

      <Sequence from={timingData.scenes[3].startFrame} durationInFrames={timingData.scenes[3].endFrame - timingData.scenes[3].startFrame}>
        <Scene4 startFrame={timingData.scenes[3].startFrame} endFrame={timingData.scenes[3].endFrame} globalFrame={frame} />
      </Sequence>

      <Sequence from={timingData.scenes[4].startFrame} durationInFrames={timingData.scenes[4].endFrame - timingData.scenes[4].startFrame}>
        <Scene5 startFrame={timingData.scenes[4].startFrame} endFrame={timingData.scenes[4].endFrame} globalFrame={frame} />
      </Sequence>

      {/* Top Arcade Hook Banner (Exact @science_in_8bit typography) */}
      <div
        style={{
          position: "absolute",
          top: 190,
          left: 0,
          right: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          pointerEvents: "none",
          zIndex: 50,
          textAlign: "center",
          padding: "0 30px"
        }}
      >
        <div
          style={{
            fontSize: "40px",
            lineHeight: 1.45,
            letterSpacing: "1px",
            color: "#FFFFFF",
            textShadow:
              "-4px -4px 0 #000, 4px -4px 0 #000, -4px 4px 0 #000, 4px 4px 0 #000, 0 6px 0 #000, 0 8px 16px rgba(0,0,0,0.85)"
          }}
        >
          {activeScene.id === "scene1" && (
            <>
              <div>YOU MAKE</div>
              <div style={{ color: "#FFE600" }}>1 LITRE</div>
              <div style={{ fontSize: "32px", marginTop: "8px" }}>OF SPIT EVERY DAY</div>
            </>
          )}
          {activeScene.id === "scene2" && (
            <>
              <div>ENOUGH TO FILL</div>
              <div style={{ color: "#FFE600" }}>A FULL BOTTLE!</div>
            </>
          )}
          {activeScene.id === "scene3" && (
            <>
              <div style={{ color: "#FFE600" }}>25,000 LITRES</div>
              <div style={{ fontSize: "30px", marginTop: "8px" }}>IN A LIFETIME!</div>
            </>
          )}
          {activeScene.id === "scene4" && (
            <>
              <div>NO SALIVA =</div>
              <div style={{ color: "#FFE600" }}>NO TASTE!</div>
            </>
          )}
          {activeScene.id === "scene5" && (
            <>
              <div>ENOUGH TO</div>
              <div style={{ color: "#FFE600" }}>FILL THIS?</div>
            </>
          )}
        </div>
      </div>

      {/* Glassmorphic Subtitle Pill (Safe Zone bottom: 220px) */}
      {activeCaption && (
        <div
          style={{
            position: "absolute",
            bottom: 220,
            left: 0,
            right: 0,
            display: "flex",
            justifyContent: "center",
            pointerEvents: "none",
            zIndex: 60,
            padding: "0 30px"
          }}
        >
          <div
            style={{
              backgroundColor: "rgba(14, 13, 24, 0.9)",
              border: "3px solid #ffe600",
              borderRadius: "14px",
              padding: "16px 28px",
              boxShadow: "0 10px 24px rgba(0,0,0,0.85)",
              maxWidth: "880px",
              textAlign: "center"
            }}
          >
            <div
              style={{
                fontSize: "26px",
                lineHeight: 1.5,
                color: "#FFFFFF",
                letterSpacing: "0.5px",
                textShadow: "-2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000"
              }}
            >
              {activeCaption.words.map((w: { word: string; frame: number }, i: number) => {
                const isSpoken = frame >= w.frame;
                return (
                  <span
                    key={i}
                    style={{
                      color: isSpoken ? "#FFE600" : "#D0D6E6",
                      marginRight: "10px"
                    }}
                  >
                    {w.word}
                  </span>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
