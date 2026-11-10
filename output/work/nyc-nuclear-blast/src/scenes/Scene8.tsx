import React from "react";
import { AbsoluteFill, useCurrentFrame, spring, useVideoConfig, interpolate } from "remotion";
import { HUDHeader } from "../components/HUDHeader";
import { theme } from "../theme";

export const Scene8: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pop = spring({
    frame,
    fps,
    config: theme.spring.smooth
  });

  const translateY = interpolate(pop, [0, 1], [30, 0]);
  const opacity = interpolate(pop, [0, 1], [0, 1]);

  const blink = frame % 24 < 12;

  const pollOptions = [
    { key: "A", text: "DEEPEST SUBWAY (30M DOWN)", desc: "Shields radiation, but carbon monoxide risk" },
    { key: "B", text: "HUDSON RIVER UNDERWATER", desc: "Thermal shockwave boil & pressure wave" },
    { key: "C", text: "UPPER MANHATTAN (OUTSIDE 10KM)", desc: "Escape thermal flash, beware fallout plume" }
  ];

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <HUDHeader
        badge="PIXEL FACT ARCHIVE"
        title="SURVIVAL SCENARIO"
        metrics={[
          { label: "TARGET CHANNEL", value: "@pixel_fact.8bit" },
          { label: "TOPIC", value: "NUCLEAR BLAST PHYSICS" },
          { label: "STATUS", value: "COMMUNITY DEBATE" }
        ]}
      />

      <div
        style={{
          position: "absolute",
          top: 360,
          left: 48,
          right: 48,
          opacity,
          transform: `translateY(${translateY}px)`,
          display: "flex",
          flexDirection: "column",
          gap: 22,
          zIndex: 30
        }}
      >
        {/* Main Question Card */}
        <div
          style={{
            background: "rgba(8, 20, 40, 0.92)",
            border: "2px solid #ef4444",
            boxShadow: "0 0 40px rgba(239, 68, 68, 0.4)",
            borderRadius: 20,
            padding: "24px 28px",
            textAlign: "center"
          }}
        >
          <span
            style={{
              fontFamily: theme.fonts.mono,
              fontSize: 16,
              color: "#f87171",
              letterSpacing: "0.15em",
              textTransform: "uppercase",
              display: "block",
              marginBottom: 8
            }}
          >
            THE ULTIMATE SURVIVAL QUESTION
          </span>
          <span
            style={{
              fontFamily: theme.fonts.display,
              fontSize: 30,
              fontWeight: 800,
              color: "#ffffff",
              lineHeight: 1.2
            }}
          >
            WHERE WOULD YOU HIDE TO SURVIVE?
          </span>
        </div>

        {/* Poll Options */}
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          {pollOptions.map((opt, i) => {
            const optSpring = spring({
              frame: frame - i * 6,
              fps,
              config: theme.spring.snappy
            });
            const optY = interpolate(optSpring, [0, 1], [20, 0]);
            const optOp = interpolate(optSpring, [0, 1], [0, 1]);

            return (
              <div
                key={opt.key}
                style={{
                  opacity: optOp,
                  transform: `translateY(${optY}px)`,
                  background: "rgba(15, 23, 42, 0.94)",
                  border: "1px solid rgba(239, 68, 68, 0.35)",
                  borderRadius: 16,
                  padding: "18px 22px",
                  display: "flex",
                  alignItems: "center",
                  gap: 18
                }}
              >
                <div
                  style={{
                    width: 48,
                    height: 48,
                    borderRadius: 12,
                    background: i === 0 ? "#10b981" : "#0284c7",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    fontFamily: theme.fonts.mono,
                    fontWeight: 800,
                    fontSize: 24,
                    color: "#ffffff"
                  }}
                >
                  {opt.key}
                </div>
                <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
                  <span
                    style={{
                      fontFamily: theme.fonts.display,
                      fontSize: 20,
                      fontWeight: 700,
                      color: "#f8fafc"
                    }}
                  >
                    {opt.text}
                  </span>
                  <span
                    style={{
                      fontFamily: theme.fonts.mono,
                      fontSize: 13,
                      color: theme.colors.textMuted
                    }}
                  >
                    {opt.desc}
                  </span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Call to Action Bar */}
        <div
          style={{
            background: "rgba(239, 68, 68, 0.14)",
            border: "2px dashed #ef4444",
            borderRadius: 16,
            padding: "18px 24px",
            textAlign: "center"
          }}
        >
          <span
            style={{
              fontFamily: theme.fonts.mono,
              fontSize: 19,
              fontWeight: 800,
              color: blink ? "#f87171" : "#ffffff",
              letterSpacing: "0.08em"
            }}
          >
            COMMENT YOUR CHOICE (A, B, OR C) BELOW! 👇
          </span>
        </div>

        {/* Channel Branding Badge */}
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            gap: 12,
            marginTop: 4
          }}
        >
          <div
            style={{
              padding: "12px 24px",
              background: "rgba(3, 8, 20, 0.88)",
              border: "1px solid rgba(255, 255, 255, 0.2)",
              borderRadius: 30,
              display: "flex",
              alignItems: "center",
              gap: 12
            }}
          >
            <span
              style={{
                fontFamily: theme.fonts.mono,
                fontSize: 16,
                fontWeight: 700,
                color: "#facc15"
              }}
            >
              @pixel_fact.8bit
            </span>
            <span style={{ color: "rgba(255, 255, 255, 0.3)" }}>•</span>
            <span
              style={{
                fontFamily: theme.fonts.mono,
                fontSize: 15,
                color: "#94a3b8"
              }}
            >
              Follow for Daily 8-Bit Science
            </span>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
