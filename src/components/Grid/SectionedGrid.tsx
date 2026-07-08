import type { ItemMeta, ModInfo } from '../../types';
import { ItemCard } from '../Grid/ItemCard';

interface SectionedGridProps {
  items: ItemMeta[];
  mods: ModInfo[];
  selectedId: string | null;
  onSelect: (id: string) => void;
}

/** Group items by mod and render section headers */
export function SectionedGrid({ items, mods, selectedId, onSelect }: SectionedGridProps) {
  if (items.length === 0) {
    return (
      <div className="flex items-center justify-center h-48">
        <p className="text-sm text-jei-text-dim italic">Aucun item trouvé</p>
      </div>
    );
  }

  // Group items by mod
  const grouped = new Map<string, ItemMeta[]>();
  for (const item of items) {
    const list = grouped.get(item.mod) || [];
    list.push(item);
    grouped.set(item.mod, list);
  }

  // Sort mods in display order
  const modOrder = mods.map(m => m.id);
  const sortedGroups = Array.from(grouped.entries())
    .sort((a, b) => {
      const ia = modOrder.indexOf(a[0]);
      const ib = modOrder.indexOf(b[0]);
      return (ia === -1 ? 999 : ia) - (ib === -1 ? 999 : ib);
    });

  return (
    <div className="space-y-4">
      {sortedGroups.map(([modId, groupItems]) => {
        const modInfo = mods.find(m => m.id === modId);
        return (
          <section key={modId}>
            {/* Mod Section Header */}
            <div className="sticky top-0 z-10 bg-jei-surface/90 backdrop-blur-sm mb-2 pb-1"
              style={{ borderBottom: `2px solid ${modInfo?.color || '#666'}40` }}>
              <div className="flex items-center gap-2">
                <div
                  className="w-2 h-2 rounded-full flex-shrink-0"
                  style={{ backgroundColor: modInfo?.color || '#666' }}
                />
                <h3 className="text-xs font-bold uppercase tracking-wider"
                  style={{ color: modInfo?.color || '#666' }}>
                  {modInfo?.name || modId}
                </h3>
                <span className="text-[10px] text-jei-text-dim ml-auto">{groupItems.length}</span>
              </div>
            </div>

            {/* Items grid */}
            <div className="grid items-grid items-grid-scrollable">
              {groupItems.map(item => (
                <ItemCard
                  key={item.id}
                  item={item}
                  isSelected={item.id === selectedId}
                  onClick={() => onSelect(item.id)}
                />
              ))}
            </div>
          </section>
        );
      })}
    </div>
  );
}
