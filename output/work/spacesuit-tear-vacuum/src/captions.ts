import { ART_WIDTH, drawChar, measureText, rect } from "./pixel";
import { PALETTE } from "./palette";
import rawCaptions from "./captions.json";

export interface CaptionEntry {
  id: number;
  words: string[];
  text: string;
  highlight: string;
  start: number;
  end: number;
  startFrame: number;
  endFrame: number;
}

export const CAPTIONS: CaptionEntry[] = rawCaptions;

export function drawCaptions(ctx: CanvasRenderingContext2D, globalFrame: number) {
  const cap = CAPTIONS.find(c => globalFrame >= c.startFrame && globalFrame <= c.endFrame);
  if (!cap) return;

  const words = cap.words || cap.text.split(" ");
  const localAge = globalFrame - cap.startFrame;
  const popY = localAge < 3 ? -1 : 0;

  // With 2-3 words, scale 2 always fits cleanly on a single line!
  const scale = 2;
  const spaceW = 5 * scale + scale;

  let lineW = 0;
  words.forEach(w => {
    lineW += measureText(w, scale);
  });
  lineW += (words.length - 1) * spaceW;

  const targetY = 320 + popY;
  const curX = Math.floor((ART_WIDTH - lineW) / 2);

  // Solid, high-contrast background pill
  const padX = 10;
  const boxX = Math.max(8, curX - padX);
  const boxW = Math.min(ART_WIDTH - 16, lineW + padX * 2);
  const boxY = targetY - 6;
  const boxH = 26;

  rect(ctx, boxX, boxY, boxW, boxH, "rgba(5, 8, 18, 0.95)");
  rect(ctx, boxX, boxY, boxW, 1, PALETTE.earthAtmosphere);
  rect(ctx, boxX, boxY + boxH - 1, boxW, 1, PALETTE.earthAtmosphere);

  // Draw words
  let wordX = curX;
  for (let i = 0; i < words.length; i++) {
    const w = words[i];
    const isHighlight = w.toLowerCase().replace(/[^\w]/g, "") === cap.highlight.toLowerCase().replace(/[^\w]/g, "");
    const color = isHighlight ? PALETTE.solarYellow : "#ffffff";
    const outlineColor = "#000000";

    for (let cIdx = 0; cIdx < w.length; cIdx++) {
      drawChar(ctx, w[cIdx], wordX, targetY, scale, color, outlineColor);
      wordX += 5 * scale + scale;
    }
    wordX += spaceW;
  }
}
