/**
 * Texture resolver — maps item IDs to local texture paths
 * Textures are stored in public/textures/ and served by Vite
 */

// Mapping of item IDs to their texture file paths
// Key: item ID (e.g., "minecraft:iron_ingot")
// Value: path relative to /textures/ (e.g., "minecraft/iron_ingot.png")
const TEXTURE_MAP: Record<string, string> = {
  // ─── Vanilla items ───
  'minecraft:iron_ingot':       'minecraft/iron_ingot.png',
  'minecraft:gold_ingot':       'minecraft/gold_ingot.png',
  'minecraft:copper_ingot':     'minecraft/copper_ingot.png',
  'minecraft:diamond':          'minecraft/diamond.png',
  'minecraft:emerald':          'minecraft/emerald.png',
  'minecraft:redstone':         'minecraft/redstone.png',
  'minecraft:coal':             'minecraft/coal.png',
  'minecraft:charcoal':         'minecraft/charcoal.png',
  'minecraft:quartz':           'minecraft/quartz.png',
  'minecraft:lapis_lazuli':     'minecraft/lapis_lazuli.png',
  'minecraft:netherite_ingot':  'minecraft/netherite_ingot.png',
  'minecraft:stick':            'minecraft/stick.png',
  'minecraft:book':             'minecraft/book.png',
  'minecraft:paper':            'minecraft/paper.png',
  'minecraft:string':           'minecraft/string.png',
  'minecraft:feather':          'minecraft/feather.png',
  'minecraft:leather':          'minecraft/leather.png',
  'minecraft:flint':            'minecraft/flint.png',
  'minecraft:iron_nugget':      'minecraft/iron_nugget.png',
  'minecraft:gold_nugget':      'minecraft/gold_nugget.png',
  'minecraft:blaze_rod':        'minecraft/blaze_rod.png',
  'minecraft:ender_pearl':      'minecraft/ender_pearl.png',
  'minecraft:bucket':           'minecraft/bucket.png',
  'minecraft:lava_bucket':      'minecraft/lava_bucket.png',
  'minecraft:water_bucket':     'minecraft/water_bucket.png',
  'minecraft:iron_pickaxe':     'minecraft/iron_pickaxe.png',
  'minecraft:iron_axe':         'minecraft/iron_axe.png',
  'minecraft:iron_shovel':      'minecraft/iron_shovel.png',
  'minecraft:iron_hoe':         'minecraft/iron_hoe.png',
  'minecraft:iron_sword':       'minecraft/iron_sword.png',
  'minecraft:iron_helmet':      'minecraft/iron_helmet.png',
  'minecraft:iron_chestplate':  'minecraft/iron_chestplate.png',
  'minecraft:iron_leggings':    'minecraft/iron_leggings.png',
  'minecraft:iron_boots':       'minecraft/iron_boots.png',

  // Vanilla — block textures
  'minecraft:stone':            'minecraft/block/stone.png',
  'minecraft:cobblestone':      'minecraft/block/cobblestone.png',
  'minecraft:andesite':         'minecraft/block/andesite.png',
  'minecraft:diorite':          'minecraft/block/diorite.png',
  'minecraft:granite':          'minecraft/block/granite.png',
  'minecraft:oak_planks':       'minecraft/block/oak_planks.png',
  'minecraft:oak_log':          'minecraft/block/oak_log_top.png',
  'minecraft:glass':            'minecraft/block/glass.png',
  'minecraft:obsidian':         'minecraft/block/obsidian.png',
  'minecraft:crafting_table':   'minecraft/block/crafting_table_front.png',
  'minecraft:furnace':          'minecraft/block/furnace_front.png',
  'minecraft:chest':            'minecraft/entity/normal.png',
  'minecraft:anvil':            'minecraft/block/anvil_top.png',
  'minecraft:hopper':           'minecraft/block/hopper_outside.png',
  'minecraft:piston':           'minecraft/block/piston_top.png',
  'minecraft:sticky_piston':    'minecraft/block/piston_top_sticky.png',
  'minecraft:observer':         'minecraft/block/observer_front.png',
  'minecraft:dispenser':        'minecraft/block/dispenser_front.png',
  'minecraft:dropper':          'minecraft/block/dropper_front.png',
  'minecraft:redstone_repeater':'minecraft/block/repeater.png',
  'minecraft:netherite_block':  'minecraft/block/netherite_block.png',
  'minecraft:diamond_block':    'minecraft/block/diamond_block.png',
  'minecraft:gold_block':       'minecraft/block/gold_block.png',
  'minecraft:iron_block':       'minecraft/block/iron_block.png',
  'minecraft:copper_block':     'minecraft/block/copper_block.png',

  // ─── Mekanism ───
  'mekanism:osmium_ingot':      'mekanism/ingot_osmium.png',
  'mekanism:tin_ingot':         'mekanism/ingot_tin.png',
  'mekanism:lead_ingot':        'mekanism/ingot_lead.png',
  'mekanism:uranium_ingot':     'mekanism/ingot_uranium.png',
  'mekanism:bronze_ingot':      'mekanism/ingot_bronze.png',
  'mekanism:steel_ingot':       'mekanism/ingot_steel.png',
  'mekanism:osmium_ore':        'mekanism/raw_osmium.png',
  'mekanism:tin_ore':           'mekanism/raw_tin.png',
  'mekanism:lead_ore':          'mekanism/raw_lead.png',
  'mekanism:uranium_ore':       'mekanism/raw_uranium.png',
  'mekanism:fluorite_ore':      'mekanism/fluorite_gem.png',
  'mekanism:control_circuit_basic':    'mekanism/basic_control_circuit.png',
  'mekanism:control_circuit_advanced': 'mekanism/advanced_control_circuit.png',
  'mekanism:control_circuit_elite':    'mekanism/elite_control_circuit.png',
  'mekanism:control_circuit_ultimate': 'mekanism/ultimate_control_circuit.png',
  'mekanism:alloy_atomic':      'mekanism/alloy_atomic.png',
  'mekanism:alloy_infused':     'mekanism/alloy_infused.png',
  'mekanism:alloy_reinforced':  'mekanism/alloy_reinforced.png',
  'mekanism:enriched_diamond':  'mekanism/enriched_diamond.png',
  'mekanism:enriched_gold':     'mekanism/enriched_gold.png',
  'mekanism:enriched_iron':     'mekanism/enriched_iron.png',
  'mekanism:enriched_osmium':   'mekanism/enriched_refined_obsidian.png',
  'mekanism:enriched_redstone': 'mekanism/enriched_redstone.png',
  'mekanism:enriched_tin':      'mekanism/enriched_tin.png',
  'mekanism:substrate':         'mekanism/substrate.png',
  'mekanism:hdpe_rod':          'mekanism/hdpe_rod.png',
  'mekanism:hdpe_sheet':        'mekanism/hdpe_sheet.png',
  'mekanism:bio_fuel':          'mekanism/bio_fuel.png',
  'mekanism:basic_energy_cube':    'mekanism/block/basic_induction_cell.png',
  'mekanism:advanced_energy_cube': 'mekanism/block/advanced_induction_cell.png',
  'mekanism:elite_energy_cube':    'mekanism/block/elite_induction_cell.png',
  'mekanism:ultimate_energy_cube': 'mekanism/block/ultimate_induction_cell.png',

  // ─── Create ───
  'create:andesite_alloy':      'create/andesite_alloy.png',
  'create:brass_ingot':         'create/brass_ingot.png',
  'create:zinc_ingot':          'create/zinc_ingot.png',
  'create:iron_sheet':          'create/iron_sheet.png',
  'create:copper_sheet':        'create/copper_sheet.png',
  'create:brass_sheet':         'create/brass_sheet.png',
  'create:precision_mechanism': 'create/precision_mechanism.png',
  'create:cogwheel':            'create/block/cogwheel.png',
  'create:large_cogwheel':      'create/block/large_cogwheel.png',
  'create:shaft':               'create/block/gantry_shaft.png',
  'create:gearbox':             'create/block/gearbox.png',
  'create:mechanical_piston':   'create/block/piston_bottom.png',
  'create:mechanical_bearing':  'create/block/mechanical_bearing_side.png',
  'create:water_wheel':         'create/block/waterwheel_metal.png',
  'create:windmill_bearing':    'create/block/windmill_bearing_side.png',
  'create:belt_connector':      'create/block/belt.png',

  // ─── Thermal ───
  'thermal:tin_ingot':          'thermal/tin_ingot.png',
  'thermal:lead_ingot':         'thermal/lead_ingot.png',
  'thermal:silver_ingot':       'thermal/silver_ingot.png',
  'thermal:nickel_ingot':       'thermal/nickel_ingot.png',
  'thermal:bronze_ingot':       'thermal/bronze_ingot.png',
  'thermal:constantan_ingot':   'thermal/constantan_ingot.png',
  'thermal:electrum_ingot':     'thermal/electrum_ingot.png',
  'thermal:invar_ingot':        'thermal/invar_ingot.png',
  'thermal:steel_ingot':        'thermal/invar_ingot.png',     // fallback visual
  'thermal:signalum_ingot':     'thermal/electrum_ingot.png',  // fallback visual
  'thermal:lumium_ingot':       'thermal/electrum_ingot.png',  // fallback visual
  'thermal:enderium_ingot':     'thermal/electrum_ingot.png',  // fallback visual
  'thermal:redstone_servo':     'thermal/electrum_gear.png',   // fallback visual
  'thermal:rf_coil':            'thermal/electrum_nugget.png', // fallback visual
};

export function getItemTexture(itemId: string): string | undefined {
  const path = TEXTURE_MAP[itemId];
  if (!path) return undefined;
  return `/textures/${path}`;
}
