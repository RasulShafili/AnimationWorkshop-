// Transparent 1080x1920 overlay for the vertical teaser Short: hook on top, CTA at the bottom.
import React from "react";
import { AbsoluteFill, delayRender, continueRender } from "remotion";
import "@fontsource/inter/800.css";
import "@fontsource/inter/900.css";
export const ShortOverlay: React.FC = () => {
  const [h] = React.useState(() => delayRender("fonts"));
  React.useEffect(() => { Promise.all([document.fonts.load("900 80px Inter"), document.fonts.load("800 40px Inter")]).then(() => continueRender(h)); }, [h]);
  const sh = "0 6px 0 rgba(0,0,0,.55), 0 12px 30px rgba(0,0,0,.6)";
  return <AbsoluteFill style={{ fontFamily: "Inter", color: "#fff", alignItems: "center", textAlign: "center" }}>
    <div style={{ marginTop: 250, fontWeight: 900, fontSize: 84, lineHeight: 1.02, letterSpacing: -2, textShadow: sh, padding: "0 50px" }}>HIS HEARING IS<br /><span style={{ color: "#ffc34a" }}>100× BETTER</span></div>
    <div style={{ marginTop: 18, fontWeight: 800, fontSize: 46, color: "#cfe8ff", textShadow: sh }}>…so he takes off his headphones</div>
    <div style={{ position: "absolute", bottom: 300, padding: "18px 40px", borderRadius: 999, background: "#e8322a", fontWeight: 900, fontSize: 48, boxShadow: "0 10px 30px rgba(0,0,0,.5)" }}>FULL STORY ON THE CHANNEL ▶</div>
  </AbsoluteFill>;
};
