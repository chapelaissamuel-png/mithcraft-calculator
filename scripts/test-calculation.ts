#!/usr/bin/env node
// Quick test: check that calculateItem works for listed items
import { calculateItem } from '../src/engine/calculator.ts';
import { registry } from '../src/data/recipe-registry.ts';

const testItems = [
  'ae2:16k_me_storage_cell',
  'ae2:1k_me_storage_cell',
  'ae2:controller',
  'ae2:drive',
  'ae2:terminal',
  'pylon:teleport_amulet',
  'pylon:spirit_jar',
  'pylon:soul_shard',
  'farmersdelight:stove',
  'farmersdelight:cooking_pot',
  'mysticalagriculture:crop_blaze',
];

for (const itemId of testItems) {
  try {
    const meta = registry.getItem(itemId);
    const recipes = registry.getRecipesFor(itemId);
    console.log(`${itemId}:`);
    console.log(`  meta: ${meta ? meta.name : 'UNDEFINED'}`);
    console.log(`  recipes: ${recipes.length}`);
    const result = calculateItem(itemId, 1);
    console.log(`  calc: ${result.rawSummary ? Object.keys(result.rawSummary).length + ' raw items' : 'FAILED'}`);
    if (result.rootItem) {
      console.log(`  totalOps: ${result.totalOperations}`);
    }
  } catch (e) {
    console.log(`${itemId}: ERROR - ${e}`);
  }
}
