import { useState } from 'react';
import { registry } from '../../data/recipe-registry';
import { ItemIcon } from '../Common/ItemIcon';
import type { ModInfo } from '../../types';

interface ModBrowserProps {
  mods: ModInfo[];
  items: { id: string; name: string; mod: string; type: string }[];
  selectedId: string | null;
  onSelect: (itemId: string) => void;
}

interface MachineGroup {
  type: string;
  typeLabel: string;
  items: { id: string; name: string }[];
}

const MOD_MACHINES: Record<string, { type: string; label: string }[]> = {
  minecraft: [
    { type: 'crafting', label: '🍳 Table de craft' },
    { type: 'smelting', label: '🔥 Four' },
    { type: 'blasting', label: '🔥 Fonderie' },
    { type: 'smithing', label: '🔨 Table de forgeron' },
  ],
  mekanism: [
    { type: 'mekanism:enriching', label: '⚡ Enrichisseur' },
    { type: 'mekanism:crushing', label: '⚡ Concasseur' },
    { type: 'mekanism:combining', label: '⚡ Combineur' },
    { type: 'mekanism:infusing', label: '⚡ Infuseur métallurgique' },
    { type: 'mekanism:metallurgic_infusing', label: '⚡ Infusion avancée' },
    { type: 'mekanism:pigment_extracting', label: '⚡ Extraction' },
    { type: 'crafting', label: '🍳 Crafting' },
    { type: 'smelting', label: '🔥 Cuisson' },
    { type: 'blasting', label: '🔥 Fonderie' },
  ],
  create: [
    { type: 'crafting', label: '🍳 Crafting' },
    { type: 'create:mixing', label: '⚙️ Mélange' },
    { type: 'create:crushing', label: '⚙️ Concassage' },
    { type: 'create:pressing', label: '⚙️ Pressage' },
    { type: 'create:cutting', label: '⚙️ Sciage' },
    { type: 'create:deploying', label: '⚙️ Déploiement' },
    { type: 'create:compacting', label: '⚙️ Compactage' },
  ],
  thermal: [
    { type: 'crafting', label: '🍳 Crafting' },
    { type: 'thermal:pulverizer', label: '🔥 Pulvériseur' },
    { type: 'thermal:induction_smelter', label: '🔥 Fonte par induction' },
    { type: 'thermal:centrifuge', label: '🔥 Centrifuge' },
    { type: 'thermal:crystallizer', label: '🔥 Cristalliseur' },
    { type: 'thermal:press', label: '🔥 Presse' },
    { type: 'smelting', label: '🔥 Cuisson' },
    { type: 'blasting', label: '🔥 Fonderie' },
  ],
  ae2: [
    { type: 'crafting', label: '🍳 Crafting' },
    { type: 'ae2:inscriber', label: '🔧 Inscripteur' },
    { type: 'ae2:charger', label: '🔋 Chargeur' },
    { type: 'smelting', label: '🔥 Cuisson' },
  ],
  ic2: [
    { type: 'crafting', label: '🍳 Crafting' },
    { type: 'ic2:compressor', label: '🔄 Compresseur' },
    { type: 'ic2:extractor', label: '🔄 Extracteur' },
    { type: 'ic2:macerator', label: '🔄 Macérateur' },
    { type: 'ic2:recycler', label: '🔄 Recycleur' },
    { type: 'smelting', label: '🔥 Cuisson' },
  ],
};

export function ModBrowser({ mods, items, selectedId, onSelect }: ModBrowserProps) {
  const [expandedMods, setExpandedMods] = useState<Set<string>>(new Set(['minecraft', 'mekanism']));
  const [expandedMachines, setExpandedMachines] = useState<Set<string>>(new Set(['crafting']));
  const [modSearch, setModSearch] = useState('');

  const toggleMod = (modId: string) => {
    setExpandedMods(prev => {
      const next = new Set(prev);
      if (next.has(modId)) next.delete(modId);
      else next.add(modId);
      return next;
    });
  };

  const toggleMachine = (key: string) => {
    setExpandedMachines(prev => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  };

  const filteredItems = modSearch
    ? items.filter(i => i.name.toLowerCase().includes(modSearch.toLowerCase()))
    : items;

  // Build mod → machine → items tree
  const machineGroups = (modId: string): MachineGroup[] => {
    const machines = MOD_MACHINES[modId];
    if (!machines) return [];
    
    return machines.map(m => {
      // Find items that have recipes of this type from this mod
      const typeItems = filteredItems.filter(item => {
        if (item.mod !== modId) return false;
        const recipes = registry.getRecipesFor(item.id);
        return recipes.some(r => {
          if (m.type === 'crafting') {
            return (r.type === 'crafting' && r.mod === modId) || 
                   (r.type === 'crafting' && modId === 'minecraft');
          }
          return r.type === m.type;
        });
      }).map(item => ({ id: item.id, name: item.name }));
      
      return { type: m.type, typeLabel: m.label, items: typeItems };
    }).filter(g => g.items.length > 0);
  };

  const getModItemCount = (modId: string): number => {
    return filteredItems.filter(i => i.mod === modId).length;
  };

  const modColors: Record<string, string> = {};
  mods.forEach(m => { modColors[m.id] = m.color; });

  return (
    <div className="flex flex-col h-full">
      {/* Search within mods */}
      <div className="px-2 py-1.5 border-b border-jei-border">
        <input
          type="text"
          value={modSearch}
          onChange={e => setModSearch(e.target.value)}
          placeholder="Filtrer les items..."
          className="w-full bg-jei-surface text-xs text-jei-text px-2 py-1.5 rounded border border-jei-border/50 
                     placeholder:text-jei-text-dim/50 outline-none focus:border-jei-accent/50 transition-colors"
        />
      </div>

      {/* Mod tree */}
      <div className="flex-1 overflow-y-auto">
        {mods.map(mod => {
          const itemCount = getModItemCount(mod.id);
          if (itemCount === 0 && !modSearch) return null;
          const isExpanded = expandedMods.has(mod.id);
          const groups = isExpanded ? machineGroups(mod.id) : [];
          const hasGroups = groups.length > 0;

          return (
            <div key={mod.id} className="border-b border-jei-border/30">
              {/* Mod header */}
              <button
                onClick={() => toggleMod(mod.id)}
                className={`w-full flex items-center gap-2 px-3 py-2 text-xs font-semibold 
                  hover:bg-jei-hover transition-colors
                  ${isExpanded ? 'bg-jei-hover/50' : ''}`}
                style={{ borderLeft: `3px solid ${modColors[mod.id] || '#666'}` }}
              >
                <span className="text-[9px] text-jei-text-dim w-3">
                  {isExpanded ? '▼' : '▶'}
                </span>
                <span className="text-jei-text">{mod.name}</span>
                <span className="ml-auto text-[9px] text-jei-text-dim">{itemCount}</span>
              </button>

              {/* Machine categories */}
              {isExpanded && hasGroups && groups.map(group => {
                const machineKey = `${mod.id}:${group.type}`;
                const isMachineExpanded = expandedMachines.has(machineKey);
                if (group.items.length === 0) return null;

                return (
                  <div key={machineKey}>
                    <button
                      onClick={() => toggleMachine(machineKey)}
                      className="w-full flex items-center gap-1.5 pl-7 pr-2 py-1 text-[10px] 
                        text-jei-text-dim hover:text-jei-text hover:bg-jei-hover/30 transition-colors"
                    >
                      <span className="text-[8px]">{isMachineExpanded ? '▼' : '▶'}</span>
                      <span>{group.typeLabel}</span>
                      <span className="ml-auto text-[8px] opacity-60">{group.items.length}</span>
                    </button>

                    {/* Items */}
                    {isMachineExpanded && group.items.map(item => (
                      <button
                        key={item.id}
                        onClick={() => onSelect(item.id)}
                        className={`w-full flex items-center gap-1.5 pl-10 pr-2 py-0.5 text-[11px] 
                          hover:bg-jei-hover/50 transition-colors
                          ${selectedId === item.id ? 'bg-jei-accent/10 text-jei-accent font-medium' : 'text-jei-text-dim'}`}
                      >
                        <ItemIcon itemId={item.id} size="sm" />
                        <span className="truncate">{item.name}</span>
                      </button>
                    ))}
                  </div>
                );
              })}

              {/* Empty mod message */}
              {isExpanded && !hasGroups && itemCount > 0 && (
                <button
                  onClick={() => toggleMachine(`${mod.id}:items`)}
                  className="w-full flex items-center gap-1.5 pl-7 pr-2 py-1"
                >
                  <span className="text-[10px] text-jei-text-dim">Tous les items ({itemCount})</span>
                </button>
              )}
            </div>
          );
        })}
      </div>

      {/* Footer stats */}
      <div className="px-3 py-1.5 border-t border-jei-border text-[10px] text-jei-text-dim flex-shrink-0">
        {filteredItems.length} items • {registry.getAllRecipes().length} recettes
      </div>
    </div>
  );
}
