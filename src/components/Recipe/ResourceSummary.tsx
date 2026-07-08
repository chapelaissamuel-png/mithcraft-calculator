import type { CalcResult, MachineStep } from '../../types';
import { registry } from '../../data/recipe-registry';
import { ItemIcon } from '../Common/ItemIcon';

interface ResourceSummaryProps {
  calcResult: CalcResult;
}

export function ResourceSummary({ calcResult }: ResourceSummaryProps) {
  const { summary, rawSummary, totalOperations, machineSteps } = calcResult;

  const rawEntries = Object.entries(rawSummary).sort(([, a], [, b]) => b - a);
  const totalEntries = Object.entries(summary).sort(([, a], [, b]) => b - a);

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

      {/* Raw Materials (base resources only) */}
      <div>
        <h3 className="text-[11px] text-jei-accent font-semibold uppercase tracking-wider mb-2">
          Ressources de base
        </h3>
        <div className="grid grid-cols-[repeat(auto-fill,minmax(180px,1fr))] gap-2">
          {rawEntries.map(([itemName, count]) => {
            // Find item ID by name
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

      {/* Full Material List (including intermediates) */}
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

      {/* Recipe Tree Summary */}
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
