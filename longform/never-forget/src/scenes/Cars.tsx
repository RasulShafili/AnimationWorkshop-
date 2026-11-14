// Vehicles drawn properly (lessons from flat-vector car references): wheel arches cut into the body, big tyres with
// multi-spoke silver rims, a shoulder crease splitting a light upper body from a darker lower body, dark bumpers and
// sills, tinted glass with a reflection streak, black pillars, side mirror, swept headlight, wrap-around tail light.
// All side views are drawn facing RIGHT in local space; origin = ground under the rear bumper. Length ≈ 780.
import React from "react";

let n = 0; const uid = (p: string) => `${p}${++n}`;

export const Wheel: React.FC<{ cx: number; cy: number; r: number; rot?: number; rim?: string; hub?: string }> = ({ cx, cy, r, rot = 0, rim = "#c9cfd8", hub = "#7d8591" }) => <g>
  <circle cx={cx} cy={cy} r={r} fill="#16171c" />
  <circle cx={cx} cy={cy} r={r * 0.92} fill="none" stroke="#2a2c33" strokeWidth={r * 0.06} />
  <circle cx={cx} cy={cy} r={r * 0.62} fill={rim} />
  <circle cx={cx} cy={cy} r={r * 0.62} fill="none" stroke="#8a929e" strokeWidth={r * 0.05} />
  <g transform={`rotate(${rot} ${cx} ${cy})`}>
    {[0, 72, 144, 216, 288].map(a => <path key={a} transform={`rotate(${a} ${cx} ${cy})`} d={`M${cx - r * 0.07} ${cy - r * 0.14} L${cx - r * 0.13} ${cy - r * 0.56} L${cx + r * 0.13} ${cy - r * 0.56} L${cx + r * 0.07} ${cy - r * 0.14} Z`} fill="#e9edf2" stroke="#9aa2ae" strokeWidth={1.5} />)}
    {[36, 108, 180, 252, 324].map(a => <circle key={a} cx={cx + Math.sin(a * Math.PI / 180) * r * 0.4} cy={cy - Math.cos(a * Math.PI / 180) * r * 0.4} r={r * 0.09} fill="#5d646e" />)}
  </g>
  <circle cx={cx} cy={cy} r={r * 0.16} fill={hub} /><circle cx={cx} cy={cy} r={r * 0.07} fill="#d8dde4" />
  <path d={`M${cx - r * 0.5} ${cy - r * 0.35} A${r * 0.62} ${r * 0.62} 0 0 1 ${cx + r * 0.2} ${cy - r * 0.58}`} stroke="#fff" strokeOpacity={0.5} strokeWidth={r * 0.05} fill="none" />
</g>;

// silver hatchback (the hit-and-run car). Dent on the rear door; air freshener on the rear-view mirror.
export const HATCH = { dent: [228, -132], fresh: [528, -232], len: 780 };
export const Hatchback: React.FC<{ color?: string; wheelRot?: number; bounce?: number }> = ({ color = "#c3cad4", wheelRot = 0, bounce = 0 }) => {
  const id = React.useMemo(() => uid("hb"), []);
  const R = 62, wb = [150, 610], wy = -R;
  // body silhouette with arch cut-outs (arches = circles of radius 76 around the wheels)
  const body = `M8 -66 L4 -150 Q6 -178 34 -190 L120 -206 Q150 -212 176 -230 L276 -300 Q300 -314 340 -314 L480 -314 Q520 -312 548 -290 L628 -222 L716 -206 Q760 -198 770 -160 L776 -100 Q778 -70 760 -66
    L${wb[1] + 80} -66 A80 80 0 0 0 ${wb[1] - 80} -66 L${wb[0] + 80} -66 A80 80 0 0 0 ${wb[0] - 80} -66 Z`;
  return <g transform={`translate(0 ${bounce})`}>
    <ellipse cx={390} cy={4 - bounce} rx={430} ry={24} fill="#000" opacity={0.4} />
    <defs>
      <linearGradient id={`${id}b`} x1="0" y1="-314" x2="0" y2="-60" gradientUnits="userSpaceOnUse">
        <stop offset="0" stopColor="#f2f5f9" /><stop offset="0.42" stopColor={color} /><stop offset="0.44" stopColor="#9aa3af" /><stop offset="1" stopColor="#6d7682" /></linearGradient>
      <linearGradient id={`${id}g`} x1="0" y1="-300" x2="0" y2="-210" gradientUnits="userSpaceOnUse"><stop offset="0" stopColor="#6a7f96" /><stop offset="1" stopColor="#24303d" /></linearGradient>
    </defs>
    {/* arches (dark inner wheel wells) */}
    {wb.map(x => <path key={x} d={`M${x - 80} -66 A80 80 0 0 1 ${x + 80} -66 Z`} fill="#1a1c22" />)}
    <path d={body} fill={`url(#${id}b)`} />
    {/* shoulder crease + lower sill + bumpers */}
    <path d="M12 -150 Q300 -168 772 -150" stroke="#ffffff" strokeOpacity={0.55} strokeWidth={4} fill="none" />
    <path d="M12 -146 Q300 -164 772 -146" stroke="#59616c" strokeOpacity={0.6} strokeWidth={3} fill="none" />
    <path d={`M${wb[0] + 84} -66 L${wb[1] - 84} -66 L${wb[1] - 88} -84 L${wb[0] + 88} -84 Z`} fill="#3b4048" />
    <path d="M4 -112 L4 -70 Q6 -64 20 -64 L68 -64 A80 80 0 0 1 72 -92 L10 -112 Z" fill="#3b4048" />
    <path d="M776 -110 L778 -76 Q774 -64 760 -64 L692 -64 A80 80 0 0 0 688 -94 Z" fill="#3b4048" />
    {/* windows: rear quarter, rear door, front door; pillars */}
    <path d="M150 -214 L184 -224 L266 -292 Q286 -302 300 -302 L300 -214 Z" fill={`url(#${id}g)`} />
    <path d="M316 -214 L316 -302 L470 -302 Q506 -300 530 -282 L604 -222 L604 -214 Z" fill={`url(#${id}g)`} />
    <rect x={300} y={-306} width={16} height={96} fill="#22252c" />
    <path d="M452 -302 L466 -302 L466 -214 L452 -214 Z" fill="#22252c" opacity={0.85} />
    <path d="M330 -290 L400 -290 L360 -222 L330 -222 Z M410 -290 L432 -290 L392 -222 L370 -222 Z" fill="#fff" opacity={0.13} />
    <path d="M196 -228 L240 -264 L250 -258 L210 -224 Z" fill="#fff" opacity={0.12} />
    <path d="M150 -210 L604 -210" stroke="#22252c" strokeWidth={6} />
    {/* rear-view mirror inside + air freshener hanging from it */}
    <rect x={508} y={-298} width={36} height={11} rx={4} fill="#14161b" />
    <line x1={528} y1={-287} x2={528} y2={-262} stroke="#e8e8e8" strokeWidth={2} />
    <path d="M528 -262 L512 -236 L519 -236 L507 -216 L549 -216 L537 -236 L544 -236 Z" fill="#2fa354" stroke="#1d6e37" strokeWidth={2} />
    {/* side mirror */}
    <path d="M590 -222 Q600 -246 628 -244 L636 -222 Z" fill={color} stroke="#59616c" strokeWidth={2} /><path d="M596 -226 L630 -228" stroke="#22252c" strokeWidth={3} />
    {/* doors, handles, fuel cap */}
    <path d="M308 -214 L306 -84 M600 -214 Q606 -150 588 -86 M156 -212 Q146 -170 168 -130" stroke="#59616c" strokeWidth={3} fill="none" />
    <rect x={262} y={-176} width={34} height={8} rx={4} fill="#59616c" /><rect x={548} y={-176} width={34} height={8} rx={4} fill="#59616c" />
    <circle cx={110} cy={-168} r={11} fill="none" stroke="#59616c" strokeWidth={2.5} />
    {/* the dent on the rear door (behind the B-pillar → back door) */}
    <path d="M196 -152 Q228 -126 262 -150 Q274 -120 240 -104 Q212 -110 196 -152 Z" fill="#6b7480" opacity={0.85} />
    <path d="M206 -146 Q229 -130 254 -146" stroke="#f4f6fa" strokeWidth={3} fill="none" opacity={0.9} />
    <path d="M214 -116 Q232 -110 246 -116" stroke="#4a515c" strokeWidth={2} fill="none" opacity={0.8} />
    {/* lights */}
    <path d="M6 -176 Q8 -186 30 -190 L48 -192 L46 -140 L6 -132 Z" fill="#c8302c" /><path d="M12 -178 L42 -184 L42 -170 L12 -164 Z" fill="#ff8a7a" opacity={0.7} />
    <path d="M722 -200 Q760 -194 768 -168 L726 -162 Q716 -180 722 -200 Z" fill="#fdf6d8" stroke="#8a929e" strokeWidth={2} />
    <path d="M770 -140 L776 -112 L740 -112 Z" fill="#e8a33a" opacity={0.85} />
    {/* roof rail + antenna */}
    <path d="M300 -318 L480 -318" stroke="#59616c" strokeWidth={5} strokeLinecap="round" /><path d="M200 -244 L176 -290" stroke="#22252c" strokeWidth={3} />
    {wb.map(x => <Wheel key={x} cx={x} cy={wy} r={R} rot={wheelRot} />)}
  </g>;
};

// rear view of the same hatchback: plate in the recess on the tailgate, wrap-around tail lights, bumper, mirrors
export const HatchRear: React.FC<{ color?: string }> = ({ color = "#c3cad4" }) => {
  const id = React.useMemo(() => uid("hr"), []);
  return <g>
    <defs>
      <linearGradient id={`${id}b`} x1="0" y1="-440" x2="0" y2="-40" gradientUnits="userSpaceOnUse"><stop offset="0" stopColor="#eef2f6" /><stop offset="0.5" stopColor={color} /><stop offset="0.52" stopColor="#a2aab5" /><stop offset="1" stopColor="#6d7682" /></linearGradient>
      <linearGradient id={`${id}g`} x1="0" y1="-420" x2="0" y2="-300" gradientUnits="userSpaceOnUse"><stop offset="0" stopColor="#6a7f96" /><stop offset="1" stopColor="#202a36" /></linearGradient>
    </defs>
    <ellipse cx={0} cy={4} rx={360} ry={26} fill="#000" opacity={0.45} />
    {/* tyres under the body */}
    <rect x={-318} y={-120} width={92} height={122} rx={20} fill="#16171c" /><rect x={226} y={-120} width={92} height={122} rx={20} fill="#16171c" />
    {/* side mirrors */}
    <path d="M-330 -300 L-386 -312 Q-400 -300 -390 -280 L-330 -282 Z" fill={color} stroke="#59616c" strokeWidth={2} /><path d="M330 -300 L386 -312 Q400 -300 390 -280 L330 -282 Z" fill={color} stroke="#59616c" strokeWidth={2} />
    {/* body: wide lower part, narrower glasshouse */}
    <path d="M-336 -70 L-342 -250 Q-338 -292 -300 -302 L-250 -312 Q-226 -420 -150 -432 L150 -432 Q226 -420 250 -312 L300 -302 Q338 -292 342 -250 L336 -70 Q0 -56 -336 -70 Z" fill={`url(#${id}b)`} />
    {/* rear window + spoiler */}
    <path d="M-220 -318 Q-206 -404 -146 -414 L146 -414 Q206 -404 220 -318 Z" fill={`url(#${id}g)`} />
    <path d="M-150 -400 L-30 -400 L-90 -326 L-190 -326 Z" fill="#fff" opacity={0.1} />
    <path d="M-160 -428 L160 -428" stroke="#22252c" strokeWidth={10} strokeLinecap="round" />
    <rect x={-20} y={-424} width={40} height={8} rx={3} fill="#c8302c" />
    {/* shoulder crease */}
    <path d="M-338 -236 Q0 -252 338 -236" stroke="#fff" strokeOpacity={0.5} strokeWidth={4} fill="none" />
    {/* wrap-around tail lights */}
    <path d="M-340 -270 Q-336 -296 -300 -300 L-212 -300 Q-200 -270 -214 -246 L-338 -232 Z" fill="#c8302c" />
    <path d="M340 -270 Q336 -296 300 -300 L212 -300 Q200 -270 214 -246 L338 -232 Z" fill="#c8302c" />
    <path d="M-326 -284 L-226 -288 L-228 -274 L-326 -266 Z M326 -284 L226 -288 L228 -274 L326 -266 Z" fill="#ff8a7a" opacity={0.7} />
    {/* tailgate handle + badge + plate recess */}
    <path d="M-150 -224 L150 -224 L136 -146 L-136 -146 Z" fill="#9aa3af" />
    <rect x={-112} y={-212} width={224} height={58} rx={6} fill="#f4f1e6" stroke="#20242c" strokeWidth={4} />
    <text x={0} y={-169} fontFamily="Inter" fontWeight={900} fontSize={44} fill="#1a2a6a" textAnchor="middle" letterSpacing={2}>7KR·419</text>
    <rect x={-40} y={-246} width={80} height={10} rx={5} fill="#59616c" />
    {/* bumper */}
    <path d="M-340 -124 L340 -124 L334 -66 Q0 -54 -334 -66 Z" fill="#3b4048" />
    <rect x={-300} y={-112} width={60} height={14} rx={4} fill="#c8302c" opacity={0.8} /><rect x={240} y={-112} width={60} height={14} rx={4} fill="#c8302c" opacity={0.8} />
    <rect x={180} y={-80} width={46} height={16} rx={8} fill="#16171c" />
  </g>;
};

// police sedan (three-box), black-and-white livery, lightbar. Facing RIGHT in local space.
export const PoliceCar: React.FC<{ f: number; wheelRot?: number }> = ({ f, wheelRot = 0 }) => {
  const id = React.useMemo(() => uid("pc"), []);
  const R = 60, wb = [160, 640];
  const red = f % 16 < 8, blue = !red;
  const body = `M6 -70 L2 -166 Q4 -186 30 -192 L150 -206 L230 -288 Q252 -304 290 -304 L470 -304 Q506 -302 528 -284 L606 -210 L760 -196 Q800 -188 808 -160 L812 -104 Q812 -72 792 -70
    L${wb[1] + 80} -70 A80 80 0 0 0 ${wb[1] - 80} -70 L${wb[0] + 80} -70 A80 80 0 0 0 ${wb[0] - 80} -70 Z`;
  return <g>
    <defs>
      <clipPath id={`${id}c`}><path d={body} /></clipPath>
      <linearGradient id={`${id}g`} x1="0" y1="-300" x2="0" y2="-212" gradientUnits="userSpaceOnUse"><stop offset="0" stopColor="#6a7f96" /><stop offset="1" stopColor="#1e2834" /></linearGradient>
      <linearGradient id={`${id}s`} x1="0" y1="-310" x2="0" y2="-70" gradientUnits="userSpaceOnUse"><stop offset="0" stopColor="#fff" stopOpacity={0.25} /><stop offset="0.5" stopColor="#fff" stopOpacity={0} /><stop offset="1" stopColor="#000" stopOpacity={0.3} /></linearGradient>
    </defs>
    <ellipse cx={410} cy={4} rx={450} ry={24} fill="#000" opacity={0.45} />
    {wb.map(x => <path key={x} d={`M${x - 80} -70 A80 80 0 0 1 ${x + 80} -70 Z`} fill="#121318" />)}
    <g clipPath={`url(#${id}c)`}>
      <rect x={0} y={-320} width={820} height={260} fill="#f4f5f7" />
      {/* black hood/front fender and trunk/rear fender, black lower body */}
      <path d="M560 -320 L820 -320 L820 -60 L620 -60 Q600 -140 560 -210 Z" fill="#17181d" />
      <path d="M0 -320 L210 -320 L196 -210 Q170 -140 150 -60 L0 -60 Z" fill="#17181d" />
      <rect x={0} y={-118} width={820} height={60} fill="#17181d" />
      <rect x={0} y={-320} width={820} height={260} fill={`url(#${id}s)`} />
    </g>
    {/* glass + pillars */}
    <path d="M178 -212 L244 -280 Q262 -292 290 -292 L336 -292 L336 -212 Z" fill={`url(#${id}g)`} />
    <path d="M352 -212 L352 -292 L466 -292 Q498 -290 518 -274 L582 -212 Z" fill={`url(#${id}g)`} />
    <rect x={336} y={-296} width={16} height={86} fill="#17181d" />
    <path d="M362 -282 L420 -282 L388 -222 L362 -222 Z" fill="#fff" opacity={0.12} />
    <path d="M178 -208 L590 -208" stroke="#17181d" strokeWidth={6} />
    {/* doors + lettering + star badge */}
    <path d="M344 -208 L342 -116 M594 -206 Q600 -160 586 -118 M176 -206 Q168 -160 176 -118" stroke="#9aa0aa" strokeWidth={3} fill="none" />
    <text x={470} y={-146} fontFamily="Inter" fontWeight={900} fontSize={40} fill="#1b2a5a" textAnchor="middle" letterSpacing={3}>POLICE</text>
    <g transform="translate(262 -160)"><path d="M0 -30 L9 -10 L30 -9 L14 5 L19 26 L0 15 L-19 26 L-14 5 L-30 -9 L-9 -10 Z" fill="#d8a838" stroke="#8a6a1a" strokeWidth={2.5} /><circle r={7} fill="#1b2a5a" /></g>
    <rect x={300} y={-190} width={30} height={7} rx={3} fill="#9aa0aa" /><rect x={540} y={-190} width={30} height={7} rx={3} fill="#9aa0aa" />
    {/* lights, push bar, mirror */}
    <path d="M8 -178 Q10 -188 30 -190 L46 -192 L44 -146 L6 -140 Z" fill="#c8302c" />
    <path d="M764 -192 Q800 -186 806 -164 L766 -158 Q756 -176 764 -192 Z" fill="#fdf6d8" />
    <path d="M812 -150 L840 -150 L840 -80 L812 -80" stroke="#2a2b31" strokeWidth={10} fill="none" strokeLinejoin="round" /><line x1={812} y1={-115} x2={840} y2={-115} stroke="#2a2b31" strokeWidth={8} />
    <path d="M578 -214 Q586 -236 612 -234 L620 -214 Z" fill="#17181d" />
    {/* lightbar */}
    <rect x={300} y={-326} width={180} height={22} rx={6} fill="#1d1e24" />
    <rect x={306} y={-322} width={80} height={14} rx={4} fill={red ? "#ff3a3a" : "#5a1414"} /><rect x={394} y={-322} width={80} height={14} rx={4} fill={blue ? "#3a7aff" : "#141c4a"} />
    {red && <ellipse cx={346} cy={-316} rx={120} ry={40} fill="#ff3a3a" opacity={0.25} style={{ filter: "blur(12px)" }} />}
    {blue && <ellipse cx={434} cy={-316} rx={120} ry={40} fill="#3a7aff" opacity={0.25} style={{ filter: "blur(12px)" }} />}
    {wb.map(x => <Wheel key={x} cx={x} cy={-R} r={R} rot={wheelRot} rim="#2a2c33" hub="#4a4e56" />)}
  </g>;
};
