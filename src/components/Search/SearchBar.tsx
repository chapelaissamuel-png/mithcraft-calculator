import { useRef, useEffect } from 'react';

interface SearchBarProps {
  value: string;
  onChange: (val: string) => void;
  totalItems: number;
  totalRecipes: number;
}

export function SearchBar({ value, onChange, totalItems, totalRecipes }: SearchBarProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const hasModFilter = value.includes('@');

  return (
    <div className="space-y-2">
      <div className="relative">
        <input
          ref={inputRef}
          type="text"
          value={value}
          onChange={e => onChange(e.target.value)}
          placeholder="Rechercher un item... (@mekanism pour filtrer)"
          className="jei-search rounded w-full px-3 py-2 text-sm pl-8"
        />
        <svg
          className="absolute left-2.5 top-1/2 -translate-y-1/2"
          width="14" height="14" viewBox="0 0 24 24"
          fill="none" stroke="#555" strokeWidth="2"
        >
          <circle cx="11" cy="11" r="8" />
          <path d="M21 21l-4.35-4.35" />
        </svg>
      </div>
      <div className="flex items-center justify-between text-[11px] text-jei-text-dim px-1">
        <span>{totalItems} items • {totalRecipes} recettes</span>
        {hasModFilter && (
          <span className="text-jei-accent">Filtre mod actif</span>
        )}
      </div>
    </div>
  );
}
