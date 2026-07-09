// Simple Storage Network recipes
import { r, res, ing } from './helpers';
import type { Recipe } from '../../types';

const R: Recipe[] = [
  r('storagenetwork:network_cable', 'crafting', 'storagenetwork', [res('storagenetwork:network_cable', 8)],
    [ing('minecraft:glass', 2), ing('minecraft:redstone', 2), ing('minecraft:iron_ingot', 2)],
    { pattern: ['ABA', 'ACA', 'ABA'], key: { A: ing('minecraft:glass'), B: ing('minecraft:redstone'), C: ing('minecraft:iron_ingot') } }),
  r('storagenetwork:storage_request', 'crafting', 'storagenetwork', [res('storagenetwork:storage_request')],
    [ing('minecraft:redstone', 4), ing('minecraft:chest', 4), ing('minecraft:diamond')],
    { pattern: ['ABA', 'BCB', 'ABA'], key: { A: ing('minecraft:redstone'), B: ing('minecraft:chest'), C: ing('minecraft:diamond') } }),
  r('storagenetwork:inventory', 'crafting', 'storagenetwork', [res('storagenetwork:inventory')],
    [ing('minecraft:chest', 4), ing('minecraft:iron_ingot', 4), ing('minecraft:redstone')],
    { pattern: ['ABA', 'BCB', 'ABA'], key: { A: ing('minecraft:chest'), B: ing('minecraft:iron_ingot'), C: ing('minecraft:redstone') } }),
  r('storagenetwork:remote', 'crafting', 'storagenetwork', [res('storagenetwork:remote')],
    [ing('minecraft:diamond', 2), ing('minecraft:ender_pearl', 2), ing('storagenetwork:storage_request')],
    { pattern: [' AB', ' CD', '  E'], key: { A: ing('minecraft:diamond'), B: ing('minecraft:diamond'), C: ing('minecraft:ender_pearl'), D: ing('minecraft:ender_pearl'), E: ing('storagenetwork:storage_request') } }),
  r('storagenetwork:collector', 'crafting', 'storagenetwork', [res('storagenetwork:collector')],
    [ing('minecraft:hopper', 4), ing('storagenetwork:network_cable', 4), ing('minecraft:chest')],
    { pattern: ['ABA', 'BCB', 'ABA'], key: { A: ing('minecraft:hopper'), B: ing('storagenetwork:network_cable'), C: ing('minecraft:chest') } }),
  r('storagenetwork:filter', 'crafting', 'storagenetwork', [res('storagenetwork:filter')],
    [ing('minecraft:iron_ingot', 6), ing('minecraft:redstone'), ing('minecraft:glass')],
    { pattern: ['AAA', 'BCD', 'AAA'], key: { A: ing('minecraft:iron_ingot'), B: ing('minecraft:redstone'), C: ing('minecraft:glass'), D: ing('minecraft:redstone') } }),
  r('storagenetwork:upgrade', 'crafting', 'storagenetwork', [res('storagenetwork:upgrade')],
    [ing('minecraft:redstone', 4), ing('minecraft:gold_ingot', 4), ing('minecraft:diamond')],
    { pattern: ['ABA', 'BCB', 'ABA'], key: { A: ing('minecraft:redstone'), B: ing('minecraft:gold_ingot'), C: ing('minecraft:diamond') } }),
];

export default R;
