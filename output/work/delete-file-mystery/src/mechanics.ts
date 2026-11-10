import {
  ART_WIDTH,
  ART_HEIGHT,
  rect,
  circle,
  ring,
  line,
  px,
  dither,
  drawText,
  seededSine,
  seededRandom
} from "./pixel";
import { PALETTE } from "./palette";

// 1. DESKTOP WORKSTATION & TRASH BIN
export function drawWorkstation(
  ctx: CanvasRenderingContext2D,
  frame: number,
  showTrashAnimation: boolean
) {
  // Room background
  rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT, PALETTE.dark);

  // Big Glowing Computer Monitor in upper center
  const monX = 35;
  const monY = 60;
  const monW = 200;
  const monH = 150;

  // Monitor bezel
  rect(ctx, monX - 4, monY - 4, monW + 8, monH + 8, PALETTE.black);
  rect(ctx, monX, monY, monW, monH, PALETTE.cyberNavy);

  // Monitor stand
  rect(ctx, 125, monY + monH + 4, 20, 20, PALETTE.steelDark);
  rect(ctx, 110, monY + monH + 24, 50, 6, PALETTE.black);

  // Desktop screen contents (blue OS wallpaper)
  rect(ctx, monX + 4, monY + 4, monW - 8, monH - 8, PALETTE.deepNavy);

  // Desktop Icons on left
  for (let i = 0; i < 3; i++) {
    const iy = monY + 16 + i * 26;
    rect(ctx, monX + 12, iy, 14, 12, PALETTE.neonCyan);
    rect(ctx, monX + 14, iy + 2, 10, 8, PALETTE.white);
    drawText(ctx, `FILE_${i + 1}`, monX + 30, iy + 2, 1, PALETTE.silver);
  }

  // Trash Bin on lower right of screen
  const trashX = monX + monW - 45;
  const trashY = monY + monH - 45;
  rect(ctx, trashX, trashY, 26, 28, PALETTE.steelMid);
  rect(ctx, trashX - 2, trashY - 4, 30, 4, PALETTE.steelLight);
  // Trash lines
  line(ctx, trashX + 6, trashY + 6, trashX + 6, trashY + 22, PALETTE.black);
  line(ctx, trashX + 13, trashY + 6, trashX + 13, trashY + 22, PALETTE.black);
  line(ctx, trashX + 20, trashY + 6, trashX + 20, trashY + 22, PALETTE.black);
  drawText(ctx, "TRASH", trashX - 2, trashY + 30, 1, PALETTE.silver);

  // "EMPTY TRASH" Modal Dialog popping up
  if (showTrashAnimation) {
    const popX = 65;
    const popY = 100;
    rect(ctx, popX - 2, popY - 2, 144, 64, PALETTE.black);
    rect(ctx, popX, popY, 140, 60, PALETTE.cyberNavy);
    rect(ctx, popX, popY, 140, 14, PALETTE.deepNavy);
    drawText(ctx, "PERMANENT DELETE?", popX + 8, popY + 4, 1, PALETTE.yellow);
    drawText(ctx, "ERASE 1.5 GB PHOTO?", popX + 8, popY + 22, 1, PALETTE.white);

    // Red "EMPTY" Button
    rect(ctx, popX + 35, popY + 38, 70, 16, PALETTE.red);
    drawText(ctx, "EMPTY BIN", popX + 44, popY + 42, 1, PALETTE.white);

    // Cursor clicking button
    const curX = popX + 85 + Math.round(seededSine(frame * 2, 1, 2));
    const curY = popY + 44;
    line(ctx, curX, curY, curX + 6, curY + 6, PALETTE.white);
    line(ctx, curX, curY, curX + 2, curY + 8, PALETTE.white);
  }

  // Desk Surface
  rect(ctx, 20, 240, 230, 15, PALETTE.steelDark);
  rect(ctx, 20, 255, 230, 80, PALETTE.deepNavy);

  // Keyboard & Mouse on desk
  rect(ctx, 80, 244, 70, 8, PALETTE.black);
  rect(ctx, 165, 245, 12, 6, PALETTE.steelMid);
}

// 2. 2.5D SILICON NAND FLASH & BINARY MATRIX
export function drawSiliconMemoryMatrix(ctx: CanvasRenderingContext2D, frame: number) {
  // Dark cyber motherboard background
  rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT, PALETTE.dark);

  // Header
  rect(ctx, 25, 60, 220, 26, PALETTE.black);
  rect(ctx, 27, 62, 216, 22, PALETTE.deepNavy);
  drawText(ctx, "SSD SILICON MEMORY CHIP", 36, 68, 1, PALETTE.cyan);

  // Main Silicon Chip in 2.5D perspective
  const chipX = 45;
  const chipY = 100;
  const chipW = 180;
  const chipH = 150;

  // Chip substrate
  rect(ctx, chipX - 2, chipY - 2, chipW + 4, chipH + 4, PALETTE.black);
  rect(ctx, chipX, chipY, chipW, chipH, PALETTE.cyberNavy);

  // Gold connector pins on edges
  for (let x = chipX + 10; x < chipX + chipW - 10; x += 12) {
    rect(ctx, x, chipY - 6, 6, 6, PALETTE.gold);
    rect(ctx, x, chipY + chipH, 6, 6, PALETTE.gold);
  }

  // Microscopic Memory Cells Grid (Binary 1s and 0s)
  const gridStartX = chipX + 16;
  const gridStartY = chipY + 20;
  const cols = 8;
  const rows = 6;

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const cellX = gridStartX + c * 18;
      const cellY = gridStartY + r * 18;

      // Memory cell box
      rect(ctx, cellX, cellY, 15, 14, PALETTE.black);
      rect(ctx, cellX + 1, cellY + 1, 13, 12, PALETTE.deepNavy);

      // Binary bit 1 or 0 glowing
      const bitVal = (r * cols + c + Math.floor(frame / 6)) % 2;
      const bitColor = bitVal === 1 ? PALETTE.cyan : PALETTE.neonGreen;
      drawText(ctx, `${bitVal}`, cellX + 4, cellY + 3, 1, bitColor);
    }
  }

  // Status readout below
  rect(ctx, 25, 275, 220, 38, PALETTE.black);
  rect(ctx, 27, 277, 216, 34, PALETTE.deepNavy);
  drawText(ctx, "1.5 GB = 12 BILLION BITS", 40, 283, 1, PALETTE.yellow);
  drawText(ctx, "ERASING ALL TAKES TOO LONG!", 34, 295, 1, PALETTE.red);
}

// 3. MASTER FILE TABLE & UNLINKED POINTER
export function drawMasterFileTable(
  ctx: CanvasRenderingContext2D,
  frame: number,
  isUnlinked: boolean
) {
  rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT, PALETTE.dark);

  // Header
  rect(ctx, 20, 60, 230, 28, PALETTE.black);
  rect(ctx, 22, 62, 226, 24, PALETTE.deepNavy);
  drawText(ctx, "MASTER FILE TABLE (MFT)", 38, 70, 1, PALETTE.cyan);

  // Left Column: Index Pointers
  const col1X = 25;
  const colY = 100;
  const colW = 95;
  const colH = 140;

  rect(ctx, col1X, colY, colW, colH, PALETTE.cyberNavy);
  rect(ctx, col1X, colY, colW, 16, PALETTE.deepNavy);
  drawText(ctx, "INDEX POINTER", col1X + 8, colY + 4, 1, PALETTE.yellow);

  // Pointer Row
  const rowY = colY + 30;
  rect(ctx, col1X + 4, rowY, colW - 8, 22, PALETTE.black);
  drawText(ctx, "Photo.jpg", col1X + 8, rowY + 6, 1, isUnlinked ? PALETTE.steelMid : PALETTE.white);

  // Right Column: Physical Silicon Storage
  const col2X = 150;
  rect(ctx, col2X, colY, colW, colH, PALETTE.cyberNavy);
  rect(ctx, col2X, colY, colW, 16, PALETTE.deepNavy);
  drawText(ctx, "SECTOR DATA", col2X + 12, colY + 4, 1, PALETTE.neonGreen);

  // Data Sector Row
  rect(ctx, col2X + 4, rowY, colW - 8, 22, PALETTE.black);
  drawText(ctx, "0x4F8A (RAW)", col2X + 8, rowY + 6, 1, PALETTE.neonGreen);

  // Pointer Arrow linking them
  if (isUnlinked) {
    // Red broken severed link!
    line(ctx, col1X + colW - 4, rowY + 11, col2X + 4, rowY + 11, PALETTE.red);
    // Big RED 'X' on link
    drawText(ctx, "X", 132, rowY + 6, 2, PALETTE.red);

    // Status Banner: ONLY POINTER DELETED
    rect(ctx, 20, 260, 230, 38, PALETTE.black);
    rect(ctx, 22, 262, 226, 34, PALETTE.deepNavy);
    drawText(ctx, "ONLY THE POINTER IS REMOVED!", 28, 268, 1, PALETTE.red);
    drawText(ctx, "RAW DATA IS STILL ON THE DRIVE!", 26, 280, 1, PALETTE.greenSafe);
  } else {
    // Intact glowing cyan link
    line(ctx, col1X + colW - 4, rowY + 11, col2X + 4, rowY + 11, PALETTE.cyan);
    drawText(ctx, "->", 126, rowY + 6, 1, PALETTE.cyan);
  }
}

// 4. THE BOOK METAPHOR (Tearing Table of Contents)
export function drawBookMetaphor(ctx: CanvasRenderingContext2D, frame: number) {
  rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT, PALETTE.deepNavy);

  // Header
  rect(ctx, 20, 60, 230, 28, PALETTE.black);
  rect(ctx, 22, 62, 226, 24, PALETTE.cyberNavy);
  drawText(ctx, "THE BOOK METAPHOR", 62, 70, 1, PALETTE.yellow);

  // Open Book in 2.5D perspective
  const bookX = 35;
  const bookY = 110;
  const bookW = 200;
  const bookH = 130;

  // Book cover spine
  rect(ctx, bookX - 4, bookY - 4, bookW + 8, bookH + 8, PALETTE.darkRed);
  rect(ctx, bookX, bookY, bookW, bookH, PALETTE.white);
  line(ctx, 135, bookY, 135, bookY + bookH, PALETTE.steelMid);

  // Left Page: "TABLE OF CONTENTS" (Torn out!)
  drawText(ctx, "CONTENTS", bookX + 10, bookY + 10, 1, PALETTE.red);
  // Torn jagged page edges
  for (let y = bookY + 25; y < bookY + bookH - 10; y += 6) {
    line(ctx, bookX + 8, y, bookX + 85 + Math.sin(y + frame) * 4, y, PALETTE.steelMid);
  }
  drawText(ctx, "[TORN OUT!]", bookX + 12, bookY + 80, 1, PALETTE.red);

  // Right Page: All 500 Chapters completely intact!
  drawText(ctx, "CHAPTER 1", bookX + 110, bookY + 10, 1, PALETTE.black);
  for (let y = bookY + 25; y < bookY + bookH - 10; y += 8) {
    line(ctx, bookX + 110, y, bookX + 185, y, PALETTE.steelDark);
  }
  drawText(ctx, "STILL INTACT!", bookX + 112, bookY + 100, 1, PALETTE.matrixGreen);

  // Explanation box below
  rect(ctx, 20, 260, 230, 36, PALETTE.black);
  rect(ctx, 22, 262, 226, 32, PALETTE.deepNavy);
  drawText(ctx, "WITHOUT THE CONTENTS PAGE,", 36, 268, 1, PALETTE.silver);
  drawText(ctx, "THE BOOK IS STILL THERE!", 40, 280, 1, PALETTE.greenSafe);
}

// 5. FORENSIC DATA RECOVERY (Bringing file back to life)
export function drawForensicRecovery(ctx: CanvasRenderingContext2D, frame: number) {
  rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT, PALETTE.dark);

  // Header
  rect(ctx, 20, 60, 230, 28, PALETTE.black);
  rect(ctx, 22, 62, 226, 24, PALETTE.deepNavy);
  drawText(ctx, "DEEP SECTOR RECOVERY TOOL", 32, 70, 1, PALETTE.neonGreen);

  // Laser scanner passing over raw memory block
  const boxX = 40;
  const boxY = 100;
  const boxW = 190;
  const boxH = 130;

  rect(ctx, boxX, boxY, boxW, boxH, PALETTE.black);
  rect(ctx, boxX + 2, boxY + 2, boxW - 4, boxH - 4, PALETTE.cyberNavy);

  // Recovered Photo Preview appearing inside
  const scanProgress = Math.min(1.0, (frame % 90) / 70);
  const photoH = Math.floor(90 * scanProgress);

  // Image silhouette (e.g. sunset landscape)
  rect(ctx, boxX + 25, boxY + 15, 140, photoH, PALETTE.deepNavy);
  circle(ctx, boxX + 60, boxY + 45, 16, PALETTE.yellow); // sun
  // Mountain
  line(ctx, boxX + 25, boxY + 15 + photoH, boxX + 85, boxY + 50, PALETTE.steelMid);
  line(ctx, boxX + 85, boxY + 50, boxX + 165, boxY + 15 + photoH, PALETTE.steelMid);

  // Scanning laser line
  const laserY = boxY + 15 + photoH;
  line(ctx, boxX + 10, laserY, boxX + boxW - 10, laserY, PALETTE.neonGreen);
  line(ctx, boxX + 10, laserY + 1, boxX + boxW - 10, laserY + 1, PALETTE.white);

  // Progress Bar
  rect(ctx, 40, 245, 190, 16, PALETTE.black);
  rect(ctx, 42, 247, Math.floor(186 * scanProgress), 12, PALETTE.neonGreen);
  drawText(ctx, `${Math.floor(scanProgress * 100)}% RECOVERED`, 80, 250, 1, PALETTE.black);

  // Banner
  rect(ctx, 20, 275, 230, 30, PALETTE.black);
  rect(ctx, 22, 277, 226, 26, PALETTE.deepNavy);
  drawText(ctx, "DELETED FILES CAN BE RESCUED!", 28, 284, 1, PALETTE.yellow);
}

// 6. TRUE DATA DESTRUCTION (Overwriting with Zeros)
export function drawTrueDestruction(ctx: CanvasRenderingContext2D, frame: number) {
  rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT, PALETTE.dark);

  // Header
  rect(ctx, 20, 60, 230, 28, PALETTE.black);
  rect(ctx, 22, 62, 226, 24, PALETTE.darkRed);
  drawText(ctx, "HOW TO TRULY DESTROY DATA", 32, 70, 1, PALETTE.white);

  // Grid of blocks being overwritten with ZEROS (0 0 0 0)
  const gridX = 35;
  const gridY = 105;
  const cols = 6;
  const rows = 5;

  const wipeIndex = Math.floor(frame / 2);

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const idx = r * cols + c;
      const bx = gridX + c * 34;
      const by = gridY + r * 28;

      rect(ctx, bx, by, 30, 24, PALETTE.black);
      if (idx <= wipeIndex) {
        // Overwritten with 0!
        rect(ctx, bx + 1, by + 1, 28, 22, PALETTE.darkGreen);
        drawText(ctx, "0", bx + 11, by + 6, 1, PALETTE.matrixGreen);
      } else {
        // Residual old data
        rect(ctx, bx + 1, by + 1, 28, 22, PALETTE.cyberNavy);
        drawText(ctx, "DATA", bx + 4, by + 6, 1, PALETTE.steelMid);
      }
    }
  }

  // Destruction Callout
  rect(ctx, 20, 260, 230, 38, PALETTE.black);
  rect(ctx, 22, 262, 226, 34, PALETTE.deepNavy);
  drawText(ctx, "1. MULTI-PASS ZERO OVERWRITE", 30, 268, 1, PALETTE.greenSafe);
  drawText(ctx, "2. PHYSICAL DRIVE SHREDDING", 32, 280, 1, PALETTE.yellow);
}
