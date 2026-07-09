import type { Ingredient, Recipe, RecipeCategory, Result } from '../../types';

/** Build a simple ingredient reference */
export const ing = (item: string, count = 1): Ingredient => ({ item, count });

/** Build a tag ingredient reference */
export const ingTag = (tag: string, count = 1): Ingredient => ({ item: '', count, tag });

/** Extract unique ingredients from pattern+key */
function extractIngredients(
  ingredients: Ingredient[],
  opts?: { pattern?: string[]; key?: Record<string, Ingredient> },
): Ingredient[] {
  if (ingredients.length > 0) return ingredients;
  if (opts?.key) {
    const seen = new Set<string>();
    const result: Ingredient[] = [];
    for (const ingr of Object.values(opts.key)) {
      const key = ingr.item || ingr.tag || '';
      if (!seen.has(key)) {
        seen.add(key);
        result.push({ ...ingr });
      }
    }
    return result;
  }
  return ingredients;
}

/** Recipe builder factory */
export const res = (item: string, count = 1): Result => ({ item, count });

export function r(
  id: string,
  type: RecipeCategory,
  mod: string,
  results: { item: string; count?: number }[],
  ingredients: Ingredient[],
  opts?: {
    pattern?: string[];
    key?: Record<string, Ingredient>;
    energy?: number;
    time?: number;
    machine?: string;
  },
): Recipe {
  return {
    id,
    type,
    mod,
    ingredients: extractIngredients(ingredients, opts),
    results: results.map(r => ({ item: r.item, count: r.count ?? 1 })),
    ...(opts?.pattern ? { pattern: opts.pattern, key: opts.key } : {}),
    ...(opts?.energy ? { energy: opts.energy } : {}),
    ...(opts?.time ? { processingTime: opts.time } : {}),
  };
}
