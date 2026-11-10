import { ART_WIDTH, drawChar, measureText, rect } from "./pixel";
import { PALETTE } from "./palette";
import rawCaptions from "./captions.json";

export interface CaptionEntry {
  text: string;
  highlight: string;
  start: number;
  end: number;
  startFrame: number;
  endFrame: number;
}

export const CAPTIONS: CaptionEntry[] = rawCaptions as CaptionEntry[];

export function drawCaptions(ctx: CanvasRenderingContext2D, globalFrame: number) {
  const cap = CAPTIONS.find(c => globalFrame >= c.startFrame && globalFrame <= c.endFrame);
  if (!cap) return;

  const words = cap.text.split(" ");
  const localAge = globalFrame - cap.startFrame;
  const popY = localAge < 3 ? -1 : 0;

  // Single-line 2-3 word chunking at scale 2
  const scale = 2;
  const spaceW = 5 * scale + scale;

  let lineW = 0;
  words.forEach(w => {
    lineW += measureText(w, scale);
  });
  lineW += (words.length - 1) * spaceW;

  const targetY = 320 + popY;
  const curX = Math.floor((ART_WIDTH - lineW) / 2);

  // High contrast background pill at safe y=320, strictly avoiding y<=255 artwork
  const padX = 8;
  const boxX = Math.max(8, curX - padX);
  const boxW = Math.min(ART_WIDTH - 16, lineW + padX * 2);
  const boxY = targetY - 6;
  const boxH = 26;

  rect(ctx, boxX, boxY, boxW, boxH, "rgba(8, 4, 10, 0.94)");
  rect(ctx, boxX, boxY, boxW, 1, PALETTE.venomGreen);
  rect(ctx, boxX, boxY + boxH - 1, boxW, 1, PALETTE.venomGreen);
  rect(ctx, boxX, boxY, 1, boxH, PALETTE.venomGreen);
  rect(ctx, boxX + boxW - 1, boxY, 1, boxH, PALETTE.venomGreen);

  // Draw words with highlighted keywords
  let wordX = curX;
  for (let i = 0; i < words.length; i++) {
    const w = words[i];
    const cleanWord = w.toLowerCase().replace(/[^\w]/g, "");
    const cleanHi = cap.highlight.toLowerCase().replace(/[^\w]/g, "");
    const isHighlight = cleanWord === cleanHi || cleanWord.includes(cleanHi) || cleanHi.includes(cleanWord);
    const color = isHighlight ? PALETTE.plasmaYellow : "#ffffff";
    const outlineColor = "#000000";

    for (let cIdx = 0; cIdx < w.length; cIdx++) {
      drawChar(ctx, w[cIdx], wordX, targetY, scale, color, outlineColor);
      wordX += 5 * scale + scale;
    }
    wordX += spaceW;
  }
}
