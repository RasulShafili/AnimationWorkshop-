import { circle, line, px, rect, ring, seededSine } from "./pixel";
import { PALETTE } from "./palette";

export type AstronautExpression = "calm" | "shocked" | "gasping" | "unconscious" | "relieved";

export interface AstronautOptions {
  expression?: AstronautExpression;
  breach?: boolean;
  reachArm?: boolean;
  floating?: boolean;
  freezeEffect?: boolean;
  sunHeatEffect?: boolean;
  scale?: number;
}

export function drawAstronaut(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  opts: AstronautOptions = {}
) {
  const expr = opts.expression || "calm";
  const breach = !!opts.breach;
  const reachArm = !!opts.reachArm;
  const floating = opts.floating !== false;
  const scale = opts.scale || 1;

  // Zero-g float drift
  const floatY = floating ? seededSine(frame, 2.5, 3) : 0;
  const floatRot = floating ? seededSine(frame, 1.8, 2) : 0;

  const bx = Math.floor(cx);
  const by = Math.floor(cy + floatY);

  // 1. Life support backpack (PLSS)
  rect(ctx, bx - 16 * scale, by - 26 * scale, 32 * scale, 44 * scale, PALETTE.suitDark);
  rect(ctx, bx - 14 * scale, by - 24 * scale, 28 * scale, 40 * scale, PALETTE.suitShade);
  // Backpack vents
  rect(ctx, bx - 11 * scale, by - 20 * scale, 8 * scale, 4 * scale, "#222a36");
  rect(ctx, bx + 3 * scale, by - 20 * scale, 8 * scale, 4 * scale, "#222a36");

  // 2. Torso (EMU Suit Body)
  rect(ctx, bx - 12 * scale, by - 14 * scale, 24 * scale, 28 * scale, PALETTE.suitWhite);
  // Shading on right side
  rect(ctx, bx + 6 * scale, by - 14 * scale, 6 * scale, 28 * scale, PALETTE.suitShade);

  // Chest Display Unit (CDU)
  rect(ctx, bx - 7 * scale, by - 10 * scale, 14 * scale, 12 * scale, PALETTE.suitDark);
  rect(ctx, bx - 5 * scale, by - 8 * scale, 10 * scale, 8 * scale, "#182230");

  // Status LEDs on chest
  const ledColor = breach ? ((frame % 10 < 5) ? PALETTE.hazardRed : "#4a1212") : PALETTE.hudGreen;
  px(ctx, bx - 3 * scale, by - 6 * scale, ledColor);
  px(ctx, bx * scale, by - 6 * scale, PALETTE.solarYellow);
  px(ctx, bx + 3 * scale, by - 6 * scale, PALETTE.iceCyan);

  // 3. Legs
  const legSwing = floating ? seededSine(frame, 3, 2) : 0;
  // Left leg
  rect(ctx, bx - 10 * scale, by + 14 * scale, 8 * scale, 16 * scale, PALETTE.suitWhite);
  rect(ctx, bx - 10 * scale, by + 22 * scale, 8 * scale, 3 * scale, PALETTE.suitShade); // Joint ring
  rect(ctx, bx - 11 * scale, by + 28 * scale, 9 * scale, 6 * scale, PALETTE.suitDark);  // Left boot
  // Right leg
  rect(ctx, bx + 2 * scale, by + 14 * scale + legSwing, 8 * scale, 16 * scale, PALETTE.suitShade);
  rect(ctx, bx + 2 * scale, by + 22 * scale + legSwing, 8 * scale, 3 * scale, PALETTE.suitDark);  // Joint ring
  rect(ctx, bx + 2 * scale, by + 28 * scale + legSwing, 9 * scale, 6 * scale, PALETTE.suitDark);  // Right boot

  // 4. Arms
  // Left arm
  if (reachArm) {
    // Reaching across chest to hold breached arm
    rect(ctx, bx - 16 * scale, by - 12 * scale, 6 * scale, 14 * scale, PALETTE.suitWhite);
    rect(ctx, bx - 12 * scale, by + 2 * scale, 16 * scale, 6 * scale, PALETTE.suitWhite);
    circle(ctx, bx + 4 * scale, by + 5 * scale, 3 * scale, PALETTE.suitDark); // Gloved hand
  } else {
    const armWiggle = floating ? seededSine(frame, 2, 2) : 0;
    rect(ctx, bx - 18 * scale, by - 12 * scale + armWiggle, 6 * scale, 18 * scale, PALETTE.suitWhite);
    circle(ctx, bx - 15 * scale, by + 7 * scale + armWiggle, 3 * scale, PALETTE.suitDark); // Glove
  }

  // Right arm (where puncture/breach happens)
  const rArmY = by - 12 * scale;
  rect(ctx, bx + 12 * scale, rArmY, 6 * scale, 18 * scale, PALETTE.suitShade);
  circle(ctx, bx + 15 * scale, rArmY + 19 * scale, 3 * scale, PALETTE.suitDark); // Glove

  // BREACH EFFECT: Vapor jet & hole
  if (breach) {
    // Hole on right sleeve
    px(ctx, bx + 14 * scale, rArmY + 8 * scale, PALETTE.hazardRed);
    px(ctx, bx + 15 * scale, rArmY + 8 * scale, "#000000");

    // Pressure jet spraying into vacuum
    for (let p = 0; p < 12; p++) {
      const pSpeed = 2 + (p % 4);
      const pxX = bx + 17 * scale + ((frame * pSpeed + p * 7) % 36);
      const pxY = rArmY + 8 * scale + seededSine(frame * 3 + p * 15, 4, 6);
      const pAlpha = Math.max(0, 1 - (pxX - (bx + 17 * scale)) / 36);
      if (pAlpha > 0.2) {
        px(ctx, pxX, pxY, (p % 2 === 0) ? PALETTE.cloudWhite : PALETTE.earthAtmosphere);
      }
    }
  }

  // 5. Helmet & Neck Ring
  rect(ctx, bx - 11 * scale, by - 16 * scale, 22 * scale, 4 * scale, PALETTE.suitDark); // Neck ring
  // Helmet dome
  circle(ctx, bx, by - 26 * scale, 15 * scale, PALETTE.suitWhite);
  // Visor (Gold / Cyan reflective glass)
  circle(ctx, bx, by - 26 * scale, 11 * scale, PALETTE.deepBlue);
  // Visor reflection (curved gold & atmosphere highlight)
  circle(ctx, bx - 2 * scale, by - 28 * scale, 8 * scale, PALETTE.earthCyan);
  rect(ctx, bx - 8 * scale, by - 26 * scale, 16 * scale, 6 * scale, "#142542");

  // 6. Face inside visor
  const vx = bx;
  const vy = by - 26 * scale;

  if (expr === "calm") {
    // Eyes looking forward
    px(ctx, vx - 4 * scale, vy - 1 * scale, "#ffffff");
    px(ctx, vx + 3 * scale, vy - 1 * scale, "#ffffff");
    // Pupils
    px(ctx, vx - 3 * scale, vy - 1 * scale, "#1a2233");
    px(ctx, vx + 4 * scale, vy - 1 * scale, "#1a2233");
    // Calm mouth
    rect(ctx, vx - 2 * scale, vy + 4 * scale, 4 * scale, 1 * scale, PALETTE.suitShade);
  } else if (expr === "shocked") {
    // Wide open eyes
    rect(ctx, vx - 5 * scale, vy - 3 * scale, 3 * scale, 3 * scale, "#ffffff");
    rect(ctx, vx + 2 * scale, vy - 3 * scale, 3 * scale, 3 * scale, "#ffffff");
    px(ctx, vx - 4 * scale, vy - 2 * scale, "#000000");
    px(ctx, vx + 3 * scale, vy - 2 * scale, "#000000");
    // Open gasping mouth
    circle(ctx, vx, vy + 3 * scale, 2 * scale, "#1a0808");
    // Sweat drops
    px(ctx, vx + 7 * scale, vy - 4 * scale, PALETTE.earthAtmosphere);
    px(ctx, vx - 7 * scale, vy - 2 * scale, PALETTE.earthAtmosphere);
  } else if (expr === "gasping") {
    // Agonized eyes
    line(ctx, vx - 5 * scale, vy - 3 * scale, vx - 2 * scale, vy - 1 * scale, "#ffffff");
    line(ctx, vx + 2 * scale, vy - 1 * scale, vx + 5 * scale, vy - 3 * scale, "#ffffff");
    // Open mouth with boiling moisture
    circle(ctx, vx, vy + 3 * scale, 3 * scale, "#2a0a0a");
    // Boiling bubbles inside visor
    const bub1 = (frame * 2) % 8;
    px(ctx, vx - 1 + (frame % 3), vy + 3 - bub1, PALETTE.cloudWhite);
  } else if (expr === "unconscious") {
    // Slanted closed eyes
    line(ctx, vx - 5 * scale, vy - 1 * scale, vx - 2 * scale, vy, "#ffffff");
    line(ctx, vx + 2 * scale, vy, vx + 5 * scale, vy - 1 * scale, "#ffffff");
    // Limp mouth
    line(ctx, vx - 2 * scale, vy + 4 * scale, vx + 2 * scale, vy + 4 * scale, PALETTE.suitDark);
  } else if (expr === "relieved") {
    // Happy arch eyes
    px(ctx, vx - 4 * scale, vy - 2 * scale, "#ffffff");
    px(ctx, vx - 3 * scale, vy - 3 * scale, "#ffffff");
    px(ctx, vx - 2 * scale, vy - 2 * scale, "#ffffff");
    px(ctx, vx + 2 * scale, vy - 2 * scale, "#ffffff");
    px(ctx, vx + 3 * scale, vy - 3 * scale, "#ffffff");
    px(ctx, vx + 4 * scale, vy - 2 * scale, "#ffffff");
    // Big smile
    line(ctx, vx - 3 * scale, vy + 3 * scale, vx + 3 * scale, vy + 3 * scale, PALETTE.suitWhite);
    px(ctx, vx - 3 * scale, vy + 2 * scale, PALETTE.suitWhite);
    px(ctx, vx + 3 * scale, vy + 2 * scale, PALETTE.suitWhite);
  }

  // 7. Thermal / Ice overlays
  if (opts.freezeEffect) {
    // Blue frost crystals coating right half
    for (let c = 0; c < 15; c++) {
      const fx = bx + 4 + (c * 7) % 18;
      const fy = by - 30 + (c * 11) % 55;
      px(ctx, fx, fy, PALETTE.iceCyan);
      if (c % 2 === 0) px(ctx, fx + 1, fy, PALETTE.cloudWhite);
    }
  }

  if (opts.sunHeatEffect) {
    // Solar radiance outline on left half
    for (let h = 0; h < 20; h++) {
      const hx = bx - 18 - (h * 3) % 10;
      const hy = by - 35 + (h * 5) % 65;
      px(ctx, hx, hy, (h % 2 === 0) ? PALETTE.solarYellow : PALETTE.hazardOrange);
    }
  }
}
