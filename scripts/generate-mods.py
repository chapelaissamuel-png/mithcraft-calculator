#!/usr/bin/env python3
"""Generate Mod recipe files + textures for 10 mods."""

import os, json, hashlib, struct
from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECIPES_DIR = os.path.join(BASE, 'src', 'data', 'recipes')
TEXTURES_DIR = os.path.join(BASE, 'public', 'textures')
ITEM_DEFS = os.path.join(BASE, 'src', 'data', 'item-defs.ts')

# ─── COLOR PALETTE ─────────────────────────────────────────────────────
# Deterministic color from item_id
def color_from_id(item_id):
    h = int(hashlib.md5(item_id.encode()).hexdigest()[:6], 16)
    r = (h >> 16) & 0xFF
    g = (h >> 8) & 0xFF
    b = h & 0xFF
    # Ensure minimum brightness
    if r + g + b < 200:
        r = min(255, r + 100)
        g = min(255, g + 100)
        b = min(255, b + 100)
    return f'{r:02X}{g:02X}{b:02X}'

def short_from_id(item_id):
    name = item_id.split(':')[-1] if ':' in item_id else item_id
    parts = name.replace('_', ' ').split()
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()

# ─── MOD DATA ──────────────────────────────────────────────────────────

RECIPES = {}

# Helper to add items
def add_items(mod, items_list):
    if mod not in RECIPES:
        RECIPES[mod] = {'items': {}, 'recipes': []}
    for item_id, name, color in items_list:
        full_id = f'{mod}:{item_id}'
        RECIPES[mod]['items'][full_id] = {
            'mod': mod,
            'name': name,
            'color': color,
            'short': short_from_id(full_id)
        }

# Helper to add shaped recipe
def shaped(mod, out_id, out_count, pattern, keys):
    full_id = f'{mod}:{out_id}'
    ingredients = []
    for k, v in keys.items():
        if isinstance(v, list):
            ingredients.extend(v)
        else:
            ingredients.append(v)
    RECIPES[mod]['recipes'].append({
        'output': full_id,
        'count': out_count,
        'type': 'shaped',
        'pattern': pattern,
        'keys': keys,
        'ingredients': ingredients
    })

# Helper to add shapeless recipe
def shapeless(mod, out_id, out_count, *ingredients):
    full_id = f'{mod}:{out_id}'
    RECIPES[mod]['recipes'].append({
        'output': full_id,
        'count': out_count,
        'type': 'shapeless',
        'ingredients': list(ingredients)
    })

# ═══════════════════════════════════════════
# 1. Farmer's Delight
# ═══════════════════════════════════════════
fd = 'farmersdelight'
add_items(fd, [
    ('stove', 'Stove', '8B4513'),
    ('cooking_pot', 'Cooking Pot', '4A4A4A'),
    ('skillet', 'Skillet', '4A4A4A'),
    ('cutting_board', 'Cutting Board', 'D2B48C'),
    ('knife_flint', 'Flint Knife', '808080'),
    ('knife_iron', 'Iron Knife', 'C0C0C0'),
    ('knife_gold', 'Gold Knife', 'FFD700'),
    ('knife_diamond', 'Diamond Knife', '00FFFF'),
    ('knife_netherite', 'Netherite Knife', '3C3C3C'),
    ('ham', 'Ham', 'CD5C5C'),
    ('smoked_ham', 'Smoked Ham', '8B0000'),
    ('honey_glazed_ham', 'Honey Glazed Ham', 'DAA520'),
    ('cabbage', 'Cabbage', '98FB98'),
    ('cabbage_leaf', 'Cabbage Leaf', '90EE90'),
    ('cabbage_roll', 'Cabbage Roll', '9ACD32'),
    ('tomato', 'Tomato', 'FF6347'),
    ('onion', 'Onion', 'FFD700'),
    ('rice', 'Rice', 'F5F5DC'),
    ('cooked_rice', 'Cooked Rice', 'FFF8DC'),
    ('fried_rice', 'Fried Rice', 'F5DEB3'),
    ('rice_roll', 'Rice Roll', 'F5F5DC'),
    ('chicken_sandwich', 'Chicken Sandwich', 'DEB887'),
    ('egg_sandwich', 'Egg Sandwich', 'FFE4B5'),
    ('bacon_sandwich', 'Bacon Sandwich', 'CD853F'),
    ('mutton_wrap', 'Mutton Wrap', '8FBC8F'),
    ('dog_food', 'Dog Food', '8B4513'),
    ('horse_feed', 'Horse Feed', 'DAA520'),
    ('roast_chicken', 'Roast Chicken', 'D2691E'),
    ('shepherds_pie', "Shepherd's Pie", 'D2B48C'),
    ('steak_and_potatoes', 'Steak and Potatoes', '8B4513'),
    ('stuffed_pumpkin', 'Stuffed Pumpkin', 'FF8C00'),
    ('baked_cod_stew', 'Baked Cod Stew', 'DAA520'),
    ('noodle_soup', 'Noodle Soup', 'FFE4B5'),
    ('pumpkin_soup', 'Pumpkin Soup', 'FF8C00'),
    ('tomato_soup', 'Tomato Soup', 'FF6347'),
    ('cake_slice', 'Cake Slice', 'FFE4C4'),
    ('apple_pie', 'Apple Pie', 'DAA520'),
    ('sweet_berry_cheesecake', 'Sweet Berry Cheesecake', 'DC143C'),
    ('chocolate_pie', 'Chocolate Pie', '8B4513'),
    ('raw_pasta', 'Raw Pasta', 'F5DEB3'),
    ('beef_stroganoff', 'Beef Stroganoff', '8B4513'),
    ('chicken_soup', 'Chicken Soup', 'FFE4B5'),
    ('fish_stew', 'Fish Stew', '4682B4'),
    ('fried_egg', 'Fried Egg', 'FFFACD'),
    ('minced_beef', 'Minced Beef', 'CD5C5C'),
    ('beef_patty', 'Beef Patty', '8B4513'),
    ('chicken_cuts', 'Chicken Cuts', 'FFE4B5'),
    ('bacon', 'Bacon', 'CD853F'),
    ('cod_slice', 'Cod Slice', 'F0F0F0'),
    ('salmon_slice', 'Salmon Slice', 'FFA07A'),
    ('mutton_chops', 'Mutton Chops', 'CD853F'),
    ('dumplings', 'Dumplings', 'F5DEB3'),
    ('stuffed_potato', 'Stuffed Potato', 'D2B48C'),
    ('wild_cabbages', 'Wild Cabbages', '98FB98'),
    ('onion', 'Onion', 'FFD700'),
    ('wild_onions', 'Wild Onions', 'FFD700'),
    ('wild_tomatoes', 'Wild Tomatoes', 'FF6347'),
    ('wild_rice', 'Wild Rice', 'F5F5DC'),
    ('rope', 'Rope', 'D2B48C'),
    ('canvas', 'Canvas', 'F5F5DC'),
    ('safety_net', 'Safety Net', 'D2B48C'),
    ('rich_soil', 'Rich Soil', '3C2F1A'),
    ('organic_compost', 'Organic Compost', '5C4033'),
    ('tree_fertilizer', 'Tree Fertilizer', '228B22'),
    ('pie_crust', 'Pie Crust', 'D2B48C'),
    ('dough', 'Dough', 'F5DEB3'),
    ('nether_wart_stew', 'Nether Wart Stew', '800080'),
    ('glow_berry_custard', 'Glow Berry Custard', 'FFD700'),
])

# Knives
shaped(fd, 'knife_flint', 1, 'AB\nC ', {'A': 'minecraft:flint', 'B': 'minecraft:stick', 'C': 'minecraft:string'})
shaped(fd, 'knife_iron', 1, 'AB\nC ', {'A': 'minecraft:iron_ingot', 'B': 'minecraft:stick', 'C': 'minecraft:string'})
shaped(fd, 'knife_gold', 1, 'AB\nC ', {'A': 'minecraft:gold_ingot', 'B': 'minecraft:stick', 'C': 'minecraft:string'})
shaped(fd, 'knife_diamond', 1, 'AB\nC ', {'A': 'minecraft:diamond', 'B': 'minecraft:stick', 'C': 'minecraft:string'})
shaped(fd, 'knife_netherite', 1, 'AB\nC ', {'A': 'minecraft:netherite_ingot', 'B': 'minecraft:stick', 'C': 'minecraft:string'})
# Workstations
shaped(fd, 'stove', 1, 'AA\nBC', {'A': 'minecraft:iron_ingot', 'B': 'minecraft:brick', 'C': 'minecraft:brick'})
shaped(fd, 'cooking_pot', 1, 'ABA\nACA', {'A': 'minecraft:brick', 'B': 'minecraft:iron_ingot', 'C': 'minecraft:iron_ingot'})
shaped(fd, 'skillet', 1, ' AA\n BA\nC  ', {'A': 'minecraft:iron_ingot', 'B': 'minecraft:iron_ingot', 'C': 'minecraft:stick'})
shaped(fd, 'cutting_board', 1, 'AA\nBC', {'A': 'minecraft:oak_log', 'B': 'minecraft:stick', 'C': 'minecraft:stick'})
# Materials
shaped(fd, 'canvas', 1, 'AA\nAA', {'A': 'minecraft:string'})
shaped(fd, 'dough', 1, 'AA\n B', {'A': 'minecraft:wheat', 'B': 'minecraft:water_bucket'})
shaped(fd, 'pie_crust', 1, 'AA\n A', {'A': 'dough'})
shaped(fd, 'rope', 2, ' A\n B\n A', {'A': 'canvas', 'B': 'canvas'})
shaped(fd, 'safety_net', 1, 'AAA\nABA\nAAA', {'A': 'rope', 'B': 'minecraft:air'})
shapeless(fd, 'rich_soil', 1, 'minecraft:dirt', 'organic_compost')
shapeless(fd, 'organic_compost', 1, 'minecraft:rotten_flesh', 'minecraft:wheat', 'minecraft:wheat')
shapeless(fd, 'tree_fertilizer', 1, 'organic_compost', 'minecraft:bone_meal', 'minecraft:sugar')
# Food processing
shapeless(fd, 'ham', 1, 'minecraft:porkchop', 'minecraft:porkchop', 'minecraft:porkchop')
shapeless(fd, 'minced_beef', 1, 'minecraft:beef')
shapeless(fd, 'beef_patty', 1, 'minced_beef')
shapeless(fd, 'bacon', 1, 'minecraft:porkchop')
shapeless(fd, 'chicken_cuts', 1, 'minecraft:chicken')
shapeless(fd, 'mutton_chops', 1, 'minecraft:mutton')
shapeless(fd, 'cod_slice', 1, 'minecraft:cod')
shapeless(fd, 'salmon_slice', 1, 'minecraft:salmon')
shapeless(fd, 'fried_egg', 1, 'minecraft:egg')
shapeless(fd, 'cabbage', 1, 'wild_cabbages')
shapeless(fd, 'cabbage_leaf', 2, 'cabbage')
shapeless(fd, 'cooked_rice', 1, 'rice')
# Meals
shapeless(fd, 'cabbage_roll', 1, 'cabbage_leaf', 'minced_beef', 'cooked_rice')
shapeless(fd, 'fried_rice', 1, 'cooked_rice', 'minecraft:egg', 'minecraft:carrot')
shapeless(fd, 'rice_roll', 1, 'cooked_rice', 'salmon_slice')
shapeless(fd, 'chicken_sandwich', 1, 'minecraft:bread', 'chicken_cuts', 'cabbage_leaf')
shapeless(fd, 'egg_sandwich', 1, 'minecraft:bread', 'fried_egg')
shapeless(fd, 'bacon_sandwich', 1, 'minecraft:bread', 'bacon', 'cabbage_leaf')
shapeless(fd, 'mutton_wrap', 1, 'cabbage_leaf', 'mutton_chops', 'cooked_rice')
shapeless(fd, 'dog_food', 1, 'minced_beef', 'minecraft:rotten_flesh')
shapeless(fd, 'horse_feed', 1, 'minecraft:apple', 'minecraft:golden_carrot', 'minecraft:hay_block')
shapeless(fd, 'roast_chicken', 1, 'minecraft:cooked_chicken', 'minecraft:carrot', 'minecraft:baked_potato')
shapeless(fd, 'shepherds_pie', 1, 'minced_beef', 'minecraft:baked_potato', 'onion')
shapeless(fd, 'steak_and_potatoes', 1, 'minecraft:cooked_beef', 'minecraft:baked_potato')
shapeless(fd, 'pumpkin_soup', 1, 'minecraft:pumpkin', 'minecraft:milk_bucket')
shapeless(fd, 'tomato_soup', 1, 'tomato', 'tomato')
shapeless(fd, 'noodle_soup', 1, 'raw_pasta', 'minecraft:carrot')
shapeless(fd, 'chicken_soup', 1, 'chicken_cuts', 'minecraft:carrot', 'minecraft:potato')
shapeless(fd, 'fish_stew', 1, 'cod_slice', 'minecraft:potato')
shapeless(fd, 'beef_stroganoff', 1, 'minecraft:cooked_beef', 'minecraft:mushroom')
shapeless(fd, 'baked_cod_stew', 1, 'cod_slice', 'minecraft:baked_potato')
shapeless(fd, 'dumplings', 1, 'dough', 'minced_beef', 'cabbage_leaf')
shapeless(fd, 'stuffed_potato', 1, 'minecraft:baked_potato', 'minced_beef')
shapeless(fd, 'nether_wart_stew', 1, 'minecraft:nether_wart')
shapeless(fd, 'glow_berry_custard', 1, 'minecraft:glow_berries', 'minecraft:milk_bucket', 'minecraft:egg')
# Desserts
shaped(fd, 'apple_pie', 1, 'AAA\n B ', {'A': 'minecraft:apple', 'B': 'pie_crust'})
shaped(fd, 'sweet_berry_cheesecake', 1, 'AAA\n B ', {'A': 'minecraft:sweet_berries', 'B': 'pie_crust'})
shaped(fd, 'chocolate_pie', 1, 'AAA\n B ', {'A': 'minecraft:cocoa_beans', 'B': 'pie_crust'})
shapeless(fd, 'cake_slice', 1, 'pie_crust', 'minecraft:milk_bucket', 'minecraft:sugar')
shapeless(fd, 'stuffed_pumpkin', 1, 'minecraft:pumpkin', 'cooked_rice', 'minced_beef')
shapeless(fd, 'honey_glazed_ham', 1, 'ham', 'minecraft:honey_bottle')
shapeless(fd, 'smoked_ham', 1, 'ham')

print(f"Farmer's Delight: {len(RECIPES[fd]['items'])} items, {len(RECIPES[fd]['recipes'])} recipes")

# Continue with remaining mods in next files...
# For now, save the script state
import json
with open(os.path.join(BASE, 'scripts', '_recipe_data.json'), 'w') as f:
    data = {}
    for mod_id, mod_data in RECIPES.items():
        data[mod_id] = {
            'items': {k: v for k, v in mod_data['items'].items()},
            'recipes': mod_data['recipes']
        }
    json.dump(data, f, indent=2)

print(f"Saved recipe data for {len(RECIPES)} mods to _recipe_data.json")
