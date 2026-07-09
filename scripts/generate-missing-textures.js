const fs = require('fs');
const path = require('path');
const { createCanvas } = require('canvas');

// 1. Collect existing texture files
const textureFiles = new Set();
function walk(dir, base) {
  if (!fs.existsSync(dir)) return;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    if (e.isDirectory()) walk(path.join(dir, e.name), path.join(base, e.name));
    else if (e.name.endsWith('.png')) {
      textureFiles.add(path.join(base, e.name).replace('public/textures/', ''));
    }
  }
}
walk('public/textures', 'public/textures');
console.log('Existing texture files:', textureFiles.size);

// 2. Collect all item IDs
const recipeFiles = ['vanilla.ts', 'create.ts', 'mekanism.ts', 'mekanism-processing.ts', 'thermal.ts', 'thermal-processing.ts', 'ae2.ts', 'ic2.ts'];
let content = '';
for (const f of recipeFiles) {
  const p = 'src/data/recipes/' + f;
  if (fs.existsSync(p)) content += fs.readFileSync(p, 'utf8') + '\n';
}

const allRefs = new Set();
const matches = content.match(/[a-z_]+:[a-z_0-9]+/g) || [];
for (const m of matches) {
  const id = m;
  if (!id.match(/recipes?/) && !id.includes('recipe') && !id.includes('_smelt') && !id.includes('_blast') && !id.match(/_[a-z]+_from_/)) {
    allRefs.add(id);
  }
}

// Also include items from item-defs.ts
const itemDefs = fs.readFileSync('src/data/item-defs.ts', 'utf8');
const defMatches = itemDefs.match(/'([a-z_]+:[a-z_0-9_]+)'/g) || [];
for (const m of defMatches) {
  const id = m.replace(/'/g, '');
  if (id !== 'id') allRefs.add(id);
}

// 3. Simple hash to color
function hashColor(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
  }
  const h = ((hash % 360) + 360) % 360;
  const s = 40 + (hash % 30);
  const l = 35 + (hash % 20);
  return { h, s, l };
}

// 4. Generate missing textures
let generated = 0;
let skipped = 0;

for (const id of allRefs) {
  if (id.startsWith('energy:') || id.startsWith('fluid:')) {
    skipped++;
    continue;
  }

  const [mod, ...rest] = id.split(':');
  const itemName = rest.join(':');
  const convPath = mod + '/' + itemName + '.png';
  const fullPath = 'public/textures/' + convPath;

  if (textureFiles.has(convPath)) {
    skipped++;
    continue;
  }

  // Check if already exists at this path
  if (fs.existsSync(fullPath)) {
    skipped++;
    continue;
  }

  // Create directory if needed
  const dir = path.dirname(fullPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  // Generate a 16x16 colored placeholder
  try {
    const canvas = createCanvas(16, 16);
    const ctx = canvas.getContext('2d');

    const { h, s, l } = hashColor(id);
    // Fill with main color
    ctx.fillStyle = `hsl(${h}, ${s}%, ${l}%)`;
    ctx.fillRect(0, 0, 16, 16);

    // Add a subtle pattern - cross/diamond highlight
    ctx.fillStyle = `hsl(${h}, ${s}%, ${Math.min(l + 15, 70)}%)`;
    ctx.fillRect(2, 2, 4, 4);
    ctx.fillRect(10, 2, 4, 4);
    ctx.fillRect(2, 10, 4, 4);
    ctx.fillRect(10, 10, 4, 4);

    // Darker center accent
    ctx.fillStyle = `hsl(${h}, ${s}%, ${Math.max(l - 10, 15)}%)`;
    ctx.fillRect(6, 6, 4, 4);

    const buf = canvas.toBuffer('image/png');
    fs.writeFileSync(fullPath, buf);
    generated++;
  } catch (err) {
    console.error('Failed to generate texture for', id, ':', err.message);
  }
}

console.log(`Generated ${generated} new placeholder textures`);
console.log(`Skipped ${skipped} items (already have textures or skipped types)`);
