import { rect, circle, drawText, ART_WIDTH } from "./pixel";
import { PALETTE } from "./palette";

/**
 * Draw heavy work-class deep-sea ROV (Remotely Operated Vehicle)
 * with yellow buoyancy chassis, thrusters, floodlights, and hydraulic robotic arms.
 * Strict bounds: kept within y <= 255.
 */
export function drawDeepSeaROV(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  opts: {
    clawOpen?: boolean;
    holdingCable?: boolean;
    lightOn?: boolean;
  } = {}
) {
  const { clawOpen = false, holdingCable = false, lightOn = true } = opts;
  const bob = Math.sin(frame * 0.12) * 2;

  // 1. Conical halogen floodlight beams cutting into dark abyss
  if (lightOn) {
    const lx = cx - 24;
    const ly = cy + 6 + bob;

    // Left floodlight beam
    ctx.save();
    ctx.fillStyle = "rgba(34, 211, 238, 0.12)";
    ctx.beginPath();
    ctx.moveTo(lx, ly);
    ctx.lineTo(lx - 55, ly + 65);
    ctx.lineTo(lx + 20, ly + 65);
    ctx.closePath();
    ctx.fill();

    // Right floodlight beam
    const rx = cx + 24;
    ctx.beginPath();
    ctx.moveTo(rx, ly);
    ctx.lineTo(rx - 20, ly + 65);
    ctx.lineTo(rx + 55, ly + 65);
    ctx.closePath();
    ctx.fill();
    ctx.restore();
  }

  // 2. Main ROV Yellow Buoyancy Foam Chassis
  const rx = cx - 34;
  const ry = cy - 20 + bob;
  const rw = 68;
  const rh = 34;

  // Upper yellow foam block
  rect(ctx, rx, ry, rw, rh, PALETTE.rovYellow);
  rect(ctx, rx + 2, ry + 2, rw - 4, 6, "#fef08a"); // top highlight
  rect(ctx, rx, ry + rh - 6, rw, 6, PALETTE.rovShadow); // bottom shade

  // Subsea equipment decals
  rect(ctx, rx + 12, ry + 12, 14, 8, "#1e293b"); // side instrumentation
  circle(ctx, rx + 19, ry + 16, 2, PALETTE.laserCyan); // sensor eye
  rect(ctx, rx + 34, ry + 12, 22, 6, "#334155"); // pressure canister

  // 3. Ducted Thrusters (left & right)
  // Left thruster
  rect(ctx, rx - 10, ry + 8, 10, 16, "#475569");
  rect(ctx, rx - 10, ry + 11, 2, 10, "#0f172a");
  // Right thruster
  rect(ctx, rx + rw, ry + 8, 10, 16, "#475569");
  rect(ctx, rx + rw + 8, ry + 11, 2, 10, "#0f172a");

  // Thruster cavitation bubbles
  const bubbleFrame = frame % 16;
  circle(ctx, rx - 14 - bubbleFrame, ry + 16 + (bubbleFrame % 3), 1, "rgba(255, 255, 255, 0.6)");
  circle(ctx, rx + rw + 14 + bubbleFrame, ry + 16 - (bubbleFrame % 3), 1, "rgba(255, 255, 255, 0.6)");

  // 4. Heavy Steel Crash Frame (tubular roll-cage beneath)
  rect(ctx, rx - 4, ry + rh, rw + 8, 5, "#64748b");
  rect(ctx, rx - 2, ry + rh + 5, 8, 8, "#475569"); // landing skid left
  rect(ctx, rx + rw - 6, ry + rh + 5, 8, 8, "#475569"); // landing skid right

  // 5. High-Intensity Floodlight Housings
  rect(ctx, rx + 6, ry + rh - 4, 8, 6, "#0f172a");
  circle(ctx, rx + 10, ry + rh - 1, 3, "#ffffff");
  rect(ctx, rx + rw - 14, ry + rh - 4, 8, 6, "#0f172a");
  circle(ctx, rx + rw - 10, ry + rh - 1, 3, "#ffffff");

  // 6. Yellow Umbilical Cable Tether (leading up to surface ship)
  const tetherX = cx;
  const tetherY = ry;
  for (let u = 0; u < 25; u++) {
    const ux = tetherX + Math.sin((u + frame * 0.2) * 0.3) * 3;
    const uy = tetherY - u;
    rect(ctx, ux, uy, 2, 1, PALETTE.dataPulseYellow);
  }

  // 7. Articulated Hydraulic Robotic Arm & Grappling Claw
  const armBaseX = cx + 18;
  const armBaseY = ry + rh;

  // Upper boom
  rect(ctx, armBaseX, armBaseY, 6, 12, "#334155");
  circle(ctx, armBaseX + 3, armBaseY + 12, 3, "#94a3b8"); // elbow joint

  // Forearm extending down
  const armAngle = holdingCable ? 16 : (clawOpen ? 22 : 18);
  rect(ctx, armBaseX + 1, armBaseY + 12, 4, armAngle, "#475569");
  const wristY = armBaseY + 12 + armAngle;

  // Hydraulic Gripping Claw
  if (clawOpen) {
    // Open jaws
    rect(ctx, armBaseX - 4, wristY, 3, 7, "#cbd5e1");
    rect(ctx, armBaseX + 6, wristY, 3, 7, "#cbd5e1");
  } else {
    // Closed jaws clamping
    rect(ctx, armBaseX - 1, wristY, 7, 7, "#cbd5e1");
    rect(ctx, armBaseX, wristY + 2, 5, 3, "#0f172a");
  }

  // Cable clamped in claw
  if (holdingCable) {
    rect(ctx, armBaseX - 35, wristY + 3, 85, 4, PALETTE.polyethyleneBlack);
    rect(ctx, armBaseX - 35, wristY + 4, 85, 1, PALETTE.copperConductor);
    // Glowing severed fiber tip
    circle(ctx, armBaseX + 50, wristY + 5, 2, PALETTE.laserCyan);
    circle(ctx, armBaseX + 50, wristY + 5, 1, "#ffffff");
  }
}

/**
 * Draw Cleanroom Technician aboard Cable Ship
 * with anti-static bunny suit, bilateral magnification loupes, and precision tools.
 * Strict bounds: kept within y <= 255.
 */
export function drawRepairTechnician(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number
) {
  const breath = Math.sin(frame * 0.1) * 1.5;

  // 1. Shoulders & White Anti-Static Bunny Suit
  rect(ctx, cx - 38, cy + 30 + breath, 76, 50, "#f8fafc");
  rect(ctx, cx - 38, cy + 30 + breath, 76, 2, "#cbd5e1"); // collar
  rect(ctx, cx - 14, cy + 24 + breath, 28, 10, "#e2e8f0"); // neck

  // 2. Head with Cleanroom Hood
  rect(ctx, cx - 25, cy - 25, 50, 52, "#ffffff");
  rect(ctx, cx - 22, cy - 28, 44, 56, "#ffffff");
  rect(ctx, cx - 20, cy - 30, 40, 58, "#ffffff");
  // Hood elastic seam
  rect(ctx, cx - 21, cy - 20, 42, 2, "#94a3b8");

  // 3. Face Opening & Skin
  rect(ctx, cx - 18, cy - 16, 36, 26, "#fed7aa"); // face
  rect(ctx, cx - 16, cy - 18, 32, 28, "#fed7aa");

  // 4. BILATERAL EYES & Precision Magnification Loupes (Symmetrical!)
  const eyeY = cy - 8;
  const spacing = 9;

  // Left Eye
  rect(ctx, cx - spacing - 4, eyeY, 8, 6, "#ffffff");
  circle(ctx, cx - spacing, eyeY + 3, 2, "#1e293b");
  // Right Eye
  rect(ctx, cx + spacing - 4, eyeY, 8, 6, "#ffffff");
  circle(ctx, cx + spacing, eyeY + 3, 2, "#1e293b");

  // High-Tech Surgical/Optical Magnification Loupes (Binocular barrels)
  // Left loupe barrel
  rect(ctx, cx - spacing - 5, eyeY - 2, 10, 9, "#334155");
  rect(ctx, cx - spacing - 3, eyeY + 7, 6, 4, "#0284c7");
  circle(ctx, cx - spacing, eyeY + 9, 2, PALETTE.laserCyan); // blue coated lens
  // Right loupe barrel
  rect(ctx, cx + spacing - 5, eyeY - 2, 10, 9, "#334155");
  rect(ctx, cx + spacing - 3, eyeY + 7, 6, 4, "#0284c7");
  circle(ctx, cx + spacing, eyeY + 9, 2, PALETTE.laserCyan); // blue coated lens
  // Bridge connecting both loupes
  rect(ctx, cx - spacing, eyeY + 2, spacing * 2, 2, "#0f172a");

  // Headband for loupes
  rect(ctx, cx - 22, eyeY - 4, 44, 2, "#0f172a");

  // 5. Cleanroom Face Mask (covering nose & mouth)
  rect(ctx, cx - 18, cy + 2, 36, 16, "#e0f2fe");
  rect(ctx, cx - 16, cy + 2, 32, 16, "#bae6fd");
  rect(ctx, cx - 16, cy + 7, 32, 1, "#7dd3fc"); // mask pleats
  rect(ctx, cx - 16, cy + 12, 32, 1, "#7dd3fc");

  // 6. Cleanroom Nitrile Gloves & Micro-Tweezers (bottom hands)
  rect(ctx, cx - 22, cy + 62, 12, 14, "#38bdf8"); // left glove
  rect(ctx, cx + 10, cy + 62, 12, 14, "#38bdf8"); // right glove
  // Silver precision tweezers
  rect(ctx, cx - 14, cy + 72, 14, 2, "#cbd5e1");
  rect(ctx, cx + 2, cy + 72, 14, 2, "#cbd5e1");
}
