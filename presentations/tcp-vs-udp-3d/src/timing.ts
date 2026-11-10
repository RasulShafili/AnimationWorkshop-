// All event times (frames @30 fps). Shared by picture and (via timing.json) the SFX script.
import T from "./timing.json";
export const FPS = T.fps, TOTAL = T.totalFrames, SEC = T.sections;
export const HS = T.handshake, DV = T.delivery, UD = T.udp, HOL = T.hol;
export const secIndex = (f: number) => { let i = 0; while (i < SEC.length - 2 && f >= SEC[i + 1]) i++; return i; };
