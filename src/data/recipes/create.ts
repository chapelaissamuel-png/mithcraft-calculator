import { r, ing } from './helpers';
import type { Recipe } from '../../types';

const CR: Recipe[] = [
  // ─── BASE MATERIALS ──────────────────────────────
  r('create:andesite_alloy', 'crafting', 'create',
    [{ item: 'create:andesite_alloy', count: 2 }],
    [ing('minecraft:andesite'), ing('minecraft:iron_nugget')]),
  r('create:copper_sheet', 'create:pressing', 'create',
    [{ item: 'create:copper_sheet' }], [ing('minecraft:copper_ingot')], { energy: 200 }),
  r('create:iron_sheet', 'create:pressing', 'create',
    [{ item: 'create:iron_sheet' }], [ing('minecraft:iron_ingot')], { energy: 200 }),
  r('create:brass_ingot', 'create:mixing', 'create',
    [{ item: 'create:brass_ingot', count: 2 }],
    [ing('minecraft:copper_ingot'), ing('create:zinc_ingot')], { energy: 400, time: 100 }),
  r('create:brass_sheet', 'create:pressing', 'create',
    [{ item: 'create:brass_sheet' }], [ing('create:brass_ingot')], { energy: 200 }),

  // ─── KINETIC COMPONENTS ──────────────────────────
  r('create:cogwheel', 'crafting', 'create',
    [{ item: 'create:cogwheel' }],
    [], { pattern: [' S ', 'SAS', ' S '], key: { S: ing('minecraft:stick'), A: ing('create:andesite_alloy') } }),
  r('create:large_cogwheel', 'crafting', 'create',
    [{ item: 'create:large_cogwheel' }],
    [], { pattern: [' S ', 'SCS', ' S '], key: { S: ing('minecraft:stick'), C: ing('create:cogwheel') } }),
  r('create:shaft', 'crafting', 'create',
    [{ item: 'create:shaft' }],
    [], { pattern: ['A', 'A'], key: { A: ing('create:andesite_alloy') } }),
  r('create:gearbox', 'crafting', 'create',
    [{ item: 'create:gearbox' }],
    [], { pattern: ['SCS', 'C C', 'SCS'], key: { S: ing('create:shaft'), C: ing('create:cogwheel') } }),

  // ─── BELTS & TRANSPORT ───────────────────────────
  r('create:belt_connector', 'crafting', 'create',
    [{ item: 'create:belt_connector' }],
    [], { pattern: ['SSS', 'SSS'], key: { S: ing('minecraft:slime_ball') } }),
  r('create:mechanical_piston', 'crafting', 'create',
    [{ item: 'create:mechanical_piston' }],
    [ing('create:piston'), ing('create:shaft'), ing('create:andesite_alloy')]),
  r('create:piston_extension_pole', 'crafting', 'create',
    [{ item: 'create:piston_extension_pole' }],
    [], { pattern: ['A', 'A', 'A'], key: { A: ing('create:andesite_alloy') } }),
  r('create:mechanical_bearing', 'crafting', 'create',
    [{ item: 'create:mechanical_bearing' }],
    [], { pattern: ['SCS', 'SAS', 'S S'], key: { S: ing('create:shaft'), C: ing('create:cogwheel'), A: ing('create:andesite_alloy') } }),
  r('create:windmill_bearing', 'crafting', 'create',
    [{ item: 'create:windmill_bearing' }],
    [], { pattern: ['SAS', 'S S', 'SAS'], key: { S: ing('create:shaft'), A: ing('create:andesite_alloy') } }),

  // ─── WATER / POWER ───────────────────────────────
  r('create:water_wheel', 'crafting', 'create',
    [{ item: 'create:water_wheel' }],
    [], { pattern: ['SSS', 'SCS', 'SSS'], key: { S: ing('minecraft:oak_planks'), C: ing('create:shaft') } }),
  r('create:large_water_wheel', 'crafting', 'create',
    [{ item: 'create:large_water_wheel' }],
    [], { pattern: ['SPS', 'PCP', 'SPS'], key: { S: ing('create:shaft'), P: ing('minecraft:oak_planks'), C: ing('create:water_wheel') } }),

  // ─── MECHANICAL PRECISION ────────────────────────
  r('create:precision_mechanism', 'crafting', 'create',
    [{ item: 'create:precision_mechanism' }],
    [], { pattern: [' C ', 'CSC', ' C '], key: { C: ing('create:cogwheel'), S: ing('create:iron_sheet') } }),

  // ─── DEPOT / FUNNELS / CHUTES ────────────────────
  r('create:depot', 'crafting', 'create',
    [{ item: 'create:depot' }],
    [], { pattern: ['SWS', 'SCS'], key: { S: ing('create:andesite_alloy'), W: ing('minecraft:oak_planks'), C: ing('create:cogwheel') } }),
  r('create:chute', 'crafting', 'create',
    [{ item: 'create:chute', count: 4 }],
    [], { pattern: ['IBI', 'I I', 'IBI'], key: { I: ing('create:iron_sheet'), B: ing('create:brass_sheet') } }),
  r('create:smart_chute', 'crafting', 'create',
    [{ item: 'create:smart_chute' }],
    [ing('create:chute', 2), ing('create:precision_mechanism')]),
  r('create:andesite_funnel', 'crafting', 'create',
    [{ item: 'create:andesite_funnel', count: 2 }],
    [], { pattern: ['A', 'C'], key: { A: ing('create:andesite_alloy'), C: ing('create:andesite_casing') } }),
  r('create:brass_funnel', 'crafting', 'create',
    [{ item: 'create:brass_funnel', count: 2 }],
    [], { pattern: ['B', 'C'], key: { B: ing('create:brass_ingot'), C: ing('create:brass_casing') } }),
  r('create:andesite_tunnel', 'crafting', 'create',
    [{ item: 'create:andesite_tunnel', count: 2 }],
    [], { pattern: ['A', 'F'], key: { A: ing('create:andesite_alloy'), F: ing('create:andesite_casing') } }),
  r('create:brass_tunnel', 'crafting', 'create',
    [{ item: 'create:brass_tunnel', count: 2 }],
    [], { pattern: ['B', 'F'], key: { B: ing('create:brass_ingot'), F: ing('create:brass_casing') } }),

  // ─── CASINGS ─────────────────────────────────────
  r('create:andesite_casing', 'crafting', 'create',
    [{ item: 'create:andesite_casing' }],
    [], { pattern: ['AA', 'AA'], key: { A: ing('create:andesite_alloy') } }),
  r('create:brass_casing', 'crafting', 'create',
    [{ item: 'create:brass_casing' }],
    [], { pattern: ['BB', 'BB'], key: { B: ing('create:brass_ingot') } }),
  r('create:copper_casing', 'crafting', 'create',
    [{ item: 'create:copper_casing' }],
    [], { pattern: ['CC', 'CC'], key: { C: ing('minecraft:copper_ingot') } }),

  // ─── MISC ────────────────────────────────────────
  r('create:crushing_wheel', 'crafting', 'create',
    [{ item: 'create:crushing_wheel' }],
    [], { pattern: ['AAA', 'S S', 'AAA'], key: { A: ing('create:andesite_alloy'), S: ing('create:shaft') } }),
  r('create:mechanical_press', 'crafting', 'create',
    [{ item: 'create:mechanical_press' }],
    [], { pattern: [' A ', 'SAS', 'SAS'], key: { A: ing('create:andesite_alloy'), S: ing('create:iron_sheet') } }),
  r('create:mechanical_mixer', 'crafting', 'create',
    [{ item: 'create:mechanical_mixer' }],
    [], { pattern: [' A ', 'SAS', 'S S'], key: { A: ing('create:andesite_alloy'), S: ing('create:iron_sheet') } }),
  r('create:mechanical_saw', 'crafting', 'create',
    [{ item: 'create:mechanical_saw' }],
    [], { pattern: ['IAI', 'S S'], key: { I: ing('minecraft:iron_ingot'), A: ing('create:andesite_alloy'), S: ing('create:shaft') } }),
];

export default CR;
