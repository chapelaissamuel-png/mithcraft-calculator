#!/usr/bin/env python3
"""
MithCraft Recipe Generator — Base helpers
"""
from typing import List, Tuple, Optional

def ing(item: str, count: int = 1) -> str:
    if count == 1:
        return f"ing('{item}')"
    return f"ing('{item}', {count})"

def r_simple(name: str, category: str, mod: str, output_item: str,
             output_count: int, input_items: list, opts: str = "") -> str:
    outs = []
    if output_count == 1:
        outs.append(f"{{ item: '{output_item}' }}")
    else:
        outs.append(f"{{ item: '{output_item}', count: {output_count} }}")
    ins = [ing(item_id, cnt) for item_id, cnt in input_items]
    in_str = ", ".join(ins) if ins else ""
    opt_str = f", {{ {opts} }}" if opts else ""
    return f"  r('{name}', '{category}', '{mod}', [{outs[0]}], [{in_str}]{opt_str}),"

def r_shaped(name: str, mod: str, output_item: str, output_count: int,
             pattern: List[str], key_map: dict) -> str:
    outs = []
    if output_count == 1:
        outs.append(f"{{ item: '{output_item}' }}")
    else:
        outs.append(f"{{ item: '{output_item}', count: {output_count} }}")
    key_strs = [f"{k}: {v}" for k, v in key_map.items()]
    pat_str = ", ".join(f"'{p}'" for p in pattern)
    return (f"  r('{name}', 'crafting', '{mod}',\n"
            f"    [{outs[0]}],\n"
            f"    [], {{ pattern: [{pat_str}], key: {{ {', '.join(key_strs)} }} }}),")

def write_header(lines: List[str], mod_id: str):
    lines.append("import { r, ing } from './helpers';")
    lines.append("import type { Recipe } from '../../types';")
    lines.append(f"const {mod_id.upper()}: Recipe[] = [")

def write_footer(lines: List[str], var_name: str):
    lines.append("];")
    lines.append(f"export default {var_name};")
