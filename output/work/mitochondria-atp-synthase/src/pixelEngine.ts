// Mitochondria ATP Synthase Nanomotor Pixel Engine (360x640 Canvas)
export const PW = 360;
export const PH = 640;

// Pixel drawing primitives
export function pRect(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  color: string
) {
  ctx.fillStyle = color;
  ctx.fillRect(Math.round(x), Math.round(y), Math.round(w), Math.round(h));
}

export function pCircle(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  r: number,
  color: string,
  step = 2
) {
  ctx.fillStyle = color;
  const rc = Math.round(r);
  for (let dy = -rc; dy <= rc; dy += step) {
    for (let dx = -rc; dx <= rc; dx += step) {
      if (dx * dx + dy * dy <= rc * rc) {
        ctx.fillRect(Math.round(cx + dx), Math.round(cy + dy), step, step);
      }
    }
  }
}

// 1. Draw Cellular Environment / Macro Cristae Background
export function drawCellularBackground(ctx: CanvasRenderingContext2D, frame: number) {
  // Deep mitochondrial matrix background
  ctx.fillStyle = "#0A0914";
  ctx.fillRect(0, 0, PW, PH);

  // Cytoplasmic muscle fiber striations in distance (subtle moving dark bands)
  for (let y = 0; y < PH; y += 8) {
    const band = Math.sin(y * 0.05 + frame * 0.02);
    if (band > 0.3) {
      ctx.fillStyle = "rgba(42, 10, 24, 0.25)";
      ctx.fillRect(0, y, PW, 4);
    }
  }

  // Floating background mitochondrial ribosomes and metabolic particles
  for (let i = 0; i < 28; i++) {
    const seed = i * 997;
    const bx = (seed + frame * (0.3 + (i % 3) * 0.2)) % (PW + 40) - 20;
    const by = (seed * 3 + Math.sin(frame * 0.03 + i) * 15) % PH;
    const r = (i % 3) + 1;
    const col = i % 2 === 0 ? "rgba(100, 200, 255, 0.15)" : "rgba(255, 180, 80, 0.12)";
    pCircle(ctx, bx, by, r, col, 2);
  }
}

// Macro Mitochondria overview in early frames (Scene 1: f0 - f120)
export function drawMacroMitochondria(
  ctx: CanvasRenderingContext2D,
  frame: number,
  alpha: number
) {
  if (alpha <= 0.01) return;
  ctx.save();
  ctx.globalAlpha = alpha;

  const cx = 180;
  const cy = 370;

  // Outer membrane glowing bean
  for (let dy = -100; dy <= 100; dy += 2) {
    const rad = Math.sqrt(Math.max(0, 1 - Math.pow(dy / 100, 2))) * 125;
    ctx.fillStyle = "#E64A19";
    ctx.fillRect(cx - rad, cy + dy, rad * 2, 2);
  }
  // Intermembrane Space
  for (let dy = -94; dy <= 94; dy += 2) {
    const rad = Math.sqrt(Math.max(0, 1 - Math.pow(dy / 94, 2))) * 118;
    ctx.fillStyle = "#FF7043";
    ctx.fillRect(cx - rad, cy + dy, rad * 2, 2);
  }
  // Inner matrix void
  for (let dy = -88; dy <= 88; dy += 2) {
    const rad = Math.sqrt(Math.max(0, 1 - Math.pow(dy / 88, 2))) * 110;
    ctx.fillStyle = "#1E0810";
    ctx.fillRect(cx - rad, cy + dy, rad * 2, 2);
  }

  // Folded Cristae convolutions
  const folds = [
    { y: -70, len: 85, dir: 1 },
    { y: -46, len: 95, dir: -1 },
    { y: -22, len: 100, dir: 1 },
    { y: 2, len: 105, dir: -1 },
    { y: 26, len: 100, dir: 1 },
    { y: 50, len: 95, dir: -1 },
    { y: 72, len: 85, dir: 1 },
  ];

  folds.forEach((f) => {
    const sx = f.dir > 0 ? cx - 100 : cx + 100 - f.len;
    pRect(ctx, sx, cy + f.y, f.len, 12, "#FF7043");
    pRect(ctx, sx + (f.dir > 0 ? 0 : 4), cy + f.y + 2, f.len - 4, 8, "#FFB74D");

    // Mini rotary engine specks on cristae folds!
    for (let sp = 10; sp < f.len - 8; sp += 16) {
      const mx = sx + sp;
      const my = cy + f.y + (f.dir > 0 ? 14 : -4);
      pCircle(ctx, mx, my, 3, "#00E5FF", 1);
      pCircle(ctx, mx, my + 3, 2, "#FFD54F", 1);
    }
  });

  // Floating Mitochondrial DNA loops (mtDNA)
  pCircle(ctx, cx - 40, cy + 30, 8, "#76FF03", 2);
  pCircle(ctx, cx - 40, cy + 30, 5, "#1E0810", 2);
  pCircle(ctx, cx + 35, cy - 35, 7, "#76FF03", 2);
  pCircle(ctx, cx + 35, cy - 35, 4, "#1E0810", 2);

  // Zooming Target Reticle
  const pulse = Math.sin(frame * 0.15) * 3;
  const rw = 70 + pulse * 2;
  const rh = 46 + pulse * 2;
  ctx.strokeStyle = "#00E5FF";
  ctx.lineWidth = 2;
  ctx.strokeRect(cx - rw / 2, cy - rh / 2, rw, rh);

  // Crosshairs
  pRect(ctx, cx - rw / 2 - 8, cy, 6, 2, "#00E5FF");
  pRect(ctx, cx + rw / 2 + 2, cy, 6, 2, "#00E5FF");
  pRect(ctx, cx, cy - rh / 2 - 8, 2, 6, "#00E5FF");
  pRect(ctx, cx, cy + rh / 2 + 2, 2, 6, "#00E5FF");

  // Label above reticle
  pRect(ctx, cx - 75, cy - rh / 2 - 18, 150, 14, "rgba(0,0,0,0.85)");
  ctx.strokeStyle = "#00E5FF";
  ctx.strokeRect(cx - 75, cy - rh / 2 - 18, 150, 14);
  ctx.fillStyle = "#00E5FF";
  ctx.font = "8px monospace";
  ctx.fillText("TARGET: CRISTAE [100,000x]", cx - 68, cy - rh / 2 - 8);

  ctx.restore();
}

// 2. The Inner Mitochondrial Membrane (Lipid Bilayer)
export function drawLipidBilayer(ctx: CanvasRenderingContext2D, frame: number) {
  const memY = 210; // Horizon where membrane is positioned
  const memHeight = 36;

  // Intermembrane Space Top Tint (high proton concentration, acidic amber/rose)
  const gradTop = ctx.createLinearGradient(0, 0, 0, memY);
  gradTop.addColorStop(0, "rgba(45, 12, 16, 0.85)");
  gradTop.addColorStop(1, "rgba(80, 20, 30, 0.70)");
  ctx.fillStyle = gradTop;
  ctx.fillRect(0, 0, PW, memY);

  // Matrix Bottom Tint (alkaline, ATP production chamber, deep high-tech bio violet)
  const gradBot = ctx.createLinearGradient(0, memY + memHeight, 0, PH);
  gradBot.addColorStop(0, "rgba(10, 16, 35, 0.85)");
  gradBot.addColorStop(1, "rgba(5, 8, 20, 0.95)");
  ctx.fillStyle = gradBot;
  ctx.fillRect(0, memY + memHeight, PW, PH - (memY + memHeight));

  // Membrane Core (hydrophobic interior, golden brown)
  pRect(ctx, 0, memY + 6, PW, memHeight - 12, "#3E2723");

  // Phospholipid Polar Heads - Top Layer (facing Intermembrane Space)
  for (let x = 0; x < PW; x += 6) {
    if (x > 120 && x < 240) continue; // Gap for ATP Synthase
    const wobble = Math.sin(x * 0.15 + frame * 0.08) * 1.5;
    pCircle(ctx, x + 3, memY + 4 + wobble, 3, "#FFB74D", 1);
    pCircle(ctx, x + 3, memY + 4 + wobble, 1, "#FFE082", 1);
    pRect(ctx, x + 2, memY + 8 + wobble, 1, 8, "#FFA000");
    pRect(ctx, x + 4, memY + 8 + wobble, 1, 9, "#FF8F00");
  }

  // Phospholipid Polar Heads - Bottom Layer (facing Matrix)
  for (let x = 0; x < PW; x += 6) {
    if (x > 120 && x < 240) continue;
    const wobble = Math.cos(x * 0.15 + frame * 0.08) * 1.5;
    pCircle(ctx, x + 3, memY + memHeight - 4 + wobble, 3, "#FFB74D", 1);
    pCircle(ctx, x + 3, memY + memHeight - 4 + wobble, 1, "#FFE082", 1);
    pRect(ctx, x + 2, memY + memHeight - 16 + wobble, 1, 8, "#FFA000");
    pRect(ctx, x + 4, memY + memHeight - 17 + wobble, 1, 9, "#FF8F00");
  }

  // Gradient Voltage Indicator
  pRect(ctx, 6, memY - 24, 84, 16, "rgba(0,0,0,0.8)");
  ctx.strokeStyle = "#FF5252";
  ctx.strokeRect(6, memY - 24, 84, 16);
  ctx.fillStyle = "#FF8A80";
  ctx.font = "8px monospace";
  ctx.fillText("IMS: [H+] HIGH", 10, memY - 13);

  pRect(ctx, 6, memY + memHeight + 10, 92, 16, "rgba(0,0,0,0.8)");
  ctx.strokeStyle = "#5CE1E6";
  ctx.strokeRect(6, memY + memHeight + 10, 92, 16);
  ctx.fillStyle = "#5CE1E6";
  ctx.font = "8px monospace";
  ctx.fillText("MATRIX: [H+] LOW", 10, memY + memHeight + 21);
}

// 3. ATP Synthase Nanomotor (F0 Base, Rotor Ring, Central Stalk, Stator Bracket, F1 Catalytic Head)
export function drawAtpSynthase(ctx: CanvasRenderingContext2D, frame: number) {
  const cx = 180;
  const memY = 210;

  // Rotation angle: smooth continuous 9,000 RPM simulation
  const rotAngle = (frame * 0.28) % (Math.PI * 2);

  // A. Subunit 'a' (Stator Base in membrane, left side of rotor)
  pRect(ctx, cx - 52, memY - 4, 26, 44, "#00838F");
  pRect(ctx, cx - 50, memY - 2, 22, 40, "#00ACC1");
  pRect(ctx, cx - 46, memY + 4, 3, 28, "#26C6DA");
  pRect(ctx, cx - 38, memY + 4, 3, 28, "#80DEEA");

  // Proton input half-channel (top slot)
  pRect(ctx, cx - 36, memY - 2, 8, 14, "#004D40");
  // Proton exit half-channel (bottom slot)
  pRect(ctx, cx - 36, memY + 24, 8, 16, "#004D40");

  // B. Subunit 'c-ring' Rotor (In membrane, cx-24 to cx+24)
  const rotorRadius = 24;
  const numBarrels = 10;

  pRect(ctx, cx - 26, memY + 2, 52, 32, "#37474F");

  // Rotating vertical alpha-helix cylinders
  for (let i = 0; i < numBarrels; i++) {
    const angle = rotAngle + (i * Math.PI * 2) / numBarrels;
    const xPos = cx + Math.sin(angle) * rotorRadius;
    const zDepth = Math.cos(angle);

    if (zDepth > -0.2) {
      const width = Math.max(3, Math.round(5 * (zDepth * 0.4 + 0.8)));
      const height = 30;
      const yPos = memY + 3;

      const hasProton = Math.sin(angle) > -0.5 && Math.sin(angle) < 0.6;
      let col = zDepth > 0.4 ? "#4DD0E1" : "#0097A7";
      if (hasProton) {
        col = zDepth > 0.4 ? "#76FF03" : "#64DD17";
      }

      pRect(ctx, xPos - width / 2, yPos, width, height, col);
      if (zDepth > 0.5) {
        pRect(ctx, xPos - width / 2 + 1, yPos + 2, 1, height - 4, "#FFFFFF");
      }
      pCircle(ctx, xPos, yPos + 15, hasProton ? 2 : 1, hasProton ? "#FFFF00" : "#006064", 1);
    }
  }

  // C. Peripheral Stator Arm (Anchored to subunit 'a', holding F1 head still)
  pRect(ctx, cx - 58, memY + 38, 10, 110, "#455A64");
  pRect(ctx, cx - 56, memY + 40, 6, 106, "#78909C");
  for (let ry = memY + 46; ry < memY + 140; ry += 18) {
    pCircle(ctx, cx - 53, ry, 2, "#CFD8DC", 1);
  }
  pRect(ctx, cx - 52, memY + 140, 26, 12, "#546E7A");
  pRect(ctx, cx - 50, memY + 142, 22, 8, "#90A4AE");

  // OSCP top cap
  pRect(ctx, cx - 18, memY + 70, 36, 10, "#B0BEC5");
  pRect(ctx, cx - 14, memY + 72, 28, 6, "#ECEFF1");

  // D. Central Stalk (Gamma & Epsilon shaft)
  const camWobble = Math.sin(rotAngle) * 5;
  const shaftX = cx + camWobble;

  pRect(ctx, shaftX - 6, memY + 35, 12, 45, "#FFB300");
  pRect(ctx, shaftX - 4, memY + 37, 8, 41, "#FFE082");
  for (let sy = memY + 40; sy < memY + 75; sy += 8) {
    const sw = Math.sin(rotAngle + sy * 0.2) * 4;
    pRect(ctx, shaftX + sw - 2, sy, 4, 3, "#FF6F00");
  }
  pRect(ctx, shaftX - 5, memY + 80, 10, 70, "#FFA000");

  // E. F1 Catalytic Head (Alpha3 / Beta3 Hexamer)
  const f1Y = memY + 120;
  const f1Radius = 36;
  const numSubunits = 6;

  for (let s = 0; s < numSubunits; s++) {
    const subAngle = (s * Math.PI * 2) / numSubunits;
    const subX = cx + Math.cos(subAngle) * f1Radius;
    const subY = f1Y + Math.sin(subAngle) * (f1Radius * 0.7);

    const isBeta = s % 2 === 0;
    const camDist = Math.hypot(subX - shaftX, subY - (memY + 115));
    const isCompressed = camDist < 34;

    const baseCol = isBeta
      ? isCompressed
        ? "#E040FB"
        : "#7C4DFF"
      : isCompressed
      ? "#536DFE"
      : "#3D5AFE";

    const lightCol = isBeta
      ? isCompressed
        ? "#EA80FC"
        : "#B388FF"
      : isCompressed
      ? "#8C9EFF"
      : "#82B1FF";

    const subSize = isCompressed ? 17 : 19;
    pCircle(ctx, subX, subY, subSize, baseCol, 2);
    pCircle(ctx, subX - 3, subY - 3, Math.round(subSize * 0.6), lightCol, 2);
    pCircle(ctx, subX - 5, subY - 5, 3, "#FFFFFF", 1);

    if (isBeta && isCompressed) {
      const spark = Math.sin(frame * 0.5 + s) > 0;
      if (spark) {
        pCircle(ctx, subX, subY, 6, "#FFFF00", 1);
        pCircle(ctx, subX, subY, 3, "#FFFFFF", 1);
        pRect(ctx, subX + 7, subY - 4, 3, 2, "#FFD700");
        pRect(ctx, subX - 8, subY + 5, 2, 3, "#FFD700");
      }
    }
  }

  // Central cam head
  pCircle(ctx, shaftX, f1Y, 11, "#FF8F00", 2);
  pCircle(ctx, shaftX, f1Y, 7, "#FFE082", 2);
  pCircle(ctx, shaftX, f1Y, 3, "#FFFFFF", 1);
}

// 4. Dynamic Proton Stream (Flowing through stator into rotor and down into matrix)
export function drawProtonStream(ctx: CanvasRenderingContext2D, frame: number) {
  const cx = 180;
  const memY = 210;

  const numProtons = 36;
  for (let i = 0; i < numProtons; i++) {
    const seed = i * 433;
    const t = (frame * 0.025 + i / numProtons) % 1;
    let px = 0;
    let py = 0;

    if (t < 0.45) {
      const prog = t / 0.45;
      const startX = cx - 140 + (seed % 280);
      const startY = 40 + (seed % 140);
      px = startX + (cx - 36 - startX) * Math.pow(prog, 2);
      py = startY + (memY - 6 - startY) * Math.pow(prog, 1.5);
    } else if (t < 0.7) {
      const prog = (t - 0.45) / 0.25;
      const angle = (frame * 0.28) + prog * Math.PI;
      px = cx + Math.sin(angle) * 20;
      py = memY + 16 + Math.sin(prog * Math.PI) * 4;
    } else {
      const prog = (t - 0.7) / 0.3;
      px = cx - 36 - prog * (30 + (seed % 60));
      py = memY + 40 + prog * 100;
    }

    pCircle(ctx, px, py, 3, "#76FF03", 1);
    pCircle(ctx, px, py, 1, "#FFFFFF", 1);

    if (i % 3 === 0) {
      pRect(ctx, px - 1, py, 3, 1, "#004D40");
      pRect(ctx, px, py - 1, 1, 3, "#004D40");
    }
  }
}

// 5. ADP & Phosphate entering, ATP Batteries being forged and ejected!
export function drawAtpSynthesisEvents(ctx: CanvasRenderingContext2D, frame: number) {
  const cx = 180;
  const f1Y = 330;

  for (let i = 0; i < 4; i++) {
    const progress = ((frame * 0.02 + i * 0.25) % 1);
    const angle = (i * Math.PI * 2) / 3 + 0.4;

    if (progress < 0.35) {
      const p = progress / 0.35;
      const adpX = cx + 110 - p * 60;
      const adpY = f1Y + 90 - p * 70;
      const piX = cx + 80 - p * 40;
      const piY = f1Y + 120 - p * 90;

      pRect(ctx, adpX - 4, adpY - 3, 8, 6, "#0288D1");
      pRect(ctx, adpX - 2, adpY - 1, 4, 2, "#4FC3F7");
      pRect(ctx, adpX + 5, adpY - 3, 4, 6, "#FFB300");

      pCircle(ctx, piX, piY, 3, "#FF9100", 1);
      pCircle(ctx, piX, piY, 1, "#FFE082", 1);
    } else if (progress >= 0.5) {
      const p = (progress - 0.5) / 0.5;
      const shootAngle = angle + (i % 2 === 0 ? 0.3 : -0.3);
      const dist = 40 + Math.pow(p, 1.3) * 150;
      const atpX = cx + Math.cos(shootAngle) * dist;
      const atpY = f1Y + Math.sin(shootAngle) * dist * 0.75;

      if (atpY < PH - 30) {
        const pulse = Math.sin(frame * 0.4 + i) * 2;
        pCircle(ctx, atpX, atpY, 9 + pulse, "rgba(255, 238, 88, 0.35)", 2);
        pCircle(ctx, atpX, atpY, 6, "#FFD54F", 1);

        pRect(ctx, atpX - 8, atpY - 2, 4, 4, "#FF9100");
        pRect(ctx, atpX - 3, atpY - 2, 4, 4, "#FFB300");
        pRect(ctx, atpX + 2, atpY - 2, 4, 4, "#FFD700");

        pRect(ctx, atpX - 12, atpY - 12, 24, 8, "rgba(0,0,0,0.7)");
        ctx.fillStyle = "#FFEB3B";
        ctx.font = "6px monospace";
        ctx.fillText("ATP⚡", atpX - 9, atpY - 6);
      }
    }
  }
}

// 6. Scientific Cockpit Telemetry HUD (Positioned in Bottom Matrix Area for Zero Clutter!)
export function drawTachometerHud(ctx: CanvasRenderingContext2D, frame: number) {
  // Bottom Right Tachometer Dial
  const dialX = 295;
  const dialY = 450;
  const dialR = 26;

  // Background bezel
  pCircle(ctx, dialX, dialY, dialR + 3, "#37474F", 1);
  pCircle(ctx, dialX, dialY, dialR, "#080C16", 1);

  // Tick marks
  for (let a = 0; a < 8; a++) {
    const ang = -Math.PI * 0.8 + (a * Math.PI * 1.6) / 7;
    const tx = dialX + Math.cos(ang) * (dialR - 4);
    const ty = dialY + Math.sin(ang) * (dialR - 4);
    pRect(ctx, tx, ty, 2, 2, a >= 6 ? "#FF1744" : "#00E5FF");
  }

  // Spinning Needle (pinned near max redline ~9,000 RPM!)
  const needleJitter = Math.sin(frame * 0.8) * 0.08;
  const needleAng = Math.PI * 0.55 + needleJitter;
  const nx = dialX + Math.cos(needleAng) * (dialR - 6);
  const ny = dialY + Math.sin(needleAng) * (dialR - 6);

  ctx.strokeStyle = "#FF5252";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(dialX, dialY);
  ctx.lineTo(nx, ny);
  ctx.stroke();
  pCircle(ctx, dialX, dialY, 4, "#FFFFFF", 1);

  // Digital RPM Readout
  pRect(ctx, dialX - 35, dialY + 32, 70, 16, "rgba(8,12,24,0.92)");
  ctx.strokeStyle = "#FFD54F";
  ctx.strokeRect(dialX - 35, dialY + 32, 70, 16);
  ctx.fillStyle = "#FFEB3B";
  ctx.font = "8px monospace";
  ctx.fillText("9,000 RPM", dialX - 26, dialY + 43);

  // Bottom Left: Daily Output Counter (Accumulating ~70 KG)
  const kgProgress = Math.min(70.0, (frame / 960) * 70.0);
  pRect(ctx, 16, 436, 124, 30, "rgba(8,12,24,0.92)");
  ctx.strokeStyle = "#5CE1E6";
  ctx.strokeRect(16, 436, 124, 30);
  ctx.fillStyle = "#B2EBF2";
  ctx.font = "7px monospace";
  ctx.fillText("DAILY ATP RECYCLED:", 20, 448);
  ctx.fillStyle = "#5CE1E6";
  ctx.font = "11px monospace";
  ctx.fillText(`${kgProgress.toFixed(1)} KG / DAY`, 20, 461);

  // Molecular Chemical Synthesis Formula
  pRect(ctx, 50, 506, 260, 20, "rgba(8,12,24,0.85)");
  ctx.strokeStyle = "rgba(255,213,79,0.5)";
  ctx.strokeRect(50, 506, 260, 20);
  ctx.fillStyle = "#FFD54F";
  ctx.font = "8px monospace";
  ctx.fillText("ADP + Pi + H+  ➔  ATP + H2O", 78, 519);
}

// 7. Subtle Vignette & Scanline Overlay
export function drawVignetteAndScanlines(ctx: CanvasRenderingContext2D) {
  // Vignette
  const grad = ctx.createRadialGradient(
    PW / 2,
    PH / 2,
    140,
    PW / 2,
    PH / 2,
    330
  );
  grad.addColorStop(0, "rgba(0,0,0,0)");
  grad.addColorStop(1, "rgba(0,0,0,0.65)");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, PW, PH);

  // Scanlines
  ctx.fillStyle = "rgba(0, 0, 0, 0.12)";
  for (let y = 0; y < PH; y += 4) {
    ctx.fillRect(0, y, PW, 1);
  }
}
