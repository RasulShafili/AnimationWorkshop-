import React, { useEffect, useState } from "react";
import { AbsoluteFill, Audio, staticFile, useCurrentFrame, delayRender, continueRender } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import "@fontsource/vt323";
import { Scene, LIGHT_OFF, sat, lerp } from "./Space";
import { PixelPost } from "./PixelPost";
import T from "./timeline.json";

// text is drawn at 1080x1920 on a 4px grid (VT323) so it matches the 270x480 pixel render
const stroke = "4px 0 0 #05040e, -4px 0 0 #05040e, 0 4px 0 #05040e, 0 -4px 0 #05040e, 4px 4px 0 #05040e, -4px 4px 0 #05040e, 4px -4px 0 #05040e, -4px -4px 0 #05040e, 0 8px 0 #05040e, 4px 8px 0 #05040e, -4px 8px 0 #05040e";
const B = T.beats;
const beatOf = (f: number) => { let i = 0; while (i < B.length - 2 && f >= B[i + 1]) i++; return i; };
const snap = (v: number) => Math.round(v / 4) * 4;
const ACCENT = ["#ffcf3a", "#7ad8ff", "#ffe08a", "#ffd27a", "#d8b060", "#bfe6ff", "#55efc4"];

export const Video: React.FC<{ withAudio?: boolean }> = ({ withAudio = true }) => {
  const f = useCurrentFrame();
  const [h] = useState(() => delayRender("font"));
  useEffect(() => { document.fonts.load("80px VT323").then(() => continueRender(h)); }, [h]);
  const bi = beatOf(f), lf = f - B[bi], [l1, l2] = T.texts[bi];
  const typed = bi === 0 ? 999 : Math.max(0, (lf - 3) * 1.4);
  const show = (s: string, off: number) => s.slice(0, Math.max(0, Math.floor(typed - off)));
  const pop = bi === 0 ? 1 : lf < 8 ? 1 + 0.25 * (1 - lf / 8) : 1;
  // flashes: the collapse, and the dive into the hole at the end (which loops into frame 0)
  const flash = Math.max(f >= T.collapse && f < T.collapse + 12 ? 1 - (f - T.collapse) / 12 : 0, sat((f - 974) / 16) * 0.85);
  // dip to black on the cuts between space and the ground
  const dip = Math.max(...[B[3], B[6]].map(c => sat(1 - Math.abs(f - c) / 6)));
  // counters
  const secs = Math.round(499 * sat((f - T.shellStart) / (LIGHT_OFF - T.shellStart)));
  const timer = `${Math.floor(secs / 60)}:${String(secs % 60).padStart(2, "0")}`;
  const temp = Math.round(f < T.week ? lerp(15, -18, sat((f - B[4] - 10) / (T.week - B[4] - 10))) : lerp(-18, -73, sat((f - B[5] - 10) / (T.year - B[5] - 10))));
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <div style={{ width: 270, height: 480, transform: "scale(4)", transformOrigin: "top left", imageRendering: "pixelated" }}>
        <ThreeCanvas width={270} height={480} flat dpr={1} camera={{ fov: 46, position: [0, 0, 3] }} gl={{ antialias: false }} style={{ imageRendering: "pixelated" }}>
          <Scene f={f} />
          <PixelPost />
        </ThreeCanvas>
      </div>
      <AbsoluteFill style={{ background: `rgba(255,248,230,${flash})` }} />
      <AbsoluteFill style={{ background: `rgba(0,0,0,${dip})` }} />
      <AbsoluteFill style={{ fontFamily: "VT323", color: "#fff", alignItems: "center", textAlign: "center", WebkitFontSmoothing: "none" }}>
        <div style={{ marginTop: 236, fontSize: 100, lineHeight: 0.95, textShadow: stroke }}>{show(l1, 0)}</div>
        <div style={{ marginTop: 8, fontSize: bi === 0 ? 144 : 100, lineHeight: 0.95, color: ACCENT[bi], textShadow: stroke, transform: `scale(${Math.round(pop * 8) / 8})` }}>{show(l2, l1.length)}</div>
      </AbsoluteFill>
      {bi === 1 && lf > 30 && <div style={{ position: "absolute", width: "100%", top: 1010, textAlign: "center", fontFamily: "VT323", fontSize: 72, color: "#7ad8ff", textShadow: stroke }}>ORBIT: UNCHANGED</div>}
      {bi === 1 && lf > 55 && <div style={{ position: "absolute", width: "100%", top: 1094, textAlign: "center", fontFamily: "VT323", fontSize: 60, color: "#ffb070", textShadow: stroke }}>BLACK HOLE: ONLY 6 KM WIDE</div>}
      {bi === 2 && f >= T.shellStart && (
        <div style={{ position: "absolute", width: "100%", top: 960, textAlign: "center", fontFamily: "VT323", textShadow: stroke }}>
          <div style={{ fontSize: 176, lineHeight: 0.9, color: f >= LIGHT_OFF ? "#ff5a5a" : "#ffe08a" }}>{timer}</div>
          <div style={{ fontSize: 60, color: "#fff" }}>{f >= LIGHT_OFF ? "LAST LIGHT HAS PASSED" : "LAST SUNLIGHT ON ITS WAY"}</div>
        </div>
      )}
      {bi === 3 && (
        <div style={{ position: "absolute", width: "100%", top: 1300, textAlign: "center", fontFamily: "VT323", textShadow: stroke }}>
          <div style={{ fontSize: 150, lineHeight: 0.9, color: f >= T.dark ? "#ff5a5a" : "#ffe08a" }}>12:00</div>
          <div style={{ fontSize: 60, color: "#fff" }}>{f >= T.dark ? "STILL NOON" : "NOON"}</div>
        </div>
      )}
      {(bi === 4 || bi === 5) && (
        <div style={{ position: "absolute", width: "100%", top: 1300, textAlign: "center", fontFamily: "VT323", textShadow: stroke }}>
          <div style={{ fontSize: 176, lineHeight: 0.9, color: temp > 0 ? "#ffe08a" : temp > -40 ? "#9ad8ff" : "#e8f6ff" }}>{temp}°C</div>
          <div style={{ fontSize: 60, color: "#fff" }}>{bi === 4 ? (f < T.week - 6 ? "DAYS LATER" : "~1 WEEK LATER") : (f < T.year - 6 ? "MONTHS LATER" : "~1 YEAR LATER")}</div>
        </div>
      )}
      {(bi === 1 || bi === 2) && <div style={{ position: "absolute", left: 48, bottom: 300, fontFamily: "VT323", fontSize: 44, color: "#c8d8ff", opacity: 0.85, textShadow: stroke }}>NOT TO SCALE</div>}
      {withAudio && <Audio src={staticFile("mix.wav")} />}
    </AbsoluteFill>
  );
};
