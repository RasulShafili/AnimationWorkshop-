// shared overlays: fonts, fact card, memory time-stamp, title.
import React from "react";
import { delayRender, continueRender } from "remotion";
import "@fontsource/inter/700.css";
import "@fontsource/inter/800.css";
import "@fontsource/inter/900.css";
import "@fontsource/vt323/400.css";
import "@fontsource/permanent-marker/400.css";
export const useFonts = () => {
  const [h] = React.useState(() => delayRender("fonts"));
  React.useEffect(() => { Promise.all(["700 24px Inter", "800 24px Inter", "900 80px Inter", "400 40px VT323", "400 60px 'Permanent Marker'"].map(s => document.fonts.load(s))).then(() => continueRender(h)); }, [h]);
};
export const FactCard: React.FC<{ text: string; k: number; side?: "left" | "right" }> = ({ text, k, side = "left" }) => k <= 0 ? null :
  <div style={{ position: "absolute", [side]: 80, bottom: 90, maxWidth: 860, padding: "20px 30px 22px", borderRadius: 20, background: "rgba(10,10,22,.80)", backdropFilter: "blur(6px)", border: "1px solid rgba(255,201,74,.35)", boxShadow: "0 18px 50px rgba(0,0,0,.45)", fontFamily: "Inter", fontWeight: 800, fontSize: 33, lineHeight: 1.28, color: "#fff", opacity: Math.min(1, k), transform: `translateY(${(1 - Math.min(1, k)) * 34}px)` }}>
    <div style={{ color: "#ffc94a", fontSize: 22, letterSpacing: 4, marginBottom: 6 }}>REAL SCIENCE</div>{text}</div>;
// memory replay stamp: VHS-like date/time in a corner
export const Stamp: React.FC<{ text: string; k: number; f: number }> = ({ text, k, f }) => k <= 0 ? null :
  <div style={{ position: "absolute", right: 60, top: 48, padding: "4px 18px", borderRadius: 8, background: "rgba(10,6,0,.55)", fontFamily: "VT323", fontSize: 72, color: "#ffd56a", opacity: k * (0.85 + 0.15 * Math.sin(f * 0.9)), textShadow: "2px 0 rgba(255,60,60,.6), -2px 0 rgba(60,200,255,.6), 0 0 18px rgba(255,200,80,.6)" }}>
    <span style={{ color: "#ff4a4a" }}>{Math.floor(f / 15) % 2 ? "●" : "○"} </span>{text}</div>;
// red hand-written day/time stamp (top-left), writes on letter by letter
export const DayStamp: React.FC<{ day: string; time?: string; t: number; dur?: number }> = ({ day, time, t, dur = 150 }) => {
  if (t < 0 || t > dur) return null;
  const o = Math.min(1, t / 6, (dur - t) / 10), n1 = Math.floor(t / 1.6), n2 = Math.floor(Math.max(0, t - day.length * 1.6 - 4) / 1.4);
  const st: React.CSSProperties = { fontFamily: "'Permanent Marker'", color: "#d8202a", textShadow: "0 3px 0 rgba(0,0,0,.5), 0 0 6px rgba(0,0,0,.9), 0 0 22px rgba(0,0,0,.8), 0 0 40px rgba(0,0,0,.6)", lineHeight: 1.0 };
  return <div style={{ position: "absolute", left: 70, top: 50, opacity: o, transform: "rotate(-2deg)" }}>
    <div style={{ ...st, fontSize: 112 }}>{day.slice(0, n1)}</div>
    {time && <div style={{ ...st, fontSize: 64, marginTop: 6 }}>{time.slice(0, n2)}</div>}
  </div>;
};
