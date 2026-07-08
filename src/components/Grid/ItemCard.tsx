import type { ItemMeta } from '../../types';
import { ItemIcon } from '../Common/ItemIcon';

interface ItemCardProps {
  item: ItemMeta;
  isSelected: boolean;
  onClick: () => void;
}

export function ItemCard({ item, isSelected, onClick }: ItemCardProps) {
  return (
    <div
      className={`item-cell flex flex-col items-center justify-center gap-0.5 p-1 ${
        isSelected ? 'selected' : ''
      }`}
      onClick={onClick}
      title={`${item.name} (${item.mod})`}
    >
      <ItemIcon itemMeta={item} size="sm" showTooltip={false} />
      <span className="text-[9px] text-jei-text-dim truncate w-full text-center leading-tight">
        {item.short}
      </span>
    </div>
  );
}
