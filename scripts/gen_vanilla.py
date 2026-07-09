#!/usr/bin/env python3
"""Generate vanilla.ts — all vanilla Minecraft recipes"""
import os
from generate_base import *

def generate():
    lines = []
    write_header(lines, "V")
    lines.append("")
    
    # ─── SMELTING ───
    lines.append("// ─── SMELTING ─────────────────────────────────────────────────")
    for rid, out, ins in [
        ("minecraft:iron_ingot_smelt", "minecraft:iron_ingot", [("minecraft:raw_iron", 1)]),
        ("minecraft:gold_ingot_smelt", "minecraft:gold_ingot", [("minecraft:raw_gold", 1)]),
        ("minecraft:copper_ingot_smelt", "minecraft:copper_ingot", [("minecraft:raw_copper", 1)]),
        ("minecraft:iron_ingot_smelt_ore", "minecraft:iron_ingot", [("minecraft:iron_ore", 1)]),
        ("minecraft:gold_ingot_smelt_ore", "minecraft:gold_ingot", [("minecraft:gold_ore", 1)]),
        ("minecraft:copper_ingot_smelt_ore", "minecraft:copper_ingot", [("minecraft:copper_ore", 1)]),
        ("minecraft:glass_smelt", "minecraft:glass", [("minecraft:sand", 1)]),
        ("minecraft:charcoal_smelt", "minecraft:charcoal", [("minecraft:oak_log", 1)]),
        ("minecraft:stone_smelt", "minecraft:stone", [("minecraft:cobblestone", 1)]),
        ("minecraft:brick_smelt", "minecraft:brick", [("minecraft:clay_ball", 1)]),
        ("minecraft:netherite_scrap_smelt", "minecraft:netherite_scrap", [("minecraft:ancient_debris", 1)]),
        ("minecraft:terracotta_smelt", "minecraft:terracotta", [("minecraft:clay", 1)]),
        ("minecraft:glass_bottle_smelt", "minecraft:glass_bottle", [("minecraft:glass", 1)]),
        ("minecraft:lime_dye_smelt", "minecraft:lime_dye", [("minecraft:kelp", 1)]),
        ("minecraft:cooked_beef_smelt", "minecraft:cooked_beef", [("minecraft:beef", 1)]),
        ("minecraft:cooked_chicken_smelt", "minecraft:cooked_chicken", [("minecraft:chicken", 1)]),
        ("minecraft:cooked_porkchop_smelt", "minecraft:cooked_porkchop", [("minecraft:porkchop", 1)]),
        ("minecraft:cooked_mutton_smelt", "minecraft:cooked_mutton", [("minecraft:mutton", 1)]),
        ("minecraft:cooked_cod_smelt", "minecraft:cooked_cod", [("minecraft:cod", 1)]),
        ("minecraft:cooked_salmon_smelt", "minecraft:cooked_salmon", [("minecraft:salmon", 1)]),
        ("minecraft:baked_potato_smelt", "minecraft:baked_potato", [("minecraft:potato", 1)]),
        ("minecraft:dried_kelp_smelt", "minecraft:dried_kelp", [("minecraft:kelp", 1)]),
        ("minecraft:sponge_smelt", "minecraft:sponge", [("minecraft:wet_sponge", 1)]),
        ("minecraft:cactus_green_smelt", "minecraft:green_dye", [("minecraft:cactus", 1)]),
    ]:
        lines.append(r_simple(rid, "smelting", "minecraft", out, 1, ins))
    
    # ─── BLASTING ───
    lines.append("\n// ─── BLASTING ─────────────────────────────────────────────────")
    for rid, out, ins in [
        ("minecraft:iron_ingot_blast", "minecraft:iron_ingot", [("minecraft:raw_iron", 1)]),
        ("minecraft:gold_ingot_blast", "minecraft:gold_ingot", [("minecraft:raw_gold", 1)]),
        ("minecraft:copper_ingot_blast", "minecraft:copper_ingot", [("minecraft:raw_copper", 1)]),
        ("minecraft:iron_ingot_blast_ore", "minecraft:iron_ingot", [("minecraft:iron_ore", 1)]),
        ("minecraft:gold_ingot_blast_ore", "minecraft:gold_ingot", [("minecraft:gold_ore", 1)]),
        ("minecraft:copper_ingot_blast_ore", "minecraft:copper_ingot", [("minecraft:copper_ore", 1)]),
        ("minecraft:netherite_scrap_blast", "minecraft:netherite_scrap", [("minecraft:ancient_debris", 1)]),
        ("minecraft:glass_blast", "minecraft:glass", [("minecraft:sand", 1)]),
        ("minecraft:stone_blast", "minecraft:stone", [("minecraft:cobblestone", 1)]),
        ("minecraft:terracotta_blast", "minecraft:terracotta", [("minecraft:clay", 1)]),
    ]:
        lines.append(r_simple(rid, "blasting", "minecraft", out, 1, ins))
    
    # ─── BLOCKS ───
    lines.append("\n// ─── BLOCKS FROM INGOTS/MATERIALS ────────────────────────────────")
    for block, mat in [
        ("iron_block", "iron_ingot"), ("gold_block", "gold_ingot"),
        ("diamond_block", "diamond"), ("netherite_block", "netherite_ingot"),
        ("copper_block", "copper_ingot"), ("lapis_block", "lapis_lazuli"),
        ("coal_block", "coal"), ("emerald_block", "emerald"),
        ("redstone_block", "redstone"), ("quartz_block", "quartz"),
        ("amethyst_block", "amethyst_shard"), ("raw_iron_block", "raw_iron"),
        ("raw_gold_block", "raw_gold"), ("raw_copper_block", "raw_copper"),
        ("bone_block", "bone_meal"), ("honey_block", "honey_bottle"),
        ("slime_block", "slime_ball"), ("snow_block", "snowball"),
        ("clay", "clay_ball"), ("nether_wart_block", "nether_wart"),
        ("warped_wart_block", "warped_wart"),
    ]:
        fid = f"minecraft:{block}"
        mid = f"minecraft:{mat}"
        lines.append(r_shaped(f"minecraft:{block}", "minecraft", fid, 1,
            ["III", "III", "III"], {"I": ing(mid)}))
    
    # ─── UN-BLOCKS ───
    lines.append("\n// ─── UN-BLOCKS (9x → 1) ──────────────────────────────────────────────")
    for item, src, cnt in [
        ("iron_ingot", "iron_block", 9), ("gold_ingot", "gold_block", 9),
        ("diamond", "diamond_block", 9), ("netherite_ingot", "netherite_block", 9),
        ("copper_ingot", "copper_block", 9), ("lapis_lazuli", "lapis_block", 9),
        ("coal", "coal_block", 9), ("emerald", "emerald_block", 9),
        ("redstone", "redstone_block", 9), ("quartz", "quartz_block", 4),
        ("amethyst_shard", "amethyst_block", 4),
        ("raw_iron", "raw_iron_block", 9), ("raw_gold", "raw_gold_block", 9),
        ("raw_copper", "raw_copper_block", 9),
        ("clay_ball", "clay", 4), ("snowball", "snow_block", 4),
        ("slime_ball", "slime_block", 9), ("honey_bottle", "honey_block", 4),
        ("bone_meal", "bone_block", 9),
    ]:
        lines.append(r_shaped(f"minecraft:{item}_from_{src}", "minecraft", f"minecraft:{item}", cnt,
            ["I"], {"I": ing(f"minecraft:{src}")}))
    
    # ─── NUGGETS ───
    lines.append("\n// ─── NUGGETS ─────────────────────────────────────────────────")
    lines.append(r_shaped("minecraft:iron_nugget", "minecraft", "minecraft:iron_nugget", 9,
        ["I"], {"I": ing("minecraft:iron_ingot")}))
    lines.append(r_shaped("minecraft:gold_nugget", "minecraft", "minecraft:gold_nugget", 9,
        ["I"], {"I": ing("minecraft:gold_ingot")}))
    lines.append(r_shaped("minecraft:iron_ingot_from_nuggets", "minecraft", "minecraft:iron_ingot", 1,
        ["III", "III", "III"], {"I": ing("minecraft:iron_nugget")}))
    lines.append(r_shaped("minecraft:gold_ingot_from_nuggets", "minecraft", "minecraft:gold_ingot", 1,
        ["III", "III", "III"], {"I": ing("minecraft:gold_nugget")}))
    
    # ─── TOOLS ───
    for tier_name, mat in [("wooden", "minecraft:oak_planks"), ("stone", "minecraft:cobblestone"),
                           ("iron", "minecraft:iron_ingot"), ("golden", "minecraft:gold_ingot"),
                           ("diamond", "minecraft:diamond"), ("netherite", "minecraft:netherite_ingot")]:
        lines.append(f"\n// ─── {tier_name.upper()} TOOLS ────────────────────────────────────────────")
        for tool, pat, keys_extra in [
            ("sword", ["I", "I", "S"], {}),
            ("pickaxe", ["III", " S ", " S "], {}),
            ("axe", ["II", "IS", " S"], {}),
            ("shovel", ["I", "S", "S"], {}),
            ("hoe", ["II", " S", " S"], {}),
        ]:
            keys = {"I": ing(mat), "S": ing("minecraft:stick")}
            keys.update(keys_extra)
            lines.append(r_shaped(f"minecraft:{tier_name}_{tool}", "minecraft", 
                f"minecraft:{tier_name}_{tool}", 1, pat, keys))
    
    # ─── ARMOR ───
    for tier_name, mat in [("leather", "minecraft:leather"), ("chainmail", "minecraft:iron_ingot"),
                           ("iron", "minecraft:iron_ingot"), ("golden", "minecraft:gold_ingot"),
                           ("diamond", "minecraft:diamond"), ("netherite", "minecraft:netherite_ingot")]:
        lines.append(f"\n// ─── {tier_name.upper()} ARMOR ────────────────────────────────────────────")
        lines.append(r_shaped(f"minecraft:{tier_name}_helmet", "minecraft", f"minecraft:{tier_name}_helmet", 1,
            ["III", "I I"], {"I": ing(mat)}))
        lines.append(r_shaped(f"minecraft:{tier_name}_chestplate", "minecraft", f"minecraft:{tier_name}_chestplate", 1,
            ["I I", "III", "III"], {"I": ing(mat)}))
        lines.append(r_shaped(f"minecraft:{tier_name}_leggings", "minecraft", f"minecraft:{tier_name}_leggings", 1,
            ["III", "I I", "I I"], {"I": ing(mat)}))
        lines.append(r_shaped(f"minecraft:{tier_name}_boots", "minecraft", f"minecraft:{tier_name}_boots", 1,
            ["I I", "I I"], {"I": ing(mat)}))
    
    # ─── USEFUL VANILLA ───
    lines.append("\n// ─── USEFUL CRAFTS ───────────────────────────────────────────")
    crafts = [
        ("minecraft:stick", "minecraft:stick", 4, ["P", "P"], {"P": ing("minecraft:oak_planks")}),
        ("minecraft:furnace", "minecraft:furnace", 1, ["CCC", "C C", "CCC"], {"C": ing("minecraft:cobblestone")}),
        ("minecraft:chest", "minecraft:chest", 1, ["PPP", "P P", "PPP"], {"P": ing("minecraft:oak_planks")}),
        ("minecraft:crafting_table", "minecraft:crafting_table", 1, ["PP", "PP"], {"P": ing("minecraft:oak_planks")}),
        ("minecraft:torch", "minecraft:torch", 4, ["C", "S"], {"C": ing("minecraft:coal"), "S": ing("minecraft:stick")}),
        ("minecraft:ladder", "minecraft:ladder", 3, ["S S", "SSS", "S S"], {"S": ing("minecraft:stick")}),
        ("minecraft:iron_bars", "minecraft:iron_bars", 16, ["III", "III"], {"I": ing("minecraft:iron_ingot")}),
        ("minecraft:glass_pane", "minecraft:glass_pane", 16, ["GGG", "GGG"], {"G": ing("minecraft:glass")}),
        ("minecraft:anvil", "minecraft:anvil", 1, ["BBB", " I ", "III"], {"B": ing("minecraft:iron_block"), "I": ing("minecraft:iron_ingot")}),
        ("minecraft:enchanting_table", "minecraft:enchanting_table", 1, [" B ", "DOD", "OOO"], {"B": ing("minecraft:book"), "D": ing("minecraft:diamond"), "O": ing("minecraft:obsidian")}),
        ("minecraft:brewing_stand", "minecraft:brewing_stand", 1, [" I ", "BBB"], {"I": ing("minecraft:blaze_rod"), "B": ing("minecraft:cobblestone")}),
        ("minecraft:hopper", "minecraft:hopper", 1, ["I I", "ICI", " I "], {"I": ing("minecraft:iron_ingot"), "C": ing("minecraft:chest")}),
        ("minecraft:piston", "minecraft:piston", 1, ["PPP", "CIC", "CRC"], {"P": ing("minecraft:oak_planks"), "C": ing("minecraft:cobblestone"), "I": ing("minecraft:iron_ingot"), "R": ing("minecraft:redstone")}),
        ("minecraft:sticky_piston", "minecraft:sticky_piston", 1, ["S", "P"], {"S": ing("minecraft:slime_ball"), "P": ing("minecraft:piston")}),
        ("minecraft:observer", "minecraft:observer", 1, ["CCC", "CQQ", "CCC"], {"C": ing("minecraft:cobblestone"), "Q": ing("minecraft:redstone")}),
        ("minecraft:book", "minecraft:book", 1, ["P", "P", "P"], {"P": ing("minecraft:paper")}),
        ("minecraft:compass", "minecraft:compass", 1, [" I ", "IRI", " I "], {"I": ing("minecraft:iron_ingot"), "R": ing("minecraft:redstone")}),
        ("minecraft:clock", "minecraft:clock", 1, [" G ", "GRG", " G "], {"G": ing("minecraft:gold_ingot"), "R": ing("minecraft:redstone")}),
        ("minecraft:bucket", "minecraft:bucket", 1, ["I I", " I "], {"I": ing("minecraft:iron_ingot")}),
        ("minecraft:shears", "minecraft:shears", 1, ["I", "I"], {"I": ing("minecraft:iron_ingot")}),
        ("minecraft:flint_and_steel", "minecraft:flint_and_steel", 1, ["I", "F"], {"I": ing("minecraft:iron_ingot"), "F": ing("minecraft:flint")}),
        ("minecraft:shield", "minecraft:shield", 1, ["PIP", "PPP", " P "], {"P": ing("minecraft:oak_planks"), "I": ing("minecraft:iron_ingot")}),
        ("minecraft:fishing_rod", "minecraft:fishing_rod", 1, ["  S", " S ", "S S"], {"S": ing("minecraft:stick")}),
        ("minecraft:bow", "minecraft:bow", 1, ["IS ", "I S", "IS "], {"I": ing("minecraft:stick"), "S": ing("minecraft:string")}),
        ("minecraft:arrow", "minecraft:arrow", 4, ["F", "S", "F"], {"F": ing("minecraft:flint"), "S": ing("minecraft:stick")}),
        ("minecraft:beacon", "minecraft:beacon", 1, ["GGG", "GSG", "OOO"], {"G": ing("minecraft:glass"), "S": ing("minecraft:nether_star"), "O": ing("minecraft:obsidian")}),
        ("minecraft:ender_chest", "minecraft:ender_chest", 1, ["EEE", "ECE", "EEE"], {"E": ing("minecraft:ender_eye"), "C": ing("minecraft:obsidian")}),
        ("minecraft:jukebox", "minecraft:jukebox", 1, ["PPP", "PDP", "PPP"], {"P": ing("minecraft:oak_planks"), "D": ing("minecraft:diamond")}),
        ("minecraft:note_block", "minecraft:note_block", 1, ["PPP", "PRP", "PPP"], {"P": ing("minecraft:oak_planks"), "R": ing("minecraft:redstone")}),
        ("minecraft:respawn_anchor", "minecraft:respawn_anchor", 1, ["CCC", "GGG", "CCC"], {"C": ing("minecraft:crying_obsidian"), "G": ing("minecraft:glowstone")}),
        ("minecraft:conduit", "minecraft:conduit", 1, ["HHH", "HNH", "HHH"], {"H": ing("minecraft:nautilus_shell"), "N": ing("minecraft:heart_of_the_sea")}),
        ("minecraft:tnt", "minecraft:tnt", 1, ["GSG", "SGS", "GSG"], {"G": ing("minecraft:gunpowder"), "S": ing("minecraft:sand")}),
        ("minecraft:rail", "minecraft:rail", 16, ["I I", "ISI", "I I"], {"I": ing("minecraft:iron_ingot"), "S": ing("minecraft:stick")}),
        ("minecraft:powered_rail", "minecraft:powered_rail", 6, ["G G", "GSG", "G G"], {"G": ing("minecraft:gold_ingot"), "S": ing("minecraft:stick")}),
        ("minecraft:detector_rail", "minecraft:detector_rail", 6, ["I I", "IPI", "IRI"], {"I": ing("minecraft:iron_ingot"), "P": ing("minecraft:stone_pressure_plate"), "R": ing("minecraft:redstone")}),
        ("minecraft:minecart", "minecraft:minecart", 1, ["I I", "III"], {"I": ing("minecraft:iron_ingot")}),
        ("minecraft:saddle", "minecraft:saddle", 1, ["LLL", "LIL", "I I"], {"L": ing("minecraft:leather"), "I": ing("minecraft:iron_ingot")}),
        ("minecraft:name_tag", "minecraft:name_tag", 1, ["PP", "PS"], {"P": ing("minecraft:paper"), "S": ing("minecraft:string")}),
        ("minecraft:lead", "minecraft:lead", 2, ["SS ", "SBS", "  S"], {"S": ing("minecraft:string"), "B": ing("minecraft:slime_ball")}),
    ]
    for rid, out, cnt, pat, keys in crafts:
        lines.append(r_shaped(rid, "minecraft", out, cnt, pat, keys))
    
    # ─── REDSTONE ───
    lines.append("\n// ─── REDSTONE COMPONENTS ─────────────────────────────────────────")
    redstone = [
        ("minecraft:redstone_torch", "minecraft:redstone_torch", 1, ["R", "S"], {"R": ing("minecraft:redstone"), "S": ing("minecraft:stick")}),
        ("minecraft:repeater", "minecraft:repeater", 1, ["SRS", "III"], {"S": ing("minecraft:redstone_torch"), "R": ing("minecraft:redstone"), "I": ing("minecraft:stone")}),
        ("minecraft:comparator", "minecraft:comparator", 1, [" S ", "SQS", "III"], {"S": ing("minecraft:redstone_torch"), "Q": ing("minecraft:quartz"), "I": ing("minecraft:stone")}),
        ("minecraft:dropper", "minecraft:dropper", 1, ["CCC", "C C", "CRC"], {"C": ing("minecraft:cobblestone"), "R": ing("minecraft:redstone")}),
        ("minecraft:dispenser", "minecraft:dispenser", 1, ["CCC", "CBC", "CRC"], {"C": ing("minecraft:cobblestone"), "B": ing("minecraft:bow"), "R": ing("minecraft:redstone")}),
        ("minecraft:target", "minecraft:target", 1, ["RBR", "BHB", "RBR"], {"R": ing("minecraft:redstone"), "B": ing("minecraft:iron_ingot"), "H": ing("minecraft:hay_block")}),
        ("minecraft:lectern", "minecraft:lectern", 1, ["SSS", " B ", " S "], {"S": ing("minecraft:oak_slab"), "B": ing("minecraft:book")}),
        ("minecraft:grindstone", "minecraft:grindstone", 1, ["I I", " S ", "PPP"], {"I": ing("minecraft:stick"), "S": ing("minecraft:stone_slab"), "P": ing("minecraft:oak_planks")}),
        ("minecraft:smithing_table", "minecraft:smithing_table", 1, ["II", "PP", "PP"], {"I": ing("minecraft:iron_ingot"), "P": ing("minecraft:oak_planks")}),
        ("minecraft:composter", "minecraft:composter", 1, ["S S", "S S", "SSS"], {"S": ing("minecraft:oak_slab")}),
        ("minecraft:cauldron", "minecraft:cauldron", 1, ["I I", "I I", "III"], {"I": ing("minecraft:iron_ingot")}),
        ("minecraft:blast_furnace", "minecraft:blast_furnace", 1, ["III", "IFI", "SSS"], {"I": ing("minecraft:iron_ingot"), "F": ing("minecraft:furnace"), "S": ing("minecraft:smooth_stone")}),
        ("minecraft:smoker", "minecraft:smoker", 1, ["LLL", "LFL", "LLL"], {"L": ing("minecraft:oak_log"), "F": ing("minecraft:furnace")}),
        ("minecraft:campfire", "minecraft:campfire", 1, [" S ", "S S", "LLL"], {"S": ing("minecraft:stick"), "L": ing("minecraft:oak_log")}),
        ("minecraft:bell", "minecraft:bell", 1, ["GGG", "G G", "GGG"], {"G": ing("minecraft:gold_ingot")}),
        ("minecraft:lodestone", "minecraft:lodestone", 1, ["CCC", "CIC", "CCC"], {"C": ing("minecraft:chiseled_stone_bricks"), "I": ing("minecraft:netherite_ingot")}),
        ("minecraft:daylight_detector", "minecraft:daylight_detector", 1, ["GGG", "QQQ", "SSS"], {"G": ing("minecraft:glass"), "Q": ing("minecraft:quartz"), "S": ing("minecraft:oak_slab")}),
    ]
    for rid, out, cnt, pat, keys in redstone:
        lines.append(r_shaped(rid, "minecraft", out, cnt, pat, keys))
    
    # ─── DECOR / BLOCKS ───
    lines.append("\n// ─── DECORATIVE BLOCKS ────────────────────────────────────────────")
    decor = [
        ("minecraft:stone_bricks", "minecraft:stone_bricks", 4, ["SS", "SS"], {"S": ing("minecraft:stone")}),
        ("minecraft:bricks_dec", "minecraft:bricks", 1, ["BB", "BB"], {"B": ing("minecraft:brick")}),
        ("minecraft:oak_planks_from_log", "minecraft:oak_planks", 4, ["L"], {"L": ing("minecraft:oak_log")}),
        ("minecraft:oak_stairs", "minecraft:oak_stairs", 4, ["P  ", "PP ", "PPP"], {"P": ing("minecraft:oak_planks")}),
        ("minecraft:cobblestone_stairs", "minecraft:cobblestone_stairs", 4, ["C  ", "CC ", "CCC"], {"C": ing("minecraft:cobblestone")}),
        ("minecraft:stone_stairs", "minecraft:stone_stairs", 4, ["S  ", "SS ", "SSS"], {"S": ing("minecraft:stone")}),
        ("minecraft:oak_slab", "minecraft:oak_slab", 6, ["PPP"], {"P": ing("minecraft:oak_planks")}),
        ("minecraft:cobblestone_slab", "minecraft:cobblestone_slab", 6, ["CCC"], {"C": ing("minecraft:cobblestone")}),
        ("minecraft:stone_slab", "minecraft:stone_slab", 6, ["SSS"], {"S": ing("minecraft:stone")}),
        ("minecraft:oak_fence", "minecraft:oak_fence", 3, ["PSP", "PSP"], {"P": ing("minecraft:oak_planks"), "S": ing("minecraft:stick")}),
        ("minecraft:oak_fence_gate", "minecraft:oak_fence_gate", 1, ["SPS", "SPS"], {"P": ing("minecraft:oak_planks"), "S": ing("minecraft:stick")}),
        ("minecraft:oak_door", "minecraft:oak_door", 3, ["PP", "PP", "PP"], {"P": ing("minecraft:oak_planks")}),
        ("minecraft:oak_trapdoor", "minecraft:oak_trapdoor", 2, ["PPP", "PPP"], {"P": ing("minecraft:oak_planks")}),
        ("minecraft:cobblestone_wall", "minecraft:cobblestone_wall", 6, ["CCC", "CCC"], {"C": ing("minecraft:cobblestone")}),
        ("minecraft:stone_pressure_plate", "minecraft:stone_pressure_plate", 1, ["SS"], {"S": ing("minecraft:stone")}),
        ("minecraft:oak_pressure_plate", "minecraft:oak_pressure_plate", 1, ["PP"], {"P": ing("minecraft:oak_planks")}),
        ("minecraft:stone_button", "minecraft:stone_button", 1, ["S"], {"S": ing("minecraft:stone")}),
        ("minecraft:oak_button", "minecraft:oak_button", 1, ["P"], {"P": ing("minecraft:oak_planks")}),
        ("minecraft:paper", "minecraft:paper", 3, ["SSS"], {"S": ing("minecraft:sugar_cane")}),
        ("minecraft:bookshelf", "minecraft:bookshelf", 1, ["PPP", "BBB", "PPP"], {"P": ing("minecraft:oak_planks"), "B": ing("minecraft:book")}),
        ("minecraft:painting", "minecraft:painting", 1, ["SSS", "SWS", "SSS"], {"S": ing("minecraft:stick"), "W": ing("minecraft:white_wool")}),
        ("minecraft:bed", "minecraft:white_bed", 1, ["WWW", "PPP"], {"W": ing("minecraft:white_wool"), "P": ing("minecraft:oak_planks")}),
        ("minecraft:lava_bucket", "minecraft:lava_bucket", 1, ["B", "L"], {"B": ing("minecraft:bucket"), "L": ing("minecraft:lava_bucket")}),
    ]
    for rid, out, cnt, pat, keys in decor:
        lines.append(r_shaped(rid, "minecraft", out, cnt, pat, keys))
    
    write_footer(lines, "V")
    return "\n".join(lines)

if __name__ == "__main__":
    out = generate()
    os.makedirs("src/data/recipes", exist_ok=True)
    with open("src/data/recipes/vanilla.ts", "w") as f:
        f.write(out)
    rc = out.count("r('")
    print(f"Generated vanilla.ts — {rc} recipes")
