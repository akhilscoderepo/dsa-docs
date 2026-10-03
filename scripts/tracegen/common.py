import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2] / 'dsa-skills' / 'manuscripts'
def block(cells, pointers, steps):
    return "```trace\n" + json.dumps({"cells": cells, "pointers": pointers, "steps": steps}, separators=(",", ":")) + "\n```"
def fill(ch, name, trace, ph="@@TRACE@@"):
    p = ROOT / ch / name
    t = p.read_text()
    assert ph in t, "no placeholder " + ph
    p.write_text(t.replace(ph, trace, 1))
