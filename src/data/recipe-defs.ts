// ─── COMPREHENSIVE RECIPE DATABASE ───────────────────
// Compact format to minimize file size while covering:
// Vanilla + Mekanism + Thermal + Create + AE2 + IC2

import type { Recipe, Ingredient, RecipeCategory } from '../types';

// Helper to build ingredient quickly
const ing = (item: string, count = 1): Ingredient => ({ item, count });
const ingTag = (tag: string, count = 1): Ingredient => ({ item: '', count, tag });

// Recipe builder
const r = (
  id: string, type: RecipeCategory, mod: string,
  results: { item: string; count?: number }[],
  ingredients: Ingredient[],
  opts?: { pattern?: string[]; key?: Record<string, Ingredient>; energy?: number; time?: number },
): Recipe => ({
  id, type, mod,
  ingredients,
  results: results.map(r => ({ item: r.item, count: r.count ?? 1 })),
  ...(opts?.pattern ? { pattern: opts.pattern, key: opts.key } : {}),
  ...(opts?.energy ? { energy: opts.energy } : {}),
  ...(opts?.time ? { processingTime: opts.time } : {}),
});

// ─── VANILLA RECIPES ─────────────────────────────────

const V: Recipe[] = [

  // === IRON TOOLS ===
  r('minecraft:iron_sword', 'crafting', 'minecraft', [{ item: 'minecraft:iron_sword' }], [], {
    pattern: ['I', 'I', 'S'], key: { I: ing('minecraft:iron_ingot'), S: ing('minecraft:stick') },
  }),
  r('minecraft:iron_pickaxe', 'crafting', 'minecraft', [{ item: 'minecraft:iron_pickaxe' }], [], {
    pattern: ['III', ' S ', ' S '], key: { I: ing('minecraft:iron_ingot'), S: ing('minecraft:stick') },
  }),
  r('minecraft:iron_axe', 'crafting', 'minecraft', [{ item: 'minecraft:iron_axe' }], [], {
    pattern: ['II', 'IS', ' S'], key: { I: ing('minecraft:iron_ingot'), S: ing('minecraft:stick') },
  }),
  r('minecraft:iron_shovel', 'crafting', 'minecraft', [{ item: 'minecraft:iron_shovel' }], [], {
    pattern: ['I', 'S', 'S'], key: { I: ing('minecraft:iron_ingot'), S: ing('minecraft:stick') },
  }),
  r('minecraft:iron_hoe', 'crafting', 'minecraft', [{ item: 'minecraft:iron_hoe' }], [], {
    pattern: ['II', ' S', ' S'], key: { I: ing('minecraft:iron_ingot'), S: ing('minecraft:stick') },
  }),

  // === IRON ARMOR ===
  r('minecraft:iron_helmet', 'crafting', 'minecraft', [{ item: 'minecraft:iron_helmet' }], [], {
    pattern: ['III', 'I I'], key: { I: ing('minecraft:iron_ingot') },
  }),
  r('minecraft:iron_chestplate', 'crafting', 'minecraft', [{ item: 'minecraft:iron_chestplate' }], [], {
    pattern: ['I I', 'III', 'III'], key: { I: ing('minecraft:iron_ingot') },
  }),
  r('minecraft:iron_leggings', 'crafting', 'minecraft', [{ item: 'minecraft:iron_leggings' }], [], {
    pattern: ['III', 'I I', 'I I'], key: { I: ing('minecraft:iron_ingot') },
  }),
  r('minecraft:iron_boots', 'crafting', 'minecraft', [{ item: 'minecraft:iron_boots' }], [], {
    pattern: ['I I', 'I I'], key: { I: ing('minecraft:iron_ingot') },
  }),

  // === BLOCK CONVERSIONS ===
  r('minecraft:iron_block', 'crafting', 'minecraft', [{ item: 'minecraft:iron_block' }], [ing('minecraft:iron_ingot', 9)], { pattern: ['III', 'III', 'III'], key: { I: ing('minecraft:iron_ingot') } }),
  r('minecraft:iron_ingot', 'crafting', 'minecraft', [{ item: 'minecraft:iron_ingot', count: 9 }], [ing('minecraft:iron_block')], { pattern: ['B'], key: { B: ing('minecraft:iron_block') } }),
  r('minecraft:gold_block', 'crafting', 'minecraft', [{ item: 'minecraft:gold_block' }], [ing('minecraft:gold_ingot', 9)], { pattern: ['III', 'III', 'III'], key: { I: ing('minecraft:gold_ingot') } }),
  r('minecraft:gold_ingot', 'crafting', 'minecraft', [{ item: 'minecraft:gold_ingot', count: 9 }], [ing('minecraft:gold_block')], { pattern: ['B'], key: { B: ing('minecraft:gold_block') } }),
  r('minecraft:diamond_block', 'crafting', 'minecraft', [{ item: 'minecraft:diamond_block' }], [ing('minecraft:diamond', 9)], { pattern: ['III', 'III', 'III'], key: { I: ing('minecraft:diamond') } }),
  r('minecraft:diamond', 'crafting', 'minecraft', [{ item: 'minecraft:diamond', count: 9 }], [ing('minecraft:diamond_block')], { pattern: ['B'], key: { B: ing('minecraft:diamond_block') } }),
  r('minecraft:copper_block', 'crafting', 'minecraft', [{ item: 'minecraft:copper_block' }], [ing('minecraft:copper_ingot', 9)], { pattern: ['III', 'III', 'III'], key: { I: ing('minecraft:copper_ingot') } }),
  r('minecraft:copper_ingot', 'crafting', 'minecraft', [{ item: 'minecraft:copper_ingot', count: 9 }], [ing('minecraft:copper_block')], { pattern: ['B'], key: { B: ing('minecraft:copper_block') } }),
  r('minecraft:netherite_block', 'crafting', 'minecraft', [{ item: 'minecraft:netherite_block' }], [ing('minecraft:netherite_ingot', 9)], { pattern: ['III', 'III', 'III'], key: { I: ing('minecraft:netherite_ingot') } }),

  // === NUGGETS ===
  r('minecraft:iron_nugget', 'crafting', 'minecraft', [{ item: 'minecraft:iron_nugget', count: 9 }], [ing('minecraft:iron_ingot')], { pattern: ['I'], key: { I: ing('minecraft:iron_ingot') } }),
  r('minecraft:iron_ingot', 'crafting', 'minecraft', [{ item: 'minecraft:iron_ingot' }], [ing('minecraft:iron_nugget', 9)]),
  r('minecraft:gold_nugget', 'crafting', 'minecraft', [{ item: 'minecraft:gold_nugget', count: 9 }], [ing('minecraft:gold_ingot')], { pattern: ['I'], key: { I: ing('minecraft:gold_ingot') } }),
  r('minecraft:gold_ingot', 'crafting', 'minecraft', [{ item: 'minecraft:gold_ingot' }], [ing('minecraft:gold_nugget', 9)]),

  // === SMELTING ===
  r('minecraft:iron_ingot_furnace', 'smelting', 'minecraft', [{ item: 'minecraft:iron_ingot' }], [ing('minecraft:iron_ore')]),
  r('minecraft:gold_ingot_furnace', 'smelting', 'minecraft', [{ item: 'minecraft:gold_ingot' }], [ing('minecraft:gold_ore')]),
  r('minecraft:copper_ingot_furnace', 'smelting', 'minecraft', [{ item: 'minecraft:copper_ingot' }], [ing('minecraft:copper_ore')]),
  r('minecraft:iron_ingot_blasting', 'blasting', 'minecraft', [{ item: 'minecraft:iron_ingot' }], [ing('minecraft:iron_ore')]),
  r('minecraft:gold_ingot_blasting', 'blasting', 'minecraft', [{ item: 'minecraft:gold_ingot' }], [ing('minecraft:gold_ore')]),

  // === COMPONENTS ===
  r('minecraft:stick', 'crafting', 'minecraft', [{ item: 'minecraft:stick', count: 4 }], [ing('minecraft:oak_planks', 2)], { pattern: ['P', 'P'], key: { P: ing('minecraft:oak_planks') } }),
  r('minecraft:chest', 'crafting', 'minecraft', [{ item: 'minecraft:chest' }], [], { pattern: ['PPP', 'P P', 'PPP'], key: { P: ing('minecraft:oak_planks') } }),
  r('minecraft:furnace', 'crafting', 'minecraft', [{ item: 'minecraft:furnace' }], [], { pattern: ['CCC', 'C C', 'CCC'], key: { C: ing('minecraft:cobblestone') } }),
  r('minecraft:crafting_table', 'crafting', 'minecraft', [{ item: 'minecraft:crafting_table' }], [], { pattern: ['PP', 'PP'], key: { P: ing('minecraft:oak_planks') } }),
  r('minecraft:anvil', 'crafting', 'minecraft', [{ item: 'minecraft:anvil' }], [], { pattern: ['BBB', ' I ', 'III'], key: { B: ing('minecraft:iron_block'), I: ing('minecraft:iron_ingot') } }),
  r('minecraft:piston', 'crafting', 'minecraft', [{ item: 'minecraft:piston' }], [], { pattern: ['PPP', 'CIC', 'CSC'], key: { P: ing('minecraft:oak_planks'), C: ing('minecraft:cobblestone'), I: ing('minecraft:iron_ingot'), S: ing('minecraft:redstone') } }),
  r('minecraft:sticky_piston', 'crafting', 'minecraft', [{ item: 'minecraft:sticky_piston' }], [ing('minecraft:slime_ball'), ing('minecraft:piston')]),
  r('minecraft:hopper', 'crafting', 'minecraft', [{ item: 'minecraft:hopper' }], [], { pattern: ['I I', 'ICI', ' I '], key: { I: ing('minecraft:iron_ingot'), C: ing('minecraft:chest') } }),
  r('minecraft:dropper', 'crafting', 'minecraft', [{ item: 'minecraft:dropper' }], [], { pattern: ['CCC', 'C C', 'CRC'], key: { C: ing('minecraft:cobblestone'), R: ing('minecraft:redstone') } }),
  r('minecraft:dispenser', 'crafting', 'minecraft', [{ item: 'minecraft:dispenser' }], [], { pattern: ['CCC', 'CBC', 'CRC'], key: { C: ing('minecraft:cobblestone'), B: ing('minecraft:bow'), R: ing('minecraft:redstone') } }),
  r('minecraft:observer', 'crafting', 'minecraft', [{ item: 'minecraft:observer' }], [], { pattern: ['CCC', 'RQR', 'CCC'], key: { C: ing('minecraft:cobblestone'), R: ing('minecraft:redstone'), Q: ing('minecraft:quartz') } }),
  r('minecraft:redstone_repeater', 'crafting', 'minecraft', [{ item: 'minecraft:redstone_repeater' }], [], { pattern: ['R R', 'SSS', 'TTT'], key: { R: ing('minecraft:redstone_torch'), S: ing('minecraft:stone'), T: ing('minecraft:redstone') } }),
  r('minecraft:comparator', 'crafting', 'minecraft', [{ item: 'minecraft:comparator' }], [], { pattern: [' T ', 'TQT', 'SSS'], key: { T: ing('minecraft:redstone_torch'), Q: ing('minecraft:quartz'), S: ing('minecraft:stone') } }),
  r('minecraft:book', 'crafting', 'minecraft', [{ item: 'minecraft:book' }], [ing('minecraft:paper', 3), ing('minecraft:leather')]),
  r('minecraft:paper', 'crafting', 'minecraft', [{ item: 'minecraft:paper', count: 3 }], [], { pattern: ['SSS'], key: { S: ing('minecraft:sugar_cane') } }),
  r('minecraft:bucket', 'crafting', 'minecraft', [{ item: 'minecraft:bucket' }], [], { pattern: ['I I', ' I '], key: { I: ing('minecraft:iron_ingot') } }),
  r('minecraft:glass', 'smelting', 'minecraft', [{ item: 'minecraft:glass' }], [ing('minecraft:sand')]),

  // === BASE MATERIALS ===
  r('minecraft:oak_planks', 'crafting', 'minecraft', [{ item: 'minecraft:oak_planks', count: 4 }], [], { pattern: ['L'], key: { L: ing('minecraft:oak_log') } }),
  r('minecraft:iron_ingot_nuggets', 'crafting', 'minecraft', [{ item: 'minecraft:iron_ingot' }], [ing('minecraft:iron_nugget', 9)]),
  r('minecraft:gold_ingot_nuggets', 'crafting', 'minecraft', [{ item: 'minecraft:gold_ingot' }], [ing('minecraft:gold_nugget', 9)]),

  // === SLIME / SPECIAL ===
  r('minecraft:slime_ball', 'crafting', 'minecraft', [{ item: 'minecraft:slime_ball', count: 4 }], [ing('minecraft:slime_block')]),
];

// ─── MEKANISM RECIPES ───────────────────────────────

const MEK: Recipe[] = [

  // === PROCESSING (Ore → Ingot) ===
  r('mekanism:osmium_ingot_smelting', 'smelting', 'mekanism', [{ item: 'mekanism:osmium_ingot' }], [ing('mekanism:osmium_ore')]),
  r('mekanism:tin_ingot_smelting', 'smelting', 'mekanism', [{ item: 'mekanism:tin_ingot' }], [ing('mekanism:tin_ore')]),
  r('mekanism:lead_ingot_smelting', 'smelting', 'mekanism', [{ item: 'mekanism:lead_ingot' }], [ing('mekanism:lead_ore')]),

  // === ALLOYS ===
  r('mekanism:steel_ingot', 'mekanism:metallurgic_infusing', 'mekanism',
    [{ item: 'mekanism:steel_ingot' }],
    [ing('minecraft:iron_ingot'), ingTag('forge:coal', 1)],
    { energy: 400 },
  ),
  r('mekanism:bronze_ingot', 'mekanism:metallurgic_infusing', 'mekanism',
    [{ item: 'mekanism:bronze_ingot' }],
    [ing('mekanism:copper_ingot', 3), ing('mekanism:tin_ingot')],
    { energy: 400 },
  ),
  r('mekanism:enriched_iron', 'mekanism:enriching', 'mekanism',
    [{ item: 'mekanism:enriched_iron' }],
    [ing('minecraft:iron_ingot', 3)],
    { energy: 200 },
  ),
  r('mekanism:enriched_gold', 'mekanism:enriching', 'mekanism',
    [{ item: 'mekanism:enriched_gold' }],
    [ing('minecraft:gold_ingot', 3)],
    { energy: 200 },
  ),
  r('mekanism:enriched_tin', 'mekanism:enriching', 'mekanism',
    [{ item: 'mekanism:enriched_tin' }],
    [ing('mekanism:tin_ingot', 3)],
    { energy: 200 },
  ),
  r('mekanism:enriched_osmium', 'mekanism:enriching', 'mekanism',
    [{ item: 'mekanism:enriched_osmium' }],
    [ing('mekanism:osmium_ingot', 3)],
    { energy: 200 },
  ),
  r('mekanism:enriched_diamond', 'mekanism:enriching', 'mekanism',
    [{ item: 'mekanism:enriched_diamond' }],
    [ing('minecraft:diamond', 3)],
    { energy: 400 },
  ),
  r('mekanism:enriched_redstone', 'mekanism:enriching', 'mekanism',
    [{ item: 'mekanism:enriched_redstone' }],
    [ing('minecraft:redstone', 8)],
    { energy: 200 },
  ),

  // === ALLOYS ===
  r('mekanism:alloy_infused', 'mekanism:metallurgic_infusing', 'mekanism',
    [{ item: 'mekanism:alloy_infused' }],
    [ing('minecraft:iron_ingot'), ing('mekanism:enriched_redstone')],
    { energy: 400 },
  ),
  r('mekanism:alloy_reinforced', 'mekanism:metallurgic_infusing', 'mekanism',
    [{ item: 'mekanism:alloy_reinforced' }],
    [ing('mekanism:alloy_infused'), ing('mekanism:enriched_diamond')],
    { energy: 600 },
  ),
  r('mekanism:alloy_atomic', 'mekanism:metallurgic_infusing', 'mekanism',
    [{ item: 'mekanism:alloy_atomic' }],
    [ing('mekanism:alloy_reinforced'), ing('mekanism:enriched_refined_obsidian')],
    { energy: 1000 },
  ),

  // === CONTROL CIRCUITS ===
  r('mekanism:control_circuit_basic', 'crafting', 'mekanism',
    [{ item: 'mekanism:control_circuit_basic' }],
    [], {
    pattern: ['OSO', 'R R', 'OSO'],
    key: { O: ing('mekanism:osmium_ingot'), S: ing('minecraft:stick'), R: ing('minecraft:redstone') },
  }),
  r('mekanism:control_circuit_advanced', 'crafting', 'mekanism',
    [{ item: 'mekanism:control_circuit_advanced' }],
    [], {
    pattern: ['GEG', 'R R', 'GEG'],
    key: { G: ing('minecraft:gold_ingot'), E: ing('mekanism:enriched_diamond'), R: ing('mekanism:control_circuit_basic') },
  }),
  r('mekanism:control_circuit_elite', 'crafting', 'mekanism',
    [{ item: 'mekanism:control_circuit_elite' }],
    [], {
    pattern: ['DAD', 'R R', 'DAD'],
    key: { D: ing('minecraft:diamond'), A: ing('mekanism:alloy_reinforced'), R: ing('mekanism:control_circuit_advanced') },
  }),
  r('mekanism:control_circuit_ultimate', 'crafting', 'mekanism',
    [{ item: 'mekanism:control_circuit_ultimate' }],
    [], {
    pattern: ['PAP', 'R R', 'PAP'],
    key: { P: ing('mekanism:polonium_pellet'), A: ing('mekanism:alloy_atomic'), R: ing('mekanism:control_circuit_elite') },
  }),

  // === ENERGY CUBES ===
  r('mekanism:basic_energy_cube', 'crafting', 'mekanism',
    [{ item: 'mekanism:basic_energy_cube' }],
    [], {
    pattern: ['OSO', 'S S', 'OSO'],
    key: { O: ing('mekanism:osmium_ingot'), S: ing('mekanism:steel_ingot') },
  }),
  r('mekanism:advanced_energy_cube', 'crafting', 'mekanism',
    [{ item: 'mekanism:advanced_energy_cube' }],
    [], {
    pattern: ['GAG', 'A A', 'GAG'],
    key: { G: ing('minecraft:gold_ingot'), A: ing('mekanism:alloy_infused') },
  }),

  // === HDPE ===
  r('mekanism:hdpe_sheet', 'mekanism:pigment_extracting', 'mekanism',
    [{ item: 'mekanism:hdpe_sheet', count: 3 }],
    [ing('mekanism:substrate')],
    { energy: 200 },
  ),
  r('mekanism:substrate', 'mekanism:crushing', 'mekanism',
    [{ item: 'mekanism:substrate' }],
    [ing('mekanism:bio_fuel', 4)],
    { energy: 800 },
  ),
  r('mekanism:bio_fuel', 'mekanism:crushing', 'mekanism',
    [{ item: 'mekanism:bio_fuel', count: 5 }],
    [ingTag('forge:seeds', 1)],
    { energy: 100 },
  ),
];

// ─── AE2 RECIPES ────────────────────────────────────

const AE: Recipe[] = [
  r('ae2:silicon', 'smelting', 'ae2', [{ item: 'ae2:silicon' }], [ingTag('forge:sand', 1)]),
  r('ae2:fluix_crystal', 'crafting', 'ae2', [{ item: 'ae2:fluix_crystal', count: 2 }],
    [ing('ae2:charged_certus_quartz_crystal'), ing('minecraft:redstone'), ing('ae2:certus_quartz_dust')]),
  r('ae2:fluix_dust', 'mekanism:crushing', 'ae2', [{ item: 'ae2:fluix_dust', count: 4 }],
    [ing('ae2:fluix_crystal')], { energy: 400 }),
  r('ae2:certus_quartz_dust', 'mekanism:crushing', 'ae2', [{ item: 'ae2:certus_quartz_dust', count: 2 }],
    [ing('ae2:certus_quartz_crystal')], { energy: 200 }),
  r('ae2:charged_certus_quartz_crystal', 'ae2:charger', 'ae2',
    [{ item: 'ae2:charged_certus_quartz_crystal' }],
    [ing('ae2:certus_quartz_crystal')], { energy: 800 }),
  r('ae2:printed_silicon', 'ae2:inscriber', 'ae2',
    [{ item: 'ae2:printed_silicon' }],
    [ing('ae2:silicon')], { pattern: ['P'], key: { P: ing('ae2:silicon') } }),
  r('ae2:printed_calculation_processor', 'ae2:inscriber', 'ae2',
    [{ item: 'ae2:printed_calculation_processor' }],
    [ing('ae2:certus_quartz_crystal')], { pattern: ['P'], key: { P: ing('ae2:certus_quartz_crystal') } }),
  r('ae2:printed_engineering_processor', 'ae2:inscriber', 'ae2',
    [{ item: 'ae2:printed_engineering_processor' }],
    [ing('minecraft:diamond')], { pattern: ['P'], key: { P: ing('minecraft:diamond') } }),
  r('ae2:printed_logic_processor', 'ae2:inscriber', 'ae2',
    [{ item: 'ae2:printed_logic_processor' }],
    [ing('minecraft:gold_ingot')], { pattern: ['P'], key: { P: ing('minecraft:gold_ingot') } }),

  // === PROCESSORS ===
  r('ae2:calculation_processor', 'crafting', 'ae2', [{ item: 'ae2:calculation_processor' }],
    [ing('ae2:printed_calculation_processor'), ing('ae2:printed_silicon'), ing('ae2:redstone')]),
  r('ae2:engineering_processor', 'crafting', 'ae2', [{ item: 'ae2:engineering_processor' }],
    [ing('ae2:printed_engineering_processor'), ing('ae2:printed_silicon'), ing('minecraft:redstone')]),
  r('ae2:logic_processor', 'crafting', 'ae2', [{ item: 'ae2:logic_processor' }],
    [ing('ae2:printed_logic_processor'), ing('ae2:printed_silicon'), ing('minecraft:redstone')]),

  // === STORAGE COMPONENTS ===
  r('ae2:cell_component_1k', 'crafting', 'ae2', [{ item: 'ae2:cell_component_1k' }],
    [], {
    pattern: ['CCC', 'CRC', 'CCC'],
    key: { C: ing('ae2:certus_quartz_crystal'), R: ing('ae2:calculation_processor') },
  }),
  r('ae2:cell_component_4k', 'crafting', 'ae2', [{ item: 'ae2:cell_component_4k' }],
    [], {
    pattern: ['CCC', 'CRC', 'CCC'],
    key: { C: ing('ae2:cell_component_1k'), R: ing('ae2:calculation_processor') },
  }),
  r('ae2:cell_component_16k', 'crafting', 'ae2', [{ item: 'ae2:cell_component_16k' }],
    [], {
    pattern: ['CCC', 'CRC', 'CCC'],
    key: { C: ing('ae2:cell_component_4k'), R: ing('ae2:calculation_processor') },
  }),
  r('ae2:cell_component_64k', 'crafting', 'ae2', [{ item: 'ae2:cell_component_64k' }],
    [], {
    pattern: ['CCC', 'CRC', 'CCC'],
    key: { C: ing('ae2:cell_component_16k'), R: ing('ae2:calculation_processor') },
  }),
  r('ae2:cell_component_256k', 'crafting', 'ae2', [{ item: 'ae2:cell_component_256k' }],
    [], {
    pattern: ['CCC', 'CRC', 'CCC'],
    key: { C: ing('ae2:cell_component_64k'), R: ing('ae2:calculation_processor') },
  }),
];

// ─── CREATE RECIPES ─────────────────────────────────

const CR: Recipe[] = [
  r('create:andesite_alloy', 'crafting', 'create', [{ item: 'create:andesite_alloy', count: 2 }],
    [ing('minecraft:andesite'), ing('minecraft:iron_nugget')]),
  r('create:copper_sheet', 'create:pressing', 'create', [{ item: 'create:copper_sheet' }],
    [ing('minecraft:copper_ingot')], { energy: 200 }),
  r('create:iron_sheet', 'create:pressing', 'create', [{ item: 'create:iron_sheet' }],
    [ing('minecraft:iron_ingot')], { energy: 200 }),
  r('create:brass_ingot', 'create:mixing', 'create', [{ item: 'create:brass_ingot', count: 2 }],
    [ing('minecraft:copper_ingot'), ing('create:zinc_ingot')], { energy: 400, time: 100 }),
  r('create:brass_sheet', 'create:pressing', 'create', [{ item: 'create:brass_sheet' }],
    [ing('create:brass_ingot')], { energy: 200 }),
  r('create:cogwheel', 'crafting', 'create', [{ item: 'create:cogwheel' }],
    [], { pattern: [' S ', 'SAS', ' S '], key: { S: ing('minecraft:stick'), A: ing('create:andesite_alloy') } }),
  r('create:large_cogwheel', 'crafting', 'create', [{ item: 'create:large_cogwheel' }],
    [], { pattern: [' S ', 'SCS', ' S '], key: { S: ing('minecraft:stick'), C: ing('create:cogwheel') } }),
  r('create:shaft', 'crafting', 'create', [{ item: 'create:shaft' }],
    [], { pattern: ['A', 'A'], key: { A: ing('create:andesite_alloy') } }),
  r('create:belt_connector', 'crafting', 'create', [{ item: 'create:belt_connector' }],
    [], { pattern: ['SSS', 'SSS'], key: { S: ing('minecraft:slime_ball') } }),
  r('create:gearbox', 'crafting', 'create', [{ item: 'create:gearbox' }],
    [], { pattern: ['SCS', 'C C', 'SCS'], key: { S: ing('create:shaft'), C: ing('create:cogwheel') } }),
  r('create:mechanical_piston', 'crafting', 'create', [{ item: 'create:mechanical_piston' }],
    [ing('create:piston'), ing('create:shaft'), ing('create:andesite_alloy')]),
  r('create:mechanical_bearing', 'crafting', 'create', [{ item: 'create:mechanical_bearing' }],
    [], { pattern: ['SCS', 'SAS', 'S S'], key: { S: ing('create:shaft'), C: ing('create:cogwheel'), A: ing('create:andesite_alloy') } }),
  r('create:water_wheel', 'crafting', 'create', [{ item: 'create:water_wheel' }],
    [], { pattern: ['SSS', 'SCS', 'SSS'], key: { S: ing('minecraft:oak_planks'), C: ing('create:shaft') } }),
  r('create:windmill_bearing', 'crafting', 'create', [{ item: 'create:windmill_bearing' }],
    [], { pattern: ['SAS', 'S S', 'SAS'], key: { S: ing('create:shaft'), A: ing('create:andesite_alloy') } }),
  r('create:precision_mechanism', 'crafting', 'create', [{ item: 'create:precision_mechanism' }],
    [], { pattern: [' C ', 'CSC', ' C '], key: { C: ing('create:cogwheel'), S: ing('create:iron_sheet') } }),
];

// ─── IC2 RECIPES ────────────────────────────────────

const IC: Recipe[] = [
  r('ic2:refined_iron_ingot', 'ic2:compressor', 'ic2', [{ item: 'ic2:refined_iron_ingot' }],
    [ing('minecraft:iron_ingot')], { energy: 400 }),
  r('ic2:carbon_plate', 'ic2:compressor', 'ic2', [{ item: 'ic2:carbon_plate' }],
    [ingTag('forge:coal', 4)], { energy: 800 }),
  r('ic2:electronic_circuit', 'crafting', 'ic2', [{ item: 'ic2:electronic_circuit' }],
    [ing('ic2:insulated_copper_cable'), ing('ic2:refined_iron_ingot'), ing('minecraft:redstone')]),
  r('ic2:advanced_circuit', 'crafting', 'ic2', [{ item: 'ic2:advanced_circuit' }],
    [ing('ic2:electronic_circuit', 2), ing('minecraft:redstone'), ing('ic2:carbon_plate'), ing('minecraft:lapis_lazuli', 4)]),
  r('ic2:machine_block_basic', 'crafting', 'ic2', [{ item: 'ic2:machine_block_basic' }],
    [], { pattern: ['III', 'ISI', 'III'], key: { I: ing('ic2:refined_iron_ingot'), S: ing('ic2:electronic_circuit') } }),
  r('ic2:machine_block_advanced', 'crafting', 'ic2', [{ item: 'ic2:machine_block_advanced' }],
    [], { pattern: ['III', 'IAI', 'III'], key: { I: ing('ic2:refined_iron_ingot'), A: ing('ic2:advanced_circuit') } }),
  r('ic2:generator', 'crafting', 'ic2', [{ item: 'ic2:generator' }],
    [], { pattern: [' B ', 'BIB', 'IBI'], key: { B: ing('ic2:machine_block_basic'), I: ing('minecraft:iron_ingot') } }),
  r('ic2:solar_panel', 'crafting', 'ic2', [{ item: 'ic2:solar_panel' }],
    [], { pattern: ['GGG', 'CAC', 'IGI'], key: { G: ing('minecraft:glass'), C: ing('ic2:electronic_circuit'), A: ing('ic2:generator'), I: ing('minecraft:iron_ingot') } }),
  r('ic2:insulated_copper_cable', 'crafting', 'ic2', [{ item: 'ic2:insulated_copper_cable', count: 6 }],
    [ing('minecraft:copper_ingot', 3), ing('minecraft:rubber', 6)]),
  r('ic2:glass_fibre_cable', 'crafting', 'ic2', [{ item: 'ic2:glass_fibre_cable', count: 8 }],
    [ing('minecraft:glass', 2), ing('minecraft:diamond')]),
];

// ─── THERMAL RECIPES ────────────────────────────────

const TH: Recipe[] = [
  r('thermal:redstone_servo', 'crafting', 'thermal', [{ item: 'thermal:redstone_servo' }],
    [], { pattern: [' R ', 'RIR', ' R '], key: { R: ing('minecraft:redstone'), I: ing('minecraft:iron_ingot') } }),
  r('thermal:rf_coil', 'crafting', 'thermal', [{ item: 'thermal:rf_coil' }],
    [], { pattern: ['IRI', 'I I', 'IRI'], key: { I: ing('minecraft:iron_ingot'), R: ing('minecraft:redstone') } }),
  r('thermal:bronze_ingot', 'thermal:induction_smelter', 'thermal',
    [{ item: 'thermal:bronze_ingot', count: 4 }],
    [ing('thermal:copper_ingot', 3), ing('thermal:tin_ingot')], { energy: 400 }),
  r('thermal:electrum_ingot', 'thermal:induction_smelter', 'thermal',
    [{ item: 'thermal:electrum_ingot', count: 2 }],
    [ing('minecraft:gold_ingot'), ing('thermal:silver_ingot')], { energy: 400 }),
  r('thermal:invar_ingot', 'thermal:induction_smelter', 'thermal',
    [{ item: 'thermal:invar_ingot', count: 3 }],
    [ing('minecraft:iron_ingot', 2), ing('thermal:nickel_ingot')], { energy: 400 }),
  r('thermal:constantan_ingot', 'thermal:induction_smelter', 'thermal',
    [{ item: 'thermal:constantan_ingot', count: 2 }],
    [ing('minecraft:copper_ingot'), ing('thermal:nickel_ingot')], { energy: 400 }),
  r('thermal:steel_ingot', 'thermal:induction_smelter', 'thermal',
    [{ item: 'thermal:steel_ingot' }],
    [ing('minecraft:iron_ingot'), ingTag('forge:coal', 1)], { energy: 600 }),
  r('thermal:enderium_ingot', 'thermal:induction_smelter', 'thermal',
    [{ item: 'thermal:enderium_ingot', count: 2 }],
    [ing('thermal:silver_ingot', 2), ing('minecraft:ender_pearl', 2)], { energy: 1000 }),
];

// Export the factory
export function getAllRecipes(): Recipe[] {
  return [...V, ...MEK, ...AE, ...CR, ...IC, ...TH];
}
