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
      // Node.js fallback
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
  // Normalize lon to [-180, 180)
  const nLon = ((lonDeg + 180) % 360 + 360) % 360 - 180;
  let col = Math.floor(((nLon + 180) / 360) * WORLD_MAP_WIDTH);
  let row = Math.floor(((90 - latDeg) / 180) * WORLD_MAP_HEIGHT);
  col = Math.max(0, Math.min(WORLD_MAP_WIDTH - 1, col));
  row = Math.max(0, Math.min(WORLD_MAP_HEIGHT - 1, row));
  const idx = row * WORLD_MAP_WIDTH + col;
  const byteVal = bytes[idx >> 3];
  return (byteVal & (1 << (7 - (idx & 7)))) !== 0;
}

export interface CableRoute {
  name: string;
  points: [number, number][]; // [lon, lat]
  color: string;
  glowColor: string;
  speed: number;
}

export const REAL_CABLE_ROUTES: CableRoute[] = [
  // Transatlantic (US East Coast - UK/France)
  {
    name: "TAT-14 / MAREA (Transatlantic)",
    points: [
      [-74.0, 40.7],  // NYC
      [-60.0, 42.5],
      [-42.0, 48.0],
      [-22.0, 50.5],
      [-5.0, 50.2],   // UK Cornwall / France
      [2.3, 48.8]     // Paris
    ],
    color: "#22d3ee",
    glowColor: "rgba(34, 211, 238, 0.6)",
    speed: 0.02
  },
  // Transpacific (Tokyo - California)
  {
    name: "FASTER / UNITY (Transpacific)",
    points: [
      [139.7, 35.6],  // Tokyo
      [158.0, 38.0],
      [180.0, 42.0],
      [-160.0, 41.0],
      [-140.0, 39.0],
      [-122.4, 37.7]  // San Francisco
    ],
    color: "#38bdf8",
    glowColor: "rgba(56, 189, 248, 0.6)",
    speed: 0.015
  },
  // Europe - Mediterranean - Red Sea - India - SE Asia (SEA-ME-WE)
  {
    name: "SEA-ME-WE (Eurasia Corridor)",
    points: [
      [-5.0, 36.0],   // Gibraltar
      [5.3, 43.3],    // Marseille
      [14.5, 36.0],   // Sicily
      [32.3, 30.0],   // Suez Canal
      [38.0, 22.0],   // Red Sea
      [43.5, 12.5],   // Bab-el-Mandeb Strait
      [58.0, 15.0],   // Arabian Sea
      [72.8, 19.0],   // Mumbai
      [80.2, 13.0],   // Chennai
      [103.8, 1.3]    // Singapore
    ],
    color: "#f59e0b",
    glowColor: "rgba(245, 158, 11, 0.7)",
    speed: 0.018
  },
  // South Atlantic (Brazil - West Africa)
  {
    name: "SAIL (South Atlantic)",
    points: [
      [-38.5, -3.7],  // Fortaleza, Brazil
      [-20.0, -4.0],
      [-5.0, -4.5],
      [9.5, 0.5]      // Gabon / Cameroon
    ],
    color: "#06b6d4",
    glowColor: "rgba(6, 182, 212, 0.5)",
    speed: 0.022
  },
  // Asia-Pacific Gateway (Singapore - Hong Kong - Tokyo)
  {
    name: "APG (East Asia)",
    points: [
      [103.8, 1.3],   // Singapore
      [108.0, 12.0],  // Vietnam
      [114.2, 22.3],  // Hong Kong
      [121.5, 25.0],  // Taiwan
      [139.7, 35.6]   // Tokyo
    ],
    color: "#10b981",
    glowColor: "rgba(16, 185, 129, 0.6)",
    speed: 0.02
  }
];

export function renderMicroPixelGlobe(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  R: number,
  rotDeg: number,
  frame: number,
  options: {
    highlightCut?: boolean;
    cutLocation?: [number, number]; // [lon, lat]
  } = {}
) {
  const width = ctx.canvas.width;
  const height = ctx.canvas.height;

  // Render base sphere using fast ImageData
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

      // Spherical diffuse and rim lighting
      const diffuse = Math.max(0.0, dx * 0.38 - dy * 0.28 + dz * 0.88);
      const rim = Math.pow(1.0 - dz, 2.8);

      let r: number, g: number, b: number;
      if (land) {
        // High-density micro-pixel continent terrain
        // Realistic continent emerald/olive with elevation & atmosphere
        r = Math.floor(18 + 32 * diffuse + 45 * rim);
        g = Math.floor(130 + 85 * diffuse + 55 * rim);
        b = Math.floor(65 + 45 * diffuse + 90 * rim);
      } else {
        // Deep oceanic abyss (dark cyan-sapphire)
        r = Math.floor(2 + 14 * diffuse + 22 * rim);
        g = Math.floor(28 + 58 * diffuse + 95 * rim);
        b = Math.floor(88 + 115 * diffuse + 160 * rim);
      }

      const pixelIdx = y * width + x;
      // Little-endian RGBA: 0xAABBGGRR
      data32[pixelIdx] =
        (255 << 24) |
        (Math.min(255, b) << 16) |
        (Math.min(255, g) << 8) |
        Math.min(255, r);
    }
  }

  ctx.putImageData(imgData, 0, 0);

  // Draw atmosphere rings and orbital grid in micro-pixels
  ctx.save();
  ctx.strokeStyle = "rgba(34, 211, 238, 0.4)";
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.arc(cx, cy, R + 1, 0, Math.PI * 2);
  ctx.stroke();

  ctx.strokeStyle = "rgba(34, 211, 238, 0.18)";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.arc(cx, cy, R + 12, 0, Math.PI * 2);
  ctx.stroke();

  // Draw oceanic cables mapped onto sphere
  REAL_CABLE_ROUTES.forEach(route => {
    ctx.strokeStyle = route.color;
    ctx.lineWidth = 2;
    ctx.shadowColor = route.glowColor;
    ctx.shadowBlur = 8;
    ctx.beginPath();

    let started = false;
    const projectedPts: { x: number; y: number; z: number }[] = [];

    // Interpolate points along the path for smooth spherical arc
    for (let i = 0; i < route.points.length - 1; i++) {
      const p1 = route.points[i];
      const p2 = route.points[i + 1];
      const steps = 14;

      for (let s = 0; s <= steps; s++) {
        const t = s / steps;
        const lon = p1[0] + (p2[0] - p1[0]) * t;
        const lat = p1[1] + (p2[1] - p1[1]) * t;

        const rLon = ((lon - rotDeg) * Math.PI) / 180;
        const rLat = (lat * Math.PI) / 180;

        const z = R * Math.cos(rLat) * Math.cos(rLon);
        const px = cx + R * Math.cos(rLat) * Math.sin(rLon);
        const py = cy - R * Math.sin(rLat);

        projectedPts.push({ x: px, y: py, z });
      }
    }

    // Connect visible front-facing segments
    for (let i = 0; i < projectedPts.length; i++) {
      const pt = projectedPts[i];
      if (pt.z > -10) {
        if (!started) {
          ctx.beginPath();
          ctx.moveTo(pt.x, pt.y);
          started = true;
        } else {
          ctx.lineTo(pt.x, pt.y);
        }
      } else {
        if (started) {
          ctx.stroke();
          started = false;
        }
      }
    }
    if (started) {
      ctx.stroke();
    }

    // High-speed Traveling Photons along the cable
    const numPhotons = 3;
    for (let p = 0; p < numPhotons; p++) {
      const pProgress = ((frame * route.speed + p / numPhotons) % 1 + 1) % 1;
      const targetIdx = Math.floor(pProgress * (projectedPts.length - 1));
      const pt = projectedPts[targetIdx];
      if (pt && pt.z > 0) {
        ctx.fillStyle = "#ffffff";
        ctx.shadowColor = "#fef08a";
        ctx.shadowBlur = 10;
        ctx.fillRect(Math.floor(pt.x - 2), Math.floor(pt.y - 2), 4, 4);

        ctx.fillStyle = "#facc15";
        ctx.fillRect(Math.floor(pt.x - 3), Math.floor(pt.y - 3), 6, 6);
      }
    }
  });

  // If severed cut highlight is active (e.g. Red Sea / Bab-el-Mandeb)
  if (options.highlightCut) {
    const cutLon = options.cutLocation ? options.cutLocation[0] : 43.5;
    const cutLat = options.cutLocation ? options.cutLocation[1] : 12.5;

    const rLon = ((cutLon - rotDeg) * Math.PI) / 180;
    const rLat = (cutLat * Math.PI) / 180;
    const z = R * Math.cos(rLat) * Math.cos(rLon);

    if (z > 0) {
      const cutX = cx + R * Math.cos(rLat) * Math.sin(rLon);
      const cutY = cy - R * Math.sin(rLat);

      const pulse = (Math.sin(frame * 0.25) + 1) * 0.5;
      const blastR = 8 + pulse * 14;

      ctx.save();
      ctx.strokeStyle = `rgba(239, 68, 68, ${0.8 - pulse * 0.4})`;
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.arc(cutX, cutY, blastR, 0, Math.PI * 2);
      ctx.stroke();

      ctx.fillStyle = "#ef4444";
      ctx.fillRect(cutX - 3, cutY - 3, 6, 6);

      ctx.fillStyle = "#ffffff";
      ctx.fillRect(cutX - 1.5, cutY - 1.5, 3, 3);
      ctx.restore();
    }
  }

  // Draw Orbiting Satellite in micro-pixel art
  const satAngle = (frame * -0.6 * Math.PI) / 180;
  const satDist = R + 46;
  const satX = cx + Math.cos(satAngle) * satDist;
  const satY = cy + Math.sin(satAngle) * (satDist * 0.55);

  ctx.save();
  ctx.shadowColor = "rgba(34, 211, 238, 0.5)";
  ctx.shadowBlur = 6;
  // Satellite body
  ctx.fillStyle = "#e2e8f0";
  ctx.fillRect(satX - 4, satY - 4, 8, 8);
  // Solar panels (blue micro-pixel rectangles)
  ctx.fillStyle = "#0284c7";
  ctx.fillRect(satX - 14, satY - 3, 8, 6);
  ctx.fillRect(satX + 6, satY - 3, 8, 6);
  // Solar panel gold grid line
  ctx.fillStyle = "#facc15";
  ctx.fillRect(satX - 11, satY - 1, 2, 2);
  ctx.fillRect(satX + 9, satY - 1, 2, 2);

  // Faint dashed beam from satellite to Earth
  ctx.strokeStyle = "rgba(255, 255, 255, 0.2)";
  ctx.setLineDash([3, 4]);
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(satX, satY);
  ctx.lineTo(cx + (satX - cx) * 0.75, cy + (satY - cy) * 0.75);
  ctx.stroke();
  ctx.restore();

  ctx.restore();
}
