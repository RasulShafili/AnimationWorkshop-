// Word-by-word burned-in captions (copy into a project's src/). Shows a 1–3 word chunk; the word being spoken pops
// and turns accent-coloured. words: [{w, s, e}] in frames (tools/captions/word_timings.py).
import React from "react";
export type Word = { w: string; s: number; e: number };
const chunks = (words: Word[], max = 3) => {
  const out: Word[][] = []; let cur: Word[] = [];
  for (const w of words) {
    cur.push(w);
    if (cur.length >= max || /[,.!?;:…]$/.test(w.w) || w.w.length > 9) { out.push(cur); cur = []; }
  }
  if (cur.length) out.push(cur);
  return out;
};
export const Captions: React.FC<{ f: number; words: Word[]; top?: number; accent?: string; size?: number }> = ({ f, words, top = 1180, accent = "#ffd36a", size = 92 }) => {
  const cs = chunks(words);
  const c = cs.find(ch => f >= ch[0].s - 1 && f < ch[ch.length - 1].e + 6);
  if (!c) return null;
  const chars = c.reduce((a, w) => a + w.w.length, 0) + c.length * 1.6;
  const fs = Math.min(size, 1450 / chars);   // always one line
  return (
    <div style={{ position: "absolute", top, width: "100%", display: "flex", justifyContent: "center", gap: 18, flexWrap: "nowrap", padding: "0 40px", fontFamily: "Inter", fontWeight: 900 }}>
      {c.map((w, i) => {
        const active = f >= w.s && f < w.e + 2, k = Math.max(0, Math.min(1, (f - w.s) / 3));
        const shown = f >= w.s - 1;
        return (
          <span key={i} style={{
            fontSize: fs, lineHeight: 1.1, letterSpacing: -1, textTransform: "uppercase",
            color: active ? accent : "#ffffff", opacity: shown ? 1 : 0,
            transform: `scale(${active ? 1 + 0.18 * (1 - k) + 0.06 : 1}) rotate(${active ? (i % 2 ? 2 : -2) : 0}deg)`,
            padding: "2px 14px", borderRadius: 14, background: active ? "rgba(10,10,20,.78)" : "rgba(10,10,20,.5)",
            WebkitTextStroke: "3px rgba(10,8,30,.9)", paintOrder: "stroke fill", textShadow: "0 6px 0 rgba(10,8,30,.55)",
          }}>{w.w.replace(/[,.;:]$/, "")}</span>
        );
      })}
    </div>
  );
};
