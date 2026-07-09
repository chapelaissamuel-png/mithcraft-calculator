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
import IRONCHEST from './recipes/ironchest';
import PYLON from './recipes/pylon';
import PREFAB from './recipes/prefab';
import STORAGENET from './recipes/storagenetwork';
import SOPHSTORAGE from './recipes/sophisticatedstorage';
import SOPHBACKPACKS from './recipes/sophisticatedbackpacks';
import ROOTS from './recipes/rootsclassic';
import IRONSPELLS from './recipes/irons_spellbooks';
import FARMERS from './recipes/farmersdelight';
import MYSTICAL from './recipes/mysticalagriculture';

export function getAllRecipes(): Recipe[] {
  return [
    ...V,           // Vanilla Minecraft
    ...MEK,         // Mekanism
    ...MEK_PROC,    // Mekanism processing
    ...CR,          // Create
    ...TH,          // Thermal Series
    ...TH_PROC,     // Thermal processing
    ...AE,          // Applied Energistics 2
    ...IC,          // IndustrialCraft 2
    ...IRONCHEST,   // Iron Chests
    ...PYLON,       // Pylon
    ...PREFAB,      // Prefab
    ...STORAGENET,  // Simple Storage Network
    ...SOPHSTORAGE, // Sophisticated Storage
    ...SOPHBACKPACKS, // Sophisticated Backpacks
    ...ROOTS,       // Roots Classic
    ...IRONSPELLS,  // Iron's Spells 'n Spellbooks
    ...FARMERS,     // Farmer's Delight
    ...MYSTICAL,    // Mystical Agriculture
  ];
}
