import React from "react";
import { AbsoluteFill, Audio, staticFile, useCurrentFrame, useVideoConfig, interpolate, Easing } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import "@fontsource/anton";
import "@fontsource/vt323";
import { Scene } from "./World";
import { PixelPost } from "./PixelPost";
import { CAPTIONS, heightAt, fmtHeight } from "./timeline";

const strokeSmooth = "0 0 2px #0a0820, 3px 3px 0 #0a0820, -3px 3px 0 #0a0820, 3px -3px 0 #0a0820, -3px -3px 0 #0a0820, 0 8px 18px rgba(0,0,0,.45)";
const strokePixel = "4px 0 0 #0a0820, -4px 0 0 #0a0820, 0 4px 0 #0a0820, 0 -4px 0 #0a0820, 4px 4px 0 #0a0820, -4px 4px 0 #0a0820, 4px -4px 0 #0a0820, -4px -4px 0 #0a0820, 0 8px 0 #0a0820, 4px 8px 0 #0a0820, -4px 8px 0 #0a0820";

export const Video: React.FC<{ withAudio?: boolean; pixel?: boolean }> = ({ withAudio = true, pixel = false }) => {
  const frame = useCurrentFrame(), { fps, width, height } = useVideoConfig();
  const t = frame / fps, n = Math.floor(t), h = heightAt(t), local = (t - n) * fps;
  const pop = interpolate(local, [0, 4, 10], [1.25, 0.94, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const capIn = n === 0 ? interpolate(local, [6, 16], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : interpolate(local, [2, 9], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const space = n >= 16 && n <= 30;
  const W = pixel ? width / 4 : width, H = pixel ? height / 4 : height;
  const font = pixel ? "VT323" : "Anton", stroke = pixel ? strokePixel : strokeSmooth;
  const sz = pixel ? { small: 64, big: 192, cap: 80, tag: 64, note: 48 } : { small: 52, big: 150, cap: 64, tag: 40, note: 26 };
  // pixel mode: snap the pop to whole steps so letters stay on the 4px grid
  const scale = pixel ? Math.round(pop * 8) / 8 : pop;
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <div style={{ width: W, height: H, transform: pixel ? "scale(4)" : undefined, transformOrigin: "top left", imageRendering: pixel ? "pixelated" : undefined }}>
        <ThreeCanvas width={W} height={H} shadows flat={pixel} dpr={1} camera={{ fov: 42, position: [0, 0.5, 3] }} gl={{ logarithmicDepthBuffer: true, antialias: !pixel }} style={{ imageRendering: pixel ? "pixelated" : undefined }}>
          <Scene t={t} h={h} n={n} />
          {pixel && <PixelPost />}
        </ThreeCanvas>
      </div>
      <AbsoluteFill style={{ fontFamily: font, alignItems: "center", color: "#fff", textAlign: "center", WebkitFontSmoothing: pixel ? "none" : undefined }}>
        <div style={{ marginTop: 248, fontSize: sz.small, letterSpacing: pixel ? 0 : 4, textShadow: stroke }}>SECOND {n}</div>
        <div style={{ fontSize: pixel && fmtHeight(n).length > 9 ? 128 : sz.big, lineHeight: pixel ? 0.9 : 1.05, color: "#ffe14e", textShadow: stroke, transform: `scale(${scale})` }}>{fmtHeight(n)}</div>
        <div style={{ marginTop: 18, fontSize: sz.cap, lineHeight: 1.05, maxWidth: 960, textShadow: stroke, opacity: capIn, transform: `translateY(${Math.round((1 - capIn) * 6) * 4}px)` }}>{CAPTIONS[n]}</div>
      </AbsoluteFill>
      <div style={{ position: "absolute", left: 48, bottom: 330, fontFamily: font, fontSize: sz.tag, color: "#fff", textShadow: stroke }}>×2 EVERY SECOND</div>
      {space && <div style={{ position: "absolute", left: 48, bottom: 286, fontFamily: font, fontSize: sz.note, color: "#c8d8ff", opacity: 0.8 }}>SATELLITES &amp; MOON NOT TO SCALE</div>}
      {withAudio && <Audio src={staticFile("mix.wav")} />}
    </AbsoluteFill>
  );
};
