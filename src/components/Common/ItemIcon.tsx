import type { ItemMeta } from '../../types';
import { registry } from '../../data/recipe-registry';

interface ItemIconProps {
  itemId?: string;
  itemMeta?: ItemMeta;
  size?: 'sm' | 'md' | 'lg';
  count?: number;
  showTooltip?: boolean;
}

const sizeMap = { sm: 32, md: 48, lg: 64 };
const fontMap = { sm: 8, md: 10, lg: 13 };

export function ItemIcon({ itemId, itemMeta, size = 'md', count, showTooltip = true }: ItemIconProps) {
  const meta = itemMeta || (itemId ? registry.getItem(itemId) : undefined);
  if (!meta) {
    return (
      <div
        className="item-cell flex items-center justify-center"
        style={{ width: sizeMap[size], height: sizeMap[size] }}
      >
        <span style={{ fontSize: fontMap[size], color: '#555' }}>?</span>
      </div>
    );
  }

  const px = sizeMap[size];
  const fs = fontMap[size];

  return (
    <div
      className={`item-cell flex items-center justify-center tier-${meta.tier}`}
      style={{ width: px, height: px }}
      title={showTooltip ? `${meta.name} (${meta.mod})` : undefined}
    >
      {/* Background color blob */}
      <div
        style={{
          width: px - 8,
          height: px - 8,
          borderRadius: 2,
          backgroundColor: meta.color + '30',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          position: 'relative',
        }}
      >
        {/* Item abbreviation */}
        <span
          style={{
            fontSize: fs,
            fontWeight: 600,
            color: meta.color,
            textShadow: '0 1px 2px rgba(0,0,0,0.5)',
            userSelect: 'none',
          }}
        >
          {meta.short}
        </span>

        {/* Stack count badge */}
        {count && count > 1 && (
          <span
            style={{
              position: 'absolute',
              bottom: -2,
              right: -2,
              fontSize: 8,
              fontWeight: 700,
              color: '#FFF',
              background: 'rgba(0,0,0,0.7)',
              padding: '0 3px',
              borderRadius: 2,
              lineHeight: '12px',
            }}
          >
            {count}
          </span>
        )}
      </div>
    </div>
  );
}
