// ─── Core Types ───────────────────────────────────────────

export type RecipeCategory =
  | 'crafting'           // Vanilla crafting table
  | 'smelting'           // Furnace
  | 'blasting'           // Blast furnace
  | 'smoking'            // Smoker
  | 'campfire'           // Campfire
  | 'smithing'           // Smithing table
  | 'stonecutting'       // Stonecutter
  | 'brewing'            // Brewing stand
  | 'mekanism:crushing'
  | 'mekanism:enriching'
  | 'mekanism:combining'
  | 'mekanism:infusing'
  | 'mekanism:pigment_extracting'
  | 'mekanism:metallurgic_infusing'
  | 'thermal:pulverizer'
  | 'thermal:smelter'
  | 'thermal:centrifuge'
  | 'thermal:crystallizer'
  | 'thermal:press'
  | 'thermal:refinery'
  | 'thermal:induction_smelter'
  | 'create:mixing'
  | 'create:crushing'
  | 'create:pressing'
  | 'create:cutting'
  | 'create:deploying'
  | 'create:haunting'
  | 'create:splashing'
  | 'create:compacting'
  | 'ic2:compressor'
  | 'ic2:extractor'
  | 'ic2:macerator'
  | 'ic2:recycler'
  | 'ae2:inscriber'
  | 'ae2:charger'
  | 'immersiveengineering:crusher'
  | 'immersiveengineering:arc_furnace'
  | 'immersiveengineering:metal_press'
  | 'pam:cutting_board'
  | 'occult:ritual'
  | 'bloodmagic:altar'
  | 'botania:runic_altar'
  | 'botania:mana_pool'
  | 'machine';            // Generic machine recipe

export interface Ingredient {
  /** Item ID (e.g. "minecraft:iron_ingot") */
  item: string;
  /** Stack count (default 1) */
  count: number;
  /** Ore dictionary / tag (alternative to item) */
  tag?: string;
  /** NBT or other metadata */
  nbt?: string;
  /** Whether this ingredient is NOT consumed (catalyst) */
  catalyst?: boolean;
  /** Fluid input */
  fluid?: string;
  /** Fluid amount in mb */
  fluidAmount?: number;
}

export interface Result {
  /** Item ID */
  item: string;
  /** Stack count (default 1) */
  count: number;
  /** Fluid output */
  fluid?: string;
  fluidAmount?: number;
  /** Chance (0-1), for secondary/bonus outputs */
  chance?: number;
}

export interface Recipe {
  /** Unique ID (e.g. "minecraft:iron_ingot_from_blasting") */
  id: string;
  /** Recipe type */
  type: RecipeCategory;
  /** Mod namespace (e.g. "minecraft", "mekanism", "thermal") */
  mod: string;
  /** Input ingredients */
  ingredients: Ingredient[];
  /** Output results (primary is [0]) */
  results: Result[];
  /** For shaped recipes — the pattern rows */
  pattern?: string[];
  /** For shaped recipes — pattern key → ingredient map */
  key?: Record<string, Ingredient>;
  /** Energy required (RF/FE) */
  energy?: number;
  /** Processing time in ticks (20 ticks = 1s) */
  processingTime?: number;
  /** Whether the recipe is shapeless */
  shapeless?: boolean;
}

// ─── Item Registry ────────────────────────────────────────

export interface ItemMeta {
  /** Namespaced ID */
  id: string;
  /** Display name (e.g. "Iron Ingot") */
  name: string;
  /** Mod namespace */
  mod: string;
  /** Rarity tier for color coding */
  tier: 'common' | 'uncommon' | 'rare' | 'epic';
  /** Stack size (default 64) */
  maxStack: number;
  /** Item type */
  type: 'item' | 'block' | 'tool' | 'armor' | 'food' | 'fluid';
  /** Short display (1-3 chars for grid view) */
  short: string;
  /** Hex color for background representation */
  color: string;
  /** Tags this item belongs to */
  tags: string[];
}

// ─── Mod Registry ─────────────────────────────────────────

export interface ModInfo {
  /** Namespace (e.g. "mekanism") */
  id: string;
  /** Display name (e.g. "Mekanism") */
  name: string;
  /** Hex color for mod badge */
  color: string;
  /** Number of items known */
  itemCount: number;
  /** Short code for @ filtering */
  short: string;
}

// ─── Calculator Types ─────────────────────────────────────

export interface CalcNode {
  /** The item being calculated */
  item: string;
  /** Required quantity */
  quantity: number;
  /** How this item is crafted (recipe used) */
  recipe: Recipe | null;
  /** Sub-components (children) */
  children: CalcNode[];
  /** Whether this is a raw/basic resource (not craftable) */
  isRaw: boolean;
  /** Depth level for display indentation */
  depth: number;
}

export interface CalcResult {
  /** The root item calculated */
  rootItem: string;
  /** Total quantity requested */
  quantity: number;
  /** Full calculation tree */
  tree: CalcNode;
  /** Flattened summary: item_id → total count needed */
  summary: Record<string, number>;
  /** Only raw/base resources in summary */
  rawSummary: Record<string, number>;
  /** Total number of crafting operations */
  totalOperations: number;
  /** Machine steps breakdown */
  machineSteps: MachineStep[];
}

export interface MachineStep {
  /** Machine name */
  machine: string;
  /** Recipe category */
  type: RecipeCategory;
  /** Input items going in */
  inputs: { item: string; count: number }[];
  /** Output items coming out */
  outputs: { item: string; count: number }[];
  /** Times this operation is performed */
  times: number;
  /** Energy per operation */
  energyPerOp: number;
  /** Total energy */
  totalEnergy: number;
  /** Processing time per operation (ticks) */
  timePerOp: number;
  /** Total processing time (ticks) */
  totalTime: number;
}

// ─── Search Types ─────────────────────────────────────────

export interface SearchFilter {
  /** Search query text */
  query: string;
  /** Optional mod filter (@mekanism) */
  modFilter: string | null;
  /** Item type filter */
  typeFilter: string | null;
  /** Sort mode */
  sort: 'name' | 'mod' | 'tier';
}
