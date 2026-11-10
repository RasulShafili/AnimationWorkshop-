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
    { key: "A", text: "DEEP UNDERGROUND BUNKER", desc: "Crushed by M12 fault displacement" },
    { key: "B", text: "FLYING IN HIGH-ALTITUDE JET", desc: "Survives initial wind, air turbulence" },
    { key: "C", text: "STANDING AT THE NORTH POLE", desc: "Near-zero rotational inertia (~0 km/h)" }
  ];

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <HUDHeader
        badge="PIXEL FACT ARCHIVE"
        title="SURVIVAL DEBATE"
        metrics={[
          { label: "TARGET CHANNEL", value: "@pixel_fact.8bit" },
          { label: "TOPIC", value: "PLANETARY PHYSICS" },
          { label: "STATUS", value: "COMMUNITY POLL ACTIVE" }
        ]}
      />

      <div
        style={{
          position: "absolute",
          top: 380,
          left: 48,
          right: 48,
          opacity,
          transform: `translateY(${translateY}px)`,
          display: "flex",
          flexDirection: "column",
          gap: 24,
          zIndex: 30
        }}
      >
        {/* Main Question Card */}
        <div
          style={{
            background: "rgba(8, 20, 40, 0.92)",
            border: "2px solid #22d3ee",
            boxShadow: "0 0 40px rgba(34, 211, 238, 0.4)",
            borderRadius: 20,
            padding: "26px 30px",
            textAlign: "center"
          }}
        >
          <span
            style={{
              fontFamily: theme.fonts.mono,
              fontSize: 16,
              color: "#38bdf8",
              letterSpacing: "0.15em",
              textTransform: "uppercase",
              display: "block",
              marginBottom: 10
            }}
          >
            THE ULTIMATE SURVIVAL QUESTION
          </span>
          <span
            style={{
              fontFamily: theme.fonts.display,
              fontSize: 32,
              fontWeight: 800,
              color: "#ffffff",
              lineHeight: 1.25
            }}
          >
            WHERE WOULD YOU SURVIVE THAT 1 SECOND?
          </span>
        </div>

        {/* Poll Options */}
        <div style={{ display: "flex", flexDirection: "column", gap: 18 }}>
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
                  border: "1px solid rgba(56, 189, 248, 0.35)",
                  borderRadius: 16,
                  padding: "20px 24px",
                  display: "flex",
                  alignItems: "center",
                  gap: 20
                }}
              >
                <div
                  style={{
                    width: 52,
                    height: 52,
                    borderRadius: 12,
                    background: i === 2 ? "#10b981" : "#0284c7",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    fontFamily: theme.fonts.mono,
                    fontWeight: 800,
                    fontSize: 26,
                    color: "#ffffff"
                  }}
                >
                  {opt.key}
                </div>
                <div style={{ display: "flex", flexDirection: "column", gap: 3 }}>
                  <span
                    style={{
                      fontFamily: theme.fonts.display,
                      fontSize: 22,
                      fontWeight: 700,
                      color: "#f8fafc"
                    }}
                  >
                    {opt.text}
                  </span>
                  <span
                    style={{
                      fontFamily: theme.fonts.mono,
                      fontSize: 14,
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
            background: "rgba(34, 211, 238, 0.14)",
            border: "2px dashed #22d3ee",
            borderRadius: 16,
            padding: "20px 24px",
            textAlign: "center"
          }}
        >
          <span
            style={{
              fontFamily: theme.fonts.mono,
              fontSize: 20,
              fontWeight: 800,
              color: blink ? "#22d3ee" : "#ffffff",
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
