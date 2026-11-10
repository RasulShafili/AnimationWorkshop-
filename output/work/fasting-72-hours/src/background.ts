import { ART_WIDTH, ART_HEIGHT, dither, line, rect, px } from "./pixel";
import { PALETTE } from "./palette";

export type BgTheme = "PEACH" | "GREY_PURPLE" | "CYAN_BLUE" | "YELLOW_GREEN";

export function drawBackground(
  ctx: CanvasRenderingContext2D,
  frame: number,
  theme: BgTheme = "PEACH",
  cameraX: number = 0
) {
  // Drift: 1 px per 20 frames
  const drift = Math.floor(frame / 20);

  // Colors per theme
  let skyA = PALETTE.peach;
  let skyB = PALETTE.skinLight;
  let floorA = PALETTE.darkPurple;
  let floorB = PALETTE.greyPurple;

  if (theme === "GREY_PURPLE") {
    skyA = PALETTE.greyPurple;
    skyB = PALETTE.darkPurple;
    floorA = PALETTE.dark;
    floorB = PALETTE.darkPurple;
  } else if (theme === "CYAN_BLUE") {
    skyA = PALETTE.cyan;
    skyB = PALETTE.blue;
    floorA = PALETTE.darkPurple;
    floorB = PALETTE.blue;
  } else if (theme === "YELLOW_GREEN") {
    skyA = PALETTE.brightGreen;
    skyB = PALETTE.yellow;
    floorA = PALETTE.green;
    floorB = PALETTE.brightGreen;
  }

  // 1. FAR LAYER (0..215): dithered sky with slow drift (0.2x speed)
  const farOffset = Math.floor((cameraX + drift) * 0.2);
  dither(ctx, 0, 0, ART_WIDTH, 215, skyA, skyB, "check");

  // Far clouds / geometric shapes
  for (let c = 0; c < 3; c++) {
    const cloudX = (c * 100 - farOffset + 300) % (ART_WIDTH + 60) - 30;
    const cloudY = 30 + c * 25;
    rect(ctx, cloudX, cloudY, 40, 8, PALETTE.white);
    rect(ctx, cloudX + 8, cloudY - 6, 24, 6, PALETTE.white);
  }

  // 2. MID LAYER (horizon at y=215, 0.5x speed)
  const midOffset = Math.floor((cameraX + drift) * 0.5);
  // Horizon silhouette line
  line(ctx, 0, 214, ART_WIDTH, 214, PALETTE.dark);
  for (let b = 0; b < 6; b++) {
    const houseX = (b * 60 - midOffset + 360) % (ART_WIDTH + 60) - 30;
    const houseW = 28;
    const houseH = 18 + (b % 3) * 6;
    rect(ctx, houseX, 215 - houseH, houseW, houseH, PALETTE.darkPurple);
    // Tiny windows
    px(ctx, houseX + 6, 215 - houseH + 6, PALETTE.yellow);
    px(ctx, houseX + 16, 215 - houseH + 6, PALETTE.yellow);
  }

  // 3. D2 FLOOR PERSPECTIVE (top y=215, bottom y=360)
  // Vanishing point: (135, 150)
  const vpX = 135;
  const vpY = 150;
  const floorTopY = 215;
  const floorBottomY = 360;

  // Fill floor background
  rect(ctx, 0, floorTopY, ART_WIDTH, floorBottomY - floorTopY, floorA);

  // 6-8 horizontal lines with growing spacing
  const hLineSpacings = [8, 11, 15, 20, 26, 33, 42];
  let curY = floorTopY;
  for (const sp of hLineSpacings) {
    curY += sp;
    if (curY >= floorBottomY) break;
    line(ctx, 0, curY, ART_WIDTH, curY, floorB);
  }

  // 5 lines converging to vanishing point (135, 150)
  const groundTargets = [10, 70, 135, 200, 260];
  for (const gx of groundTargets) {
    line(ctx, vpX, vpY, gx, floorBottomY, floorB);
  }

  // Bottom area (y=360..480): solid dark floor base
  rect(ctx, 0, floorBottomY, ART_WIDTH, ART_HEIGHT - floorBottomY, PALETTE.dark);
}
