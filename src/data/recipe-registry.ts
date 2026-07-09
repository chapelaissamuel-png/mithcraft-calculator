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

  /** Generate a display name from an item ID */
  private nameFromId(id: string): string {
    const parts = id.split(':').pop()?.split('_') || [];
    return parts.map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  }

  /** Generate deterministic color from item ID hash */
  private colorFromId(id: string): string {
    const hues = [0, 25, 45, 80, 130, 180, 210, 260, 300, 330];
    let h = 0;
    for (let i = 0; i < id.length; i++) h = (h * 31 + id.charCodeAt(i)) | 0;
    return `hsl(${hues[Math.abs(h) % hues.length]}, 35%, 45%)`;
  }

  /** Generate a short code (1-3 chars) from an item ID */
  private shortFromId(id: string): string {
    const name = id.split(':').pop() || id;
    const parts = name.split('_');
    const primary = parts.find(p => !['block','ingot','nugget','dust','plate','sheet','crystal','gem'].includes(p)) || parts[0];
    // Take first 2 chars of primary word
    return primary.substring(0, 2).toUpperCase();
  }

  private buildIndex() {
    const recipes = getAllRecipes();

    // Collect all unique item IDs referenced in recipes
    const referenceIds = new Set<string>();
    for (const recipe of recipes) {
      for (const r of recipe.results) referenceIds.add(r.item);
      for (const ing of recipe.ingredients) referenceIds.add(ing.item);
      if (recipe.key) {
        for (const k in recipe.key) referenceIds.add(recipe.key[k].item);
      }
    }

    // Auto-generate metadata for items not in the static registry
    for (const id of referenceIds) {
      if (!this.items.has(id)) {
        const mod = id.split(':')[0];
        this.items.set(id, {
          id,
          name: this.nameFromId(id),
          mod,
          tier: 'common',
          maxStack: 64,
          type: 'item',
          short: this.shortFromId(id),
          color: this.colorFromId(id),
          tags: [],
        });
      }
    }
    
    // Count items per mod (from all items, including auto-generated)
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

    // Build item list for searching — sort by name for consistency
    this.itemList = Array.from(this.items.values())
      .sort((a, b) => a.name.localeCompare(b.name));
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
