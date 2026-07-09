#!/usr/bin/env python3
"""Generate placeholder textures for all items referenced in recipes."""
import os, re, hashlib
from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECIPES_DIR = os.path.join(BASE, 'src', 'data', 'recipes')
TEX_DIR = os.path.join(BASE, 'public', 'textures')

def color_from_id(name):
    h = int(hashlib.md5(name.encode()).hexdigest()[:6], 16)
    r = (h >> 16) & 0xFF
    g = (h >> 8) & 0xFF
    b = h & 0xFF
    if r + g + b < 180:
        r = min(255, r + 120)
        g = min(255, g + 120) 
        b = min(255, b + 120)
    return (r, g, b)

# Discover all item IDs from recipe files
all_items = set()

for fname in os.listdir(RECIPES_DIR):
    if not fname.endswith('.ts') or fname == 'helpers.ts':
        continue
    with open(os.path.join(RECIPES_DIR, fname)) as f:
        content = f.read()
    # Match full item IDs with mod prefix
    for m in re.finditer(r"'([a-z_]+:[a-z_0-9]+)'", content):
        all_items.add(m.group(1))
    # Also match vanilla items without mod prefix in context
    for m in re.finditer(r"'minecraft:([a-z_]+)'", content):
        pass  # already covered by above

print(f"Found {len(all_items)} unique item IDs in recipes")

# Generate textures
generated = 0
existing = 0
for item_id in sorted(all_items):
    if ':' not in item_id:
        continue
    mod, item_name = item_id.split(':', 1)
    if not item_name:
        continue
    
    dir_path = os.path.join(TEX_DIR, mod)
    os.makedirs(dir_path, exist_ok=True)
    
    tex_path = os.path.join(dir_path, f'{item_name}.png')
    if not os.path.exists(tex_path):
        r, g, b = color_from_id(item_id)
        img = Image.new('RGBA', (16, 16), (r, g, b, 255))
        # Add subtle pattern - border
        for x in range(16):
            for y in range(16):
                if x == 0 or x == 15 or y == 0 or y == 15:
                    dr = max(0, int(r * 0.7))
                    dg = max(0, int(g * 0.7))
                    db = max(0, int(b * 0.7))
                    img.putpixel((x, y), (dr, dg, db, 255))
        # Center cross pattern
        img.putpixel((7, 7), (min(255, r+30), min(255, g+30), min(255, b+30), 255))
        img.putpixel((8, 7), (min(255, r+30), min(255, g+30), min(255, b+30), 255))
        img.putpixel((7, 8), (min(255, r+30), min(255, g+30), min(255, b+30), 255))
        img.putpixel((8, 8), (min(255, r+30), min(255, g+30), min(255, b+30), 255))
        img.save(tex_path)
        generated += 1
    else:
        existing += 1

print(f"Generated {generated} new textures, {existing} already existed")
