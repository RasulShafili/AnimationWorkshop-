import { rect, circle, drawText, ART_WIDTH } from "./pixel";
import { PALETTE } from "./palette";

/**
 * Draw menacing Pit Viper snake with coiled body, diamondback scales,
 * striking jaw, heat pits, slit pupil, and venom dripping fangs.
 * Strict bounds: kept within y <= 255.
 */
export function drawViperSnake(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  strikeLunge: number = 0 // 0 to 1
) {
  const lungeX = Math.floor(strikeLunge * 28);
  const breath = Math.sin(frame * 0.12) * 2;
  const tongueFlick = frame % 45 < 15;

  // 1. Coiled body behind
  for (let c = 0; c < 3; c++) {
    const coilY = cy + 50 + c * 16 + breath;
    const coilW = 140 - c * 25;
    const coilH = 22;
    // Dark green body
    rect(ctx, cx - coilW / 2 + (c % 2 ? 8 : -8), coilY, coilW, coilH, "#1b4332");
    // Dorsal scales
    rect(ctx, cx - coilW / 2 + 6, coilY + 2, coilW - 12, 4, "#2d6a4f");
    // Diamond markings
    for (let dx = cx - coilW / 2 + 15; dx < cx + coilW / 2 - 15; dx += 20) {
      rect(ctx, dx, coilY + 5, 8, 8, "#081c15");
      rect(ctx, dx + 2, coilY + 7, 4, 4, "#d8f3dc");
    }
    // Underside belly scales
    rect(ctx, cx - coilW / 2 + (c % 2 ? 8 : -8), coilY + coilH - 5, coilW, 4, "#d9ed92");
  }

  // 2. Muscular S-curve neck
  const neckX = cx + lungeX - 10;
  const neckY = cy + 20 + breath;
  for (let ny = 0; ny < 35; ny += 3) {
    const t = ny / 35;
    const nx = neckX + Math.sin(t * Math.PI * 1.5) * 16;
    rect(ctx, nx - 14, neckY + ny, 28, 4, "#2d6a4f");
    rect(ctx, nx - 6, neckY + ny, 12, 3, "#40916c");
    rect(ctx, nx - 14, neckY + ny + 1, 4, 2, "#d9ed92");
  }

  // 3. Triangular Pit Viper Head
  const headX = cx + lungeX + 25;
  const headY = cy + 12 + breath;

  // Upper snout / skull
  rect(ctx, headX - 25, headY - 14, 45, 18, "#1b4332");
  rect(ctx, headX - 15, headY - 18, 30, 8, "#2d6a4f");
  rect(ctx, headX + 15, headY - 10, 16, 12, "#1b4332"); // snout tip

  // Diamond scale pattern on skull
  rect(ctx, headX - 8, headY - 16, 6, 6, "#081c15");
  rect(ctx, headX + 4, headY - 14, 6, 6, "#081c15");
  rect(ctx, headX - 6, headY - 14, 2, 2, "#b7e4c7");

  // Heat-sensing pit between eye and nostril
  rect(ctx, headX + 12, headY - 6, 4, 3, "#081c15");

  // Vertical yellow slit eye
  rect(ctx, headX, headY - 12, 8, 8, "#ffd43b");
  rect(ctx, headX + 3, headY - 12, 2, 8, "#000000"); // slit pupil
  rect(ctx, headX + 1, headY - 13, 6, 2, "#081c15"); // supraocular scale brow

  // Open gaping lower jaw (gape angle depends on strikeLunge)
  const jawDrop = Math.floor(12 + strikeLunge * 14);
  rect(ctx, headX - 20, headY + 4, 38, 8 + jawDrop, "#99e9f2"); // mouth interior pink/pale
  rect(ctx, headX - 22, headY + 4, 40, 4, "#e03131"); // inner gum line
  rect(ctx, headX - 18, headY + 6 + jawDrop, 36, 6, "#2d6a4f"); // lower mandible skin
  rect(ctx, headX - 15, headY + 11 + jawDrop, 30, 4, "#d9ed92"); // lower chin

  // 4. Deadly Hollow Fangs & Venom Droplets
  const fangBaseX = headX + 14;
  const fangBaseY = headY + 2;
  const fangLen = 14;

  // Left fang (sheathed/exposed)
  for (let f = 0; f < fangLen; f++) {
    const fx = fangBaseX - Math.floor((f * f) / 32);
    const fy = fangBaseY + f;
    rect(ctx, fx, fy, 3, 1, "#f8f9fa"); // enamel white
    if (f > 8) rect(ctx, fx + 1, fy, 1, 1, "#dee2e6");
  }

  // Right fang (perspective inner)
  for (let f = 0; f < fangLen - 2; f++) {
    const fx = fangBaseX - 6 - Math.floor((f * f) / 36);
    const fy = fangBaseY + f;
    rect(ctx, fx, fy, 2, 1, "#e9ecef");
  }

  // Venom gland & venom canal duct highlight
  rect(ctx, headX - 12, headY - 4, 14, 6, "rgba(81, 207, 102, 0.4)");

  // Glistening venom droplet forming at fang tip
  const dropGlow = Math.sin(frame * 0.25) * 0.3 + 0.7;
  const dropY = fangBaseY + fangLen + (frame % 18 < 6 ? 1 : 0);
  circle(ctx, fangBaseX - 3, dropY, 2, PALETTE.venomToxicLime);
  circle(ctx, fangBaseX - 3, dropY + 1, 1, "#ffffff");
  if (strikeLunge > 0.5) {
    // Flying venom spray droplets
    rect(ctx, fangBaseX + 6, dropY + 4, 2, 2, PALETTE.venomGreen);
    rect(ctx, fangBaseX + 14, dropY + 8, 2, 2, PALETTE.venomToxicLime);
    rect(ctx, fangBaseX + 22, dropY + 12, 1, 1, "#a9e34b");
  }

  // Forked tongue flicking
  if (tongueFlick && strikeLunge < 0.3) {
    const tx = headX + 24;
    const ty = headY + 4;
    rect(ctx, tx, ty, 10, 2, "#495057"); // tongue base
    rect(ctx, tx + 10, ty - 2, 6, 1, "#212529"); // upper fork
    rect(ctx, tx + 10, ty + 3, 6, 1, "#212529"); // lower fork
  }
}

/**
 * Draw human patient with bilateral anatomical symmetry.
 * Both left and right eyes rendered with eyelid drooping (ptosis),
 * respiratory strain or stable medical ICU recovery.
 * Strict bounds: kept within y <= 255.
 */
export function drawPatient(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  opts: {
    eyelidDroop?: number; // 0 (open) to 1 (shut)
    sweat?: boolean;
    pale?: boolean;
    oxygenMask?: boolean;
    recovery?: boolean;
  } = {}
) {
  const { eyelidDroop = 0, sweat = false, pale = false, oxygenMask = false, recovery = false } = opts;
  const skin = pale ? "#d0b8ac" : PALETTE.skinTone;
  const skinDark = pale ? "#9c8175" : PALETTE.skinShadow;
  const breath = recovery ? Math.sin(frame * 0.08) * 2 : Math.sin(frame * 0.2) * 3;

  // Hospital gown / shoulders
  const gownColor = recovery ? "#4dabf7" : "#868e96";
  rect(ctx, cx - 45, cy + 42 + breath, 90, 48, gownColor);
  rect(ctx, cx - 18, cy + 34 + breath, 36, 12, skinDark); // neck
  rect(ctx, cx - 16, cy + 34 + breath, 32, 12, skin);

  // Head base
  rect(ctx, cx - 28, cy - 25, 56, 62, skin);
  rect(ctx, cx - 26, cy - 27, 52, 64, skin);
  rect(ctx, cx - 24, cy - 29, 48, 66, skin);

  // Dark brown hair
  rect(ctx, cx - 28, cy - 35, 56, 14, "#2b1e16");
  rect(ctx, cx - 30, cy - 28, 8, 22, "#2b1e16");
  rect(ctx, cx + 22, cy - 28, 8, 22, "#2b1e16");
  rect(ctx, cx - 24, cy - 36, 48, 4, "#3e2c20");

  // Ears
  rect(ctx, cx - 31, cy - 5, 4, 12, skinDark);
  rect(ctx, cx + 27, cy - 5, 4, 12, skinDark);

  // Eyebrows (strained or resting)
  const browY = cy - 12 + (eyelidDroop > 0.5 ? 2 : 0);
  rect(ctx, cx - 20, browY, 14, 3, "#2b1e16");
  rect(ctx, cx + 6, browY, 14, 3, "#2b1e16");

  // BILATERAL EYES: Strictly draw BOTH left and right eyes symmetrically!
  const eyeY = cy - 6;
  const eyeSpacing = 13;

  // Left Eye
  rect(ctx, cx - eyeSpacing - 6, eyeY, 12, 8, "#ffffff"); // sclera
  rect(ctx, cx - eyeSpacing - 2, eyeY + 1, 5, 6, "#2b1e16"); // iris
  circle(ctx, cx - eyeSpacing, eyeY + 4, 1, "#000000"); // pupil
  // Right Eye
  rect(ctx, cx + eyeSpacing - 6, eyeY, 12, 8, "#ffffff"); // sclera
  rect(ctx, cx + eyeSpacing - 3, eyeY + 1, 5, 6, "#2b1e16"); // iris
  circle(ctx, cx + eyeSpacing - 1, eyeY + 4, 1, "#000000"); // pupil

  // Drooping Eyelids (Ptosis - hallmark of neurotoxic envenomation)
  if (eyelidDroop > 0.1) {
    const droopH = Math.min(8, Math.floor(eyelidDroop * 8));
    // Left eyelid
    rect(ctx, cx - eyeSpacing - 6, eyeY, 12, droopH, skinDark);
    rect(ctx, cx - eyeSpacing - 6, eyeY + droopH - 1, 12, 1, "#495057"); // lash line
    // Right eyelid
    rect(ctx, cx + eyeSpacing - 6, eyeY, 12, droopH, skinDark);
    rect(ctx, cx + eyeSpacing - 6, eyeY + droopH - 1, 12, 1, "#495057"); // lash line
  }

  // Nose
  rect(ctx, cx - 2, cy + 2, 4, 10, skinDark);
  rect(ctx, cx - 4, cy + 10, 8, 2, skinDark);

  // Mouth / Lips
  if (oxygenMask) {
    // Clear medical mask over nose and mouth
    rect(ctx, cx - 18, cy + 6, 36, 26, "rgba(220, 240, 255, 0.45)");
    rect(ctx, cx - 18, cy + 6, 36, 1, "#74c0fc");
    rect(ctx, cx - 18, cy + 31, 36, 1, "#74c0fc");
    // Elastic strap
    rect(ctx, cx - 28, cy + 14, 10, 2, "#495057");
    rect(ctx, cx + 18, cy + 14, 10, 2, "#495057");
    // Green O2 tubing
    rect(ctx, cx - 2, cy + 32, 4, 30, PALETTE.hudGreen);
  } else {
    // Strained open mouth gasping for air
    if (pale && eyelidDroop > 0.4) {
      rect(ctx, cx - 8, cy + 18, 16, 7, "#343a40");
      rect(ctx, cx - 6, cy + 19, 12, 2, "#e9ecef"); // upper teeth
      rect(ctx, cx - 10, cy + 17, 20, 2, skinDark); // lip shadow
    } else {
      rect(ctx, cx - 8, cy + 19, 16, 3, skinDark);
    }
  }

  // Cold sweat beads running down temples
  if (sweat) {
    const swY = (frame * 1.5) % 30;
    circle(ctx, cx - 22, cy - 8 + swY, 1, "#a5d8ff");
    circle(ctx, cx + 20, cy - 4 + (swY * 0.8), 1, "#a5d8ff");
  }

  // Pulse oximeter on patient's finger (bottom right)
  if (recovery) {
    rect(ctx, cx + 34, cy + 62, 14, 8, "#212529");
    circle(ctx, cx + 41, cy + 66, 2, "#ff6b6b"); // red sensor LED
    rect(ctx, cx + 41, cy + 70, 2, 25, "#868e96"); // wire to monitor
  }
}
