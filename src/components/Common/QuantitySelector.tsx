interface QuantitySelectorProps {
  value: number;
  onChange: (val: number) => void;
}

const PRESETS = [1, 2, 4, 8, 16, 32, 64];

export function QuantitySelector({ value, onChange }: QuantitySelectorProps) {
  return (
    <div className="flex items-center gap-1">
      <span className="text-xs text-jei-text-dim mr-1">×</span>
      <input
        type="number"
        min={1}
        max={9999}
        value={value}
        onChange={e => {
          const v = parseInt(e.target.value) || 1;
          onChange(Math.max(1, Math.min(9999, v)));
        }}
        className="jei-search rounded px-2 py-1 text-sm w-16 text-center"
      />
      <div className="flex gap-0.5">
        {PRESETS.map(p => (
          <button
            key={p}
            onClick={() => onChange(p)}
            className={`text-xs px-1.5 py-1 rounded transition-colors ${
              value === p
                ? 'bg-jei-accent text-black font-bold'
                : 'bg-jei-input text-jei-text-dim hover:text-jei-text hover:bg-jei-hover'
            }`}
          >
            {p}
          </button>
        ))}
      </div>
    </div>
  );
}
