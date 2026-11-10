import React from "react";
import { interpolate, Easing } from "remotion";
import T from "./timing.json";
import { SEC, HS, DV, UD, secIndex } from "./timing";
import { TCP_C, UDP_C, ACK_C, LOST_C } from "./Scene3D";

const TRAVEL = T.travel;
const fade = (l: number, a: number, d = 12) => interpolate(l, [a, a + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
const panel: React.CSSProperties = { background: "rgba(9,13,30,0.82)", border: "1px solid rgba(120,150,255,0.18)", borderRadius: 18, boxShadow: "0 18px 50px rgba(0,0,0,.35)" };

const Heading: React.FC<{ l: number; num?: string; title: string; sub: string; color?: string }> = ({ l, num, title, sub, color = TCP_C }) => (
  <div style={{ position: "absolute", left: 70, top: 56, maxWidth: 1080, opacity: fade(l, 0), transform: `translateY(${(1 - fade(l, 0)) * 16}px)` }}>
    <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
      {num && <div style={{ background: color, color: "#061020", fontWeight: 800, fontSize: 34, borderRadius: 12, padding: "4px 16px" }}>{num}</div>}
      <div style={{ fontSize: 54, fontWeight: 800, color: "#fff", letterSpacing: -0.5 }}>{title}</div>
    </div>
    <div style={{ marginTop: 10, fontSize: 31, fontWeight: 500, color: "#a9bce6", opacity: fade(l, 10) }}>{sub}</div>
  </div>
);

// ---------- sequence diagram ----------
type Ev = { t: number; dir: "CS" | "SC"; label: string; color: string; lost?: boolean };
const SeqDiagram: React.FC<{ l: number; events: Ev[]; notes?: { t: number; y0: number; y1: number; text: string; color: string; side: "C" | "S" }[]; title: string }> = ({ l, events, notes = [], title }) => {
  const x0 = 1215, w = 640, top = 205, h = 790, cx = x0 + 120, sx = x0 + w - 120, rowH = Math.min(74, (h - 150) / Math.max(1, events.length));
  return (
    <div style={{ position: "absolute", left: x0, top, width: w, height: h, ...panel, opacity: fade(l, 4) }}>
      <svg width={w} height={h} style={{ position: "absolute", left: 0, top: 0 }}>
        <defs>{[TCP_C, UDP_C, ACK_C, LOST_C].map(c => <marker key={c} id={"m" + c.slice(1)} markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill={c} /></marker>)}</defs>
        <text x={w / 2} y={44} fill="#cfe0ff" fontSize={26} fontWeight={700} textAnchor="middle" fontFamily="Inter">{title}</text>
        {[["Kliyent", cx - x0], ["Server", sx - x0]].map(([t, x]) => (
          <g key={t as string}>
            <rect x={(x as number) - 70} y={66} width={140} height={44} rx={10} fill="#1a2446" stroke="rgba(150,180,255,.3)" />
            <text x={x as number} y={96} fill="#fff" fontSize={24} fontWeight={700} textAnchor="middle" fontFamily="Inter">{t}</text>
            <line x1={x as number} y1={112} x2={x as number} y2={h - 24} stroke="#3a4a7a" strokeWidth={3} strokeDasharray="8 8" />
          </g>
        ))}
        {notes.map((n, i) => {
          const a = fade(l, n.t, 10); if (a <= 0) return null;
          const x = n.side === "C" ? cx - x0 - 30 : sx - x0 + 30, y0 = 140 + n.y0 * rowH, y1 = 140 + n.y1 * rowH;
          return <g key={i} opacity={a}><path d={`M${x + (n.side === "C" ? 10 : -10)},${y0} L${x},${y0} L${x},${y1} L${x + (n.side === "C" ? 10 : -10)},${y1}`} stroke={n.color} strokeWidth={3} fill="none" />
            <text x={n.side === "C" ? x - 10 : x + 10} y={(y0 + y1) / 2 + 8} fill={n.color} fontSize={20} fontWeight={700} textAnchor={n.side === "C" ? "end" : "start"} fontFamily="Inter">{n.text}</text></g>;
        })}
        {events.map((e, i) => {
          const p = Math.min(1, Math.max(0, (l - e.t) / TRAVEL)); if (p <= 0) return null;
          const y = 150 + i * rowH, fromX = e.dir === "CS" ? cx - x0 : sx - x0, toX = e.dir === "CS" ? sx - x0 : cx - x0;
          const endP = e.lost ? Math.min(p, 0.5) : p, x2 = fromX + (toX - fromX) * endP, y2 = y + rowH * 0.55 * endP;
          return (
            <g key={i}>
              <line x1={fromX} y1={y} x2={x2} y2={y2} stroke={e.color} strokeWidth={4} markerEnd={!e.lost || p < 0.5 ? `url(#m${e.color.slice(1)})` : undefined} />
              <text x={(fromX + toX) / 2} y={y + rowH * 0.27 - 10} fill={e.color} fontSize={22} fontWeight={700} textAnchor="middle" fontFamily="Inter" opacity={fade(l, e.t, 8)}>{e.label}</text>
              {e.lost && p >= 0.5 && <text x={x2} y={y2 + 10} fill={LOST_C} fontSize={34} fontWeight={800} textAnchor="middle" fontFamily="Inter">✕</text>}
            </g>
          );
        })}
      </svg>
    </div>
  );
};

const Bullets: React.FC<{ l: number; start: number; items: string[]; color: string; left?: number; bottom?: number; width?: number }> = ({ l, start, items, color, left = 70, bottom = 50, width = 900 }) => (
  <div style={{ position: "absolute", left, bottom, width, padding: "22px 30px", ...panel, opacity: fade(l, start) }}>
    {items.map((s, i) => (
      <div key={i} style={{ display: "flex", gap: 16, alignItems: "baseline", fontSize: 27, color: "#e6eeff", fontWeight: 500, margin: "4px 0", opacity: fade(l, start + 8 + i * 14), transform: `translateX(${(1 - fade(l, start + 8 + i * 14)) * -20}px)` }}>
        <span style={{ color, fontWeight: 800 }}>•</span><span>{s}</span>
      </div>
    ))}
  </div>
);

// ---------- icons for the examples ----------
const Icon: React.FC<{ k: string; c: string }> = ({ k, c }) => {
  const s = { stroke: c, strokeWidth: 4, fill: "none", strokeLinecap: "round" as const, strokeLinejoin: "round" as const };
  return (
    <svg width={64} height={64} viewBox="0 0 64 64">
      {k === "web" && <><circle cx={32} cy={32} r={24} {...s} /><ellipse cx={32} cy={32} rx={11} ry={24} {...s} /><line x1={8} y1={32} x2={56} y2={32} {...s} /></>}
      {k === "mail" && <><rect x={8} y={14} width={48} height={36} rx={5} {...s} /><path d="M10 18 L32 36 L54 18" {...s} /></>}
      {k === "file" && <><path d="M8 18 h18 l6 6 h24 v28 h-48 z" {...s} /><path d="M32 30 v14 M25 37 l7 7 l7 -7" {...s} /></>}
      {k === "ssh" && <><rect x={8} y={12} width={48} height={40} rx={5} {...s} /><path d="M18 26 l8 6 l-8 6 M30 40 h14" {...s} /></>}
      {k === "dns" && <><circle cx={27} cy={27} r={15} {...s} /><line x1={38} y1={38} x2={54} y2={54} {...s} /></>}
      {k === "call" && <><rect x={8} y={18} width={34} height={28} rx={5} {...s} /><path d="M42 28 l14 -8 v24 l-14 -8 z" {...s} /></>}
      {k === "game" && <><path d="M16 22 h32 a10 10 0 0 1 10 10 v4 a8 8 0 0 1 -14 5 l-4 -5 h-16 l-4 5 a8 8 0 0 1 -14 -5 v-4 a10 10 0 0 1 10 -10 z" {...s} /><path d="M20 30 v8 M16 34 h8" {...s} /><circle cx={44} cy={32} r={2} fill={c} /><circle cx={48} cy={37} r={2} fill={c} /></>}
      {k === "tv" && <><rect x={6} y={12} width={52} height={34} rx={5} {...s} /><path d="M24 54 h16 M32 46 v8" {...s} /></>}
    </svg>
  );
};

const Card: React.FC<{ l: number; t: number; k: string; title: string; proto: string; c: string }> = ({ l, t, k, title, proto, c }) => (
  <div style={{ display: "flex", alignItems: "center", gap: 22, padding: "16px 22px", margin: "14px 0", ...panel, opacity: fade(l, t), transform: `translateY(${(1 - fade(l, t)) * 18}px)` }}>
    <Icon k={k} c={c} />
    <div><div style={{ fontSize: 32, fontWeight: 700, color: "#fff" }}>{title}</div><div style={{ fontSize: 24, color: c, fontWeight: 600 }}>{proto}</div></div>
  </div>
);

const ROWS: [string, string, string][] = [
  ["Bağlantı", "Əlaqə yönümlü (3 addımlı əl sıxma)", "Əlaqəsiz"],
  ["Etibarlılıq", "Zəmanətli: ACK + təkrar göndərmə", "Zəmanət yoxdur"],
  ["Ardıcıllıq", "Qorunur (Seq nömrələri)", "Qorunmur"],
  ["Axın / tıxanma nəzarəti", "Var", "Yoxdur"],
  ["Gecikmə", "Daha çox", "Daha az"],
  ["Başlıq ölçüsü", "20–60 bayt", "8 bayt"],
  ["Nümunələr", "HTTP/HTTPS, SMTP, FTP, SSH", "DNS, VoIP (RTP), oyunlar, IPTV"],
];

export const Overlay: React.FC<{ f: number }> = ({ f }) => {
  const si = secIndex(f), l = f - SEC[si];
  if (si === 0) return (
    <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", alignItems: "center", paddingTop: 120 }}>
      <div style={{ fontSize: 30, letterSpacing: 6, color: "#8fb0ff", fontWeight: 600, opacity: fade(l, 6) }}>NƏQLİYYAT QATI PROTOKOLLARI</div>
      <div style={{ fontSize: 128, fontWeight: 800, color: "#fff", lineHeight: 1.05, marginTop: 10, opacity: fade(l, 12), transform: `scale(${0.96 + 0.04 * fade(l, 12)})` }}><span style={{ color: TCP_C }}>TCP</span> və <span style={{ color: UDP_C }}>UDP</span></div>
      <div style={{ fontSize: 46, fontWeight: 600, color: "#dfe8ff", opacity: fade(l, 22) }}>müqayisəsi</div>
      <div style={{ marginTop: 26, fontSize: 30, color: "#a9bce6", opacity: fade(l, 34) }}>Şəfili Rəsul · Kompüter şəbəkələri · KOM24A</div>
    </div>
  );
  if (si === 1) return (
    <>
      <Heading l={l} title="Məlumat seqmentlərə bölünür" sub="Göndərmə qaydasını nəqliyyat qatı müəyyən edir: TCP və ya UDP" />
      <div style={{ position: "absolute", right: 70, top: 230, width: 520, padding: 26, ...panel, opacity: fade(l, 20) }}>
        <div style={{ fontSize: 24, color: "#8fb0ff", fontWeight: 700, marginBottom: 12 }}>TCP/IP modeli</div>
        {[["Tətbiq qatı", "HTTP, DNS, SMTP ..."], ["Nəqliyyat qatı", "TCP  |  UDP"], ["İnternet qatı", "IP"], ["Şəbəkə girişi", "Ethernet, Wi-Fi"]].map(([a, b], i) => {
          const hl = i === 1;
          return <div key={a} style={{ display: "flex", justifyContent: "space-between", padding: "14px 18px", margin: "8px 0", borderRadius: 12, fontSize: 27, fontWeight: hl ? 800 : 600, color: hl ? "#061020" : "#dfe8ff", background: hl ? `linear-gradient(90deg, ${TCP_C}, ${UDP_C})` : "#162042", opacity: fade(l, 26 + i * 8), boxShadow: hl ? "0 0 30px rgba(46,196,255,.35)" : undefined }}><span>{a}</span><span style={{ opacity: 0.85 }}>{b}</span></div>;
        })}
      </div>
    </>
  );
  if (si === 2) return (
    <>
      <Heading l={l} num="1" title="TCP əlaqə yönümlüdürmü? Bəli." sub="Məlumatdan əvvəl bağlantı qurulur: 3 addımlı əl sıxma" />
      <SeqDiagram l={l} title="3 addımlı əl sıxma" events={[
        { t: HS.syn, dir: "CS", label: "SYN", color: TCP_C },
        { t: HS.synack, dir: "SC", label: "SYN-ACK", color: ACK_C },
        { t: HS.ack, dir: "CS", label: "ACK", color: TCP_C },
      ]} />
      {l > HS.established && <div style={{ position: "absolute", left: 1215, top: 1010 - 70, width: 640, textAlign: "center", fontSize: 30, fontWeight: 800, color: ACK_C, opacity: fade(l, HS.established) }}>Bağlantı quruldu: məlumat göndərilə bilər</div>}
    </>
  );
  if (si === 3) {
    const q4 = l >= 200;
    return (
      <>
        {q4 ? <Heading l={l - 200} num="4" title="TCP-də etibarlılıq necə təmin olunur?" sub="İtən seqment aşkarlanır və yenidən göndərilir" />
            : <Heading l={l} num="3" title="ACK nədir?" sub="Qəbul edənin təsdiqi: ACK = növbəti gözlənilən Seq nömrəsi" color={ACK_C} />}
        <SeqDiagram l={l} title="Seqmentlərin ötürülməsi" events={[
          { t: DV.send[0], dir: "CS", label: "Seq 1", color: TCP_C },
          { t: DV.send[1], dir: "CS", label: "Seq 2", color: TCP_C },
          { t: DV.acks[0][0], dir: "SC", label: "ACK 2", color: ACK_C },
          { t: DV.send[2], dir: "CS", label: "Seq 3", color: LOST_C, lost: true },
          { t: DV.acks[1][0], dir: "SC", label: "ACK 3", color: ACK_C },
          { t: DV.send[3], dir: "CS", label: "Seq 4", color: TCP_C },
          { t: DV.acks[2][0], dir: "SC", label: "ACK 3 (dublikat)", color: "#ffcc4a" },
          { t: DV.resend, dir: "CS", label: "Seq 3 (təkrar)", color: TCP_C },
          { t: DV.finalAck[0], dir: "SC", label: "ACK 5", color: ACK_C },
        ]} notes={[{ t: DV.timerStart + 10, y0: 3.1, y1: 7.0, text: "Taymer", color: "#ffcc4a", side: "C" }]} />
        <Bullets l={l} start={DV.bullets} color={TCP_C} items={["Hər seqmentin ardıcıllıq nömrəsi var (Seq)", "Qəbul edən ACK ilə təsdiqləyir", "ACK gəlməsə: taymer bitir → təkrar göndərmə", "Buferdə seqmentlər düzgün sıraya düzülür", "Checksum ilə xəta yoxlanılır"]} />
      </>
    );
  }
  if (si === 4) return (
    <>
      <Heading l={l} num="2" title="UDP necə işləyir?" sub="Əl sıxma yoxdur, ACK yoxdur: datagramlar sadəcə göndərilir" color={UDP_C} />
      <SeqDiagram l={l} title="UDP datagramları" events={Array.from({ length: 9 }, (_, i) => ({ t: UD.start + i * UD.every, dir: "SC" as const, label: i === UD.lost ? `#${i + 1} itdi` : `Datagram #${i + 1}`, color: i === UD.lost ? LOST_C : UDP_C, lost: i === UD.lost }))} />
      <Bullets l={l} start={150} color={UDP_C} items={["Bağlantı qurulmur (əlaqəsiz)", "Təsdiq və təkrar göndərmə yoxdur", "İtən datagram geri qaytarılmır, axın davam edir", "Başlıq cəmi 8 bayt: sürətli və yüngül"]} />
    </>
  );
  if (si === 5) return (
    <>
      <Heading l={l} num="5" title="UDP nə zaman üstündür?" sub="Gecikmə itkidən daha vacib olanda: real vaxt tətbiqləri" color={UDP_C} />
      <div style={{ position: "absolute", left: 70, bottom: 70, width: 860, padding: "20px 28px", ...panel, opacity: fade(l, 40) }}>
        <div style={{ fontSize: 28, color: "#e6eeff", fontWeight: 600 }}><span style={{ color: TCP_C, fontWeight: 800 }}>TCP:</span> itən paket gözlənilir, arxadakılar növbədə qalır</div>
        <div style={{ fontSize: 28, color: "#e6eeff", fontWeight: 600, marginTop: 8, opacity: fade(l, 60) }}><span style={{ color: UDP_C, fontWeight: 800 }}>UDP:</span> itki olsa da axın dayanmadan davam edir</div>
      </div>
      <div style={{ position: "absolute", right: 70, bottom: 70, width: 760, padding: "20px 28px", ...panel, opacity: fade(l, 200) }}>
        <div style={{ fontSize: 28, color: "#e6eeff", fontWeight: 600 }}>Video və səs zəngi · onlayn oyunlar · DNS sorğuları · IPTV</div>
      </div>
    </>
  );
  if (si === 6) return (
    <>
      <Heading l={l} num="6" title="Tətbiq nümunələri" sub="Hər bayt vacibdirsə TCP, sürət vacibdirsə UDP" />
      <div style={{ position: "absolute", left: 70, top: 250, width: 560 }}>
        <div style={{ fontSize: 40, fontWeight: 800, color: TCP_C, opacity: fade(l, 10) }}>TCP</div>
        <Card l={l} t={18} k="web" title="Veb səhifələr" proto="HTTP / HTTPS" c={TCP_C} />
        <Card l={l} t={30} k="mail" title="E-poçt" proto="SMTP / IMAP" c={TCP_C} />
        <Card l={l} t={42} k="file" title="Fayl ötürmə" proto="FTP" c={TCP_C} />
        <Card l={l} t={54} k="ssh" title="Uzaqdan idarə" proto="SSH" c={TCP_C} />
      </div>
      <div style={{ position: "absolute", right: 70, top: 250, width: 560 }}>
        <div style={{ fontSize: 40, fontWeight: 800, color: UDP_C, opacity: fade(l, 80) }}>UDP</div>
        <Card l={l} t={88} k="dns" title="Domen adları" proto="DNS" c={UDP_C} />
        <Card l={l} t={100} k="call" title="Video / səs zəngi" proto="VoIP (RTP)" c={UDP_C} />
        <Card l={l} t={112} k="game" title="Onlayn oyunlar" proto="real vaxt" c={UDP_C} />
        <Card l={l} t={124} k="tv" title="IPTV / canlı TV" proto="RTP / multicast" c={UDP_C} />
      </div>
    </>
  );
  // table
  return (
    <>
      <div style={{ position: "absolute", left: 0, right: 0, top: 50, textAlign: "center", fontSize: 54, fontWeight: 800, color: "#fff", opacity: fade(l, 0) }}><span style={{ color: TCP_C }}>TCP</span> vs <span style={{ color: UDP_C }}>UDP</span>: müqayisə cədvəli</div>
      <div style={{ position: "absolute", left: 150, top: 160, width: 1620, ...panel, padding: "10px 0", opacity: fade(l, 6) }}>
        <div style={{ display: "grid", gridTemplateColumns: "420px 1fr 1fr", fontSize: 30, fontWeight: 800, padding: "14px 34px", color: "#8fb0ff" }}><span>Xüsusiyyət</span><span style={{ color: TCP_C }}>TCP</span><span style={{ color: UDP_C }}>UDP</span></div>
        {ROWS.map(([a, b, c], i) => (
          <div key={a} style={{ display: "grid", gridTemplateColumns: "420px 1fr 1fr", fontSize: 29, padding: "15px 34px", background: i % 2 ? "transparent" : "rgba(80,110,220,0.08)", color: "#e6eeff", opacity: fade(l, 16 + i * 18), transform: `translateX(${(1 - fade(l, 16 + i * 18)) * 30}px)` }}>
            <span style={{ fontWeight: 700, color: "#fff" }}>{a}</span><span>{b}</span><span>{c}</span>
          </div>
        ))}
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 60, textAlign: "center", fontSize: 44, fontWeight: 800, color: ACK_C, opacity: fade(l, 250) }}>Diqqətiniz üçün təşəkkürlər!</div>
    </>
  );
};
