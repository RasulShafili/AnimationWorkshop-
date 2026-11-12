import React from "react";
import { AbsoluteFill, useCurrentFrame, delayRender, continueRender } from "remotion";
import "@fontsource/inter/800.css";
import "@fontsource/inter/900.css";
import { Stage, Layer, camAt, sat, easeOut } from "./engine/core";
import { Vignette, Grain, Grade, Glow } from "./engine/fx";
import { Bedroom } from "./scenes/Bedroom";
import { Field, House, Ear } from "./scenes/Places";
import { Character } from "./chars/Rig";
import { HERO } from "./chars/cast";
export const C2 = { field: 170, house: 280, ear: 380, hiss: 770, end: 900 };
export const C2VO = [10, 176, 286, 386, 525, 776];
// decibel bar: normal hearing threshold vs yours (100x quieter = 20 dB lower)
const DbBar: React.FC<{ k: number }> = ({ k }) => {
  const x0 = 360, x1 = 1560, dbx = (db: number) => x0 + (db + 20) / 160 * (x1 - x0);
  return <svg width={1920} height={1080} style={{ position: "absolute", opacity: k }}>
    <rect x={x0 - 40} y={800} width={x1 - x0 + 80} height={190} rx={24} fill="rgba(10,10,24,.72)" />
    <defs><linearGradient id="db" x1="0" x2="1"><stop offset="0" stopColor="#5ae0ff" /><stop offset="0.5" stopColor="#ffd34a" /><stop offset="1" stopColor="#ff4a4a" /></linearGradient></defs>
    <rect x={x0} y={880} width={(x1 - x0) * easeOut(k)} height={16} rx={8} fill="url(#db)" />
    {[["WHISPER", 30], ["TALK", 60], ["TRAFFIC", 85], ["JET", 140]].map(([t, d]) => <g key={t as string}><line x1={dbx(+d)} y1={870} x2={dbx(+d)} y2={906} stroke="#fff" strokeWidth={3} /><text x={dbx(+d)} y={940} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={24} fill="#cfd8ff">{t}</text></g>)}
    <line x1={dbx(0)} y1={846} x2={dbx(0)} y2={910} stroke="#ffffff" strokeWidth={4} /><text x={dbx(0)} y={838} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={24} fill="#fff">NORMAL QUIETEST</text>
    <g opacity={sat((k - 0.6) * 3)}><line x1={dbx(-20)} y1={846} x2={dbx(-20)} y2={910} stroke="#5ae0ff" strokeWidth={6} /><text x={dbx(-20)} y={972} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={28} fill="#5ae0ff">YOU · 100× QUIETER</text></g>
  </svg>;
};
export const Chapter2: React.FC = () => {
  const f = useCurrentFrame();
  const [h] = React.useState(() => delayRender("fonts"));
  React.useEffect(() => { Promise.all([document.fonts.load("800 24px Inter"), document.fonts.load("900 80px Inter")]).then(() => continueRender(h)); }, [h]);
  let scene: React.ReactNode, grade = true;
  if (f < C2.field) {
    scene = <Stage cam={camAt(f, [[0, 120, 60, 1.25], [170, 40, 60, 1.35]])}><Bedroom f={f} eyes={1} look={[1, 0]} day={1} lying={false}>
      <Character look={HERO} pose={{ lL: [90, 90], lR: [86, 86], aL: [30, 60], aR: [-10, 40], mouth: "smile", look: [1, -0.3] }} x={640} y={858} rim={{ dx: 4, dy: -3, color: "#ffd8a0" }} />
    </Bedroom></Stage>;
  } else if (f < C2.house) { const l = f - C2.field; scene = <Stage cam={camAt(l, [[0, -1860, -60, 1.0], [18, -1860, -60, 1.0], [100, 1840, -60, 1.0]])}><Field f={f} whisper={sat((l - 10) / 80)} /></Stage>; }
  else if (f < C2.ear) { const l = f - C2.house; scene = <Stage cam={camAt(l, [[0, 0, 0, 1.0], [100, 40, 0, 1.06]])}><House f={f} /></Stage>; }
  else if (f < C2.hiss) {
    const l = f - C2.ear;
    if (l < 80) {   // into the ear: a big profile head, sound lines flowing in, zoom into the ear
      const z = 1 + Math.pow(sat((l - 20) / 60), 3) * 9;
      scene = <svg width={1920} height={1080} style={{ position: "absolute", background: "#1a1430" }}><g transform={`translate(1060 520) scale(${z}) translate(-1060 -520)`}>
        <Glow x={700} y={500} r={600} color="#6a5aff" o={0.25} />
        <circle cx={760} cy={520} r={360} fill="#1c1a26" /><path d="M980 300 Q1180 230 1150 480 Q1140 560 1080 600" stroke="#ffb36a" strokeWidth={10} fill="none" />
        <path d="M1010 400 Q1110 360 1100 470 Q1095 520 1050 560 Q1030 520 1060 480 Q1080 430 1010 440 Z" fill="#2a2636" stroke="#ffb36a" strokeWidth={6} /><circle cx={1060} cy={520} r={16} fill="#05040a" />
        {[0, 1, 2, 3, 4].map(k => { const t = ((l + k * 8) % 40) / 40; return <path key={k} d={`M${1700 - t * 600} ${380 + k * 40} q30 -20 60 0 t60 0 t60 0`} stroke="#9ec8ff" strokeWidth={5} fill="none" opacity={1 - t} />; })}
      </g></svg>;
    } else {
      const k = sat((l - 80) / 300), z = 1 + k * 0.12;
      scene = <div style={{ position: "absolute", inset: 0, transform: `scale(${z}) translate(${-k * 30}px, 0px)`, transformOrigin: "60% 50%", opacity: sat((l - 80) / 10) }}><Ear f={f} zoom={1} mine={sat((l - 150) / 30)} /></div>;
    }
    grade = false;
  }
  else scene = <Stage cam={camAt(f - C2.hiss, [[0, -380, 80, 2.3], [130, -380, 80, 2.45]])} bg="#05040a"><Bedroom f={f} eyes={1} look={[0, -1]} brow={-0.4} mouth="worried" /></Stage>;
  const hissK = f >= C2.hiss ? sat((f - C2.hiss) / 20) : 0;
  return <AbsoluteFill>
    {scene}
    {f < C2.field && <DbBar k={sat((f - 30) / 70)} />}
    {hissK > 0 && <svg width={1920} height={1080} style={{ position: "absolute", opacity: hissK }}><path d={Array.from({ length: 200 }, (_, i) => `${i ? "L" : "M"}${i * 9.6} ${900 + Math.sin(i * 1.7 + f) * 6 + Math.sin(i * 4.1 - f * 2) * 4}`).join(" ")} stroke="#9ec8ff" strokeWidth={3} fill="none" opacity={0.6} /><text x={960} y={980} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={34} fill="#cfe0ff" opacity={0.8}>sssssssssssss…</text></svg>}
    {grade && <Grade top="rgba(40,60,140,1)" bottom="rgba(120,40,80,1)" o={0.18} />}
    <Vignette o={0.75} />
    <Grain f={f} o={hissK > 0 ? 0.14 : 0.06} />
  </AbsoluteFill>;
};
