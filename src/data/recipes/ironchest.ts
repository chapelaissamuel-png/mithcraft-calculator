// Iron Chests recipes
import { r, res, ing } from './helpers';
import type { Recipe } from '../../types';

const R: Recipe[] = [
  r('ironchest:iron_chest', 'crafting', 'ironchest', [res('ironchest:iron_chest')],
    [ing('minecraft:iron_ingot')], { pattern: ['AAA', 'A A', 'AAA'], key: { A: ing('minecraft:iron_ingot') } }),
  r('ironchest:copper_chest', 'crafting', 'ironchest', [res('ironchest:copper_chest')],
    [ing('minecraft:copper_ingot'), ing('minecraft:chest')], { pattern: ['AAA', 'ABA', 'AAA'], key: { A: ing('minecraft:copper_ingot'), B: ing('minecraft:chest') } }),
  r('ironchest:gold_chest', 'crafting', 'ironchest', [res('ironchest:gold_chest')],
    [ing('minecraft:gold_ingot'), ing('ironchest:iron_chest')], { pattern: ['AAA', 'ABA', 'AAA'], key: { A: ing('minecraft:gold_ingot'), B: ing('ironchest:iron_chest') } }),
  r('ironchest:silver_chest', 'crafting', 'ironchest', [res('ironchest:silver_chest')],
    [ing('minecraft:iron_ingot'), ing('ironchest:copper_chest')], { pattern: ['AAA', 'ABA', 'AAA'], key: { A: ing('minecraft:iron_ingot'), B: ing('ironchest:copper_chest') } }),
  r('ironchest:diamond_chest', 'crafting', 'ironchest', [res('ironchest:diamond_chest')],
    [ing('minecraft:diamond'), ing('ironchest:gold_chest')], { pattern: ['AAA', 'ABA', 'AAA'], key: { A: ing('minecraft:diamond'), B: ing('ironchest:gold_chest') } }),
  r('ironchest:crystal_chest', 'crafting', 'ironchest', [res('ironchest:crystal_chest')],
    [ing('minecraft:glass'), ing('minecraft:obsidian'), ing('ironchest:diamond_chest')], { pattern: ['ABA', 'BCB', 'ABA'], key: { A: ing('minecraft:glass'), B: ing('minecraft:obsidian'), C: ing('ironchest:diamond_chest') } }),
  r('ironchest:obsidian_chest', 'crafting', 'ironchest', [res('ironchest:obsidian_chest')],
    [ing('minecraft:obsidian'), ing('ironchest:diamond_chest')], { pattern: ['AAA', 'ABA', 'AAA'], key: { A: ing('minecraft:obsidian'), B: ing('ironchest:diamond_chest') } }),
];

export default R;