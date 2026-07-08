import { r, ing, ingTag } from './helpers';
import type { Recipe } from '../../types';

const AE: Recipe[] = [
  // ─── BASE MATERIALS ──────────────────────────────
  r('ae2:silicon', 'smelting', 'ae2',
    [{ item: 'ae2:silicon' }], [ingTag('forge:sand', 1)]),
  r('ae2:certus_quartz_dust', 'mekanism:crushing', 'ae2',
    [{ item: 'ae2:certus_quartz_dust', count: 2 }],
    [ing('ae2:certus_quartz_crystal')], { energy: 200 }),
  r('ae2:fluix_crystal', 'crafting', 'ae2',
    [{ item: 'ae2:fluix_crystal', count: 2 }],
    [ing('ae2:charged_certus_quartz_crystal'), ing('minecraft:redstone'), ing('ae2:certus_quartz_dust')]),
  r('ae2:fluix_dust', 'mekanism:crushing', 'ae2',
    [{ item: 'ae2:fluix_dust', count: 4 }],
    [ing('ae2:fluix_crystal')], { energy: 400 }),
  r('ae2:charged_certus_quartz_crystal', 'ae2:charger', 'ae2',
    [{ item: 'ae2:charged_certus_quartz_crystal' }],
    [ing('ae2:certus_quartz_crystal')], { energy: 800 }),

  // ─── INSCRIBER PRINTS ────────────────────────────
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

  // ─── PROCESSORS ──────────────────────────────────
  r('ae2:calculation_processor', 'crafting', 'ae2',
    [{ item: 'ae2:calculation_processor' }],
    [ing('ae2:printed_calculation_processor'), ing('ae2:printed_silicon'), ing('minecraft:redstone')]),
  r('ae2:engineering_processor', 'crafting', 'ae2',
    [{ item: 'ae2:engineering_processor' }],
    [ing('ae2:printed_engineering_processor'), ing('ae2:printed_silicon'), ing('minecraft:redstone')]),
  r('ae2:logic_processor', 'crafting', 'ae2',
    [{ item: 'ae2:logic_processor' }],
    [ing('ae2:printed_logic_processor'), ing('ae2:printed_silicon'), ing('minecraft:redstone')]),

  // ─── STORAGE COMPONENTS ──────────────────────────
  r('ae2:cell_component_1k', 'crafting', 'ae2',
    [{ item: 'ae2:cell_component_1k' }],
    [], { pattern: ['CCC', 'CRC', 'CCC'], key: { C: ing('ae2:certus_quartz_crystal'), R: ing('ae2:calculation_processor') } }),
  r('ae2:cell_component_4k', 'crafting', 'ae2',
    [{ item: 'ae2:cell_component_4k' }],
    [], { pattern: ['CCC', 'CRC', 'CCC'], key: { C: ing('ae2:cell_component_1k'), R: ing('ae2:calculation_processor') } }),
  r('ae2:cell_component_16k', 'crafting', 'ae2',
    [{ item: 'ae2:cell_component_16k' }],
    [], { pattern: ['CCC', 'CRC', 'CCC'], key: { C: ing('ae2:cell_component_4k'), R: ing('ae2:calculation_processor') } }),
  r('ae2:cell_component_64k', 'crafting', 'ae2',
    [{ item: 'ae2:cell_component_64k' }],
    [], { pattern: ['CCC', 'CRC', 'CCC'], key: { C: ing('ae2:cell_component_16k'), R: ing('ae2:calculation_processor') } }),
  r('ae2:cell_component_256k', 'crafting', 'ae2',
    [{ item: 'ae2:cell_component_256k' }],
    [], { pattern: ['CCC', 'CRC', 'CCC'], key: { C: ing('ae2:cell_component_64k'), R: ing('ae2:calculation_processor') } }),

  // ─── CELL HOUSINGS ───────────────────────────────
  r('ae2:item_cell_housing', 'crafting', 'ae2',
    [{ item: 'ae2:item_cell_housing' }],
    [], { pattern: ['EEE', 'ECE', 'EEE'], key: { E: ing('ae2:fluix_crystal'), C: ing('ae2:charged_certus_quartz_crystal') } }),
  r('ae2:fluid_cell_housing', 'crafting', 'ae2',
    [{ item: 'ae2:fluid_cell_housing' }],
    [], { pattern: ['EGE', 'ECE', 'EGE'], key: { E: ing('ae2:fluix_crystal'), G: ing('minecraft:glass'), C: ing('ae2:charged_certus_quartz_crystal') } }),
];

export default AE;
