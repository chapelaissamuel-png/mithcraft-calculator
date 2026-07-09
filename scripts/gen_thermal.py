#!/usr/bin/env python3
"""Generate thermal.ts"""
import os, sys; sys.path.insert(0, os.path.dirname(__file__))
from generate_base import *

def generate():
    lines = []
    write_header(lines, "TH"); lines.append("")
    
    for ore in ["tin","lead","silver","nickel"]:
        lines.append(r_simple(f"thermal:{ore}_ingot_smelt","smelting","thermal",f"thermal:{ore}_ingot",1,[(f"thermal:{ore}_ore",1)]))
    lines.append("")
    
    lines.append("// ─── ALLOYS ─────────────────────────────────────────────")
    for item,cnt,ins in [
        ("thermal:bronze_ingot",4,[("minecraft:copper_ingot",3),("thermal:tin_ingot",1)]),
        ("thermal:constantan_ingot",2,[("minecraft:copper_ingot",1),("thermal:nickel_ingot",1)]),
        ("thermal:electrum_ingot",2,[("minecraft:gold_ingot",1),("thermal:silver_ingot",1)]),
        ("thermal:invar_ingot",3,[("minecraft:iron_ingot",2),("thermal:nickel_ingot",1)]),
        ("thermal:steel_ingot",1,[("minecraft:iron_ingot",1),("minecraft:coal",2)]),
        ("thermal:signalum_ingot",2,[("minecraft:copper_ingot",1),("thermal:silver_ingot",1),("minecraft:redstone",4)]),
        ("thermal:lumium_ingot",2,[("thermal:tin_ingot",1),("thermal:silver_ingot",1),("minecraft:glowstone_dust",4)]),
        ("thermal:enderium_ingot",2,[("thermal:lead_ingot",1),("minecraft:diamond",1),("minecraft:ender_pearl",2)]),
    ]:
        lines.append(r_simple(f"thermal:{item.split(':')[1]}_alloy","thermal:induction_smelter","thermal",item,cnt,ins,"energy: 400"))
    
    lines.append("\n// ─── COMPONENTS ─────────────────────────────────────────")
    lines.append(r_shaped("thermal:redstone_servo","thermal","thermal:redstone_servo",1,
        [" I ","IRI"," I "],{"I":ing("minecraft:iron_ingot"),"R":ing("minecraft:redstone")}))
    lines.append(r_shaped("thermal:rf_coil","thermal","thermal:rf_coil",1,
        [" G ","GIG"," G "],{"G":ing("minecraft:gold_ingot"),"I":ing("minecraft:iron_ingot")}))
    lines.append(r_shaped("thermal:machine_frame","thermal","thermal:machine_frame",1,
        ["SRS","RIR","SRS"],{"S":ing("thermal:redstone_servo"),"R":ing("thermal:rf_coil"),"I":ing("minecraft:iron_ingot")}))
    
    lines.append("\n// ─── AUGMENTS ───────────────────────────────────────────")
    for name,tier,mat in [("1","1","iron_ingot"),("2","2","gold_ingot"),("3","3","diamond")]:
        lines.append(r_shaped(f"thermal:upgrade_augment_{tier}","thermal",f"thermal:upgrade_augment_{tier}",1,
            [" M ","MSM"," M "],{"M":ing(f"minecraft:{mat}"),"S":ing("thermal:redstone_servo")}))
    
    lines.append("\n// ─── MACHINES ───────────────────────────────────────────")
    for mid,pat,keys in [
        ("thermal:pulverizer",["IRI","IFI","ICI"],{"I":ing("minecraft:iron_ingot"),"R":ing("minecraft:redstone"),"F":ing("thermal:machine_frame"),"C":ing("thermal:redstone_servo")}),
        ("thermal:induction_smelter",["IRI","IFI","IRI"],{"I":ing("minecraft:iron_ingot"),"R":ing("minecraft:redstone"),"F":ing("thermal:machine_frame")}),
        ("thermal:centrifuge",["IRI","IFI","IRI"],{"I":ing("minecraft:gold_ingot"),"R":ing("minecraft:redstone"),"F":ing("thermal:machine_frame")}),
        ("thermal:refinery",["IGI","GFG","IGI"],{"I":ing("minecraft:iron_ingot"),"G":ing("minecraft:glass"),"F":ing("thermal:machine_frame")}),
        ("thermal:crystallizer",["DGD","GFG","DGD"],{"D":ing("minecraft:diamond"),"G":ing("minecraft:glass"),"F":ing("thermal:machine_frame")}),
        ("thermal:press",["IPI","IFI","IRI"],{"I":ing("minecraft:iron_ingot"),"P":ing("minecraft:piston"),"F":ing("thermal:machine_frame"),"R":ing("thermal:rf_coil")}),
        ("thermal:fluid_encapsulator",["IGI","GFG","IRI"],{"I":ing("minecraft:iron_ingot"),"G":ing("minecraft:glass"),"F":ing("thermal:machine_frame"),"R":ing("thermal:rf_coil")}),
        ("thermal:machine_crafter",["IGI","CFC","IRI"],{"C":ing("thermal:redstone_servo"),"F":ing("thermal:machine_frame"),"G":ing("minecraft:glass"),"I":ing("minecraft:iron_ingot"),"R":ing("thermal:rf_coil")}),
        ("thermal:dynamo",["IGI","CFC","IGI"],{"C":ing("minecraft:redstone"),"F":ing("thermal:machine_frame"),"G":ing("minecraft:redstone"),"I":ing("minecraft:iron_ingot")}),
        ("thermal:device_composter",["GFG","GDG","GFG"],{"D":ing("thermal:redstone_servo"),"F":ing("thermal:machine_frame"),"G":ing("minecraft:iron_ingot")}),
        ("thermal:device_water_gen",["GFG","GCG","GFG"],{"C":ing("thermal:rf_coil"),"F":ing("thermal:machine_frame"),"G":ing("minecraft:iron_ingot")}),
        ("thermal:energy_cell",["SRS","CGC","SRS"],{"C":ing("thermal:machine_frame"),"G":ing("minecraft:gold_ingot"),"R":ing("thermal:rf_coil"),"S":ing("thermal:redstone_servo")}),
        ("thermal:fluid_cell",["SRS","CGC","SRS"],{"C":ing("thermal:machine_frame"),"G":ing("minecraft:glass"),"R":ing("thermal:rf_coil"),"S":ing("thermal:redstone_servo")}),
    ]:
        lines.append(r_shaped(mid,"thermal",mid,1,pat,keys))
    
    lines.append("\n// ─── DUCTS ──────────────────────────────────────────────")
    for tier,mat in [("basic","minecraft:iron_ingot"),("hardened","thermal:invar_ingot"),("reinforced","thermal:signalum_ingot"),("signalum","thermal:signalum_ingot")]:
        for duct in ["fluxduct","fluiduct","itemduct"]:
            lines.append(r_shaped(f"thermal:{tier}_{duct}","thermal",f"thermal:{tier}_{duct}",4,
                ["DD","DD"],{"D":ing(mat)}))
    
    lines.append("\n// ─── MACHINE AUGMENTS ───────────────────────────────────")
    augments = [
        ("thermal:machine_speed_augment",[" M ","MSM"," M "],{"M":ing("minecraft:redstone"),"S":ing("thermal:redstone_servo")}),
        ("thermal:machine_efficiency_augment",[" M ","MSM"," M "],{"M":ing("minecraft:glass"),"S":ing("thermal:redstone_servo")}),
        ("thermal:machine_output_augment",[" M ","MSM"," M "],{"M":ing("minecraft:diamond"),"S":ing("thermal:redstone_servo")}),
    ]
    for mid, pat, keys in augments:
        lines.append(r_shaped(mid,"thermal",mid,1,pat,keys))
    
    write_footer(lines, "TH")
    return "\n".join(lines)

if __name__ == "__main__":
    out = generate()
    os.makedirs("src/data/recipes", exist_ok=True)
    with open("src/data/recipes/thermal.ts","w") as f: f.write(out)
    rc = out.count("r('")
    print(f"Generated thermal.ts — {rc} recipes")
