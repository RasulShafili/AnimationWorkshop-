// Skeleton robot (our own design, 2026-11-17) — same skeleton/joint maths as Rig2 (root between the feet, hips 168 up,
// shoulders 292 up, head centre 362 up) and the same Pose API (aL/aR/lL/lR/lean/head/facing/bob/talk/look/eyes), so it
// drops into every scene, camera helper and onHead() like a person. NOT a movie robot: no human skull, no teeth, no
// jaw. Capsule head + dark visor with a light-bar eye, stacked-disc neck, rib-frame torso with a glowing power core,
// rod "bones" with a parallel piston, ball joints, three-finger claws, wedge feet.
// shell 0..1: white helper-robot plates over the frame (1 = friendly home robot, 0 = bare skeleton; in between the
// plates drop away one by one — the "its shell cracks" story beat). mode: calm (two round eyes) / scan (sweeping dot)
// / hostile (narrow red slit + glow). dmg 0..1: scratches, a cracked visor and a sparking wire.
import React from "react";
import { rnd } from "../engine/core";
import type { Pose } from "./Rig2";
import { shade } from "./Rig2";

export type RobotLook = { frame?: string; joint?: string; plate?: string; shell?: number; mode?: "calm" | "scan" | "hostile";
  eye?: string; dmg?: number; tag?: string; scale?: number; core?: boolean;
  dark?: number; night?: string; noArmR?: boolean; smiley?: boolean; gun?: boolean; drop?: number[] };   // drop: plate ids forced off (1 chest, 2 belly, 3 head, 10-13 arms, 20-23 legs)   // dark 0..1: body sinks into the night colour, eyes + core stay lit and get a halo
type Rim = { dx: number; dy: number; color: string } | null;
const rad = (d: number) => (d * Math.PI) / 180;
const fk = (j: number[], len: number, a: number) => [j[0] + len * Math.sin(rad(a)), j[1] + len * Math.cos(rad(a))];
let uidN = 0;

export const Robot: React.FC<{ look: RobotLook; pose: Pose; x: number; y: number; s?: number; rim?: Rim; f?: number; seed?: number; rot?: number; opacity?: number }> =
  ({ look, pose, x, y, s = 1, rim = null, f = 0, seed = 1, rot = 0, opacity = 1 }) => {
  const id = React.useMemo(() => `r${++uidN}`, []);
  const P = { lean: 0, head: 0, aL: [8, 12], aR: [-6, 10], lL: [4, 4], lR: [-4, 4], eyes: 1, look: [0.5, 0], bob: 0, facing: 1 as 1 | -1, talk: 0, hold: null, ...pose };
  const frame = look.frame ?? "#3c424e", joint = look.joint ?? "#1e2128", plate = look.plate ?? "#eef1f5", shell = look.shell ?? 0, dmg = look.dmg ?? 0;
  const mode = look.mode ?? "calm", eyeC = look.eye ?? (mode === "hostile" ? "#ff3a24" : mode === "scan" ? "#ffb02a" : "#5ad8ff");
  const hum = Math.sin((f + seed * 13) / 40) * 1.2;                                  // servo idle, not breathing
  const hipY = -168 + P.bob, hipL = [-14, hipY], hipR = [14, hipY];
  const sh = [0, -292 + P.bob + hum * 0.4], shL = [-34, sh[1] + 6], shR = [34, sh[1] + 6];
  // plates fall off in this order as shell goes 1 → 0 (threshold per plate)
  const has = (i: number) => !(look.drop ?? []).includes(i) && (shell >= 1 - 0.0001 || rnd(i, seed + 7) < shell);
  const hiC = shade(frame, 1.6), loC = shade(frame, 0.7);

  const ball = (p: number[], r: number, c: string | null) => <g><circle cx={p[0]} cy={p[1]} r={r} fill={c ?? joint} />
    {!c && <circle cx={p[0] - r * 0.3} cy={p[1] - r * 0.35} r={r * 0.35} fill="#fff" opacity={0.25} />}</g>;
  // a bone: main rod + thin piston beside it + end collars
  const bone = (a: number[], b: number[], w: number, c: string | null, back: boolean, piston = true) => {
    const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L, o = w * 0.9;
    return <g>
      <line x1={a[0]} y1={a[1]} x2={b[0]} y2={b[1]} stroke={c ?? (back ? loC : frame)} strokeWidth={w} strokeLinecap="round" />
      {!c && <line x1={a[0] - nx * w * 0.2} y1={a[1] - ny * w * 0.2} x2={b[0] - nx * w * 0.2} y2={b[1] - ny * w * 0.2} stroke={hiC} strokeOpacity={back ? 0.15 : 0.35} strokeWidth={w * 0.25} strokeLinecap="round" />}
      {piston && !c && <><line x1={a[0] + nx * o + dx * 0.15} y1={a[1] + ny * o + dy * 0.15} x2={a[0] + nx * o + dx * 0.62} y2={a[1] + ny * o + dy * 0.62} stroke={back ? shade(frame, 0.55) : shade(frame, 0.85)} strokeWidth={w * 0.55} strokeLinecap="round" />
        <line x1={a[0] + nx * o + dx * 0.55} y1={a[1] + ny * o + dy * 0.55} x2={a[0] + nx * o + dx * 0.85} y2={a[1] + ny * o + dy * 0.85} stroke="#b8c0cc" strokeOpacity={back ? 0.4 : 0.8} strokeWidth={w * 0.3} strokeLinecap="round" /></>}
    </g>;
  };
  // rim light = the part drawn once more, offset, in the rim colour, BEHIND the real part (plain function, not a component)
  const Rm = (children: (c: string | null) => React.ReactNode) =>
    <>{rim && <g transform={`translate(${rim.dx},${rim.dy})`}>{children(rim.color)}</g>}{children(null)}</>;

  const leg = (hip: number[], a: number[], back: boolean, k0: number) => {
    const k = fk(hip, 88, a[0]), ft = fk(k, 86, a[0] - a[1]), fr = -(a[0] - a[1]) * 0.25;
    return Rm((c) => <g>
      {bone(hip, k, 13, c, back)}{bone(k, ft, 12, c, back)}
      {/* wedge foot */}
      <path d={`M${ft[0] - 16} ${ft[1] + 9} L${ft[0] - 10} ${ft[1] - 6} L${ft[0] + 14} ${ft[1] - 6} L${ft[0] + 34} ${ft[1] + 9} Z`} fill={c ?? (back ? shade(frame, 0.55) : shade(frame, 0.8))} transform={`rotate(${fr} ${ft[0]} ${ft[1]})`} />
      {!c && has(k0) && <path d={`M${k[0] - 13} ${k[1] + 10} Q${k[0]} ${k[1] + 4} ${k[0] + 13} ${k[1] + 10} L${(k[0] + ft[0]) / 2 + 11} ${(k[1] + ft[1]) / 2 + 22} Q${(k[0] + ft[0]) / 2} ${(k[1] + ft[1]) / 2 + 28} ${(k[0] + ft[0]) / 2 - 11} ${(k[1] + ft[1]) / 2 + 22} Z`} fill={back ? shade(plate, 0.75) : `url(#${id}p)`} />}
      {!c && has(k0 + 1) && <ellipse cx={(hip[0] + k[0]) / 2} cy={(hip[1] + k[1]) / 2} rx={19} ry={34} fill={back ? shade(plate, 0.75) : `url(#${id}p)`} transform={`rotate(${-a[0]} ${(hip[0] + k[0]) / 2} ${(hip[1] + k[1]) / 2})`} />}
      {ball(k, 10, c)}{ball(ft, 7, c)}
    </g>);
  };
  const claw = (h: number[], ang: number, back: boolean, c: string | null) => {
    const grip = P.hold ? 1 : 0;
    return <g transform={`translate(${h[0]} ${h[1]}) rotate(${-ang})`}>
      <rect x={-9} y={-2} width={18} height={14} rx={4} fill={c ?? (back ? shade(frame, 0.6) : frame)} />
      {[-7, 0, 7].map((dx, i) => <path key={i} d={`M${dx} 10 L${dx * (1.4 - grip * 0.6)} 26 L${dx * (1.1 - grip * 0.8) + (i === 1 ? 0 : 0)} 34`} stroke={c ?? (back ? shade(frame, 0.6) : shade(frame, 0.9))} strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" fill="none" />)}
    </g>;
  };
  const arm = (s0: number[], a: number[], back: boolean, k0: number) => {
    const e = fk(s0, 78, a[0]), h = fk(e, 70, a[0] + a[1]);
    return Rm((c) => <g>
      {bone(s0, e, 12, c, back)}{bone(e, h, 11, c, back)}
      {!c && has(k0) && <ellipse cx={(e[0] + h[0]) / 2} cy={(e[1] + h[1]) / 2} rx={15} ry={30} fill={back ? shade(plate, 0.75) : `url(#${id}p)`} transform={`rotate(${-(a[0] + a[1])} ${(e[0] + h[0]) / 2} ${(e[1] + h[1]) / 2})`} />}
      {ball(e, 9, c)}{claw(h, a[0] + a[1], back, c)}
      {look.gun && !back && !c && (() => { const mx = (e[0] + h[0]) / 2, my = (e[1] + h[1]) / 2; return <g transform={`translate(${mx} ${my}) rotate(${-(a[0] + a[1])})`}>
        <rect x={-13} y={-22} width={26} height={44} rx={6} fill={shade(frame, 0.7)} /><rect x={-9} y={18} width={18} height={14} rx={3} fill={joint} /><circle cx={0} cy={30} r={6} fill={eyeC} opacity={0.8} /></g>; })()}
      {!c && has(k0 + 1) && <path d={`M${s0[0] - 22} ${s0[1] + 6} Q${s0[0] - 22} ${s0[1] - 22} ${s0[0]} ${s0[1] - 22} Q${s0[0] + 22} ${s0[1] - 22} ${s0[0] + 22} ${s0[1] + 6} Q${s0[0]} ${s0[1] + 18} ${s0[0] - 22} ${s0[1] + 6} Z`} fill={back ? shade(plate, 0.75) : `url(#${id}p)`} />}
      {(!has(k0 + 1) || c) && ball(s0, 12, c)}
    </g>);
  };

  // torso: spine + ribs + core; shell = chest plate with seams
  const spineTop = sh[1] - 6, coreY = sh[1] + 52, coreR = 15, glow = mode === "hostile" ? 1 : 0.7;
  const torso = Rm((c) => <g>
    {/* pelvis bowl */}
    <path d={`M-30 ${hipY - 14} Q0 ${hipY - 22} 30 ${hipY - 14} L22 ${hipY + 8} Q0 ${hipY + 16} -22 ${hipY + 8} Z`} fill={c ?? shade(frame, 0.85)} />
    {/* spine: vertebra blocks */}
    {Array.from({ length: 7 }, (_, i) => { const yy = hipY - 26 - i * ((hipY - 26 - spineTop) / 7); return <rect key={i} x={-9} y={yy - 9} width={18} height={12} rx={4} fill={c ?? (i % 2 ? shade(frame, 0.8) : frame)} />; })}
    {/* collar bar */}
    <path d={`M-38 ${sh[1] + 8} Q0 ${sh[1] - 6} 38 ${sh[1] + 8}`} stroke={c ?? frame} strokeWidth={11} strokeLinecap="round" fill="none" />
    {/* ribs: 4 C-shaped bars each side */}
    {!c && [0, 1, 2, 3].map(i => { const yy = sh[1] + 22 + i * 19, w = 40 - i * 4; return <path key={i} d={`M-6 ${yy} Q${-w - 6} ${yy - 6} ${-w + 2} ${yy + 12} M6 ${yy} Q${w + 6} ${yy - 6} ${w - 2} ${yy + 12}`} stroke={c ?? frame} strokeWidth={7} strokeLinecap="round" fill="none" />; })}
    {!c && <>
      {look.core !== false && <><circle cx={0} cy={coreY} r={coreR * 2.4} fill={eyeC} opacity={0.18 * glow} /><circle cx={0} cy={coreY} r={coreR} fill={eyeC} opacity={0.9} /><circle cx={-4} cy={coreY - 5} r={5} fill="#fff" opacity={0.8} /></>}
      {/* wires from core to collar */}
      <path d={`M-4 ${coreY - coreR} Q-20 ${sh[1] + 20} -28 ${sh[1] + 8}`} stroke="#c8402e" strokeWidth={3} fill="none" opacity={0.8} />
      <path d={`M4 ${coreY - coreR} Q22 ${sh[1] + 24} 30 ${sh[1] + 10}`} stroke="#3a8ac8" strokeWidth={3} fill="none" opacity={0.8} />
      {/* shell: chest plate + belly plate */}
      {has(1) && <path d={`M-40 ${sh[1] + 2} Q0 ${sh[1] - 14} 40 ${sh[1] + 2} Q50 ${sh[1] + 40} 36 ${sh[1] + 86} Q0 ${sh[1] + 100} -36 ${sh[1] + 86} Q-50 ${sh[1] + 40} -40 ${sh[1] + 2} Z`} fill={`url(#${id}p)`} />}
      {has(1) && <><path d={`M-30 ${sh[1] + 70} Q0 ${sh[1] + 80} 30 ${sh[1] + 70}`} stroke={shade(plate, 0.7)} strokeWidth={2.5} fill="none" />
        <circle cx={0} cy={coreY} r={11} fill={shade(plate, 0.8)} /><circle cx={0} cy={coreY} r={7} fill={eyeC} opacity={0.85} />
        {look.tag && <text x={0} y={sh[1] + 34} textAnchor="middle" transform={P.facing < 0 ? "scale(-1 1)" : undefined} fontFamily="Inter" fontWeight={900} fontSize={13} fill={shade(plate, 0.45)} letterSpacing={1}>{look.tag}</text>}</>}
      {has(2) && <path d={`M-30 ${sh[1] + 96} Q0 ${sh[1] + 106} 30 ${sh[1] + 96} L26 ${hipY - 6} Q0 ${hipY + 2} -26 ${hipY - 6} Z`} fill={`url(#${id}p)`} />}
      {/* cracked edge where the chest plate broke */}
      {!has(1) && shell > 0 && <path d={`M-40 ${sh[1] + 2} L-30 ${sh[1] + 14} L-36 ${sh[1] + 26} L-24 ${sh[1] + 34}`} stroke={plate} strokeWidth={6} fill="none" strokeLinejoin="bevel" />}
      {dmg > 0.3 && <path d={`M18 ${sh[1] + 40} l14 -4 l-6 10 l12 -2`} stroke="#ffd84a" strokeWidth={3} fill="none" opacity={0.5 + 0.5 * Math.abs(Math.sin(f * 1.7))} />}
    </>}
  </g>);

  // head: neck discs + capsule + visor + eye light (no jaw, no skull)
  const hc = [6, -362 + P.bob + hum * 0.6], hw = 64, hh = 52, talk = Math.max(0, Math.min(1, P.talk));
  const vx = hc[0] + 6, vy = hc[1] + 2;
  const headShell = has(3);
  const eyesG = (() => {
    const lx = P.look[0] * 9, ly = P.look[1] * 5, e = Math.max(0.08, P.eyes);
    if (mode === "hostile") return <g><rect x={vx - 40 + lx} y={vy - 4 * e + ly} width={80} height={8 * e} rx={4} fill={eyeC} /><rect x={vx - 52 + lx} y={vy - 12 + ly} width={104} height={24} rx={12} fill={eyeC} opacity={0.22} /></g>;
    if (mode === "scan") { const sx = Math.sin(f * 0.12) * 34; return <g><rect x={vx - 44} y={vy - 2} width={88} height={4} rx={2} fill={eyeC} opacity={0.35} /><circle cx={vx + sx} cy={vy} r={8 * e} fill={eyeC} /><circle cx={vx + sx} cy={vy} r={18} fill={eyeC} opacity={0.25} /></g>; }
    return <g>{[-1, 1].map(k => <g key={k}><circle cx={vx + k * 22 + lx} cy={vy + ly} r={12} fill={eyeC} opacity={0.25} /><ellipse cx={vx + k * 22 + lx} cy={vy + ly} rx={8} ry={9 * e} fill={eyeC} /><circle cx={vx + k * 22 + lx - 2} cy={vy + ly - 3} r={2.5} fill="#fff" opacity={0.9} /></g>)}</g>;
  })();
  const headG = <g transform={`rotate(${P.head} ${hc[0]} ${hc[1] + 44})`}>
    {Rm((c) => <g>
      {[0, 1, 2].map(i => <rect key={i} x={-12 + i} y={hc[1] + 40 + i * 9} width={24 - i * 2} height={7} rx={3} fill={c ?? (i % 2 ? shade(frame, 0.75) : frame)} />)}
      <rect x={hc[0] - hw} y={hc[1] - hh} width={hw * 2} height={hh * 2} rx={46} fill={c ?? (headShell ? `url(#${id}p)` : `url(#${id}f)`)} />
    </g>)}
    {/* side ear disc with a ring light */}
    <circle cx={hc[0] - hw + 4} cy={hc[1] + 2} r={14} fill={headShell ? shade(plate, 0.8) : joint} /><circle cx={hc[0] - hw + 4} cy={hc[1] + 2} r={8} fill="none" stroke={eyeC} strokeWidth={3} opacity={0.8} />
    {!headShell && <>{[-30, -10, 10, 30].map(dx => <line key={dx} x1={hc[0] + dx} y1={hc[1] - hh + 8} x2={hc[0] + dx} y2={hc[1] - hh + 22} stroke={shade(frame, 0.6)} strokeWidth={4} strokeLinecap="round" />)}</>}
    {/* visor */}
    <rect x={vx - 54} y={vy - 24} width={108} height={48} rx={22} fill="#0b0e14" />
    <rect x={vx - 46} y={vy - 20} width={44} height={6} rx={3} fill="#fff" opacity={0.12} />
    {eyesG}
    {look.smiley && <path d={`M${vx - 18} ${vy + 12} Q${vx} ${vy + 22} ${vx + 18} ${vy + 12}`} stroke="#f4f1e8" strokeWidth={3.5} fill="none" strokeLinecap="round" opacity={0.85} />}
    {/* talking: equaliser bars under the eyes */}
    {talk > 0.06 && [-2, -1, 0, 1, 2].map(i => { const hgt = 3 + 10 * talk * (0.5 + 0.5 * Math.abs(Math.sin(f * 0.9 + i * 1.3))); return <rect key={i} x={vx + i * 8 - 3} y={vy + 16 - hgt / 2} width={5} height={hgt} rx={2} fill={eyeC} opacity={0.85} />; })}
    {dmg > 0.5 && <path d={`M${vx + 20} ${vy - 24} l-8 14 l10 6 l-6 14`} stroke="#d8e4f0" strokeWidth={2.5} fill="none" opacity={0.8} />}
    {dmg > 0 && [0, 1, 2].map(i => <line key={i} x1={hc[0] - 40 + i * 30} y1={hc[1] - 30 + i * 6} x2={hc[0] - 28 + i * 30} y2={hc[1] - 36 + i * 6} stroke="#000" strokeOpacity={0.3 * dmg} strokeWidth={2} />)}
    {/* spec highlight */}
    <ellipse cx={hc[0] + 26} cy={hc[1] - 36} rx={16} ry={7} fill="#fff" opacity={0.3} transform={`rotate(-14 ${hc[0] + 26} ${hc[1] - 36})`} />
  </g>;
  const upper = <g transform={`rotate(${P.lean} 0 ${hipY})`}>{arm(shL, P.aL, true, 10)}{torso}{headG}{look.noArmR ? <g>{ball(shR, 12, null)}<path d={`M${shR[0]} ${shR[1]} q8 14 2 26 M${shR[0]} ${shR[1]} q-6 16 4 22`} stroke="#c8402e" strokeWidth={3} fill="none" /><path d={`M${shR[0] + 2} ${shR[1] + 22} l6 6`} stroke="#ffd84a" strokeWidth={3} opacity={0.5 + 0.5 * Math.abs(Math.sin(f * 1.3))} /></g> : arm(shR, P.aR, false, 12)}</g>;
  // night pass: the eyes + core again, unfiltered and blurred into a halo, on top of the darkened body
  const dark = look.dark ?? 0, nightC = look.night ?? "#0e1422";
  const glowPass = dark > 0 && <g transform={`rotate(${P.lean} 0 ${hipY})`}>
    {look.core !== false && <><circle cx={0} cy={coreY} r={coreR * 2.2} fill={eyeC} opacity={0.5 * dark} filter={`url(#${id}b)`} /><circle cx={0} cy={coreY} r={coreR * 0.8} fill={eyeC} opacity={0.9 * dark} /></>}
    <g transform={`rotate(${P.head} ${hc[0]} ${hc[1] + 44})`}><ellipse cx={vx} cy={vy} rx={90} ry={44} fill={eyeC} opacity={0.35 * dark} filter={`url(#${id}b)`} /><g filter={`url(#${id}b)`} opacity={dark}>{eyesG}{eyesG}</g>{eyesG}</g>
  </g>;
  return <g transform={`translate(${x} ${y}) rotate(${rot}) scale(${s * (look.scale ?? 1) * P.facing} ${s * (look.scale ?? 1)})`} opacity={opacity}>
    <defs>
      <linearGradient id={`${id}p`} x1="0.2" y1="0" x2="0.8" y2="1"><stop offset="0" stopColor="#ffffff" /><stop offset="0.5" stopColor={plate} /><stop offset="1" stopColor={shade(plate, 0.78)} /></linearGradient>
      <linearGradient id={`${id}f`} x1="0.2" y1="0" x2="0.8" y2="1"><stop offset="0" stopColor={shade(frame, 1.5)} /><stop offset="0.5" stopColor={frame} /><stop offset="1" stopColor={shade(frame, 0.6)} /></linearGradient>
      <filter id={`${id}b`} x="-1" y="-1" width="3" height="3"><feGaussianBlur stdDeviation={9} /></filter>
      <filter id={`${id}d`}><feColorMatrix type="matrix" values={(() => { const n = parseInt(nightC.slice(1), 16), k = 1 - 0.85 * dark;
        const cr = ((n >> 16) & 255) / 255 * (1 - k), cg = ((n >> 8) & 255) / 255 * (1 - k), cb = (n & 255) / 255 * (1 - k);
        return `${k} 0 0 0 ${cr} 0 ${k} 0 0 ${cg} 0 0 ${k} 0 ${cb} 0 0 0 1 0`; })()} /></filter>
    </defs>
    <ellipse cx={4} cy={6} rx={56} ry={10} fill="#000" opacity={0.28} />
    <g filter={dark > 0 ? `url(#${id}d)` : undefined}>{leg(hipL, P.lL, true, 20)}{leg(hipR, P.lR, false, 22)}{upper}</g>{glowPass}
  </g>;
};

// handy presets
export const HELPER: RobotLook = { shell: 1, mode: "calm", tag: "ORIN" };
export const HUNTER: RobotLook = { shell: 0, mode: "hostile", frame: "#2e333c", scale: 1.12 };
