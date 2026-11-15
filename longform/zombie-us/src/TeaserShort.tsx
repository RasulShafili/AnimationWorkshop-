// Vertical teaser Short (1080x1920, 28 s) from the climax: blurred fill + the 16:9 clip in the middle, hook on top,
// word-by-word captions under the picture, "FULL STORY ON THE CHANNEL" CTA. Clip = public/teaser_clip.mp4 (6:00–6:28).
import React from "react";
import { AbsoluteFill, OffthreadVideo, staticFile, useCurrentFrame } from "remotion";
import { sat, easeOut } from "./engine/core";
import { Captions } from "./Captions";
import { useFonts } from "./ui";
import words1 from "./teaser_words.json";
export const TEASER_LEN = 878;
type P = { clip?: string; words?: any; h1?: string; h2?: string; sub?: string };
export const TeaserShort: React.FC<P> = ({ clip = "teaser_clip.mp4", words = words1, h1 = "DAY 3 OF THE", h2 = "ZOMBIE OUTBREAK", sub = "…don't make a sound 🤫" }) => {
  useFonts(); const f = useCurrentFrame(); const sh = "0 6px 0 rgba(0,0,0,.55), 0 12px 30px rgba(0,0,0,.6)";
  return <AbsoluteFill style={{ background: "#000" }}>
    <OffthreadVideo src={staticFile(clip)} muted style={{ position: "absolute", width: 3413, height: 1920, left: -1166, top: 0, filter: "blur(40px) brightness(0.45)" }} />
    <div style={{ position: "absolute", top: 560, left: 0, width: 1080, height: 608, boxShadow: "0 30px 80px rgba(0,0,0,.7)", borderTop: "4px solid rgba(154,216,138,.7)", borderBottom: "4px solid rgba(154,216,138,.7)" }}>
      <OffthreadVideo src={staticFile(clip)} style={{ width: 1080, height: 608 }} /></div>
    <AbsoluteFill style={{ fontFamily: "Inter", color: "#fff", alignItems: "center", textAlign: "center" }}>
      <div style={{ marginTop: 200, fontWeight: 900, fontSize: 86, lineHeight: 1.0, letterSpacing: -2, textShadow: sh, padding: "0 50px", transform: `scale(${0.9 + 0.1 * easeOut(f / 12)})` }}>
        {h1}<br /><span style={{ color: "#9ad88a" }}>{h2}</span></div>
      <div style={{ marginTop: 18, fontWeight: 800, fontSize: 46, color: "#e8dcff", textShadow: sh, opacity: sat((f - 8) / 10) }}>{sub}</div>
    </AbsoluteFill>
    <Captions f={f} words={words as any} top={1330} accent="#ffc94a" size={80} />
    <div style={{ position: "absolute", bottom: 250, width: "100%", display: "flex", justifyContent: "center" }}>
      <div style={{ padding: "18px 40px", borderRadius: 999, background: "#e8322a", fontFamily: "Inter", fontWeight: 900, fontSize: 48, color: "#fff", boxShadow: "0 10px 30px rgba(0,0,0,.5)", transform: `scale(${1 + 0.04 * Math.sin(f * 0.15)})` }}>FULL STORY ON THE CHANNEL ▶</div></div>
  </AbsoluteFill>;
};
