#!/usr/bin/env python3
"""Generate 10 mod recipe TypeScript files for MithCraft Calculator."""

import os, hashlib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECIPE_DIR = os.path.join(BASE, 'src', 'data', 'recipes')
TEX_DIR = os.path.join(BASE, 'public', 'textures')

def color_from_id(item_id):
    h = int(hashlib.md5(item_id.encode()).hexdigest()[:6], 16)
    r = (h >> 16) & 0xFF
    g = (h >> 8) & 0xFF
    b = h & 0xFF
    if r + g + b < 200:
        r = min(255, r + 100)
        g = min(255, g + 100)
        b = min(255, b + 100)
    return f'{r:02X}{g:02X}{b:02X}'

def short_from_id(item_id):
    name = item_id.split(':')[-1]
    parts = name.replace('_', ' ').split()
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()

def gen_shaped(id, results, pattern, key):
    """Generate shaped recipe entry"""
    ings = {k: v for k, v in key.items() if v != 'minecraft:air'}
    ings_str = ', '.join(f"ing('{v}')" for k, v in ings.items())
    return f"""  r('{id}', 'crafting', '{id.split(':')[0]}', [res('{id}'{', ' + str(results) if results > 1 else ''})],
    [{', '.join(f"ing('{v}')" for k, v in ings.items())}], {{ pattern: {pattern_str(pattern)}, key: {{ {', '.join(f"{k}: ing('{v}')" for k, v in ings.items())} }} }}),"""

def pattern_str(pattern):
    return '[' + ', '.join(f"'{row}'" for row in pattern) + ']'

def gen_shapeless(id, results, ingredients):
    """Generate shapeless recipe entry"""
    ings_str = ', '.join(f"ing('{i}')" for i in ingredients)
    return f"""  r('{id}', 'crafting', '{id.split(':')[0]}', [res('{id}'{', ' + str(results) if results > 1 else ''})],
    [{ings_str}]),"""

# ─── MOD DATA ──────────────────────────────────────────────────────────

ALL_ITEMS = {}  # full_id -> {name, color, mod}
ALL_RECIPES = {}  # mod_id -> [recipe strings]

MOD_NAMES = {
    'ironchest': 'Iron Chests',
    'pylon': 'Pylon',
    'prefab': 'Prefab',
    'storagenetwork': 'Simple Storage Network',
    'sophisticatedstorage': 'Sophisticated Storage',
    'sophisticatedbackpacks': 'Sophisticated Backpacks',
    'farmersdelight': "Farmer's Delight",
    'mysticalagriculture': 'Mystical Agriculture',
    'rootsclassic': 'Roots Classic',
    'irons_spellbooks': "Iron's Spells 'n Spellbooks",
}

MOD_COLORS = {
    'ironchest': '#C0C0C0',
    'pylon': '#00BFFF',
    'prefab': '#D4A574',
    'storagenetwork': '#4A90D9',
    'sophisticatedstorage': '#A0522D',
    'sophisticatedbackpacks': '#8B4513',
    'farmersdelight': '#5B8C2A',
    'mysticalagriculture': '#7B2DB5',
    'rootsclassic': '#2D8B4E',
    'irons_spellbooks': '#DC143C',
}

def add(mod, item_id, name, color=None):
    full = f'{mod}:{item_id}'
    ALL_ITEMS[full] = {
        'name': name,
        'color': color or color_from_id(full),
        'mod': mod
    }
    return full

def shaped(mod, out, count, pattern, keys):
    """out: item_id, count: int, pattern: list of strings, keys: dict char->full_id"""
    full = f'{mod}:{out}'
    if mod not in ALL_RECIPES:
        ALL_RECIPES[mod] = []
    ings_str = ', '.join(f"ing('{v}')" for v in keys.values())
    pat_str = pattern_str(pattern)
    key_str = ', '.join(f"{k}: ing('{v}')" for k, v in keys.items())
    ALL_RECIPES[mod].append(
        f"  r('{full}', 'crafting', '{mod}', [res('{full}'{', ' + str(count) if count > 1 else ''})],\n"
        f"    [{ings_str}], {{ pattern: {pat_str}, key: {{ {key_str} }} }}),"
    )

def shapeless(mod, out, count, *ingredients):
    full = f'{mod}:{out}'
    if mod not in ALL_RECIPES:
        ALL_RECIPES[mod] = []
    ings_str = ', '.join(f"ing('{i}')" for i in ingredients)
    ALL_RECIPES[mod].append(
        f"  r('{full}', 'crafting', '{mod}', [res('{full}'{', ' + str(count) if count > 1 else ''})],\n"
        f"    [{ings_str}]),"
    )

# ═══════════════════════════════════════════
# 1. IRON CHESTS
# ═══════════════════════════════════════════
m = 'ironchest'
add(m, 'iron_chest', 'Iron Chest', 'C0C0C0')
add(m, 'gold_chest', 'Gold Chest', 'FFD700')
add(m, 'diamond_chest', 'Diamond Chest', '00FFFF')
add(m, 'crystal_chest', 'Crystal Chest', 'ADD8E6')
add(m, 'obsidian_chest', 'Obsidian Chest', '3C3C3C')
add(m, 'copper_chest', 'Copper Chest', 'FF8C00')
add(m, 'silver_chest', 'Silver Chest', 'E0E0E0')

shaped(m, 'iron_chest', 1, ['AAA', 'A A', 'AAA'], {'A': 'minecraft:iron_ingot'})
shaped(m, 'copper_chest', 1, ['AAA', 'ABA', 'AAA'], {'A': 'minecraft:copper_ingot', 'B': 'minecraft:chest'})
shaped(m, 'gold_chest', 1, ['AAA', 'ABA', 'AAA'], {'A': 'minecraft:gold_ingot', 'B': f'{m}:iron_chest'})
shaped(m, 'silver_chest', 1, ['AAA', 'ABA', 'AAA'], {'A': 'minecraft:iron_ingot', 'B': f'{m}:copper_chest'})
shaped(m, 'diamond_chest', 1, ['AAA', 'ABA', 'AAA'], {'A': 'minecraft:diamond', 'B': f'{m}:gold_chest'})
shaped(m, 'crystal_chest', 1, ['ABA', 'BCB', 'ABA'], {'A': 'minecraft:glass', 'B': 'minecraft:obsidian', 'C': f'{m}:diamond_chest'})
shaped(m, 'obsidian_chest', 1, ['AAA', 'ABA', 'AAA'], {'A': 'minecraft:obsidian', 'B': f'{m}:diamond_chest'})

# Write files
print("Generating recipe files...")
for mod_id in MOD_NAMES:
    lines = [f"// {MOD_NAMES[mod_id]} recipes"]
    lines.append("import { r, res, ing } from './helpers';")
    lines.append("import type { Recipe } from '../../types';")
    lines.append("")
    lines.append(f"const R: Recipe[] = [")
    
    if mod_id in ALL_RECIPES:
        for r in ALL_RECIPES[mod_id]:
            lines.append(r)
    
    lines.append("];")
    lines.append("")
    lines.append(f"export default R;")
    
    filepath = os.path.join(RECIPE_DIR, f"{mod_id}.ts")
    with open(filepath, 'w') as f:
        f.write('\n'.join(lines))
    print(f"  ✓ {mod_id}.ts ({len(ALL_RECIPES.get(mod_id,[]))} recettes)")

# Generate texture placeholders
print("\nGenerating texture placeholders...")
from PIL import Image
count = 0
for full_id, info in ALL_ITEMS.items():
    mod = info['mod']
    item_name = full_id.split(':')[1]
    dir_path = os.path.join(TEX_DIR, mod)
    os.makedirs(dir_path, exist_ok=True)
    
    tex_path = os.path.join(dir_path, f'{item_name}.png')
    if not os.path.exists(tex_path):
        # Generate a small colored texture
        color = info['color']
        r, g, b = int(color[:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        img = Image.new('RGBA', (16, 16), (r, g, b, 255))
        # Add subtle pattern - darker border
        for x in range(16):
            for y in range(16):
                if x == 0 or x == 15 or y == 0 or y == 15:
                    dr, dg, db = int(r * 0.7), int(g * 0.7), int(b * 0.7)
                    img.putpixel((x, y), (dr, dg, db, 255))
        img.save(tex_path)
        count += 1

print(f"  ✓ {count} nouvelles textures générées")
print(f"  ✓ Total: {len(ALL_ITEMS)} items dans 10 mods")

# Generate item-defs.ts additions
print("\nItem definitions to add to item-defs.ts:")
print("Add the following items to the 'items' array:")
for full_id, info in sorted(ALL_ITEMS.items()):
    short = short_from_id(full_id)
    print(f"  {{ id: '{full_id}', name: '{info['name']}', mod: '{info['mod']}', short: '{short}', color: '#{info['color']}', tier: 'common', tags: [] }},")

print("\nAdd the following mods to MODS array:")
for mod_id, name in MOD_NAMES.items():
    icon = list(ALL_ITEMS.keys())[0].split(':')[1]  # not great
    print(f"  {{ id: '{mod_id}', name: '{name}', color: '{MOD_COLORS[mod_id]}', icon: '{mod_id}:{list(k for k in ALL_ITEMS if k.startswith(mod_id+':'))[0].split(':')[1]}' }},")
