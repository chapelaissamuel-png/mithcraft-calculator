#!/usr/bin/env python3
"""Generate ic2.ts"""
import os, sys; sys.path.insert(0, os.path.dirname(__file__))
from generate_base import *

def generate():
    lines = []
    write_header(lines, "IC"); lines.append("")
    
    lines.append("// ─── BASE MATERIALS ─────────────────────────────────────")
    lines.append(r_simple("ic2:refined_iron_ingot","ic2:compressor","ic2","ic2:refined_iron_ingot",1,[("minecraft:iron_ingot",1)],"energy:200"))
    lines.append(r_simple("ic2:rubber","ic2:extractor","ic2","ic2:rubber",3,[("minecraft:oak_log",1)],"energy:100"))
    lines.append(r_simple("ic2:carbon_plate","ic2:compressor","ic2","ic2:carbon_plate",1,[("minecraft:coal",8)],"energy:400"))
    
    cables = [
        ("ic2:insulated_copper_cable",6,[("ic2:rubber",2),("minecraft:copper_ingot",3)]),
        ("ic2:tin_cable",6,[("minecraft:tin_ingot",3)]),
        ("ic2:copper_cable",6,[("minecraft:copper_ingot",3)]),
        ("ic2:gold_cable",4,[("minecraft:gold_ingot",2)]),
        ("ic2:glass_fibre_cable",4,[("ic2:rubber",2),("minecraft:glass",2)]),
    ]
    for item,cnt,ins in cables:
        lines.append(r_shaped(item,"ic2",item,cnt,
            ["CCC","C C","CCC"],{"C":ing("minecraft:copper_ingot" if "copper" in item else item.split(":")[1])}))
    
    lines.append("\n// ─── CIRCUITS ───────────────────────────────────────────")
    lines.append(r_shaped("ic2:electronic_circuit","ic2","ic2:electronic_circuit",1,
        ["CRC","CCC","CRC"],{"C":ing("ic2:insulated_copper_cable"),"R":ing("ic2:refined_iron_ingot")}))
    lines.append(r_shaped("ic2:advanced_circuit","ic2","ic2:advanced_circuit",1,
        ["CRC","CEC","RCR"],{"C":ing("ic2:electronic_circuit"),"R":ing("minecraft:redstone"),"E":ing("minecraft:glowstone_dust")}))
    
    lines.append("\n// ─── MACHINE BLOCKS ─────────────────────────────────────")
    lines.append(r_shaped("ic2:machine_block_basic","ic2","ic2:machine_block_basic",1,
        ["III","IRI","III"],{"I":ing("ic2:refined_iron_ingot"),"R":ing("ic2:electronic_circuit")}))
    lines.append(r_shaped("ic2:machine_block_advanced","ic2","ic2:machine_block_advanced",1,
        ["CRC","RBR","CRC"],{"C":ing("ic2:carbon_plate"),"R":ing("ic2:electronic_circuit"),"B":ing("ic2:machine_block_basic")}))
    
    lines.append("\n// ─── ENERGY ─────────────────────────────────────────────")
    energy = [
        ("ic2:generator",["IBI","IFI","III"],{"I":ing("minecraft:iron_ingot"),"B":ing("ic2:machine_block_basic"),"F":ing("minecraft:furnace")}),
        ("ic2:solar_panel",["GGG","CSC","IGI"],{"G":ing("minecraft:glass"),"C":ing("ic2:electronic_circuit"),"S":ing("ic2:generator"),"I":ing("ic2:refined_iron_ingot")}),
        ("ic2:cesu",["CBC","BCB","CBC"],{"C":ing("ic2:insulated_copper_cable"),"B":ing("ic2:machine_block_basic")}),
        ("ic2:mf_unit",["CRC","RCR","CRC"],{"C":ing("ic2:insulated_copper_cable"),"R":ing("ic2:refined_iron_ingot")}),
        ("ic2:mfs_unit",["CAC","AMA","CAC"],{"C":ing("ic2:carbon_plate"),"A":ing("ic2:advanced_circuit"),"M":ing("ic2:mf_unit")}),
        ("ic2:storage_battery",["RBR","ICI","RBR"],{"R":ing("ic2:refined_iron_ingot"),"B":ing("ic2:machine_block_basic"),"I":ing("ic2:insulated_copper_cable"),"C":ing("ic2:electronic_circuit")}),
    ]
    for mid,pat,keys in energy:
        lines.append(r_shaped(mid,"ic2",mid,1,pat,keys))
    
    lines.append("\n// ─── MACHINES ───────────────────────────────────────────")
    machines = [
        ("ic2:compressor",["III","IMI","III"],{"I":ing("minecraft:iron_ingot"),"M":ing("ic2:machine_block_basic")}),
        ("ic2:extractor",["III","IMI","III"],{"I":ing("minecraft:iron_ingot"),"M":ing("ic2:machine_block_basic")}),
        ("ic2:macerator",["IRI","IFI","IRI"],{"I":ing("ic2:refined_iron_ingot"),"R":ing("ic2:electronic_circuit"),"F":ing("ic2:machine_block_basic")}),
        ("ic2:thermal_centrifuge",["III","IMI","IRI"],{"I":ing("ic2:refined_iron_ingot"),"M":ing("ic2:machine_block_advanced"),"R":ing("ic2:electronic_circuit")}),
        ("ic2:recycler",["III","IMI","ICI"],{"C":ing("ic2:electronic_circuit"),"I":ing("ic2:refined_iron_ingot"),"M":ing("ic2:machine_block_basic")}),
        ("ic2:induction_furnace",["CIC","IFM","CIC"],{"C":ing("ic2:electronic_circuit"),"F":ing("ic2:machine_block_advanced"),"I":ing("ic2:refined_iron_ingot"),"M":ing("ic2:machine_block_basic")}),
        ("ic2:magnetizer",["IRI","CFC","IXI"],{"C":ing("ic2:electronic_circuit"),"F":ing("ic2:machine_block_basic"),"I":ing("ic2:refined_iron_ingot"),"R":ing("minecraft:redstone"),"X":ing("minecraft:iron_ingot")}),
        ("ic2:mining_drill",["II","IC"," S"],{"C":ing("ic2:electronic_circuit"),"I":ing("ic2:refined_iron_ingot"),"S":ing("ic2:storage_battery")}),
        ("ic2:diamond_drill",["DD","DC"," S"],{"C":ing("ic2:electronic_circuit"),"D":ing("minecraft:diamond"),"S":ing("ic2:storage_battery")}),
        ("ic2:nuclear_reactor",["CBC","RMR","CBC"],{"C":ing("ic2:advanced_circuit"),"B":ing("ic2:machine_block_advanced"),"R":ing("ic2:refined_iron_ingot"),"M":ing("ic2:machine_block_basic")}),
        ("ic2:fluid_enricher",["IFI","FMF","IFI"],{"F":ing("ic2:machine_block_basic"),"I":ing("minecraft:iron_ingot"),"M":ing("ic2:electronic_circuit")}),
        ("ic2:rotary_macerator",["IRI","CMC","IRI"],{"C":ing("ic2:advanced_circuit"),"I":ing("ic2:refined_iron_ingot"),"M":ing("ic2:macerator"),"R":ing("minecraft:redstone")}),
        ("ic2:scanner",["IGI","IMI","IRI"],{"G":ing("minecraft:glass"),"I":ing("ic2:refined_iron_ingot"),"M":ing("ic2:machine_block_basic"),"R":ing("ic2:electronic_circuit")}),
    ]
    for mid,pat,keys in machines:
        lines.append(r_shaped(mid,"ic2",mid,1,pat,keys))
    
    # Upgrades
    lines.append("\n// ─── UPGRADES ───────────────────────────────────────────")
    upgrades = [
        ("ic2:overclocker_upgrade",["C","R","C"],{"C":ing("ic2:electronic_circuit"),"R":ing("minecraft:redstone")}),
        ("ic2:transformer_upgrade",["C","G","C"],{"C":ing("ic2:electronic_circuit"),"G":ing("minecraft:gold_ingot")}),
        ("ic2:energy_storage_upgrade",["C","B","C"],{"B":ing("ic2:storage_battery"),"C":ing("ic2:electronic_circuit")}),
    ]
    for mid,pat,keys in upgrades:
        lines.append(r_shaped(mid,"ic2",mid,1,pat,keys))
    
    write_footer(lines, "IC")
    return "\n".join(lines)

if __name__ == "__main__":
    out = generate()
    os.makedirs("src/data/recipes", exist_ok=True)
    with open("src/data/recipes/ic2.ts","w") as f: f.write(out)
    rc = out.count("r('")
    print(f"Generated ic2.ts — {rc} recipes")
