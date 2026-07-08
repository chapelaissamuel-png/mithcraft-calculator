import type { CalcNode, CalcResult, MachineStep, RecipeCategory } from '../types';
import { registry } from '../data/recipe-registry';

const MACHINE_NAMES: Partial<Record<RecipeCategory, string>> = {
  'crafting': 'Crafting Table',
  'smelting': 'Furnace',
  'blasting': 'Blast Furnace',
  'smoking': 'Smoker',
  'campfire': 'Campfire',
  'smithing': 'Smithing Table',
  'stonecutting': 'Stonecutter',
  'mekanism:crushing': 'Mekanism Crusher',
  'mekanism:enriching': 'Mekanism Enricher',
  'mekanism:combining': 'Mekanism Combiner',
  'mekanism:infusing': 'Mekanism Metallurgic Infuser',
  'mekanism:metallurgic_infusing': 'Mekanism Metallurgic Infuser',
  'mekanism:pigment_extracting': 'Mekanism Pigment Extractor',
  'thermal:pulverizer': 'Thermal Pulverizer',
  'thermal:smelter': 'Thermal Induction Smelter',
  'thermal:induction_smelter': 'Thermal Induction Smelter',
  'thermal:centrifuge': 'Thermal Centrifuge',
  'thermal:crystallizer': 'Thermal Crystallizer',
  'thermal:press': 'Thermal Multi-Servo Press',
  'thermal:refinery': 'Thermal Refinery',
  'create:mixing': 'Create Mixer',
  'create:crushing': 'Create Crushing Wheels',
  'create:pressing': 'Create Mechanical Press',
  'create:cutting': 'Create Mechanical Saw',
  'create:deploying': 'Create Deployer',
  'create:haunting': 'Create Haunting',
  'create:splashing': 'Create Washing',
  'create:compacting': 'Create Mechanical Press',
  'ic2:compressor': 'IC2 Compressor',
  'ic2:extractor': 'IC2 Extractor',
  'ic2:macerator': 'IC2 Macerator',
  'ic2:recycler': 'IC2 Recycler',
  'ae2:inscriber': 'AE2 Inscriber',
  'ae2:charger': 'AE2 Charger',
};

interface CalcOptions {
  maxDepth: number;
  trackMachines: boolean;
}

const DEFAULT_OPTIONS: CalcOptions = {
  maxDepth: 20,
  trackMachines: true,
};

export function calculateItem(
  itemId: string,
  quantity: number,
  options: Partial<CalcOptions> = {},
): CalcResult {
  const opts = { ...DEFAULT_OPTIONS, ...options };
  const machineSteps: MachineStep[] = [];

  function buildNode(id: string, qty: number, depth: number, path: Set<string> = new Set()): CalcNode {
    if (depth > opts.maxDepth || path.has(id)) {
      return { item: id, quantity: qty, recipe: null, children: [], isRaw: true, depth };
    }

    const recipes = registry.getRecipesFor(id);
    const isRaw = recipes.length === 0;

    if (isRaw) {
      return { item: id, quantity: qty, recipe: null, children: [], isRaw: true, depth };
    }

    const recipe = recipes[0];

    // Skip recipes that produce themselves (cycle via block↔ingot)
    if (recipe.ingredients.some(ing => ing.item === id)) {
      return { item: id, quantity: qty, recipe: null, children: [], isRaw: true, depth };
    }

    const perCraft = recipe.results[0]?.count ?? 1;
    const times = Math.ceil(qty / perCraft);
    const actualOutput = times * perCraft;

    const children: CalcNode[] = [];
    const newPath = new Set(path);
    newPath.add(id);

    for (const ing of recipe.ingredients) {
      if (ing.catalyst) continue;
      const neededQty = ing.count * times;
      const itemKey = ing.item || ing.tag || '';
      const child = buildNode(itemKey, neededQty, depth + 1, newPath);
      children.push(child);
    }

    if (opts.trackMachines && recipe.type !== 'crafting') {
      const machineName = MACHINE_NAMES[recipe.type] || recipe.type;
      let step = machineSteps.find(s => s.machine === machineName && s.type === recipe.type);
      if (step) {
        step.times += times;
        step.totalEnergy += (recipe.energy ?? 0) * times;
        step.totalTime += (recipe.processingTime ?? 0) * times;
        for (const ing of recipe.ingredients) {
          if (!ing.catalyst) {
            const key = ing.item || ing.tag || '';
            const existing = step.inputs.find(i => i.item === key);
            if (existing) existing.count += ing.count * times;
            else step.inputs.push({ item: key, count: ing.count * times });
          }
        }
        for (const res of recipe.results) {
          const existing = step.outputs.find(o => o.item === res.item);
          if (existing) existing.count += res.count * times;
          else step.outputs.push({ item: res.item, count: res.count * times });
        }
      } else {
        step = {
          machine: machineName,
          type: recipe.type,
          inputs: recipe.ingredients.filter(i => !i.catalyst).map(i => ({ item: i.item || i.tag || '', count: i.count * times })),
          outputs: recipe.results.map(r => ({ item: r.item, count: r.count * times })),
          times,
          energyPerOp: recipe.energy ?? 0,
          totalEnergy: (recipe.energy ?? 0) * times,
          timePerOp: recipe.processingTime ?? 0,
          totalTime: (recipe.processingTime ?? 0) * times,
        };
        machineSteps.push(step);
      }
    }

    return { item: id, quantity: actualOutput, recipe, children, isRaw: false, depth };
  }

  const tree = buildNode(itemId, quantity, 0);

  const summary: Record<string, number> = {};
  const rawSummary: Record<string, number> = {};

  function flatten(node: CalcNode) {
    const itemName = registry.getItemName(node.item);
    summary[itemName] = (summary[itemName] || 0) + node.quantity;
    if (node.isRaw) {
      rawSummary[itemName] = (rawSummary[itemName] || 0) + node.quantity;
    }
    for (const child of node.children) flatten(child);
  }
  flatten(tree);

  let totalOperations = 0;
  function countOps(node: CalcNode) {
    if (!node.isRaw && node.recipe) totalOperations++;
    for (const child of node.children) countOps(child);
  }
  countOps(tree);

  return {
    rootItem: itemId,
    quantity,
    tree,
    summary,
    rawSummary,
    totalOperations,
    machineSteps,
  };
}
