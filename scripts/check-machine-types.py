#!/usr/bin/env python3
"""Check which recipe types are used but not in MOD_MACHINES."""
import re, glob

RECIPES_DIR = 'src/data/recipes/'
SRC_FILE = 'src/components/Browser/ModBrowser.tsx'

# Extract types from recipe files
used_types = {}  # mod_id -> set of recipe types

for f in sorted(glob.glob(RECIPES_DIR + '*.ts')):
    if f.endswith('helpers.ts'):
        continue
    text = open(f).read()
    mod_name = f.split('/')[-1].replace('.ts', '')
    # Extract recipe type from r() calls
    types = set(re.findall(r"r\('[^']+',\s*'([^']+)'", text))
    used_types[mod_name] = types

# Extract MOD_MACHINES entries
mod_machines_text = open(SRC_FILE).read()
# Find the MOD_MACHINES block
m = re.search(r'const MOD_MACHINES: Record<string,.*?\{.*?\n\};', mod_machines_text, re.DOTALL)
if m:
    # Extract defined mods and their types
    defined_mods = {}
    current_mod = None
    for line in m.group(0).split('\n'):
        mm = re.match(r'\s+(\w+):\s*\[', line)
        if mm:
            current_mod = mm.group(1)
            defined_mods[current_mod] = set()
        mm = re.findall(r"type:\s*'([^']+)'", line)
        if current_mod and mm:
            for t in mm:
                defined_mods[current_mod].add(t)

    # Compare
    print("RECIPE TYPES NOT IN MOD_MACHINES:")
    for mod, types in sorted(used_types.items()):
        # Map recipe file mod names to MOD_MACHINES key names
        mod_key = mod.replace('-processing', '').replace('thermal', 'thermal').replace('vanilla', 'minecraft')
        if mod_key in defined_mods:
            missing_types = types - defined_mods[mod_key]
            if missing_types:
                print(f"  {mod_key}: MISSING {missing_types}")
        else:
            print(f"  {mod_key}: NOT IN MOD_MACHINES (types: {types})")
