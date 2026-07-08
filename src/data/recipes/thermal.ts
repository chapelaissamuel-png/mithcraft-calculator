import { r, ing, ingTag } from './helpers';
import type { Recipe } from '../../types';

const TH: Recipe[] = [
  // ─── ALLOYS (Induction Smelter) ──────────────────
  r('thermal:bronze_ingot', 'thermal:induction_smelter', 'thermal',
    [{ item: 'thermal:bronze_ingot', count: 4 }],
    [ing('minecraft:copper_ingot', 3), ing('thermal:tin_ingot')], { energy: 400 }),
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

  // ─── SPECIAL ALLOYS ──────────────────────────────
  r('thermal:enderium_ingot', 'thermal:induction_smelter', 'thermal',
    [{ item: 'thermal:enderium_ingot', count: 2 }],
    [ing('thermal:silver_ingot', 2), ing('minecraft:ender_pearl', 2)], { energy: 1000 }),
  r('thermal:lumium_ingot', 'thermal:induction_smelter', 'thermal',
    [{ item: 'thermal:lumium_ingot', count: 2 }],
    [ing('thermal:tin_ingot', 2), ing('minecraft:glowstone_dust', 2)], { energy: 800 }),
  r('thermal:signalum_ingot', 'thermal:induction_smelter', 'thermal',
    [{ item: 'thermal:signalum_ingot', count: 2 }],
    [ing('minecraft:copper_ingot', 2), ing('minecraft:redstone', 4)], { energy: 800 }),

  // ─── COMPONENTS ──────────────────────────────────
  r('thermal:redstone_servo', 'crafting', 'thermal',
    [{ item: 'thermal:redstone_servo' }],
    [], { pattern: [' R ', 'RIR', ' R '], key: { R: ing('minecraft:redstone'), I: ing('minecraft:iron_ingot') } }),
  r('thermal:rf_coil', 'crafting', 'thermal',
    [{ item: 'thermal:rf_coil' }],
    [], { pattern: ['IRI', 'I I', 'IRI'], key: { I: ing('minecraft:iron_ingot'), R: ing('minecraft:redstone') } }),

  // ─── MACHINES ────────────────────────────────────
  r('thermal:machine_frame', 'crafting', 'thermal',
    [{ item: 'thermal:machine_frame' }],
    [], { pattern: ['INI', 'NSN', 'INI'], key: { I: ing('minecraft:iron_ingot'), N: ing('thermal:nickel_ingot'), S: ing('thermal:redstone_servo') } }),
  r('thermal:pulverizer', 'crafting', 'thermal',
    [{ item: 'thermal:pulverizer' }],
    [ing('thermal:machine_frame'), ing('thermal:rf_coil'), ing('minecraft:flint', 2), ing('minecraft:iron_ingot', 2)]),
  r('thermal:induction_smelter', 'crafting', 'thermal',
    [{ item: 'thermal:induction_smelter' }],
    [ing('thermal:machine_frame'), ing('thermal:rf_coil'), ing('minecraft:redstone', 4)]),
  r('thermal:fluid_encapsulator', 'crafting', 'thermal',
    [{ item: 'thermal:fluid_encapsulator' }],
    [ing('thermal:machine_frame'), ing('thermal:rf_coil'), ing('minecraft:glass', 4)]),
  r('thermal:centrifuge', 'crafting', 'thermal',
    [{ item: 'thermal:centrifuge' }],
    [ing('thermal:machine_frame'), ing('thermal:rf_coil'), ing('minecraft:bucket', 2)]),
  r('thermal:refinery', 'crafting', 'thermal',
    [{ item: 'thermal:refinery' }],
    [ing('thermal:machine_frame'), ing('thermal:rf_coil'), ing('minecraft:iron_block')]),
  r('thermal:crystallizer', 'crafting', 'thermal',
    [{ item: 'thermal:crystallizer' }],
    [ing('thermal:machine_frame'), ing('thermal:rf_coil'), ing('minecraft:diamond', 2)]),
  r('thermal:press', 'crafting', 'thermal',
    [{ item: 'thermal:press' }],
    [ing('thermal:machine_frame'), ing('thermal:rf_coil'), ing('minecraft:piston'), ing('minecraft:iron_block')]),

  // ─── AUGMENTS ────────────────────────────────────
  r('thermal:upgrade_augment_1', 'crafting', 'thermal',
    [{ item: 'thermal:upgrade_augment_1' }],
    [], { pattern: [' G ', 'GSG', ' G '], key: { G: ing('minecraft:gold_ingot'), S: ing('thermal:redstone_servo') } }),
  r('thermal:upgrade_augment_2', 'crafting', 'thermal',
    [{ item: 'thermal:upgrade_augment_2' }],
    [], { pattern: [' G ', 'GAG', ' G '], key: { G: ing('minecraft:gold_ingot'), A: ing('thermal:upgrade_augment_1') } }),
  r('thermal:upgrade_augment_3', 'crafting', 'thermal',
    [{ item: 'thermal:upgrade_augment_3' }],
    [], { pattern: [' D ', 'DAD', ' D '], key: { D: ing('minecraft:diamond'), A: ing('thermal:upgrade_augment_2') } }),
];

export default TH;
