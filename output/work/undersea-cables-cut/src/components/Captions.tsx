import React from "react";
import { useCurrentFrame, spring, useVideoConfig, interpolate } from "remotion";
import { theme } from "../theme";
import rawCaptions from "../captions.json";

export interface CaptionEntry {
  text: string;
  highlight: string;
  start: number;
  end: number;
  startFrame: number;
  endFrame: number;
}

export const CAPTIONS: CaptionEntry[] = rawCaptions as CaptionEntry[];

export const Captions: React.FC = () => {
  const globalFrame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const currentCap = CAPTIONS.find(
    c => globalFrame >= c.startFrame && globalFrame <= c.endFrame
  );

  if (!currentCap) return null;

  const age = globalFrame - currentCap.startFrame;
  const pop = spring({
    frame: age,
    fps,
    config: { damping: 14, stiffness: 180, mass: 0.5 }
  });

  const scale = interpolate(pop, [0, 1], [0.92, 1]);
  const translateY = interpolate(pop, [0, 1], [15, 0]);
  const opacity = interpolate(pop, [0, 1], [0, 1]);

  const words = currentCap.text.split(" ");
  const cleanHighlight = currentCap.highlight.toLowerCase().replace(/[^\w]/g, "");

  return (
    <div
      style={{
        position: "absolute",
        bottom: 220,
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        pointerEvents: "none",
        zIndex: 50,
        transform: `translateY(${translateY}px) scale(${scale})`,
        opacity
      }}
    >
      <div
        style={{
          background: "rgba(3, 8, 20, 0.88)",
          backdropFilter: "blur(18px)",
          border: `1.5px solid rgba(34, 211, 238, 0.45)`,
          boxShadow: `0 18px 48px -12px rgba(0, 0, 0, 0.8), 0 0 30px rgba(34, 211, 238, 0.25)`,
          borderRadius: 9999,
          padding: "16px 36px",
          display: "flex",
          alignItems: "center",
          gap: 14,
          maxWidth: 960
        }}
      >
        {words.map((w, idx) => {
          const cleanWord = w.toLowerCase().replace(/[^\w]/g, "");
          const isHighlighted =
            cleanWord === cleanHighlight ||
            cleanWord.includes(cleanHighlight) ||
            cleanHighlight.includes(cleanWord);

          return (
            <span
              key={idx}
              style={{
                fontFamily: theme.fonts.display,
                fontSize: 42,
                fontWeight: isHighlighted ? 900 : 700,
                letterSpacing: "-0.01em",
                color: isHighlighted ? theme.colors.accentGold : theme.colors.textWhite,
                textShadow: isHighlighted
                  ? `0 0 24px ${theme.colors.accentGoldGlow}, 0 2px 4px rgba(0,0,0,0.8)`
                  : "0 2px 6px rgba(0,0,0,0.9)",
                display: "inline-block"
              }}
            >
              {w}
            </span>
          );
        })}
      </div>
    </div>
  );
};
