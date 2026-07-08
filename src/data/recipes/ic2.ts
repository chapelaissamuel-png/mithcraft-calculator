import { r, ing, ingTag } from './helpers';
import type { Recipe } from '../../types';

const IC: Recipe[] = [
  // ─── PROCESSING ──────────────────────────────────
  r('ic2:refined_iron_ingot', 'ic2:compressor', 'ic2',
    [{ item: 'ic2:refined_iron_ingot' }],
    [ing('minecraft:iron_ingot')], { energy: 400 }),
  r('ic2:carbon_plate', 'ic2:compressor', 'ic2',
    [{ item: 'ic2:carbon_plate' }],
    [ingTag('forge:coal', 4)], { energy: 800 }),

  // ─── CABLES ──────────────────────────────────────
  r('ic2:insulated_copper_cable', 'crafting', 'ic2',
    [{ item: 'ic2:insulated_copper_cable', count: 6 }],
    [ing('minecraft:copper_ingot', 3), ing('ic2:rubber', 6)]),
  r('ic2:glass_fibre_cable', 'crafting', 'ic2',
    [{ item: 'ic2:glass_fibre_cable', count: 8 }],
    [ing('minecraft:glass', 2), ing('minecraft:diamond')]),

  // ─── CIRCUITS ────────────────────────────────────
  r('ic2:electronic_circuit', 'crafting', 'ic2',
    [{ item: 'ic2:electronic_circuit' }],
    [ing('ic2:insulated_copper_cable'), ing('ic2:refined_iron_ingot'), ing('minecraft:redstone')]),
  r('ic2:advanced_circuit', 'crafting', 'ic2',
    [{ item: 'ic2:advanced_circuit' }],
    [ing('ic2:electronic_circuit', 2), ing('minecraft:redstone'), ing('ic2:carbon_plate'), ing('minecraft:lapis_lazuli', 4)]),

  // ─── MACHINE BLOCKS ──────────────────────────────
  r('ic2:machine_block_basic', 'crafting', 'ic2',
    [{ item: 'ic2:machine_block_basic' }],
    [], { pattern: ['III', 'ISI', 'III'], key: { I: ing('ic2:refined_iron_ingot'), S: ing('ic2:electronic_circuit') } }),
  r('ic2:machine_block_advanced', 'crafting', 'ic2',
    [{ item: 'ic2:machine_block_advanced' }],
    [], { pattern: ['III', 'IAI', 'III'], key: { I: ing('ic2:refined_iron_ingot'), A: ing('ic2:advanced_circuit') } }),

  // ─── POWER GENERATION ────────────────────────────
  r('ic2:generator', 'crafting', 'ic2',
    [{ item: 'ic2:generator' }],
    [], { pattern: [' B ', 'BIB', 'IBI'], key: { B: ing('ic2:machine_block_basic'), I: ing('minecraft:iron_ingot') } }),
  r('ic2:solar_panel', 'crafting', 'ic2',
    [{ item: 'ic2:solar_panel' }],
    [], { pattern: ['GGG', 'CAC', 'IGI'], key: { G: ing('minecraft:glass'), C: ing('ic2:electronic_circuit'), A: ing('ic2:generator'), I: ing('minecraft:iron_ingot') } }),

  // ─── ENERGY STORAGE ──────────────────────────────
  r('ic2:cesu', 'crafting', 'ic2',
    [{ item: 'ic2:cesu' }],
    [], { pattern: ['ECE', 'CSC', 'ECE'], key: { E: ing('ic2:electronic_circuit'), C: ing('ic2:insulated_copper_cable'), S: ing('ic2:storage_battery') } }),
  r('ic2:mf_unit', 'crafting', 'ic2',
    [{ item: 'ic2:mf_unit' }],
    [], { pattern: ['EAE', 'ABA', 'EAE'], key: { E: ing('ic2:electronic_circuit'), A: ing('ic2:advanced_circuit'), B: ing('ic2:machine_block_basic') } }),
  r('ic2:mfs_unit', 'crafting', 'ic2',
    [{ item: 'ic2:mfs_unit' }],
    [], { pattern: ['EAE', 'ABA', 'EAE'], key: { E: ing('ic2:advanced_circuit'), A: ing('ic2:mf_unit'), B: ing('ic2:machine_block_advanced') } }),
];

export default IC;
