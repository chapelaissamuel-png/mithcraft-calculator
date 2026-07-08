/**
 * Minecraft Item Texture Downloader v2
 * Downloads item textures for vanilla + mods into public/textures/
 */
import { writeFileSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const TEXTURE_DIR = join(__dirname, '..', 'public', 'textures');

// Texture source: for each item ID, the URL to fetch and the local path to save
// Uses: mcasset.cloud for vanilla, raw.githubusercontent.com for mods
const TEXTURES = {
  // ─── Vanilla Minecraft (mcasset.cloud) ───
  'minecraft:iron_ingot':       'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/iron_ingot.png',
  'minecraft:gold_ingot':       'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/gold_ingot.png',
  'minecraft:copper_ingot':     'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/copper_ingot.png',
  'minecraft:diamond':          'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/diamond.png',
  'minecraft:emerald':          'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/emerald.png',
  'minecraft:redstone':         'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/redstone.png',
  'minecraft:coal':             'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/coal.png',
  'minecraft:charcoal':         'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/charcoal.png',
  'minecraft:quartz':           'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/quartz.png',
  'minecraft:lapis_lazuli':     'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/lapis_lazuli.png',
  'minecraft:netherite_ingot':  'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/netherite_ingot.png',
  'minecraft:stick':            'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/stick.png',
  'minecraft:book':             'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/book.png',
  'minecraft:paper':            'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/paper.png',
  'minecraft:string':           'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/string.png',
  'minecraft:feather':          'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/feather.png',
  'minecraft:leather':          'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/leather.png',
  'minecraft:flint':            'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/flint.png',
  'minecraft:iron_nugget':      'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/iron_nugget.png',
  'minecraft:gold_nugget':      'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/gold_nugget.png',
  'minecraft:blaze_rod':        'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/blaze_rod.png',
  'minecraft:ender_pearl':      'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/ender_pearl.png',
  'minecraft:bucket':           'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/bucket.png',
  'minecraft:lava_bucket':      'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/lava_bucket.png',
  'minecraft:water_bucket':     'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/water_bucket.png',
  'minecraft:iron_pickaxe':     'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/iron_pickaxe.png',
  'minecraft:iron_axe':         'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/iron_axe.png',
  'minecraft:iron_shovel':      'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/iron_shovel.png',
  'minecraft:iron_hoe':         'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/iron_hoe.png',
  'minecraft:iron_sword':       'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/iron_sword.png',
  'minecraft:iron_helmet':      'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/iron_helmet.png',
  'minecraft:iron_chestplate':  'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/iron_chestplate.png',
  'minecraft:iron_leggings':    'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/iron_leggings.png',
  'minecraft:iron_boots':       'https://assets.mcasset.cloud/latest/assets/minecraft/textures/item/iron_boots.png',

  // Vanilla — block textures
  'minecraft:stone':            'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/stone.png',
  'minecraft:cobblestone':      'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/cobblestone.png',
  'minecraft:andesite':         'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/andesite.png',
  'minecraft:diorite':          'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/diorite.png',
  'minecraft:granite':          'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/granite.png',
  'minecraft:oak_planks':       'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/oak_planks.png',
  'minecraft:oak_log':          'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/oak_log_top.png',
  'minecraft:glass':            'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/glass.png',
  'minecraft:obsidian':         'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/obsidian.png',
  'minecraft:crafting_table':   'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/crafting_table_front.png',
  'minecraft:furnace':          'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/furnace_front.png',
  'minecraft:chest':            'https://assets.mcasset.cloud/latest/assets/minecraft/textures/entity/chest/normal.png',
  'minecraft:anvil':            'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/anvil_top.png',
  'minecraft:hopper':           'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/hopper_outside.png',
  'minecraft:piston':           'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/piston_top.png',
  'minecraft:sticky_piston':    'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/piston_top_sticky.png',
  'minecraft:observer':         'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/observer_front.png',
  'minecraft:dispenser':        'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/dispenser_front.png',
  'minecraft:dropper':          'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/dropper_front.png',
  'minecraft:redstone_repeater':'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/repeater.png',
  'minecraft:netherite_block':  'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/netherite_block.png',
  'minecraft:diamond_block':    'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/diamond_block.png',
  'minecraft:gold_block':       'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/gold_block.png',
  'minecraft:iron_block':       'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/iron_block.png',
  'minecraft:copper_block':     'https://assets.mcasset.cloud/latest/assets/minecraft/textures/block/copper_block.png',

  // ─── Mekanism (raw.githubusercontent.com) ───
  'mekanism:osmium_ingot':    'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/ingot_osmium.png',
  'mekanism:tin_ingot':       'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/ingot_tin.png',
  'mekanism:lead_ingot':      'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/ingot_lead.png',
  'mekanism:uranium_ingot':   'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/ingot_uranium.png',
  'mekanism:bronze_ingot':    'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/ingot_bronze.png',
  'mekanism:steel_ingot':     'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/ingot_steel.png',
  'mekanism:osmium_ore':      'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/raw_osmium.png',
  'mekanism:tin_ore':         'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/raw_tin.png',
  'mekanism:lead_ore':        'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/raw_lead.png',
  'mekanism:uranium_ore':     'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/raw_uranium.png',
  'mekanism:fluorite_ore':    'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/fluorite_gem.png',
  'mekanism:control_circuit_basic':    'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/basic_control_circuit.png',
  'mekanism:control_circuit_advanced': 'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/advanced_control_circuit.png',
  'mekanism:control_circuit_elite':    'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/elite_control_circuit.png',
  'mekanism:control_circuit_ultimate': 'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/ultimate_control_circuit.png',
  'mekanism:alloy_atomic':     'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/alloy_atomic.png',
  'mekanism:alloy_infused':    'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/alloy_infused.png',
  'mekanism:alloy_reinforced': 'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/alloy_reinforced.png',
  'mekanism:enriched_diamond': 'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/enriched_diamond.png',
  'mekanism:enriched_gold':    'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/enriched_gold.png',
  'mekanism:enriched_iron':    'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/enriched_iron.png',
  'mekanism:enriched_osmium':  'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/enriched_refined_obsidian.png',
  'mekanism:enriched_redstone':'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/enriched_redstone.png',
  'mekanism:enriched_tin':     'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/enriched_tin.png',
  'mekanism:substrate':        'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/substrate.png',
  'mekanism:hdpe_rod':         'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/hdpe_rod.png',
  'mekanism:hdpe_sheet':       'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/hdpe_sheet.png',
  'mekanism:bio_fuel':         'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/item/bio_fuel.png',

  // Mekanism energy cubes → block textures (closest match)
  'mekanism:basic_energy_cube':    'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/block/basic_induction_cell.png',
  'mekanism:advanced_energy_cube': 'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/block/advanced_induction_cell.png',
  'mekanism:elite_energy_cube':    'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/block/elite_induction_cell.png',
  'mekanism:ultimate_energy_cube': 'https://raw.githubusercontent.com/mekanism/Mekanism/1.21.x/src/main/resources/assets/mekanism/textures/block/ultimate_induction_cell.png',

  // ─── Create (raw.githubusercontent.com) ───
  'create:andesite_alloy':     'https://raw.githubusercontent.com/Creators-of-Create/Create/mc1.20.1/dev/src/main/resources/assets/create/textures/item/andesite_alloy.png',
  'create:brass_ingot':        'https://raw.githubusercontent.com/Creators-of-Create/Create/mc1.20.1/dev/src/main/resources/assets/create/textures/item/brass_ingot.png',
  'create:zinc_ingot':         'https://raw.githubusercontent.com/Creators-of-Create/Create/mc1.20.1/dev/src/main/resources/assets/create/textures/item/zinc_ingot.png',
  'create:iron_sheet':         'https://raw.githubusercontent.com/Creators-of-Create/Create/mc1.20.1/dev/src/main/resources/assets/create/textures/item/iron_sheet.png',
  'create:copper_sheet':       'https://raw.githubusercontent.com/Creators-of-Create/Create/mc1.20.1/dev/src/main/resources/assets/create/textures/item/copper_sheet.png',
  'create:brass_sheet':        'https://raw.githubusercontent.com/Creators-of-Create/Create/mc1.20.1/dev/src/main/resources/assets/create/textures/item/brass_sheet.png',
  'create:precision_mechanism':'https://raw.githubusercontent.com/Creators-of-Create/Create/mc1.20.1/dev/src/main/resources/assets/create/textures/item/precision_mechanism.png',

  // Create → block textures (these items are blocks)
  'create:cogwheel':           'https://raw.githubusercontent.com/Creators-of-Create/Create/mc1.20.1/dev/src/main/resources/assets/create/textures/block/cogwheel.png',
  'create:large_cogwheel':     'https://raw.githubusercontent.com/Creators-of-Create/Create/mc1.20.1/dev/src/main/resources/assets/create/textures/block/large_cogwheel.png',
  'create:shaft':              'https://raw.githubusercontent.com/Creators-of-Create/Create/mc1.20.1/dev/src/main/resources/assets/create/textures/block/gantry_shaft.png',
  'create:gearbox':            'https://raw.githubusercontent.com/Creators-of-Create/Create/mc1.20.1/dev/src/main/resources/assets/create/textures/block/gearbox.png',
  'create:mechanical_piston':  'https://raw.githubusercontent.com/Creators-of-Create/Create/mc1.20.1/dev/src/main/resources/assets/create/textures/block/piston_bottom.png',
  'create:mechanical_bearing': 'https://raw.githubusercontent.com/Creators-of-Create/Create/mc1.20.1/dev/src/main/resources/assets/create/textures/block/mechanical_bearing_side.png',
  'create:water_wheel':        'https://raw.githubusercontent.com/Creators-of-Create/Create/mc1.20.1/dev/src/main/resources/assets/create/textures/block/waterwheel_metal.png',
  'create:windmill_bearing':   'https://raw.githubusercontent.com/Creators-of-Create/Create/mc1.20.1/dev/src/main/resources/assets/create/textures/block/windmill_bearing_side.png',
  'create:belt_connector':     'https://raw.githubusercontent.com/Creators-of-Create/Create/mc1.20.1/dev/src/main/resources/assets/create/textures/block/belt.png',

  // ─── Thermal Foundation (raw.githubusercontent.com) ───
  'thermal:tin_ingot':         'https://raw.githubusercontent.com/CoFH/ThermalFoundation/1.20.x/src/main/resources/assets/thermal/textures/item/tin_ingot.png',
  'thermal:lead_ingot':        'https://raw.githubusercontent.com/CoFH/ThermalFoundation/1.20.x/src/main/resources/assets/thermal/textures/item/lead_ingot.png',
  'thermal:silver_ingot':      'https://raw.githubusercontent.com/CoFH/ThermalFoundation/1.20.x/src/main/resources/assets/thermal/textures/item/silver_ingot.png',
  'thermal:nickel_ingot':      'https://raw.githubusercontent.com/CoFH/ThermalFoundation/1.20.x/src/main/resources/assets/thermal/textures/item/nickel_ingot.png',
  'thermal:bronze_ingot':      'https://raw.githubusercontent.com/CoFH/ThermalFoundation/1.20.x/src/main/resources/assets/thermal/textures/item/bronze_ingot.png',
  'thermal:constantan_ingot':  'https://raw.githubusercontent.com/CoFH/ThermalFoundation/1.20.x/src/main/resources/assets/thermal/textures/item/constantan_ingot.png',
  'thermal:electrum_ingot':    'https://raw.githubusercontent.com/CoFH/ThermalFoundation/1.20.x/src/main/resources/assets/thermal/textures/item/electrum_ingot.png',
  'thermal:invar_ingot':       'https://raw.githubusercontent.com/CoFH/ThermalFoundation/1.20.x/src/main/resources/assets/thermal/textures/item/invar_ingot.png',
  'thermal:steel_ingot':       'https://raw.githubusercontent.com/CoFH/ThermalFoundation/1.20.x/src/main/resources/assets/thermal/textures/item/invar_ingot.png', // fallback: closest match
  'thermal:signalum_ingot':    'https://raw.githubusercontent.com/CoFH/ThermalFoundation/1.20.x/src/main/resources/assets/thermal/textures/item/electrum_ingot.png', // fallback: looks similar
  'thermal:lumium_ingot':      'https://raw.githubusercontent.com/CoFH/ThermalFoundation/1.20.x/src/main/resources/assets/thermal/textures/item/electrum_ingot.png', // fallback
  'thermal:enderium_ingot':    'https://raw.githubusercontent.com/CoFH/ThermalFoundation/1.20.x/src/main/resources/assets/thermal/textures/item/electrum_ingot.png', // fallback
  'thermal:redstone_servo':    'https://raw.githubusercontent.com/CoFH/ThermalFoundation/1.20.x/src/main/resources/assets/thermal/textures/item/electrum_gear.png', // fallback
  'thermal:rf_coil':           'https://raw.githubusercontent.com/CoFH/ThermalFoundation/1.20.x/src/main/resources/assets/thermal/textures/item/electrum_nugget.png', // fallback
};

async function download(url, outputPath) {
  mkdirSync(dirname(outputPath), { recursive: true });
  try {
    const resp = await fetch(url);
    if (!resp.ok) {
      console.log(`  ❌ ${url.split('/').pop()} (${resp.status})`);
      return false;
    }
    const buf = Buffer.from(await resp.arrayBuffer());
    writeFileSync(outputPath, buf);
    const kb = (buf.length / 1024).toFixed(1);
    const shortPath = outputPath.replace(TEXTURE_DIR, 'textures');
    console.log(`  ✅ ${shortPath} (${kb} KB)`);
    return true;
  } catch (e) {
    console.log(`  ❌ ${url.split('/').pop()} (${e.message})`);
    return false;
  }
}

async function main() {
  console.log('=== Downloading Minecraft Item Textures v2 ===\n');
  
  const entries = Object.entries(TEXTURES);
  let success = 0;
  let fail = 0;
  
  for (const [itemId, url] of entries) {
    const [ns, name] = itemId.split(':');
    const parts = url.split('/');
    // Determine subfolder based on URL path
    let subdir = ns;
    if (url.includes('/block/')) subdir = ns + '/block';
    else if (url.includes('/entity/')) subdir = ns + '/entity';
    
    const filename = parts[parts.length - 1];
    const outputPath = join(TEXTURE_DIR, subdir, filename);
    
    console.log(`\n${itemId}:`);
    await download(url, outputPath);
  }
  
  console.log(`\n=== Done ===`);
}

main().catch(console.error);
