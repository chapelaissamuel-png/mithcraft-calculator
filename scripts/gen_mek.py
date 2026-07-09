#!/usr/bin/env python3
"""Generate mekanism.ts"""
import os, sys; sys.path.insert(0, os.path.dirname(__file__))
from generate_base import *

def generate():
    lines = []
    write_header(lines, "MEK"); lines.append("")
    
    ores = ["osmium","tin","lead","uranium"]
    all_ores = ores + ["copper","gold","iron"]
    
    lines.append("// ─── ORE → INGOT ────────────────────────────────────────────")
    for ore in all_ores:
        ingot = f"minecraft:{ore}_ingot" if ore in ("copper","gold","iron") else f"mekanism:{ore}_ingot"
        raw = f"minecraft:raw_{ore}" if ore in ("copper","gold","iron") else f"mekanism:raw_{ore}"
        lines.append(r_simple(f"mekanism:{ore}_ingot_smelt","smelting","mekanism",ingot,1,[(raw,1)]))
        lines.append(r_simple(f"mekanism:{ore}_ingot_blast","blasting","mekanism",ingot,1,[(raw,1)]))
    
    lines.append("\n// ─── BLOCKS ────────────────────────────────────────────────")
    for ore in ores:
        ingot = f"mekanism:{ore}_ingot"
        block = f"mekanism:{ore}_block"
        lines.append(r_shaped(block,"mekanism",block,1,["III","III","III"],{"I":ing(ingot)}))
        lines.append(r_shaped(f"{ore}_ingot_from_block","mekanism",ingot,9,["I"],{"I":ing(block)}))
    
    lines.append("\n// ─── RAW ORES ────────────────────────────────────────────────")
    for ore in ores:
        raw = f"mekanism:raw_{ore}"
        block = f"mekanism:raw_{ore}_block"
        lines.append(r_shaped(block,"mekanism",block,1,["III","III","III"],{"I":ing(raw)}))
        lines.append(r_shaped(f"raw_{ore}_from_block","mekanism",raw,9,["I"],{"I":ing(block)}))
    
    lines.append("\n// ─── DUSTS (ENRICHMENT) ──────────────────────────────────────")
    for ore in all_ores:
        dust = f"mekanism:{ore}_dust"
        raw = f"minecraft:raw_{ore}" if ore in ("copper","gold","iron") else f"mekanism:raw_{ore}"
        lines.append(r_simple(f"mekanism:{ore}_dust_enrich","mekanism:enrichment_chamber","mekanism",dust,2,[(raw,1)]))
    
    lines.append("\n// ─── ALLOYS ────────────────────────────────────────────────")
    alloys = [
        ("mekanism:enriched_iron",1,[("minecraft:iron_ingot",1)]),
        ("mekanism:alloy_infused",1,[("minecraft:iron_ingot",1),("mekanism:tin_ingot",2)]),
        ("mekanism:alloy_reinforced",1,[("mekanism:alloy_infused",2),("minecraft:diamond",1)]),
        ("mekanism:alloy_atomic",1,[("mekanism:alloy_reinforced",2),("mekanism:refined_obsidian_ingot",1)]),
    ]
    for item,cnt,ins in alloys:
        lines.append(r_simple(f"{item.split(':')[1]}_alloy","mekanism:metallurgic_infuser","mekanism",item,cnt,ins,"energy:400"))
    
    lines.append("\n// ─── REFINED MATERIALS ─────────────────────────────────────")
    lines.append(r_simple("mekanism:refined_obsidian_ingot","mekanism:enrichment_chamber","mekanism","mekanism:refined_obsidian_ingot",1,[("minecraft:obsidian",4)],"energy:800"))
    lines.append(r_simple("mekanism:refined_glowstone_ingot","mekanism:enrichment_chamber","mekanism","mekanism:refined_glowstone_ingot",1,[("minecraft:glowstone",4)],"energy:800"))
    
    lines.append("\n// ─── CONTROL CIRCUITS ─────────────────────────────────────────")
    for tier,mat in [("basic","osmium_ingot"),("advanced","alloy_infused"),("elite","alloy_reinforced"),("ultimate","alloy_atomic")]:
        mat_id = f"mekanism:{mat}" if ":" not in mat else mat
        lines.append(r_shaped(f"mekanism:control_circuit_{tier}","mekanism",f"mekanism:control_circuit_{tier}",1,
            ["PPP","RPR","PPP"],{"P":ing(mat_id),"R":ing("minecraft:redstone")}))
    
    lines.append("\n// ─── ENERGY TABLETS & CUBES ─────────────────────────────────")
    lines.append(r_shaped("mekanism:energy_tablet","mekanism","mekanism:energy_tablet",1,
        [" P ","PCP"," P "],{"P":ing("mekanism:osmium_ingot"),"C":ing("mekanism:control_circuit_basic")}))
    for tier in ["basic","advanced","elite","ultimate"]:
        mat = f"mekanism:{tier}_control_circuit" if tier != "basic" else "mekanism:control_circuit_basic"
        alloy = f"mekanism:{'alloy_infused' if tier == 'basic' else 'alloy_' + ('infused' if tier == 'advanced' else 'reinforced' if tier == 'elite' else 'atomic')}"
        lines.append(r_shaped(f"mekanism:{tier}_energy_cube","mekanism",f"mekanism:{tier}_energy_cube",1,
            ["CMC","CEC","CMC"],{"C":ing(mat),"M":ing(alloy),"E":ing("mekanism:energy_tablet")}))
    
    lines.append("\n// ─── PIPES, CABLES, TANKS ───────────────────────────────────")
    pipe_types = ["mechanical_pipe","universal_cable","pressurized_tube","logistical_transporter","chemical_tank"]
    tier_mats = {"basic":"mekanism:osmium_ingot","advanced":"mekanism:alloy_infused",
                 "elite":"mekanism:alloy_reinforced","ultimate":"mekanism:alloy_atomic"}
    for tier, mat in tier_mats.items():
        for ptype in pipe_types:
            cnt = 2 if "tank" in ptype else 8
            lines.append(r_shaped(f"mekanism:{tier}_{ptype}","mekanism",f"mekanism:{tier}_{ptype}",cnt,
                ["PPP","P P","PPP"],{"P":ing(mat)}))
    
    lines.append("\n// ─── CORE MACHINES ──────────────────────────────────────────")
    machines = [
        ("mekanism:enrichment_chamber",["III","IF ","III"],{"I":ing("mekanism:osmium_ingot"),"F":ing("mekanism:control_circuit_basic")}),
        ("mekanism:crusher",["III","IFI","III"],{"I":ing("mekanism:osmium_ingot"),"F":ing("mekanism:control_circuit_basic")}),
        ("mekanism:combiner",["OIO","IFI","OIO"],{"O":ing("mekanism:osmium_ingot"),"I":ing("minecraft:iron_ingot"),"F":ing("mekanism:control_circuit_basic")}),
        ("mekanism:purification_chamber",["OIO","EFO","OAO"],{"O":ing("mekanism:osmium_ingot"),"I":ing("mekanism:control_circuit_basic"),"E":ing("mekanism:enrichment_chamber"),"F":ing("mekanism:control_circuit_advanced"),"A":ing("mekanism:alloy_infused")}),
        ("mekanism:metallurgic_infuser",["IOI","O O","IOI"],{"I":ing("minecraft:iron_ingot"),"O":ing("mekanism:osmium_ingot")}),
        ("mekanism:osmium_compressor",["CIC","CFC","CIC"],{"C":ing("mekanism:control_circuit_advanced"),"I":ing("mekanism:osmium_ingot"),"F":ing("mekanism:enrichment_chamber")}),
        ("mekanism:injection_chamber",["OAO","C C","OAO"],{"A":ing("mekanism:alloy_reinforced"),"C":ing("mekanism:control_circuit_advanced"),"O":ing("mekanism:osmium_ingot")}),
        ("mekanism:smelter",["III","IFI","III"],{"I":ing("mekanism:osmium_ingot"),"F":ing("minecraft:furnace")}),
        ("mekanism:rotary_condensentrator",["CAC","A A","CAC"],{"C":ing("mekanism:control_circuit_elite"),"A":ing("mekanism:alloy_atomic")}),
        ("mekanism:chemical_dissolution_chamber",["AIA","CFC","AIA"],{"A":ing("mekanism:alloy_atomic"),"I":ing("mekanism:control_circuit_elite"),"C":ing("mekanism:osmium_ingot"),"F":ing("mekanism:injection_chamber")}),
        ("mekanism:chemical_washer",["C C","AFA","CCC"],{"C":ing("mekanism:control_circuit_elite"),"A":ing("mekanism:alloy_atomic"),"F":ing("mekanism:chemical_dissolution_chamber")}),
        ("mekanism:chemical_crystallizer",["CAC","A A","CAC"],{"C":ing("mekanism:control_circuit_elite"),"A":ing("mekanism:alloy_atomic")}),
        ("mekanism:pressurized_reaction_chamber",["ACA","C C","ACA"],{"C":ing("mekanism:control_circuit_elite"),"A":ing("mekanism:alloy_atomic")}),
        ("mekanism:isotopic_centrifuge",["CAC","A A","CAC"],{"C":ing("mekanism:control_circuit_ultimate"),"A":ing("mekanism:alloy_atomic")}),
        ("mekanism:solar_neutron_activator",["GGG","A A","CAC"],{"C":ing("mekanism:control_circuit_elite"),"A":ing("mekanism:alloy_atomic"),"G":ing("minecraft:glass")}),
        ("mekanism:digital_miner",["CAC","A A","CAC"],{"C":ing("mekanism:control_circuit_elite"),"A":ing("mekanism:alloy_atomic")}),
        ("mekanism:quantum_entangloporter",["A A"," C ","A A"],{"C":ing("mekanism:control_circuit_ultimate"),"A":ing("mekanism:alloy_atomic")}),
        ("mekanism:induction_casing",["OOO","OCO","OOO"],{"O":ing("mekanism:osmium_ingot"),"C":ing("mekanism:control_circuit_elite")}),
        ("mekanism:induction_port",[" O ","OCO"," O "],{"O":ing("mekanism:osmium_ingot"),"C":ing("mekanism:control_circuit_elite")}),
        ("mekanism:electrolytic_separator",["IRI","CSC","IRI"],{"I":ing("mekanism:osmium_ingot"),"R":ing("mekanism:control_circuit_advanced"),"C":ing("minecraft:copper_ingot"),"S":ing("mekanism:alloy_infused")}),
        ("mekanism:precision_sawmill",["III","ICI","III"],{"I":ing("mekanism:osmium_ingot"),"C":ing("mekanism:control_circuit_basic")}),
    ]
    for mid, pat, keys in machines:
        lines.append(r_shaped(mid,"mekanism",mid,1,pat,keys))
    
    lines.append("\n// ─── FACTORIES ────────────────────────────────────────────────")
    for fm in ["smelting","enriching","crushing","compressing","injecting"]:
        for tier, circ, alloy in [
            ("basic","mekanism:control_circuit_basic","mekanism:alloy_infused"),
            ("advanced","mekanism:control_circuit_advanced","mekanism:alloy_reinforced"),
            ("elite","mekanism:control_circuit_elite","mekanism:alloy_atomic"),
            ("ultimate","mekanism:control_circuit_ultimate","mekanism:alloy_atomic"),
        ]:
            lines.append(r_shaped(f"mekanism:{tier}_{fm}_factory","mekanism",f"mekanism:{tier}_{fm}_factory",1,
                ["III","CSC","AAA"],{"I":ing("mekanism:osmium_ingot"),"C":ing(circ),"S":ing(alloy),"A":ing("mekanism:alloy_infused")}))
    
    lines.append("\n// ─── HDPE & SUBSTRATE ───────────────────────────────────────")
    lines.append(r_simple("mekanism:bio_fuel","mekanism:crusher","mekanism","mekanism:bio_fuel",4,[("minecraft:wheat",8)]))
    lines.append(r_simple("mekanism:substrate","mekanism:pressurized_reaction_chamber","mekanism","mekanism:substrate",1,[("mekanism:bio_fuel",1),("mekanism:water",1)],"energy:800"))
    lines.append(r_simple("mekanism:hdpe_pellets","mekanism:pressurized_reaction_chamber","mekanism","mekanism:hdpe_pellets",1,[("mekanism:substrate",1),("mekanism:hydrogen",1)],"energy:600"))
    lines.append(r_simple("mekanism:hdpe_sheet","mekanism:pressurized_reaction_chamber","mekanism","mekanism:hdpe_sheet",1,[("mekanism:hdpe_pellets",3)],"energy:200"))
    lines.append(r_simple("mekanism:hdpe_rod","mekanism:pressurized_reaction_chamber","mekanism","mekanism:hdpe_rod",1,[("mekanism:hdpe_pellets",2)],"energy:150"))
    
    lines.append("\n// ─── FLUIDS (SYMBOLIC) ──────────────────────────────────────")
    lines.append(r_simple("mekanism:water","crafting","mekanism","mekanism:water",1,[("minecraft:water_bucket",1)]))
    lines.append(r_simple("mekanism:hydrogen","mekanism:electrolytic_separator","mekanism","mekanism:hydrogen",1,[("mekanism:water",2)],"energy:400"))
    lines.append(r_simple("mekanism:oxygen","mekanism:electrolytic_separator","mekanism","mekanism:oxygen",1,[("mekanism:water",2)],"energy:400"))
    lines.append(r_simple("mekanism:chlorine","mekanism:electrolytic_separator","mekanism","mekanism:chlorine",1,[("mekanism:water",2)],"energy:400"))
    
    lines.append("\n// ─── NUCLEAR ────────────────────────────────────────────────")
    lines.append(r_shaped("mekanism:reactor_frame","mekanism","mekanism:reactor_frame",1,
        ["ACA","C C","ACA"],{"C":ing("mekanism:control_circuit_ultimate"),"A":ing("mekanism:alloy_atomic")}))
    lines.append(r_shaped("mekanism:reactor_port","mekanism","mekanism:reactor_port",1,
        [" A ","C C"," A "],{"C":ing("mekanism:control_circuit_ultimate"),"A":ing("mekanism:alloy_atomic")}))
    lines.append(r_simple("mekanism:uranium_oxide","mekanism:enrichment_chamber","mekanism","mekanism:uranium_oxide",1,[("mekanism:uranium_ingot",1)]))
    lines.append(r_simple("mekanism:yellow_cake","mekanism:chemical_crystallizer","mekanism","mekanism:yellow_cake",1,[("mekanism:uranium_oxide",1)]))
    lines.append(r_simple("mekanism:fissile_fuel","mekanism:chemical_dissolution_chamber","mekanism","mekanism:fissile_fuel",1,[("mekanism:yellow_cake",1)]))
    
    # Processing recipes (symbolic)
    lines.append("\n// ─── PROCESSING ─────────────────────────────────────────────")
    proc_recipes = [
        ("mekanism:iron_enrich","mekanism:enrichment_chamber","mekanism:enriched_iron",1,[("minecraft:iron_ingot",1)]),
        ("mekanism:gold_enrich","mekanism:enrichment_chamber","mekanism:gold_dust",2,[("minecraft:raw_gold",1)]),
    ]
    for rid, cat, out, cnt, ins in proc_recipes:
        lines.append(r_simple(rid,cat,"mekanism",out,cnt,ins))
    
    write_footer(lines, "MEK")
    return "\n".join(lines)

if __name__ == "__main__":
    out = generate()
    os.makedirs("src/data/recipes", exist_ok=True)
    with open("src/data/recipes/mekanism.ts","w") as f: f.write(out)
    rc = out.count("r('")
    print(f"Generated mekanism.ts — {rc} recipes")
