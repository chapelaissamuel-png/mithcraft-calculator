import type { CalcResult, MachineStep, Recipe } from '../../types';
import { registry } from '../../data/recipe-registry';
import { ItemIcon } from '../Common/ItemIcon';

interface ResourceSummaryProps {
  calcResult: CalcResult;
}

export function ResourceSummary({ calcResult }: ResourceSummaryProps) {
  const { summary, rawSummary, totalOperations, machineSteps, tree } = calcResult;

  const rawEntries = Object.entries(rawSummary).sort(([, a], [, b]) => b - a);
  const totalEntries = Object.entries(summary).sort(([, a], [, b]) => b - a);

  // Get the primary recipe used
  const primaryRecipe = tree?.recipe as Recipe | undefined;

  return (
    <div className="space-y-4 panel-enter">
      {/* Header */}
      <div className="flex items-center gap-2 pb-2 border-b border-jei-border">
        <ItemIcon itemId={calcResult.rootItem} size="lg" count={calcResult.quantity} />
        <div>
          <h2 className="text-sm font-semibold text-jei-text">
            {registry.getItemName(calcResult.rootItem)}
          </h2>
          <p className="text-[11px] text-jei-text-dim">
            ×{calcResult.quantity} — {totalOperations} opérations de craft
          </p>
        </div>
      </div>

      {/* Crafting Grid (3x3) */}
      {primaryRecipe && primaryRecipe.pattern && primaryRecipe.key && (
        <div>
          <h3 className="text-[11px] text-jei-accent font-semibold uppercase tracking-wider mb-2">
            Recette {recipeTypeLabel(primaryRecipe.type)}
          </h3>
          <div className="flex items-start gap-3">
            {/* 3×3 Grid */}
            <div className="grid grid-cols-3 gap-0.5 bg-jei-border/30 p-0.5 rounded border border-jei-border/50 w-fit">
              {renderGrid(primaryRecipe.pattern, primaryRecipe.key)}
            </div>
            {/* Arrow */}
            <div className="flex items-center h-full pt-4">
              <svg width="20" height="20" viewBox="0 0 20 16" className="text-jei-accent">
                <path d="M0 8h15M10 2l6 6-6 6" stroke="currentColor" strokeWidth="2" fill="none" />
              </svg>
            </div>
            {/* Result */}
            <div className="pt-2">
              {primaryRecipe.results.map((r, i) => (
                <div key={i} className="flex items-center gap-1">
                  <ItemIcon itemId={r.item} size="lg" count={r.count} />
                  <span className="text-[10px] text-jei-text-dim">
                    {r.count > 1 ? `×${r.count}` : ''}
                  </span>
                </div>
              ))}
            </div>
          </div>
          {/* Energy / Time info */}
          {primaryRecipe.energy && (
            <p className="text-[10px] text-jei-text-dim mt-1">
              ⚡ {(primaryRecipe.energy / 1000).toFixed(1)}k RF
              {primaryRecipe.processingTime ? `  ⏱ ${primaryRecipe.processingTime}t` : ''}
            </p>
          )}
        </div>
      )}

      {/* Simple recipe (no pattern, just ingredients list) */}
      {primaryRecipe && !primaryRecipe.pattern && primaryRecipe.ingredients.length > 0 && (
        <div>
          <h3 className="text-[11px] text-jei-accent font-semibold uppercase tracking-wider mb-2">
            Recette {recipeTypeLabel(primaryRecipe.type)}
          </h3>
          <div className="flex items-center gap-3 flex-wrap">
            {primaryRecipe.ingredients.map((ing, i) => (
              <div key={i} className="flex items-center gap-1 bg-jei-panel rounded px-2 py-1 border border-jei-border/50">
                {ing.item && <ItemIcon itemId={ing.item} size="sm" />}
                <span className="text-[10px] text-jei-text-dim">{ing.count}</span>
              </div>
            ))}
            <svg width="20" height="16" viewBox="0 0 20 16" className="text-jei-accent">
              <path d="M0 8h15M10 2l6 6-6 6" stroke="currentColor" strokeWidth="2" fill="none" />
            </svg>
            {primaryRecipe.results.map((r, i) => (
              <div key={i} className="flex items-center gap-1">
                <ItemIcon itemId={r.item} size="md" count={r.count} />
                {r.count > 1 && <span className="text-[10px] text-jei-text-dim">×{r.count}</span>}
              </div>
            ))}
          </div>
          {primaryRecipe.energy && (
            <p className="text-[10px] text-jei-text-dim mt-1">
              ⚡ {(primaryRecipe.energy / 1000).toFixed(1)}k RF
              {primaryRecipe.processingTime ? `  ⏱ ${primaryRecipe.processingTime}t` : ''}
            </p>
          )}
        </div>
      )}

      {/* Raw Materials */}
      <div>
        <h3 className="text-[11px] text-jei-accent font-semibold uppercase tracking-wider mb-2">
          Ressources de base
        </h3>
        <div className="grid grid-cols-[repeat(auto-fill,minmax(180px,1fr))] gap-2">
          {rawEntries.map(([itemName, count]) => {
            const itemId = findItemIdByName(itemName);
            return (
              <div
                key={itemName}
                className="flex items-center gap-2 bg-jei-panel rounded p-2 border border-jei-border"
              >
                {itemId && <ItemIcon itemId={itemId} size="sm" />}
                <div className="min-w-0 flex-1">
                  <div className="text-xs text-jei-text truncate">{itemName}</div>
                  <div className="text-sm font-bold text-jei-accent">
                    {count.toLocaleString()}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
        {rawEntries.length === 0 && (
          <p className="text-xs text-jei-text-dim italic">Aucune — cet item n'a pas de recette définie.</p>
        )}
      </div>

      {/* Full Material List */}
      <details className="group">
        <summary className="text-[11px] text-jei-text-dim cursor-pointer hover:text-jei-text transition-colors">
          Voir tous les matériaux (intermédiaires inclus)
        </summary>
        <div className="mt-2 space-y-1">
          {totalEntries.map(([itemName, count]) => (
            <div key={itemName} className="flex items-center justify-between text-xs px-2 py-1 hover:bg-jei-hover rounded">
              <span className="text-jei-text-dim truncate mr-2">{itemName}</span>
              <span className="text-jei-text font-mono">{count.toLocaleString()}</span>
            </div>
          ))}
        </div>
      </details>

      {/* Machine Steps */}
      {machineSteps.length > 0 && (
        <div>
          <h3 className="text-[11px] text-jei-accent font-semibold uppercase tracking-wider mb-2">
            Étapes machines
          </h3>
          <div className="space-y-2">
            {machineSteps.map((step, i) => (
              <MachineStepCard key={i} step={step} />
            ))}
          </div>
        </div>
      )}

      {/* Recipe Tree */}
      <details className="group">
        <summary className="text-[11px] text-jei-text-dim cursor-pointer hover:text-jei-text transition-colors">
          Arbre de craft complet
        </summary>
        <div className="mt-2">
          <TreeNode node={calcResult.tree} depth={0} />
        </div>
      </details>
    </div>
  );
}

function renderGrid(pattern: string[], key: Record<string, any>): React.ReactNode {
  const grid: (React.ReactNode | null)[] = [];

  for (let row = 0; row < 3; row++) {
    const patternRow = pattern[row] || '';
    for (let col = 0; col < 3; col++) {
      const char = patternRow[col] || ' ';
      const ingredient = key[char];
      if (ingredient && ingredient.item) {
        grid.push(
          <div key={`${row}-${col}`} className="bg-jei-surface w-9 h-9 flex items-center justify-center rounded border border-jei-border/30">
            <ItemIcon itemId={ingredient.item} size="sm" />
          </div>
        );
      } else {
        grid.push(
          <div key={`${row}-${col}`} className="bg-jei-surface/50 w-9 h-9 rounded border border-jei-border/10" />
        );
      }
    }
  }
  return grid;
}

function recipeTypeLabel(type: string): string {
  const labels: Record<string, string> = {
    'crafting': '🍳 Crafting',
    'smelting': '🔥 Cuisson',
    'blasting': '🔥 Fonderie',
    'mekanism:enriching': '⚡ Enrichissement',
    'mekanism:metallurgic_infusing': '⚡ Infusion',
    'mekanism:crushing': '⚡ Concassage',
    'mekanism:pigment_extracting': '⚡ Extraction',
    'create:pressing': '⚙️ Pressage',
    'create:mixing': '⚙️ Mélange',
    'ae2:inscriber': '🔧 Inscription',
    'ae2:charger': '🔋 Charge',
    'thermal:induction_smelter': '🔥 Fonte par induction',
    'ic2:compressor': '🔄 Compression',
  };
  return labels[type] || type;
}

function MachineStepCard({ step }: { step: MachineStep }) {
  return (
    <div className="machine-card">
      <div className="flex items-center justify-between mb-1.5">
        <span className="text-xs font-semibold text-jei-text">{step.machine}</span>
        <span className="text-[10px] text-jei-text-dim">
          ×{step.times} {step.energyPerOp > 0 && `| ${(step.totalEnergy / 1000).toFixed(1)}k RF`}
        </span>
      </div>
      <div className="flex items-center gap-2">
        <div className="flex items-center gap-1 flex-wrap">
          {step.inputs.map((input, i) => (
            <div key={i} className="flex items-center gap-0.5">
              <ItemIcon itemId={input.item} size="sm" />
              <span className="text-[10px] text-jei-text-dim">{input.count}</span>
            </div>
          ))}
        </div>
        <svg width="14" height="12" viewBox="0 0 20 16" className="text-jei-accent flex-shrink-0">
          <path d="M0 8h15M10 2l6 6-6 6" stroke="currentColor" strokeWidth="2" fill="none" />
        </svg>
        <div className="flex items-center gap-1 flex-wrap">
          {step.outputs.map((output, i) => (
            <div key={i} className="flex items-center gap-0.5">
              <ItemIcon itemId={output.item} size="sm" />
              <span className="text-[10px] text-jei-text-dim">{output.count}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function TreeNode({ node, depth }: { node: any; depth: number }) {
  const itemName = registry.getItemName(node.item);
  const indent = depth * 16;

  return (
    <div>
      <div
        className="flex items-center gap-1.5 py-0.5 hover:bg-jei-hover rounded px-1"
        style={{ marginLeft: indent }}
      >
        {depth > 0 && <div className="w-3 h-px bg-jei-border/30 flex-shrink-0" />}
        <ItemIcon itemId={node.item} size="sm" />
        <span className="text-[11px] text-jei-text">
          {itemName}
        </span>
        <span className="text-[10px] text-jei-accent font-mono">
          ×{node.quantity}
        </span>
        {node.isRaw && (
          <span className="text-[9px] text-jei-text-dim italic">(base)</span>
        )}
        {node.recipe && (
          <span className="text-[8px] text-jei-text-dim/50 ml-auto">{node.recipe.type}</span>
        )}
      </div>
      {node.children.map((child: any, i: number) => (
        <TreeNode key={i} node={child} depth={depth + 1} />
      ))}
    </div>
  );
}

function findItemIdByName(name: string): string | undefined {
  const all = registry.getAllItems();
  const found = all.find(i => i.name === name);
  return found?.id;
}
