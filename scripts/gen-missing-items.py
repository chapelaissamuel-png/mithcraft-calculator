#!/usr/bin/env python3
"""Generate missing item definitions for ALL items referenced in recipes.

1. Scans all recipe files for item IDs
2. Reads existing item-defs.ts
3. For each missing item, generates a def with auto-name, color, etc.
4. Outputs the complete new item-defs.ts
"""
import re
import json
import colorsys
from pathlib import Path
from collections import defaultdict, OrderedDict

RECIPES_DIR = Path('src/data/recipes')
ITEM_DEFS_FILE = Path('src/data/item-defs.ts')

# ─── Parse recipe files for item IDs ───────────────────────────
all_item_ids = set()
recipe_source_for_item = defaultdict(set)  # item_id -> which recipe files

for f in sorted(RECIPES_DIR.glob('*.ts')):
    if f.name == 'helpers.ts':
        continue
    text = f.read_text()
    # Find all item references in helpers
    items = re.findall(r"(?:ing|res)\('([^']+)'", text)
    for item_id in items:
        all_item_ids.add(item_id)
        recipe_source_for_item[item_id].add(f.name.replace('.ts', ''))

# Also check for items in the key dict patterns
for f in sorted(RECIPES_DIR.glob('*.ts')):
    if f.name == 'helpers.ts':
        continue
    text = f.read_text()
    items = re.findall(r"key\s*:\s*\{[^}]+\}", text, re.DOTALL)
    # These are complex; the simpler regex above usually catches them via the ing() wrapper
    # But also catch direct item refs in key blocks
    items2 = re.findall(r"item:\s*'([^']+)'", text)
    for item_id in items2:
        all_item_ids.add(item_id)

print(f"Total unique item IDs in recipes: {len(all_item_ids)}")

# ─── Parse existing item-defs.ts ────────────────────────────────
existing_items = set()
mod_sections = OrderedDict()
current_mod = None
current_section_lines = []
mod_var_names = {}  # var_name -> mod_id_lower

def extract_mod_entries(text):
    """Parse item-defs.ts into mod sections."""
    result = OrderedDict()
    lines = text.split('\n')
    current_var = None
    current_lines = []
    in_mod_section = False
    
    for line in lines:
        m = re.match(r'^const (\w+): RawDef', line)
        if m:
            if current_var and current_lines:
                result[current_var] = '\n'.join(current_lines)
            current_var = m.group(1)
            current_lines = [line]
            in_mod_section = True
            continue
        
        if line.strip().startswith('] as RawDef;'):
            if current_var and in_mod_section:
                current_lines.append(line)
                result[current_var] = '\n'.join(current_lines)
                current_var = None
                current_lines = []
                in_mod_section = False
            continue
        
        if current_var:
            current_lines.append(line)
    
    return result

with open(ITEM_DEFS_FILE) as f:
    existing_content = f.read()

# Find all items defined in the file
for line in existing_content.split('\n'):
    m = re.match(r"\s*\['([^']+)',\s*'([^']+)'", line)
    if m:
        existing_items.add(m.group(1))

print(f"Existing item definitions: {len(existing_items)}")

# ─── Find missing items ─────────────────────────────────────────
missing = sorted(all_item_ids - existing_items)
print(f"Missing item definitions: {len(missing)}")

# Group by namespace/mod
missing_by_ns = defaultdict(list)
for item_id in missing:
    ns = item_id.split(':')[0]
    missing_by_ns[ns].append(item_id)

for ns in sorted(missing_by_ns.keys()):
    print(f"  {ns}: {len(missing_by_ns[ns])}")

# ─── Parse existing mod sections ────────────────────────────────
section_lines = []
current_var = None
current_entries = []
sections = {}  # var_name -> {'header': str, 'entries': list[str], 'trailer': str}

for line in existing_content.split('\n'):
    m = re.match(r'^const (\w+): RawDef', line)
    if m:
        # Save previous section
        if current_var:
            sections[current_var] = {
                'entries': current_entries,
            }
        current_var = m.group(1)
        current_entries = []
        continue
    
    if current_var:
        if line.strip().startswith('] as RawDef;') or line.strip() == '];':
            sections[current_var] = {
                'entries': current_entries,
            }
            current_var = None
        else:
            current_entries.append(line)

# Map mod var names to their item entries
# var name -> list of (id, full_line)
var_entries = {}
for var_name, sec in sections.items():
    entries = []
    for line in sec['entries']:
        m = re.match(r"\s*\['([^']+)'", line)
        if m:
            entries.append((m.group(1), line))
    var_entries[var_name] = entries

# Also handle the ALL_DEFS section
all_defs_start = existing_content.find('const ALL_DEFS')
all_defs_end = existing_content.find('\n];', all_defs_start) + 3
all_defs_section = existing_content[all_defs_start:all_defs_end]

print(f"\nMod sections found: {list(var_entries.keys())}")

# ─── Generate missing definitions ───────────────────────────────
# Color palette for auto-generation
COLORS = [
    '#5C6BC0', '#42A5F5', '#26A69A', '#66BB6A', '#FF7043',
    '#AB47BC', '#EC407A', '#26C6DA', '#9CCC65', '#FFA726',
    '#8D6E63', '#78909C', '#7E57C2', '#29B6F6', '#66BB6A',
    '#EF5350', '#FF8A65', '#FFCA28', '#A5D6A7', '#B0BEC5',
    '#FFD54F', '#CE93D8', '#81D4FA', '#A1887F', '#F48FB1',
    '#80CBC4', '#E0E0E0', '#B39DDB', '#FFAB91', '#9FA8DA',
]

def name_from_id(item_id: str) -> str:
    """Convert snake_case item ID to human-readable name."""
    name = item_id.split(':')[-1]
    # Special processing
    replacements = {
        'me': 'ME', 'ae2': 'AE2', 'rf': 'RF', 'tnt': 'TNT',
        'p2p': 'P2P', 'i_o': 'I/O',
    }
    parts = name.split('_')
    result = []
    for p in parts:
        if p in replacements:
            result.append(replacements[p])
        elif p:
            result.append(p[0].upper() + p[1:] if len(p) > 1 else p.upper())
    return ' '.join(result)

def short_from_id(item_id: str, used_shorts: set) -> str:
    """Generate a 1-3 char short code."""
    name = item_id.split(':')[-1]
    parts = name.split('_')
    # Skip common suffixes
    skip_words = {'block', 'ingot', 'nugget', 'dust', 'plate', 'sheet', 
                   'crystal', 'gem', 'ore', 'raw', 'chunk', 'piece'}
    primary = [p for p in parts if p not in skip_words]
    if not primary:
        primary = parts
    # Take first char of first 2 parts
    s = ''.join(p[0].upper() for p in primary[:2] if p)
    if not s:
        s = parts[0][0].upper()
    return s[:3]

def color_from_id(item_id: str, index: int) -> str:
    """Generate a deterministic color."""
    idx = hash(item_id) % len(COLORS)
    return COLORS[idx]

def detect_tier(item_id: str) -> str:
    """Detect tier from item name."""
    name = item_id.lower()
    if any(x in name for x in ['creative', 'ultimate', 'omega', 'max']):
        return 'epic'
    if any(x in name for x in ['advanced', 'elite', 'hybrid', 'quantum']):
        return 'rare'
    if any(x in name for x in ['basic', 'standard']):
        return 'uncommon'
    return 'common'

def detect_type(item_id: str) -> str:
    """Detect item type from name."""
    name = item_id.lower()
    if any(x in name for x in ['sword', 'pickaxe', 'axe', 'shovel', 'hoe']):
        return 'tool'
    if any(x in name for x in ['helmet', 'chestplate', 'leggings', 'boots']):
        return 'armor'
    if any(x in name for x in ['block', 'wall', 'stair', 'slab', 'fence']):
        return 'block'
    if any(x in name for x in ['upgrade', 'card', 'module']):
        return 'upgrade'
    if any(x in name for x in ['crystal', 'gem', 'ingot', 'nugget', 'dust']):
        return 'material'
    if any(x in name for x in ['bucket']):
        return 'fluid'
    if any(x in name for x in ['seed', 'essence']):
        return 'component'
    return 'item'

# ─── Output ─────────────────────────────────────────────────────
# We'll generate the new definitions and add them to existing mod sections
# or create new mod sections for missing mods

# First, collect which missing items belong to which mod var name
# by mapping namespace to var name
ns_to_var = {
    'minecraft': 'VANILLA',
    'mekanism': 'MEKANISM',
    'thermal': 'THERMAL',
    'create': 'CREATE',
    'ae2': 'AE2',
    'ic2': 'IC2',
    'farmersdelight': 'FARMERSDELIGHT',
    'mysticalagriculture': 'MYSTICALAGRICULTURE',
    'prefab': 'PREFAB',
    'storagenetwork': 'STORAGENETWORK',
    'ironchest': 'IRONCHEST',
    'rootsclassic': 'ROOTSCLASSIC',
    'pylon': 'PYLON',
    'irons_spellbooks': 'IRONS_SPELLBOOKS',
    'sophisticatedstorage': 'SOPHISTICATEDSTORAGE',
    'sophisticatedbackpacks': 'SOPHISTICATEDBACKPACKS',
    'create': 'CREATE',
}

# Generate missing defs per mod
missing_by_var = defaultdict(list)
for item_id in missing:
    ns = item_id.split(':')[0]
    var = ns_to_var.get(ns)
    if var:
        missing_by_var[var].append(item_id)
    else:
        missing_by_var['OTHER'].append(item_id)

print(f"\nGenerating missing definitions by mod section:")
for var, items in sorted(missing_by_var.items()):
    print(f"  {var}: {len(items)} items")

# Read existing content
with open(ITEM_DEFS_FILE) as f:
    content = f.read()

# Generate definitions
used_shorts = set()
all_generated = []

def make_def(item_id, idx):
    """Create a definition line."""
    name = name_from_id(item_id)
    short = short_from_id(item_id, used_shorts)
    used_shorts.add(short)
    color = color_from_id(item_id, idx)
    tier = detect_tier(item_id)
    type_ = detect_type(item_id)
    return f"  ['{item_id}', '{name}', '{color}', '{tier}', '{type_}'],"

# Generate additions for each mod section
new_content = content
insertions = []

for var, items in sorted(missing_by_var.items()):
    if var not in sections:
        print(f"  WARNING: Mod section {var} not found, skipping {len(items)} items")
        continue
    
    gen_lines = []
    for idx, item_id in enumerate(sorted(items)):
        gen_lines.append(make_def(item_id, idx))
    
    # Find the last entry line in this section
    section = sections[var]
    entries = var_entries.get(var, [])
    if entries:
        last_entry_line = entries[-1][1]
        new_entries = '\n'.join(gen_lines)
        new_content = new_content.replace(
            last_entry_line,
            last_entry_line + '\n' + new_entries
        )
        print(f"  Added {len(gen_lines)} items to {var}")

# Also handle items from unknown mods - create new sections if needed
if 'OTHER' in missing_by_var:
    # Add to end of ALL_DEFS or as new MODS entry
    gen_lines = []
    for idx, item_id in enumerate(sorted(missing_by_var['OTHER'])):
        gen_lines.append(make_def(item_id, idx))
    print(f"  OTHER items could not be auto-added: {len(gen_lines)}")

# Write new file
with open(ITEM_DEFS_FILE, 'w') as f:
    f.write(new_content)

print(f"\nDone! Missing count: {len(missing)}, Modified sections: {len([v for v in missing_by_var if v in sections])}")
