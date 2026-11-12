// Chapter 3 places: morning street + bus stop, kitchen, classroom (with the hallway through the door),
// locker hallway, and the school cut-away.
import React from "react";
import { Layer, W, H, rnd, lerp, sat } from "../engine/core";
import { Glow, Shaft, Bokeh } from "../engine/fx";
import { Noise, AO, Wallpaper, Wood, Bricks } from "../engine/tex";
import { Character, walkPose } from "../chars/Rig";
import { HERO, HERO_HP, MIA, TEACHER1, TEACHER2, STUDENTS } from "../chars/cast";
const SUN = { dx: 4, dy: -3, color: "#ffe0b0" };
export const talkM = (f: number, on: boolean) => (on ? (["open", "flat", "o", "flat"] as const)[Math.floor(f / 3) % 4] : "flat");

export const BusStop: React.FC<{ f: number; busX: number; rings: number; extra?: React.ReactNode; hero?: React.ReactNode }> = ({ f, busX, rings, extra, hero }) => {
  const g = 860;
  return <>
    <Layer depth={0.3}>
      <defs><linearGradient id="msky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#7aa8e0" /><stop offset="1" stopColor="#ffd8b0" /></linearGradient></defs>
      <rect x={-800} y={-400} width={W + 1600} height={g + 400} fill="url(#msky)" />
      {Array.from({ length: 12 }, (_, i) => <rect key={i} x={-600 + i * 260} y={g - 300 - rnd(i, 1) * 260} width={200} height={600} fill="#b8b0c8" opacity={0.6} />)}
      <Glow x={300} y={200} r={500} color="#fff2d0" o={0.5} />
    </Layer>
    <Layer depth={1}>
      {/* road + sidewalk */}
      <rect x={-800} y={g} width={W + 1600} height={60} fill="#b8b4b0" /><rect x={-800} y={g + 60} width={W + 1600} height={400} fill="#5a5a66" />
      <Noise x={-800} y={g} w={W + 1600} h={460} freq={0.7} o={0.3} />
      {Array.from({ length: 10 }, (_, i) => <rect key={i} x={-700 + i * 300} y={g + 190} width={150} height={10} fill="#f0f0e0" opacity={0.7} />)}
      {/* the bus, coming out from behind the corner building */}
      <g transform={`translate(${busX} ${g + 80})`}>
        <rect x={0} y={-300} width={720} height={260} rx={30} fill="#2a9a8a" /><rect x={0} y={-130} width={720} height={30} fill="#f0c040" />
        {[0, 1, 2, 3, 4].map(k => <rect key={k} x={60 + k * 130} y={-270} width={100} height={100} rx={10} fill="#bfe0f0" opacity={0.8} />)}
        <circle cx={140} cy={-40} r={46} fill="#1a1a1a" /><circle cx={580} cy={-40} r={46} fill="#1a1a1a" />
        <rect x={-10} y={-260} width={20} height={60} rx={6} fill="#fff2c0" />
      </g>
      {/* the corner building that hides the bus */}
      <Bricks x={-500} y={-200} w={760} h={g + 260} color="#a8644a" mortar="#6a3a2a" />
      {Array.from({ length: 8 }, (_, i) => <rect key={i} x={-440 + (i % 3) * 230} y={40 + Math.floor(i / 3) * 260} width={150} height={180} fill="#4a6a8a" stroke="#f0e8d8" strokeWidth={10} />)}
      <AO x={160} y={-200} w={100} h={g + 260} dir="left" o={0.4} />
      {/* sound coming round the corner */}
      {rings > 0 && [0, 1, 2, 3].map(k => { const t = ((f + k * 9) % 36) / 36; return <path key={k} d={`M${260 + t * 500} ${g - 200 - t * 120} q 40 ${120 + t * 100} 0 ${240 + t * 200}`} stroke="#5ae0ff" strokeWidth={5} fill="none" opacity={(1 - t) * rings} />; })}
      {/* bus stop */}
      <rect x={1150} y={g - 330} width={14} height={330} fill="#3a3a44" /><rect x={1150} y={g - 330} width={380} height={18} fill="#3a3a44" /><rect x={1170} y={g - 312} width={340} height={230} fill="#bfe0f0" opacity={0.35} />
      <circle cx={1580} cy={g - 360} r={40} fill="#2a9a8a" /><text x={1580} y={g - 348} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={34} fill="#fff">B</text><rect x={1575} y={g - 320} width={10} height={320} fill="#3a3a44" />
      {hero ?? <Character look={HERO_HP} pose={{ look: [-1, 0], facing: -1, mouth: "smile", brow: 0.5 }} x={1360} y={g} rim={SUN} />}
      {extra}
      <rect x={1700} y={g - 230} width={20} height={230} fill="#4a3a2a" /><circle cx={1710} cy={g - 280} r={110} fill="#4a8a4a" /><circle cx={1660} cy={g - 230} r={70} fill="#3a7a3a" />
    </Layer>
  </>;
};

export const Kitchen: React.FC<{ f: number; pop: number }> = ({ f, pop }) => {
  const g = 860, ty = pop < 0 ? 0 : -Math.sin(Math.min(1, pop) * Math.PI) * 220 + Math.min(1, pop) * 60;
  return <>
    <Layer depth={0.6}>
      <defs><pattern id="tiles" width={60} height={60} patternUnits="userSpaceOnUse"><rect width={60} height={60} fill="#e8e4d8" /><rect width={60} height={60} fill="none" stroke="#b8b0a0" strokeWidth={3} /></pattern></defs>
      <rect x={-600} y={-300} width={W + 1200} height={H + 600} fill="#f0d8b8" />
      <rect x={-600} y={360} width={W + 1200} height={240} fill="url(#tiles)" />
      <rect x={1240} y={60} width={460} height={420} fill="#bfe0ff" stroke="#f8f4ec" strokeWidth={18} /><Glow x={1470} y={260} r={500} color="#fff4d8" o={0.6} />
      <Shaft pts={[[1240, 80], [1700, 80], [1300, 1100], [500, 1100]]} color="#fff2d0" o={0.3} blur={22} from={[1470, 80]} to={[900, 1100]} />
      {[0, 1, 2].map(k => <g key={k}><line x1={260 + k * 90} y1={60} x2={260 + k * 90} y2={200} stroke="#3a3a3a" strokeWidth={3} /><circle cx={260 + k * 90} cy={240} r={44} fill="#3a3a44" /><rect x={252 + k * 90} y={190} width={16} height={30} fill="#3a3a44" /></g>)}
      <rect x={-200} y={180} width={300} height={680} rx={10} fill="#e8ecf0" /><rect x={-200} y={420} width={300} height={6} fill="#b8bcc8" />
    </Layer>
    <Layer depth={1}>
      <rect x={-600} y={600} width={W + 1200} height={40} fill="#8a6a4a" /><rect x={-600} y={640} width={W + 1200} height={600} fill="#c8a880" /><Wood x={-600} y={640} w={W + 1200} h={240} color="#a8845a" rows={3} />
      <AO x={-600} y={640} w={W + 1200} h={50} dir="down" o={0.35} />
      {/* toaster + toast */}
      <rect x={760} y={480} width={260} height={130} rx={30} fill="#d8dce4" /><rect x={760} y={480} width={260} height={30} rx={14} fill="#f0f4f8" /><rect x={800} y={470} width={80} height={14} rx={4} fill="#2a2a2a" /><rect x={900} y={470} width={80} height={14} rx={4} fill="#2a2a2a" />
      <rect x={1020} y={520} width={18} height={50} rx={4} fill="#2a2a2a" />
      {[0, 1].map(k => <g key={k} transform={`translate(${810 + k * 100} ${470 + ty}) rotate(${pop > 0.5 ? (k ? 12 : -10) * Math.min(1, pop) : 0})`}><rect x={-6} y={-70} width={72} height={78} rx={14} fill="#d8a050" /><rect x={0} y={-62} width={60} height={64} rx={10} fill="#f0d090" /></g>)}
      <Glow x={890} y={470} r={140} color="#ff8a3a" o={pop < 0 ? 0.35 : 0} />
      <Character look={HERO} pose={{ aR: [100, 30], aL: [70, 60], mouth: pop > 0.9 ? "grin" : "smile", look: [1, -0.6], brow: 0.4 }} x={540} y={g} rim={SUN} />
      <ellipse cx={720} cy={560} rx={90} ry={16} fill="#f8f8f8" stroke="#c8c8d0" strokeWidth={3} />
      {pop > 0.9 && <text x={890} y={380} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={50} fill="#c84a2a">POP!</text>}
    </Layer>
  </>;
};

export const Classroom: React.FC<{ f: number; whisper: number; teachersTalk: boolean; tell: number }> = ({ f, whisper, teachersTalk, tell }) => {
  const g = 900;
  return <>
    <Layer depth={0.7}>
      <rect x={-600} y={-300} width={W + 1200} height={H + 600} fill="#e8dcc0" /><Noise x={-600} y={-300} w={W + 1200} h={H + 600} freq={0.8} o={0.15} />
      <rect x={-600} y={540} width={W + 1200} height={400} fill="#c8b890" />
      {/* hallway seen through the open door (left) */}
      <rect x={-480} y={180} width={360} height={720} fill="#a8c0c8" /><rect x={-480} y={180} width={360} height={720} fill="none" stroke="#5a4a3a" strokeWidth={16} />
      {Array.from({ length: 4 }, (_, i) => <rect key={i} x={-470 + i * 88} y={420} width={80} height={480} fill="#4a6aa8" stroke="#2a4a88" strokeWidth={4} />)}
      {/* chalkboard */}
      <rect x={300} y={200} width={900} height={380} fill="#2a4a3a" stroke="#6a4a2a" strokeWidth={18} /><Noise x={300} y={200} w={900} h={380} freq={0.5} o={0.3} blend="screen" />
      <text x={380} y={300} fontFamily="Inter" fontWeight={800} fontSize={54} fill="#e8f0e8" opacity={0.8}>CHAPTER 5: CELLS</text><path d="M420 380 Q520 330 620 400 T820 380" stroke="#e8f0e8" strokeWidth={5} fill="none" opacity={0.6} /><circle cx={1000} cy={430} r={70} stroke="#e8f0e8" strokeWidth={5} fill="none" opacity={0.6} />
      {/* windows with daylight */}
      {[1340, 1640].map(x => <g key={x}><rect x={x} y={160} width={240} height={360} fill="#cfe8ff" stroke="#f4ece0" strokeWidth={14} /><line x1={x + 120} y1={160} x2={x + 120} y2={520} stroke="#f4ece0" strokeWidth={8} /></g>)}
      <Shaft pts={[[1340, 180], [1880, 180], [1500, 1100], [800, 1100]]} color="#fff2d0" o={0.25} blur={24} from={[1600, 180]} to={[1100, 1100]} />
      <Character look={TEACHER1} pose={{ facing: 1, mouth: talkM(f, teachersTalk), look: [1, 0], aR: [30, 60] }} x={-390} y={g} s={0.8} />
      <Character look={TEACHER2} pose={{ facing: -1, mouth: talkM(f + 5, teachersTalk), look: [1, 0], aL: [20, 40] }} x={-220} y={g} s={0.8} />
      <AO x={-600} y={g - 100} w={W + 1200} h={100} dir="up" o={0.3} />
    </Layer>
    <Layer depth={1}>
      <Wood x={-600} y={g} w={W + 1200} h={400} color="#8a6a4a" rows={6} />
      {/* rows of desks + students (back row first) */}
      {[0, 1].map(row => [0, 1, 2, 3].map(c => { const x = 140 + c * 440 + row * 80, y = g + 20 + row * 120, s = 0.78 + row * 0.12, isHero = row === 1 && c === 1, st = STUDENTS[(row * 4 + c) % 6];
        const turn = !isHero && tell > 0.2 && c < 3, shocked = tell > 0.6 && !isHero;
        return <g key={`${row}${c}`}>
          {isHero ? <Character look={HERO_HP} pose={{ lL: [80, 80], lR: [76, 76], mouth: tell > 0 ? talkM(f, tell < 0.8) : "flat", look: whisper > 0 && tell === 0 ? [-1, -0.2] : [1, 0], brow: whisper > 0.5 ? 1 : 0, aR: tell > 0 ? [100, 20] : [40, 60], hands: tell > 0 ? "open" : undefined }} x={x} y={y + 30} s={s} rim={SUN} />
            : <Character look={st} pose={{ lL: [80, 80], lR: [76, 76], mouth: shocked ? "o" : "flat", look: turn ? [1, 0] : [1, -0.3], facing: turn ? (c === 2 ? -1 : 1) : 1, brow: shocked ? 1 : 0 }} x={x} y={y + 30} s={s} rim={SUN} />}
          <rect x={x + 30 * s} y={y - 200 * s} width={230 * s} height={18} rx={4} fill="#c89a6a" /><rect x={x + 40 * s} y={y - 182 * s} width={12} height={170 * s} fill="#6a4a2a" /><rect x={x + 240 * s} y={y - 182 * s} width={12} height={170 * s} fill="#6a4a2a" />
          <rect x={x + 60 * s} y={y - 212 * s} width={90 * s} height={12} fill={["#d84a4a", "#4a8ad8", "#e8c84a"][(row + c) % 3]} />
        </g>; }))}
      {/* the whisper path from the hallway to the hero's ear */}
      {whisper > 0 && <path d={`M-200 ${g - 500} Q300 ${g - 700} ${660} ${g - 420}`} stroke="#5ae0ff" strokeWidth={5} fill="none" strokeDasharray="8 20" strokeDashoffset={-f * 4} opacity={whisper} style={{ filter: "drop-shadow(0 0 8px #5ae0ff)" }} />}
      {teachersTalk && <g><rect x={-80} y={g - 860} width={560} height={110} rx={24} fill="rgba(10,20,30,.75)" stroke="#5ae0ff" strokeWidth={3} /><text x={200} y={g - 793} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={40} fill="#e8faff">…pop quiz, chapter six…</text></g>}
    </Layer>
  </>;
};

export const Lockers: React.FC<{ f: number; miaTalk: boolean }> = ({ f, miaTalk }) => {
  const g = 880;
  return <>
    <Layer depth={0.7}>
      <rect x={-600} y={-300} width={W + 1200} height={H + 600} fill="#d8d0c0" /><Noise x={-600} y={-300} w={W + 1200} h={H + 600} freq={0.8} o={0.12} />
      {Array.from({ length: 22 }, (_, i) => <g key={i}><rect x={-500 + i * 130} y={330} width={120} height={550} fill={i % 5 === 2 ? "#d84a4a" : "#3a6ab8"} stroke="#1a3a78" strokeWidth={5} />{[0, 1, 2].map(k => <rect key={k} x={-470 + i * 130} y={360 + k * 16} width={60} height={6} fill="#1a3a78" />)}<rect x={-405 + i * 130} y={600} width={8} height={30} fill="#d8d8e0" /></g>)}
      <rect x={-600} y={120} width={W + 1200} height={180} fill="#c8bca8" /><rect x={300} y={140} width={420} height={150} fill="#a87a4a" />{[0, 1, 2, 3].map(k => <rect key={k} x={320 + k * 100} y={160 + (k % 2) * 20} width={80} height={100} fill={["#f0e08a", "#8ad0f0", "#f0a0b8", "#fff"][k]} />)}
      <AO x={-600} y={g - 120} w={W + 1200} h={120} dir="up" o={0.35} />
      {Array.from({ length: 6 }, (_, i) => <g key={i}><rect x={-560 + i * 520} y={40} width={200} height={14} fill="#f8f4e8" /><Glow x={-460 + i * 520} y={60} r={300} color="#fff8e0" o={0.35} /></g>)}
    </Layer>
    <Layer depth={1}>
      <rect x={-600} y={g} width={W + 1200} height={400} fill="#b8b0a0" /><Noise x={-600} y={g} w={W + 1200} h={400} freq={0.6} o={0.2} />
      {Array.from({ length: 12 }, (_, i) => <rect key={i} x={-600 + i * 260} y={g} width={4} height={400} fill="#000" opacity={0.15} />)}
      <Character look={MIA} pose={{ mouth: talkM(f, miaTalk), brow: 0.9, aR: [90, 60], hands: "open", look: [1, 0] }} x={760} y={g} rim={SUN} />
      <Character look={HERO_HP} pose={{ mouth: miaTalk ? "grin" : "smile", facing: -1, look: [1, 0], aR: [-10, 30] }} x={1160} y={g} rim={SUN} />
    </Layer>
  </>;
};

export const SchoolCut: React.FC<{ f: number; phone: number }> = ({ f, phone }) => {
  const floors = [0, 1, 2], fh = 300, top = 120;
  return <>
    <Layer depth={0.4}><rect x={-600} y={-300} width={W + 1200} height={H + 600} fill="#8ab0d8" /><Glow x={1700} y={100} r={500} color="#fff2d0" o={0.5} /></Layer>
    <Layer depth={1}>
      <Bricks x={180} y={top - 60} w={1560} h={fh * 3 + 80} color="#b8704a" mortar="#7a4a30" />
      {floors.map(i => { const y = top + i * fh; return <g key={i}>
        <rect x={220} y={y + 20} width={1480} height={fh - 40} fill={["#e8dcc0", "#dcd8c8", "#e8d8c8"][i]} />
        <Wood x={220} y={y + fh - 50} w={1480} h={30} color="#8a6a4a" rows={1} />
        <rect x={260} y={y + 60} width={300} height={140} fill="#2a4a3a" stroke="#6a4a2a" strokeWidth={8} />
        {[0, 1, 2, 3, 4].map(k => <rect key={k} x={700 + k * 200} y={y + 190} width={140} height={14} fill="#c89a6a" />)}
        <text x={1660} y={y + 80} textAnchor="end" fontFamily="Inter" fontWeight={900} fontSize={40} fill="#6a5a4a" opacity={0.5}>{`FLOOR ${3 - i}`}</text>
      </g>; })}
      {/* hero on floor 3 pointing down; backpack on floor 1 */}
      <Character look={HERO_HP} pose={{ aR: [30, 0], mouth: "grin", look: [0.5, 1], hands: "open" }} x={600} y={top + fh - 50} s={0.62} rim={SUN} />
      <g transform={`translate(${1300 + (phone > 0 ? Math.sin(f * 3) * 3 : 0)} ${top + fh * 3 - 60})`}><rect x={-50} y={-90} width={100} height={110} rx={24} fill="#d84a4a" /><rect x={-34} y={-60} width={68} height={40} rx={10} fill="#a83a3a" /></g>
      {phone > 0 && [0, 1, 2, 3].map(k => { const t = ((f + k * 8) % 32) / 32; return <circle key={k} cx={1300} cy={top + fh * 3 - 100} r={30 + t * 700} fill="none" stroke="#5ae0ff" strokeWidth={4} opacity={(1 - t) * phone * 0.8} />; })}
      {phone > 0 && <text x={1300} y={top + fh * 3 - 180} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={38} fill="#5ae0ff" opacity={phone}>bzzt… bzzt…</text>}
    </Layer>
  </>;
};
