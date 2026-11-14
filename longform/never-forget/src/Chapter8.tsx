// Chapter 8 — "The missing day" (cliffhanger) + outro/end card (12 s of calm space for YouTube end-screen elements).
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Stage, camAt, sat, ease, easeOut, lerp, W, H } from "./engine/core";
import { Vignette, Grain, Grade, Glow } from "./engine/fx";
import { PalaceCorridor, PalaceHall } from "./scenes/Palace";
import { Character } from "./chars/Rig2";
import { LINA } from "./chars/cast";
import { useFonts } from "./ui";
import { VO_C8, talkAt } from "./vo_c8";

const D = (k: string) => VO_C8[`c8_${k}`]?.dur ?? 60;
const T: Record<string, number> = {};
T.n1 = 20; T.n2 = T.n1 + D("n1") + 8; T.hall = T.n2 + Math.round(D("n2") * 0.5); T.lina1 = T.n2 + D("n2") + 8; T.push = T.lina1 + D("lina1") + 10;
T.n3 = T.push + 84; T.card = T.n3 + D("n3") + 24; T.n4 = T.card + 96; T.n5 = T.n4 + D("n4") + 10; T.end = T.n5 + D("n5") + 360;
export const C8 = T; export const C8_LEN = T.end;
const DARK = 3653, HALL0 = 3646;   // 14 MAR 2020 (a Saturday) = door 7 in the hall (x 900)

export const Chapter8: React.FC = () => {
  useFonts();
  const f = useCurrentFrame();
  const tk = (k: string) => talkAt(VO_C8[`c8_${k}`], f, T[k]);
  let shot: React.ReactNode = null, grade = "palace";
  const knocks = [T.push + 34, T.push + 46, T.push + 58], knock = knocks.some(k => f >= k && f < k + 6) ? 1 : 0;
  if (f < T.n2) { const lx = lerp(-150, 640, (f - 0) / T.n2);
    shot = <Stage cam={camAt(f, [[0, lx - 960, 60, 1.25], [T.n2, lx - 960, 60, 1.3]])} bg="#0a0716"><PalaceHall f={f} linaX={lx} doorStart={HALL0} darkDoor={DARK} dim={0.3} pillars={false}
      lina={{ gold: 0.6, look: [0.7, -0.3], aR: [60 + 10 * Math.sin(f * 0.1), 50], mouth: "flat" }} /></Stage>; }
  else if (f < T.hall) shot = <PalaceCorridor f={f} z={(f - T.n2) * 4} doorStart={DARK - 6} darkDoor={DARK} brightEnd={0.5} />;
  else if (f < T.lina1) shot = <Stage cam={camAt(f, [[T.hall, -20, 30, 1.3], [T.lina1, 20, 60, 1.6]])} bg="#0a0716"><PalaceHall f={f} linaX={780} walking={false} doorStart={HALL0} darkDoor={DARK} dim={0.25} pillars={false}
    lina={{ gold: 0.6, look: [0.8, -0.2], mouth: "o", eyes: 1.2 }} /></Stage>;
  else if (f < T.push) shot = <Stage cam={camAt(f, [[T.lina1, -180, -162, 2.1], [T.push, -176, -162, 2.25]])} bg="#0a0716"><PalaceHall f={f} linaX={780} walking={false} doorStart={HALL0} darkDoor={DARK} dim={0.25} pillars={false}
    lina={{ gold: 0.6, look: [0.8, -0.1], mouth: "worried", talk: tk("lina1"), eyes: 1.2, brow: 0, browIn: 0.9 }} /></Stage>;
  else if (f < T.n3) { const back = f > knocks[2] + 6 ? easeOut((f - knocks[2] - 6) / 14) : 0;
    shot = <Stage cam={camAt(f, [[T.push, 0, 20, 1.5], [T.n3, 10, 20, 1.6]])} bg="#0a0716"><PalaceHall f={f} linaX={lerp(800, 690, back)} walking={false} doorStart={HALL0} darkDoor={DARK} dim={0.25} pillars={false} shake={knock}
      lina={{ gold: 0.6, look: [0.8, -0.1], aR: back ? [20, 30] : [76, 6], mouth: knock || back ? "o" : "flat", eyes: back ? 1.3 : 1.1, brow: back ? 0.8 : 0, lean: back ? -8 : 6 }} /></Stage>; }
  else if (f < T.card) { const k = sat((f - T.n3) / (T.card - T.n3));
    shot = <div style={{ position: "absolute", inset: 0, opacity: 1 - sat((f - T.card + 14) / 14) }}><Stage cam={camAt(f, [[T.n3, 35, -30, 2.2], [T.card, 35, -40, 2.9]])} bg="#0a0716">
      <PalaceHall f={f} linaX={-300} walking={false} doorStart={HALL0} darkDoor={DARK} dim={0.35 + 0.3 * k} pillars={false} /></Stage></div>; }
  else if (f < T.n4) { grade = "none"; const t = f - T.card;
    shot = <AbsoluteFill style={{ background: "#05030c", alignItems: "center", justifyContent: "center", flexDirection: "column" }}>
      <div style={{ fontFamily: "Inter", fontWeight: 900, fontSize: 70, letterSpacing: 16, color: "#ffc94a", opacity: sat(t / 14), textShadow: "0 0 30px rgba(255,190,60,.6)" }}>PART 2</div>
      <div style={{ fontFamily: "Inter", fontWeight: 900, fontSize: 130, color: "#fff", opacity: sat((t - 10) / 14), transform: `scale(${0.94 + 0.06 * easeOut((t - 10) / 20)})` }}>THE MISSING DAY</div>
      <div style={{ fontFamily: "Inter", fontWeight: 700, fontSize: 40, letterSpacing: 10, color: "#8a80a8", opacity: sat((t - 30) / 14), marginTop: 20 }}>COMING SOON</div></AbsoluteFill>; }
  else if (f < T.n5) { const t = f - T.n4;
    shot = <><PalaceCorridor f={f} z={t * 2} doorStart={500} brightEnd={1} />
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}><div style={{ padding: "34px 60px", borderRadius: 30, background: "rgba(10,6,20,.72)", border: "2px solid rgba(255,201,74,.5)", textAlign: "center", opacity: sat(t / 14), transform: `translateY(${(1 - easeOut(t / 20)) * 40}px)` }}>
        <div style={{ fontFamily: "Inter", fontWeight: 900, fontSize: 80, color: "#fff", lineHeight: 1.1 }}>WHICH ONE DAY<br />WOULD YOU KEEP<span style={{ color: "#ffc94a" }}> FOREVER?</span></div>
        <div style={{ fontFamily: "Inter", fontWeight: 800, fontSize: 40, color: "#ffc94a", marginTop: 18 }}>💬 tell us in the comments</div></div></AbsoluteFill></>; }
  else { grade = "none"; const t = f - T.n5;
    // end card: Lina waves on the left; big calm space on the right for YouTube's end-screen video tiles + subscribe
    shot = <AbsoluteFill style={{ background: "radial-gradient(circle at 30% 50%, #2a1e4a, #07050f 75%)" }}>
      <svg width={W} height={H} style={{ position: "absolute" }}><Glow x={520} y={560} r={600} color="#ffc94a" o={0.25} />
        <Character look={LINA} pose={{ facing: 1, gold: 0.8, look: [0.7, -0.1], mouth: "smile", aR: [112 + 8 * Math.sin(t * 0.3), 40 + 18 * Math.sin(t * 0.3)] }} x={520} y={900} s={1.25} f={f} seed={1} rim={{ dx: 4, dy: -3, color: "#ffc94a" }} />
      </svg>
      <div style={{ position: "absolute", left: 110, top: 90, fontFamily: "Inter", fontWeight: 900, fontSize: 64, color: "#fff", opacity: sat(t / 12) }}>THANKS FOR WATCHING</div>
      <div style={{ position: "absolute", left: 110, top: 170, fontFamily: "Inter", fontWeight: 800, fontSize: 36, color: "#ffc94a", opacity: sat((t - 8) / 12) }}>PART 2 IS COMING — DON'T FORGET 😉</div>
      <div style={{ position: "absolute", left: 300, bottom: 70, padding: "20px 46px", borderRadius: 16, background: "#e8302c", fontFamily: "Inter", fontWeight: 900, fontSize: 44, color: "#fff", opacity: sat((t - 20) / 10), transform: `scale(${1 + 0.06 * Math.sin(t * 0.15)})` }}>SUBSCRIBE 🔔</div>
    </AbsoluteFill>; }
  return <AbsoluteFill style={{ background: "#000" }}>
    {shot}
    {grade === "palace" && <Grade top="rgba(120,100,200,1)" bottom="rgba(20,10,40,1)" o={0.25} />}
    {grade !== "none" && <Vignette o={0.85} />}
    <Grain f={f} o={0.05} />
  </AbsoluteFill>;
};
