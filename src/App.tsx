import { useState } from 'react';
import { useRecipeSearch } from './hooks/useRecipeSearch';
import { useCalculator } from './hooks/useCalculator';
import { SearchBar } from './components/Search/SearchBar';
import { SectionedGrid } from './components/Grid/SectionedGrid';
import { QuantitySelector } from './components/Common/QuantitySelector';
import { ResourceSummary } from './components/Recipe/ResourceSummary';
import { registry } from './data/recipe-registry';

export default function App() {
  const { results, mods, setQuery, totalItems, totalRecipes } = useRecipeSearch();
  const { calcResult, isCalculating, selectedItem, quantity, setQuantity, calculate } = useCalculator();

  const [searchInput, setSearchInput] = useState('');
  const [showModList, setShowModList] = useState(false);

  const handleSearchChange = (val: string) => {
    setSearchInput(val);
    setQuery(val);
  };

  const handleSelectItem = (itemId: string) => {
    if (itemId === selectedItem) return;
    calculate(itemId, quantity);
  };

  const handleQuantityChange = (val: number) => {
    setQuantity(val);
    if (selectedItem) {
      calculate(selectedItem, val);
    }
  };

  const handleModClick = (modId: string) => {
    const newQuery = `@${modId} `;
    setSearchInput(newQuery);
    setQuery(newQuery);
    setShowModList(false);
  };

  return (
    <div className="h-screen flex flex-col bg-jei-bg">
      {/* === HEADER === */}
      <header className="flex items-center justify-between px-4 py-2 border-b border-jei-border bg-jei-panel flex-shrink-0">
        <div className="flex items-center gap-3">
          <h1 className="text-sm font-bold text-jei-accent tracking-wide">
            MITH<span className="text-jei-text">CRAFT</span>
          </h1>
          <span className="text-[10px] text-jei-text-dim border-l border-jei-border pl-3">
            Calculateur de Crafts Moddés
          </span>
        </div>
        <div className="flex items-center gap-4">
          <div className="relative">
            <button
              onClick={() => setShowModList(!showModList)}
              className="text-[11px] text-jei-text-dim hover:text-jei-text px-2 py-1 rounded hover:bg-jei-hover transition-colors"
            >
              Mods ▾
            </button>
            {showModList && (
              <div className="absolute right-0 top-full mt-1 bg-jei-panel border border-jei-border rounded shadow-xl z-50 py-1 min-w-[180px]">
                <div className="max-h-[300px] overflow-y-auto">
                  {mods.map(mod => (
                    <button
                      key={mod.id}
                      onClick={() => handleModClick(mod.id)}
                      className="w-full text-left px-3 py-1.5 text-xs text-jei-text-dim hover:text-jei-text hover:bg-jei-hover transition-colors flex items-center gap-2"
                    >
                      <span className="w-2 h-2 rounded-full flex-shrink-0" style={{ backgroundColor: mod.color }} />
                      <span>{mod.name}</span>
                      <span className="ml-auto text-[10px] text-jei-text-dim">{mod.itemCount}</span>
                    </button>
                  ))}
                </div>
                <div className="border-t border-jei-border mt-1 pt-1">
                  <button
                    onClick={() => { setSearchInput(''); setQuery(''); setShowModList(false); }}
                    className="w-full text-left px-3 py-1.5 text-xs text-jei-accent hover:bg-jei-hover transition-colors"
                  >
                    ✕ Effacer le filtre
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* === MAIN LAYOUT === */}
      <div className="flex flex-1 overflow-hidden">
        {/* === LEFT PANEL: Search + Grid === */}
        <div className="flex flex-col w-[340px] min-w-[260px] border-r border-jei-border flex-shrink-0">
          <div className="px-3 py-2 border-b border-jei-border">
            <SearchBar
              value={searchInput}
              onChange={handleSearchChange}
              totalItems={totalItems}
              totalRecipes={totalRecipes}
            />
          </div>

          <div className="px-3 py-2 border-b border-jei-border">
            <QuantitySelector value={quantity} onChange={handleQuantityChange} />
          </div>

          <div className="flex-1 overflow-y-auto px-3 py-2">
            <SectionedGrid
              items={results}
              mods={mods}
              selectedId={selectedItem}
              onSelect={handleSelectItem}
            />
          </div>

          <div className="px-3 py-1.5 border-t border-jei-border text-[10px] text-jei-text-dim flex-shrink-0">
            {results.length} résultats
          </div>
        </div>

        {/* === RIGHT PANEL: Recipe Details === */}
        <div className="flex-1 overflow-y-auto bg-jei-bg">
          {isCalculating ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-sm text-jei-text-dim animate-pulse">Calcul en cours...</div>
            </div>
          ) : calcResult ? (
            <div className="p-4">
              <ResourceSummary calcResult={calcResult} />
            </div>
          ) : selectedItem ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-center space-y-2">
                <div className="text-sm text-jei-text-dim">Aucune recette trouvée pour</div>
                <div className="text-sm text-jei-accent font-semibold">
                  {registry.getItemName(selectedItem)}
                </div>
                <div className="text-xs text-jei-text-dim">
                  Cet item est peut-être une ressource de base.
                </div>
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-center h-full">
              <div className="text-center space-y-3 max-w-md">
                <div className="text-3xl">🔍</div>
                <h2 className="text-base font-semibold text-jei-text-dim">
                  Sélectionne un item
                </h2>
                <p className="text-xs text-jei-text-dim leading-relaxed">
                  Cherche un item dans la barre de recherche, clique sur un résultat,
                  et le calculateur décomposera automatiquement sa recette en ressources de base.
                </p>
                <div className="flex flex-wrap gap-2 justify-center mt-4">
                  {['Iron Pickaxe', 'Piston', 'Diamond Block'].map(name => {
                    const item = registry.getAllItems().find(i => i.name === name);
                    return item ? (
                      <button
                        key={name}
                        onClick={() => handleSelectItem(item.id)}
                        className="text-xs px-3 py-1.5 bg-jei-panel border border-jei-border rounded hover:bg-jei-hover text-jei-text-dim hover:text-jei-text transition-colors"
                      >
                        {name}
                      </button>
                    ) : null;
                  })}
                </div>
                <p className="text-[10px] text-jei-text-dim mt-4 border-t border-jei-border pt-3">
                  {totalItems} items • {totalRecipes} recettes • {mods.length} mods chargés
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
