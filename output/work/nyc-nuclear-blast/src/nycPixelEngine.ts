/**
/**
 * High-Density Micro-Pixel NYC & Nuclear Blast Physics Engine (540x960 native space)
 * Renders fine 2px micro-pixel art for Manhattan skyline, blast physics, and cross-sections.
 */

export function px(ctx: CanvasRenderingContext2D, x: number, y: number, color: string) {
  ctx.fillStyle = color;
  ctx.fillRect(Math.floor(x), Math.floor(y), 1, 1);
}

/**
 * Draws the Iconic Manhattan Skyline in Micro-Pixels (Scene 1)
 */
export function drawManhattanSkyline(
  ctx: CanvasRenderingContext2D,
  frame: number,
  options: {
    fireballAlpha?: number;
    fireballRadius?: number;
    detonationY?: number;
    vaporizeRadius?: number;
  } = {}
) {
  const W = ctx.canvas.width;
  const H = ctx.canvas.height;
  const waterY = 740;

  // 1. Twilight / Cyber Night Sky
  const sky = ctx.createLinearGradient(0, 0, 0, waterY);
  sky.addColorStop(0, "#030712");
  sky.addColorStop(0.5, "#0b192c");
  sky.addColorStop(1, "#1e293b");
  ctx.fillStyle = sky;
  ctx.fillRect(0, 0, W, waterY);

  // 2. Stars and distant city glow
  for (let s = 0; s < 45; s++) {
    const sx = (s * 47) % W;
    const sy = (s * 31) % (waterY - 300);
    ctx.fillStyle = s % 3 === 0 ? "#94a3b8" : "#38bdf8";
    ctx.fillRect(sx, sy, 1, 1);
  }

  // 3. East River / Hudson River in micro-pixels
  const river = ctx.createLinearGradient(0, waterY, 0, H);
  river.addColorStop(0, "#0284c7");
  river.addColorStop(0.3, "#082f49");
  river.addColorStop(1, "#020617");
  ctx.fillStyle = river;
  ctx.fillRect(0, waterY, W, H - waterY);

  // Water reflections in micro-pixels
  for (let r = 0; r < 70; r++) {
    const rx = (r * 23 + frame * 0.4) % W;
    const ry = waterY + 6 + (r * 11) % 180;
    ctx.fillStyle = "rgba(56, 189, 248, 0.25)";
    ctx.fillRect(Math.floor(rx), Math.floor(ry), 8 + (r % 6) * 4, 1);
  }

  // 4. Iconic Manhattan Buildings
  // [x, width, height, type: 'wtc' | 'empire' | 'chrysler' | 'tower', baseColor, winColor]
  const buildings = [
    { x: 20, w: 32, h: 220, type: "tower", color: "#1e293b", win: "#38bdf8" },
    { x: 58, w: 42, h: 320, type: "tower", color: "#334155", win: "#facc15" },
    { x: 106, w: 48, h: 460, type: "wtc", color: "#1e293b", win: "#22d3ee" }, // One WTC
    { x: 160, w: 36, h: 280, type: "tower", color: "#334155", win: "#f8fafc" },
    { x: 202, w: 46, h: 390, type: "chrysler", color: "#475569", win: "#38bdf8" }, // Chrysler Building
    { x: 254, w: 52, h: 480, type: "empire", color: "#1e293b", win: "#facc15" }, // Empire State
    { x: 312, w: 40, h: 340, type: "tower", color: "#334155", win: "#38bdf8" },
    { x: 358, w: 44, h: 300, type: "tower", color: "#1e293b", win: "#f8fafc" },
    { x: 408, w: 38, h: 260, type: "tower", color: "#334155", win: "#facc15" },
    { x: 452, w: 34, h: 210, type: "tower", color: "#1e293b", win: "#38bdf8" },
    { x: 492, w: 36, h: 180, type: "tower", color: "#334155", win: "#f8fafc" }
  ];

  const detX = 270;
  const detY = options.detonationY || 350;
  const vapR = options.vaporizeRadius || 0;

  buildings.forEach(bld => {
    const topY = waterY - bld.h;

    // Check vaporization distance from Midtown detonation
    const dist = Math.hypot((bld.x + bld.w / 2) - detX, (waterY - bld.h / 2) - detY);
    if (vapR > 0 && dist < vapR) {
      // Disintegrated into plasma
      return;
    }

    ctx.fillStyle = bld.color;
    ctx.fillRect(bld.x, topY, bld.w, bld.h);

    // Spire detailing for landmarks
    if (bld.type === "wtc") {
      // Antenna spire
      ctx.fillStyle = "#94a3b8";
      ctx.fillRect(bld.x + bld.w / 2 - 2, topY - 50, 4, 50);
      // Red aviation beacon
      if (frame % 30 < 15) {
        ctx.fillStyle = "#ef4444";
        ctx.fillRect(bld.x + bld.w / 2 - 3, topY - 53, 6, 4);
      }
    } else if (bld.type === "empire") {
      // Art Deco stepped tiers and antenna
      ctx.fillStyle = "#475569";
      ctx.fillRect(bld.x + 8, topY - 30, bld.w - 16, 30);
      ctx.fillRect(bld.x + bld.w / 2 - 2, topY - 70, 4, 40);
      if (frame % 30 < 15) {
        ctx.fillStyle = "#ef4444";
        ctx.fillRect(bld.x + bld.w / 2 - 3, topY - 73, 6, 4);
      }
    } else if (bld.type === "chrysler") {
      // Stepped crown and needle
      ctx.fillStyle = "#cbd5e1";
      ctx.fillRect(bld.x + 6, topY - 20, bld.w - 12, 20);
      ctx.fillRect(bld.x + bld.w / 2 - 1, topY - 55, 2, 35);
    }

    // Windows in micro-pixels
    ctx.fillStyle = bld.win;
    for (let wy = topY + 12; wy < waterY - 8; wy += 18) {
      for (let wx = bld.x + 4; wx < bld.x + bld.w - 6; wx += 9) {
        if ((wx + wy) % 5 !== 0) {
          ctx.fillRect(wx, wy, 4, 6);
        }
      }
    }
  });

  // Brooklyn Bridge Suspension Cables across foreground
  ctx.save();
  ctx.strokeStyle = "rgba(148, 163, 184, 0.6)";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(0, waterY - 45);
  ctx.quadraticCurveTo(W * 0.25, waterY + 20, W * 0.5, waterY - 45);
  ctx.quadraticCurveTo(W * 0.75, waterY + 20, W, waterY - 45);
  ctx.stroke();

  // Vertical suspender wires
  for (let c = 10; c < W; c += 22) {
    ctx.beginPath();
    ctx.moveTo(c, waterY - 15);
    ctx.lineTo(c, waterY);
    ctx.stroke();
  }
  ctx.restore();
}

/**
 * Draws the 100M°C Blinding Thermal Fireball (Scene 2)
 */
export function drawThermalFireball(
  ctx: CanvasRenderingContext2D,
  frame: number,
  fireballProgress: number
) {
  const W = ctx.canvas.width;
  const H = ctx.canvas.height;
  const detX = 270;
  const detY = 380;
  const maxR = 210 * fireballProgress;

  // Flash illumination across entire sky
  ctx.save();
  const flashAlpha = Math.min(1.0, 0.4 + fireballProgress * 0.6);
  ctx.fillStyle = `rgba(254, 240, 138, ${flashAlpha * 0.35})`;
  ctx.fillRect(0, 0, W, H);

  // Radial Fireball (White-hot core -> Golden plasma -> Crimson boundary)
  const fg = ctx.createRadialGradient(detX, detY, 0, detX, detY, maxR);
  fg.addColorStop(0, "#ffffff");
  fg.addColorStop(0.2, "#fef08a");
  fg.addColorStop(0.5, "#f59e0b");
  fg.addColorStop(0.8, "#ea580c");
  fg.addColorStop(1, "rgba(220, 38, 38, 0)");

  ctx.fillStyle = fg;
  ctx.shadowColor = "#f59e0b";
  ctx.shadowBlur = 30;
  ctx.beginPath();
  ctx.arc(detX, detY, maxR, 0, Math.PI * 2);
  ctx.fill();

  // High-Energy Thermal Flash Rays Piercing Outward
  const numRays = 24;
  for (let r = 0; r < numRays; r++) {
    const angle = (r * Math.PI * 2) / numRays + frame * 0.04;
    const rayLen = maxR + 90 + Math.sin(frame * 0.3 + r) * 35;
    ctx.strokeStyle = "rgba(255, 255, 255, 0.7)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(detX, detY);
    ctx.lineTo(detX + Math.cos(angle) * rayLen, detY + Math.sin(angle) * rayLen);
    ctx.stroke();
  }

  // Vaporized Building Plasma Particles
  for (let p = 0; p < 120; p++) {
    const seed = p * 987;
    const pAngle = (seed % 360) * (Math.PI / 180);
    const pDist = (maxR * 0.6) + (seed % Math.floor(maxR * 0.6 + 10));
    const px = detX + Math.cos(pAngle) * pDist;
    const py = detY + Math.sin(pAngle) * pDist;
    ctx.fillStyle = p % 2 === 0 ? "#ffffff" : "#fde047";
    ctx.fillRect(Math.floor(px), Math.floor(py), 3, 3);
  }

  ctx.restore();
}

/**
 * Draws the 30 PSI Supersonic Overpressure Shockwave (Scene 3)
 */
export function drawOverpressureShockwave(
  ctx: CanvasRenderingContext2D,
  frame: number,
  shockProgress: number
) {
  const W = ctx.canvas.width;
  const H = ctx.canvas.height;
  const groundY = 720;

  // Ground bedrock
  ctx.fillStyle = "#1e293b";
  ctx.fillRect(0, groundY, W, H - groundY);

  // Concentric supersonic shock fronts expanding across frame
  const cx = 270;
  const cy = 360;
  const shockR = 60 + shockProgress * 380;

  ctx.save();
  for (let s = 0; s < 3; s++) {
    const sr = shockR - s * 40;
    if (sr > 0) {
      ctx.strokeStyle = `rgba(255, 255, 255, ${Math.max(0, 0.9 - sr / 480)})`;
      ctx.lineWidth = 4 - s;
      ctx.shadowColor = "#38bdf8";
      ctx.shadowBlur = 12;
      ctx.beginPath();
      ctx.arc(cx, cy, sr, 0, Math.PI * 2);
      ctx.stroke();
    }
  }

  // Skyscrapers getting sheared & pulverizing in micro-pixels
  const bCount = 9;
  for (let b = 0; b < bCount; b++) {
    const bx = 30 + b * 56;
    const bw = 38;
    const bh = 240 + (b % 4) * 50;
    const distToCenter = Math.abs((bx + bw / 2) - cx);

    if (distToCenter < shockR) {
      // Building shattered into debris
      const shatterAlpha = Math.max(0, 1 - (shockR - distToCenter) / 180);
      ctx.fillStyle = `rgba(148, 163, 184, ${shatterAlpha})`;
      ctx.fillRect(bx, groundY - bh * 0.4, bw, bh * 0.4);

      // Flying pulverization particles
      for (let p = 0; p < 25; p++) {
        const pSpeed = (shockR - distToCenter) * 0.8;
        const dir = bx < cx ? -1 : 1;
        const px = bx + dir * pSpeed + (p % 10) * 4;
        const py = groundY - bh * 0.6 - (p % 15) * 8;
        ctx.fillStyle = p % 2 === 0 ? "#ef4444" : "#f1f5f9";
        ctx.fillRect(Math.floor(px), Math.floor(py), 2, 2);
      }
    } else {
      // Intact building about to get hit
      ctx.fillStyle = "#334155";
      ctx.fillRect(bx, groundY - bh, bw, bh);
      // Windows
      ctx.fillStyle = "#38bdf8";
      for (let wy = groundY - bh + 10; wy < groundY - 10; wy += 16) {
        ctx.fillRect(bx + 6, wy, 8, 8);
        ctx.fillRect(bx + bw - 14, wy, 8, 8);
      }
    }
  }
  ctx.restore();
}

/**
 * Draws the Hurricane Firestorm & Oxygen Depletion (Scene 4)
 */
export function drawHurricaneFirestorm(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  const W = ctx.canvas.width;
  const H = ctx.canvas.height;
  const groundY = 720;

  // Dark inferno sky
  const sky = ctx.createLinearGradient(0, 0, 0, H);
  sky.addColorStop(0, "#180506");
  sky.addColorStop(0.4, "#450a0a");
  sky.addColorStop(1, "#7f1d1d");
  ctx.fillStyle = sky;
  ctx.fillRect(0, 0, W, H);

  // Ground rubble glowing hot
  ctx.fillStyle = "#292524";
  ctx.fillRect(0, groundY, W, H - groundY);
  ctx.fillStyle = "#ea580c";
  for (let r = 0; r < W; r += 12) {
    ctx.fillRect(r, groundY + 4, 8, 4);
  }

  // Central Fire Tornado Vortex (150+ mph inrush)
  const coreX = 270;
  ctx.save();
  for (let layer = 0; layer < 6; layer++) {
    const fH = 460 - layer * 40;
    const fW = 120 + layer * 30;
    const swirl = Math.sin(frame * 0.2 + layer) * 25;

    const fireGrad = ctx.createLinearGradient(0, groundY, 0, groundY - fH);
    fireGrad.addColorStop(0, "rgba(255, 255, 255, 0.9)");
    fireGrad.addColorStop(0.3, "rgba(250, 204, 21, 0.85)");
    fireGrad.addColorStop(0.7, "rgba(234, 88, 12, 0.8)");
    fireGrad.addColorStop(1, "rgba(185, 28, 28, 0)");

    ctx.fillStyle = fireGrad;
    ctx.beginPath();
    ctx.moveTo(coreX - fW / 2 + swirl, groundY);
    ctx.quadraticCurveTo(coreX - fW * 0.2, groundY - fH * 0.5, coreX, groundY - fH);
    ctx.quadraticCurveTo(coreX + fW * 0.2, groundY - fH * 0.5, coreX + fW / 2 + swirl, groundY);
    ctx.closePath();
    ctx.fill();
  }

  // Inward hurricane wind vectors (air suction towards the fire core)
  ctx.strokeStyle = "rgba(255, 255, 255, 0.7)";
  ctx.lineWidth = 2;
  for (let w = 0; w < 6; w++) {
    const wy = 520 + w * 32;
    // Left suction
    const lx = ((frame * 12 + w * 50) % 200);
    ctx.beginPath();
    ctx.moveTo(lx, wy);
    ctx.lineTo(lx + 40, wy);
    ctx.stroke();

    // Right suction
    const rx = W - ((frame * 12 + w * 50) % 200);
    ctx.beginPath();
    ctx.moveTo(rx, wy);
    ctx.lineTo(rx - 40, wy);
    ctx.stroke();
  }

  // Floating fiery ember particles
  for (let e = 0; e < 160; e++) {
    const seed = e * 653;
    const ex = coreX + ((seed + frame * 3) % 320) - 160;
    const ey = groundY - ((seed * 3 + frame * 9) % 520);
    ctx.fillStyle = e % 3 === 0 ? "#fef08a" : "#f97316";
    ctx.fillRect(Math.floor(ex), Math.floor(ey), 2, 2);
  }
  ctx.restore();
}

/**
 * Draws the Deep Underground NYC Subway Bedrock Cross-Section (Scene 5)
 */
export function drawSubwayCrossSection(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  const W = ctx.canvas.width;
  const H = ctx.canvas.height;

  // 1. Surface Ruins (Top 220px)
  const surfaceY = 240;
  ctx.fillStyle = "#180506";
  ctx.fillRect(0, 0, W, surfaceY);

  // Surface fire & collapsed building skeletons
  ctx.fillStyle = "#ea580c";
  for (let f = 0; f < W; f += 18) {
    const fH = 15 + Math.sin(frame * 0.3 + f) * 10;
    ctx.fillRect(f, surfaceY - fH, 12, fH);
  }

  // 2. Manhattan Schist Bedrock Layer (Surface down to Subway)
  const tunnelY = 560;
  ctx.fillStyle = "#334155"; // Dense schist rock
  ctx.fillRect(0, surfaceY, W, H - surfaceY);

  // Rock strata texture in micro-pixels
  for (let r = 0; r < 80; r++) {
    const rx = (r * 37) % W;
    const ry = surfaceY + 20 + (r * 19) % (tunnelY - surfaceY - 40);
    ctx.fillStyle = "#1e293b";
    ctx.fillRect(rx, ry, 25 + (r % 5) * 8, 3);
  }

  // Heat conduction gradient through top 5 meters of bedrock
  const heatGrad = ctx.createLinearGradient(0, surfaceY, 0, surfaceY + 90);
  heatGrad.addColorStop(0, "rgba(239, 68, 68, 0.85)");
  heatGrad.addColorStop(0.5, "rgba(234, 88, 12, 0.4)");
  heatGrad.addColorStop(1, "rgba(51, 65, 85, 0)");
  ctx.fillStyle = heatGrad;
  ctx.fillRect(0, surfaceY, W, 90);

  // 3. Deep Subway Tunnel Vault (30 Meters Underground)
  const tH = 180;
  const tW = 460;
  const tX = (W - tW) / 2;

  ctx.save();
  // Tunnel Interior
  ctx.fillStyle = "#0f172a";
  ctx.fillRect(tX, tunnelY, tW, tH);

  // Arched tunnel concrete lining
  ctx.strokeStyle = "#64748b";
  ctx.lineWidth = 6;
  ctx.strokeRect(tX, tunnelY, tW, tH);

  // Heavy steel support beams & pillars
  for (let p = tX + 40; p < tX + tW; p += 85) {
    ctx.fillStyle = "#475569";
    ctx.fillRect(p, tunnelY, 14, tH);
    // Steel rivets in micro-pixels
    ctx.fillStyle = "#94a3b8";
    for (let rv = tunnelY + 15; rv < tunnelY + tH; rv += 25) {
      ctx.fillRect(p + 4, rv, 4, 4);
    }
  }

  // Subway Train on tracks
  const trainX = tX + 30;
  const trainY = tunnelY + 50;
  const trainW = 260;
  const trainH = 95;

  ctx.fillStyle = "#94a3b8"; // Stainless steel R160/R179 train body
  ctx.fillRect(trainX, trainY, trainW, trainH);
  ctx.fillStyle = "#0284c7"; // Blue MTA accent stripe
  ctx.fillRect(trainX, trainY + 35, trainW, 8);

  // Train windows with yellow interior emergency lighting
  ctx.fillStyle = "#fef08a";
  for (let tw = trainX + 15; tw < trainX + trainW - 20; tw += 38) {
    ctx.fillRect(tw, trainY + 12, 22, 18);
  }

  // Steel rails on ballast
  ctx.fillStyle = "#cbd5e1";
  ctx.fillRect(tX + 15, tunnelY + tH - 12, tW - 30, 4);
  ctx.fillRect(tX + 15, tunnelY + tH - 24, tW - 30, 4);

  // 4. Toxic Smoke Ingress from Ventilation Shafts
  const ventX = tX + tW - 70;
  ctx.fillStyle = "rgba(15, 23, 42, 0.75)";
  ctx.fillRect(ventX, surfaceY, 35, tunnelY - surfaceY);

  // Billowing smoke particles entering the tunnel
  for (let s = 0; s < 40; s++) {
    const smY = tunnelY + ((s * 13 + frame * 3) % 90);
    const smX = ventX - 20 + ((s * 17) % 65);
    ctx.fillStyle = "rgba(71, 85, 105, 0.55)";
    ctx.fillRect(smX, smY, 8, 8);
  }

  // Depth and Shielding Callouts
  ctx.fillStyle = "#facc15";
  ctx.font = "bold 13px 'JetBrains Mono', monospace";
  ctx.fillText("30 METERS MANHATTAN SCHIST BEDROCK", tX + 18, tunnelY - 14);
  ctx.fillStyle = "#38bdf8";
  ctx.fillText("✓ 100% THERMAL & RADIATION SHIELDED", tX + 18, tunnelY + 28);
  ctx.fillStyle = "#ef4444";
  ctx.fillText("✗ OXYGEN DEPLETION VIA VENT SHAFTS", tX + 18, tunnelY + tH - 40);

  ctx.restore();
}

/**
 * Draws the 20-Kilometer Stratospheric Mushroom Cloud (Scene 6)
 */
export function drawMushroomCloud(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  const W = ctx.canvas.width;
  const H = ctx.canvas.height;
  const groundY = 820;

  // Dark post-blast sky with stratospheric boundary
  const sky = ctx.createLinearGradient(0, 0, 0, groundY);
  sky.addColorStop(0, "#030712");
  sky.addColorStop(0.3, "#0b1528");
  sky.addColorStop(0.7, "#1e1b4b");
  sky.addColorStop(1, "#3b0764");
  ctx.fillStyle = sky;
  ctx.fillRect(0, 0, W, groundY);

  // Horizon ruins
  ctx.fillStyle = "#0f172a";
  ctx.fillRect(0, groundY, W, H - groundY);

  const cx = 270;
  const cloudTopY = 220;

  ctx.save();
  // 1. Toroidal Mushroom Cap (Vortex billowing into stratosphere)
  const capW = 340;
  const capH = 160;

  const capGrad = ctx.createRadialGradient(cx, cloudTopY + 40, 20, cx, cloudTopY + 40, capW / 2);
  capGrad.addColorStop(0, "#fde047");
  capGrad.addColorStop(0.25, "#ea580c");
  capGrad.addColorStop(0.65, "#475569");
  capGrad.addColorStop(1, "rgba(15, 23, 42, 0.95)");

  ctx.fillStyle = capGrad;
  ctx.beginPath();
  ctx.ellipse(cx, cloudTopY + 40, capW / 2, capH / 2, 0, 0, Math.PI * 2);
  ctx.fill();

  // Micro-pixel billowing cloud lobes
  for (let l = 0; l < 14; l++) {
    const lAngle = (l * Math.PI) / 7;
    const lx = cx + Math.cos(lAngle) * (capW * 0.42) + Math.sin(frame * 0.1 + l) * 10;
    const ly = cloudTopY + 40 + Math.sin(lAngle) * (capH * 0.42);
    ctx.fillStyle = l % 2 === 0 ? "#64748b" : "#475569";
    ctx.beginPath();
    ctx.arc(lx, ly, 38, 0, Math.PI * 2);
    ctx.fill();
  }

  // 2. Rising Stem with Inward Condensation Collar
  const stemW = 75;
  const stemGrad = ctx.createLinearGradient(cx - stemW, 0, cx + stemW, 0);
  stemGrad.addColorStop(0, "#334155");
  stemGrad.addColorStop(0.5, "#f97316");
  stemGrad.addColorStop(1, "#1e293b");

  ctx.fillStyle = stemGrad;
  ctx.fillRect(cx - stemW / 2, cloudTopY + capH * 0.6, stemW, groundY - (cloudTopY + capH * 0.6));

  // Condensation ring around the stem
  ctx.strokeStyle = "rgba(255, 255, 255, 0.65)";
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.ellipse(cx, cloudTopY + 180, 95, 24, 0, 0, Math.PI * 2);
  ctx.stroke();

  // Internal electrostatic lightning discharges inside the dust plume
  if (frame % 16 < 8) {
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 2;
    ctx.shadowColor = "#38bdf8";
    ctx.shadowBlur = 8;
    ctx.beginPath();
    ctx.moveTo(cx - 30, cloudTopY + 50);
    ctx.lineTo(cx - 10, cloudTopY + 90);
    ctx.lineTo(cx - 25, cloudTopY + 120);
    ctx.stroke();
  }

  // Altitude Stratosphere Grid Lines
  ctx.strokeStyle = "rgba(56, 189, 248, 0.4)";
  ctx.setLineDash([4, 6]);
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(30, cloudTopY);
  ctx.lineTo(W - 30, cloudTopY);
  ctx.stroke();
  ctx.setLineDash([]);

  ctx.fillStyle = "#38bdf8";
  ctx.font = "bold 13px 'JetBrains Mono', monospace";
  ctx.fillText("STRATOSPHERE APEX: 20 KM (65,000 FT)", 45, cloudTopY - 10);
  ctx.restore();
}

/**
 * Draws the Radioactive Fallout Plume Map (Scene 7)
 */
export function drawFalloutMap(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  const W = ctx.canvas.width;
  const H = ctx.canvas.height;

  // Tactical dark map grid
  ctx.fillStyle = "#020617";
  ctx.fillRect(0, 0, W, H);

  // Coordinate grid lines
  ctx.strokeStyle = "rgba(56, 189, 248, 0.15)";
  ctx.lineWidth = 1;
  for (let x = 0; x < W; x += 40) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, H);
    ctx.stroke();
  }
  for (let y = 0; y < H; y += 40) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(W, y);
    ctx.stroke();
  }

  // Geographic Landmass Outlines (Manhattan, Brooklyn, Queens, Long Island, NJ)
  ctx.save();
  ctx.fillStyle = "#1e293b";
  ctx.strokeStyle = "rgba(56, 189, 248, 0.5)";
  ctx.lineWidth = 1.5;

  // New Jersey (West)
  ctx.beginPath();
  ctx.moveTo(0, 240);
  ctx.lineTo(120, 240);
  ctx.lineTo(130, 480);
  ctx.lineTo(110, 720);
  ctx.lineTo(0, 720);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  // Manhattan Island
  ctx.beginPath();
  ctx.moveTo(150, 310);
  ctx.lineTo(190, 330);
  ctx.lineTo(175, 520);
  ctx.lineTo(155, 530);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  // Long Island (Brooklyn, Queens, Nassau, Suffolk extending East)
  ctx.beginPath();
  ctx.moveTo(185, 490);
  ctx.lineTo(240, 470);
  ctx.lineTo(520, 490);
  ctx.lineTo(520, 620);
  ctx.lineTo(210, 610);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  // Ground Zero Detonation Point (Midtown Manhattan)
  const gzX = 175;
  const gzY = 410;

  // Jet Stream Wind Vector Arrow pointing East-North-East
  ctx.strokeStyle = "#facc15";
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.moveTo(gzX, gzY);
  ctx.lineTo(gzX + 280, gzY + 40);
  ctx.stroke();

  // Arrowhead
  ctx.fillStyle = "#facc15";
  ctx.beginPath();
  ctx.moveTo(gzX + 290, gzY + 41);
  ctx.lineTo(gzX + 275, gzY + 34);
  ctx.lineTo(gzX + 275, gzY + 48);
  ctx.closePath();
  ctx.fill();

  ctx.fillStyle = "#facc15";
  ctx.font = "bold 12px 'JetBrains Mono', monospace";
  ctx.fillText("PREVAILING WINDS (45 KM/H EAST)", gzX + 80, gzY + 25);

  // Elliptical Fallout Contours
  // Zone 1: Severe Lethal (>1000 Rem/hr)
  ctx.fillStyle = "rgba(239, 68, 68, 0.45)";
  ctx.strokeStyle = "#ef4444";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.ellipse(gzX + 60, gzY + 8, 80, 28, 0.14, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  // Zone 2: Fatal Exposure (>300 Rem/hr)
  ctx.fillStyle = "rgba(249, 115, 22, 0.3)";
  ctx.strokeStyle = "#f97316";
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.ellipse(gzX + 130, gzY + 18, 160, 46, 0.14, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  // Zone 3: Acute Sickness (>100 Rem/hr)
  ctx.fillStyle = "rgba(234, 179, 8, 0.18)";
  ctx.strokeStyle = "#eab308";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.ellipse(gzX + 180, gzY + 25, 230, 65, 0.14, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  // Ground Zero Pulsing Marker
  const gzPulse = 6 + (frame % 20);
  ctx.strokeStyle = "rgba(255, 255, 255, 0.8)";
  ctx.beginPath();
  ctx.arc(gzX, gzY, gzPulse, 0, Math.PI * 2);
  ctx.stroke();
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(gzX - 3, gzY - 3, 6, 6);

  // Fallout Legend
  const legY = 680;
  ctx.fillStyle = "rgba(15, 23, 42, 0.9)";
  ctx.strokeStyle = "rgba(56, 189, 248, 0.4)";
  ctx.strokeRect(30, legY, W - 60, 95);
  ctx.fillRect(30, legY, W - 60, 95);

  ctx.fillStyle = "#ef4444";
  ctx.fillRect(45, legY + 18, 14, 14);
  ctx.font = "bold 12px 'JetBrains Mono', monospace";
  ctx.fillText(">1,000 REM/HR (FATAL WITHIN MINUTES)", 68, legY + 30);

  ctx.fillStyle = "#f97316";
  ctx.fillRect(45, legY + 42, 14, 14);
  ctx.fillText(">300 REM/HR (FATAL WITHIN HOURS)", 68, legY + 54);

  ctx.fillStyle = "#eab308";
  ctx.fillRect(45, legY + 66, 14, 14);
  ctx.fillText(">100 REM/HR (ACUTE RADIATION SYNDROME)", 68, legY + 78);

  ctx.restore();
}
