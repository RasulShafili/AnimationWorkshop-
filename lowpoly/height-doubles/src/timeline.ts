import tl from "./timeline.json";
export const FPS = tl.fps;
export const TOTAL = tl.seconds * tl.fps;
export const CAPTIONS = tl.captions;
// growth happens in a quick spurt right after each tick, then holds: 1 doubling per second
const SPURT = 0.38;
export const growth = (t: number) => {
  const n = Math.floor(t), u = Math.min(1, (t - n) / SPURT);
  const e = u < 1 ? 1 - Math.pow(1 - u, 3) : 1;
  return n + e;
};
export const heightAt = (t: number) => tl.startHeight * Math.pow(2, growth(t)); // metres
export const fmtHeight = (n: number) => {
  const m = tl.startHeight * Math.pow(2, n);
  if (m < 1000) return `${m < 10 ? m.toFixed(1) : Math.round(m)} M`;
  const km = m / 1000;
  if (km < 10) return `${km.toFixed(1)} KM`;
  if (km < 1e6) return `${Math.round(km).toLocaleString("en-US")} KM`;
  return `${(km / 1e6).toFixed(1)} MILLION KM`;
};
