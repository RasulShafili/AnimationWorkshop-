// Timeline player: every chapter is a list of beats (plan.json, shared with the Python audio scripts) and a list of
// shots. A beat = optional voice line (id) with pre/post gaps, or a silent hold. Shots start at [beatKey, fraction of
// the beat span] and run until the next shot. Lip-sync, fact cards and day stamps come from the same timeline.
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import PLAN from "./plan.json";
import { Grain, Vignette } from "./engine/fx";
import { FactCard, DayStamp, useFonts } from "./ui";
// owner 2026-11-16: on-screen "DAY N · TIME" stamps at chapter starts feel like chapter cards → off
const SHOW_DAYS = true;
export type VO = Record<string, { dur: number; env: number[] }>;
export type Beat = { id?: string; key?: string; pre?: number; post?: number; hold?: number };
export type Span = { s: number; line: number; dur: number; e: number };
export const timeline = (ch: string, vo: VO) => {
  const T: Record<string, Span> = {}; let t = 0;
  for (const b of (PLAN as any)[ch] as Beat[]) {
    const k = b.key ?? b.id!; const dur = b.id ? (vo[`${ch}_${b.id}`]?.dur ?? 60) : (b.hold ?? 30);
    const line = t + (b.pre ?? 0); const e = line + dur + (b.post ?? 0); T[k] = { s: t, line, dur, e }; t = e;
  }
  return { T, len: t };
};
export type Ctx = { f: number; t: number; d: number; T: Record<string, Span>; talk: (id: string) => number; at: (k: string, fr?: number) => number };
export type Shot = { at: [string, number?]; r: (c: Ctx) => React.ReactNode; grade?: boolean };
export const ChapterPlayer: React.FC<{ ch: string; vo: VO; shots: Shot[]; facts?: [string, string, ("left" | "right")?][]; days?: [string, string, string?, number?][]; tint?: string }> = ({ ch, vo, shots, facts = [], days = [], tint }) => {
  useFonts();
  const f = useCurrentFrame(); const { T, len } = timeline(ch, vo);
  const at = (k: string, fr = 0) => { const b = T[k]; if (!b) throw new Error(`no beat ${k} in ${ch}`); return Math.round(b.s + (b.e - b.s) * fr); };
  // shots may be listed in any order: sort by start frame (stable)
  const ord = shots.map((s, j) => ({ s, st: at(s.at[0], s.at[1] ?? 0), j })).sort((a, b) => a.st - b.st || a.j - b.j);
  shots = ord.map(o => o.s); const starts = ord.map(o => o.st);
  let i = 0; for (let j = 0; j < shots.length; j++) if (f >= starts[j]) i = j;
  const end = i + 1 < shots.length ? starts[i + 1] : len;
  const talk = (id: string) => { const v = vo[`${ch}_${id}`], b = T[id]; if (!v || !b) return 0; const k = Math.floor(f - b.line); return k >= 0 && k < v.env.length ? v.env[k] : 0; };
  const c: Ctx = { f, t: f - starts[i], d: end - starts[i], T, talk, at };
  return <AbsoluteFill style={{ background: "#000" }}>
    {shots[i].r(c)}
    {tint && <AbsoluteFill style={{ background: tint, mixBlendMode: "soft-light", opacity: 0.35, pointerEvents: "none" }} />}
    <Vignette o={0.32} />
    {facts.map(([k, text, side], j) => { const b = T[k]; if (!b) return null; const kk = Math.min((f - b.line + 6) / 12, (b.line + b.dur + 8 - f) / 10); return <FactCard key={j} text={text} k={kk} side={side ?? "left"} />; })}
    {SHOW_DAYS && days.map(([k, day, time, dur], j) => <DayStamp key={j} day={day} time={time} t={f - at(k)} dur={dur ?? 120} />)}
    <Grain f={f} o={0.05} />
  </AbsoluteFill>;
};
export const chLen = (ch: string, vo: VO) => timeline(ch, vo).len;
