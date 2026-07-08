import { useRef, useCallback } from 'react';
import { useVirtualizer } from '@tanstack/react-virtual';
import type { ItemMeta } from '../../types';
import { ItemCard } from './ItemCard';

interface ItemGridProps {
  items: ItemMeta[];
  selectedItem: string | null;
  onSelectItem: (itemId: string) => void;
}

const GRID_GAP = 4; // px
const ITEM_SIZE = 68; // 64px cell + 4px gap
const COL_WIDTH = ITEM_SIZE + GRID_GAP;

export function ItemGrid({ items, selectedItem, onSelectItem }: ItemGridProps) {
  const parentRef = useRef<HTMLDivElement>(null);

  // Calculate number of columns based on container width
  const getColumnCount = useCallback(() => {
    if (!parentRef.current) return 8;
    return Math.max(1, Math.floor(parentRef.current.clientWidth / COL_WIDTH));
  }, []);

  const columnCount = getColumnCount();
  const rowCount = Math.ceil(items.length / columnCount);

  const virtualizer = useVirtualizer({
    count: rowCount,
    getScrollElement: () => parentRef.current,
    estimateSize: () => ITEM_SIZE + GRID_GAP,
    overscan: 5,
  });

  return (
    <div
      ref={parentRef}
      className="flex-1 overflow-y-auto px-2"
      style={{ contain: 'strict' }}
    >
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          width: '100%',
          position: 'relative',
        }}
      >
        {virtualizer.getVirtualItems().map(virtualRow => {
          const rowIndex = virtualRow.index;
          const startIdx = rowIndex * columnCount;
          const rowItems = items.slice(startIdx, startIdx + columnCount);

          return (
            <div
              key={rowIndex}
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                transform: `translateY(${virtualRow.start}px)`,
                display: 'flex',
                gap: GRID_GAP,
                padding: `0 0 ${GRID_GAP}px 0`,
              }}
            >
              {rowItems.map(item => (
                <div key={item.id} style={{ width: ITEM_SIZE, flexShrink: 0 }}>
                  <ItemCard
                    item={item}
                    isSelected={selectedItem === item.id}
                    onClick={() => onSelectItem(item.id)}
                  />
                </div>
              ))}
              {/* Fill remaining space */}
              {rowItems.length < columnCount && (
                <div style={{ flex: 1 }} />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
