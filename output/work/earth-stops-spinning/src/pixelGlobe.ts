import { WORLD_MAP_B64, WORLD_MAP_WIDTH, WORLD_MAP_HEIGHT } from "./worldData";

// Decode base64 bitmask once at module initialization
let worldBytes: Uint8Array | null = null;

function getWorldBytes(): Uint8Array {
  if (!worldBytes) {
    if (typeof atob === "function") {
      const bin = atob(WORLD_MAP_B64);
      worldBytes = new Uint8Array(bin.length);
      for (let i = 0; i < bin.length; i++) {
        worldBytes[i] = bin.charCodeAt(i);
      }
    } else {
      const buf = Buffer.from(WORLD_MAP_B64, "base64");
      worldBytes = new Uint8Array(buf);
    }
  }
  return worldBytes;
}

/**
 * Returns true if the given (longitude, latitude) coordinate on Earth is land.
 * lonDeg: -180 to +180
 * latDeg: -90 to +90
 */
export function isEarthLand(lonDeg: number, latDeg: number): boolean {
  const bytes = getWorldBytes();
  const nLon = ((lonDeg + 180) % 360 + 360) % 360 - 180;
  let col = Math.floor(((nLon + 180) / 360) * WORLD_MAP_WIDTH);
  let row = Math.floor(((90 - latDeg) / 180) * WORLD_MAP_HEIGHT);
  col = Math.max(0, Math.min(WORLD_MAP_WIDTH - 1, col));
  row = Math.max(0, Math.min(WORLD_MAP_HEIGHT - 1, row));
  const idx = row * WORLD_MAP_WIDTH + col;
  const byteVal = bytes[idx >> 3];
  return (byteVal & (1 << (7 - (idx & 7)))) !== 0;
}

/**
 * Renders high-density micro-pixel rotating Earth.
 */
export function renderEarthSpinning(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  R: number,
  rotDeg: number,
  frame: number,
  options: {
    showEquatorSpeed?: boolean;
    showCoordinates?: boolean;
    glowColor?: string;
  } = {}
) {
  const width = ctx.canvas.width;
  const height = ctx.canvas.height;
  const imgData = ctx.createImageData(width, height);
  const data32 = new Uint32Array(imgData.data.buffer);

  const startY = Math.max(0, Math.floor(cy - R));
  const endY = Math.min(height - 1, Math.ceil(cy + R));

  for (let y = startY; y <= endY; y++) {
    const dy = (y - cy) / R;
    const dy2 = dy * dy;
    if (dy2 >= 1.0) continue;

    const dxMax = Math.sqrt(1.0 - dy2) * R;
    const startX = Math.max(0, Math.floor(cx - dxMax));
    const endX = Math.min(width - 1, Math.ceil(cx + dxMax));

    const latRad = Math.asin(-dy);
    const latDeg = latRad * (180 / Math.PI);

    for (let x = startX; x <= endX; x++) {
      const dx = (x - cx) / R;
      const r2 = dx * dx + dy2;
      if (r2 >= 1.0) continue;

      const dz = Math.sqrt(1.0 - r2);
      const lonRad = Math.atan2(dx, dz) + (rotDeg * Math.PI) / 180;
      const lonDeg = lonRad * (180 / Math.PI);

      const land = isEarthLand(lonDeg, latDeg);

      // Spherical lighting
      const diffuse = Math.max(0.0, dx * 0.38 - dy * 0.28 + dz * 0.88);
      const rim = Math.pow(1.0 - dz, 2.6);

      let r: number, g: number, b: number;
      if (land) {
        // High-density natural terrain
        r = Math.floor(18 + 36 * diffuse + 40 * rim);
        g = Math.floor(135 + 85 * diffuse + 50 * rim);
        b = Math.floor(65 + 40 * diffuse + 85 * rim);
      } else {
        // Oceanic abyss
        r = Math.floor(2 + 14 * diffuse + 20 * rim);
        g = Math.floor(30 + 60 * diffuse + 95 * rim);
        b = Math.floor(92 + 120 * diffuse + 160 * rim);
      }

      // Latitudinal grid lines in micro-pixels
      if (Math.abs(latDeg % 30) < 1.2 || Math.abs(latDeg) < 1.0) {
        r = Math.min(255, r + 45);
        g = Math.min(255, g + 65);
        b = Math.min(255, b + 90);
      }

      const pixelIdx = y * width + x;
      data32[pixelIdx] =
        (255 << 24) |
        (Math.min(255, b) << 16) |
        (Math.min(255, g) << 8) |
        Math.min(255, r);
    }
  }

  ctx.putImageData(imgData, 0, 0);

  // Outer atmospheric glow ring
  ctx.save();
  ctx.strokeStyle = options.glowColor || "rgba(34, 211, 238, 0.45)";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(cx, cy, R + 1, 0, Math.PI * 2);
  ctx.stroke();

  ctx.strokeStyle = "rgba(34, 211, 238, 0.2)";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.arc(cx, cy, R + 10, 0, Math.PI * 2);
  ctx.stroke();

  // Equatorial Velocity tangent vector inside canvas boundaries
  if (options.showEquatorSpeed) {
    const eqY = cy;
    const arrowXStart = cx + 20;
    const arrowXEnd = cx + R + 25;

    // Glowing cyan tangent arrow
    ctx.strokeStyle = "#22d3ee";
    ctx.lineWidth = 3;
    ctx.shadowColor = "#22d3ee";
    ctx.shadowBlur = 10;
    ctx.beginPath();
    ctx.moveTo(arrowXStart, eqY);
    ctx.lineTo(arrowXEnd, eqY);
    ctx.stroke();

    // Arrowhead
    ctx.fillStyle = "#22d3ee";
    ctx.beginPath();
    ctx.moveTo(arrowXEnd + 8, eqY);
    ctx.lineTo(arrowXEnd - 6, eqY - 6);
    ctx.lineTo(arrowXEnd - 6, eqY + 6);
    ctx.closePath();
    ctx.fill();

    // Centered Equatorial speed badge below the globe
    const badgeW = 240;
    const badgeH = 50;
    const badgeX = cx - badgeW / 2;
    const badgeY = cy + R + 20;

    ctx.fillStyle = "rgba(3, 8, 20, 0.88)";
    ctx.strokeStyle = "rgba(34, 211, 238, 0.7)";
    ctx.lineWidth = 1.5;
    ctx.fillRect(badgeX, badgeY, badgeW, badgeH);
    ctx.strokeRect(badgeX, badgeY, badgeW, badgeH);

    ctx.fillStyle = "#22d3ee";
    ctx.font = "bold 12px 'JetBrains Mono', monospace";
    ctx.textAlign = "center";
    ctx.fillText("EQUATORIAL ROTATION SPEED", cx, badgeY + 18);
    ctx.fillStyle = "#f8fafc";
    ctx.font = "bold 20px 'JetBrains Mono', monospace";
    ctx.fillText("1,670 KM/H (465 M/S)", cx, badgeY + 40);
    ctx.textAlign = "left";
  }

  ctx.restore();
}

/**
 * Renders Earth with Inertia Vectors & Sudden Halting Shockwave (Scene 2)
 */
export function renderEarthInertia(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  R: number,
  rotDeg: number,
  frame: number,
  alertProgress: number
) {
  const width = ctx.canvas.width;
  const height = ctx.canvas.height;
  const imgData = ctx.createImageData(width, height);
  const data32 = new Uint32Array(imgData.data.buffer);

  const startY = Math.max(0, Math.floor(cy - R));
  const endY = Math.min(height - 1, Math.ceil(cy + R));

  for (let y = startY; y <= endY; y++) {
    const dy = (y - cy) / R;
    const dy2 = dy * dy;
    if (dy2 >= 1.0) continue;

    const dxMax = Math.sqrt(1.0 - dy2) * R;
    const startX = Math.max(0, Math.floor(cx - dxMax));
    const endX = Math.min(width - 1, Math.ceil(cx + dxMax));

    const latRad = Math.asin(-dy);
    const latDeg = latRad * (180 / Math.PI);

    for (let x = startX; x <= endX; x++) {
      const dx = (x - cx) / R;
      const r2 = dx * dx + dy2;
      if (r2 >= 1.0) continue;

      const dz = Math.sqrt(1.0 - r2);
      const lonRad = Math.atan2(dx, dz) + (rotDeg * Math.PI) / 180;
      const lonDeg = lonRad * (180 / Math.PI);

      const land = isEarthLand(lonDeg, latDeg);
      const diffuse = Math.max(0.0, dx * 0.38 - dy * 0.28 + dz * 0.88);
      const rim = Math.pow(1.0 - dz, 2.6);

      let r: number, g: number, b: number;
      if (land) {
        r = Math.floor(25 + 40 * diffuse + (alertProgress * 40));
        g = Math.floor(120 + 70 * diffuse);
        b = Math.floor(60 + 35 * diffuse);
      } else {
        r = Math.floor(2 + 10 * diffuse);
        g = Math.floor(30 + 50 * diffuse);
        b = Math.floor(95 + 110 * diffuse);
      }

      // Red highlight at equator when halting
      if (Math.abs(latDeg) < 8.0) {
        r = Math.min(255, r + Math.floor(alertProgress * 110));
        g = Math.max(0, g - Math.floor(alertProgress * 40));
      }

      const pixelIdx = y * width + x;
      data32[pixelIdx] =
        (255 << 24) |
        (Math.min(255, b) << 16) |
        (Math.min(255, g) << 8) |
        Math.min(255, r);
    }
  }

  ctx.putImageData(imgData, 0, 0);

  // Inertia momentum vector arrows across latitudes
  ctx.save();
  const latitudes = [
    { deg: 0, speed: "1,670 KM/H", len: 80, color: "#ef4444", label: "EQUATOR (MAX INERTIA)" },
    { deg: 30, speed: "1,446 KM/H", len: 65, color: "#f97316", label: "30° LATITUDE" },
    { deg: -30, speed: "1,446 KM/H", len: 65, color: "#f97316", label: "30°S LATITUDE" },
    { deg: 60, speed: "835 KM/H", len: 45, color: "#eab308", label: "60° LATITUDE" },
    { deg: 85, speed: "145 KM/H", len: 20, color: "#22c55e", label: "POLES: ~0 KM/H" }
  ];

  latitudes.forEach(item => {
    const yOff = cy - Math.sin((item.deg * Math.PI) / 180) * R;
    const arrowLen = item.len * alertProgress;

    // Line across sphere tangent
    ctx.strokeStyle = item.color;
    ctx.lineWidth = 2.5;
    ctx.shadowColor = item.color;
    ctx.shadowBlur = 8;
    ctx.beginPath();
    ctx.moveTo(cx - 50, yOff);
    ctx.lineTo(cx + arrowLen, yOff);
    ctx.stroke();

    // Arrowhead
    ctx.fillStyle = item.color;
    ctx.beginPath();
    ctx.moveTo(cx + arrowLen + 6, yOff);
    ctx.lineTo(cx + arrowLen - 5, yOff - 4);
    ctx.lineTo(cx + arrowLen - 5, yOff + 4);
    ctx.closePath();
    ctx.fill();

    // Label tag
    if (arrowLen > 25) {
      ctx.fillStyle = item.color;
      ctx.font = "bold 11px 'JetBrains Mono', monospace";
      ctx.fillText(`${item.speed}`, cx + arrowLen + 10, yOff + 4);
    }
  });

  // Sudden Stop Red Kinetic Ring
  const pulseR = R + ((frame * 3) % 45);
  ctx.strokeStyle = `rgba(239, 68, 68, ${Math.max(0, 0.7 - (pulseR - R) / 45)})`;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(cx, cy, pulseR, 0, Math.PI * 2);
  ctx.stroke();

  ctx.restore();
}

/**
 * Renders Planetary Core Cross-Section (Scene 5)
 */
export function renderEarthCoreSlice(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  R: number,
  frame: number,
  sloshOffset: number
) {
  // Planetary layers
  const crustR = R;
  const mantleR = R * 0.88;
  const outerCoreR = R * 0.52;
  const innerCoreR = R * 0.22;

  ctx.save();

  // 1. Mantle (Silicate rock convection, dark molten amber)
  const mantleGrad = ctx.createRadialGradient(cx, cy, outerCoreR, cx, cy, crustR);
  mantleGrad.addColorStop(0, "#ea580c");
  mantleGrad.addColorStop(0.5, "#9a3412");
  mantleGrad.addColorStop(1, "#451a03");
  ctx.fillStyle = mantleGrad;
  ctx.beginPath();
  ctx.arc(cx, cy, crustR, 0, Math.PI * 2);
  ctx.fill();

  // 2. Liquid Iron Outer Core (Sloshing violently with vortex swirls)
  const coreX = cx + Math.sin(frame * 0.2) * sloshOffset;
  const coreY = cy + Math.cos(frame * 0.15) * (sloshOffset * 0.6);
  const outerCoreGrad = ctx.createRadialGradient(coreX, coreY, innerCoreR, coreX, coreY, outerCoreR);
  outerCoreGrad.addColorStop(0, "#fef08a");
  outerCoreGrad.addColorStop(0.4, "#facc15");
  outerCoreGrad.addColorStop(0.8, "#d97706");
  outerCoreGrad.addColorStop(1, "#991b1b");

  ctx.fillStyle = outerCoreGrad;
  ctx.shadowColor = "#f59e0b";
  ctx.shadowBlur = 18;
  ctx.beginPath();
  ctx.arc(coreX, coreY, outerCoreR, 0, Math.PI * 2);
  ctx.fill();

  // Molten metal convection swirls
  ctx.strokeStyle = "rgba(255, 255, 255, 0.6)";
  ctx.lineWidth = 2;
  for (let a = 0; a < 6; a++) {
    const angle = (frame * 0.08) + (a * Math.PI) / 3;
    const swirlR = innerCoreR + 18 + Math.sin(frame * 0.1 + a) * 12;
    ctx.beginPath();
    ctx.arc(coreX, coreY, swirlR, angle, angle + 0.8);
    ctx.stroke();
  }

  // 3. Solid Dense Inner Core (White-hot crystallization)
  const innerCoreGrad = ctx.createRadialGradient(coreX, coreY, 0, coreX, coreY, innerCoreR);
  innerCoreGrad.addColorStop(0, "#ffffff");
  innerCoreGrad.addColorStop(0.6, "#fef9c3");
  innerCoreGrad.addColorStop(1, "#fde047");
  ctx.fillStyle = innerCoreGrad;
  ctx.shadowColor = "#ffffff";
  ctx.shadowBlur = 24;
  ctx.beginPath();
  ctx.arc(coreX, coreY, innerCoreR, 0, Math.PI * 2);
  ctx.fill();

  // 4. Crust Rim in Micro-Pixels
  ctx.strokeStyle = "#22c55e";
  ctx.lineWidth = 4;
  ctx.shadowBlur = 0;
  ctx.beginPath();
  ctx.arc(cx, cy, crustR, 0, Math.PI * 2);
  ctx.stroke();

  // 5. Collapsing Geomagnetic Field Lines (Snapping & flickering)
  const numLines = 8;
  const breakFlicker = (frame % 8 < 4);
  for (let i = 0; i < numLines; i++) {
    const sign = i % 2 === 0 ? 1 : -1;
    const spread = (Math.floor(i / 2) + 1) * 36;
    ctx.strokeStyle = breakFlicker ? "rgba(239, 68, 68, 0.55)" : "rgba(34, 211, 238, 0.3)";
    ctx.lineWidth = 1.5;
    ctx.setLineDash([8, 12]);
    ctx.beginPath();
    ctx.ellipse(cx, cy, R + spread, (R + spread) * 0.55, 0, 0, Math.PI * 2);
    ctx.stroke();
  }
  ctx.setLineDash([]);

  // Solar Wind Cosmic Radiation Rays bombarding the surface
  const solarRayCount = 14;
  for (let r = 0; r < solarRayCount; r++) {
    const rayY = cy - R + (r * (2 * R)) / solarRayCount;
    const rayXStart = cx - R - 130;
    const rayXEnd = cx - R + 10 + Math.sin(frame * 0.2 + r) * 15;

    ctx.strokeStyle = "rgba(239, 68, 68, 0.75)";
    ctx.lineWidth = 2;
    ctx.shadowColor = "#ef4444";
    ctx.shadowBlur = 6;
    ctx.beginPath();
    ctx.moveTo(rayXStart, rayY);
    ctx.lineTo(rayXEnd, rayY);
    ctx.stroke();

    // Impact spark
    ctx.fillStyle = "#fef08a";
    ctx.fillRect(rayXEnd - 2, rayY - 2, 4, 4);
  }

  // Layer Labels
  ctx.fillStyle = "#ffffff";
  ctx.font = "bold 13px 'JetBrains Mono', monospace";
  ctx.fillText("CRUST", cx + R - 15, cy - R + 30);
  ctx.fillText("MANTLE", cx + R - 60, cy - R * 0.7);
  ctx.fillStyle = "#facc15";
  ctx.fillText("LIQUID IRON CORE (SLOSHING)", cx + 20, cy + outerCoreR * 0.85);
  ctx.fillStyle = "#fef08a";
  ctx.fillText("SOLID INNER CORE", cx - 60, cy - innerCoreR - 8);

  ctx.restore();
}

/**
 * Renders Earth Restart & Global Magnitude 12 Quakes (Scene 6)
 */
export function renderEarthQuakeFaults(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  R: number,
  rotDeg: number,
  frame: number
) {
  renderEarthSpinning(ctx, cx, cy, R, rotDeg, frame, { glowColor: "rgba(239, 68, 68, 0.6)" });

  ctx.save();
  // Glowing magma tectonic fault lines
  const faultLines = [
    // Pacific Ring of Fire
    [[-120, 38], [-140, 55], [-170, 60], [160, 50], [140, 35], [125, 10], [140, -20], [-170, -40]],
    // Mid-Atlantic Ridge
    [[-30, 70], [-25, 45], [-35, 15], [-20, -10], [-15, -45]],
    // Alpine-Himalayan belt
    [[0, 38], [25, 36], [50, 32], [80, 30], [95, 25], [105, 5]]
  ];

  faultLines.forEach((line, lIdx) => {
    ctx.strokeStyle = lIdx === 0 ? "#ef4444" : "#f97316";
    ctx.lineWidth = 2.5;
    ctx.shadowColor = "#ef4444";
    ctx.shadowBlur = 12;

    let started = false;
    ctx.beginPath();
    line.forEach(coord => {
      const lon = coord[0];
      const lat = coord[1];
      const rLon = ((lon - rotDeg) * Math.PI) / 180;
      const rLat = (lat * Math.PI) / 180;
      const z = R * Math.cos(rLat) * Math.cos(rLon);

      if (z > 0) {
        const px = cx + R * Math.cos(rLat) * Math.sin(rLon);
        const py = cy - R * Math.sin(rLat);
        if (!started) {
          ctx.moveTo(px, py);
          started = true;
        } else {
          ctx.lineTo(px, py);
        }
      } else {
        started = false;
      }
    });
    ctx.stroke();
  });

  // Seismic shockwave rings propagating from major epicenters
  for (let s = 0; s < 3; s++) {
    const sPhase = ((frame * 2.5 + s * 22) % 65);
    const sRadius = 15 + sPhase * 1.8;
    const alpha = Math.max(0, 0.8 - sPhase / 65);

    ctx.strokeStyle = `rgba(239, 68, 68, ${alpha})`;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(cx - 40, cy + 10, sRadius, 0, Math.PI * 2);
    ctx.stroke();

    ctx.strokeStyle = `rgba(250, 204, 21, ${alpha})`;
    ctx.beginPath();
    ctx.arc(cx + 60, cy - 30, sRadius * 0.8, 0, Math.PI * 2);
    ctx.stroke();
  }

  ctx.restore();
}

/**
 * Renders Planetary Aftermath: Oceans drained to poles, dry equator supercontinent (Scene 7)
 */
export function renderEarthAftermath(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  R: number,
  rotDeg: number,
  frame: number
) {
  const width = ctx.canvas.width;
  const height = ctx.canvas.height;
  const imgData = ctx.createImageData(width, height);
  const data32 = new Uint32Array(imgData.data.buffer);

  const startY = Math.max(0, Math.floor(cy - R));
  const endY = Math.min(height - 1, Math.ceil(cy + R));

  for (let y = startY; y <= endY; y++) {
    const dy = (y - cy) / R;
    const dy2 = dy * dy;
    if (dy2 >= 1.0) continue;

    const dxMax = Math.sqrt(1.0 - dy2) * R;
    const startX = Math.max(0, Math.floor(cx - dxMax));
    const endX = Math.min(width - 1, Math.ceil(cx + dxMax));

    const latRad = Math.asin(-dy);
    const latDeg = latRad * (180 / Math.PI);

    for (let x = startX; x <= endX; x++) {
      const dx = (x - cx) / R;
      const r2 = dx * dx + dy2;
      if (r2 >= 1.0) continue;

      const dz = Math.sqrt(1.0 - r2);
      const diffuse = Math.max(0.0, dx * 0.38 - dy * 0.28 + dz * 0.88);
      const rim = Math.pow(1.0 - dz, 2.6);

      // In a non-spinning Earth, centrifugal bulge disappears!
      // Water drains towards high latitudes (> 45° and < -45°),
      // creating two polar super-oceans and an equatorial dry land belt.
      const isWater = Math.abs(latDeg) > 42.0;

      let r: number, g: number, b: number;
      if (isWater) {
        // Polar oceans
        r = Math.floor(2 + 10 * diffuse + 20 * rim);
        g = Math.floor(35 + 50 * diffuse + 80 * rim);
        b = Math.floor(100 + 110 * diffuse + 150 * rim);
      } else {
        // Equatorial desert & dry seabeds (canyons, arid rock)
        r = Math.floor(120 + 65 * diffuse + 40 * rim);
        g = Math.floor(85 + 45 * diffuse + 25 * rim);
        b = Math.floor(55 + 30 * diffuse + 20 * rim);
      }

      const pixelIdx = y * width + x;
      data32[pixelIdx] =
        (255 << 24) |
        (Math.min(255, b) << 16) |
        (Math.min(255, g) << 8) |
        Math.min(255, r);
    }
  }

  ctx.putImageData(imgData, 0, 0);

  // Labels for the transformed planet
  ctx.save();
  ctx.fillStyle = "#38bdf8";
  ctx.font = "bold 13px 'JetBrains Mono', monospace";
  ctx.fillText("NORTH POLAR OCEAN", cx - 80, cy - R + 45);
  ctx.fillText("SOUTH POLAR OCEAN", cx - 80, cy + R - 35);

  ctx.fillStyle = "#facc15";
  ctx.font = "bold 15px 'JetBrains Mono', monospace";
  ctx.fillText("EQUATORIAL MEGA-CONTINENT", cx - 120, cy + 5);
  ctx.font = "12px 'JetBrains Mono', monospace";
  ctx.fillText("(OCEANS DRAINED WITHOUT CENTRIFUGAL FORCE)", cx - 150, cy + 25);
  ctx.restore();
}
