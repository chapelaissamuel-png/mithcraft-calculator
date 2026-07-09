#!/usr/bin/env python3
"""Fix mekanism recipe types to match RecipeCategory"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

fname = sys.argv[1] if len(sys.argv) > 1 else "scripts/gen_mek.py"
content = open(fname).read()

replacements = {
    "'mekanism:enrichment_chamber'": "'mekanism:enriching'",
    "'mekanism:metallurgic_infuser'": "'mekanism:infusing'",
    "'mekanism:crusher'": "'mekanism:crushing'",
    "'mekanism:pressurized_reaction_chamber'": "'mekanism:reacting'",
    "'mekanism:chemical_dissolution_chamber'": "'mekanism:dissolving'",
    "'mekanism:chemical_washer'": "'mekanism:washing'",
    "'mekanism:chemical_crystallizer'": "'mekanism:crystallizing'",
    "'mekanism:chemical_injection_chamber'": "'mekanism:injecting'",
    "'mekanism:electrolytic_separator'": "'mekanism:separating'",
    "'mekanism:rotary_condensentrator'": "'mekanism:separating'",
    "'mekanism:isotopic_centrifuge'": "'mekanism:separating'",
    "'mekanism:solar_neutron_activator'": "'mekanism:reacting'",
    "'mekanism:digital_miner'": "'mekanism:enriching'",
    "'mekanism:quantum_entangloporter'": "'mekanism:infusing'",
    "'mekanism:precision_sawmill'": "'mekanism:crushing'",
    "'mekanism:combiner'": "'mekanism:combining'",
    "'mekanism:purification_chamber'": "'mekanism:enriching'",
    "'mekanism:injection_chamber'": "'mekanism:injecting'",
    "'mekanism:smelter'": "'mekanism:smelting'",
    "'mekanism:osmium_compressor'": "'mekanism:compressing'",
    "'mekanism:induction_casing'": "'crafting'",
    "'mekanism:induction_port'": "'crafting'",
}

count = 0
for old, new in replacements.items():
    c = content.count(old)
    if c > 0:
        count += c
        content = content.replace(old, new)

open(fname, 'w').write(content)
print(f"Fixed {count} type references in {fname}")
