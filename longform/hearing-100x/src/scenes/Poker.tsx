// Dad's poker night: a kitchen at night, one hanging lamp, a round table, chips and cards; heartbeat icons.
import React from "react";
import { Layer, W, H, rnd, lerp, sat } from "../engine/core";
import { Glow, Shaft } from "../engine/fx";
import { Noise, AO, Wallpaper, Wood } from "../engine/tex";
import { Character } from "../chars/Rig";
import { HERO, DAD, UNCLE, AUNT, FRIEND } from "../chars/cast";
import { talkM } from "./School";
const LAMP = { dx: 0, dy: -4, color: "#ffc27a" };
// a heart icon that beats at `bpm`; fast ones turn red and grow
export const HeartIcon: React.FC<{ x: number; y: number; f: number; bpm: number; on: number }> = ({ x, y, f, bpm, on }) => {
  const per = 1800 / bpm, ph = (f % per) / per, beat = Math.exp(-ph * 9) + (ph > 0.25 ? 0.6 * Math.exp(-(ph - 0.25) * 9) : 0);
  const fast = bpm > 110, s = 1 + beat * (fast ? 0.45 : 0.22);
  return <g opacity={on} transform={`translate(${x} ${y}) scale(${s})`}>
    <Glow x={0} y={0} r={60} color={fast ? "#ff3a4a" : "#ff9aa8"} o={0.5 * beat} />
    <path d="M0 18 C -26 -2 -22 -26 -6 -24 C 0 -23 0 -18 0 -14 C 0 -18 0 -23 6 -24 C 22 -26 26 -2 0 18 Z" fill={fast ? "#ff3a4a" : "#ff9aa8"} />
    <text y={52} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={22} fill="#fff" opacity={0.85}>{Math.round(bpm)}</text>
  </g>;
};
export const Poker: React.FC<{ f: number; icons: number; uncleTalk: boolean; dadTalk: boolean; reveal: number; chips: number; uncleBpm: number; heroMouth?: any }> = ({ f, icons, uncleTalk, dadTalk, reveal, chips, uncleBpm, heroMouth = "smile" }) => {
  const g = 900, tableY = 700;
  const seats = [{ look: DAD, x: 520, facing: 1 as const, bpm: 72, talk: dadTalk }, { look: UNCLE, x: 820, facing: 1 as const, bpm: uncleBpm, talk: uncleTalk }, { look: AUNT, x: 1180, facing: -1 as const, bpm: 80, talk: false }, { look: FRIEND, x: 1460, facing: -1 as const, bpm: 76, talk: false }];
  return <>
    <Layer depth={0.75}>
      <Wallpaper x={-600} y={-300} w={W + 1200} h={g + 300} base="#2a1e1a" ink="#5a3e2a" kind="stripe" o={0.15} />
      <AO x={-600} y={-300} w={W + 1200} h={500} dir="down" o={0.7} />
      {/* cabinets, window with night, fridge, clock */}
      <rect x={-300} y={100} width={500} height={220} fill="#3a2a22" />{[0, 1, 2].map(k => <rect key={k} x={-286 + k * 165} y={114} width={150} height={192} fill="#4a3428" />)}
      <rect x={1640} y={160} width={260} height={300} fill="#0e1428" stroke="#1a120e" strokeWidth={14} /><circle cx={1840} cy={210} r={22} fill="#e8e4d0" opacity={0.8} />
      <circle cx={1340} cy={180} r={50} fill="#d8ccb0" stroke="#3a2a1a" strokeWidth={8} /><line x1={1340} y1={180} x2={1340} y2={150} stroke="#2a1a10" strokeWidth={5} /><line x1={1340} y1={180} x2={1362} y2={190} stroke="#2a1a10" strokeWidth={4} />
      <rect x={-560} y={240} width={220} height={660} rx={10} fill="#c8c4b8" opacity={0.6} />
    </Layer>
    <Layer depth={1}>
      <Wood x={-600} y={g} w={W + 1200} h={400} color="#3a2418" rows={6} />
      {/* the lamp and its cone of light */}
      <line x1={990} y1={-300} x2={990} y2={250} stroke="#0e0a08" strokeWidth={5} /><path d="M900 250 L1080 250 L1040 200 L940 200 Z" fill="#2a3a2a" /><ellipse cx={990} cy={252} rx={70} ry={10} fill="#fff0c8" />
      <Glow x={990} y={260} r={260} color="#ffd890" o={0.7} />
      <Shaft pts={[[930, 252], [1050, 252], [1500, 900], [480, 900]]} color="#ffd890" o={0.3} blur={18} from={[990, 252]} to={[990, 900]} />
      {/* players behind the table */}
      {seats.map((s, i) => <Character key={i} look={s.look} pose={{ lL: [80, 80], lR: [76, 76], facing: s.facing, mouth: s.talk ? talkM(f, true) : i === 1 && reveal > 0.5 ? "frown" : "flat", look: [1, 0.2], aR: [62, 28], aL: [52, 34], brow: i === 1 && uncleBpm > 110 ? -0.3 : 0 }} x={s.x} y={tableY + 150} rim={LAMP} s={0.95} />)}
      {/* table */}
      <ellipse cx={990} cy={tableY} rx={620} ry={70} fill="#1e4a2e" /><ellipse cx={990} cy={tableY + 8} rx={620} ry={70} fill="none" stroke="#5a3418" strokeWidth={18} />
      <rect x={560} y={tableY + 60} width={30} height={200} fill="#2a1a10" /><rect x={1390} y={tableY + 60} width={30} height={200} fill="#2a1a10" />
      {/* chips pile drifting toward the hero's seat (right front) */}
      {Array.from({ length: 10 }, (_, k) => { const c = ["#d83a3a", "#3a6ad8", "#f0f0f0", "#2a2a2a"][k % 4]; const x = lerp(900 + (k % 5) * 30, 1680 + (k % 5) * 18, chips), y = tableY - 10 - Math.floor(k / 5) * 12 - k * 2; return <ellipse key={k} cx={x} cy={y} rx={24} ry={8} fill={c} stroke="#000" strokeWidth={2} />; })}
      {/* uncle's cards: face down, then flipped to a full house */}
      {[0, 1, 2, 3, 4].map(k => { const flip = sat(reveal * 1.5 - k * 0.1); const sx = Math.abs(Math.cos(flip * Math.PI)); const face = flip > 0.5; const lab = ["K", "K", "K", "9", "9"][k]; return <g key={k} transform={`translate(${760 + k * 64} ${tableY - 40}) scale(${sx} 1)`}><rect x={-26} y={-38} width={52} height={74} rx={6} fill={face ? "#fbfaf4" : "#2a4ab8"} stroke="#0a0a0a" strokeWidth={2} />{face ? <text y={10} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={32} fill={k % 2 ? "#d83a3a" : "#1a1a1a"}>{lab}</text> : <rect x={-18} y={-30} width={36} height={58} rx={4} fill="none" stroke="#8aa8ff" strokeWidth={2} />}</g>; })}
      {/* the hero's chair, then the hero sitting on it */}
      {(() => { const cx = 1720, s = 1.1, seatY = g + 80 - 168 * s + 6; return <g><rect x={cx - 70} y={seatY} width={150} height={20} rx={6} fill="#5a3a22" /><rect x={cx + 60} y={seatY - 230} width={18} height={250} rx={6} fill="#4a2e1a" /><rect x={cx - 64} y={seatY + 20} width={14} height={g + 80 - seatY - 20} fill="#3a2414" /><rect x={cx + 58} y={seatY + 20} width={14} height={g + 80 - seatY - 20} fill="#3a2414" /></g>; })()}
      {/* the hero at the front right, back to us three-quarters */}
      <Character look={HERO} pose={{ lL: [80, 80], lR: [76, 76], facing: -1, mouth: heroMouth, look: [1, -0.2], aR: [50, 40], aL: [40, 50], brow: 0.3 }} x={1720} y={g + 80} rim={LAMP} s={1.1} />
      {/* heart icons above the players */}
      {seats.map((s, i) => <HeartIcon key={i} x={s.x + 10} y={tableY - 400} f={f + i * 7} bpm={s.bpm} on={icons} />)}
      <AO x={-600} y={g} w={W + 1200} h={80} dir="down" o={0.5} />
    </Layer>
  </>;
};
