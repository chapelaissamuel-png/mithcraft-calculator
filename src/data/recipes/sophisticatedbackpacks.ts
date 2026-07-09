// Sophisticated Backpacks recipes
import { r, res, ing } from './helpers';
import type { Recipe } from '../../types';

const R: Recipe[] = [
  r('sophisticatedbackpacks:backpack', 'crafting', 'sophisticatedbackpacks', [res('sophisticatedbackpacks:backpack')],
    [ing('minecraft:leather', 4), ing('minecraft:string', 2), ing('minecraft:chest')],
    { pattern: ['ABA', 'ACA', 'DDD'], key: { A: ing('minecraft:leather'), B: ing('minecraft:string'), C: ing('minecraft:chest'), D: ing('minecraft:string') } }),
  r('sophisticatedbackpacks:iron_backpack', 'crafting', 'sophisticatedbackpacks', [res('sophisticatedbackpacks:iron_backpack')],
    [ing('sophisticatedbackpacks:backpack'), ing('minecraft:iron_ingot', 7)],
    { pattern: ['AAA', 'ABA', 'AAA'], key: { A: ing('minecraft:iron_ingot'), B: ing('sophisticatedbackpacks:backpack') } }),
  r('sophisticatedbackpacks:gold_backpack', 'crafting', 'sophisticatedbackpacks', [res('sophisticatedbackpacks:gold_backpack')],
    [ing('sophisticatedbackpacks:iron_backpack'), ing('minecraft:gold_ingot', 7)],
    { pattern: ['AAA', 'ABA', 'AAA'], key: { A: ing('minecraft:gold_ingot'), B: ing('sophisticatedbackpacks:iron_backpack') } }),
  r('sophisticatedbackpacks:diamond_backpack', 'crafting', 'sophisticatedbackpacks', [res('sophisticatedbackpacks:diamond_backpack')],
    [ing('sophisticatedbackpacks:gold_backpack'), ing('minecraft:diamond', 7)],
    { pattern: ['AAA', 'ABA', 'AAA'], key: { A: ing('minecraft:diamond'), B: ing('sophisticatedbackpacks:gold_backpack') } }),
  r('sophisticatedbackpacks:netherite_backpack', 'crafting', 'sophisticatedbackpacks', [res('sophisticatedbackpacks:netherite_backpack')],
    [ing('sophisticatedbackpacks:diamond_backpack'), ing('minecraft:netherite_ingot')],
    { pattern: ['AAA', 'ABA', 'AAA'], key: { A: ing('minecraft:netherite_ingot'), B: ing('sophisticatedbackpacks:diamond_backpack') } }),
  r('sophisticatedbackpacks:upgrade_base', 'crafting', 'sophisticatedbackpacks', [res('sophisticatedbackpacks:upgrade_base')],
    [ing('minecraft:leather', 4), ing('minecraft:gold_nugget', 4), ing('minecraft:redstone')],
    { pattern: ['ABA', 'BCB', 'ABA'], key: { A: ing('minecraft:leather'), B: ing('minecraft:gold_nugget'), C: ing('minecraft:redstone') } }),
  r('sophisticatedbackpacks:pickup_upgrade', 'crafting', 'sophisticatedbackpacks', [res('sophisticatedbackpacks:pickup_upgrade')],
    [ing('sophisticatedbackpacks:upgrade_base'), ing('minecraft:hopper')],
    { pattern: [' A ', 'ABA', ' A '], key: { A: ing('minecraft:hopper'), B: ing('sophisticatedbackpacks:upgrade_base') } }),
  r('sophisticatedbackpacks:filter_upgrade', 'crafting', 'sophisticatedbackpacks', [res('sophisticatedbackpacks:filter_upgrade')],
    [ing('sophisticatedbackpacks:upgrade_base'), ing('minecraft:composter')],
    { pattern: [' A ', 'ABA', ' A '], key: { A: ing('minecraft:composter'), B: ing('sophisticatedbackpacks:upgrade_base') } }),
  r('sophisticatedbackpacks:magnet_upgrade', 'crafting', 'sophisticatedbackpacks', [res('sophisticatedbackpacks:magnet_upgrade')],
    [ing('sophisticatedbackpacks:upgrade_base'), ing('minecraft:iron_ingot', 4), ing('minecraft:redstone')],
    { pattern: [' A ', 'ABA', ' A '], key: { A: ing('minecraft:iron_ingot'), B: ing('sophisticatedbackpacks:upgrade_base') } }),
  r('sophisticatedbackpacks:compacting_upgrade', 'crafting', 'sophisticatedbackpacks', [res('sophisticatedbackpacks:compacting_upgrade')],
    [ing('sophisticatedbackpacks:upgrade_base'), ing('minecraft:piston')],
    { pattern: [' A ', 'ABA', ' A '], key: { A: ing('minecraft:piston'), B: ing('sophisticatedbackpacks:upgrade_base') } }),
  r('sophisticatedbackpacks:void_upgrade', 'crafting', 'sophisticatedbackpacks', [res('sophisticatedbackpacks:void_upgrade')],
    [ing('sophisticatedbackpacks:upgrade_base'), ing('minecraft:lava_bucket')],
    { pattern: [' A ', 'ABA', ' A '], key: { A: ing('minecraft:lava_bucket'), B: ing('sophisticatedbackpacks:upgrade_base') } }),
];

export default R;
