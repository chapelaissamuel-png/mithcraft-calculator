#!/usr/bin/env python3
"""Generate processing recipes — all ore chains per mod"""
import os, sys; sys.path.insert(0, os.path.dirname(__file__))
from generate_base import *

def generate():
    all_lines = []
    
    # ─── MEKANISM PROCESSING ───
    lines = []
    write_header(lines, "MEK_PROC"); lines.append("")
    ores = {
        "iron":     {"mod":"minecraft","ingot":"minecraft:iron_ingot"},
        "gold":     {"mod":"minecraft","ingot":"minecraft:gold_ingot"},
        "copper":   {"mod":"minecraft","ingot":"minecraft:copper_ingot"},
        "osmium":   {"mod":"mekanism","ingot":"mekanism:osmium_ingot"},
        "tin":      {"mod":"mekanism","ingot":"mekanism:tin_ingot"},
        "lead":     {"mod":"mekanism","ingot":"mekanism:lead_ingot"},
        "uranium":  {"mod":"mekanism","ingot":"mekanism:uranium_ingot"},
        "silver":   {"mod":"thermal","ingot":"thermal:silver_ingot"},
        "nickel":   {"mod":"thermal","ingot":"thermal:nickel_ingot"},
    }
    
    lines.append("// ─── ENRICHMENT (RAW→DUST×2) ─────────────────────────────────")
    for ore, info in ores.items():
        mod = info["mod"]
        raw = f"{mod}:raw_{ore}" if mod in ("mekanism","thermal") else f"minecraft:raw_{ore}"
        dust = f"mekanism:{ore}_dust"
        lines.append(r_simple(f"mekanism:{ore}_enrich","mekanism:enrichment_chamber","mekanism",dust,2,[(raw,1)],"energy:200"))
    
    lines.append("\n// ─── ENRICHMENT (ORE→DUST×4) ────────────────────────────────")
    for ore in ores:
        dust = f"mekanism:{ore}_dust"
        ore_id = f"{ores[ore]['mod']}:{ore}_ore"
        lines.append(r_simple(f"mekanism:{ore}_enrich_ore","mekanism:enrichment_chamber","mekanism",dust,4,[(ore_id,1)],"energy:400"))
    
    lines.append("\n// ─── CRUSHER (RAW→DIRTY DUST) ───────────────────────────────")
    for ore, info in ores.items():
        mod = info["mod"]
        raw = f"{mod}:raw_{ore}" if mod in ("mekanism","thermal") else f"minecraft:raw_{ore}"
        dust = f"mekanism:{ore}_dirty_dust"
        lines.append(r_simple(f"mekanism:{ore}_crush","mekanism:crusher","mekanism",dust,1,[(raw,1)],"energy:200"))
        # Also enrich dirty dust
        clean_dust = f"mekanism:{ore}_dust"
        lines.append(r_simple(f"mekanism:{ore}_dirty_enrich","mekanism:enrichment_chamber","mekanism",clean_dust,1,[(dust,1)],"energy:100"))
    
    lines.append("\n// ─── PURIFICATION (RAW→SHARD) ───────────────────────────────")
    for ore, info in ores.items():
        mod = info["mod"]
        raw = f"{mod}:raw_{ore}" if mod in ("mekanism","thermal") else f"minecraft:raw_{ore}"
        shard = f"mekanism:{ore}_shard"
        lines.append(r_simple(f"mekanism:{ore}_purify","mekanism:purification_chamber","mekanism",shard,3,[(raw,1)],"energy:400"))
        # Shard → Dust
        lines.append(r_simple(f"mekanism:{ore}_shard_enrich","mekanism:enrichment_chamber","mekanism",f"mekanism:{ore}_dust",1,[(shard,1)],"energy:100"))
    
    lines.append("\n// ─── INJECTION (RAW→DIRTY SLURRY) ───────────────────────────")
    for ore, info in ores.items():
        mod = info["mod"]
        raw = f"{mod}:raw_{ore}" if mod in ("mekanism","thermal") else f"minecraft:raw_{ore}"
        slurry = f"mekanism:{ore}_dirty_slurry"
        lines.append(r_simple(f"mekanism:{ore}_inject","mekanism:chemical_injection_chamber","mekanism",slurry,1,[(raw,1)],"energy:600"))
    
    lines.append("\n// ─── WASHING (DIRTY→CLEAN SLURRY) ───────────────────────────")
    for ore in ores:
        dirty = f"mekanism:{ore}_dirty_slurry"
        clean = f"mekanism:{ore}_clean_slurry"
        lines.append(r_simple(f"mekanism:{ore}_wash","mekanism:chemical_washer","mekanism",clean,1,[(dirty,1)],"energy:400"))
        # Crystalize
        lines.append(r_simple(f"mekanism:{ore}_crystalize","mekanism:chemical_crystallizer","mekanism",f"mekanism:{ore}_crystal",1,[(clean,1)],"energy:400"))
        # Crystal → Dust
        lines.append(r_simple(f"mekanism:{ore}_crystal_enrich","mekanism:enrichment_chamber","mekanism",f"mekanism:{ore}_dust",1,[(f"mekanism:{ore}_crystal",1)],"energy:100"))
    
    # Smelting chain
    lines.append("\n// ─── DUST→INGOT (SMELTING) ───────────────────────────────────")
    for ore, info in ores.items():
        ingot = info["ingot"]
        dust = f"mekanism:{ore}_dust"
        lines.append(r_simple(f"mekanism:{ore}_dust_smelt","smelting","mekanism",ingot,1,[(dust,1)]))
    
    # COMPRESSOR CHAIN
    lines.append("\n// ─── OSMIUM COMPRESSOR ────────────────────────────────────────")
    for ore in ["iron","gold","copper","osmium","tin","lead","uranium","silver","nickel"]:
        info = ores.get(ore, {})
        if not info: continue
        dust = f"mekanism:{ore}_dust"
        crystal = f"mekanism:{ore}_crystal"
        compressed = f"mekanism:{ore}_compressed"
        lines.append(r_simple(f"mekanism:{ore}_compress","mekanism:osmium_compressor","mekanism",compressed,1,[(crystal,1)],"energy:600"))
    
    write_footer(lines, "MEK_PROC")
    all_lines.append("\n".join(lines))
    
    # ─── CREATE PROCESSING ───
    lines = []
    write_header(lines, "CR_PROC"); lines.append("")
    lines.append("// ─── MILLSTONE (ORE→DUST) ────────────────────────────────────")
    for ore in ores:
        mod = ores[ore]["mod"]
        ore_id = f"{mod}:{ore}_ore"
        dust = f"create:{ore}_dust"
        lines.append(r_simple(f"create:{ore}_mill","create:millstone","create",dust,2,[(ore_id,1)],"energy:200"))
    
    lines.append("\n// ─── CRUSHING WHEELS (ORE→CRUSHED + BYPRODUCT) ────────────────")
    for ore in ores:
        mod = ores[ore]["mod"]
        ore_id = f"{mod}:{ore}_ore"
        crushed = f"create:{ore}_ore_crushed"
        byproduct = ores.get(ore, {}).get("byproduct", "minecraft:cobblestone")
        lines.append(r_simple(f"create:{ore}_crush","create:crushing_wheels","create",crushed,2,[(ore_id,1)],"energy:400"))
    
    lines.append("\n// ─── CRUSHED→SMELT/CRUSHED→INGOT ─────────────────────────────")
    for ore, info in ores.items():
        crushed = f"create:{ore}_ore_crushed"
        ingot = info["ingot"]
        lines.append(r_simple(f"create:{ore}_crushed_smelt","smelting","create",ingot,1,[(crushed,1)]))
        lines.append(r_simple(f"create:{ore}_crushed_blast","blasting","create",ingot,1,[(crushed,1)]))
    
    lines.append("\n// ─── MIXING (ALLOYS) ─────────────────────────────────────────")
    mix_recipes = [
        ("create:brass_mix","create:brass_ingot",[("minecraft:copper_ingot",1),("create:zinc_ingot",1)]),
    ]
    for rid, out, ins in mix_recipes:
        lines.append(r_simple(rid,"create:mixing","create",out,1,ins,"energy:200"))
    
    lines.append("\n// ─── PRESSING ─────────────────────────────────────────────────")
    press_recipes = [
        ("create:iron_press","minecraft:iron_ingot",[("minecraft:iron_block",1)]),
        ("create:gold_press","minecraft:gold_ingot",[("minecraft:gold_block",1)]),
    ]
    for rid, out, ins in press_recipes:
        lines.append(r_simple(rid,"create:pressing","create",out,4,ins,"energy:200"))
    
    write_footer(lines, "CR_PROC")
    all_lines.append("\n".join(lines))
    
    # ─── THERMAL PROCESSING ───
    lines = []
    write_header(lines, "TH_PROC"); lines.append("")
    lines.append("// ─── PULVERIZER (ORE→DUST×2) ─────────────────────────────────")
    for ore, info in ores.items():
        mod = info["mod"]
        ore_id = f"{mod}:{ore}_ore"
        dust = f"thermal:{ore}_dust"
        lines.append(r_simple(f"thermal:{ore}_pulverize","thermal:pulverizer","thermal",dust,2,[(ore_id,1)],"energy:400"))
    
    lines.append("\n// ─── PULVERIZER (RAW→DUST×1.5) ──────────────────────────────")
    for ore, info in ores.items():
        mod = info["mod"]
        raw = f"{mod}:raw_{ore}" if mod in ("mekanism","thermal") else f"minecraft:raw_{ore}"
        dust = f"thermal:{ore}_dust"
        lines.append(r_simple(f"thermal:{ore}_pulverize_raw","thermal:pulverizer","thermal",dust,1,[(raw,1)],"energy:200"))
    
    lines.append("\n// ─── SMELTING FROM DUST ──────────────────────────────────────")
    for ore, info in ores.items():
        ingot = info["ingot"]
        dust = f"thermal:{ore}_dust"
        lines.append(r_simple(f"thermal:{ore}_dust_smelt","smelting","thermal",ingot,1,[(dust,1)]))
    
    lines.append("\n// ─── CENTRIFUGE ──────────────────────────────────────────────")
    for ore in ["iron","gold","copper"]:
        dust = f"thermal:{ore}_dust"
        ingot = f"minecraft:{ore}_ingot"
        lines.append(r_simple(f"thermal:{ore}_centrifuge","thermal:centrifuge","thermal",ingot,1,[(dust,2)],"energy:400"))
    
    write_footer(lines, "TH_PROC")
    all_lines.append("\n".join(lines))
    
    return "\n\n".join(all_lines)

# Export all separately
def write_file(path, lines):
    with open(path, "w") as f:
        f.write(lines)

if __name__ == "__main__":
    gen = generate()
    # Write mekanism processing
    mek_start = gen.find("import")
    mek_end = gen.find("import", mek_start + 1)
    # Actually, let's just write 3 separate files manually
    print("Generated processing recipes")
    print(f"Total: {gen.count(\"r('\")} recipes")
