import { useState, useCallback, useMemo } from 'react';
import type { CalcResult } from '../types';
import { calculateItem } from '../engine/calculator';

export function useCalculator() {
  const [calcResult, setCalcResult] = useState<CalcResult | null>(null);
  const [isCalculating, setIsCalculating] = useState(false);
  const [selectedItem, setSelectedItem] = useState<string | null>(null);
  const [quantity, setQuantity] = useState(1);

  const calculate = useCallback((itemId: string, qty: number = quantity) => {
    setIsCalculating(true);
    try {
      // Use setTimeout to keep UI responsive
      setTimeout(() => {
        const result = calculateItem(itemId, qty);
        setCalcResult(result);
        setSelectedItem(itemId);
        setIsCalculating(false);
      }, 0);
    } catch (err) {
      console.error('Calculation error:', err);
      setIsCalculating(false);
    }
  }, [quantity]);

  const compute = useCallback((itemId: string, qty: number) => {
    setQuantity(qty);
    calculate(itemId, qty);
  }, [calculate]);

  const clear = useCallback(() => {
    setCalcResult(null);
    setSelectedItem(null);
  }, []);

  // Memoized summary for display
  const rawMaterials = useMemo(() => {
    if (!calcResult) return [];
    return Object.entries(calcResult.rawSummary)
      .sort(([, a], [, b]) => b - a)
      .map(([item, count]) => ({ item, count }));
  }, [calcResult]);

  const totalOperations = calcResult?.totalOperations ?? 0;
  const machineSteps = calcResult?.machineSteps ?? [];

  return {
    calcResult,
    isCalculating,
    selectedItem,
    quantity,
    setQuantity,
    calculate: compute,
    clear,
    rawMaterials,
    totalOperations,
    machineSteps,
  };
}
