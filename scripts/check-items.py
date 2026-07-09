#!/usr/bin/env python3
"""Extract all item IDs from recipes and compare against item-defs.ts."""
import re
import sys
from pathlib import Path

RECIPES_DIR = Path('src/data/recipes')
ITEM_DEFS_FILE = Path('src/data/item-defs.ts')

# Extract mod ID from recipe filename
def mod_from_file(fname: str) -> str:
    name = fname.replace('.ts', '')
    # Special case: thermal-processing -> thermal
    return name.split('-')[0]

# Extract all item IDs from recipe files
recipe_items = set()  # (mod, item_id)
item_to_recipe_mods = {}  # item_id -> set of mods
item_to_source_files = {}  # item_id -> set of files

for f in sorted(RECIPES_DIR.glob('*.ts')):
    if f.name == 'helpers.ts':
        continue
    text = f.read_text()
    mod = mod_from_file(f.name)
    
    # Find all item references in r() calls
    # Match both ing('mod:item') and res('mod:item')
    items = re.findall(r"(?:ing|res)\('([^:']+):([^']+)'", text)
    for ns, item_name in items:
        full_id = f"{ns}:{item_name}"
        recipe_items.add((mod.replace('-processing', ''), full_id))
        item_to_recipe_mods.setdefault(full_id, set()).add(mod)
        item_to_source_files.setdefault(full_id, set()).add(f.name)

# Parse item-defs.ts and extract defined IDs
defined_items = set()
current_mod = None
for line in open(ITEM_DEFS_FILE):
    m = re.match(r"const (\w+): RawDef", line)
    if m:
        current_mod = m.group(1).lower()
        continue
    m = re.match(r"\s*\['([^']+)'", line)
    if m:
        full_id = m.group(1)
        defined_items.add(full_id)

# Find items used in recipes but NOT defined
missing = []
for mod_src, item_id in sorted(recipe_items):
    if item_id not in defined_items:
        source = item_to_source_files[item_id]
        missing.append((item_id, list(source)))

# Also find items defined but never used in recipes
unused = defined_items - {item for _, item in recipe_items}
# But exclude vanilla items that might be listed separately
# (vanilla items like iron_ingot, etc. are used as ingredients)

print(f"Total unique item IDs in recipes: {len(recipe_items)}")
print(f"Total defined item IDs: {len(defined_items)}")
print(f"Defined but unused (not in any recipe): {len(unused)}")
print()

# Group missing items by mod namespace
from collections import defaultdict
by_ns = defaultdict(list)
for item_id, sources in missing:
    ns = item_id.split(':')[0]
    by_ns[ns].append(item_id)

print(f"MISSING ITEM DEFINITIONS: {len(missing)} total")
print()
for ns in sorted(by_ns.keys()):
    items = by_ns[ns]
    print(f"  {ns}: {len(items)} missing")
    for item_id in sorted(items):
        print(f"    - {item_id}")

print()

# For each mod, show actual recipe count vs defined count
from collections import Counter
defined_by_ns = Counter()
for item_id in defined_items:
    ns = item_id.split(':')[0]
    defined_by_ns[ns] += 1

recipe_unique_by_ns = Counter()
for _, item_id in recipe_items:
    ns = item_id.split(':')[0]
    recipe_unique_by_ns[ns] += 1

print("MOD COVERAGE:")
print(f"{'Mod':<25} {'Defined':>8} {'In Recipes':>10} {'Missing':>8}")
print("-"*55)
for ns in sorted(set(list(defined_by_ns.keys()) + list(recipe_unique_by_ns.keys()))):
    d = defined_by_ns.get(ns, 0)
    r = recipe_unique_by_ns.get(ns, 0)
    m = max(0, r - d)
    print(f"{ns:<25} {d:>8} {r:>10} {m:>8}")
