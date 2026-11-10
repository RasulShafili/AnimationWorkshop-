// What Nicotine Does to Your Brain: Cartoon Pixel Art Engine (360x640 Canvas)
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

// 1. Atmospheric Cartoon Night Street Background
export function drawCityStreetBackground(ctx: CanvasRenderingContext2D, frame: number) {
  // Midnight gradient sky
  const skyGrad = ctx.createLinearGradient(0, 0, 0, PH);
  skyGrad.addColorStop(0, "#080614");
  skyGrad.addColorStop(0.6, "#120D24");
  skyGrad.addColorStop(1, "#1A1432");
  ctx.fillStyle = skyGrad;
  ctx.fillRect(0, 0, PW, PH);

  // Crescent Moon
  pCircle(ctx, 300, 70, 20, "#FFF9C4", 2);
  pCircle(ctx, 308, 65, 17, "#080614", 2);

  // Twinkling cartoon stars
  const stars = [
    { x: 40, y: 50 }, { x: 95, y: 80 }, { x: 160, y: 45 },
    { x: 230, y: 65 }, { x: 70, y: 130 }, { x: 260, y: 110 }
  ];
  stars.forEach((s, idx) => {
    const twinkle = Math.sin(frame * 0.15 + idx) > 0;
    if (twinkle) {
      pRect(ctx, s.x, s.y, 2, 2, "#FFFFFF");
      pRect(ctx, s.x - 2, s.y, 6, 2, "rgba(255,255,255,0.4)");
      pRect(ctx, s.x, s.y - 2, 2, 6, "rgba(255,255,255,0.4)");
    }
  });

  // Distant city skyline buildings (dark silhouette)
  pRect(ctx, 10, 180, 50, 460, "#0E0B1A");
  pRect(ctx, 55, 140, 65, 500, "#141026");
  pRect(ctx, 115, 170, 70, 470, "#0F0C1E");
  pRect(ctx, 180, 130, 80, 510, "#16122B");
  pRect(ctx, 255, 160, 60, 480, "#100D22");
  pRect(ctx, 310, 190, 45, 450, "#0D0A1C");

  // Glowing yellow apartment windows
  for (let b = 0; b < 6; b++) {
    const bx = 20 + b * 55;
    for (let wy = 200; wy < 420; wy += 35) {
      if ((b + wy) % 3 === 0) {
        pRect(ctx, bx + 12, wy, 8, 12, "#FFD54F");
        pRect(ctx, bx + 14, wy + 2, 4, 8, "#FFF59D");
      }
    }
  }

  // Brick Wall Foreground & Sidewalk
  pRect(ctx, 0, 450, PW, 190, "#211A2C");
  // Brick mortar lines
  for (let by = 450; by < 550; by += 14) {
    pRect(ctx, 0, by, PW, 2, "#171220");
    const offset = (by % 28 === 0) ? 0 : 18;
    for (let bx = offset; bx < PW; bx += 36) {
      pRect(ctx, bx, by, 2, 14, "#171220");
    }
  }

  // Sidewalk Curb & Street Floor
  pRect(ctx, 0, 545, PW, 12, "#37474F");
  pRect(ctx, 0, 545, PW, 3, "#546E7A");
  pRect(ctx, 0, 557, PW, 83, "#1A1A24");

  // Classic Street Lamp (on left side)
  pRect(ctx, 45, 230, 8, 315, "#263238"); // Pole
  pRect(ctx, 41, 230, 16, 8, "#37474F");
  pRect(ctx, 35, 205, 28, 26, "#1E272C");  // Lamp head
  // Glowing yellow lantern
  pRect(ctx, 39, 213, 20, 16, "#FFEE58");
  pRect(ctx, 42, 215, 14, 12, "#FFFFFF");

  // Warm golden cone of light shining down
  const lampGrad = ctx.createRadialGradient(49, 220, 10, 100, 420, 240);
  lampGrad.addColorStop(0, "rgba(255, 238, 88, 0.35)");
  lampGrad.addColorStop(0.5, "rgba(255, 213, 79, 0.15)");
  lampGrad.addColorStop(1, "rgba(0, 0, 0, 0)");
  ctx.fillStyle = lampGrad;
  ctx.fillRect(0, 200, 260, 440);
}

// 2. Animated Character "Alex" - High-Detail Cartoon Character
export function drawAlexCharacter(
  ctx: CanvasRenderingContext2D,
  frame: number,
  mode: "smoking" | "superhero" | "cravingZombie"
) {
  const ax = 180;
  const ay = 400; // Base position near sidewalk

  if (mode === "smoking") {
    // SCENE 1: Taking a puff under the lamp
    // Body breathing motion
    const breath = Math.sin(frame * 0.1) * 2;

    // Shadow on ground
    pCircle(ctx, ax, 552, 38, "rgba(0,0,0,0.5)", 2);

    // Legs & Denim Jeans
    pRect(ctx, ax - 18, ay + 68, 14, 80, "#1E3C72");
    pRect(ctx, ax + 4, ay + 68, 14, 80, "#1E3C72");
    // Shoes (Red retro sneakers)
    pRect(ctx, ax - 24, ay + 142, 20, 10, "#E53935");
    pRect(ctx, ax - 26, ay + 148, 24, 4, "#FFFFFF");
    pRect(ctx, ax + 4, ay + 142, 20, 10, "#E53935");
    pRect(ctx, ax + 2, ay + 148, 24, 4, "#FFFFFF");

    // Torso (Dark Teal Hoodie)
    pRect(ctx, ax - 26, ay - 8 + breath, 52, 80, "#00695C");
    pRect(ctx, ax - 22, ay - 6 + breath, 44, 76, "#00796B");
    pRect(ctx, ax - 8, ay - 8 + breath, 16, 76, "#004D40"); // Center zipper
    pRect(ctx, ax - 4, ay - 8 + breath, 8, 40, "#E0F2F1");  // White t-shirt inner

    // Left Arm (holding vape/cigarette up to mouth)
    pRect(ctx, ax + 24, ay + 6 + breath, 14, 38, "#00796B");
    pRect(ctx, ax + 14, ay + 40 + breath, 22, 12, "#00695C");
    // Hand & Vape
    pRect(ctx, ax + 8, ay + 20 + breath, 12, 12, "#FFCC80");
    pRect(ctx, ax - 6, ay + 12 + breath, 18, 6, "#CFD8DC"); // Vape body
    pRect(ctx, ax - 8, ay + 11 + breath, 4, 8, "#00E5FF");  // Glowing cyan LED tip!

    // Right Arm (in pocket)
    pRect(ctx, ax - 38, ay + 4 + breath, 14, 55, "#00695C");
    pRect(ctx, ax - 30, ay + 50 + breath, 12, 14, "#004D40");

    // Neck
    pRect(ctx, ax - 8, ay - 24 + breath, 16, 18, "#FFA726");
    pRect(ctx, ax - 6, ay - 22 + breath, 12, 16, "#FFCC80");

    // Head (Facing left-center, closed eyes puffing in pleasure)
    pRect(ctx, ax - 24, ay - 75 + breath, 48, 52, "#FFA726");
    pRect(ctx, ax - 22, ay - 73 + breath, 44, 48, "#FFCC80");

    // Brown anime hair
    pRect(ctx, ax - 28, ay - 88 + breath, 56, 25, "#4E342E");
    pRect(ctx, ax - 26, ay - 85 + breath, 52, 20, "#6D4C41");
    // Front hair bangs
    pRect(ctx, ax - 28, ay - 70 + breath, 12, 18, "#4E342E");
    pRect(ctx, ax - 16, ay - 72 + breath, 14, 14, "#5D4037");

    // Face features (Eyes closed in relaxed bliss: ^ _)
    pRect(ctx, ax - 14, ay - 54 + breath, 8, 3, "#3E2723"); // Left eye curve
    pRect(ctx, ax + 4, ay - 54 + breath, 8, 3, "#3E2723");  // Right eye curve
    // Rosy cheeks
    pCircle(ctx, ax - 16, ay - 44 + breath, 4, "rgba(255, 112, 67, 0.5)", 1);
    pCircle(ctx, ax + 14, ay - 44 + breath, 4, "rgba(255, 112, 67, 0.5)", 1);
    // Mouth on vape mouthpiece
    pRect(ctx, ax - 6, ay - 38 + breath, 8, 4, "#D84315");

    // Billowing Pixel Smoke Clouds!
    const smokePhase = frame * 0.12;
    for (let c = 0; c < 8; c++) {
      const age = ((frame * 1.6 + c * 25) % 140);
      const sy = ay - 36 - age * 1.1;
      const sx = ax - 20 - age * 0.6 + Math.sin(smokePhase + c) * 12;
      const r = 8 + age * 0.22;
      const alpha = Math.max(0, 1 - age / 130);
      pCircle(ctx, sx, sy, r, `rgba(236, 239, 241, ${alpha * 0.75})`, 2);
      pCircle(ctx, sx - 2, sy - 2, r * 0.7, `rgba(255, 255, 255, ${alpha * 0.85})`, 2);
    }

    // Glowing Neon Energy Bolt rushing up neck into head!
    const energyY = ay + 30 - ((frame * 4) % 110);
    pCircle(ctx, ax, energyY, 6, "#76FF03", 1);
    pCircle(ctx, ax, energyY, 3, "#FFFFFF", 1);

    // Comic Badge in air: "10s TO BRAIN! ⚡"
    pRect(ctx, ax + 40, ay - 110, 130, 26, "rgba(10, 15, 28, 0.95)");
    ctx.strokeStyle = "#76FF03";
    ctx.lineWidth = 2;
    ctx.strokeRect(ax + 40, ay - 110, 130, 26);
    ctx.fillStyle = "#76FF03";
    ctx.font = "8px monospace";
    ctx.fillText("10s SPRINT TO BRAIN!⚡", ax + 46, ay - 94);
  }

  else if (mode === "superhero") {
    // SCENE 3: Chest puffed, smiling wide, glowing superhero aura, heart thumping!
    const bounce = Math.sin(frame * 0.2) * 3;

    // Glowing Golden Superhero Aura!
    for (let a = 1; a <= 3; a++) {
      const auraR = 60 + a * 14 + Math.sin(frame * 0.3 + a) * 6;
      ctx.strokeStyle = `rgba(255, 213, 79, ${0.4 - a * 0.1})`;
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.arc(ax, ay + 20 + bounce, auraR, 0, Math.PI * 2);
      ctx.stroke();
    }

    // Shadow
    pCircle(ctx, ax, 552, 42, "rgba(0,0,0,0.5)", 2);

    // Legs standing wide & confident
    pRect(ctx, ax - 26, ay + 68, 16, 80, "#1E3C72");
    pRect(ctx, ax + 10, ay + 68, 16, 80, "#1E3C72");
    pRect(ctx, ax - 34, ay + 142, 24, 10, "#E53935");
    pRect(ctx, ax + 10, ay + 142, 24, 10, "#E53935");

    // Torso (Puffed up!)
    pRect(ctx, ax - 32, ay - 12 + bounce, 64, 82, "#00796B");
    pRect(ctx, ax - 28, ay - 10 + bounce, 56, 78, "#00897B");

    // Arms on hips (Superhero pose!)
    // Left arm
    pRect(ctx, ax - 48, ay - 4 + bounce, 18, 14, "#00695C");
    pRect(ctx, ax - 46, ay + 8 + bounce, 14, 34, "#00695C");
    pRect(ctx, ax - 34, ay + 38 + bounce, 12, 12, "#FFCC80");
    // Right arm
    pRect(ctx, ax + 30, ay - 4 + bounce, 18, 14, "#00695C");
    pRect(ctx, ax + 32, ay + 8 + bounce, 14, 34, "#00695C");
    pRect(ctx, ax + 22, ay + 38 + bounce, 12, 12, "#FFCC80");

    // Big Cartoon Pumping Heart on chest!
    const heartPump = Math.sin(frame * 0.5) > 0 ? 4 : 0;
    pCircle(ctx, ax - 6, ay + 14 + bounce, 10 + heartPump, "#FF1744", 2);
    pCircle(ctx, ax + 6, ay + 14 + bounce, 10 + heartPump, "#FF1744", 2);
    // Heart bottom triangle
    for (let hy = 0; hy < 12; hy += 2) {
      pRect(ctx, ax - 12 + hy, ay + 18 + hy + bounce, 24 - hy * 2, 2, "#FF1744");
    }
    // "95 BPM!" Heart rate label
    pRect(ctx, ax - 24, ay + 34 + bounce, 48, 14, "rgba(0,0,0,0.85)");
    ctx.fillStyle = "#FFEB3B";
    ctx.font = "8px monospace";
    ctx.fillText("95 BPM!♥", ax - 20, ay + 44 + bounce);

    // Head (Tilted up, confident wide grin!)
    pRect(ctx, ax - 24, ay - 78 + bounce, 48, 52, "#FFCC80");
    pRect(ctx, ax - 28, ay - 90 + bounce, 56, 25, "#4E342E"); // Hair

    // Big Star Eyes! (★ ‿ ★)
    pRect(ctx, ax - 16, ay - 56 + bounce, 8, 8, "#FFD54F");
    pRect(ctx, ax - 14, ay - 54 + bounce, 4, 4, "#FFFFFF");
    pRect(ctx, ax + 8, ay - 56 + bounce, 8, 8, "#FFD54F");
    pRect(ctx, ax + 10, ay - 54 + bounce, 4, 4, "#FFFFFF");

    // Big confident happy smile!
    pRect(ctx, ax - 12, ay - 40 + bounce, 24, 6, "#FFFFFF");
    pRect(ctx, ax - 8, ay - 38 + bounce, 16, 8, "#D84315");

    // Speed lines zooming in background!
    for (let sl = 0; sl < 6; sl++) {
      const ly = (frame * 12 + sl * 80) % 500;
      const lx = 20 + sl * 60;
      pRect(ctx, lx, ly, 2, 25, "rgba(255, 238, 88, 0.45)");
    }
  }

  else if (mode === "cravingZombie") {
    // SCENE 5: Hunched over, pale skin, shivering jitter, sweat flying!
    const jitterX = (Math.sin(frame * 0.8) + (frame % 3 === 0 ? 2 : -2));
    const cxP = ax + jitterX;

    // Shadow
    pCircle(ctx, cxP, 552, 34, "rgba(0,0,0,0.5)", 2);

    // Legs shivering
    pRect(ctx, cxP - 16, ay + 75, 12, 75, "#15284F");
    pRect(ctx, cxP + 4, ay + 75, 12, 75, "#15284F");
    pRect(ctx, cxP - 22, ay + 144, 20, 10, "#9E9E9E");
    pRect(ctx, cxP + 4, ay + 144, 20, 10, "#9E9E9E");

    // Hunched Torso (Slumped forward)
    pRect(ctx, cxP - 28, ay + 6, 56, 74, "#004D40");
    pRect(ctx, cxP - 24, ay + 8, 48, 70, "#00695C");

    // Arms trembling, hands clutching chest / pockets
    pRect(ctx, cxP - 36, ay + 16, 12, 45, "#004D40");
    pRect(ctx, cxP - 26, ay + 48, 14, 14, "#CFD8DC"); // Shivering pale hand
    pRect(ctx, cxP + 24, ay + 16, 12, 45, "#004D40");
    pRect(ctx, cxP + 12, ay + 48, 14, 14, "#CFD8DC");

    // Neck (Slumped)
    pRect(ctx, cxP - 8, ay - 8, 16, 18, "#B0BEC5");

    // Head (Pale sickly skin `#CFD8DC`, messy hair)
    pRect(ctx, cxP - 24, ay - 58, 48, 52, "#B0BEC5");
    pRect(ctx, cxP - 22, ay - 56, 44, 48, "#CFD8DC");
    pRect(ctx, cxP - 28, ay - 72, 56, 24, "#37474F"); // Messy uncombed hair

    // Bloodshot stressed eyes! (X _ X) or twitching circles
    pCircle(ctx, cxP - 12, ay - 38, 7, "#FF1744", 1);
    pCircle(ctx, cxP - 12, ay - 38, 4, "#FFFFFF", 1);
    pCircle(ctx, cxP - 12, ay - 38, 2, "#000000", 1);

    pCircle(ctx, cxP + 12, ay - 38, 7, "#FF1744", 1);
    pCircle(ctx, cxP + 12, ay - 38, 4, "#FFFFFF", 1);
    pCircle(ctx, cxP + 12, ay - 38, 2, "#000000", 1);

    // Mouth trembling in anxiety
    pRect(ctx, cxP - 10, ay - 22, 20, 4, "#37474F");
    pRect(ctx, cxP - 8, ay - 20, 4, 3, "#FFFFFF"); // Chattering teeth
    pRect(ctx, cxP, ay - 20, 4, 3, "#FFFFFF");
    pRect(ctx, cxP + 6, ay - 20, 4, 3, "#FFFFFF");

    // Flying cartoon sweat drops!
    for (let sw = 0; sw < 4; sw++) {
      const dropProg = ((frame * 0.15 + sw * 0.25) % 1);
      const dx = (sw % 2 === 0 ? cxP - 30 : cxP + 30) + (sw % 2 === 0 ? -dropProg * 25 : dropProg * 25);
      const dy = ay - 45 + dropProg * 40;
      pCircle(ctx, dx, dy, 3, "#80DEEA", 1);
      pCircle(ctx, dx, dy, 1, "#FFFFFF", 1);
    }

    // Shaking comic speed lines around him
    pRect(ctx, cxP - 42, ay, 8, 2, "#FF5252");
    pRect(ctx, cxP - 46, ay + 20, 10, 2, "#FF5252");
    pRect(ctx, cxP + 38, ay, 8, 2, "#FF5252");
    pRect(ctx, cxP + 42, ay + 20, 10, 2, "#FF5252");

    // Thought bubble: Cigarette / Vape with red glowing exclamation mark!
    pCircle(ctx, cxP + 55, ay - 85, 26, "rgba(10, 15, 28, 0.95)", 2);
    ctx.strokeStyle = "#FF1744";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(cxP + 55, ay - 85, 26, 0, Math.PI * 2);
    ctx.stroke();

    // Little cigarette inside thought bubble
    pRect(ctx, cxP + 42, ay - 88, 26, 6, "#ECEFF1");
    pRect(ctx, cxP + 42, ay - 88, 6, 6, "#FFB74D"); // Filter
    pRect(ctx, cxP + 66, ay - 89, 4, 8, "#FF1744");  // Lit cherry tip!
    // Smoke curl
    pCircle(ctx, cxP + 72, ay - 96, 4, "rgba(255,255,255,0.7)", 1);
  }
}

// 3. The Animated Cartoon Brain Character (Scenes 2 & 4)
export function drawCartoonBrainCharacter(
  ctx: CanvasRenderingContext2D,
  frame: number,
  mode: "jackpotParty" | "hungryMonster"
) {
  const bx = 180;
  const by = 350;

  if (mode === "jackpotParty") {
    // SCENE 2: Brain wearing sunglasses, dancing, coins & stars bursting!
    const dance = Math.sin(frame * 0.25) * 6;
    const wiggle = Math.cos(frame * 0.25) * 4;

    // Disco light beams behind brain
    for (let b = 0; b < 6; b++) {
      const ang = (b * Math.PI) / 3 + frame * 0.04;
      const lx = bx + Math.cos(ang) * 160;
      const ly = by + Math.sin(ang) * 160;
      ctx.strokeStyle = (b % 2 === 0 ? "rgba(255, 213, 79, 0.25)" : "rgba(118, 255, 3, 0.20)");
      ctx.lineWidth = 14;
      ctx.beginPath();
      ctx.moveTo(bx, by);
      ctx.lineTo(lx, ly);
      ctx.stroke();
    }

    // Pink Brain Lobes Body
    pCircle(ctx, bx - 35 + wiggle, by - 15 + dance, 42, "#F06292", 2);
    pCircle(ctx, bx + 35 + wiggle, by - 15 + dance, 42, "#F06292", 2);
    pCircle(ctx, bx + wiggle, by + 10 + dance, 44, "#EC407A", 2);
    // Brain convolutions & texture squiggles
    pCircle(ctx, bx - 20 + wiggle, by - 35 + dance, 22, "#F48FB1", 2);
    pCircle(ctx, bx + 20 + wiggle, by - 35 + dance, 22, "#F48FB1", 2);
    pCircle(ctx, bx - 45 + wiggle, by + 8 + dance, 20, "#D81B60", 2);
    pCircle(ctx, bx + 45 + wiggle, by + 8 + dance, 20, "#D81B60", 2);

    // Cool 8-Bit Sunglasses!
    pRect(ctx, bx - 38 + wiggle, by - 16 + dance, 32, 18, "#212121");
    pRect(ctx, bx + 6 + wiggle, by - 16 + dance, 32, 18, "#212121");
    pRect(ctx, bx - 6 + wiggle, by - 12 + dance, 12, 6, "#212121"); // Bridge
    // White reflection glare on shades
    pRect(ctx, bx - 34 + wiggle, by - 14 + dance, 6, 6, "#FFFFFF");
    pRect(ctx, bx + 10 + wiggle, by - 14 + dance, 6, 6, "#FFFFFF");

    // Big Cartoon Smiling Mouth
    pRect(ctx, bx - 14 + wiggle, by + 18 + dance, 28, 8, "#FFFFFF");
    pRect(ctx, bx - 10 + wiggle, by + 20 + dance, 20, 10, "#C2185B");

    // Little cartoon dancing hands in the air!
    pCircle(ctx, bx - 65 + wiggle, by - 40 - dance, 10, "#F06292", 2);
    pCircle(ctx, bx + 65 + wiggle, by - 40 + dance, 10, "#F06292", 2);

    // Neon Nicotine Troopers parachuting in!
    for (let p = 0; p < 4; p++) {
      const py = 120 + ((frame * 2.5 + p * 45) % 180);
      const px = bx - 90 + p * 60 + Math.sin(frame * 0.1 + p) * 8;
      // Green parachute
      ctx.strokeStyle = "#76FF03";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(px, py - 12, 14, Math.PI, 0);
      ctx.stroke();
      // Nicotine dot
      pCircle(ctx, px, py, 6, "#76FF03", 1);
      pCircle(ctx, px, py, 2, "#FFFFFF", 1);
    }

    // Explosive Dopamine Jackpot! (Gold Coins, Stars, Diamonds flying!)
    for (let j = 0; j < 14; j++) {
      const jProg = ((frame * 0.04 + j * 0.08) % 1);
      const ang = (j * Math.PI * 2) / 14;
      const dist = 40 + jProg * 140;
      const jx = bx + Math.cos(ang) * dist;
      const jy = by + Math.sin(ang) * dist * 0.75;
      const rot = frame * 0.2 + j;

      if (j % 3 === 0) {
        // Gold Coin (★)
        pCircle(ctx, jx, jy, 8, "#FFD54F", 1);
        pCircle(ctx, jx, jy, 5, "#FFA000", 1);
        pRect(ctx, jx - 2, jy - 2, 4, 4, "#FFFFFF");
      } else if (j % 3 === 1) {
        // Cyan Diamond Gem
        pRect(ctx, jx - 5, jy - 5, 10, 10, "#00E5FF");
        pRect(ctx, jx - 2, jy - 2, 4, 4, "#FFFFFF");
      } else {
        // Sparkle
        pCircle(ctx, jx, jy, 5, "#76FF03", 1);
      }
    }

    // Floating Jackpot Banner: "DOPAMINE JACKPOT! 🎰"
    pRect(ctx, bx - 90, by + 85, 180, 28, "rgba(10, 15, 28, 0.95)");
    ctx.strokeStyle = "#FFD54F";
    ctx.lineWidth = 2;
    ctx.strokeRect(bx - 90, by + 85, 180, 28);
    ctx.fillStyle = "#FFD54F";
    ctx.font = "9px monospace";
    ctx.fillText("DOPAMINE JACKPOT! 🎰", bx - 78, by + 103);
  }

  else if (mode === "hungryMonster") {
    // SCENE 4: Brain mutant with hungry open jaws/mouths demanding MORE!
    const shake = Math.sin(frame * 0.4) * 3;

    // Darker mutated purple brain
    pCircle(ctx, bx - 35, by - 15 + shake, 44, "#8E24AA", 2);
    pCircle(ctx, bx + 35, by - 15 + shake, 44, "#8E24AA", 2);
    pCircle(ctx, bx, by + 10 + shake, 46, "#6A1B9A", 2);

    // Shocked / Angry Cartoon Eyes
    pCircle(ctx, bx - 16, by - 18 + shake, 10, "#FFFFFF", 2);
    pCircle(ctx, bx - 16, by - 18 + shake, 5, "#FF1744", 1); // Angry red pupil
    pCircle(ctx, bx + 16, by - 18 + shake, 10, "#FFFFFF", 2);
    pCircle(ctx, bx + 16, by - 18 + shake, 5, "#FF1744", 1);

    // Angry Eyebrows (V-shape)
    pRect(ctx, bx - 26, by - 32 + shake, 18, 4, "#4A148C");
    pRect(ctx, bx + 8, by - 32 + shake, 18, 4, "#4A148C");

    // 4 Hungry Monster Mouths sprouting all over the brain champing open & shut!
    const mouthPositions = [
      { x: bx - 50, y: by - 35, phase: 0 },
      { x: bx + 50, y: by - 35, phase: 1.5 },
      { x: bx, y: by + 25, phase: 3.0 },
      { x: bx - 45, y: by + 15, phase: 4.5 },
    ];

    mouthPositions.forEach((m) => {
      const chomp = Math.sin(frame * 0.35 + m.phase) > 0;
      // Mouth background
      pCircle(ctx, m.x, m.y + shake, 14, "#4A148C", 2);
      pCircle(ctx, m.x, m.y + shake, chomp ? 11 : 4, "#FF1744", 1);
      // Sharp monster teeth!
      pRect(ctx, m.x - 8, m.y - 8 + shake, 4, 4, "#FFFFFF");
      pRect(ctx, m.x - 1, m.y - 8 + shake, 4, 4, "#FFFFFF");
      pRect(ctx, m.x + 6, m.y - 8 + shake, 4, 4, "#FFFFFF");
      pRect(ctx, m.x - 5, m.y + 4 + shake, 4, 4, "#FFFFFF");
      pRect(ctx, m.x + 2, m.y + 4 + shake, 4, 4, "#FFFFFF");
    });

    // Comic speech signs popping up: "WE WANT MORE!", "FEED US!"
    pRect(ctx, bx - 120, by - 80, 105, 24, "rgba(255, 23, 68, 0.95)");
    ctx.strokeStyle = "#FFFFFF";
    ctx.strokeRect(bx - 120, by - 80, 105, 24);
    ctx.fillStyle = "#FFFFFF";
    ctx.font = "8px monospace";
    ctx.fillText("FEED US! 👾", bx - 110, by - 65);

    pRect(ctx, bx + 20, by - 80, 105, 24, "rgba(255, 23, 68, 0.95)");
    ctx.strokeStyle = "#FFFFFF";
    ctx.strokeRect(bx + 20, by - 80, 105, 24);
    ctx.fillStyle = "#FFFFFF";
    ctx.font = "8px monospace";
    ctx.fillText("MORE! 💥", bx + 35, by - 65);

    // Mutation status banner
    pRect(ctx, bx - 100, by + 85, 200, 26, "rgba(10, 15, 28, 0.95)");
    ctx.strokeStyle = "#5CE1E6";
    ctx.lineWidth = 2;
    ctx.strokeRect(bx - 100, by + 85, 200, 26);
    ctx.fillStyle = "#5CE1E6";
    ctx.font = "8px monospace";
    ctx.fillText("MILLIONS OF HUNGRY LOCKS!👾", bx - 92, by + 102);
  }
}

// 4. Subtle Vignette & Scanlines
export function drawVignetteAndScanlines(ctx: CanvasRenderingContext2D) {
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

  ctx.fillStyle = "rgba(0, 0, 0, 0.10)";
  for (let y = 0; y < PH; y += 4) {
    ctx.fillRect(0, y, PW, 1);
  }
}
