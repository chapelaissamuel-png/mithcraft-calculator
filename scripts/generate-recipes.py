#!/usr/bin/env python3
"""MithCraft Recipe Generator — full mod recipe trees."""
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'recipes')
H = "import { r, ing } from './helpers';\nimport type { Recipe } from '../../types';\n"

def ing(item, count=1):
    return f"ing('{item}'{', ' + str(count) if count > 1 else ''})"

def write_recipes(fname, var, body):
    with open(os.path.join(OUT, fname), 'w') as f:
        f.write(H + f'const {var}: Recipe[] = [\n{body}\n];\n\nexport default {var};\n')

def gen_pattern(mod, out_id, pattern, keymap, count=1):
    ps = ', '.join(f"'{p}'" for p in pattern)
    ks = ', '.join(f'{k}: {ing(v)}' for k,v in sorted(keymap.items()))
    cnt = f', count: {count}' if count > 1 else ''
    return f"  r('{mod}:{out_id}', 'crafting', '{mod}',\n    [{{ item: '{mod}:{out_id}'{cnt} }}],\n    [], {{ pattern: [{ps}], key: {{ {ks} }} }}),"

def gen_tools(mod, prefix, mat, rod):
    pats = {
        'sword': (['I','I','S'], {'I':mat,'S':rod}),
        'pickaxe': (['III',' S ',' S '], {'I':mat,'S':rod}),
        'axe': (['II','IS',' S'], {'I':mat,'S':rod}),
        'shovel': (['I','S','S'], {'I':mat,'S':rod}),
        'hoe': (['II',' S',' S'], {'I':mat,'S':rod}),
        'helmet': (['III','I I'], {'I':mat}),
        'chestplate': (['I I','III','III'], {'I':mat}),
        'leggings': (['III','I I','I I'], {'I':mat}),
        'boots': (['I I','I I'], {'I':mat}),
    }
    lines = []
    for name, (pat, km) in pats.items():
        ps = ', '.join(f"'{p}'" for p in pat)
        ks = ', '.join(f'{k}: {ing(v)}' for k,v in sorted(km.items()))
        lines.append(f"  r('{mod}:{prefix}_{name}', 'crafting', '{mod}',\n    [{{ item: '{mod}:{prefix}_{name}' }}],\n    [], {{ pattern: [{ps}], key: {{ {ks} }} }}),")
    return '\n'.join(lines)

# ===== DATA COLLECTORS =====
V, MK, CR, TH, AE, IC = [], [], [], [], [], []

# ═══════════════════════════════════════════════════════════════════════════
# VANILLA
# ═══════════════════════════════════════════════════════════════════════════

V += [
    "// ─── SMELTING ─────────────────────────────────────────────────",
  r"  r('minecraft:iron_ingot_smelt', 'smelting', 'minecraft', [{ item: 'minecraft:iron_ingot' }], [ing('minecraft:iron_ore')]),",
  r"  r('minecraft:gold_ingot_smelt', 'smelting', 'minecraft', [{ item: 'minecraft:gold_ingot' }], [ing('minecraft:gold_ore')]),",
  r"  r('minecraft:copper_ingot_smelt', 'smelting', 'minecraft', [{ item: 'minecraft:copper_ingot' }], [ing('minecraft:copper_ore')]),",
  r"  r('minecraft:glass_smelt', 'smelting', 'minecraft', [{ item: 'minecraft:glass' }], [ing('minecraft:sand')]),",
  r"  r('minecraft:charcoal_smelt', 'smelting', 'minecraft', [{ item: 'minecraft:charcoal' }], [ing('minecraft:oak_log')]),",
  "",
  "// ─── BLOCKS ────────────────────────────────────────────────────",
]

for b,i in [('iron_block','iron_ingot'),('gold_block','gold_ingot'),('diamond_block','diamond'),
            ('netherite_block','netherite_ingot'),('copper_block','copper_ingot'),
            ('lapis_block','lapis_lazuli'),('coal_block','coal'),('emerald_block','emerald')]:
    V.append(gen_pattern('minecraft', b, ['III','III','III'], {'I': i}))

V += [
    "// ─── NUGGETS ─────────────────────────────────────────────────",
]
for m in ['iron','gold']:
    V.append(gen_pattern('minecraft', f'{m}_nugget', ['I'], {'I': f'minecraft:{m}_ingot'}, count=9))

V += [
    "",
    "// ─── TOOLS & ARMOR ───────────────────────────────────────────",
    gen_tools('minecraft','iron','minecraft:iron_ingot','minecraft:stick'),
    "",
    gen_tools('minecraft','diamond','minecraft:diamond','minecraft:stick'),
    "",
    gen_tools('minecraft','golden','minecraft:gold_ingot','minecraft:stick'),
    "",
    "// ─── BASIC MATERIALS ─────────────────────────────────────────",
  r"  r('minecraft:oak_planks', 'crafting', 'minecraft', [{ item: 'minecraft:oak_planks', count: 4 }], [], { pattern: ['L'], key: { L: ing('minecraft:oak_log') } }),",
  r"  r('minecraft:stick', 'crafting', 'minecraft', [{ item: 'minecraft:stick', count: 4 }], [], { pattern: ['P', 'P'], key: { P: ing('minecraft:oak_planks') } }),",
  r"  r('minecraft:torch', 'crafting', 'minecraft', [{ item: 'minecraft:torch', count: 4 }], [], { pattern: ['C', 'S'], key: { C: ing('minecraft:coal'), S: ing('minecraft:stick') } }),",
  r"  r('minecraft:redstone_torch', 'crafting', 'minecraft', [{ item: 'minecraft:redstone_torch' }], [], { pattern: ['R', 'S'], key: { R: ing('minecraft:redstone'), S: ing('minecraft:stick') } }),",
  r"  r('minecraft:redstone_repeater', 'crafting', 'minecraft', [{ item: 'minecraft:redstone_repeater' }], [], { pattern: ['R R', 'SSS', 'TTT'], key: { R: ing('minecraft:redstone_torch'), S: ing('minecraft:stone'), T: ing('minecraft:redstone') } }),",
  r"  r('minecraft:comparator', 'crafting', 'minecraft', [{ item: 'minecraft:comparator' }], [], { pattern: [' T ', 'TQT', 'SSS'], key: { T: ing('minecraft:redstone_torch'), Q: ing('minecraft:quartz'), S: ing('minecraft:stone') } }),",
  r"  r('minecraft:lever', 'crafting', 'minecraft', [{ item: 'minecraft:lever' }], [], { pattern: ['S', 'C'], key: { S: ing('minecraft:stick'), C: ing('minecraft:cobblestone') } }),",
  "",
  "// ─── WORKSTATIONS ─────────────────────────────────────────────",
  r"  r('minecraft:crafting_table', 'crafting', 'minecraft', [{ item: 'minecraft:crafting_table' }], [], { pattern: ['PP', 'PP'], key: { P: ing('minecraft:oak_planks') } }),",
  r"  r('minecraft:furnace', 'crafting', 'minecraft', [{ item: 'minecraft:furnace' }], [], { pattern: ['CCC', 'C C', 'CCC'], key: { C: ing('minecraft:cobblestone') } }),",
  r"  r('minecraft:chest', 'crafting', 'minecraft', [{ item: 'minecraft:chest' }], [], { pattern: ['PPP', 'P P', 'PPP'], key: { P: ing('minecraft:oak_planks') } }),",
  r"  r('minecraft:anvil', 'crafting', 'minecraft', [{ item: 'minecraft:anvil' }], [], { pattern: ['BBB', ' I ', 'III'], key: { B: ing('minecraft:iron_block'), I: ing('minecraft:iron_ingot') } }),",
  r"  r('minecraft:enchanting_table', 'crafting', 'minecraft', [{ item: 'minecraft:enchanting_table' }], [], { pattern: [' B ', 'DOD', 'OOO'], key: { B: ing('minecraft:book'), D: ing('minecraft:diamond'), O: ing('minecraft:obsidian') } }),",
  r"  r('minecraft:beacon', 'crafting', 'minecraft', [{ item: 'minecraft:beacon' }], [], { pattern: ['GGG', 'GSG', 'OOO'], key: { G: ing('minecraft:glass'), S: ing('minecraft:nether_star'), O: ing('minecraft:obsidian') } }),",
  "",
  "// ─── MECHANICAL ───────────────────────────────────────────────",
  r"  r('minecraft:piston', 'crafting', 'minecraft', [{ item: 'minecraft:piston' }], [], { pattern: ['PPP', 'CIC', 'CRC'], key: { P: ing('minecraft:oak_planks'), C: ing('minecraft:cobblestone'), I: ing('minecraft:iron_ingot'), R: ing('minecraft:redstone') } }),",
  r"  r('minecraft:sticky_piston', 'crafting', 'minecraft', [{ item: 'minecraft:sticky_piston' }], [ing('minecraft:slime_ball'), ing('minecraft:piston')]),",
  r"  r('minecraft:hopper', 'crafting', 'minecraft', [{ item: 'minecraft:hopper' }], [], { pattern: ['I I', 'ICI', ' I '], key: { I: ing('minecraft:iron_ingot'), C: ing('minecraft:chest') } }),",
  r"  r('minecraft:dispenser', 'crafting', 'minecraft', [{ item: 'minecraft:dispenser' }], [], { pattern: ['CCC', 'CBC', 'CRC'], key: { C: ing('minecraft:cobblestone'), B: ing('minecraft:bow'), R: ing('minecraft:redstone') } }),",
  r"  r('minecraft:observer', 'crafting', 'minecraft', [{ item: 'minecraft:observer' }], [], { pattern: ['CCC', 'RQR', 'CCC'], key: { C: ing('minecraft:cobblestone'), R: ing('minecraft:redstone'), Q: ing('minecraft:quartz') } }),",
  r"  r('minecraft:note_block', 'crafting', 'minecraft', [{ item: 'minecraft:note_block' }], [], { pattern: ['PPP', 'PRP', 'PPP'], key: { P: ing('minecraft:oak_planks'), R: ing('minecraft:redstone') } }),",
  r"  r('minecraft:jukebox', 'crafting', 'minecraft', [{ item: 'minecraft:jukebox' }], [], { pattern: ['PPP', 'PDP', 'PPP'], key: { P: ing('minecraft:oak_planks'), D: ing('minecraft:diamond') } }),",
  "",
  "// ─── RAILS ────────────────────────────────────────────────────",
  r"  r('minecraft:rail', 'crafting', 'minecraft', [{ item: 'minecraft:rail', count: 16 }], [], { pattern: ['I I', 'ISI', 'I I'], key: { I: ing('minecraft:iron_ingot'), S: ing('minecraft:stick') } }),",
  r"  r('minecraft:powered_rail', 'crafting', 'minecraft', [{ item: 'minecraft:powered_rail', count: 6 }], [], { pattern: ['R R', 'RIR', 'RSR'], key: { R: ing('minecraft:gold_ingot'), I: ing('minecraft:iron_ingot'), S: ing('minecraft:stick') } }),",
  "",
  "// ─── DOORS ────────────────────────────────────────────────────",
  r"  r('minecraft:iron_door', 'crafting', 'minecraft', [{ item: 'minecraft:iron_door', count: 3 }], [], { pattern: ['II', 'II', 'II'], key: { I: ing('minecraft:iron_ingot') } }),",
  r"  r('minecraft:iron_trapdoor', 'crafting', 'minecraft', [{ item: 'minecraft:iron_trapdoor' }], [], { pattern: ['II', 'II'], key: { I: ing('minecraft:iron_ingot') } }),",
]

for w in ['oak','spruce','birch','jungle','acacia','dark_oak']:
    V.append(gen_pattern('minecraft', f'{w}_door', ['PP','PP','PP'], {'P': f'minecraft:{w}_planks'}, count=3))
    V.append(gen_pattern('minecraft', f'{w}_trapdoor', ['PPP','PPP'], {'P': f'minecraft:{w}_planks'}))
    V.append(gen_pattern('minecraft', f'{w}_fence', ['PSP','PSP'], {'P': f'minecraft:{w}_planks', 'S': 'minecraft:stick'}, count=3))
    V.append(gen_pattern('minecraft', f'{w}_slab', ['SSS'], {'S': f'minecraft:{w}_planks'}, count=6))
    V.append(gen_pattern('minecraft', f'{w}_stairs', ['S  ','SS ','SSS'], {'S': f'minecraft:{w}_planks'}, count=4))

for s in ['stone','cobblestone','andesite','diorite','granite','sandstone','bricks','stone_bricks']:
    V.append(gen_pattern('minecraft', f'{s}_slab', ['SSS'], {'S': f'minecraft:{s}'}, count=6))
    V.append(gen_pattern('minecraft', f'{s}_stairs', ['S  ','SS ','SSS'], {'S': f'minecraft:{s}'}, count=4))
    V.append(gen_pattern('minecraft', f'{s}_wall', ['SSS','SSS'], {'S': f'minecraft:{s}'}, count=6))

V += [
  r"  r('minecraft:bow', 'crafting', 'minecraft', [{ item: 'minecraft:bow' }], [], { pattern: [' S ', 'S I', ' S '], key: { S: ing('minecraft:stick'), I: ing('minecraft:string') } }),",
  r"  r('minecraft:arrow', 'crafting', 'minecraft', [{ item: 'minecraft:arrow', count: 4 }], [], { pattern: ['F', 'S', 'E'], key: { F: ing('minecraft:flint'), S: ing('minecraft:stick'), E: ing('minecraft:feather') } }),",
  r"  r('minecraft:netherite_ingot', 'crafting', 'minecraft', [{ item: 'minecraft:netherite_ingot' }], [ing('minecraft:netherite_scrap', 4), ing('minecraft:gold_ingot', 4)]),",
  r"  r('minecraft:tnt', 'crafting', 'minecraft', [{ item: 'minecraft:tnt' }], [], { pattern: ['GSG', 'SGS', 'GSG'], key: { G: ing('minecraft:gunpowder'), S: ing('minecraft:sand') } }),",
  r"  r('minecraft:shield', 'crafting', 'minecraft', [{ item: 'minecraft:shield' }], [], { pattern: ['WIW', 'WWW', ' W '], key: { W: ing('minecraft:oak_planks'), I: ing('minecraft:iron_ingot') } }),",
  r"  r('minecraft:flint_and_steel', 'crafting', 'minecraft', [{ item: 'minecraft:flint_and_steel' }], [ing('minecraft:iron_ingot'), ing('minecraft:flint')]),",
  r"  r('minecraft:book', 'crafting', 'minecraft', [{ item: 'minecraft:book' }], [ing('minecraft:paper', 3), ing('minecraft:leather')]),",
  r"  r('minecraft:bread', 'crafting', 'minecraft', [{ item: 'minecraft:bread' }], [], { pattern: ['WWW'], key: { W: ing('minecraft:wheat') } }),",
  "",
  "// ─── NETHERITE UPGRADES ───────────────────────────────────────",
]

for t in ['pickaxe','sword','axe','shovel','hoe','helmet','chestplate','leggings','boots']:
    V.append( f"  r('minecraft:netherite_{t}', 'smithing', 'minecraft',\n"
             f"    [{{ item: 'minecraft:netherite_{t}' }}],\n"
             f"    [ing('minecraft:diamond_{t}'), ing('minecraft:netherite_ingot')]),")

# Remove empty trailing entries and fix formatting
# The gen_pattern adds a trailing comma after 'key: { ... }' but pattern already has ','
V = [l for l in V if l]  # remove empties

print("Vanilla done")

# ═══════════════════════════════════════════════════════════════════════════
# MEKANISM
# ═══════════════════════════════════════════════════════════════════════════

MK += [
    "// ─── ORE → INGOT ─────────────────────────────────────────────",
]
for i,o in [('osmium_ingot','osmium_ore'),('tin_ingot','tin_ore'),('lead_ingot','lead_ore'),('uranium_ingot','uranium_ore')]:
    MK.append(f"  r('mekanism:{i}_smelt', 'smelting', 'mekanism', [{{ item: 'mekanism:{i}' }}], [ing('mekanism:{o}')]),")

MK += [
    "",
    "// ─── ENRICHING ───────────────────────────────────────────────",
]
for m,i,c in [('iron','minecraft:iron_ingot',3),('gold','minecraft:gold_ingot',3),('tin','mekanism:tin_ingot',3),('osmium','mekanism:osmium_ingot',3)]:
    MK.append(f"  r('mekanism:enriched_{m}', 'mekanism:enriching', 'mekanism', [{{ item: 'mekanism:enriched_{m}' }}], [ing('{i}', {c})], {{ energy: 200 }}),")
MK += [
  r"  r('mekanism:enriched_diamond', 'mekanism:enriching', 'mekanism', [{ item: 'mekanism:enriched_diamond' }], [ing('minecraft:diamond', 3)], { energy: 400 }),",
  r"  r('mekanism:enriched_redstone', 'mekanism:enriching', 'mekanism', [{ item: 'mekanism:enriched_redstone' }], [ing('minecraft:redstone', 8)], { energy: 200 }),",
  "",
  "// ─── ALLOYS ───────────────────────────────────────────────────",
  r"  r('mekanism:steel_ingot', 'mekanism:metallurgic_infusing', 'mekanism', [{ item: 'mekanism:steel_ingot' }], [ing('minecraft:iron_ingot'), ing('minecraft:coal', 2)], { energy: 400 }),",
  r"  r('mekanism:bronze_ingot', 'mekanism:metallurgic_infusing', 'mekanism', [{ item: 'mekanism:bronze_ingot' }], [ing('minecraft:copper_ingot', 3), ing('mekanism:tin_ingot')], { energy: 400 }),",
  r"  r('mekanism:alloy_infused', 'mekanism:metallurgic_infusing', 'mekanism', [{ item: 'mekanism:alloy_infused' }], [ing('minecraft:iron_ingot'), ing('mekanism:enriched_redstone')], { energy: 400 }),",
  r"  r('mekanism:alloy_reinforced', 'mekanism:metallurgic_infusing', 'mekanism', [{ item: 'mekanism:alloy_reinforced' }], [ing('mekanism:alloy_infused'), ing('mekanism:enriched_diamond')], { energy: 600 }),",
  r"  r('mekanism:alloy_atomic', 'mekanism:metallurgic_infusing', 'mekanism', [{ item: 'mekanism:alloy_atomic' }], [ing('mekanism:alloy_reinforced'), ing('mekanism:polonium_pellet')], { energy: 1000 }),",
  "",
  "// ─── SUBSTRATE / HDPE ─────────────────────────────────────────",
  r"  r('mekanism:bio_fuel', 'mekanism:crushing', 'mekanism', [{ item: 'mekanism:bio_fuel', count: 5 }], [ing('minecraft:wheat', 4)], { energy: 100 }),",
  r"  r('mekanism:substrate', 'mekanism:crushing', 'mekanism', [{ item: 'mekanism:substrate' }], [ing('mekanism:bio_fuel', 4)], { energy: 800 }),",
  r"  r('mekanism:hdpe_sheet', 'mekanism:pigment_extracting', 'mekanism', [{ item: 'mekanism:hdpe_sheet', count: 3 }], [ing('mekanism:substrate')], { energy: 200 }),",
  r"  r('mekanism:hdpe_rod', 'mekanism:pigment_extracting', 'mekanism', [{ item: 'mekanism:hdpe_rod' }], [ing('mekanism:substrate')], { energy: 200 }),",
  "",
  "// ─── CONTROL CIRCUITS (4 TIERS) ───────────────────────────────",
]
for tier, (prev, mat) in [('basic',('mekanism:osmium_ingot','minecraft:redstone')),
                          ('advanced',('mekanism:control_circuit_basic','minecraft:gold_ingot')),
                          ('elite',('mekanism:control_circuit_advanced','mekanism:enriched_diamond')),
                          ('ultimate',('mekanism:control_circuit_elite','mekanism:alloy_atomic'))]:
    MK.append(gen_pattern('mekanism', f'control_circuit_{tier}',
        ['PCP', 'R R', 'PCP'], {'P': prev, 'C': mat, 'R': 'minecraft:redstone'}))

MK += [
    "",
    "// ─── ENERGY CUBES (4 TIERS) ──────────────────────────────────",
]
for tier, (circ, mat) in [('basic',('mekanism:control_circuit_basic','mekanism:osmium_ingot')),
                          ('advanced',('mekanism:control_circuit_advanced','minecraft:gold_ingot')),
                          ('elite',('mekanism:control_circuit_elite','mekanism:enriched_diamond')),
                          ('ultimate',('mekanism:control_circuit_ultimate','mekanism:alloy_atomic'))]:
    MK.append(gen_pattern('mekanism', f'{tier}_energy_cube',
        ['SPS', 'ACA', 'SPS'], {'S': circ, 'P': mat, 'A': 'mekanism:alloy_infused', 'C': circ}))

MK += [
    "",
    "// ─── MACHINES ────────────────────────────────────────────────",
  r"  r('mekanism:enrichment_chamber', 'crafting', 'mekanism', [{ item: 'mekanism:enrichment_chamber' }], [], { pattern: ['OAO', 'S S', 'OAO'], key: { O: ing('mekanism:osmium_ingot'), A: ing('mekanism:alloy_infused'), S: ing('mekanism:control_circuit_basic') } }),",
  r"  r('mekanism:metallurgic_infuser', 'crafting', 'mekanism', [{ item: 'mekanism:metallurgic_infuser' }], [], { pattern: ['IAI', 'S S', 'IAI'], key: { I: ing('minecraft:iron_ingot'), A: ing('mekanism:alloy_infused'), S: ing('mekanism:control_circuit_basic') } }),",
  r"  r('mekanism:combiner', 'crafting', 'mekanism', [{ item: 'mekanism:combiner' }], [], { pattern: ['OAO', 'S S', 'OAO'], key: { O: ing('mekanism:osmium_ingot'), A: ing('mekanism:alloy_reinforced'), S: ing('mekanism:control_circuit_advanced') } }),",
  r"  r('mekanism:crusher', 'crafting', 'mekanism', [{ item: 'mekanism:crusher' }], [], { pattern: ['OAO', 'S S', 'OAO'], key: { O: ing('mekanism:osmium_ingot'), A: ing('mekanism:alloy_reinforced'), S: ing('mekanism:control_circuit_advanced') } }),",
  r"  r('mekanism:purification_chamber', 'crafting', 'mekanism', [{ item: 'mekanism:purification_chamber' }], [], { pattern: ['OAO', 'C C', 'OAO'], key: { O: ing('mekanism:osmium_ingot'), A: ing('mekanism:alloy_atomic'), C: ing('mekanism:control_circuit_elite') } }),",
  r"  r('mekanism:chemical_injection_chamber', 'crafting', 'mekanism', [{ item: 'mekanism:chemical_injection_chamber' }], [], { pattern: ['OAO', 'C C', 'OAO'], key: { O: ing('mekanism:osmium_ingot'), A: ing('mekanism:alloy_atomic'), C: ing('mekanism:control_circuit_elite') } }),",
  r"  r('mekanism:digital_miner', 'crafting', 'mekanism', [{ item: 'mekanism:digital_miner' }], [], { pattern: ['UCU', 'CAC', 'UCU'], key: { U: ing('mekanism:uranium_ingot'), C: ing('mekanism:control_circuit_ultimate'), A: ing('mekanism:alloy_atomic') } }),",
  "",
  "// ─── FLUORITE / NUCLEAR ───────────────────────────────────────",
  r"  r('mekanism:fluorite_gem', 'smelting', 'mekanism', [{ item: 'mekanism:fluorite_gem' }], [ing('mekanism:fluorite_ore')]),",
  r"  r('mekanism:polonium_pellet', 'machine', 'mekanism', [{ item: 'mekanism:polonium_pellet' }], [ing('mekanism:uranium_ingot', 2)], { energy: 8000 }),",
]

# Tiered factories
for tier, circ, alloy in [('basic','control_circuit_basic','alloy_infused'),
                          ('advanced','control_circuit_advanced','alloy_reinforced'),
                          ('elite','control_circuit_elite','alloy_atomic')]:
    for mach in ['smelting','enriching','crushing','compressing']:
        MK.append(f"  r('mekanism:{tier}_{mach}_factory', 'crafting', 'mekanism',\n"
                 f"    [{{ item: 'mekanism:{tier}_{mach}_factory' }}],\n"
                 f"    [], {{ pattern: ['III', 'CSC', 'AAA'],\n"
                 f"          key: {{ I: ing('mekanism:osmium_ingot'), C: ing('mekanism:{circ}'),\n"
                 f"                S: ing('mekanism:{alloy}'), A: ing('mekanism:alloy_infused') }} }}),")

print("Mekanism done")

# ═══════════════════════════════════════════════════════════════════════════
# CREATE
# ═══════════════════════════════════════════════════════════════════════════

CR += [
    "// ─── BASE COMPONENTS ─────────────────────────────────────────",
  r"  r('create:andesite_alloy', 'crafting', 'create', [{ item: 'create:andesite_alloy', count: 2 }], [ing('minecraft:andesite'), ing('minecraft:iron_nugget', 2)]),",
  r"  r('create:brass_ingot', 'smelting', 'create', [{ item: 'create:brass_ingot' }], [ing('create:zinc_ingot'), ing('minecraft:copper_ingot')], { energy: 200 }),",
  r"  r('create:zinc_ingot', 'smelting', 'create', [{ item: 'create:zinc_ingot' }], [ing('create:zinc_ore')]),",
  "",
  "// ─── SHEETS ───────────────────────────────────────────────────",
  r"  r('create:iron_sheet', 'create:pressing', 'create', [{ item: 'create:iron_sheet' }], [ing('minecraft:iron_ingot')], { energy: 200 }),",
  r"  r('create:copper_sheet', 'create:pressing', 'create', [{ item: 'create:copper_sheet' }], [ing('minecraft:copper_ingot')], { energy: 200 }),",
  r"  r('create:brass_sheet', 'create:pressing', 'create', [{ item: 'create:brass_sheet' }], [ing('create:brass_ingot')], { energy: 200 }),",
  "",
  "// ─── KINETICS ─────────────────────────────────────────────────",
  r"  r('create:cogwheel', 'crafting', 'create', [{ item: 'create:cogwheel' }], [], { pattern: [' A ', 'ASA', ' A '], key: { A: ing('create:andesite_alloy'), S: ing('minecraft:stick') } }),",
  r"  r('create:large_cogwheel', 'crafting', 'create', [{ item: 'create:large_cogwheel' }], [], { pattern: ['AAA', 'ACA', 'AAA'], key: { A: ing('create:andesite_alloy'), C: ing('create:cogwheel') } }),",
  r"  r('create:shaft', 'crafting', 'create', [{ item: 'create:shaft' }], [], { pattern: ['A', 'S'], key: { A: ing('create:andesite_alloy'), S: ing('minecraft:stick') } }),",
  r"  r('create:gearbox', 'crafting', 'create', [{ item: 'create:gearbox' }], [], { pattern: [' C ', 'CSC', ' C '], key: { C: ing('create:cogwheel'), S: ing('create:shaft') } }),",
  r"  r('create:piston_extension_pole', 'crafting', 'create', [{ item: 'create:piston_extension_pole' }], [], { pattern: ['A', 'S', 'A'], key: { A: ing('create:andesite_alloy'), S: ing('create:shaft') } }),",
  "",
  "// ─── PRECISION MECHANISM ──────────────────────────────────────",
  r"  r('create:precision_mechanism', 'crafting', 'create', [{ item: 'create:precision_mechanism' }], [], { pattern: [' C ', 'CBC', ' C '], key: { C: ing('create:cogwheel'), B: ing('create:brass_sheet') } }),",
  "",
  "// ─── CASINGS ──────────────────────────────────────────────────",
  r"  r('create:andesite_casing', 'crafting', 'create', [{ item: 'create:andesite_casing' }], [], { pattern: ['AAA', 'AWA', 'AAA'], key: { A: ing('create:andesite_alloy'), W: ing('minecraft:oak_planks') } }),",
  r"  r('create:brass_casing', 'crafting', 'create', [{ item: 'create:brass_casing' }], [], { pattern: ['BBB', 'BWB', 'BBB'], key: { B: ing('create:brass_sheet'), W: ing('minecraft:oak_planks') } }),",
  r"  r('create:copper_casing', 'crafting', 'create', [{ item: 'create:copper_casing' }], [], { pattern: ['CCC', 'CWC', 'CCC'], key: { C: ing('create:copper_sheet'), W: ing('minecraft:oak_planks') } }),",
  r"  r('create:andesite_block', 'crafting', 'create', [{ item: 'create:andesite_block' }], [], { pattern: ['AA', 'AA'], key: { A: ing('create:andesite_alloy') } }),",
  r"  r('create:brass_block', 'crafting', 'create', [{ item: 'create:brass_block' }], [], { pattern: ['BB', 'BB'], key: { B: ing('create:brass_ingot') } }),",
  r"  r('create:zinc_block', 'crafting', 'create', [{ item: 'create:zinc_block' }], [], { pattern: ['ZZ', 'ZZ'], key: { Z: ing('create:zinc_ingot') } }),",
  "",
  "// ─── MACHINES ─────────────────────────────────────────────────",
  r"  r('create:mechanical_press', 'crafting', 'create', [{ item: 'create:mechanical_press' }], [], { pattern: [' I ', 'SIS', 'ACA'], key: { I: ing('minecraft:iron_block'), S: ing('create:shaft'), A: ing('minecraft:andesite'), C: ing('create:andesite_casing') } }),",
  r"  r('create:mechanical_mixer', 'crafting', 'create', [{ item: 'create:mechanical_mixer' }], [], { pattern: [' C ', 'CBC', 'ACA'], key: { C: ing('create:cogwheel'), B: ing('create:brass_casing'), A: ing('create:andesite_casing') } }),",
  r"  r('create:mechanical_saw', 'crafting', 'create', [{ item: 'create:mechanical_saw' }], [], { pattern: [' I ', ' S ', 'ACA'], key: { I: ing('minecraft:iron_ingot'), S: ing('create:shaft'), A: ing('create:andesite_casing') } }),",
  r"  r('create:mechanical_bearing', 'crafting', 'create', [{ item: 'create:mechanical_bearing' }], [], { pattern: [' S ', 'SAS', ' A '], key: { S: ing('create:shaft'), A: ing('create:andesite_casing') } }),",
  r"  r('create:mechanical_piston', 'crafting', 'create', [{ item: 'create:mechanical_piston' }], [], { pattern: ['PPP', 'ACA', ' A '], key: { P: ing('create:piston_extension_pole'), A: ing('create:andesite_casing'), C: ing('create:cogwheel') } }),",
  r"  r('create:crushing_wheel', 'crafting', 'create', [{ item: 'create:crushing_wheel' }], [], { pattern: ['A A', 'ACA', 'ADA'], key: { A: ing('create:andesite_alloy'), C: ing('create:cogwheel'), D: ing('create:andesite_casing') } }),",
  r"  r('create:belt_connector', 'crafting', 'create', [{ item: 'create:belt_connector' }], [], { pattern: ['KKK', 'SSS', 'KKK'], key: { K: ing('create:andesite_alloy'), S: ing('minecraft:string') } }),",
  r"  r('create:water_wheel', 'crafting', 'create', [{ item: 'create:water_wheel' }], [], { pattern: [' S ', 'SWS', ' S '], key: { S: ing('create:shaft'), W: ing('minecraft:oak_planks') } }),",
  r"  r('create:large_water_wheel', 'crafting', 'create', [{ item: 'create:large_water_wheel' }], [], { pattern: ['WWW', 'WSW', 'WWW'], key: { W: ing('create:water_wheel'), S: ing('create:shaft') } }),",
  r"  r('create:windmill_bearing', 'crafting', 'create', [{ item: 'create:windmill_bearing' }], [], { pattern: [' S ', 'SAS', ' A '], key: { S: ing('create:shaft'), A: ing('create:andesite_casing') } }),",
  r"  r('create:depot', 'crafting', 'create', [{ item: 'create:depot' }], [], { pattern: ['AAA', 'ACA'], key: { A: ing('create:andesite_alloy'), C: ing('create:andesite_casing') } }),",
  r"  r('create:chute', 'crafting', 'create', [{ item: 'create:chute', count: 4 }], [], { pattern: ['AAA', 'A A', 'AAA'], key: { A: ing('create:andesite_alloy') } }),",
  r"  r('create:smart_chute', 'crafting', 'create', [{ item: 'create:smart_chute' }], [], { pattern: [' C ', 'CCC', ' C '], key: { C: ing('create:chute') } }),",
  r"  r('create:andesite_funnel', 'crafting', 'create', [{ item: 'create:andesite_funnel', count: 2 }], [], { pattern: ['A', 'C'], key: { A: ing('create:andesite_alloy'), C: ing('create:andesite_casing') } }),",
  r"  r('create:brass_funnel', 'crafting', 'create', [{ item: 'create:brass_funnel', count: 2 }], [], { pattern: ['B', 'C'], key: { B: ing('create:brass_sheet'), C: ing('create:brass_casing') } }),",
  r"  r('create:andesite_tunnel', 'crafting', 'create', [{ item: 'create:andesite_tunnel' }], [], { pattern: ['AAA', 'ACA'], key: { A: ing('create:andesite_alloy'), C: ing('create:andesite_casing') } }),",
  r"  r('create:brass_tunnel', 'crafting', 'create', [{ item: 'create:brass_tunnel' }], [], { pattern: ['BBB', 'BCB'], key: { B: ing('create:brass_sheet'), C: ing('create:brass_casing') } }),",
]

print("Create done")

# ═══════════════════════════════════════════════════════════════════════════
# THERMAL
# ═══════════════════════════════════════════════════════════════════════════

TH += [
    "// ─── RAW → INGOT ─────────────────────────────────────────────",
]
for i,o in [('tin_ingot','tin_ore'),('lead_ingot','lead_ore'),('silver_ingot','silver_ore'),('nickel_ingot','nickel_ore')]:
    TH.append(f"  r('thermal:{i}_smelt', 'smelting', 'thermal', [{{ item: 'thermal:{i}' }}], [ing('thermal:{o}')]),")
TH += [
    "",
    "// ─── ALLOYS (INDUCTION SMELTING) ─────────────────────────────",
  r"  r('thermal:bronze_ingot', 'thermal:induction_smelter', 'thermal', [{ item: 'thermal:bronze_ingot', count: 4 }], [ing('minecraft:copper_ingot', 3), ing('thermal:tin_ingot')], { energy: 400 }),",
  r"  r('thermal:constantan_ingot', 'thermal:induction_smelter', 'thermal', [{ item: 'thermal:constantan_ingot', count: 2 }], [ing('minecraft:copper_ingot'), ing('thermal:nickel_ingot')], { energy: 400 }),",
  r"  r('thermal:electrum_ingot', 'thermal:induction_smelter', 'thermal', [{ item: 'thermal:electrum_ingot', count: 2 }], [ing('minecraft:gold_ingot'), ing('thermal:silver_ingot')], { energy: 300 }),",
  r"  r('thermal:invar_ingot', 'thermal:induction_smelter', 'thermal', [{ item: 'thermal:invar_ingot', count: 3 }], [ing('minecraft:iron_ingot', 2), ing('thermal:nickel_ingot')], { energy: 500 }),",
  r"  r('thermal:steel_ingot', 'thermal:induction_smelter', 'thermal', [{ item: 'thermal:steel_ingot' }], [ing('minecraft:iron_ingot'), ing('minecraft:coal', 2)], { energy: 400 }),",
  r"  r('thermal:signalum_ingot', 'thermal:induction_smelter', 'thermal', [{ item: 'thermal:signalum_ingot', count: 2 }], [ing('minecraft:copper_ingot'), ing('thermal:silver_ingot'), ing('minecraft:redstone', 4)], { energy: 600 }),",
  r"  r('thermal:lumium_ingot', 'thermal:induction_smelter', 'thermal', [{ item: 'thermal:lumium_ingot', count: 2 }], [ing('thermal:tin_ingot'), ing('thermal:silver_ingot'), ing('minecraft:glowstone_dust', 4)], { energy: 600 }),",
  r"  r('thermal:enderium_ingot', 'thermal:induction_smelter', 'thermal', [{ item: 'thermal:enderium_ingot', count: 2 }], [ing('thermal:lead_ingot'), ing('minecraft:diamond'), ing('minecraft:ender_pearl', 2)], { energy: 800 }),",
  "",
  "// ─── COMPONENTS ───────────────────────────────────────────────",
  r"  r('thermal:redstone_servo', 'crafting', 'thermal', [{ item: 'thermal:redstone_servo' }], [], { pattern: [' I ', 'IRI', ' I '], key: { I: ing('minecraft:iron_ingot'), R: ing('minecraft:redstone') } }),",
  r"  r('thermal:rf_coil', 'crafting', 'thermal', [{ item: 'thermal:rf_coil' }], [], { pattern: [' G ', 'GIG', ' G '], key: { G: ing('minecraft:gold_ingot'), I: ing('minecraft:iron_ingot') } }),",
  r"  r('thermal:machine_frame', 'crafting', 'thermal', [{ item: 'thermal:machine_frame' }], [], { pattern: ['SRS', 'RIR', 'SRS'], key: { S: ing('thermal:redstone_servo'), R: ing('thermal:rf_coil'), I: ing('minecraft:iron_ingot') } }),",
  "",
  "// ─── AUGMENTS ─────────────────────────────────────────────────",
  r"  r('thermal:upgrade_augment_1', 'crafting', 'thermal', [{ item: 'thermal:upgrade_augment_1' }], [], { pattern: [' I ', 'ISI', ' I '], key: { I: ing('minecraft:iron_ingot'), S: ing('thermal:redstone_servo') } }),",
  r"  r('thermal:upgrade_augment_2', 'crafting', 'thermal', [{ item: 'thermal:upgrade_augment_2' }], [], { pattern: [' G ', 'GSG', ' G '], key: { G: ing('minecraft:gold_ingot'), S: ing('thermal:upgrade_augment_1') } }),",
  r"  r('thermal:upgrade_augment_3', 'crafting', 'thermal', [{ item: 'thermal:upgrade_augment_3' }], [], { pattern: [' D ', 'DSD', ' D '], key: { D: ing('minecraft:diamond'), S: ing('thermal:upgrade_augment_2') } }),",
  "",
  "// ─── MACHINES ─────────────────────────────────────────────────",
  r"  r('thermal:pulverizer', 'crafting', 'thermal', [{ item: 'thermal:pulverizer' }], [], { pattern: ['IRI', 'IFI', 'ICI'], key: { I: ing('minecraft:iron_ingot'), R: ing('minecraft:redstone'), F: ing('thermal:machine_frame'), C: ing('thermal:redstone_servo') } }),",
  r"  r('thermal:induction_smelter', 'crafting', 'thermal', [{ item: 'thermal:induction_smelter' }], [], { pattern: ['IRI', 'IFI', 'IRI'], key: { I: ing('minecraft:iron_ingot'), R: ing('minecraft:redstone'), F: ing('thermal:machine_frame') } }),",
  r"  r('thermal:centrifuge', 'crafting', 'thermal', [{ item: 'thermal:centrifuge' }], [], { pattern: ['IRI', 'IFI', 'IRI'], key: { I: ing('minecraft:gold_ingot'), R: ing('minecraft:redstone'), F: ing('thermal:machine_frame') } }),",
  r"  r('thermal:refinery', 'crafting', 'thermal', [{ item: 'thermal:refinery' }], [], { pattern: ['IGI', 'GFG', 'IGI'], key: { I: ing('minecraft:iron_ingot'), G: ing('minecraft:glass'), F: ing('thermal:machine_frame') } }),",
  r"  r('thermal:crystallizer', 'crafting', 'thermal', [{ item: 'thermal:crystallizer' }], [], { pattern: ['DGD', 'GFG', 'DGD'], key: { D: ing('minecraft:diamond'), G: ing('minecraft:glass'), F: ing('thermal:machine_frame') } }),",
  r"  r('thermal:press', 'crafting', 'thermal', [{ item: 'thermal:press' }], [], { pattern: ['IPI', 'IFI', 'IRI'], key: { I: ing('minecraft:iron_ingot'), P: ing('minecraft:piston'), F: ing('thermal:machine_frame'), R: ing('thermal:rf_coil') } }),",
  r"  r('thermal:fluid_encapsulator', 'crafting', 'thermal', [{ item: 'thermal:fluid_encapsulator' }], [], { pattern: ['IGI', 'GFG', 'IRI'], key: { I: ing('minecraft:iron_ingot'), G: ing('minecraft:glass'), F: ing('thermal:machine_frame'), R: ing('thermal:rf_coil') } }),",
]

print("Thermal done")

# ═══════════════════════════════════════════════════════════════════════════
# AE2
# ═══════════════════════════════════════════════════════════════════════════

AE += [
    "// ─── BASE MATERIALS ──────────────────────────────────────────",
  r"  r('ae2:silicon', 'smelting', 'ae2', [{ item: 'ae2:silicon' }], [ing('minecraft:quartz')]),",
  r"  r('ae2:certus_quartz_dust', 'machine', 'ae2', [{ item: 'ae2:certus_quartz_dust' }], [ing('ae2:certus_quartz_crystal')], { energy: 200 }),",
  r"  r('ae2:charged_certus_quartz_crystal', 'ae2:charger', 'ae2', [{ item: 'ae2:charged_certus_quartz_crystal' }], [ing('ae2:certus_quartz_crystal')], { energy: 800 }),",
  r"  r('ae2:fluix_crystal', 'crafting', 'ae2', [{ item: 'ae2:fluix_crystal', count: 2 }], [ing('ae2:charged_certus_quartz_crystal'), ing('minecraft:quartz'), ing('minecraft:redstone')]),",
  r"  r('ae2:fluix_dust', 'machine', 'ae2', [{ item: 'ae2:fluix_dust' }], [ing('ae2:fluix_crystal')], { energy: 200 }),",
  "",
  "// ─── PROCESSORS ───────────────────────────────────────────────",
  r"  r('ae2:printed_silicon', 'ae2:inscriber', 'ae2', [{ item: 'ae2:printed_silicon' }], [ing('ae2:silicon')], { energy: 200 }),",
  r"  r('ae2:printed_calculation_processor', 'ae2:inscriber', 'ae2', [{ item: 'ae2:printed_calculation_processor' }], [ing('ae2:certus_quartz_crystal')], { energy: 400 }),",
  r"  r('ae2:printed_engineering_processor', 'ae2:inscriber', 'ae2', [{ item: 'ae2:printed_engineering_processor' }], [ing('minecraft:diamond')], { energy: 400 }),",
  r"  r('ae2:printed_logic_processor', 'ae2:inscriber', 'ae2', [{ item: 'ae2:printed_logic_processor' }], [ing('minecraft:redstone')], { energy: 400 }),",
  r"  r('ae2:calculation_processor', 'crafting', 'ae2', [{ item: 'ae2:calculation_processor' }], [ing('ae2:printed_calculation_processor'), ing('ae2:printed_silicon'), ing('ae2:fluix_crystal')]),",
  r"  r('ae2:engineering_processor', 'crafting', 'ae2', [{ item: 'ae2:engineering_processor' }], [ing('ae2:printed_engineering_processor'), ing('ae2:printed_silicon'), ing('ae2:fluix_crystal')]),",
  r"  r('ae2:logic_processor', 'crafting', 'ae2', [{ item: 'ae2:logic_processor' }], [ing('ae2:printed_logic_processor'), ing('ae2:printed_silicon'), ing('ae2:fluix_crystal')]),",
  "",
  "// ─── CELL COMPONENTS ──────────────────────────────────────────",
  r"  r('ae2:cell_component_1k', 'crafting', 'ae2', [{ item: 'ae2:cell_component_1k' }], [], { pattern: ['CRC', 'RFR', 'CRC'], key: { C: ing('ae2:calculation_processor'), R: ing('minecraft:redstone'), F: ing('ae2:fluix_crystal') } }),",
  r"  r('ae2:cell_component_4k', 'crafting', 'ae2', [{ item: 'ae2:cell_component_4k' }], [], { pattern: ['GDG', 'DCD', 'GDG'], key: { G: ing('minecraft:gold_ingot'), D: ing('ae2:cell_component_1k'), C: ing('ae2:calculation_processor') } }),",
  r"  r('ae2:cell_component_16k', 'crafting', 'ae2', [{ item: 'ae2:cell_component_16k' }], [], { pattern: ['CDC', 'D4D', 'CDC'], key: { C: ing('ae2:calculation_processor'), D: ing('ae2:cell_component_4k') } }),",
  r"  r('ae2:cell_component_64k', 'crafting', 'ae2', [{ item: 'ae2:cell_component_64k' }], [], { pattern: ['ECE', 'C6C', 'ECE'], key: { E: ing('ae2:engineering_processor'), C: ing('ae2:cell_component_16k') } }),",
  r"  r('ae2:cell_component_256k', 'crafting', 'ae2', [{ item: 'ae2:cell_component_256k' }], [], { pattern: ['DCD', 'C6C', 'DCD'], key: { D: ing('minecraft:diamond_block'), C: ing('ae2:cell_component_64k') } }),",
  "",
  "// ─── CELL HOUSINGS ────────────────────────────────────────────",
  r"  r('ae2:item_cell_housing', 'crafting', 'ae2', [{ item: 'ae2:item_cell_housing' }], [], { pattern: ['FFF', 'F F', 'FFF'], key: { F: ing('ae2:fluix_crystal') } }),",
  r"  r('ae2:fluid_cell_housing', 'crafting', 'ae2', [{ item: 'ae2:fluid_cell_housing' }], [], { pattern: ['FFF', 'FGF', 'FFF'], key: { F: ing('ae2:fluix_crystal'), G: ing('minecraft:glass') } }),",
  "",
  "// ─── CABLES ───────────────────────────────────────────────────",
]
for cable in ['fluix','glass','covered','smart','dense']:
    AE.append(gen_pattern('ae2', f'{cable}_cable', ['FFF','F F','FFF'], {'F': 'ae2:fluix_crystal'}, count=8))

print("AE2 done")

# ═══════════════════════════════════════════════════════════════════════════
# IC2
# ═══════════════════════════════════════════════════════════════════════════

IC += [
    "// ─── BASE MATERIALS ──────────────────────────────────────────",
  r"  r('ic2:refined_iron_ingot', 'ic2:compressor', 'ic2', [{ item: 'ic2:refined_iron_ingot' }], [ing('minecraft:iron_ingot')], { energy: 200 }),",
  r"  r('ic2:rubber', 'ic2:extractor', 'ic2', [{ item: 'ic2:rubber', count: 3 }], [ing('minecraft:oak_log')], { energy: 100 }),",
  r"  r('ic2:carbon_plate', 'ic2:compressor', 'ic2', [{ item: 'ic2:carbon_plate' }], [ing('minecraft:coal', 8)], { energy: 400 }),",
  r"  r('ic2:insulated_copper_cable', 'crafting', 'ic2', [{ item: 'ic2:insulated_copper_cable', count: 6 }], [ing('ic2:rubber', 2), ing('minecraft:copper_ingot', 3)]),",
  r"  r('ic2:glass_fibre_cable', 'crafting', 'ic2', [{ item: 'ic2:glass_fibre_cable', count: 4 }], [ing('ic2:rubber', 2), ing('minecraft:glass', 2)]),",
  "",
  "// ─── CIRCUITS ─────────────────────────────────────────────────",
  r"  r('ic2:electronic_circuit', 'crafting', 'ic2', [{ item: 'ic2:electronic_circuit' }], [], { pattern: ['CRC', 'CCC', 'CRC'], key: { C: ing('ic2:insulated_copper_cable'), R: ing('ic2:refined_iron_ingot') } }),",
  r"  r('ic2:advanced_circuit', 'crafting', 'ic2', [{ item: 'ic2:advanced_circuit' }], [], { pattern: ['CRC', 'CEC', 'RCR'], key: { C: ing('ic2:electronic_circuit'), R: ing('minecraft:redstone'), E: ing('minecraft:glowstone_dust') } }),",
  "",
  "// ─── MACHINE BLOCKS ───────────────────────────────────────────",
  r"  r('ic2:machine_block_basic', 'crafting', 'ic2', [{ item: 'ic2:machine_block_basic' }], [], { pattern: ['III', 'IRI', 'III'], key: { I: ing('ic2:refined_iron_ingot'), R: ing('ic2:electronic_circuit') } }),",
  r"  r('ic2:machine_block_advanced', 'crafting', 'ic2', [{ item: 'ic2:machine_block_advanced' }], [], { pattern: ['CRC', 'RBR', 'CRC'], key: { C: ing('ic2:carbon_plate'), R: ing('ic2:electronic_circuit'), B: ing('ic2:machine_block_basic') } }),",
  "",
  "// ─── ENERGY ───────────────────────────────────────────────────",
  r"  r('ic2:generator', 'crafting', 'ic2', [{ item: 'ic2:generator' }], [], { pattern: ['IBI', 'IFI', 'III'], key: { I: ing('minecraft:iron_ingot'), B: ing('ic2:machine_block_basic'), F: ing('minecraft:furnace') } }),",
  r"  r('ic2:solar_panel', 'crafting', 'ic2', [{ item: 'ic2:solar_panel' }], [], { pattern: ['GGG', 'CSC', 'IGI'], key: { G: ing('minecraft:glass'), C: ing('ic2:electronic_circuit'), S: ing('ic2:generator'), I: ing('ic2:refined_iron_ingot') } }),",
  r"  r('ic2:cesu', 'crafting', 'ic2', [{ item: 'ic2:cesu' }], [], { pattern: ['CBC', 'BCB', 'CBC'], key: { C: ing('ic2:insulated_copper_cable'), B: ing('ic2:machine_block_basic') } }),",
  r"  r('ic2:mf_unit', 'crafting', 'ic2', [{ item: 'ic2:mf_unit' }], [], { pattern: ['CRC', 'RCR', 'CRC'], key: { C: ing('ic2:insulated_copper_cable'), R: ing('ic2:refined_iron_ingot') } }),",
  r"  r('ic2:mfs_unit', 'crafting', 'ic2', [{ item: 'ic2:mfs_unit' }], [], { pattern: ['CAC', 'AMA', 'CAC'], key: { C: ing('ic2:carbon_plate'), A: ing('ic2:advanced_circuit'), M: ing('ic2:mf_unit') } }),",
  r"  r('ic2:storage_battery', 'crafting', 'ic2', [{ item: 'ic2:storage_battery' }], [], { pattern: ['RBR', 'ICI', 'RBR'], key: { R: ing('ic2:refined_iron_ingot'), B: ing('ic2:machine_block_basic'), I: ing('ic2:insulated_copper_cable'), C: ing('ic2:electronic_circuit') } }),",
  "",
  "// ─── MACHINES ─────────────────────────────────────────────────",
  r"  r('ic2:compressor', 'crafting', 'ic2', [{ item: 'ic2:compressor' }], [], { pattern: ['III', 'IMI', 'III'], key: { I: ing('minecraft:iron_ingot'), M: ing('ic2:machine_block_basic') } }),",
  r"  r('ic2:extractor', 'crafting', 'ic2', [{ item: 'ic2:extractor' }], [], { pattern: ['III', 'IMI', 'III'], key: { I: ing('minecraft:iron_ingot'), M: ing('ic2:machine_block_basic') } }),",
  r"  r('ic2:macerator', 'crafting', 'ic2', [{ item: 'ic2:macerator' }], [], { pattern: ['IRI', 'IFI', 'IRI'], key: { I: ing('ic2:refined_iron_ingot'), R: ing('ic2:electronic_circuit'), F: ing('ic2:machine_block_basic') } }),",
]

print("IC2 done")

# ═══════════════════════════════════════════════════════════════════════════

# ─── BULK VANILLA BUILDING BLOCKS ────────────────────────────────────
for mat in ['stone','cobblestone','andesite','diorite','granite','sandstone','bricks','stone_bricks',
            'oak_planks','spruce_planks','birch_planks','jungle_planks','acacia_planks','dark_oak_planks']:
    V.append(gen_pattern('minecraft', f'{mat}_slab', ['SSS'], {'S': f'minecraft:{mat}'}, count=6))
    V.append(gen_pattern('minecraft', f'{mat}_stairs', ['S  ','SS ','SSS'], {'S': f'minecraft:{mat}'}, count=4))

for mat in ['glass','iron']:
    V.append(gen_pattern('minecraft', f'{mat}_pane', ['SSS','SSS'], {'S': f'minecraft:{mat}'}, count=16))

V.append(gen_pattern('minecraft', 'iron_bars', ['III','III'], {'I': 'minecraft:iron_ingot'}, count=16))
V.append(gen_pattern('minecraft', 'ladder', ['S S','SSS','S S'], {'S': 'minecraft:stick'}, count=3))
V.append(gen_pattern('minecraft', 'stone_button', ['S'], {'S': 'minecraft:stone'}))
V.append(gen_pattern('minecraft', 'stone_pressure_plate', ['SS'], {'S': 'minecraft:stone'}))
V.append(gen_pattern('minecraft', 'oak_pressure_plate', ['PP'], {'P': 'minecraft:oak_planks'}))
V.append(gen_pattern('minecraft', 'tripwire_hook', ['I', 'S', 'H'], {'I': 'minecraft:iron_ingot', 'S': 'minecraft:stick', 'H': 'minecraft:oak_planks'}))
V.append(gen_pattern('minecraft', 'daylight_detector', ['GGG', 'QQQ', 'SSS'], {'G': 'minecraft:glass', 'Q': 'minecraft:quartz', 'S': 'minecraft:oak_planks'}))
V.append(gen_pattern('minecraft', 'trapped_chest', [' C ', 'STS', ' S '], {'C': 'minecraft:chest', 'T': 'minecraft:tripwire_hook', 'S': 'minecraft:oak_planks'}))
  # (fire_charge and painting added via gen_pattern)

# ─── BULK MEKANISM PIPES/COMPONENTS ──────────────────────────────────
MEK_pipes = [
    ('basic_mechanical_pipe', 'basic_energy_cube', 'mekanism:osmium_ingot'),
    ('advanced_mechanical_pipe', 'advanced_energy_cube', 'mekanism:alloy_infused'),
    ('basic_chemical_tank', 'basic_energy_cube', 'mekanism:osmium_ingot'),
    ('advanced_chemical_tank', 'advanced_energy_cube', 'mekanism:alloy_infused'),
]
for name, tier, mat in MEK_pipes:
    MK.append(gen_pattern('mekanism', name, ['PPP', 'P P', 'PPP'], {'P': mat}))
    MK.append(gen_pattern('mekanism', name.replace('pipe','cable'), ['PPP', 'P P', 'PPP'], {'P': mat}))

# ─── BULK CREATE DECORATIVE ─────────────────────────────────────────
for col in ['white','orange','magenta','light_blue','yellow','lime','pink','gray','light_gray','cyan','purple','blue','brown','green','red','black']:
    CR.append(gen_pattern('create', f'{col}_seat', ['W', 'S'], {'W': f'minecraft:{col}_wool', 'S': 'create:andesite_alloy'}, count=2))

# ─── BULK THERMAL COILS ─────────────────────────────────────────────
TH.append(gen_pattern('thermal', 'machine_speed_augment', [' M ', 'MSM', ' M '], {'M': 'minecraft:redstone', 'S': 'thermal:redstone_servo'}))
TH.append(gen_pattern('thermal', 'machine_efficiency_augment', [' M ', 'MSM', ' M '], {'M': 'minecraft:glass', 'S': 'thermal:redstone_servo'}))
TH.append(gen_pattern('thermal', 'machine_output_augment', [' M ', 'MSM', ' M '], {'M': 'minecraft:diamond', 'S': 'thermal:redstone_servo'}))

# ─── IC2 CABLING ────────────────────────────────────────────────────
for cable, mat, count, r, g in [('tin','minecraft:tin_ingot',6,None,None),('copper','minecraft:copper_ingot',6,None,None),('gold','minecraft:gold_ingot',4,None,None),('hv','minecraft:diamond',2,'ic2:glass_fibre_cable','ic2:carbon_plate')]:
    if r:
        IC.append(gen_pattern('ic2', f'{cable}_cable', ['CCC', 'CRC', 'CCC'], {'C': mat, 'R': r}, count=count))
    else:
        IC.append(gen_pattern('ic2', f'{cable}_cable', ['CCC', 'C C', 'CCC'], {'C': mat}, count=count))
    if g:
        IC.append(gen_pattern('ic2', f'{cable}_cable', ['CCC', 'CGC', 'CCC'], {'C': mat, 'G': g}, count=count))




# ─── BULK ADDITIONS v2 ──────────────────────────────────────────────

# Vanilla items
V.append(gen_pattern('minecraft', 'compass', [' I ', 'IDI', ' I '], {'I': 'minecraft:iron_ingot', 'D': 'minecraft:redstone'}))
V.append(gen_pattern('minecraft', 'clock', [' I ', 'IGI', ' I '], {'I': 'minecraft:gold_ingot', 'G': 'minecraft:redstone'}))
V.append(gen_pattern('minecraft', 'fishing_rod', ['  I', ' SI', 'S I'], {'I': 'minecraft:stick', 'S': 'minecraft:string'}))
V.append(gen_pattern('minecraft', 'shears', [' I', 'I '], {'I': 'minecraft:iron_ingot'}))
V.append(gen_pattern('minecraft', 'lead', ['SS ', 'SI ', '  S'], {'S': 'minecraft:string', 'I': 'minecraft:slime_ball'}, count=2))
V.append(gen_pattern('minecraft', 'minecart', ['I I', 'III'], {'I': 'minecraft:iron_ingot'}))
V.append(gen_pattern('minecraft', 'chest_minecart', ['C'], {'C': 'minecraft:chest'}, count=0))
V.append(gen_pattern('minecraft', 'hopper_minecart', ['H'], {'H': 'minecraft:hopper'}, count=0))
V.append(gen_pattern('minecraft', 'armor_stand', ['SSS', ' S ', 'S S'], {'S': 'minecraft:stick'}))
V.append(gen_pattern('minecraft', 'item_frame', ['SSS', 'SLS', 'SSS'], {'S': 'minecraft:stick', 'L': 'minecraft:leather'}))
V.append(gen_pattern('minecraft', 'brewing_stand', [' B ', 'CCC'], {'B': 'minecraft:blaze_rod', 'C': 'minecraft:cobblestone'}))
V.append(gen_pattern('minecraft', 'cauldron', ['I I', 'I I', 'III'], {'I': 'minecraft:iron_ingot'}))
V.append(gen_pattern('minecraft', 'bucket', ['I I', ' I '], {'I': 'minecraft:iron_ingot'}))
V.append(gen_pattern('minecraft', 'glass_bottle', ['G G', ' G '], {'G': 'minecraft:glass'}, count=3))
V.append(gen_pattern('minecraft', 'cake', ['MMM', 'SES', 'WWW'], {'M': 'minecraft:milk_bucket', 'S': 'minecraft:sugar', 'E': 'minecraft:egg', 'W': 'minecraft:wheat'}))
V.append(gen_pattern('minecraft', 'pumpkin_pie', ['P', 'S', 'E'], {'P': 'minecraft:pumpkin', 'S': 'minecraft:sugar', 'E': 'minecraft:egg'}))
V.append(gen_pattern('minecraft', 'map', ['PPP', 'PDP', 'PPP'], {'P': 'minecraft:paper', 'D': 'minecraft:compass'}))
V.append(gen_pattern('minecraft', 'furnace_minecart', ['F'], {'F': 'minecraft:furnace'}, count=0))
V.append(gen_pattern('minecraft', 'tnt_minecart', ['T'], {'T': 'minecraft:tnt'}, count=0))

# Mekanism - more tiered content (pipes, cables, tanks)
for tier, alloy in [('basic','alloy_infused'),('advanced','alloy_reinforced'),('elite','alloy_atomic'),('ultimate','alloy_atomic')]:
    mat_map = {'basic': 'mekanism:osmium_ingot', 'advanced': 'mekanism:alloy_infused',
               'elite': 'mekanism:alloy_reinforced', 'ultimate': 'mekanism:alloy_atomic'}
    MK.append(gen_pattern('mekanism', f'{tier}_mechanical_pipe', ['PPP', 'P P', 'PPP'], {'P': mat_map[tier]}, count=8))
    MK.append(gen_pattern('mekanism', f'{tier}_universal_cable', ['PPP', 'P P', 'PPP'], {'P': mat_map[tier]}, count=8))
    MK.append(gen_pattern('mekanism', f'{tier}_chemical_tank', ['P P', 'P P', 'PPP'], {'P': mat_map[tier]}, count=2))
    MK.append(gen_pattern('mekanism', f'{tier}_pressurized_tube', ['PPP', 'P P', 'PPP'], {'P': mat_map[tier]}, count=8))
    MK.append(gen_pattern('mekanism', f'{tier}_logistical_transporter', ['PPP', 'P P', 'PPP'], {'P': mat_map[tier]}, count=8))

# Create - more decorative blocks
for mat, name in [('andesite_alloy','andesite'),('brass_ingot','brass'),('zinc_ingot','zinc')]:
    CR.append(gen_pattern('create', f'{name}_pillar', ['M', 'M'], {'M': f'create:{mat}'}, count=8))
    CR.append(gen_pattern('create', f'polished_{name}', ['MM', 'MM'], {'M': f'create:{mat}'}, count=4))

# Create - doors and trapdoors for metal casings
CR.append(gen_pattern('create', 'andesite_door', ['AA', 'AA', 'AA'], {'A': 'create:andesite_alloy'}, count=3))
CR.append(gen_pattern('create', 'andesite_trapdoor', ['AA', 'AA'], {'A': 'create:andesite_alloy'}, count=2))
CR.append(gen_pattern('create', 'brass_door', ['BB', 'BB', 'BB'], {'B': 'create:brass_sheet'}, count=3))
CR.append(gen_pattern('create', 'brass_trapdoor', ['BB', 'BB'], {'B': 'create:brass_sheet'}, count=2))

# Thermal - more machines and components
TH.append(gen_pattern('thermal', 'energy_cell', ['SRS', 'CGC', 'SRS'], {'S': 'thermal:redstone_servo', 'R': 'thermal:rf_coil', 'C': 'thermal:machine_frame', 'G': 'minecraft:gold_ingot'}))
TH.append(gen_pattern('thermal', 'machine_crafter', ['IGI', 'CFC', 'IRI'], {'I': 'minecraft:iron_ingot', 'G': 'minecraft:glass', 'C': 'thermal:redstone_servo', 'F': 'thermal:machine_frame', 'R': 'thermal:rf_coil'}))
TH.append(gen_pattern('thermal', 'dynamo', ['IGI', 'CFC', 'IGI'], {'I': 'minecraft:iron_ingot', 'G': 'minecraft:redstone', 'C': 'minecraft:redstone', 'F': 'thermal:machine_frame'}))

# AE2 - more infrastructure
AE.append(gen_pattern('ae2', 'terminal', ['FFF', 'FCF', 'FFF'], {'F': 'ae2:fluix_crystal', 'C': 'ae2:calculation_processor'}))
AE.append(gen_pattern('ae2', 'crafting_terminal', ['FFF', 'FCF', 'FWF'], {'F': 'ae2:fluix_crystal', 'C': 'ae2:calculation_processor', 'W': 'ae2:terminal'}))
AE.append(gen_pattern('ae2', 'me_drive', ['FFF', 'FCF', 'FFF'], {'F': 'ae2:fluix_crystal', 'C': 'ae2:engineering_processor'}))
AE.append(gen_pattern('ae2', 'me_chest', ['FFF', 'FCF', 'FFF'], {'F': 'ae2:fluix_crystal', 'C': 'ae2:logic_processor'}))
AE.append(gen_pattern('ae2', 'energy_acceptor', ['FFF', 'FC ', 'FFF'], {'F': 'ae2:fluix_crystal', 'C': 'ae2:engineering_processor'}))
AE.append(gen_pattern('ae2', 'controller', ['FFF', 'FCF', 'FFF'], {'F': 'ae2:fluix_crystal', 'C': 'ae2:logic_processor'}))

# IC2 - more cabling and upgrades
IC.append(gen_pattern('ic2', 'copper_cable', ['C C', ' C ', 'C C'], {'C': 'minecraft:copper_ingot'}, count=6))
IC.append(gen_pattern('ic2', 'gold_cable', ['C C', ' C ', 'C C'], {'C': 'minecraft:gold_ingot'}, count=4))
IC.append(gen_pattern('ic2', 'glass_fibre_cable_v2', ['GCG', 'CCC', 'GCG'], {'G': 'minecraft:glass', 'C': 'ic2:refined_iron_ingot'}, count=4))
IC.append(gen_pattern('ic2', 'overclocker_upgrade', ['C', 'R', 'C'], {'C': 'ic2:electronic_circuit', 'R': 'minecraft:redstone'}))
IC.append(gen_pattern('ic2', 'transformer_upgrade', ['C', 'G', 'C'], {'C': 'ic2:electronic_circuit', 'G': 'minecraft:gold_ingot'}))
IC.append(gen_pattern('ic2', 'energy_storage_upgrade', ['C', 'B', 'C'], {'C': 'ic2:electronic_circuit', 'B': 'ic2:storage_battery'}))
IC.append(gen_pattern('ic2', 'thermal_centrifuge', ['III', 'IMI', 'IRI'], {'I': 'ic2:refined_iron_ingot', 'M': 'ic2:machine_block_advanced', 'R': 'ic2:electronic_circuit'}))
IC.append(gen_pattern('ic2', 'recycler', ['III', 'IMI', 'ICI'], {'I': 'ic2:refined_iron_ingot', 'M': 'ic2:machine_block_basic', 'C': 'ic2:electronic_circuit'}))



# ─── BULK ADDITIONS v3 ──────────────────────────────────────────────

# Vanilla: more building blocks, wool, carpets, beds
for col in ['white','orange','magenta','light_blue','yellow','lime','pink','gray','light_gray','cyan','purple','blue','brown','green','red','black']:
    V.append(gen_pattern('minecraft', f'{col}_carpet', ['WW'], {'W': f'minecraft:{col}_wool'}, count=3))
    V.append(gen_pattern('minecraft', f'{col}_bed', ['WWW', 'PPP'], {'W': f'minecraft:{col}_wool', 'P': 'minecraft:oak_planks'}))
    V.append(gen_pattern('minecraft', f'{col}_wool', ['SS'], {'S': 'minecraft:string'}, count=0))

# Vanilla: more redstone components
V.append(gen_pattern('minecraft', 'piston_extension_pole', ['I', 'R', 'I'], {'I': 'minecraft:iron_ingot', 'R': 'minecraft:redstone_block'}))
V.append(gen_pattern('minecraft', 'activator_rail', ['ITI', 'IRI', 'ITI'], {'I': 'minecraft:iron_ingot', 'T': 'minecraft:redstone_torch', 'R': 'minecraft:redstone'}, count=6))
V.append(gen_pattern('minecraft', 'detector_rail', ['I I', 'IPI', 'IRI'], {'I': 'minecraft:iron_ingot', 'P': 'minecraft:stone_pressure_plate', 'R': 'minecraft:redstone'}, count=6))
V.append(gen_pattern('minecraft', 'heavy_weighted_pressure_plate', ['II'], {'I': 'minecraft:iron_ingot'}))
V.append(gen_pattern('minecraft', 'light_weighted_pressure_plate', ['GG'], {'G': 'minecraft:gold_ingot'}))

# Mekanism: ore blocks, more machines
for ore in ['osmium', 'tin', 'lead', 'uranium']:
    MK.append(gen_pattern('mekanism', f'{ore}_block', ['MMM', 'MMM', 'MMM'], {'M': f'mekanism:{ore}_ingot'}))
    MK.append(gen_pattern('mekanism', f'{ore}_ore', ['MMM', 'MMM', 'MMM'], {'M': f'mekanism:raw_{ore}'}, count=0))
    MK.append(gen_pattern('mekanism', f'raw_{ore}', ['M', 'M', 'M'], {'M': f'mekanism:{ore}_ore'}, count=0))

MK.append(gen_pattern('mekanism', 'smelter', ['III', 'IF ', 'III'], {'I': 'mekanism:osmium_ingot', 'F': 'mekanism:control_circuit_basic'}))
MK.append(gen_pattern('mekanism', 'injection_chamber', ['OAO', 'C C', 'OAO'], {'O': 'mekanism:osmium_ingot', 'A': 'mekanism:alloy_reinforced', 'C': 'mekanism:control_circuit_advanced'}))

# Create: more machine types
CR.append(gen_pattern('create', 'mechanical_crafter', ['ACA', 'CSC', 'ACA'], {'A': 'create:andesite_casing', 'C': 'create:cogwheel', 'S': 'create:precision_mechanism'}))
CR.append(gen_pattern('create', 'sequenced_gearshift', [' C ', 'CSC', ' C '], {'C': 'create:cogwheel', 'S': 'create:shaft'}))
CR.append(gen_pattern('create', 'rotation_speed_controller', ['ACA', 'CSC', 'ACA'], {'A': 'create:brass_casing', 'C': 'create:large_cogwheel', 'S': 'create:precision_mechanism'}))
CR.append(gen_pattern('create', 'portable_storage_interface', [' A ', 'ACA', ' A '], {'A': 'create:andesite_alloy', 'C': 'create:andesite_casing'}))
CR.append(gen_pattern('create', 'mechanical_arm', ['CC ', 'SAC', ' CC'], {'C': 'create:andesite_alloy', 'S': 'create:shaft', 'A': 'create:andesite_casing'}))
CR.append(gen_pattern('create', 'mechanical_drill', [' I ', 'ISI', 'ACA'], {'I': 'minecraft:iron_ingot', 'S': 'create:shaft', 'A': 'create:andesite_casing'}))
CR.append(gen_pattern('create', 'mechanical_harvester', ['SS ', 'SMS', ' SAS'], {'S': 'create:andesite_alloy', 'M': 'create:mechanical_saw', 'A': 'create:andesite_casing'}))

# Thermal: fluxducts, servos, coils
for tier, mat in [('basic','minecraft:iron_ingot'),('hardened','thermal:invar_ingot'),('reinforced','thermal:signalum_ingot'),('signalum','thermal:signalum_ingot')]:
    TH.append(gen_pattern('thermal', f'{tier}_fluxduct', ['DD', 'DD'], {'D': mat}, count=4))
    TH.append(gen_pattern('thermal', f'{tier}_fluiduct', ['DD', 'DD'], {'D': mat}, count=4))
    TH.append(gen_pattern('thermal', f'{tier}_itemduct', ['DD', 'DD'], {'D': mat}, count=4))

TH.append(gen_pattern('thermal', 'device_composter', ['GFG', 'GDG', 'GFG'], {'G': 'minecraft:iron_ingot', 'F': 'thermal:machine_frame', 'D': 'thermal:redstone_servo'}))
TH.append(gen_pattern('thermal', 'device_water_gen', ['GFG', 'GCG', 'GFG'], {'G': 'minecraft:iron_ingot', 'F': 'thermal:machine_frame', 'C': 'thermal:rf_coil'}))

# AE2: more network components
AE.append(gen_pattern('ae2', 'interface', ['FFF', 'FCF', 'FFF'], {'F': 'ae2:fluix_crystal', 'C': 'ae2:calculation_processor'}))
AE.append(gen_pattern('ae2', 'import_bus', ['FFF', 'FCF', 'FFF'], {'F': 'ae2:fluix_crystal', 'C': 'ae2:engineering_processor'}))
AE.append(gen_pattern('ae2', 'export_bus', ['FFF', 'FCF', 'FFF'], {'F': 'ae2:fluix_crystal', 'C': 'ae2:logic_processor'}))
AE.append(gen_pattern('ae2', 'storage_bus', ['FFF', 'FCF', 'FFF'], {'F': 'ae2:fluix_crystal', 'C': 'ae2:engineering_processor'}))
AE.append(gen_pattern('ae2', 'level_emitter', ['FFF', 'FCF', 'FFF'], {'F': 'ae2:fluix_crystal', 'C': 'ae2:logic_processor'}))
AE.append(gen_pattern('ae2', 'annihilation_plane', ['FFF', 'FCF', 'FFF'], {'F': 'ae2:fluix_crystal', 'C': 'ae2:engineering_processor'}))
AE.append(gen_pattern('ae2', 'formation_plane', ['FFF', 'FCF', 'FFF'], {'F': 'ae2:fluix_crystal', 'C': 'ae2:engineering_processor'}))

# IC2: more machines and cables
for cable_type, mat in [('copper','minecraft:copper_ingot'),('gold','minecraft:gold_ingot'),('iron','minecraft:iron_ingot')]:
    IC.append(gen_pattern('ic2', f'{cable}_cable_insulated', ['CMC', 'C C', 'CMC'], {'C': mat, 'M': 'ic2:machine_block_basic'}, count=6))

IC.append(gen_pattern('ic2', 'induction_furnace', ['CIC', 'IFM', 'CIC'], {'C': 'ic2:electronic_circuit', 'I': 'ic2:refined_iron_ingot', 'F': 'ic2:machine_block_advanced', 'M': 'ic2:machine_block_basic'}))
IC.append(gen_pattern('ic2', 'magnetizer', ['IRI', 'CFC', 'IXI'], {'I': 'ic2:refined_iron_ingot', 'R': 'minecraft:redstone', 'C': 'ic2:electronic_circuit', 'F': 'ic2:machine_block_basic', 'X': 'minecraft:iron_ingot'}))
IC.append(gen_pattern('ic2', 'mining_drill', ['II', 'IC', ' S'], {'I': 'ic2:refined_iron_ingot', 'C': 'ic2:electronic_circuit', 'S': 'ic2:storage_battery'}))
IC.append(gen_pattern('ic2', 'diamond_drill', ['DD', 'DC', ' S'], {'D': 'minecraft:diamond', 'C': 'ic2:electronic_circuit', 'S': 'ic2:storage_battery'}))

# FINAL OUTPUT
# ═══════════════════════════════════════════════════════════════════════════

write_recipes('vanilla.ts', 'V', '\n'.join(V))
write_recipes('mekanism.ts', 'MEK', '\n'.join(MK))
write_recipes('create.ts', 'CR', '\n'.join(CR))
write_recipes('thermal.ts', 'TH', '\n'.join(TH))
write_recipes('ae2.ts', 'AE', '\n'.join(AE))
write_recipes('ic2.ts', 'IC', '\n'.join(IC))

cnt_v = sum(1 for l in V if "r('" in l)
cnt_m = sum(1 for l in MK if "r('" in l)
cnt_c = sum(1 for l in CR if "r('" in l)
cnt_t = sum(1 for l in TH if "r('" in l)
cnt_a = sum(1 for l in AE if "r('" in l)
cnt_i = sum(1 for l in IC if "r('" in l)
total = cnt_v + cnt_m + cnt_c + cnt_t + cnt_a + cnt_i

print(f"✓ vanilla.ts: {cnt_v}")
print(f"✓ mekanism.ts: {cnt_m}")
print(f"✓ create.ts: {cnt_c}")
print(f"✓ thermal.ts: {cnt_t}")
print(f"✓ ae2.ts: {cnt_a}")
print(f"✓ ic2.ts: {cnt_i}")
print(f"\n✅ {total} recipes generated.")
