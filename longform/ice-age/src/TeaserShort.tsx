// Vertical teaser Short (1080x1920, ~35 s) from c12 (the discovery): blurred fill + the 16:9 clip in the middle, hook on
// top, word-by-word captions under the picture, "FULL STORY ON THE CHANNEL" CTA. Clip = public/teaser_clip.mp4 (c12 0:00–0:34.7).
import React from "react";
import { AbsoluteFill, OffthreadVideo, staticFile, useCurrentFrame } from "remotion";
import { sat, easeOut } from "./engine/core";
import { Captions } from "./Captions";
import { useFonts } from "./ui";
import words1 from "./teaser_words.json";
import words2 from "./teaser2_words.json";
import words3 from "./teaser3_words.json";
export const TEASER_LEN = 1041, TEASER2_LEN = 791, TEASER3_LEN = 949;
type P = { clip?: string; words?: any; hook?: React.ReactNode; sub?: string };
export const TeaserShort2: React.FC = () => <TeaserShort clip="teaser2_clip.mp4" words={words2} hook={<>THE MAMMOTH<br />TURNS.<br /><span style={{ color: "#ff5a3a" }}>SHE SLIPS.</span></>} sub="…day 30 in 28,000 BC 😱" />;
export const TeaserShort3: React.FC = () => <TeaserShort clip="teaser3_clip.mp4" words={words3} hook={<>−25°C IN A<br />HOODIE IN<br /><span style={{ color: "#7ac8ff" }}>28,000 BC</span></>} sub="…and something is watching you 😳" />;
export const TeaserShort: React.FC<P> = ({ clip = "teaser_clip.mp4", words = words1, hook, sub = "…and it wasn't there yesterday 😳" }) => {
  useFonts(); const f = useCurrentFrame(); const sh = "0 6px 0 rgba(0,0,0,.55), 0 12px 30px rgba(0,0,0,.6)";
  return <AbsoluteFill style={{ background: "#000" }}>
    <OffthreadVideo src={staticFile(clip)} muted style={{ position: "absolute", width: 3413, height: 1920, left: -1166, top: 0, filter: "blur(40px) brightness(0.45)" }} />
    <div style={{ position: "absolute", top: 560, left: 0, width: 1080, height: 608, boxShadow: "0 30px 80px rgba(0,0,0,.7)", borderTop: "4px solid rgba(255,184,74,.8)", borderBottom: "4px solid rgba(255,184,74,.8)" }}>
      <OffthreadVideo src={staticFile(clip)} style={{ width: 1080, height: 608 }} /></div>
    <AbsoluteFill style={{ fontFamily: "Inter", color: "#fff", alignItems: "center", textAlign: "center" }}>
      <div style={{ marginTop: 150, fontWeight: 900, fontSize: 92, lineHeight: 1.0, letterSpacing: -2, textShadow: sh, padding: "0 50px", transform: `scale(${0.9 + 0.1 * easeOut(f / 12)})` }}>
        {hook ?? <>A 30,000-YEAR-OLD<br />PAINTING OF<br /><span style={{ color: "#ffc94a" }}>A PHONE?!</span></>}</div>
      <div style={{ marginTop: 18, fontWeight: 800, fontSize: 46, color: "#ffe8c8", textShadow: sh, opacity: sat((f - 8) / 10) }}>{sub}</div>
    </AbsoluteFill>
    <Captions f={f} words={words as any} top={1330} accent="#ffc94a" size={80} />
    <div style={{ position: "absolute", bottom: 250, width: "100%", display: "flex", justifyContent: "center" }}>
      <div style={{ padding: "18px 40px", borderRadius: 999, background: "#e8322a", fontFamily: "Inter", fontWeight: 900, fontSize: 48, color: "#fff", boxShadow: "0 10px 30px rgba(0,0,0,.5)", transform: `scale(${1 + 0.04 * Math.sin(f * 0.15)})` }}>FULL STORY ON THE CHANNEL ▶</div></div>
  </AbsoluteFill>;
};
