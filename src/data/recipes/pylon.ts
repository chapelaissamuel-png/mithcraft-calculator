// Pylon recipes
import { r, res, ing } from './helpers';
import type { Recipe } from '../../types';

const R: Recipe[] = [
  r('pylon:pylon_rod', 'crafting', 'pylon', [res('pylon:pylon_rod')],
    [ing('minecraft:iron_ingot'), ing('minecraft:redstone'), ing('minecraft:stone')],
    { pattern: [' A', ' B', ' C '], key: { A: ing('minecraft:iron_ingot'), B: ing('minecraft:redstone'), C: ing('minecraft:stone') } }),
  r('pylon:pylon_structure', 'crafting', 'pylon', [res('pylon:pylon_structure')],
    [ing('minecraft:stone', 8), ing('pylon:pylon_rod')],
    { pattern: ['AAA', 'ABA', 'AAA'], key: { A: ing('minecraft:stone'), B: ing('pylon:pylon_rod') } }),
  r('pylon:pylon', 'crafting', 'pylon', [res('pylon:pylon')],
    [ing('pylon:pylon_structure', 8), ing('minecraft:diamond')],
    { pattern: ['AAA', 'ABA', 'AAA'], key: { A: ing('pylon:pylon_structure'), B: ing('minecraft:diamond') } }),
  r('pylon:pylon_energy', 'crafting', 'pylon', [res('pylon:pylon_energy')],
    [ing('pylon:pylon_structure', 4), ing('minecraft:redstone_block', 4), ing('minecraft:diamond')],
    { pattern: ['ABA', 'BCB', 'ABA'], key: { A: ing('pylon:pylon_structure'), B: ing('minecraft:redstone_block'), C: ing('minecraft:diamond') } }),
  r('pylon:pylon_control', 'crafting', 'pylon', [res('pylon:pylon_control')],
    [ing('pylon:pylon'), ing('minecraft:redstone'), ing('minecraft:ender_pearl')]),
];

export default R;
