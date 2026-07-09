#!/usr/bin/env python3
"""Generate processing recipe files for Mekanism & Thermal"""
import os, sys; sys.path.insert(0, os.path.dirname(__file__))
from generate_base import *

ores = ["iron","gold","copper","osmium","tin","lead","uranium","silver","nickel"]
ore_mods = {"iron":"minecraft","gold":"minecraft","copper":"minecraft",
            "osmium":"mekanism","tin":"mekanism","lead":"mekanism","uranium":"mekanism",
            "silver":"thermal","nickel":"thermal"}

def gen_mek_proc():
    lines = []
    lines.append('import { r, ing } from "./helpers";')
    lines.append('import type { Recipe } from "../../types";')
    lines.append('const MEK_PROC: Recipe[] = [')
    
    for ore in ores:
        mod = ore_mods[ore]
        raw = f"{mod}:raw_{ore}" if mod in ("mekanism","thermal") else f"minecraft:raw_{ore}"
        dust = f"mekanism:{ore}_dust"
        lines.append(r_simple(f"mekanism:{ore}_enrich","mekanism:enrichment_chamber","mekanism",dust,2,[(raw,1)],"energy:200"))
    
    for ore in ores:
        mod = ore_mods[ore]
        ore_id = f"{mod}:{ore}_ore"
        dust = f"mekanism:{ore}_dust"
        lines.append(r_simple(f"mekanism:{ore}_enrich_ore","mekanism:enrichment_chamber","mekanism",dust,4,[(ore_id,1)],"energy:400"))
    
    for ore in ores:
        mod = ore_mods[ore]
        raw = f"{mod}:raw_{ore}" if mod in ("mekanism","thermal") else f"minecraft:raw_{ore}"
        ddust = f"mekanism:{ore}_dirty_dust"
        cdust = f"mekanism:{ore}_dust"
        lines.append(r_simple(f"mekanism:{ore}_crush","mekanism:crusher","mekanism",ddust,1,[(raw,1)],"energy:200"))
        lines.append(r_simple(f"mekanism:{ore}_dirty_enrich","mekanism:enrichment_chamber","mekanism",cdust,1,[(ddust,1)],"energy:100"))
    
    for ore in ores:
        mod = ore_mods[ore]
        raw = f"{mod}:raw_{ore}" if mod in ("mekanism","thermal") else f"minecraft:raw_{ore}"
        shard = f"mekanism:{ore}_shard"
        dust = f"mekanism:{ore}_dust"
        lines.append(r_simple(f"mekanism:{ore}_purify","mekanism:purification_chamber","mekanism",shard,3,[(raw,1)],"energy:400"))
        lines.append(r_simple(f"mekanism:{ore}_shard_enrich","mekanism:enrichment_chamber","mekanism",dust,1,[(shard,1)],"energy:100"))
    
    for ore in ores:
        mod = ore_mods[ore]
        raw = f"{mod}:raw_{ore}" if mod in ("mekanism","thermal") else f"minecraft:raw_{ore}"
        lines.append(r_simple(f"mekanism:{ore}_inject","mekanism:chemical_injection_chamber","mekanism",f"mekanism:{ore}_dirty_slurry",1,[(raw,1)],"energy:600"))
    
    for ore in ores:
        dirty = f"mekanism:{ore}_dirty_slurry"
        clean = f"mekanism:{ore}_clean_slurry"
        crystal = f"mekanism:{ore}_crystal"
        dust = f"mekanism:{ore}_dust"
        lines.append(r_simple(f"mekanism:{ore}_wash","mekanism:chemical_washer","mekanism",clean,1,[(dirty,1)],"energy:400"))
        lines.append(r_simple(f"mekanism:{ore}_crystalize","mekanism:chemical_crystallizer","mekanism",crystal,1,[(clean,1)],"energy:400"))
        lines.append(r_simple(f"mekanism:{ore}_crystal_enrich","mekanism:enrichment_chamber","mekanism",dust,1,[(crystal,1)],"energy:100"))
    
    for ore in ores:
        ingot = ore_mods[ore] + ":" + ore + "_ingot"
        dust = f"mekanism:{ore}_dust"
        lines.append(r_simple(f"mekanism:{ore}_dust_smelt","smelting","mekanism",ingot,1,[(dust,1)]))
    
    for ore in ores:
        crystal = f"mekanism:{ore}_crystal"
        lines.append(r_simple(f"mekanism:{ore}_compress","mekanism:osmium_compressor","mekanism",f"mekanism:{ore}_compressed",1,[(crystal,1)],"energy:600"))
    
    lines.append("];")
    lines.append("export default MEK_PROC;")
    return "\n".join(lines)

def gen_th_proc():
    lines = []
    lines.append('import { r, ing } from "./helpers";')
    lines.append('import type { Recipe } from "../../types";')
    lines.append("const TH_PROC: Recipe[] = [")
    
    for ore in ores:
        mod = ore_mods[ore]
        ore_id = f"{mod}:{ore}_ore"
        dust = f"thermal:{ore}_dust"
        raw = f"{mod}:raw_{ore}" if mod in ("mekanism","thermal") else f"minecraft:raw_{ore}"
        lines.append(r_simple(f"thermal:{ore}_pulverize","thermal:pulverizer","thermal",dust,2,[(ore_id,1)],"energy:400"))
        lines.append(r_simple(f"thermal:{ore}_pulverize_raw","thermal:pulverizer","thermal",dust,1,[(raw,1)],"energy:200"))
    
    for ore in ores:
        ingot = ore_mods[ore] + ":" + ore + "_ingot"
        dust = f"thermal:{ore}_dust"
        lines.append(r_simple(f"thermal:{ore}_dust_smelt","smelting","thermal",ingot,1,[(dust,1)]))
    
    alloy_list = [
        ("thermal:bronze_ingot  ", [("minecraft:copper_ingot", 3), ("thermal:tin_ingot", 1)]),
        ("thermal:constantan_ingot", [("minecraft:copper_ingot", 1), ("thermal:nickel_ingot", 1)]),
        ("thermal:electrum_ingot  ", [("minecraft:gold_ingot", 1), ("thermal:silver_ingot", 1)]),
        ("thermal:invar_ingot", [("minecraft:iron_ingot", 2), ("thermal:nickel_ingot", 1)]),
    ]
    for out, ins in alloy_list:
        name = out.strip().split(":")[1]
        lines.append(r_simple(f"thermal:{name}_alloy","thermal:induction_smelter","thermal",out.strip(),1,ins,"energy:400"))
    
    lines.append("];")
    lines.append("export default TH_PROC;")
    return "\n".join(lines)

if __name__ == "__main__":
    me = gen_mek_proc()
    th = gen_th_proc()
    os.makedirs("src/data/recipes", exist_ok=True)
    with open("src/data/recipes/mekanism-processing.ts","w") as f: f.write(me)
    with open("src/data/recipes/thermal-processing.ts","w") as f: f.write(th)
    print(f"Mek processing: {me.count(chr(114)+chr(40))} recipes")
    print(f"Thermal processing: {th.count(chr(114)+chr(40))} recipes")
    print("Done")
