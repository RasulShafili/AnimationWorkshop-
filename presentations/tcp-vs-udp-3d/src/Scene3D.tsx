import React, { useMemo } from "react";
import * as THREE from "three";
import { useThree } from "@react-three/fiber";
import { RoundedBoxGeometry } from "three/examples/jsm/geometries/RoundedBoxGeometry.js";
import T from "./timing.json";
import { SEC, HS, DV, UD, HOL, secIndex } from "./timing";

const sat = (v: number) => Math.min(1, Math.max(0, v));
const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
const ease = (t: number) => { t = sat(t); return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
const TRAVEL = T.travel;
export const TCP_C = "#2ec4ff", UDP_C = "#ff8a2e", ACK_C = "#3ee08a", LOST_C = "#ff4a5a";

// ---------- text labels as camera-facing sprites (font loaded before render, see Video.tsx) ----------
const texCache = new Map<string, THREE.CanvasTexture>();
const labelTex = (text: string, color: string, bg: string | null) => {
  const key = text + color + bg; let t = texCache.get(key);
  if (t) return t;
  const c = document.createElement("canvas"), ctx = c.getContext("2d")!;
  const font = "700 64px Inter, Arial, sans-serif"; ctx.font = font;
  const w = Math.ceil(ctx.measureText(text).width) + 48; c.width = w; c.height = 96;
  ctx.font = font; ctx.textBaseline = "middle"; ctx.textAlign = "center";
  if (bg) { ctx.fillStyle = bg; const r = 24; ctx.beginPath(); ctx.roundRect(4, 8, w - 8, 80, r); ctx.fill(); }
  ctx.fillStyle = color; ctx.fillText(text, w / 2, 50);
  t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; texCache.set(key, t);
  return t;
};
export const Label: React.FC<{ text: string; pos: [number, number, number]; color?: string; bg?: string | null; h?: number; opacity?: number }> = ({ text, pos, color = "#ffffff", bg = "rgba(10,14,32,0.85)", h = 0.32, opacity = 1 }) => {
  const tex = labelTex(text, color, bg), img = tex.image as HTMLCanvasElement;
  return <sprite position={pos} scale={[h * img.width / img.height, h, 1]}><spriteMaterial map={tex} transparent opacity={opacity} depthWrite={false} depthTest={false} /></sprite>;
};

// ---------- props ----------
const Laptop: React.FC<{ pos: [number, number, number]; f: number; label: string; showLabel: boolean }> = ({ pos, f, label, showLabel }) => (
  <group position={pos}>
    <mesh position={[0, 0.4, 0]} castShadow receiveShadow><boxGeometry args={[1.8, 0.8, 1.2]} /><meshStandardMaterial color="#3a4468" roughness={0.55} metalness={0.3} /></mesh>
    <group position={[0, 0.82, 0]}>
      <mesh castShadow><boxGeometry args={[1.5, 0.06, 1.0]} /><meshStandardMaterial color="#8a96b8" roughness={0.3} metalness={0.6} /></mesh>
      <group position={[0, 0.03, -0.48]} rotation={[-0.32, 0, 0]}>
        <mesh position={[0, 0.48, 0]} castShadow><boxGeometry args={[1.5, 0.96, 0.05]} /><meshStandardMaterial color="#8a96b8" roughness={0.3} metalness={0.6} /></mesh>
        <mesh position={[0, 0.48, 0.03]}><planeGeometry args={[1.36, 0.82]} /><meshBasicMaterial color="#123a66" /></mesh>
        {[0, 1, 2, 3, 4].map(i => <mesh key={i} position={[-0.35 + ((i * 37) % 30) / 100, 0.75 - i * 0.13, 0.035]}><planeGeometry args={[0.5 + ((i * 53) % 40) / 100, 0.04]} /><meshBasicMaterial color={i === Math.floor(f / 12) % 5 ? TCP_C : "#2a5a8a"} /></mesh>)}
      </group>
    </group>
    {showLabel && <Label text={label} pos={[0, -0.25, 0.9]} color="#cfe0ff" h={0.3} />}
  </group>
);

const Rack: React.FC<{ pos: [number, number, number]; f: number; label: string; showLabel: boolean }> = ({ pos, f, label, showLabel }) => (
  <group position={pos}>
    <mesh position={[0, 1.3, 0]} castShadow receiveShadow><boxGeometry args={[1.3, 2.6, 1.1]} /><meshStandardMaterial color="#3a4468" roughness={0.45} metalness={0.4} /></mesh>
    {Array.from({ length: 8 }, (_, i) => (
      <group key={i} position={[0, 0.3 + i * 0.29, 0.56]}>
        <mesh><boxGeometry args={[1.1, 0.22, 0.02]} /><meshStandardMaterial color="#56628a" roughness={0.35} metalness={0.6} /></mesh>
        {[0, 1, 2].map(k => <mesh key={k} position={[0.38 + k * 0.08, 0, 0.015]}><boxGeometry args={[0.04, 0.04, 0.01]} /><meshBasicMaterial color={Math.sin(f * 0.3 + i * 1.7 + k * 2.1) > 0.1 ? (k === 2 ? "#ffcc4a" : ACK_C) : "#1a3a2a"} /></mesh>)}
      </group>
    ))}
    {showLabel && <Label text={label} pos={[0, -0.25, 0.9]} color="#cfe0ff" h={0.3} />}
  </group>
);

// packet path: an arc from client (left) to server (right); lane z offsets separate traffic
const CL = new THREE.Vector3(-3.6, 1.35, 0), SV = new THREE.Vector3(3.6, 1.6, 0);
export const pathAt = (t: number, lane = 0, lift = 1) => {
  const p = new THREE.Vector3().lerpVectors(CL, SV, t);
  p.y += Math.sin(t * Math.PI) * 0.9 * lift; p.z += lane; return p;
};
const Cable: React.FC<{ lane: number; color: string; glow: number }> = ({ lane, color, glow }) => {
  const geo = useMemo(() => new THREE.TubeGeometry(new THREE.CatmullRomCurve3(Array.from({ length: 24 }, (_, i) => pathAt(i / 23, lane).add(new THREE.Vector3(0, -0.22, 0)))), 64, 0.03, 8, false), [lane]);
  return <mesh geometry={geo}><meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.2 + glow} roughness={0.4} /></mesh>;
};

const boxGeo = new RoundedBoxGeometry(0.42, 0.3, 0.3, 3, 0.06);
const Packet: React.FC<{ p: THREE.Vector3; color: string; label?: string; scale?: number; rot?: number; opacity?: number }> = ({ p, color, label, scale = 1, rot = 0, opacity = 1 }) => (
  <group position={p.toArray()} scale={scale} rotation={[rot, rot * 0.7, rot * 0.3]}>
    <mesh geometry={boxGeo} castShadow><meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.55} roughness={0.3} metalness={0.1} transparent={opacity < 1} opacity={opacity} /></mesh>
    <pointLight color={color} intensity={0.6 * opacity} distance={1.6} />
    {label && <Label text={label} pos={[0, 0.36, 0]} color="#ffffff" bg="rgba(10,14,32,0.8)" h={0.24} opacity={opacity} />}
  </group>
);
// forward packet at local frame l sent at s
const fwd = (l: number, s: number, lane = 0) => { const t = (l - s) / TRAVEL; return t >= 0 && t <= 1 ? pathAt(ease(t), lane) : null; };
const back = (l: number, s: number, lane = 0.45) => { const t = (l - s) / TRAVEL; return t >= 0 && t <= 1 ? pathAt(1 - ease(t), lane, 0.6) : null; };

const TimerRing: React.FC<{ p: number; alarm: boolean; pos: [number, number, number] }> = ({ p, alarm, pos }) => (
  <group position={pos}>
    <mesh><torusGeometry args={[0.32, 0.035, 8, 48]} /><meshBasicMaterial color="#2a3350" /></mesh>
    <mesh rotation={[0, 0, Math.PI / 2]} scale={[1, -1, 1]}><torusGeometry args={[0.32, 0.05, 8, 48, Math.max(0.001, p * Math.PI * 2)]} /><meshBasicMaterial color={alarm ? LOST_C : p > 0.75 ? "#ffcc4a" : TCP_C} /></mesh>
    <Label text={alarm ? "Taymer bitdi!" : "Taymer"} pos={[0, 0.55, 0]} color={alarm ? "#ff8a96" : "#cfe0ff"} h={0.22} />
  </group>
);

const Buffer: React.FC<{ have: number[]; pos: [number, number, number] }> = ({ have, pos }) => (
  <group position={pos}>
    {[1, 2, 3, 4].map((n, i) => {
      const got = have.includes(n);
      return (
        <group key={n} position={[(i - 1.5) * 0.36, 0, 0]}>
          <mesh><boxGeometry args={[0.3, 0.22, 0.22]} /><meshStandardMaterial color={got ? TCP_C : "#1a2238"} emissive={got ? TCP_C : "#000000"} emissiveIntensity={got ? 0.5 : 0} transparent opacity={got ? 1 : 0.5} /></mesh>
          <Label text={String(n)} pos={[0, 0.25, 0]} color={got ? "#ffffff" : "#5a6a8a"} bg={null} h={0.2} />
        </group>
      );
    })}
    <Label text="Qəbul buferi" pos={[0, 0.52, 0]} color="#cfe0ff" h={0.2} />
  </group>
);

// ---------- scene ----------
export const Scene3D: React.FC<{ f: number }> = ({ f }) => {
  const { camera } = useThree();
  const si = secIndex(f), l = f - SEC[si];
  // camera rig per section: [pos, target]; the diagram panel sits on the right, so the stage shifts left when it's shown
  const RIG: [number[], number[]][] = [
    [[0, 3.0, 10.5], [0, 2.3, 0]], [[0, 3.4, 10.2], [0, 1.5, 0]], [[0, 3.6, 11.6], [0, 1.5, 0]], [[0, 3.9, 12.4], [0, 1.9, 0]],
    [[0, 4.0, 13.6], [0, 1.7, 0]], [[0, 4.8, 10.8], [0, 1.2, 0]], [[0, 3.6, 10.5], [0, 1.4, 0]], [[0, 5.5, 12], [0, 1.2, 0]],
  ];
  const DIAG = [0, 0.25, 1, 1, 1, 0, 0, 0]; // fraction of the right-panel shift per section
  const k = sat(l / 30), prev = RIG[Math.max(0, si - 1)], cur = RIG[si], e = ease(k);
  const orbit = Math.sin(f * 0.004) * 0.6;
  camera.position.set(lerp(prev[0][0], cur[0][0], e) + orbit, lerp(prev[0][1], cur[0][1], e), lerp(prev[0][2], cur[0][2], e));
  camera.lookAt(lerp(prev[1][0], cur[1][0], e), lerp(prev[1][1], cur[1][1], e), lerp(prev[1][2], cur[1][2], e));
  const shift = lerp(DIAG[Math.max(0, si - 1)], DIAG[si], e) * 400;
  const pc = camera as THREE.PerspectiveCamera;
  if (shift > 0.5) pc.setViewOffset(1920, 1080, shift, 0, 1920, 1080); else pc.clearViewOffset();
  pc.updateProjectionMatrix();
  const showLabels = si < 6;

  const packets: React.ReactNode[] = [];
  let tcpGlow = 0, udpVisible = si >= 1 && si !== 2 && si !== 3, tcpVisible = si !== 4, timer: React.ReactNode = null, buffer: React.ReactNode = null;
  const lanes = { tcp: si === 5 ? -0.9 : 0, udp: si === 5 ? 0.9 : si === 4 ? 0 : 0.9 };

  if (si === 1) { // data is cut into packets above the laptop
    for (let i = 0; i < 4; i++) {
      const t = sat((l - 40 - i * 8) / 30), p = new THREE.Vector3(-3.6 + (i - 1.5) * 0.5 * t, 3.0 - t * 0.4, 0);
      packets.push(<Packet key={"d" + i} p={p} color={i % 2 ? UDP_C : TCP_C} scale={0.8} label={l > 90 ? String(i + 1) : undefined} />);
    }
  }
  if (si === 2) { // handshake
    const s = fwd(l, HS.syn), sa = back(l, HS.synack, 0), a = fwd(l, HS.ack);
    if (s) packets.push(<Packet key="syn" p={s} color={TCP_C} label="SYN" />);
    if (sa) packets.push(<Packet key="synack" p={sa} color={ACK_C} label="SYN-ACK" />);
    if (a) packets.push(<Packet key="ack" p={a} color={TCP_C} label="ACK" />);
    tcpGlow = l > HS.established ? 0.9 : 0;
  }
  if (si === 3) { // reliable delivery with a lost segment
    DV.send.forEach((s, i) => {
      const n = i + 1, t = (l - s) / TRAVEL;
      if (i === DV.lost) {
        if (t >= 0 && t < DV.lostAt) packets.push(<Packet key={"s" + n} p={pathAt(ease(t))} color={TCP_C} label={`Seq ${n}`} />);
        else if (t >= DV.lostAt && t < DV.lostAt + 0.9) { const u = (t - DV.lostAt) / 0.9, p = pathAt(ease(DV.lostAt)); p.y -= u * u * 3.2; packets.push(<Packet key="lost" p={p} color={LOST_C} label="Seq 3 itdi" rot={u * 4} opacity={1 - u} />); }
        return;
      }
      const p = fwd(l, s); if (p) packets.push(<Packet key={"s" + n} p={p} color={TCP_C} label={`Seq ${n}`} />);
    });
    const r = fwd(l, DV.resend); if (r) packets.push(<Packet key="re" p={r} color={TCP_C} label="Seq 3 (təkrar)" />);
    [...DV.acks, DV.finalAck].forEach(([s, n], i) => { const p = back(l, s); if (p) packets.push(<Packet key={"a" + i} p={p} color={ACK_C} label={`ACK ${n}`} scale={0.8} />); });
    const tp = sat((l - DV.timerStart) / (DV.timeout - DV.timerStart));
    if (l >= DV.timerStart && l < DV.resend + 10) timer = <TimerRing p={tp} alarm={l >= DV.timeout} pos={[-3.6, 3.4, 0]} />;
    const have = [1, 2, 4, 3].filter((n, i) => (n === 3 ? l > DV.resend + TRAVEL : l > DV.send[n - 1] + TRAVEL));
    buffer = <Buffer have={have} pos={[3.6, 3.5, 0]} />;
    tcpGlow = 0.6;
  }
  if (si === 4) { // UDP datagram stream, server -> client, no replies
    for (let i = 0; i < UD.count; i++) {
      const s = UD.start + i * UD.every, t = (l - s) / TRAVEL;
      if (t < 0 || t > 1) continue;
      if (i === UD.lost) { if (t < 0.5) packets.push(<Packet key={"u" + i} p={pathAt(1 - t, lanes.udp)} color={UDP_C} scale={0.75} />); else { const u = (t - 0.5) * 2, p = pathAt(0.5, lanes.udp); p.y -= u * u * 3; packets.push(<Packet key={"u" + i} p={p} color={LOST_C} scale={0.75} rot={u * 4} opacity={1 - u} label="itdi" />); } continue; }
      packets.push(<Packet key={"u" + i} p={pathAt(1 - t, lanes.udp)} color={UDP_C} scale={0.75} label={i % 5 === 0 ? `#${i + 1}` : undefined} />);
    }
  }
  if (si === 5) { // head-of-line blocking: TCP waits for the lost one, UDP keeps flowing
    for (let i = 0; i < HOL.count; i++) {
      const s = 10 + i * HOL.every;
      // UDP lane
      { const t = (l - s) / TRAVEL; if (t >= 0 && t <= 1) { if (i === HOL.lost) { if (t < 0.5) packets.push(<Packet key={"hu" + i} p={pathAt(1 - t, lanes.udp)} color={UDP_C} scale={0.7} />); } else packets.push(<Packet key={"hu" + i} p={pathAt(1 - t, lanes.udp)} color={UDP_C} scale={0.7} />); } }
      // TCP lane: after the loss, packets pile up at the client until the retransmission lands
      { let t = (l - s) / TRAVEL; if (i === HOL.lost) { if (t >= 0 && t < 0.5) packets.push(<Packet key={"ht" + i} p={pathAt(1 - t, lanes.tcp)} color={TCP_C} scale={0.7} />); const rt = (l - HOL.retransmitAt) / TRAVEL; if (rt >= 0 && rt <= 1) packets.push(<Packet key="htr" p={pathAt(1 - rt, lanes.tcp)} color={TCP_C} scale={0.7} label="təkrar" />); continue; }
        const unblocked = HOL.retransmitAt + TRAVEL;
        if (i > HOL.lost && t >= 0.92 && l < unblocked) { const q = i - HOL.lost; packets.push(<Packet key={"ht" + i} p={pathAt(0.06 + 0.075 * q, lanes.tcp)} color={TCP_C} scale={0.6} label={q === 1 ? "gözləyir" : undefined} />); continue; }
        if (t >= 0 && t <= 1 && !(i > HOL.lost && l >= unblocked && s + TRAVEL < unblocked)) packets.push(<Packet key={"ht" + i} p={pathAt(1 - Math.min(t, i > HOL.lost && l < unblocked ? 0.92 : 1), lanes.tcp)} color={TCP_C} scale={0.7} />); }
    }
    tcpGlow = 0.3;
  }

  return (
    <>
      <color attach="background" args={["#070a18"]} />
      <fog attach="fog" args={["#070a18", 12, 30]} />
      <hemisphereLight args={["#b8ccff", "#2a2030", 1.25]} />
      <ambientLight intensity={0.25} />
      <directionalLight position={[4, 8, 6]} intensity={2.6} castShadow shadow-mapSize={[1024, 1024]} shadow-camera-left={-8} shadow-camera-right={8} shadow-camera-top={8} shadow-camera-bottom={-8} />
      <pointLight position={[-3.6, 2.6, 1.8]} color={TCP_C} intensity={7} distance={7} />
      <spotLight position={[0, 7, 5]} angle={0.7} penumbra={0.6} intensity={30} distance={20} color="#e8f0ff" />
      <pointLight position={[3.6, 3.0, 1.6]} color={si === 4 || si === 5 ? UDP_C : ACK_C} intensity={3} distance={6} />
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow><planeGeometry args={[60, 60]} /><meshStandardMaterial color="#141c3a" roughness={0.8} metalness={0.2} /></mesh>
      <gridHelper args={[40, 40, "#1c2a50", "#121a36"]} position={[0, 0.002, 0]} />
      <Laptop pos={[-3.6, 0, 0]} f={f} label={si === 4 || si === 5 ? "Kliyent (izləyici)" : "Kliyent"} showLabel={showLabels} />
      <Rack pos={[3.6, 0, -0.2]} f={f} label="Server" showLabel={showLabels} />
      {tcpVisible && <Cable lane={lanes.tcp} color={TCP_C} glow={tcpGlow} />}
      {udpVisible && <Cable lane={lanes.udp} color={UDP_C} glow={si === 4 ? 0.5 : 0.2} />}
      {si === 5 && <><Label text="TCP" pos={[0, 3.0, lanes.tcp]} color={TCP_C} h={0.34} /><Label text="UDP" pos={[0, 2.2, lanes.udp + 0.6]} color={UDP_C} h={0.34} /></>}
      {packets}{timer}{buffer}
    </>
  );
};
