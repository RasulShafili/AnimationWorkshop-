import { rect, circle, drawText, ART_WIDTH } from "./pixel";
import { PALETTE } from "./palette";

/**
 * Top Telecommunications / Maritime HUD Box
 * y: 12 to 58
 */
export function drawGlobalHUD(
  ctx: CanvasRenderingContext2D,
  title: string,
  rows: string[],
  alert: boolean = false
) {
  const boxX = 10;
  const boxY = 12;
  const boxW = ART_WIDTH - 20;
  const boxH = 46;

  rect(ctx, boxX, boxY, boxW, boxH, "rgba(3, 7, 18, 0.94)");
  const borderColor = alert ? PALETTE.hazardRed : PALETTE.laserCyan;
  rect(ctx, boxX, boxY, boxW, 1, borderColor);
  rect(ctx, boxX, boxY + boxH - 1, boxW, 1, borderColor);
  rect(ctx, boxX, boxY, 1, boxH, borderColor);
  rect(ctx, boxX + boxW - 1, boxY, 1, boxH, borderColor);

  // Status icon
  circle(ctx, boxX + 8, boxY + 8, 3, alert ? PALETTE.hazardRed : PALETTE.telemetryGreen);

  // Header Title
  drawText(ctx, title, boxX + 16, boxY + 5, 1, alert ? PALETTE.hazardRed : PALETTE.laserCyan);

  // Rows of telemetry
  rows.forEach((r, idx) => {
    drawText(ctx, r, boxX + 10, boxY + 17 + idx * 9, 1, "#e2e8f0");
  });
}

/**
 * Scene 1: Rotating Pixel Earth with Subsea Cable Routes & Data Pulses
 * Strict bounds: y <= 255 (y range: 68 - 250)
 */
export function drawGlobeAndUnderseaRoutes(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number
) {
  const globeR = 48;
  const globeY = cy - 5; // ~ 135

  // 1. Globe Ocean Sphere (Deep oceanic blue)
  circle(ctx, cx, globeY, globeR, "#0369a1");
  circle(ctx, cx, globeY, globeR - 2, "#0284c7");
  // Atmosphere glow ring
  circle(ctx, cx, globeY, globeR + 3, "rgba(56, 189, 248, 0.2)");

  // 2. Continents (Pixelated continents rotating horizontally)
  const rot = (frame * 0.8) % 180;
  // Continents landmass green/tan
  const landColor = "#15803d";
  const landDark = "#166534";

  // North/South America, Eurasia, Africa approximations shifting
  for (let c = -1; c <= 1; c++) {
    const lx = cx - globeR + ((rot + c * 90) % (globeR * 2 + 20)) - 10;
    // Check if within circular disk
    const dist = Math.abs(lx - cx);
    if (dist < globeR - 8) {
      const span = Math.floor(Math.sqrt(globeR * globeR - dist * dist));
      // Northern landmass
      rect(ctx, lx, globeY - span + 10, 16, 22, landColor);
      rect(ctx, lx + 2, globeY - span + 12, 12, 18, landDark);
      // Southern landmass
      rect(ctx, lx - 4, globeY + 6, 18, 24, landColor);
      rect(ctx, lx - 2, globeY + 8, 14, 20, landDark);
    }
  }

  // 3. Glowing Undersea Cable Routes (Transatlantic, Transpacific, Indian Ocean)
  const cableRoutes = [
    // Transatlantic (US East Coast -> Europe)
    { x1: cx - 35, y1: globeY - 14, x2: cx + 18, y2: globeY - 18, ctrlY: globeY - 26 },
    // Transpacific (US West Coast -> Asia)
    { x1: cx - 42, y1: globeY - 6, x2: cx - 8, y2: globeY - 2, ctrlY: globeY + 6 },
    // Red Sea / Mediterranean Choke Point
    { x1: cx + 12, y1: globeY - 12, x2: cx + 38, y2: globeY + 14, ctrlY: globeY + 2 },
    // South Atlantic / African route
    { x1: cx - 20, y1: globeY + 22, x2: cx + 24, y2: globeY + 28, ctrlY: globeY + 36 }
  ];

  cableRoutes.forEach((route, idx) => {
    // Draw curved glowing fiber line across globe
    for (let t = 0; t <= 1; t += 0.05) {
      const px = Math.floor((1 - t) * (1 - t) * route.x1 + 2 * (1 - t) * t * ((route.x1 + route.x2) / 2) + t * t * route.x2);
      const py = Math.floor((1 - t) * (1 - t) * route.y1 + 2 * (1 - t) * t * route.ctrlY + t * t * route.y2);
      rect(ctx, px, py, 1, 1, PALETTE.laserCyan);
    }

    // High-speed Laser Data Packet traveling along cable
    const packetT = ((frame * 0.04 + idx * 0.25) % 1);
    const pakX = Math.floor((1 - packetT) * (1 - packetT) * route.x1 + 2 * (1 - packetT) * packetT * ((route.x1 + route.x2) / 2) + packetT * packetT * route.x2);
    const pakY = Math.floor((1 - packetT) * (1 - packetT) * route.y1 + 2 * (1 - packetT) * packetT * route.ctrlY + packetT * packetT * route.y2);
    circle(ctx, pakX, pakY, 2, PALETTE.dataPulseYellow);
    circle(ctx, pakX, pakY, 1, "#ffffff");
  });

  // Telemetry Labels strictly above y=255
  rect(ctx, 16, 228, ART_WIDTH - 32, 18, "rgba(3, 7, 18, 0.9)");
  rect(ctx, 16, 228, ART_WIDTH - 32, 1, PALETTE.laserCyan);
  drawText(ctx, "99% OF GLOBAL TRAFFIC UNDERSEA", 28, 233, 1, PALETTE.laserCyan);
}

/**
 * Scene 2: Mechanical Cross-Section of Submarine Armored Cable
 * Concentric layers: Polyethylene, Steel armor wires, Copper tube, Jelly, Optical fibers.
 * Strict bounds: y <= 255 (y range: 68 - 250)
 */
export function drawCableCrossSection(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number
) {
  const cableY = cy - 8; // ~ 132
  const maxR = 48;

  // 1. Layer 1: Outer Black High-Density Polyethylene Jacket
  circle(ctx, cx, cableY, maxR, PALETTE.polyethyleneBlack);
  circle(ctx, cx, cableY, maxR - 2, "#334155");

  // 2. Layer 2: Stranded High-Tensile Steel Armor Wires (Ring of circular wires)
  circle(ctx, cx, cableY, maxR - 6, "#475569");
  const numWires = 18;
  for (let w = 0; w < numWires; w++) {
    const ang = (w / numWires) * Math.PI * 2;
    const wx = cx + Math.cos(ang) * (maxR - 9);
    const wy = cableY + Math.sin(ang) * (maxR - 9);
    circle(ctx, wx, wy, 3, PALETTE.cableSteelLight);
    circle(ctx, wx, wy, 1, "#cbd5e1");
  }

  // 3. Layer 3: Copper Conductor Tube (Provides 10,000V DC to subsea optical amplifiers)
  circle(ctx, cx, cableY, maxR - 16, PALETTE.copperConductor);
  circle(ctx, cx, cableY, maxR - 20, "#b45309");

  // 4. Layer 4: Polycarbonate / Aluminum Water Barrier & Petroleum Jelly
  circle(ctx, cx, cableY, maxR - 23, "#fef08a"); // petroleum jelly yellow buffer
  circle(ctx, cx, cableY, maxR - 27, "#0f172a");

  // 5. Layer 5: Central Stainless Steel Loose Tube
  circle(ctx, cx, cableY, maxR - 29, PALETTE.cableArmorGray);
  circle(ctx, cx, cableY, maxR - 33, "#020617"); // core cavity

  // 6. Layer 6: Hair-Thin Optical Glass Fibers (Silica glass cores carrying lasers)
  const numFibers = 8;
  for (let f = 0; f < numFibers; f++) {
    const fAng = (f / numFibers) * Math.PI * 2 + frame * 0.05;
    const fx = cx + Math.cos(fAng) * 7;
    const fy = cableY + Math.sin(fAng) * 7;

    // Glowing laser core
    circle(ctx, fx, fy, 2, PALETTE.laserCyan);
    circle(ctx, fx, fy, 1, "#ffffff");
  }
  // Center king fiber
  circle(ctx, cx, cableY, 2, PALETTE.dataPulseYellow);
  circle(ctx, cx, cableY, 1, "#ffffff");

  // Layer Annotation Leader Lines (Left & Right)
  // Top left: Polyethylene jacket
  rect(ctx, 16, cableY - 38, 48, 1, PALETTE.cableSteelLight);
  drawText(ctx, "POLYETHYLENE", 18, cableY - 46, 1, "#94a3b8");

  // Bottom left: Steel armor wires
  rect(ctx, 16, cableY + 28, 48, 1, PALETTE.cableSteelLight);
  drawText(ctx, "STEEL ARMOR", 20, cableY + 32, 1, PALETTE.cableSteelLight);

  // Top right: Copper 10kV power tube
  rect(ctx, cx + 24, cableY - 24, 52, 1, PALETTE.copperConductor);
  drawText(ctx, "COPPER 10kV", cx + 34, cableY - 32, 1, PALETTE.copperConductor);

  // Bottom right: Optical glass fiber core
  rect(ctx, cx + 10, cableY + 12, 65, 1, PALETTE.laserCyan);
  drawText(ctx, "SILICA FIBERS", cx + 24, cableY + 16, 1, PALETTE.laserCyan);

  // Bottom Info Banner
  rect(ctx, 16, 230, ART_WIDTH - 32, 18, "rgba(3, 7, 18, 0.95)");
  rect(ctx, 16, 230, ART_WIDTH - 32, 1, PALETTE.dataPulseYellow);
  drawText(ctx, "HAIR-THIN GLASS TRANSPORTS 100Tbps", 18, 235, 1, PALETTE.dataPulseYellow);
}

/**
 * Scene 3: Microscopic Laser Physics (Total Internal Reflection in Silica Core)
 * Core / Cladding boundary, laser ray reflection, $10T financial trade flow.
 * Strict bounds: y <= 255 (y range: 68 - 250)
 */
export function drawLaserTotalInternalReflection(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number
) {
  const boxX = 14;
  const boxY = cy - 42; // ~ 98
  const boxW = ART_WIDTH - 28;
  const boxH = 92;

  // 1. Cladding & Core Cavity
  rect(ctx, boxX, boxY, boxW, boxH, "#021226"); // Outer glass cladding (low refractive index n2)
  rect(ctx, boxX, boxY, boxW, 14, "#03294c"); // top cladding
  rect(ctx, boxX, boxY + boxH - 14, boxW, 14, "#03294c"); // bottom cladding

  // Cladding labels
  drawText(ctx, "CLADDING (n=1.45)", 18, boxY + 4, 1, "#38bdf8");
  drawText(ctx, "CLADDING (n=1.45)", 18, boxY + boxH - 10, 1, "#38bdf8");

  // Core (9-micron silica glass core n1 > n2)
  const coreY = boxY + 14;
  const coreH = boxH - 28;
  rect(ctx, boxX, coreY, boxW, coreH, "#031c36");
  rect(ctx, boxX, coreY, boxW, 1, PALETTE.laserCyan); // critical angle boundary
  rect(ctx, boxX, coreY + coreH - 1, boxW, 1, PALETTE.laserCyan);

  drawText(ctx, "SILICA CORE (n=1.47)", cx - 48, coreY + 4, 1, PALETTE.laserCoreWhite);

  // 2. High-Speed Laser Beam via Total Internal Reflection
  // Zig-zag reflection trajectory
  const points = [];
  const segW = 38;
  const numBounces = Math.ceil(boxW / segW) + 2;
  const shiftX = (frame * 3.5) % (segW * 2);

  for (let b = -1; b <= numBounces; b++) {
    const px = boxX + b * segW - shiftX;
    const py = (b % 2 === 0) ? coreY + 4 : coreY + coreH - 4;
    points.push({ x: px, y: py });
  }

  // Draw intense laser ray path
  ctx.save();
  ctx.strokeStyle = PALETTE.laserCyan;
  ctx.lineWidth = 3;
  ctx.beginPath();
  points.forEach((p, idx) => {
    if (idx === 0) ctx.moveTo(p.x, p.y);
    else ctx.lineTo(p.x, p.y);
  });
  ctx.stroke();

  // Intense white laser core
  ctx.strokeStyle = "#ffffff";
  ctx.lineWidth = 1;
  ctx.beginPath();
  points.forEach((p, idx) => {
    if (idx === 0) ctx.moveTo(p.x, p.y);
    else ctx.lineTo(p.x, p.y);
  });
  ctx.stroke();
  ctx.restore();

  // Binary Data Photons (1s and 0s) flying along core
  for (let i = 0; i < 6; i++) {
    const bx = boxX + 16 + ((i * 34 + frame * 4) % (boxW - 32));
    const by = coreY + 18 + Math.sin(bx * 0.1) * 6;
    drawText(ctx, (i % 2 === 0 ? "1" : "0"), bx, by, 1, PALETTE.dataPulseYellow);
  }

  // Bottom Financial Ticker Banner
  rect(ctx, 16, 230, ART_WIDTH - 32, 18, "rgba(3, 7, 18, 0.95)");
  rect(ctx, 16, 230, ART_WIDTH - 32, 1, PALETTE.telemetryGreen);
  drawText(ctx, "SWIFT: $10,000,000,000,000 / DAY", 20, 235, 1, PALETTE.telemetryGreen);
}

/**
 * Scene 4: Deep Sea Sabotage / Anchor Severing Cable
 * 4,000m abyss, ocean seabed, heavy dragging anchor / submarine shear, electric spark, cable snap.
 * Strict bounds: y <= 255 (y range: 68 - 250)
 */
export function drawDeepSeaSabotage(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  cutProgress: number // 0 to 1
) {
  const bedY = cy + 42; // ~ 182

  // 1. Dark Abyssal Ocean Environment
  rect(ctx, 10, 68, ART_WIDTH - 20, bedY - 68 + 35, PALETTE.oceanAbyss);

  // Marine snow drifting in water
  for (let s = 0; s < 16; s++) {
    const sx = (s * 23 + frame * 0.3) % (ART_WIDTH - 24) + 12;
    const sy = 70 + ((s * 19 + frame * 0.6) % (bedY - 72));
    circle(ctx, sx, sy, 1, "rgba(255, 255, 255, 0.25)");
  }

  // 2. Abyssal Ocean Seabed / Mud Layer
  rect(ctx, 10, bedY, ART_WIDTH - 20, 35, "#1e293b");
  rect(ctx, 10, bedY, ART_WIDTH - 20, 4, "#334155"); // silt surface
  drawText(ctx, "ABYSSAL PLAIN (DEPTH: 4,200m)", 20, bedY + 22, 1, "#64748b");

  // 3. Submarine Armored Cable Lying on Seabed
  const cableH = 6;
  const cableY = bedY - 4;

  if (cutProgress < 0.4) {
    // Intact cable
    rect(ctx, 12, cableY, ART_WIDTH - 24, cableH, PALETTE.polyethyleneBlack);
    rect(ctx, 12, cableY + 2, ART_WIDTH - 24, 2, PALETTE.laserCyan); // internal laser pulse
  } else {
    // Severed broken cable with gap
    const gap = Math.min(36, Math.floor((cutProgress - 0.4) * 55));
    // Left segment
    rect(ctx, 12, cableY, cx - gap - 12, cableH, PALETTE.polyethyleneBlack);
    rect(ctx, 12, cableY + 2, cx - gap - 12, 2, PALETTE.laserCyan);
    // Right segment
    rect(ctx, cx + gap, cableY, ART_WIDTH - 12 - (cx + gap), cableH, PALETTE.polyethyleneBlack);

    // Laser light spilling into pitch-black ocean water!
    circle(ctx, cx - gap - 12, cableY + 3, 4, PALETTE.laserCyan);
    circle(ctx, cx - gap - 12, cableY + 3, 2, "#ffffff");
    // Trailing severed glass fiber strands
    for (let f = 0; f < 4; f++) {
      const fy = cableY - 2 + f * 3;
      rect(ctx, cx - gap - 10 + f, fy, 4, 1, PALETTE.glassFiber);
    }
  }

  // 4. Massive Steel Ship Anchor Dragging / Cutting Down
  const anchorY = 75 + Math.min(65, Math.floor(cutProgress * 68));
  const ancX = cx;

  // Heavy steel anchor shank & flukes
  rect(ctx, ancX - 3, anchorY - 24, 6, 32, "#475569");
  rect(ctx, ancX - 14, anchorY - 18, 28, 4, "#334155"); // stock
  // Curved flukes digging into seabed
  rect(ctx, ancX - 22, anchorY + 4, 44, 5, "#1e293b");
  rect(ctx, ancX - 22, anchorY - 4, 6, 8, "#334155"); // left palm
  rect(ctx, ancX + 16, anchorY - 4, 6, 8, "#334155"); // right palm

  // 5. Electric Arc & Spark when 10kV copper power tube shorts!
  if (cutProgress >= 0.35 && cutProgress <= 0.75) {
    const flash = frame % 4 < 2;
    if (flash) {
      circle(ctx, cx, cableY + 2, 12, "rgba(254, 240, 138, 0.8)");
      circle(ctx, cx, cableY + 2, 6, "#ffffff");
      // Sparks flying
      rect(ctx, cx - 8, cableY - 8, 2, 2, PALETTE.dataPulseYellow);
      rect(ctx, cx + 10, cableY - 12, 2, 2, "#ffffff");
      rect(ctx, cx + 6, cableY + 8, 2, 2, PALETTE.laserCyan);
    }
  }

  // Warning Banner strictly above y=255
  rect(ctx, 16, 230, ART_WIDTH - 32, 18, "rgba(3, 7, 18, 0.95)");
  rect(ctx, 16, 230, ART_WIDTH - 32, 1, PALETTE.hazardRed);
  drawText(ctx, "CRITICAL: CABLE SEVERED AT 4,200m", 20, 235, 1, PALETTE.hazardRed);
}

/**
 * Scene 5: Global Bandwidth Collapse & Choke Point Outage
 * NOC telemetry monitor: bandwidth drops by 70%, latency 999ms, red alert map.
 * Strict bounds: y <= 255 (y range: 68 - 250)
 */
export function drawGlobalBandwidthDrop(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  collapseProgress: number // 0 to 1
) {
  const boxX = 14;
  const boxY = cy - 40; // ~ 100
  const boxW = ART_WIDTH - 28;
  const boxH = 92;

  rect(ctx, boxX, boxY, boxW, boxH, "rgba(10, 14, 28, 0.95)");
  rect(ctx, boxX, boxY, boxW, 1, PALETTE.hazardRed);
  rect(ctx, boxX, boxY + boxH - 1, boxW, 1, PALETTE.hazardRed);

  drawText(ctx, "GLOBAL TRAFFIC MONITOR (NOC)", 18, boxY + 5, 1, PALETTE.hazardRed);

  // Bandwidth Collapse Meter
  const meterY = boxY + 20;
  rect(ctx, boxX + 6, meterY, boxW - 12, 16, "#1e293b");

  const bwPct = Math.max(28, Math.floor(100 - collapseProgress * 72));
  const barW = Math.floor((bwPct / 100) * (boxW - 14));
  rect(ctx, boxX + 7, meterY + 1, barW, 14, bwPct > 50 ? PALETTE.telemetryGreen : PALETTE.hazardRed);

  drawText(ctx, `BANDWIDTH: ${bwPct}% (-72%)`, boxX + 10, meterY + 4, 1, "#ffffff");

  // Telemetry Rows below meter
  const rowY = meterY + 24;
  const lat = Math.min(999, Math.floor(32 + collapseProgress * 967));
  drawText(ctx, `INTERCONTINENTAL LATENCY: ${lat} ms`, boxX + 8, rowY, 1, lat > 500 ? PALETTE.hazardRed : PALETTE.laserCyan);
  drawText(ctx, `PACKET LOSS: ${Math.min(98, Math.floor(collapseProgress * 98))}% (TIMEOUT)`, boxX + 8, rowY + 10, 1, PALETTE.dataPulseYellow);
  drawText(ctx, "RED SEA / ATLANTIC CORRIDOR: SEVERED", boxX + 8, rowY + 20, 1, PALETTE.hazardRed);

  // Flashing Outage Alert Banner
  const alertFlash = frame % 12 < 6;
  rect(ctx, 16, 230, ART_WIDTH - 32, 18, alertFlash ? "#7f1d1d" : "#991b1b");
  drawText(ctx, "GLOBAL INTERNET BANDWIDTH COLLAPSED", 18, 235, 1, "#ffffff");
}

/**
 * Scene 6: Financial Banking & Cloud Datacenter Blackout
 * SWIFT interbank network halt, stock exchanges freeze, servers disconnected.
 * Strict bounds: y <= 255 (y range: 68 - 250)
 */
export function drawFinancialAndCloudFreeze(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number
) {
  const boxX = 14;
  const boxY = cy - 40; // ~ 100
  const boxW = ART_WIDTH - 28;
  const boxH = 92;

  rect(ctx, boxX, boxY, boxW, boxH, "rgba(5, 8, 16, 0.95)");
  rect(ctx, boxX, boxY, boxW, 1, PALETTE.hazardRed);
  rect(ctx, boxX, boxY + boxH - 1, boxW, 1, PALETTE.hazardRed);

  // SWIFT Terminal Header
  drawText(ctx, "SWIFT INTERBANK CLEARING: FROZEN", 18, boxY + 5, 1, PALETTE.hazardRed);

  // Terminal screen readout
  rect(ctx, boxX + 6, boxY + 18, boxW - 12, 42, "#030712");
  rect(ctx, boxX + 6, boxY + 18, boxW - 12, 1, "#334155");

  drawText(ctx, "> SETTLEMENT: FAILED", boxX + 10, boxY + 22, 1, PALETTE.hazardRed);
  drawText(ctx, "> $10T TRANSACTIONS QUEUED", boxX + 10, boxY + 31, 1, PALETTE.dataPulseYellow);
  drawText(ctx, "> NYSE / LSE / TOKYO: OFFLINE", boxX + 10, boxY + 40, 1, PALETTE.hazardRed);
  drawText(ctx, "> CLOUD DATACENTERS SEVERED", boxX + 10, boxY + 49, 1, "#94a3b8");

  // Server rack icons blinking red error
  for (let s = 0; s < 5; s++) {
    const sx = boxX + 10 + s * 38;
    const sy = boxY + 66;
    rect(ctx, sx, sy, 32, 16, "#1e293b");
    circle(ctx, sx + 5, sy + 4, 2, (frame + s) % 10 < 5 ? PALETTE.hazardRed : "#475569");
    circle(ctx, sx + 12, sy + 4, 2, (frame + s) % 10 < 5 ? PALETTE.hazardRed : "#475569");
    drawText(ctx, "FAIL", sx + 6, sy + 9, 1, PALETTE.hazardRed);
  }

  // Bottom Banner
  rect(ctx, 16, 230, ART_WIDTH - 32, 18, "rgba(3, 7, 18, 0.95)");
  rect(ctx, 16, 230, ART_WIDTH - 32, 1, PALETTE.hazardRed);
  drawText(ctx, "GLOBAL FINANCIAL TRANSACTIONS HALT", 18, 235, 1, PALETTE.hazardRed);
}

/**
 * Scene 7: Specialized Cable Repair Ship & ROV Deployment
 * Surface ship in waves, crane umbilical winch, ROV descending to seabed.
 * Strict bounds: y <= 255 (y range: 68 - 250)
 */
export function drawShipAndROVDeployment(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number
) {
  // 1. Ocean Surface & Sky
  rect(ctx, 10, 68, ART_WIDTH - 20, 36, "#0369a1"); // surface ocean water
  rect(ctx, 10, 68, ART_WIDTH - 20, 8, "#38bdf8"); // wave tops

  // 2. Specialized Cable Ship (*CS Sovereign* style)
  const shipX = cx - 45;
  const shipY = 70 + Math.sin(frame * 0.1) * 2;

  // Ship hull (White & blue)
  rect(ctx, shipX, shipY, 90, 14, "#f8fafc");
  rect(ctx, shipX + 75, shipY - 6, 15, 6, "#f8fafc"); // bow rake
  rect(ctx, shipX, shipY + 10, 90, 4, "#0284c7"); // boot-topping blue stripe

  // Superstructure bridge
  rect(ctx, shipX + 22, shipY - 14, 34, 14, "#f8fafc");
  rect(ctx, shipX + 26, shipY - 10, 26, 4, "#0f172a"); // bridge windows
  rect(ctx, shipX + 38, shipY - 20, 4, 6, "#cbd5e1"); // radar mast

  // Stern A-Frame Cable Crane (Aft deployment)
  const aframeX = shipX + 6;
  rect(ctx, aframeX, shipY - 12, 3, 16, "#eab308");
  rect(ctx, aframeX + 8, shipY - 12, 3, 16, "#eab308");
  rect(ctx, aframeX, shipY - 12, 11, 2, "#eab308");

  // 3. Deep Water Column (Gradient into darkness)
  rect(ctx, 10, 104, ART_WIDTH - 20, 60, "#082f49");
  rect(ctx, 10, 164, ART_WIDTH - 20, 64, PALETTE.oceanAbyss);

  // Umbilical winch cable descending miles down
  for (let y = 104; y < 185; y += 2) {
    rect(ctx, aframeX + 4, y, 1, 1, PALETTE.dataPulseYellow);
  }

  // 4. ROV on Seabed Retrieving Broken Cable
  // Draw ROV holding the cable at bottom
  import("./characters").then(m => {
    // handled synchronously below
  });
  // Inline mini ROV depiction on seabed
  const rovY = 195;
  rect(ctx, cx - 24, rovY, 48, 22, PALETTE.rovYellow);
  circle(ctx, cx - 14, rovY + 18, 4, "#ffffff"); // floodlight
  // Light beam
  ctx.save();
  ctx.fillStyle = "rgba(255, 255, 255, 0.15)";
  ctx.beginPath();
  ctx.moveTo(cx - 14, rovY + 18);
  ctx.lineTo(cx - 40, rovY + 30);
  ctx.lineTo(cx + 10, rovY + 30);
  ctx.closePath();
  ctx.fill();
  ctx.restore();

  // Cable clamped in hydraulic arm
  rect(ctx, cx - 35, rovY + 24, 70, 3, PALETTE.polyethyleneBlack);

  // Bottom Banner
  rect(ctx, 16, 230, ART_WIDTH - 32, 18, "rgba(3, 7, 18, 0.95)");
  rect(ctx, 16, 230, ART_WIDTH - 32, 1, PALETTE.rovYellow);
  drawText(ctx, "ROV RETRIEVES SEVERED ENDS FROM 4,000m", 18, 235, 1, PALETTE.rovYellow);
}

/**
 * Scene 8: Microscopic Fiber Fusion Splice in Shipboard Cleanroom
 * Dual V-groove clamps aligning 125um glass fibers, electric arc firing, core fusion.
 * Strict bounds: y <= 255 (y range: 68 - 250)
 */
export function drawMicroscopicFusionSplice(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  spliceProgress: number // 0 to 1
) {
  const boxX = 14;
  const boxY = cy - 40; // ~ 100
  const boxW = ART_WIDTH - 28;
  const boxH = 92;

  rect(ctx, boxX, boxY, boxW, boxH, "rgba(2, 6, 23, 0.95)");
  rect(ctx, boxX, boxY, boxW, 1, PALETTE.laserCyan);
  rect(ctx, boxX, boxY + boxH - 1, boxW, 1, PALETTE.laserCyan);

  drawText(ctx, "CLEANROOM FUSION SPLICER (MICRON ZOOM)", 18, boxY + 5, 1, PALETTE.laserCyan);

  const fiberY = boxY + 44;
  const fThick = 12;

  // 1. Dual Motorized V-Groove Clamps (Left & Right)
  rect(ctx, boxX + 6, fiberY - 14, 38, 40, "#334155");
  rect(ctx, boxX + boxW - 44, fiberY - 14, 38, 40, "#334155");
  drawText(ctx, "V-GROOVE", boxX + 8, fiberY + 16, 1, "#94a3b8");
  drawText(ctx, "V-GROOVE", boxX + boxW - 42, fiberY + 16, 1, "#94a3b8");

  // 2. Optical Glass Fibers (125-micron silica cladding with 9-micron core)
  const gap = spliceProgress > 0.6 ? 0 : Math.max(0, Math.floor(18 - spliceProgress * 30));

  // Left fiber end
  rect(ctx, boxX + 44, fiberY - fThick / 2, cx - (boxX + 44) - gap, fThick, "#0284c7");
  rect(ctx, boxX + 44, fiberY - 1, cx - (boxX + 44) - gap, 2, PALETTE.laserCoreWhite); // optical core

  // Right fiber end
  rect(ctx, cx + gap, fiberY - fThick / 2, (boxX + boxW - 44) - (cx + gap), fThick, "#0284c7");
  rect(ctx, cx + gap, fiberY - 1, (boxX + boxW - 44) - (cx + gap), 2, PALETTE.laserCoreWhite); // optical core

  // 3. Top & Bottom Tungsten Electrodes
  rect(ctx, cx - 2, fiberY - 26, 4, 12, "#cbd5e1"); // top electrode
  rect(ctx, cx - 2, fiberY + 14, 4, 12, "#cbd5e1"); // bottom electrode

  // 4. High-Voltage Electric Arc Discharge (Fusing the silica glass)
  if (spliceProgress >= 0.4 && spliceProgress <= 0.8) {
    const arcFlash = frame % 3 < 2;
    if (arcFlash) {
      circle(ctx, cx, fiberY, 14, "rgba(56, 189, 248, 0.6)");
      circle(ctx, cx, fiberY, 7, "#ffffff");
      // Vertical electric plasma arc
      rect(ctx, cx - 1, fiberY - 14, 2, 28, "#e0f2fe");
    }
  }

  // 5. Signal Restored Indicator
  if (spliceProgress > 0.8) {
    circle(ctx, cx, fiberY, 4, PALETTE.telemetryGreen);
    drawText(ctx, "FUSION COMPLETE: LOSS < 0.01 dB", cx - 62, fiberY - 20, 1, PALETTE.telemetryGreen);
  } else {
    drawText(ctx, "CORE ALIGNMENT: 0.02 um", cx - 48, fiberY - 20, 1, PALETTE.dataPulseYellow);
  }

  // Bottom Banner
  rect(ctx, 16, 230, ART_WIDTH - 32, 18, "rgba(3, 7, 18, 0.95)");
  rect(ctx, 16, 230, ART_WIDTH - 32, 1, PALETTE.telemetryGreen);
  drawText(ctx, "MICROSCOPIC FIBERS SPLICED BY HAND", 22, 235, 1, PALETTE.telemetryGreen);
}
