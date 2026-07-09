// ─── RECIPE DATABASE ──────────────────────────────
// Imports organized by mod pack for clarity and maintainability
// Each file exports its own array of recipes

import type { Recipe } from '../types';
import V from './recipes/vanilla';
import MEK from './recipes/mekanism';
import CR from './recipes/create';
import TH from './recipes/thermal';
import AE from './recipes/ae2';
import IC from './recipes/ic2';
import MEK_PROC from './recipes/mekanism-processing';
import TH_PROC from './recipes/thermal-processing';

export function getAllRecipes(): Recipe[] {
  return [
    ...V,     // Vanilla Minecraft
    ...MEK,   // Mekanism
    ...MEK_PROC, // Mekanism processing
    ...CR,    // Create
    ...TH,    // Thermal Series
    ...TH_PROC, // Thermal processing
    ...AE,    // Applied Energistics 2
    ...IC,    // IndustrialCraft 2
  ];
}
