#!/usr/bin/env python3
"""Generate colored placeholder PNG textures for ALL items in recipes + texture map."""
import os, struct, zlib, re

PUB = os.path.join(os.path.dirname(__file__), '..', 'public', 'textures')
SRC = os.path.join(os.path.dirname(__file__), '..', 'src')

# Read existing TEXTURE_MAP from texture-resolver.ts
texture_file = os.path.join(SRC, 'utils', 'texture-resolver.ts')
texture_map = {}
with open(texture_file) as f:
    for m in re.finditer(r"'([^']+)':\s+'([^']+)'", f.read()):
        texture_map[m.group(1)] = m.group(2)

# Collect all item IDs from recipe files
recipe_dir = os.path.join(SRC, 'data', 'recipes')
all_items = set()
for fn in os.listdir(recipe_dir):
    if not fn.endswith('.ts'): continue
    content = open(os.path.join(recipe_dir, fn)).read()
    # Match all r('mod:id'...)
    for m in re.findall(r"\br\('([^']+)'", content):
        mod, item = m.split(':', 1)
        all_items.add(m)
    # Also match ingredients ing('mod:id'...) and key items
    for m in re.findall(r"ing\('([^']+)'", content):
        all_items.add(m)

# Also collect from texture map
for item_id in texture_map:
    all_items.add(item_id)

print(f"Total unique items: {len(all_items)}")
print(f"In texture map: {len(texture_map)}")

# Generate a deterministic color for each item
def hex_color(name):
    h = 0
    for c in name: h = (h * 31 + ord(c)) & 0xffffffff
    hues = [0, 25, 45, 80, 130, 180, 210, 260, 300, 330]
    hue = hues[abs(h) % len(hues)]
    sat = 35 + (abs(h) % 3) * 5
    light = 45 + (abs(h) % 4) * 5
    # Convert HSL to RGB (simplified)
    h = hue / 360.0
    s = sat / 100.0
    l = light / 100.0
    def hue2rgb(p, q, t):
        if t < 0: t += 1
        if t > 1: t -= 1
        if t < 1/6: return p + (q - p) * 6 * t
        if t < 1/2: return q
        if t < 2/3: return p + (q - p) * (2/3 - t) * 6
        return p
    q = l * (1 + s) if l < 0.5 else l + s - l * s
    p = 2 * l - q
    r = round(hue2rgb(p, q, h + 1/3) * 255)
    g = round(hue2rgb(p, q, h) * 255)
    b = round(hue2rgb(p, q, h - 1/3) * 255)
    return r, g, b

def create_png(path, r, g, b):
    """Create a simple 16x16 PNG with colored background + checkerboard pattern."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # 16x16 RGBA
    pixels = bytearray()
    for y in range(16):
        for x in range(16):
            # Checkerboard effect
            check = (x // 2 + y // 2) % 2
            if check:
                pr = min(255, r + 20)
                pg = min(255, g + 20)
                pb = min(255, b + 20)
            else:
                pr = max(0, r - 10)
                pg = max(0, g - 10)
                pb = max(0, b - 10)
            # 8px inner border highlight
            if 2 <= x <= 13 and 2 <= y <= 13:
                # Inner area slightly lighter
                pr = min(255, pr + 15)
                pg = min(255, pg + 15)
                pb = min(255, pb + 15)
            # Cross highlight at center
            if x == 8 or y == 8:
                pr = min(255, r + 40)
                pg = min(255, g + 40)
                pb = min(255, b + 40)
            pixels.extend([pr, pg, pb, 255])
    
    # Write PNG
    def chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(struct.pack('>I', 13) + b'IHDR' + struct.pack('>IIBBBBB', 16, 16, 8, 6, 0, 0, 0) + struct.pack('>I', zlib.crc32(b'IHDR' + struct.pack('>IIBBBBB', 16, 16, 8, 6, 0, 0, 0)) & 0xffffffff))
        compressed = zlib.compress(bytes(pixels))
        f.write(struct.pack('>I', len(compressed)) + b'IDAT' + compressed + struct.pack('>I', zlib.crc32(b'IDAT' + compressed) & 0xffffffff))
        f.write(struct.pack('>I', 0) + b'IEND' + struct.pack('>I', zlib.crc32(b'IEND') & 0xffffffff))

generated = 0
existing = 0
new_entries = 0

# 1. Generate textures for all known TEXTURE_MAP entries (mostly already exist)
for item_id, rel_path in texture_map.items():
    full_path = os.path.join(PUB, rel_path)
    if os.path.exists(full_path):
        existing += 1
        continue
    name = item_id.split(':')[-1]
    r, g, b = hex_color(name)
    create_png(full_path, r, g, b)
    generated += 1

# 2. Generate textures for items NOT in texture_map
#    Add new entries to a set to report to user
new_items = []
for item_id in sorted(all_items):
    if item_id in texture_map:
        continue
    mod = item_id.split(':')[0]
    name = item_id.split(':')[-1]
    rel_path = f"{mod}/{name}.png"
    full_path = os.path.join(PUB, rel_path)
    if os.path.exists(full_path):
        existing += 1
        continue
    r, g, b = hex_color(name)
    create_png(full_path, r, g, b)
    generated += 1
    new_items.append((item_id, rel_path))

print(f"Existing textures: {existing}")
print(f"Generated: {generated}")
print(f"New items (not in TEXTURE_MAP): {len(new_items)}")
if new_items:
    print("Sample new items:")
    for item, path in new_items[:10]:
        print(f"  {item} → {path}")

# 3. Update texture-resolver.ts with new entries
if new_items:
    with open(texture_file) as f:
        content = f.read()
    # Add new entries before the closing } of TEXTURE_MAP
    insert_pos = content.rfind('};')
    if insert_pos > 0:
        additions = '\n'.join(f"  '{item_id}': '{rel_path}'," for item_id, rel_path in new_items)
        new_content = content[:insert_pos] + '\n' + additions + '\n' + content[insert_pos:]
        with open(texture_file, 'w') as f:
            f.write(new_content)
        new_entries = len(new_items)
        print(f"Added {new_entries} entries to texture-resolver.ts")

print(f"\nDone. Total textures: {existing + generated}")
