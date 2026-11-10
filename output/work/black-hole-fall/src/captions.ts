import { ART_WIDTH, drawChar, measureText } from "./pixel";
import { PALETTE } from "./palette";
import rawCaptions from "./captions.json";

export interface CaptionItem {
  id: number;
  words: string[];
  yellowWordIndex: number;
  startTime: number;
  endTime: number;
  startFrame: number;
  endFrame: number;
}

export const CAPTIONS: CaptionItem[] = rawCaptions;

export function drawCaptions(ctx: CanvasRenderingContext2D, globalFrame: number) {
  // Find active caption
  const cap = CAPTIONS.find(c => globalFrame >= c.startFrame && globalFrame <= c.endFrame);
  if (!cap) return;

  const localAge = globalFrame - cap.startFrame;
  const popY = localAge < 3 ? -1 : 0;

  // Try scale 2 first
  let scale = 2;
  const spaceW = 5 * scale + scale;

  let totalW = 0;
  const wordWidths = cap.words.map(w => {
    const wLen = measureText(w, scale);
    totalW += wLen;
    return wLen;
  });
  totalW += (cap.words.length - 1) * spaceW;

  // Safe area: width must be <= 235 art px so there are at least 17px padding on left & right
  if (totalW > 235) {
    // Check if splitting into 2 lines fits at scale 2
    if (cap.words.length >= 2) {
      const mid = Math.ceil(cap.words.length / 2);
      const line1Words = cap.words.slice(0, mid);
      const line2Words = cap.words.slice(mid);

      const l1W = line1Words.reduce((acc, w) => acc + measureText(w, scale), 0) + (line1Words.length - 1) * spaceW;
      const l2W = line2Words.reduce((acc, w) => acc + measureText(w, scale), 0) + (line2Words.length - 1) * spaceW;

      if (l1W <= 235 && l2W <= 235) {
        // Draw 2 lines at scale 2
        drawLine(ctx, line1Words, 0, cap.yellowWordIndex, scale, 298 + popY);
        drawLine(ctx, line2Words, mid, cap.yellowWordIndex, scale, 316 + popY);
        return;
      }
    }

    // If still too wide, drop scale to 1 (easily fits anything up to 40 characters)
    scale = 1;
    drawLine(ctx, cap.words, 0, cap.yellowWordIndex, scale, 308 + popY);
    return;
  }

  // Fits on a single line at scale 2!
  drawLine(ctx, cap.words, 0, cap.yellowWordIndex, scale, 308 + popY);
}

function drawLine(
  ctx: CanvasRenderingContext2D,
  words: string[],
  offsetIdx: number,
  yellowIdx: number,
  scale: number,
  y: number
) {
  const spaceW = 5 * scale + scale;
  let lineW = 0;
  const wWidths = words.map(w => {
    const wLen = measureText(w, scale);
    lineW += wLen;
    return wLen;
  });
  lineW += (words.length - 1) * spaceW;

  let curX = Math.floor((ART_WIDTH - lineW) / 2);

  for (let i = 0; i < words.length; i++) {
    const word = words[i];
    const isYellow = (offsetIdx + i) === yellowIdx;
    const wordColor = isYellow ? PALETTE.yellow : PALETTE.white;

    for (let ci = 0; ci < word.length; ci++) {
      const ch = word[ci];
      const charX = curX + ci * (5 * scale + scale);
      // 2px shadow
      drawChar(ctx, ch, charX + 1, y + 2, scale, PALETTE.dark);
      // Outline + text
      drawChar(ctx, ch, charX, y, scale, wordColor, PALETTE.dark);
    }

    curX += wWidths[i] + spaceW;
  }
}
