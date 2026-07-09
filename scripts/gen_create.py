#!/usr/bin/env python3
"""Generate create.ts"""
import os, sys; sys.path.insert(0, os.path.dirname(__file__))
from generate_base import *

def generate():
    lines = []
    write_header(lines, "CREATE"); lines.append("")
    
    lines.append("// ─── BASIC COMPONENTS ───────────────────────────────────")
    lines.append(r_shaped("create:cogwheel","create","create:cogwheel",1,
        [" P ","P P"," P "],{"P":ing("minecraft:oak_planks")}))
    lines.append(r_shaped("create:large_cogwheel","create","create:large_cogwheel",1,
        ["PPP","P P","PPP"],{"P":ing("minecraft:oak_planks")}))
    lines.append(r_shaped("create:shaft","create","create:shaft",1,["I","I"],{"I":ing("minecraft:iron_ingot")}))
    lines.append(r_shaped("create:gearbox","create","create:gearbox",1,["S","S"],{"S":ing("create:shaft")}))
    lines.append(r_shaped("create:precision_mechanism","create","create:precision_mechanism",1,
        [" C ","CGC"," C "],{"C":ing("minecraft:gold_ingot"),"G":ing("create:cogwheel")}))
    lines.append(r_shaped("create:andesite_casing","create","create:andesite_casing",1,
        ["AAA","A A","AAA"],{"A":ing("minecraft:andesite")}))
    lines.append(r_shaped("create:copper_casing","create","create:copper_casing",1,
        ["CCC","C C","CCC"],{"C":ing("minecraft:copper_ingot")}))
    lines.append(r_shaped("create:brass_casing","create","create:brass_casing",1,
        ["BBB","B B","BBB"],{"B":ing("create:brass_ingot")}))
    
    # Alloys
    lines.append("\n// ─── ALLOYS ─────────────────────────────────────────────")
    lines.append(r_simple("create:brass_ingot","crafting","create","create:brass_ingot",1,
        [("minecraft:copper_ingot",1),("create:zinc_ingot",1)]))
    
    # Kinetics
    lines.append("\n// ─── KINETICS ───────────────────────────────────────────")
    lines.append(r_shaped("create:water_wheel","create","create:water_wheel",1,
        ["PPP","PSP","PPP"],{"P":ing("minecraft:oak_planks"),"S":ing("create:shaft")}))
    lines.append(r_shaped("create:large_water_wheel","create","create:large_water_wheel",1,
        ["PPP","PWP","PPP"],{"P":ing("minecraft:oak_planks"),"W":ing("create:water_wheel")}))
    lines.append(r_shaped("create:windmill_bearing","create","create:windmill_bearing",1,
        ["PPP","PIP","PPP"],{"P":ing("minecraft:oak_planks"),"I":ing("create:shaft")}))
    lines.append(r_shaped("create:steam_engine","create","create:steam_engine",1,
        [" I ","IFI"," I "],{"I":ing("minecraft:iron_ingot"),"F":ing("create:fluid_pipe")}))
    lines.append(r_shaped("create:flywheel","create","create:flywheel",1,
        ["III","ISI","III"],{"I":ing("minecraft:iron_ingot"),"S":ing("create:shaft")}))
    lines.append(r_shaped("create:clutch","create","create:clutch",1,
        ["III"," S ","III"],{"I":ing("create:andesite_casing"),"S":ing("create:shaft")}))
    lines.append(r_shaped("create:gearshift","create","create:gearshift",1,
        ["III"," S ","III"],{"I":ing("create:andesite_casing"),"S":ing("create:shaft")}))
    lines.append(r_shaped("create:sequenced_gearshift","create","create:sequenced_gearshift",1,
        [" I ","IGI"," I "],{"I":ing("create:andesite_casing"),"G":ing("create:precision_mechanism")}))
    lines.append(r_shaped("create:rotation_speed_controller","create","create:rotation_speed_controller",1,
        [" I ","ICI"," I "],{"I":ing("create:brass_casing"),"C":ing("create:precision_mechanism")}))
    lines.append(r_shaped("create:stressometer","create","create:stressometer",1,
        [" I ","ICI"," I "],{"I":ing("create:andesite_casing"),"C":ing("create:precision_mechanism")}))
    lines.append(r_shaped("create:speedometer","create","create:speedometer",1,
        [" I ","ICI"," I "],{"I":ing("create:andesite_casing"),"C":ing("create:precision_mechanism")}))
    
    # Mechanical machines
    lines.append("\n// ─── MECHANICAL ─────────────────────────────────────────")
    mechs = [
        ("create:mechanical_press",["III","IAI","III"],{"I":ing("create:andesite_casing"),"A":ing("create:precision_mechanism")}),
        ("create:mechanical_mixer",["I I","IAI"," I "],{"I":ing("create:andesite_casing"),"A":ing("create:precision_mechanism")}),
        ("create:mechanical_saw",["III","IAI","III"],{"I":ing("create:andesite_casing"),"A":ing("create:precision_mechanism")}),
        ("create:mechanical_crafter",["IAI","A A","IAI"],{"I":ing("create:brass_casing"),"A":ing("create:precision_mechanism")}),
        ("create:mechanical_drill",["III","IAI","I I"],{"I":ing("create:andesite_casing"),"A":ing("create:precision_mechanism")}),
        ("create:deployer",["III","IAI","I I"],{"I":ing("create:andesite_casing"),"A":ing("create:precision_mechanism")}),
        ("create:mechanical_bearing",["III","IAI","III"],{"I":ing("create:andesite_casing"),"A":ing("create:precision_mechanism")}),
        ("create:rope_pulley",["III","IAI","III"],{"I":ing("create:andesite_casing"),"A":ing("create:precision_mechanism")}),
        ("create:elevator_pulley",["III","IAI","III"],{"I":ing("create:brass_casing"),"A":ing("create:precision_mechanism")}),
        ("create:mechanical_piston",["III","IAI","III"],{"I":ing("create:andesite_casing"),"A":ing("create:precision_mechanism")}),
        ("create:gantry_carriage",["III","IAI","III"],{"I":ing("create:andesite_casing"),"A":ing("create:precision_mechanism")}),
        ("create:portable_storage_interface",["III","IAI","III"],{"I":ing("create:andesite_casing"),"A":ing("create:precision_mechanism")}),
        ("create:mechanical_roller",["III","IAI","III"],{"I":ing("create:andesite_casing"),"A":ing("create:precision_mechanism")}),
    ]
    for mid, pat, keys in mechs:
        lines.append(r_shaped(mid,"create",mid,1,pat,keys))
    
    # Processing
    lines.append("\n// ─── PROCESSING ─────────────────────────────────────────")
    proc = [
        ("create:millstone",[" I ","S S"," R "],{"I":ing("minecraft:iron_ingot"),"S":ing("create:cogwheel"),"R":ing("create:andesite_casing")}),
        ("create:crushing_wheel",["III","IAI","III"],{"I":ing("minecraft:iron_ingot"),"A":ing("create:precision_mechanism")}),
        ("create:basin",[" I ","I I","III"],{"I":ing("minecraft:iron_ingot")}),
        ("create:spout",[" I "," I "," I "],{"I":ing("create:fluid_pipe")}),
        ("create:hose_pulley",["I I","IAI","I I"],{"I":ing("create:brass_casing"),"A":ing("create:precision_mechanism")}),
        ("create:mechanical_roller",["III","IAI","III"],{"I":ing("create:andesite_casing"),"A":ing("create:precision_mechanism")}),
        ("create:item_drain",["III","I I","III"],{"I":ing("create:copper_casing")}),
    ]
    for mid, pat, keys in proc:
        lines.append(r_shaped(mid,"create",mid,1,pat,keys))
    
    # Transport
    lines.append("\n// ─── TRANSPORT ───────────────────────────────────────────")
    lines.append(r_shaped("create:belt_connector","create","create:belt_connector",8,
        ["PPP","PBP"],{"P":ing("minecraft:dried_kelp"),"B":ing("minecraft:slime_ball")}))
    lines.append(r_shaped("create:depot","create","create:depot",1,
        ["IAI"],{"I":ing("create:andesite_casing"),"A":ing("create:andesite_casing")}))
    lines.append(r_shaped("create:weighted_ejector","create","create:weighted_ejector",1,
        ["A","C"],{"A":ing("create:andesite_casing"),"C":ing("create:precision_mechanism")}))
    lines.append(r_shaped("create:chute","create","create:chute",4,
        [" I "," I "," I "],{"I":ing("minecraft:iron_ingot")}))
    lines.append(r_shaped("create:smart_chute","create","create:smart_chute",1,
        [" I ","ICI"," I "],{"I":ing("create:andesite_casing"),"C":ing("minecraft:redstone")}))
    lines.append(r_shaped("create:tunnel","create","create:tunnel",2,
        ["AAA","AAA"],{"A":ing("create:andesite_casing")}))
    lines.append(r_shaped("create:brass_tunnel","create","create:brass_tunnel",2,
        ["BBB","BBB"],{"B":ing("create:brass_casing")}))
    lines.append(r_shaped("create:funnel","create","create:funnel",1,
        [" A "," I "," I "],{"A":ing("create:andesite_casing"),"I":ing("minecraft:iron_ingot")}))
    lines.append(r_shaped("create:brass_funnel","create","create:brass_funnel",1,
        [" B "," I "," I "],{"B":ing("create:brass_casing"),"I":ing("minecraft:iron_ingot")}))
    lines.append(r_shaped("create:controller_rail","create","create:controller_rail",6,
        ["I I","IBI","III"],{"I":ing("minecraft:gold_ingot"),"B":ing("create:precision_mechanism")}))
    
    # Fluids
    lines.append("\n// ─── FLUIDS ─────────────────────────────────────────────")
    lines.append(r_shaped("create:fluid_pipe","create","create:fluid_pipe",8,
        ["PPP","PPP"],{"P":ing("minecraft:copper_ingot")}))
    lines.append(r_shaped("create:fluid_tank","create","create:fluid_tank",1,
        ["PPP","P P","PPP"],{"P":ing("minecraft:copper_ingot")}))
    lines.append(r_shaped("create:steam_whistle","create","create:steam_whistle",1,
        [" I "," I "],{"I":ing("create:copper_casing")}))
    lines.append(r_shaped("create:pipe_junction","create","create:fluid_pipe",4,
        ["P","P","P"],{"P":ing("create:fluid_pipe")}))
    lines.append(r_shaped("create:fluid_duct","create","create:fluid_pipe",8,
        ["PPP","P P","PPP"],{"P":ing("create:fluid_pipe")}))
    
    # Heat
    lines.append("\n// ─── HEAT ───────────────────────────────────────────────")
    lines.append(r_shaped("create:blaze_burner","create","create:blaze_burner",1,
        [" I ","IBI"," I "],{"I":ing("minecraft:iron_ingot"),"B":ing("minecraft:blaze_rod")}))
    lines.append(r_shaped("create:lit_blaze_burner","create","create:lit_blaze_burner",1,
        [" F ","F F"," F "],{"F":ing("create:blaze_burner")}))
    
    # Display & misc
    lines.append("\n// ─── DISPLAY ────────────────────────────────────────────")
    lines.append(r_shaped("create:display_board","create","create:display_board",1,
        ["SSS","S S","SSS"],{"S":ing("minecraft:oak_planks")}))
    lines.append(r_shaped("create:nixie_tube","create","create:nixie_tube",1,
        [" I "," I "],{"I":ing("create:brass_casing")}))
    lines.append(r_shaped("create:redstone_link","create","create:redstone_link",1,
        ["RRR","RCR","RRR"],{"R":ing("minecraft:redstone"),"C":ing("create:precision_mechanism")}))
    lines.append(r_shaped("create:analog_lever","create","create:analog_lever",1,
        [" I "," S "," S "],{"I":ing("create:andesite_casing"),"S":ing("minecraft:stick")}))
    lines.append(r_shaped("create:pulse_extender","create","create:pulse_extender",1,
        ["RRR","RCR","RRR"],{"R":ing("minecraft:redstone"),"C":ing("create:precision_mechanism")}))
    lines.append(r_shaped("create:pulse_repeater","create","create:pulse_repeater",1,
        ["RRR","RCR","RRR"],{"R":ing("minecraft:redstone"),"C":ing("create:precision_mechanism")}))
    lines.append(r_shaped("create:powered_latch","create","create:powered_latch",1,
        ["R R"," P ","R R"],{"R":ing("minecraft:redstone"),"P":ing("create:precision_mechanism")}))
    lines.append(r_shaped("create:powered_toggle_latch","create","create:powered_toggle_latch",1,
        ["R R"," P ","R R"],{"R":ing("minecraft:redstone"),"P":ing("create:precision_mechanism")}))
    
    # Trains
    lines.append("\n// ─── TRAINS ─────────────────────────────────────────────")
    lines.append(r_shaped("create:railway_casing","create","create:railway_casing",1,
        ["PPP","PAP","PPP"],{"P":ing("create:brass_casing"),"A":ing("create:precision_mechanism")}))
    lines.append(r_shaped("create:train_track","create","create:train_track",6,
        [" I "," IP"," I "],{"I":ing("minecraft:iron_ingot"),"P":ing("create:brass_casing")}))
    lines.append(r_shaped("create:schedule","create","create:schedule",1,
        ["PP","PP"],{"P":ing("minecraft:paper")}))
    lines.append(r_shaped("create:train_station","create","create:train_station",1,
        ["III","IPI","III"],{"I":ing("create:brass_casing"),"P":ing("create:precision_mechanism")}))
    lines.append(r_shaped("create:signal","create","create:signal",1,
        [" I ","IPI"," I "],{"I":ing("create:brass_casing"),"P":ing("create:precision_mechanism")}))
    
    write_footer(lines, "CREATE")
    return "\n".join(lines)

if __name__ == "__main__":
    out = generate()
    os.makedirs("src/data/recipes", exist_ok=True)
    with open("src/data/recipes/create.ts","w") as f: f.write(out)
    rc = out.count("r('")
    print(f"Generated create.ts — {rc} recipes")
