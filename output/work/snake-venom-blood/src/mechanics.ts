import { rect, circle, drawText, ART_WIDTH } from "./pixel";
import { PALETTE } from "./palette";

/**
 * Top Medical Diagnostic HUD / Telemetry Box
 * y: 10 to 65
 */
export function drawMedicalHUD(
  ctx: CanvasRenderingContext2D,
  title: string,
  rows: string[],
  alert: boolean = false
) {
  const boxX = 10;
  const boxY = 12;
  const boxW = ART_WIDTH - 20;
  const boxH = 46;

  rect(ctx, boxX, boxY, boxW, boxH, "rgba(10, 14, 24, 0.92)");
  const borderColor = alert ? PALETTE.hazardRed : PALETTE.hudGreen;
  rect(ctx, boxX, boxY, boxW, 1, borderColor);
  rect(ctx, boxX, boxY + boxH - 1, boxW, 1, borderColor);
  rect(ctx, boxX, boxY, 1, boxH, borderColor);
  rect(ctx, boxX + boxW - 1, boxY, 1, boxH, borderColor);

  // Blinking alert dot
  if (alert) {
    circle(ctx, boxX + 8, boxY + 8, 3, PALETTE.hazardRed);
  } else {
    circle(ctx, boxX + 8, boxY + 8, 3, PALETTE.hudGreen);
  }

  // Header Title
  drawText(ctx, title, boxX + 16, boxY + 5, 1, alert ? PALETTE.hazardRed : PALETTE.synapseCyan);

  // Rows of telemetry
  rows.forEach((r, idx) => {
    drawText(ctx, r, boxX + 10, boxY + 17 + idx * 9, 1, "#e9ecef");
  });
}

/**
 * Scene 1 & 2: Fang Puncture & Hypodermic Injection into Skin & Capillaries
 * Epidermis, Dermis, Subcutaneous layers, venom bolus diffusing into vessel.
 * Strict bounds: y <= 255 (y range: 70 - 250)
 */
export function drawFangSkinInjection(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  depthProgress: number // 0 to 1
) {
  const topY = cy - 30; // ~ 100
  const fDepth = Math.floor(depthProgress * 42);

  // 1. Stratified Skin Anatomy Layers
  // Epidermis (outer protective stratum corneum)
  rect(ctx, 16, topY + 10, ART_WIDTH - 32, 10, "#e9a17c");
  rect(ctx, 16, topY + 10, ART_WIDTH - 32, 2, "#d08b65"); // stratum corneum outer keratin
  drawText(ctx, "EPIDERMIS", 20, topY + 12, 1, "#495057");

  // Dermis (dense connective tissue with nerve fibers)
  rect(ctx, 16, topY + 20, ART_WIDTH - 32, 38, "#c47a5a");
  // Collagen matrix fibers
  for (let fx = 24; fx < ART_WIDTH - 40; fx += 16) {
    rect(ctx, fx, topY + 24 + ((fx * 7) % 24), 10, 1, "rgba(255, 255, 255, 0.2)");
  }
  drawText(ctx, "DERMIS (VASCULAR)", 20, topY + 23, 1, "#ffd8a8");

  // Subcutaneous Adipose Tissue (yellow lipid fat globules)
  rect(ctx, 16, topY + 58, ART_WIDTH - 32, 62, "#4a3528");
  for (let ax = 22; ax < ART_WIDTH - 30; ax += 14) {
    for (let ay = topY + 62; ay < topY + 116; ay += 12) {
      circle(ctx, ax + ((ay % 7) * 2), ay, 4, "#ffd43b");
      circle(ctx, ax + ((ay % 7) * 2), ay, 2, "#fab005");
    }
  }
  drawText(ctx, "SUBCUTANEOUS TISSUE", 20, topY + 61, 1, "#ffe066");

  // Deep Capillary / Micro-vessel
  const vesselY = topY + 84;
  rect(ctx, 16, vesselY, ART_WIDTH - 32, 18, PALETTE.endothelialDark);
  rect(ctx, 16, vesselY + 2, ART_WIDTH - 32, 14, PALETTE.cellCrimson);
  // Red blood cells streaming through vessel
  for (let bx = 20; bx < ART_WIDTH - 30; bx += 18) {
    const driftX = (bx + frame * 1.5) % (ART_WIDTH - 36) + 18;
    circle(ctx, driftX, vesselY + 9, 3, PALETTE.arteryRed);
  }
  drawText(ctx, "VENOUS CAPILLARY", 22, vesselY + 5, 1, "#ffffff");

  // 2. Twin Hollow Snake Fangs Piercing Down
  const fangLeftX = cx - 22;
  const fangRightX = cx + 18;
  const fY = topY - 14 + fDepth;

  [fangLeftX, fangRightX].forEach((fx) => {
    // Curved enamel fang body
    for (let d = 0; d < 36; d++) {
      const curX = fx + Math.floor((d * d) / 70);
      const curY = fY - 36 + d;
      if (curY <= topY + 10 + fDepth) {
        rect(ctx, curX, curY, 4, 1, "#f8f9fa");
        rect(ctx, curX + 1, curY, 2, 1, "#e9ecef");
      }
    }
    // Fang tip
    const tipX = fx + Math.floor((36 * 36) / 70);
    const tipY = fY;
    circle(ctx, tipX + 1, tipY, 2, "#ffffff");

    // Venom squirt emerging from hollow fang canal
    if (depthProgress > 0.4) {
      const vProgress = (frame * 3) % 40;
      for (let v = 0; v < 12; v++) {
        const vx = tipX + (Math.sin(v * 1.7 + frame * 0.2) * (v * 1.8));
        const vy = tipY + 4 + v * 2.5;
        if (vy < topY + 118) {
          circle(ctx, vx, vy, 2, PALETTE.venomToxicLime);
          circle(ctx, vx, vy, 1, PALETTE.venomGreen);
        }
      }
    }
  });

  // Venom diffusion cloud in subcutaneous tissue & entering capillary
  if (depthProgress > 0.6) {
    const diffR = Math.min(32, 10 + (frame % 30));
    circle(ctx, cx, vesselY + 8, diffR, "rgba(81, 207, 102, 0.35)");
    circle(ctx, cx - 12, vesselY + 9, Math.floor(diffR * 0.7), "rgba(148, 216, 45, 0.4)");
  }
}

/**
 * Scene 2 & 3: Microscopic Bloodstream Cross-Section
 * Biconcave erythrocytes, blood plasma, endothelial wall, invading venom enzymes.
 * Strict bounds: y <= 255 (y range: 70 - 245)
 */
export function drawMicroscopicBloodstream(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  venomDensity: number = 0.5 // 0 to 1
) {
  const wallTopY = cy - 45; // ~ 95
  const lumenH = 95;
  const wallBotY = wallTopY + lumenH; // ~ 190

  // 1. Vessel Endothelial Walls (top and bottom)
  // Top Endothelial Cells
  rect(ctx, 10, wallTopY - 14, ART_WIDTH - 20, 14, PALETTE.endothelialDark);
  for (let ex = 12; ex < ART_WIDTH - 22; ex += 22) {
    rect(ctx, ex, wallTopY - 12, 20, 11, PALETTE.endothelialPink);
    circle(ctx, ex + 10, wallTopY - 6, 2, "#a61e4d"); // nucleus
  }
  rect(ctx, 10, wallTopY, ART_WIDTH - 20, 2, "#ffdeeb"); // basement membrane

  // Bottom Endothelial Cells
  rect(ctx, 10, wallBotY + 2, ART_WIDTH - 20, 14, PALETTE.endothelialDark);
  for (let ex = 14; ex < ART_WIDTH - 22; ex += 22) {
    rect(ctx, ex, wallBotY + 3, 20, 11, PALETTE.endothelialPink);
    circle(ctx, ex + 10, wallBotY + 8, 2, "#a61e4d"); // nucleus
  }
  rect(ctx, 10, wallBotY, ART_WIDTH - 20, 2, "#ffdeeb");

  // 2. Blood Lumen (Fluid Blood Plasma)
  rect(ctx, 10, wallTopY + 2, ART_WIDTH - 20, lumenH - 2, PALETTE.bloodDark);

  // Flow velocity
  const flowSpeed = 2.4;

  // 3. 3D Biconcave Red Blood Cells (Erythrocytes)
  const cellPositions = [
    { x: 30, y: wallTopY + 22, r: 8, angle: 0.2 },
    { x: 75, y: wallTopY + 45, r: 9, angle: 0.6 },
    { x: 120, y: wallTopY + 28, r: 8, angle: -0.4 },
    { x: 165, y: wallTopY + 65, r: 9, angle: 0.1 },
    { x: 210, y: wallTopY + 38, r: 8, angle: 0.7 },
    { x: 50, y: wallTopY + 70, r: 8, angle: -0.2 },
    { x: 100, y: wallTopY + 78, r: 9, angle: 0.5 },
    { x: 145, y: wallTopY + 48, r: 8, angle: -0.6 },
    { x: 190, y: wallTopY + 74, r: 8, angle: 0.3 }
  ];

  cellPositions.forEach((cp, idx) => {
    const curX = ((cp.x + frame * flowSpeed + idx * 8) % (ART_WIDTH - 30)) + 15;
    const curY = cp.y + Math.sin(frame * 0.1 + idx) * 3;

    // Draw biconcave erythrocyte (doughnut-shaped dimple in 3D pixel art)
    circle(ctx, curX, curY, cp.r, PALETTE.arteryRed);
    circle(ctx, curX + 1, curY - 1, cp.r - 2, PALETTE.cellCrimson);
    circle(ctx, curX, curY, cp.r - 4, PALETTE.cellShade); // center biconcave depression
  });

  // 4. Venom Enzyme Nanoparticles Invading & Attaching
  const numEnzymes = Math.floor(venomDensity * 24);
  for (let i = 0; i < numEnzymes; i++) {
    const ex = ((i * 37 + frame * 3.2) % (ART_WIDTH - 40)) + 20;
    const ey = wallTopY + 12 + ((i * 23 + frame) % (lumenH - 24));

    // Spiked toxic enzyme complex (Snake Venoms Metalloproteinase / PLA2)
    circle(ctx, ex, ey, 3, PALETTE.venomToxicLime);
    circle(ctx, ex, ey, 1, "#ffffff");
    // Toxic enzyme spikes
    rect(ctx, ex - 4, ey, 8, 1, PALETTE.venomGreen);
    rect(ctx, ex, ey - 4, 1, 8, PALETTE.venomGreen);
  }

  // Label indicators
  drawText(ctx, "ERYTHROCYTES (RBC)", 14, wallTopY + 6, 1, PALETTE.plasmaYellow);
  drawText(ctx, "TOXIC ENZYME CASCADE", 110, wallBotY - 10, 1, PALETTE.venomToxicLime);
}

/**
 * Scene 3: Hemotoxic Clotting Cascade - Blood Turning to Solid Gelatinous Jelly!
 * Fibrin strands weaving a deadly mesh, erythrocytes trapped, vessel choking.
 * Strict bounds: y <= 255 (y range: 70 - 245)
 */
export function drawClottingCascade(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  clotProgress: number // 0 to 1
) {
  const boxX = 14;
  const boxY = cy - 40; // ~ 100
  const boxW = ART_WIDTH - 28;
  const boxH = 92;

  // Artery vessel wall
  rect(ctx, boxX, boxY, boxW, boxH, PALETTE.bloodDark);
  rect(ctx, boxX, boxY, boxW, 4, PALETTE.endothelialDark);
  rect(ctx, boxX, boxY + boxH - 4, boxW, 4, PALETTE.endothelialDark);

  // Progressive Fibrin mesh growth across center
  const meshW = Math.floor(clotProgress * (boxW - 40));
  const meshX = cx - meshW / 2;

  // Solidified dark gelatinous jelly core
  if (clotProgress > 0.3) {
    const jellyW = Math.floor((clotProgress - 0.2) * (boxW - 60));
    rect(ctx, cx - jellyW / 2, boxY + 12, jellyW, boxH - 24, "#40080d");
    rect(ctx, cx - jellyW / 2 + 4, boxY + 16, jellyW - 8, boxH - 32, "#2b0307");
    // Trapped dark deoxygenated RBCs in jelly
    for (let rbx = cx - jellyW / 2 + 8; rbx < cx + jellyW / 2 - 8; rbx += 12) {
      for (let rby = boxY + 22; rby < boxY + boxH - 22; rby += 10) {
        circle(ctx, rbx + ((rby % 3) * 2), rby, 3, PALETTE.cellShade);
      }
    }
  }

  // Intertwined Fibrin Fibers (White sticky spiderweb protein polymer)
  const strandCount = Math.floor(clotProgress * 28);
  for (let s = 0; s < strandCount; s++) {
    const sx = meshX + ((s * 17) % Math.max(10, meshW));
    const sy = boxY + 8 + ((s * 13) % (boxH - 16));
    const len = 16 + (s % 12);
    // Angular criss-cross fibrin polymer strands
    for (let p = 0; p < len; p++) {
      const px = sx + p;
      const py = sy + Math.floor(Math.sin(p * 0.5 + s) * 5);
      if (py > boxY + 5 && py < boxY + boxH - 5) {
        rect(ctx, px, py, 1, 1, PALETTE.fibrinWhite);
      }
    }
  }

  // Vessel blockage indicator & pressure buildup arrows
  if (clotProgress > 0.6) {
    // Pulsing blood damming up on left
    const damX = cx - meshW / 2 - 12;
    rect(ctx, damX - 8, boxY + 8, 8, boxH - 16, PALETTE.arteryRed);
    // Pressure arrows
    drawText(ctx, ">>> 220 mmHg >>>", 18, boxY + 8, 1, PALETTE.hazardRed);
    drawText(ctx, "MASSIVE THROMBUS", cx - 44, boxY + boxH - 12, 1, PALETTE.hazardRed);
  } else {
    drawText(ctx, "FIBRINOGEN -> FIBRIN MESH", 20, boxY + 8, 1, PALETTE.fibrinWhite);
  }
}

/**
 * Scene 4: Neurotoxin Synaptic Blockade
 * Motor neuron axon terminal, synaptic vesicles, synaptic cleft,
 * and purple neurotoxins blocking acetylcholine receptors (signal flatlines).
 * Strict bounds: y <= 255 (y range: 70 - 250)
 */
export function drawNeuromuscularSynapse(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  toxinBlock: number // 0 to 1
) {
  const topY = cy - 35; // ~ 105

  // 1. Presynaptic Axon Terminal (upper motor nerve bulb)
  rect(ctx, cx - 40, topY - 15, 80, 24, PALETTE.synapseDark);
  rect(ctx, cx - 36, topY - 12, 72, 20, "#1098ad");
  rect(ctx, cx - 36, topY + 7, 72, 3, PALETTE.synapseCyan); // presynaptic membrane
  drawText(ctx, "PRESYNAPTIC MOTOR AXON", cx - 58, topY - 22, 1, PALETTE.synapseCyan);

  // Acetylcholine synaptic vesicles (tiny blue spheres releasing transmitter)
  for (let v = 0; v < 8; v++) {
    const vx = cx - 28 + (v % 4) * 16;
    const vy = topY - 5 + Math.floor(v / 4) * 8;
    circle(ctx, vx, vy, 3, "#e3fafc");
    circle(ctx, vx, vy, 1, PALETTE.synapseCyan);
  }

  // 2. Synaptic Cleft (20nm gap)
  const cleftY = topY + 10;
  rect(ctx, cx - 45, cleftY, 90, 16, "#0b0c10");

  // Released Acetylcholine molecules (green dots traveling down)
  for (let a = 0; a < 6; a++) {
    const ax = cx - 25 + a * 10;
    const ay = cleftY + 3 + ((frame * 2 + a * 3) % 11);
    circle(ctx, ax, ay, 1, "#40c057");
  }

  // 3. Postsynaptic Muscle Membrane & Nicotinic Receptors
  const postY = cleftY + 16;
  rect(ctx, cx - 45, postY, 90, 26, "#862e9c"); // muscle fiber endplate
  rect(ctx, cx - 45, postY, 90, 3, "#cc5de8"); // postsynaptic membrane
  drawText(ctx, "MUSCLE MOTOR ENDPLATE", cx - 55, postY + 18, 1, "#f3d9fa");

  // Receptor channels on postsynaptic membrane
  for (let r = 0; r < 5; r++) {
    const rx = cx - 32 + r * 15;
    // Receptor protein channel (U-shaped pocket)
    rect(ctx, rx, postY - 2, 8, 4, "#ffd43b");
    rect(ctx, rx + 2, postY - 2, 4, 2, "#0b0c10"); // ion channel pore

    // Purple Neurotoxin molecules (e.g. Cobratoxin / Alpha-bungarotoxin)
    if (r < Math.floor(toxinBlock * 5) + 1) {
      // Neurotoxin locked tight into receptor pocket!
      circle(ctx, rx + 4, postY - 3, 3, PALETTE.neurotoxinPurple);
      circle(ctx, rx + 4, postY - 3, 1, "#ffffff");
      // Receptor blocked spark
      rect(ctx, rx + 2, postY - 6, 4, 1, PALETTE.hazardRed);
    }
  }

  // 4. Action Potential Telemetry Monitor (bottom)
  const oscY = postY + 32;
  rect(ctx, 16, oscY, ART_WIDTH - 32, 24, "rgba(5, 10, 18, 0.95)");
  rect(ctx, 16, oscY, ART_WIDTH - 32, 1, PALETTE.synapseCyan);
  rect(ctx, 16, oscY + 23, ART_WIDTH - 32, 1, PALETTE.synapseCyan);

  // Electrical waveform
  drawText(ctx, "ACTION POTENTIAL: ", 20, oscY + 3, 1, "#adb5bd");
  if (toxinBlock > 0.5) {
    drawText(ctx, "FLATLINE (0 mV) - SIGNAL BLOCKED", 110, oscY + 3, 1, PALETTE.hazardRed);
    // Flat red line
    rect(ctx, 20, oscY + 16, ART_WIDTH - 40, 2, PALETTE.hazardRed);
  } else {
    drawText(ctx, "+40 mV ACTIVE", 120, oscY + 3, 1, PALETTE.hudGreen);
    // Active spike waveform
    for (let wx = 20; wx < ART_WIDTH - 20; wx += 2) {
      const spike = Math.sin((wx - frame * 4) * 0.2) > 0.7 ? -6 : 0;
      rect(ctx, wx, oscY + 16 + spike, 2, 1, PALETTE.hudGreen);
    }
  }
}

/**
 * Scene 5: Diaphragm & Respiratory Paralysis
 * Thoracic ribcage cutaway, left & right lungs, dome-shaped diaphragm muscle,
 * SpO2 oxygen telemetry collapsing.
 * Strict bounds: y <= 255 (y range: 70 - 250)
 */
export function drawDiaphragmRespiration(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  paralysisLevel: number // 0 (breathing) to 1 (paralyzed)
) {
  const topY = cy - 35; // ~ 105
  // When paralyzed, diaphragm cannot contract downward
  const breathCycle = (1 - paralysisLevel) * Math.sin(frame * 0.15) * 5;

  // Thoracic Cavity Background
  rect(ctx, cx - 55, topY - 10, 110, 92, "#180608");
  rect(ctx, cx - 55, topY - 10, 110, 1, "#495057");

  // Bilateral Ribcage Bones (left & right ribs protecting lungs)
  for (let r = 0; r < 5; r++) {
    const ry = topY + r * 14;
    // Left rib
    rect(ctx, cx - 52, ry, 24, 4, "#e9ecef");
    rect(ctx, cx - 50, ry + 1, 22, 2, "#ced4da");
    // Right rib
    rect(ctx, cx + 28, ry, 24, 4, "#e9ecef");
    rect(ctx, cx + 28, ry + 1, 22, 2, "#ced4da");
  }

  // Central Trachea & Bronchi
  rect(ctx, cx - 3, topY - 14, 6, 20, "#adb5bd");
  rect(ctx, cx - 12, topY + 6, 10, 3, "#868e96"); // left bronchus
  rect(ctx, cx + 2, topY + 6, 10, 3, "#868e96"); // right bronchus

  // Left & Right Lungs (spongy alveolar tissue)
  const lungColor = paralysisLevel > 0.6 ? "#495057" : (paralysisLevel > 0.3 ? "#771212" : "#f783ac");
  // Left lung
  rect(ctx, cx - 40, topY + 10, 26, 42, lungColor);
  circle(ctx, cx - 27, topY + 12, 11, lungColor);
  circle(ctx, cx - 27, topY + 48, 12, lungColor);
  // Right lung
  rect(ctx, cx + 14, topY + 10, 26, 42, lungColor);
  circle(ctx, cx + 27, topY + 12, 11, lungColor);
  circle(ctx, cx + 27, topY + 48, 12, lungColor);

  // Dome-shaped Diaphragm Muscle Below Lungs
  const diaY = topY + 64 + breathCycle;
  rect(ctx, cx - 52, diaY, 104, 8, "#c92a2a");
  // Upward dome curvature
  circle(ctx, cx, diaY - 4, 30, "#c92a2a");
  rect(ctx, cx - 52, diaY + 6, 104, 4, "#771212"); // tendon line
  drawText(ctx, "DIAPHRAGM MUSCLE", cx - 42, diaY + 12, 1, "#ffc9c9");

  // Asphyxiation / Hypoxia Telemetry Display (Bottom)
  const hudY = topY + 86;
  rect(ctx, 14, hudY, ART_WIDTH - 28, 24, "rgba(5, 8, 18, 0.95)");
  rect(ctx, 14, hudY, ART_WIDTH - 28, 1, paralysisLevel > 0.5 ? PALETTE.hazardRed : PALETTE.hudGreen);
  rect(ctx, 14, hudY + 23, ART_WIDTH - 28, 1, paralysisLevel > 0.5 ? PALETTE.hazardRed : PALETTE.hudGreen);

  const spo2 = Math.max(42, Math.floor(98 - paralysisLevel * 56));
  drawText(ctx, `PULSE OXIMETER: SpO2 ${spo2}%`, 20, hudY + 4, 1, spo2 < 85 ? PALETTE.hazardRed : PALETTE.hudGreen);
  drawText(ctx, paralysisLevel > 0.5 ? "RESPIRATORY ARREST (APNEA)" : "SPONTANEOUS VENTILATION", 20, hudY + 13, 1, paralysisLevel > 0.5 ? PALETTE.hazardRed : "#ced4da");
}

/**
 * Scene 6: Cytotoxin Lysis & Cellular Necrosis
 * Phospholipase A2 enzymes disintegrating cellular lipid bilayer,
 * cell rupture, necrotic tissue destruction.
 * Strict bounds: y <= 255 (y range: 70 - 245)
 */
export function drawCytotoxinLysis(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  lysisProgress: number // 0 to 1
) {
  const boxX = 14;
  const boxY = cy - 38; // ~ 102
  const boxW = ART_WIDTH - 28;
  const boxH = 90;

  rect(ctx, boxX, boxY, boxW, boxH, "#1a1110");
  rect(ctx, boxX, boxY, boxW, 1, "#862e9c");
  rect(ctx, boxX, boxY + boxH - 1, boxW, 1, "#862e9c");

  // Lipid Bilayer Cell Membrane Cross-Section
  const memY = boxY + 42;
  drawText(ctx, "PHOSPHOLIPID BILAYER MEMBRANE", 18, boxY + 5, 1, "#e599f7");

  // Hydrophilic heads and hydrophobic tails
  for (let lx = boxX + 6; lx < boxX + boxW - 6; lx += 6) {
    const sheared = (lx > cx - 35 && lx < cx + 35) && (lysisProgress > 0.3);

    if (!sheared) {
      // Intact top layer
      circle(ctx, lx, memY - 6, 2, "#9775fa");
      rect(ctx, lx, memY - 4, 1, 4, "#ffd43b");
      // Intact bottom layer
      rect(ctx, lx, memY + 1, 1, 4, "#ffd43b");
      circle(ctx, lx, memY + 6, 2, "#9775fa");
    } else {
      // Ruptured / Disintegrated by Cytotoxins
      const floatY = Math.sin(frame * 0.2 + lx) * 8;
      circle(ctx, lx + Math.floor(floatY * 0.5), memY - 10 + floatY, 1, PALETTE.venomToxicLime);
      circle(ctx, lx, memY + 12 - floatY, 1, "#f03e3e");
    }
  }

  // Cytotoxin / Phospholipase A2 molecules cutting membrane
  for (let c = 0; c < 5; c++) {
    const cytX = cx - 25 + c * 13;
    const cytY = memY - 1 + Math.sin(frame * 0.25 + c) * 3;
    circle(ctx, cytX, cytY, 3, PALETTE.venomToxicLime);
    circle(ctx, cytX, cytY, 1, "#ffffff");
  }

  // Cellular Organelles & Cytoplasm Leaking Out
  if (lysisProgress > 0.4) {
    drawText(ctx, "CELLULAR LYSIS & NECROSIS", cx - 60, boxY + boxH - 14, 1, PALETTE.hazardRed);
    // Leaking debris
    for (let d = 0; d < 8; d++) {
      const dx = cx - 20 + ((d * 9) % 40);
      const dy = memY + 14 + ((d * 5) % 18);
      rect(ctx, dx, dy, 2, 2, "#fa5252");
    }
  }
}

/**
 * Scene 7: Antivenom Neutralization (Antibodies Binding Venom)
 * Y-shaped Fab antibody fragments locking onto venom active sites.
 * Strict bounds: y <= 255 (y range: 70 - 250)
 */
export function drawAntivenomAction(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  neutralizeProgress: number // 0 to 1
) {
  const boxX = 14;
  const boxY = cy - 35; // ~ 105
  const boxW = ART_WIDTH - 28;
  const boxH = 92;

  rect(ctx, boxX, boxY, boxW, boxH, "#09121a");
  rect(ctx, boxX, boxY, boxW, 1, PALETTE.synapseCyan);
  rect(ctx, boxX, boxY + boxH - 1, boxW, 1, PALETTE.synapseCyan);

  drawText(ctx, "ANTIVENOM IMMUNOGLOBULIN (Fab)", 18, boxY + 5, 1, PALETTE.antibodyGold);

  // 3 Target Venom Clusters
  const venomSites = [
    { x: cx - 45, y: boxY + 45 },
    { x: cx, y: boxY + 38 },
    { x: cx + 45, y: boxY + 48 }
  ];

  venomSites.forEach((site, idx) => {
    const isBound = idx < Math.floor(neutralizeProgress * 3) + 1;

    // Venom toxin molecule (green/purple)
    circle(ctx, site.x, site.y, 6, isBound ? "#495057" : PALETTE.venomToxicLime);
    circle(ctx, site.x, site.y, 3, isBound ? "#212529" : PALETTE.venomGreen);

    // Y-shaped Antibody Fragment flying toward or locked onto it
    const abDist = isBound ? 0 : Math.max(0, 30 - Math.floor(neutralizeProgress * 35));
    const abX = site.x;
    const abY = site.y - 12 - abDist;

    // Draw Y-shaped Antibody (Gold/Cyan)
    // Stem (Fc region)
    rect(ctx, abX - 1, abY - 8, 3, 8, PALETTE.antibodyGold);
    // Left Fab arm
    rect(ctx, abX - 6, abY - 14, 5, 3, PALETTE.synapseCyan);
    rect(ctx, abX - 8, abY - 18, 4, 4, PALETTE.antibodyGold);
    // Right Fab arm
    rect(ctx, abX + 2, abY - 14, 5, 3, PALETTE.synapseCyan);
    rect(ctx, abX + 5, abY - 18, 4, 4, PALETTE.antibodyGold);

    // Neutralization lock spark
    if (isBound) {
      circle(ctx, site.x, site.y - 7, 2, "#ffffff");
      circle(ctx, site.x, site.y - 7, 4, "rgba(255, 212, 59, 0.4)");
    }
  });

  // Telemetry status
  const neutralizedPct = Math.min(100, Math.floor(neutralizeProgress * 100));
  drawText(ctx, `TOXIN NEUTRALIZATION: ${neutralizedPct}%`, 18, boxY + boxH - 14, 1, PALETTE.hudGreen);
}

/**
 * Scene 8: Hospital Recovery & Vitals Normalization
 * Intensive care ECG telemetry waveform (P-QRS-T complex) pulsing at 74 BPM,
 * IV antivenom drip infusion.
 * Strict bounds: y <= 255 (y range: 70 - 250)
 */
export function drawHospitalRecovery(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number
) {
  const boxX = 14;
  const boxY = cy - 35; // ~ 105
  const boxW = ART_WIDTH - 28;
  const boxH = 92;

  rect(ctx, boxX, boxY, boxW, boxH, "rgba(5, 12, 20, 0.95)");
  rect(ctx, boxX, boxY, boxW, 1, PALETTE.hudGreen);
  rect(ctx, boxX, boxY + boxH - 1, boxW, 1, PALETTE.hudGreen);

  // Monitor Header
  drawText(ctx, "ICU TELEMETRY - NORMAL SINUS RHYTHM", 18, boxY + 5, 1, PALETTE.hudGreen);

  // Live ECG Heartbeat Line
  const ecgY = boxY + 36;
  // ECG Grid lines
  for (let gx = boxX + 4; gx < boxX + boxW - 4; gx += 16) {
    rect(ctx, gx, boxY + 16, 1, 40, "rgba(64, 192, 87, 0.15)");
  }
  for (let gy = boxY + 16; gy < boxY + 56; gy += 10) {
    rect(ctx, boxX + 4, gy, boxW - 8, 1, "rgba(64, 192, 87, 0.15)");
  }

  // Draw scrolling P-QRS-T electrocardiogram waveform
  for (let x = boxX + 4; x < boxX + boxW - 4; x += 2) {
    const phase = ((x + frame * 3) % 90);
    let dy = 0;
    if (phase > 20 && phase < 26) dy = -3; // P wave
    else if (phase >= 32 && phase < 35) dy = 2; // Q dip
    else if (phase >= 35 && phase < 39) dy = -16; // R peak!
    else if (phase >= 39 && phase < 42) dy = 6; // S trough
    else if (phase > 50 && phase < 62) dy = -5; // T wave

    rect(ctx, x, ecgY + dy, 2, 2, PALETTE.hudGreen);
  }

  // Medical Telemetry Metrics (bottom)
  const vitalsY = boxY + boxH - 24;
  rect(ctx, boxX + 4, vitalsY, boxW - 8, 20, "#081c15");
  drawText(ctx, "HR: 74 BPM", boxX + 10, vitalsY + 5, 1, PALETTE.hudGreen);
  drawText(ctx, "BP: 120/80", boxX + 75, vitalsY + 5, 1, "#ced4da");
  drawText(ctx, "SpO2: 99%", boxX + 140, vitalsY + 5, 1, PALETTE.synapseCyan);
}
