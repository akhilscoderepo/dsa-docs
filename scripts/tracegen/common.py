import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2] / 'dsa-skills' / 'manuscripts'
def block(cells, pointers, steps):
    return "```trace\n" + json.dumps({"cells": cells, "pointers": pointers, "steps": steps}, separators=(",", ":")) + "\n```"
def fill(ch, name, trace, ph="@@TRACE@@"):
    p = ROOT / ch / name
    t = p.read_text()
    assert ph in t, "no placeholder " + ph
    p.write_text(t.replace(ph, trace, 1))
def refill(ch, name, trace, idx):
    # replace the idx-th (0-based) already filled trace block with a regenerated one
    import re
    p = ROOT / ch / name
    t = p.read_text()
    spans = [m.span() for m in re.finditer(r"```trace\n.*?\n```", t, re.S)]
    a, b = spans[idx]
    p.write_text(t[:a] + trace + t[b:])
