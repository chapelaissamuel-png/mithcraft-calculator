#!/usr/bin/env python3
"""Generate ae2.ts"""
import os, sys; sys.path.insert(0, os.path.dirname(__file__))
from generate_base import *

def generate():
    lines = []
    write_header(lines, "AE"); lines.append("")
    
    # Crystals
    lines.append("// ─── CRYSTALS ────────────────────────────────────────────")
    lines.append(r_shaped("ae2:certus_quartz_crystal","ae2","ae2:certus_quartz_crystal",1,
        ["C"],{"C":ing("ae2:certus_quartz_dust")}))
    lines.append(r_shaped("ae2:fluix_crystal","ae2","ae2:fluix_crystal",1,
        ["F"],{"F":ing("ae2:fluix_dust")}))
    lines.append(r_shaped("ae2:charged_certus_quartz_crystal","ae2","ae2:charged_certus_quartz_crystal",1,
        ["C"],{"C":ing("ae2:certus_quartz_crystal")}))
    
    # Dusts
    lines.append("\n// ─── DUSTS ──────────────────────────────────────────────")
    lines.append(r_simple("ae2:certus_quartz_dust","ae2:quartz_grindstone","ae2","ae2:certus_quartz_dust",1,[("ae2:certus_quartz_crystal",1)]))
    lines.append(r_simple("ae2:fluix_dust","ae2:quartz_grindstone","ae2","ae2:fluix_dust",1,[("ae2:fluix_crystal",1)]))
    lines.append(r_simple("ae2:certus_quartz_dust_crystal","crafting","ae2","ae2:certus_quartz_dust",1,[("ae2:certus_quartz_crystal",1)]))
    
    # Fluix
    lines.append("\n// ─── FLUIX CRYSTAL (SYNTHESIS) ─────────────────────────────")
    lines.append(r_simple("ae2:fluix_synth","ae2:charger","ae2","ae2:fluix_crystal",1,[("ae2:certus_quartz_crystal",1),("minecraft:redstone",1),("minecraft:quartz",1)]))
    
    # Processors
    lines.append("\n// ─── PROCESSORS ───────────────────────────────────────────")
    procs = [
        ("ae2:printed_calculation_processor",["PPP","P P","PPP"],{"P":ing("ae2:certus_quartz_crystal")}),
        ("ae2:printed_engineering_processor",["PPP","P P","PPP"],{"P":ing("minecraft:diamond")}),
        ("ae2:printed_logic_processor",["PPP","P P","PPP"],{"P":ing("minecraft:gold_ingot")}),
        ("ae2:printed_silicon",["PPP","P P","PPP"],{"P":ing("ae2:silicon")}),
    ]
    for mid, pat, keys in procs:
        lines.append(r_shaped(mid,"ae2",mid,1,pat,keys))
    
    # Processor assembly
    lines.append(r_shaped("ae2:calculation_processor","ae2","ae2:calculation_processor",1,
        ["P","R","S"],{"P":ing("ae2:printed_calculation_processor"),"R":ing("minecraft:redstone"),"S":ing("ae2:printed_silicon")}))
    lines.append(r_shaped("ae2:engineering_processor","ae2","ae2:engineering_processor",1,
        ["P","R","S"],{"P":ing("ae2:printed_engineering_processor"),"R":ing("minecraft:redstone"),"S":ing("ae2:printed_silicon")}))
    lines.append(r_shaped("ae2:logic_processor","ae2","ae2:logic_processor",1,
        ["P","R","S"],{"P":ing("ae2:printed_logic_processor"),"R":ing("minecraft:redstone"),"S":ing("ae2:printed_silicon")}))
    
    # Silicon
    lines.append("\n// ─── SILICON ─────────────────────────────────────────────")
    lines.append(r_simple("ae2:silicon","smelting","ae2","ae2:silicon",1,[("minecraft:quartz_block",1)]))
    
    # Basic ME components
    lines.append("\n// ─── ME COMPONENTS ────────────────────────────────────────")
    lines.append(r_shaped("ae2:energy_acceptor","ae2","ae2:energy_acceptor",1,
        ["PPP","P P","PPP"],{"P":ing("minecraft:iron_ingot")}))
    lines.append(r_shaped("ae2:energy_cell","ae2","ae2:energy_cell",1,
        ["CCC","C C","CCC"],{"C":ing("ae2:certus_quartz_crystal")}))
    lines.append(r_shaped("ae2:dense_energy_cell","ae2","ae2:dense_energy_cell",1,
        ["CCC","CEC","CCC"],{"C":ing("ae2:certus_quartz_crystal"),"E":ing("ae2:energy_cell")}))
    lines.append(r_shaped("ae2:controller","ae2","ae2:controller",1,
        ["SFS","FPF","SFS"],{"S":ing("ae2:fluix_crystal"),"F":ing("ae2:fluix_block"),"P":ing("ae2:calculation_processor")}))
    
    # ME Cables
    lines.append("\n// ─── ME CABLES ────────────────────────────────────────────")
    for size,mat in [("","ae2:fluix_crystal"),("dense_","ae2:fluix_crystal")]:
        lines.append(r_shaped(f"ae2:{size}me_cable","ae2",f"ae2:{size}me_cable",8,
            ["CCC","CCC"],{"C":ing(mat)}))
    
    # Cables with covers
    for color in ["white","orange","blue","brown","green","red","black"]:
        lines.append(r_shaped(f"ae2:{color}_covered_cable","ae2",f"ae2:{color}_covered_cable",8,
            ["CCC","CCC"],{"C":ing("ae2:fluix_crystal")}))
    
    # Terminals
    lines.append("\n// ─── TERMINALS ────────────────────────────────────────────")
    terms = [
        ("ae2:terminal",["PPP","PCP","PPP"],{"P":ing("minecraft:iron_ingot"),"C":ing("ae2:calculation_processor")}),
        ("ae2:crafting_terminal",["PPP","PCP","PPP"],{"P":ing("minecraft:iron_ingot"),"C":ing("ae2:terminal")}),
        ("ae2:pattern_terminal",["PPP","PCP","PPP"],{"P":ing("minecraft:iron_ingot"),"C":ing("ae2:engineering_processor")}),
        ("ae2:interface_terminal",["PPP","PCP","PPP"],{"P":ing("minecraft:iron_ingot"),"C":ing("ae2:interface")}),
        ("ae2:drive",["AAA","ACA","AAA"],{"A":ing("ae2:fluix_crystal"),"C":ing("ae2:calculation_processor")}),
        ("ae2:cell_workbench",["CCC"," W ","WWW"],{"C":ing("ae2:calculation_processor"),"W":ing("ae2:sky_stone_block")}),
        ("ae2:molecular_assembler",["CCC","CEC","CCC"],{"C":ing("ae2:fluix_crystal"),"E":ing("ae2:energy_acceptor")}),
        ("ae2:inscriber",["III","ICI","III"],{"I":ing("minecraft:iron_ingot"),"C":ing("ae2:certus_quartz_crystal")}),
        ("ae2:charger",["CIC","I I","CIC"],{"C":ing("ae2:certus_quartz_crystal"),"I":ing("minecraft:iron_ingot")}),
        ("ae2:quartz_grindstone",[" C ","C C"," C "],{"C":ing("minecraft:cobblestone")}),
    ]
    for mid, pat, keys in terms:
        lines.append(r_shaped(mid,"ae2",mid,1,pat,keys))
    
    # Storage
    lines.append("\n// ─── STORAGE ─────────────────────────────────────────────")
    for tier,cell_mat in [("1k","ae2:certus_quartz_crystal"),("4k","ae2:fluix_crystal"),
                           ("16k","ae2:fluix_crystal"),("64k","ae2:fluix_crystal")]:
        lines.append(r_shaped(f"ae2:{tier}_me_storage_cell","ae2",f"ae2:{tier}_me_storage_cell",1,
            ["CEC","ECE","CEC"],{"C":ing(cell_mat),"E":ing("ae2:calculation_processor")}))
    
    # Blocks
    lines.append("\n// ─── BLOCKS ──────────────────────────────────────────────")
    lines.append(r_shaped("ae2:certus_quartz_block","ae2","ae2:certus_quartz_block",1,
        ["CCC","CCC","CCC"],{"C":ing("ae2:certus_quartz_crystal")}))
    lines.append(r_shaped("ae2:fluix_block","ae2","ae2:fluix_block",1,
        ["FFF","FFF","FFF"],{"F":ing("ae2:fluix_crystal")}))
    
    # Sky stone
    lines.append(r_shaped("ae2:sky_stone_block","ae2","ae2:sky_stone_block",1,
        ["SS","SS"],{"S":ing("ae2:sky_stone_dust")}))
    
    # P2P
    lines.append("\n// ─── P2P ──────────────────────────────────────────────────")
    lines.append(r_shaped("ae2:me_p2p_tunnel","ae2","ae2:me_p2p_tunnel",1,
        ["C","P"],{"C":ing("ae2:me_cable"),"P":ing("ae2:fluix_crystal")}))
    
    # Interface
    lines.append("\n// ─── INTERFACES ───────────────────────────────────────────")
    lines.append(r_shaped("ae2:interface","ae2","ae2:interface",1,
        ["EEE","EPE","EEE"],{"E":ing("ae2:fluix_crystal"),"P":ing("ae2:calculation_processor")}))
    
    write_footer(lines, "AE")
    return "\n".join(lines)

if __name__ == "__main__":
    out = generate()
    os.makedirs("src/data/recipes", exist_ok=True)
    with open("src/data/recipes/ae2.ts","w") as f: f.write(out)
    rc = out.count("r('")
    print(f"Generated ae2.ts — {rc} recipes")
