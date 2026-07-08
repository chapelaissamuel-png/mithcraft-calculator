import type { Recipe, ItemMeta, ModInfo } from '../types';
import { MODS } from './item-defs';
import { buildItemRegistry } from './item-defs';
import { getAllRecipes } from './recipe-defs';

// ─── Registry singleton ──────────────────────────────

class RecipeRegistry {
  private recipes: Map<string, Recipe[]> = new Map();   // itemId → recipes that PRODUCE it
  private allRecipes: Recipe[] = [];
  private items: Map<string, ItemMeta>;
  private mods: ModInfo[];
  private itemList: ItemMeta[] = [];

  constructor() {
    this.items = buildItemRegistry();
    this.mods = [...MODS.map(m => ({ ...m, itemCount: 0 }))];
    this.buildIndex();
  }

  private buildIndex() {
    const recipes = getAllRecipes();
    
    // Count items per mod
    for (const [id] of this.items) {
      const mod = id.split(':')[0];
      const modInfo = this.mods.find(m => m.id === mod);
      if (modInfo) modInfo.itemCount++;
    }

    // Index recipes by output item
    for (const recipe of recipes) {
      this.allRecipes.push(recipe);
      for (const result of recipe.results) {
        const existing = this.recipes.get(result.item) || [];
        existing.push(recipe);
        this.recipes.set(result.item, existing);
      }
    }

    // Build item list for searching
    this.itemList = Array.from(this.items.values());
  }

  /** Get all recipes that produce a given item */
  getRecipesFor(itemId: string): Recipe[] {
    return this.recipes.get(itemId) || [];
  }

  /** Lookup an item by ID */
  getItem(itemId: string): ItemMeta | undefined {
    return this.items.get(itemId);
  }

  /** Get an item's display name */
  getItemName(itemId: string): string {
    return this.items.get(itemId)?.name || itemId.split(':').pop() || itemId;
  }

  /** Get full item metadata */
  getItemMeta(itemId: string): ItemMeta | undefined {
    return this.items.get(itemId);
  }

  /** Check if an item has recipes (is craftable vs raw) */
  isCraftable(itemId: string): boolean {
    return this.recipes.has(itemId) && (this.recipes.get(itemId)?.length ?? 0) > 0;
  }

  /** Get all items matching a search */
  searchItems(query: string, modFilter?: string | null): ItemMeta[] {
    let results = this.itemList;
    
    if (modFilter) {
      const norm = modFilter.replace('@', '').toLowerCase();
      results = results.filter(i => i.mod === norm);
    }

    if (!query) return results;

    const q = query.toLowerCase();
    return results.filter(i =>
      i.name.toLowerCase().includes(q) ||
      i.id.toLowerCase().includes(q) ||
      i.short.toLowerCase().includes(q) ||
      i.mod.toLowerCase().includes(q)
    );
  }

  /** Get all recipes */
  getAllRecipes(): Recipe[] {
    return this.allRecipes;
  }

  /** Get all items */
  getAllItems(): ItemMeta[] {
    return this.itemList;
  }

  /** Get all mods */
  getMods(): ModInfo[] {
    return this.mods;
  }

  /** Get item count */
  getItemCount(): number {
    return this.itemList.length;
  }

  /** Get recipe count */
  getRecipeCount(): number {
    return this.allRecipes.length;
  }
}

// Singleton
export const registry = new RecipeRegistry();
