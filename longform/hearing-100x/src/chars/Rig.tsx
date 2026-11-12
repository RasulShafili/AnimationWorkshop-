// Character rig (our own design): dark round head with big expressive eyes, volumetric clothes, tapered limbs,
// rim light on the side facing the key light. Forward kinematics, degrees: 0 = limb hanging straight down,
// positive = swings toward the facing direction. Root = between the feet on the ground.
import React from "react";

export type Look = {
  head?: string; top: string; topDark?: string; pants: string; shoes?: string; hands?: string;
  hair?: "tuft" | "bald" | "grey" | "none"; headphones?: "head" | "neck" | false; hpColor?: string;
  glasses?: boolean; mustache?: boolean; vest?: string; stripes?: string; scale?: number;
};
export type Pose = {
  lean?: number; head?: number; aL?: number[]; aR?: number[]; lL?: number[]; lR?: number[];
  eyes?: number; look?: number[]; brow?: number; mouth?: "smile" | "grin" | "o" | "flat" | "open" | "frown" | "shout" | "worried";
  bob?: number; facing?: 1 | -1; hands?: "fist" | "open"; headSpin?: number;
};
type Rim = { dx: number; dy: number; color: string } | null;

const rad = (d: number) => (d * Math.PI) / 180;
const fk = (j: number[], len: number, a: number) => [j[0] + len * Math.sin(rad(a)), j[1] + len * Math.cos(rad(a))];
// draw an element twice: rim copy offset toward the light, then the base on top
const R: React.FC<{ rim: Rim; children: (c: string | null) => React.ReactNode }> = ({ rim, children }) => <>{rim && <g transform={`translate(${rim.dx},${rim.dy})`}>{children(rim.color)}</g>}{children(null)}</>;

export const Character: React.FC<{ look: Look; pose: Pose; x: number; y: number; s?: number; rim?: Rim; rot?: number; opacity?: number }> = ({ look, pose, x, y, s = 1, rim = null, rot = 0, opacity = 1 }) => {
  const P = { lean: 0, head: 0, aL: [8, 12], aR: [-6, 10], lL: [4, 4], lR: [-4, 4], eyes: 1, look: [0.6, 0], brow: 0, mouth: "flat", bob: 0, facing: 1 as 1 | -1, ...pose };
  const head = look.head ?? "#1c1a26", dark = look.topDark ?? shade(look.top, 0.72), shoes = look.shoes ?? "#15141c", hands = look.hands ?? head;
  const hipY = -168 + P.bob, hipL = [-12, hipY], hipR = [12, hipY];
  // legs (in hip space, not leaning)
  const leg = (hip: number[], a: number[], back: boolean) => {
    const k = fk(hip, 88, a[0]), ft = fk(k, 86, a[0] - a[1]);
    return <R rim={rim}>{(c) => <g>
      <path d={`M${hip[0]} ${hip[1]} L${k[0]} ${k[1]} L${ft[0]} ${ft[1]}`} stroke={c ?? (back ? shade(look.pants, 0.7) : look.pants)} strokeWidth={21} strokeLinecap="round" strokeLinejoin="round" fill="none" />
      <ellipse cx={ft[0] + 10} cy={ft[1] + 5} rx={19} ry={10} fill={c ?? (back ? shade(shoes, 0.7) : shoes)} transform={`rotate(${-(a[0] - a[1]) * 0.25} ${ft[0]} ${ft[1]})`} />
      {!c && look.stripes && <path d={`M${hip[0]} ${hip[1] + 20} L${k[0]} ${k[1]}`} stroke={look.stripes} strokeWidth={4} strokeDasharray="10 12" opacity={0.6} />}
    </g>}</R>;
  };
  const sh = [0, -292 + P.bob];
  const shL = [-24, sh[1] + 6], shR = [24, sh[1] + 6];
  const arm = (s0: number[], a: number[], back: boolean) => {
    const e = fk(s0, 78, a[0]), h = fk(e, 72, a[0] + a[1]);
    return <R rim={rim}>{(c) => <g>
      <path d={`M${s0[0]} ${s0[1]} L${e[0]} ${e[1]} L${h[0]} ${h[1]}`} stroke={c ?? (back ? dark : look.top)} strokeWidth={17} strokeLinecap="round" strokeLinejoin="round" fill="none" />
      <circle cx={h[0]} cy={h[1]} r={P.hands === "fist" ? 11 : 11.5} fill={c ?? (back ? shade(hands, 0.8) : hands)} />
      {!c && P.hands === "open" && [-1, 0, 1].map(k => { const fa = rad(a[0] + a[1] + k * 22); return <line key={k} x1={h[0]} y1={h[1]} x2={h[0] + 17 * Math.sin(fa)} y2={h[1] + 17 * Math.cos(fa)} stroke={hands} strokeWidth={6} strokeLinecap="round" />; })}
    </g>}</R>;
  };
  // torso: hoodie / shirt volume with a darker side and a hem
  const torso = <R rim={rim}>{(c) => <g>
    <path d={`M-30 ${sh[1] - 4} Q0 ${sh[1] - 16} 30 ${sh[1] - 4} Q42 ${sh[1] + 2} 40 ${sh[1] + 30} Q38 ${hipY - 20} 36 ${hipY + 12} Q0 ${hipY + 24} -36 ${hipY + 12} Q-38 ${hipY - 20} -40 ${sh[1] + 30} Q-42 ${sh[1] + 2} -30 ${sh[1] - 4} Z`} fill={c ?? look.top} />
    {!c && <path d={`M-38 ${sh[1] + 2} Q-14 ${sh[1] - 8} -6 ${sh[1]} L-10 ${hipY + 20} Q-24 ${hipY + 18} -34 ${hipY + 14} Z`} fill={dark} opacity={0.55} />}
    {!c && look.stripes && [0, 1, 2, 3].map(k => <line key={k} x1={-34} y1={sh[1] + 26 + k * 28} x2={34} y2={sh[1] + 26 + k * 28} stroke={look.stripes} strokeWidth={5} opacity={0.5} />)}
    {!c && look.vest && <g><path d={`M-36 ${sh[1] + 14} L36 ${sh[1] + 14} L33 ${hipY + 4} L-33 ${hipY + 4} Z`} fill={look.vest} /><rect x={-36} y={sh[1] + 58} width={72} height={10} fill="#e8f0f0" /><rect x={-34} y={sh[1] + 92} width={68} height={10} fill="#e8f0f0" /></g>}
  </g>}</R>;
  // head with face (features shifted toward the facing side = 3/4 view)
  const hc = [6, -362 + P.bob], fx = 10;
  const eyeY = hc[1] - 4, eo = Math.max(0.08, P.eyes);
  const mx = hc[0] + fx, my = hc[1];
  const mouthD: Record<string, string> = {
    smile: `M${mx - 12} ${my + 28} Q${mx} ${my + 39} ${mx + 12} ${my + 28}`,
    grin: `M${mx - 15} ${my + 20} Q${mx} ${my + 40} ${mx + 15} ${my + 20} Z`,
    flat: `M${mx - 9} ${my + 27} L${mx + 9} ${my + 27}`,
    frown: `M${mx - 11} ${my + 31} Q${mx} ${my + 22} ${mx + 11} ${my + 31}`,
    worried: `M${mx - 11} ${my + 30} Q${mx - 4} ${my + 25} ${mx} ${my + 28} Q${mx + 5} ${my + 31} ${mx + 11} ${my + 27}`,
  };
  const headG = <g transform={`rotate(${P.head} ${hc[0]} ${hc[1] + 40}) rotate(${(P.headSpin ?? 0) * P.facing} ${hc[0]} ${hc[1]})`}>
    {look.headphones === "neck" && <path d={`M${hc[0] - 34} ${hc[1] + 56} Q${hc[0]} ${hc[1] + 86} ${hc[0] + 34} ${hc[1] + 56}`} stroke={look.hpColor ?? "#e8a53a"} strokeWidth={9} fill="none" strokeLinecap="round" />}
    <R rim={rim}>{(c) => <g>
      <circle cx={hc[0]} cy={hc[1]} r={60} fill={c ?? head} />
      {look.hair === "tuft" && <path d={`M${hc[0] - 44} ${hc[1] - 38} Q${hc[0] - 30} ${hc[1] - 82} ${hc[0] + 12} ${hc[1] - 74} Q${hc[0] + 44} ${hc[1] - 92} ${hc[0] + 52} ${hc[1] - 60} Q${hc[0] + 34} ${hc[1] - 66} ${hc[0] + 30} ${hc[1] - 50} Z`} fill={c ?? head} />}
    </g>}</R>
    {look.hair === "grey" && <path d={`M${hc[0] - 50} ${hc[1] - 8} Q${hc[0] - 56} ${hc[1] - 44} ${hc[0] - 26} ${hc[1] - 48} M${hc[0] - 46} ${hc[1] + 6} Q${hc[0] - 58} ${hc[1] - 10} ${hc[0] - 48} ${hc[1] - 28}`} stroke="#c8ccd8" strokeWidth={8} fill="none" strokeLinecap="round" />}
    {/* eyes */}
    {[-1, 1].map(k => { const ex = hc[0] + fx + k * 20 - (k < 0 ? 3 : 0); return <g key={k}>
      <ellipse cx={ex} cy={eyeY} rx={13.5} ry={17 * eo} fill="#f4f1ea" />
      {eo > 0.25 && <circle cx={ex + P.look[0] * 5.5} cy={eyeY + P.look[1] * 6} r={7.5 * Math.min(1, eo + 0.2)} fill="#0b0a10" />}
      {eo > 0.25 && <circle cx={ex + P.look[0] * 5 + 2.5} cy={eyeY + P.look[1] * 5 - 2.5} r={2} fill="#fff" />}
      <line x1={ex - 11} y1={eyeY - 25 - (k * P.brow * 5)} x2={ex + 11} y2={eyeY - 25 + (k * P.brow * 5) - Math.abs(P.brow) * 2} stroke="#09080e" strokeWidth={6} strokeLinecap="round" />
    </g>; })}
    {look.glasses && [-1, 1].map(k => <circle key={k} cx={hc[0] + fx + k * 17} cy={eyeY} r={17} stroke="#d8d4c8" strokeWidth={3.5} fill="none" />)}
    {look.mustache && <path d={`M${hc[0] + fx - 18} ${hc[1] + 20} Q${hc[0] + fx} ${hc[1] + 10} ${hc[0] + fx + 18} ${hc[1] + 20} Q${hc[0] + fx} ${hc[1] + 16} ${hc[0] + fx - 18} ${hc[1] + 20} Z`} fill="#c8ccd8" />}
    {P.mouth === "o" ? <ellipse cx={hc[0] + fx} cy={hc[1] + 27} rx={7} ry={9} fill="#0b0a10" stroke="#f4f1ea" strokeWidth={0} />
      : P.mouth === "open" || P.mouth === "shout" ? <path d={`M${hc[0] + fx - (P.mouth === "shout" ? 14 : 10)} ${hc[1] + 20} Q${hc[0] + fx} ${hc[1] + (P.mouth === "shout" ? 46 : 36)} ${hc[0] + fx + (P.mouth === "shout" ? 14 : 10)} ${hc[1] + 20} Z`} fill="#0b0a10" stroke="#f4f1ea" strokeWidth={2.5} />
      : <path d={mouthD[P.mouth]} stroke="#f4f1ea" strokeWidth={4} fill={P.mouth === "grin" ? "#0b0a10" : "none"} strokeLinecap="round" />}
    {look.headphones === "head" && <g>
      <path d={`M${hc[0] - 46} ${hc[1] + 2} Q${hc[0] - 40} ${hc[1] - 70} ${hc[0] + 10} ${hc[1] - 60}`} stroke="#2a2a34" strokeWidth={10} fill="none" strokeLinecap="round" />
      <ellipse cx={hc[0] - 40} cy={hc[1] + 6} rx={17} ry={24} fill={look.hpColor ?? "#e8a53a"} /><ellipse cx={hc[0] - 44} cy={hc[1] + 6} rx={8} ry={14} fill="#2a2a34" />
    </g>}
  </g>;
  const upper = <g transform={`rotate(${P.lean} 0 ${hipY})`}>{arm(shL, P.aL, true)}{torso}{headG}{arm(shR, P.aR, false)}</g>;
  return <g transform={`translate(${x} ${y}) rotate(${rot}) scale(${s * (look.scale ?? 1) * P.facing} ${s * (look.scale ?? 1)})`} opacity={opacity}>
    {leg(hipL, P.lL, true)}{leg(hipR, P.lR, false)}{upper}
  </g>;
};
export const shade = (hex: string, k: number) => { const n = parseInt(hex.slice(1), 16); const r = Math.round(((n >> 16) & 255) * k), g = Math.round(((n >> 8) & 255) * k), b = Math.round((n & 255) * k); return `rgb(${r},${g},${b})`; };
// gait cycles
export const runPose = (ph: number, amp = 1): Pose => { const s = Math.sin(ph), c = Math.cos(ph);
  return { lean: 10 * amp, aL: [-50 * s * amp, 80], aR: [50 * s * amp, 80], lL: [40 * s * amp, 20 + 60 * Math.max(0, -c) * amp], lR: [-40 * s * amp, 20 + 60 * Math.max(0, c) * amp], bob: -Math.abs(c) * 10 * amp, hands: "fist" }; };
export const walkPose = (ph: number, amp = 1): Pose => { const s = Math.sin(ph), c = Math.cos(ph);
  return { lean: 3, aL: [-22 * s * amp, 14], aR: [22 * s * amp, 14], lL: [24 * s * amp, 6 + 22 * Math.max(0, -c) * amp], lR: [-24 * s * amp, 6 + 22 * Math.max(0, c) * amp], bob: -Math.abs(c) * 4 * amp }; };
