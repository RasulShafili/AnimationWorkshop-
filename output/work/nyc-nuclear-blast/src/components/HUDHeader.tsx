import React from "react";
import { useCurrentFrame, spring, useVideoConfig, interpolate } from "remotion";
import { theme } from "../theme";

interface HUDHeaderProps {
  badge: string;
  title: string;
  metrics: { label: string; value: string; alert?: boolean }[];
  alert?: boolean;
}

export const HUDHeader: React.FC<HUDHeaderProps> = ({
  badge,
  title,
  metrics,
  alert = false
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: theme.spring.smooth
  });

  const opacity = entrance;
  const translateY = interpolate(entrance, [0, 1], [-25, 0]);

  const blink = frame % 24 < 12;
  const statusColor = alert ? theme.colors.alertRed : theme.colors.heroCyan;

  return (
    <div
      style={{
        position: "absolute",
        top: 80,
        left: 48,
        right: 48,
        opacity,
        transform: `translateY(${translateY}px)`,
        zIndex: 20
      }}
    >
      {/* Glass card container */}
      <div
        style={{
          background: "rgba(8, 18, 36, 0.75)",
          backdropFilter: "blur(16px)",
          borderRadius: 20,
          border: `1px solid ${alert ? "rgba(239, 68, 68, 0.35)" : "rgba(34, 211, 238, 0.25)"}`,
          boxShadow: `0 16px 40px -10px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.08)`,
          padding: "20px 24px"
        }}
      >
        {/* Top bar with badge and live status */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            marginBottom: 10
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 10
            }}
          >
            <div
              style={{
                width: 10,
                height: 10,
                borderRadius: "50%",
                backgroundColor: statusColor,
                boxShadow: `0 0 12px ${statusColor}`,
                opacity: alert ? (blink ? 1 : 0.3) : 1
              }}
            />
            <span
              style={{
                fontFamily: theme.fonts.mono,
                fontSize: 18,
                letterSpacing: "0.12em",
                textTransform: "uppercase",
                fontWeight: 700,
                color: statusColor
              }}
            >
              {badge}
            </span>
          </div>

          <span
            style={{
              fontFamily: theme.fonts.mono,
              fontSize: 16,
              color: theme.colors.textMuted,
              letterSpacing: "0.06em"
            }}
          >
            LIVE TELEMETRY
          </span>
        </div>

        {/* Title */}
        <div
          style={{
            fontFamily: theme.fonts.display,
            fontSize: 34,
            fontWeight: 800,
            letterSpacing: "-0.02em",
            color: alert ? "#fecaca" : theme.colors.textWhite,
            textShadow: alert ? `0 0 20px ${theme.colors.alertRedGlow}` : `0 0 20px ${theme.colors.heroCyanGlow}`,
            marginBottom: 14
          }}
        >
          {title}
        </div>

        {/* Metrics Grid */}
        <div
          style={{
            display: "flex",
            gap: 16,
            paddingTop: 12,
            borderTop: "1px solid rgba(255, 255, 255, 0.08)"
          }}
        >
          {metrics.map((m, i) => (
            <div
              key={i}
              style={{
                flex: 1,
                background: "rgba(15, 23, 42, 0.5)",
                borderRadius: 10,
                padding: "8px 12px",
                border: "1px solid rgba(255, 255, 255, 0.04)"
              }}
            >
              <div
                style={{
                  fontFamily: theme.fonts.mono,
                  fontSize: 14,
                  color: theme.colors.textMuted,
                  letterSpacing: "0.05em",
                  textTransform: "uppercase",
                  marginBottom: 3
                }}
              >
                {m.label}
              </div>
              <div
                style={{
                  fontFamily: theme.fonts.mono,
                  fontSize: 20,
                  fontWeight: 700,
                  color: m.alert ? theme.colors.alertRed : theme.colors.heroCyan,
                  fontVariantNumeric: "tabular-nums"
                }}
              >
                {m.value}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
