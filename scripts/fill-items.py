#!/usr/bin/env python3
"""Generate ALL missing item definitions and add them to item-defs.ts.
Safely appends new items to existing mod sections.
"""
import re
from pathlib import Path
from collections import defaultdict, OrderedDict

RECIPES_DIR = Path('src/data/recipes')
ITEM_DEFS_FILE = Path('src/data/item-defs.ts')

# ─── Collect all item IDs from recipes ─────────────────────────
all_ids = set()
for f in sorted(RECIPES_DIR.glob('*.ts')):
    if f.name == 'helpers.ts': continue
    text = f.read_text()
    # All ing/res references
    for m in re.finditer(r"(?:ing|res)\('([^']+)'", text):
        all_ids.add(m.group(1))
    # Direct item refs in key objects
    for m in re.finditer(r"item:\s*'([^']+)'", text):
        all_ids.add(m.group(1))

# ─── Parse existing definitions ─────────────────────────────────
with open(ITEM_DEFS_FILE) as f:
    content = f.read()

existing = set(re.findall(r"^\s*'([^']+)',\s*'[^']*'", content, re.MULTILINE))

missing = sorted(all_ids - existing)
print(f"Total IDs in recipes: {len(all_ids)}")
print(f"Existing definitions: {len(existing)}")
print(f"Missing definitions: {len(missing)}")

# Group missing by namespace
missing_by_ns = defaultdict(list)
for item_id in missing:
    ns = item_id.split(':')[0]
    missing_by_ns[ns].append(item_id)

# ─── Smart color palette ────────────────────────────────────────
COLORS = [
    '#5C6BC0','#42A5F5','#26A69A','#66BB6A','#FF7043',
    '#AB47BC','#EC407A','#26C6DA','#9CCC65','#FFA726',
    '#8D6E63','#78909C','#7E57C2','#29B6F6','#EF5350',
    '#FF8A65','#FFCA28','#A5D6A7','#B0BEC5','#FFD54F',
    '#CE93D8','#81D4FA','#A1887F','#F48FB1','#80CBC4',
    '#E0E0E0','#B39DDB','#FFAB91','#9FA8DA','#90A4AE',
]

def gen_name(item_id):
    """Convert snake_case to human name."""
    name = item_id.split(':')[-1]
    repl = {'me':'ME','ae2':'AE2','rf':'RF','p2p':'P2P','i_o':'I/O','tnt':'TNT'}
    parts = name.split('_')
    result = []
    for p in parts:
        if p in repl: result.append(repl[p])
        elif p: result.append(p[0].upper()+p[1:] if len(p)>1 else p.upper())
    return ' '.join(result)

def gen_short(item_id):
    """1-3 char short code."""
    name = item_id.split(':')[-1]
    parts = name.split('_')
    skip = {'block','ingot','nugget','dust','plate','sheet','crystal','gem','ore','raw','chunk','piece'}
    primary = [p for p in parts if p not in skip] or parts
    s = ''.join(p[0].upper() for p in primary[:2] if p)
    return s[:3] if s else '? '

def gen_color(item_id):
    idx = abs(hash(item_id)) % len(COLORS)
    return COLORS[idx]

def gen_tier(item_id):
    n = item_id.lower()
    if any(x in n for x in ['creative','ultimate','omega','max','nether_star']): return 'epic'
    if any(x in n for x in ['advanced','elite','hybrid','quantum','supremium']): return 'rare'
    if any(x in n for x in ['basic','standard','inferium']): return 'uncommon'
    return 'common'

def gen_type(item_id):
    n = item_id.lower()
    if any(x in n for x in ['sword','pickaxe','axe','shovel','hoe','paxel']): return 'tool'
    if any(x in n for x in ['helmet','chestplate','leggings','boots','armor']): return 'armor'
    if any(x in n for x in ['block','wall','stair','slab','fence','brick']): return 'block'
    if any(x in n for x in ['upgrade','card','module']): return 'upgrade'
    if any(x in n for x in ['crystal','gem','ingot','nugget','dust','plate']): return 'material'
    if any(x in n for x in ['bucket','fluid']): return 'fluid'
    if any(x in n for x in ['seed','essence','crop']): return 'component'
    return 'item'

# ─── Map namespace to var name in item-defs.ts ──────────────────
NS_TO_VAR = {
    'minecraft': 'VANILLA', 'mekanism': 'MEKANISM', 'thermal': 'THERMAL',
    'create': 'CREATE', 'ae2': 'AE2', 'ic2': 'IC2',
    'farmersdelight': 'FARMERSDELIGHT', 'mysticalagriculture': 'MYSTICALAGRICULTURE',
    'prefab': 'PREFAB', 'storagenetwork': 'STORAGENETWORK',
    'ironchest': 'IRONCHEST', 'rootsclassic': 'ROOTSCLASSIC',
    'pylon': 'PYLON', 'irons_spellbooks': 'IRONS_SPELLBOOKS',
    'sophisticatedstorage': 'SOPHISTICATEDSTORAGE',
    'sophisticatedbackpacks': 'SOPHISTICATEDBACKPACKS',
}

# ─── Parse mod sections ─────────────────────────────────────────
# Find the end of each mod section
section_ends = {}
for var_name in set(NS_TO_VAR.values()):
    # Find the closing of this section
    pattern = re.compile(r'(const ' + re.escape(var_name) + r': RawDef\s*=\s*\[\n.*?\n\](?:\s*as RawDef)?\s*;)', re.DOTALL)
    m = pattern.search(content)
    if m:
        section_ends[var_name] = m.end()

# Actually, simpler: find the position right before the closing bracket of each section
# Search for "const VARNAME:" and then find the matching ]; or ] as RawDef;
var_sections = {}
for var_name in set(NS_TO_VAR.values()):
    start_match = re.search(r'^const ' + re.escape(var_name) + r': RawDef', content, re.MULTILINE)
    if not start_match:
        print(f"  WARNING: Section {var_name} not found in file")
        continue
    start = start_match.start()
    # Find matching closing
    rest = content[start:]
    # Find ]; or ] as RawDef;
    end_match = re.search(r'\](?:\s*as RawDef)?\s*;', rest)
    if not end_match:
        print(f"  WARNING: Cannot find end of section {var_name}")
        continue
    end = start + end_match.end()
    section_text = content[start:end]
    var_sections[var_name] = {'start': start, 'end': end, 'text': section_text}

# ─── Generate and insert missing defs ───────────────────────────
insertions = []  # (position, text_to_insert) sorted in reverse order

for ns, items in sorted(missing_by_ns.items()):
    var = NS_TO_VAR.get(ns)
    if not var:
        print(f"  SKIP: Unknown namespace {ns} with {len(items)} items")
        continue
    if var not in var_sections:
        print(f"  SKIP: No section for var {var} ({len(items)} items)")
        continue
    
    # Find insertion point: after the last entry inside the section
    section = var_sections[var]
    section_text = section['text']
    
    # Find last non-blank line before closing ]
    lines = section_text.split('\n')
    # Find the closing bracket index
    close_idx = None
    for i, line in enumerate(lines):
        if re.match(r'^\](?:\s*as RawDef)?\s*;', line.strip()):
            close_idx = i
            break
    
    if close_idx is None:
        print(f"  WARNING: Cannot find closing bracket in {var}")
        continue
    
    # Find the last entry before closing
    gen_lines = []
    for idx, item_id in enumerate(sorted(items)):
        line = f"  ['{item_id}', '{gen_name(item_id)}', '{gen_color(item_id)}', '{gen_tier(item_id)}', '{gen_type(item_id)}'],"
        gen_lines.append(line)
    
    # Insert before the closing bracket, preserving newlines
    # We need to find the absolute position in the file
    insert_pos = section['start'] + sum(len(l)+1 for l in lines[:close_idx])  # +1 for newline
    # Add one for the newline after the last entry
    insert_pos += 1  # after the newline of the last entry
    # Actually simpler: replace the exact text "];" with "gen_lines\n];"
    
    # The position of the closing bracket text (including newline before it)
    # Find the actual "] as RawDef;" or "];" in the section text
    bracket_match = re.search(r'\n(\](?:\s*as RawDef)?\s*;)', section['text'])
    if bracket_match:
        old = bracket_match.group(1)
        new_lines = '\n'.join(gen_lines)
        insert_at = section['start'] + bracket_match.start(1)
        insertions.append((insert_at, old, '\n' + new_lines + '\n' + old))

# Apply insertions in reverse order (to preserve positions)
insertions.sort(key=lambda x: x[0], reverse=True)
new_content = content
for pos, old, new_text in insertions:
    new_content = new_content[:pos] + new_text + new_content[pos+len(old):]

with open(ITEM_DEFS_FILE, 'w') as f:
    f.write(new_content)

print(f"\nInserted definitions for {sum(len(v) for v in missing_by_ns.values() if NS_TO_VAR.get(v[0].split(':')[0]))} items")
