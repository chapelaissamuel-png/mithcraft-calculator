for fname in ["gen_create.py", "gen_thermal.py", "gen_ae2.py", "gen_ic2.py"]:
    with open(fname) as f:
        content = f.read()
    import re
    # Replace the broken last lines with correct ones
    content = re.sub(
        r'rc = out\.count\("r\('\''"\)\n    print\(f"Generated.*recipes"\)\)',
        'rc = out.count("r(\'")\n    modname = "' + fname.replace("gen_", "").replace(".py", "") + '"\n    print(f"Generated {modname}.ts \u2014 {rc} recipes")',
        content
    )
    with open(fname, 'w') as f:
        f.write(content)
    print(f"Fixed {fname}")
