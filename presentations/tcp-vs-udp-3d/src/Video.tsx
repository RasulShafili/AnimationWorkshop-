import React, { useEffect, useState } from "react";
import { AbsoluteFill, Audio, staticFile, useCurrentFrame, delayRender, continueRender } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import "@fontsource/inter/500.css";
import "@fontsource/inter/600.css";
import "@fontsource/inter/700.css";
import "@fontsource/inter/800.css";
import { Scene3D } from "./Scene3D";
import { Overlay } from "./Overlay";
import { SEC } from "./timing";

export const Video: React.FC<{ withAudio?: boolean }> = ({ withAudio = true }) => {
  const f = useCurrentFrame();
  // labels are drawn into canvases, so the font (incl. ə ş ğ İ) must be loaded first
  const [handle] = useState(() => delayRender("fonts"));
  const [ready, setReady] = useState(false);
  useEffect(() => {
    Promise.all(["500", "600", "700", "800"].map(w => document.fonts.load(`${w} 64px Inter`, "Seq ACK əşğİçöü"))).then(() => { setReady(true); continueRender(handle); });
  }, [handle]);
  // short dip between sections
  const d = Math.min(...SEC.slice(1, 8).map(c => Math.abs(f - c)));
  const dip = d < 8 ? (1 - d / 8) * 0.85 : 0;
  return (
    <AbsoluteFill style={{ backgroundColor: "#070a18", fontFamily: "Inter" }}>
      {ready && (
        <ThreeCanvas width={1920} height={1080} shadows camera={{ fov: 38, position: [0, 3, 9] }} gl={{ antialias: true }}>
          <Scene3D f={f} />
        </ThreeCanvas>
      )}
      {ready && <AbsoluteFill><Overlay f={f} /></AbsoluteFill>}
      <AbsoluteFill style={{ background: "#070a18", opacity: dip }} />
      {withAudio && <Audio src={staticFile("mix.wav")} />}
    </AbsoluteFill>
  );
};
