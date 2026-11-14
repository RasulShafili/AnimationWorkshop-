import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Character } from "./chars/Rig2";
import * as C from "./chars/cast";
import { Glow } from "./engine/fx";
export const CharSheet: React.FC = () => {
  const f = useCurrentFrame();
  const list: [string, any, any][] = [["LINA", C.LINA, { mouth: "smile", gold: 1, look: [0.6, -0.1], aR: [30, 60], hold: "cards" }], ["AYLA", C.AYLA, { mouth: "smile", talk: 0.5 }], ["OKAFOR", C.OKAFOR, { mouth: "frown", brow: -0.6, hold: "cup", aR: [20, 70] }],
    ["SAM", C.SAM, { mouth: "grin", brow: 0.6 }], ["MANAGER", C.MANAGER, { mouth: "smirk" }], ["HALE", C.HALE, { mouth: "flat", hold: "pills", aR: [24, 66] }], ["GUARD", C.GUARD, {}], ["COP", C.COP, { hold: "phone", aR: [30, 80] }]];
  return <AbsoluteFill style={{ background: "linear-gradient(#3a4466,#1a1d2c)" }}>
    <svg width={1920} height={1080}><Glow x={960} y={300} r={900} color="#ffd08a" o={0.25} />
      {list.map(([n, l, p], i) => <g key={n}><Character look={l} pose={p} x={140 + i * 235} y={820} s={1.15} f={f} seed={i + 1} rim={{ dx: 4, dy: -2, color: "#9fd8ff" }} />
        <text x={140 + i * 235} y={900} fill="#fff" fontFamily="Inter" fontWeight={800} fontSize={26} textAnchor="middle">{n}</text></g>)}
      <g transform="translate(420,1000)"><text fill="#ccc" fontSize={20} fontFamily="Inter">seated test →</text></g>
    </svg>
  </AbsoluteFill>;
};
