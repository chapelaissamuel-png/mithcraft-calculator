import type { Recipe } from '../../types';
import { ItemIcon } from '../Common/ItemIcon';

interface CraftingGridProps {
  recipe: Recipe;
}

export function CraftingGrid({ recipe }: CraftingGridProps) {
  // For shaped recipes, arrange in 3x3 grid
  if (recipe.pattern && recipe.key) {
    const grid: (string | null)[] = [];
    for (let r = 0; r < 3; r++) {
      const row = recipe.pattern[r] || '   ';
      for (let c = 0; c < 3; c++) {
        const char = row[c] || ' ';
        const ing = recipe.key[char];
        grid.push(ing?.item || null);
      }
    }

    return (
      <div className="flex items-center gap-4">
        <div className="grid grid-cols-craft gap-0.5">
          {grid.map((item, i) => (
            <div key={i} className="craft-cell">
              {item && <ItemIcon itemId={item} size="sm" />}
            </div>
          ))}
        </div>
        <svg width="20" height="16" viewBox="0 0 20 16" className="text-jei-accent">
          <path d="M0 8h15M10 2l6 6-6 6" stroke="currentColor" strokeWidth="2" fill="none" />
        </svg>
        <div>
          <ItemIcon itemId={recipe.results[0]?.item} size="md" count={recipe.results[0]?.count} />
        </div>
      </div>
    );
  }

  // Shapeless / machine recipe
  return (
    <div className="flex items-center flex-wrap gap-3">
      <div className="flex items-center gap-1.5 flex-wrap">
        {recipe.ingredients.map((ing, i) => (
          <div key={i} className="flex flex-col items-center gap-0.5">
            <ItemIcon itemId={ing.item} size="sm" count={ing.count} />
            {ing.catalyst && <span className="text-[8px] text-jei-accent">Cat</span>}
          </div>
        ))}
      </div>
      <svg width="20" height="16" viewBox="0 0 20 16" className="text-jei-accent">
        <path d="M0 8h15M10 2l6 6-6 6" stroke="currentColor" strokeWidth="2" fill="none" />
      </svg>
      <div className="flex items-center gap-1.5">
        {recipe.results.map((res, i) => (
          <ItemIcon key={i} itemId={res.item} size="md" count={res.count} />
        ))}
      </div>
    </div>
  );
}
