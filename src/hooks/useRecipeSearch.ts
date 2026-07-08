import { useState, useMemo, useCallback, useEffect } from 'react';
import type { ItemMeta, SearchFilter } from '../types';
import { registry } from '../data/recipe-registry';
import Fuse from 'fuse.js';

const fuseOptions = {
  keys: [
    { name: 'name', weight: 2 },
    { name: 'id', weight: 1.5 },
    { name: 'short', weight: 1 },
    { name: 'mod', weight: 0.5 },
  ],
  threshold: 0.3,
  includeScore: true,
  minMatchCharLength: 1,
};

export function useRecipeSearch() {
  const allItems = registry.getAllItems();
  const mods = registry.getMods();
  const [filter, setFilter] = useState<SearchFilter>({
    query: '',
    modFilter: null,
    typeFilter: null,
    sort: 'name',
  });
  const [results, setResults] = useState<ItemMeta[]>([]);

  const fuse = useMemo(() => new Fuse(allItems, fuseOptions), [allItems]);

  const performSearch = useCallback((q: string, modFilter?: string | null) => {
    let items: ItemMeta[];
    if (q.length > 0) {
      const fuseResults = fuse.search(q);
      items = fuseResults.map(r => r.item);
    } else {
      items = allItems;
    }
    if (modFilter) {
      const norm = modFilter.replace('@', '').toLowerCase();
      items = items.filter(i => i.mod === norm);
    }
    setResults(items);
  }, [allItems, fuse]);

  useEffect(() => {
    performSearch(filter.query, filter.modFilter);
  }, [filter, performSearch]);

  const setQuery = useCallback((query: string) => {
    const modMatch = query.match(/@(\w+)/);
    const modFilter = modMatch ? modMatch[1] : null;
    const cleanQuery = query.replace(/@\w+\s*/g, '').trim();
    setFilter(prev => ({ ...prev, query: cleanQuery, modFilter }));
  }, []);

  return {
    results,
    mods,
    filter,
    setQuery,
    totalItems: allItems.length,
    totalRecipes: registry.getRecipeCount(),
  };
}
