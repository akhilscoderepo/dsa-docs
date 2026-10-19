from common import *
CH = '41-algorithmic-services-and-simulations'; F = '92-several-indexes-in-step.md'

def run(calls):
    items = {}
    cells, steps = [], []
    def view():
        low = sorted(items.values(), key=lambda r: (r[2], r[0]))
        tot = {}
        for _, a, q in items.values():
            tot[a] = tot.get(a, 0) + q
        return (" ".join(f"{s}:{q}" for s, _, q in low) or "empty",
                " ".join(f"{a}={t}" for a, t in sorted(tot.items())) or "empty")
    for n, (op, a) in enumerate(calls):
        cells.append(f"{op}({','.join(map(str, a))})")
        ok, note = True, ""
        if op == "receive":
            s, ar, k = a
            if s in items:
                _, ar0, q = items[s]; items[s] = (s, ar0, q + k)
                note = f"Call {n}: {s} exists in {ar0}, so replace swaps the old record for one with {q + k} units."
            else:
                items[s] = (s, ar, k); note = f"Call {n}: replace inserts the new record {s} with {k} units into {ar}."
        elif op == "ship":
            s, k = a
            if s not in items or items[s][2] < k:
                ok = False; note = f"Call {n}: the check fails before any write, so all three structures stay as they were."
            else:
                _, ar, q = items[s]
                if q == k:
                    del items[s]; note = f"Call {n}: all {k} units leave, so replace removes {s} from every structure."
                else:
                    items[s] = (s, ar, q - k); note = f"Call {n}: replace swaps the record of {s} for one with {q - k} units."
        else:
            s, ar = a
            if s not in items or items[s][1] == ar:
                ok = False; note = f"Call {n}: the check fails before any write, so all three structures stay as they were."
            else:
                _, ar0, q = items[s]; items[s] = (s, ar, q)
                note = f"Call {n}: replace moves {q} units of {s} from {ar0} to {ar} in the table, the set and the totals."
        low, tot = view()
        steps.append({"at": {"call": n}, "vars": {"lowest": low, "totals": tot, "result": "true" if ok else "false"}, "note": note})
    return cells, steps, items

c, s, it = run([("receive", ("a", "A1", 5)), ("receive", ("b", "A1", 2)), ("receive", ("c", "A2", 4)),
                ("transfer", ("b", "A2")), ("ship", ("b", 2))])
assert it == {"a": ("a", "A1", 5), "c": ("c", "A2", 4)}
assert s[3]["vars"]["totals"] == "A1=5 A2=6"
fill(CH, F, block(c, ["call"], s), "@@TRACE1@@")
c, s, it = run([("receive", ("x", "A1", 3)), ("receive", ("y", "A1", 3)), ("ship", ("x", 5)), ("ship", ("x", 3)),
                ("transfer", ("y", "A1")), ("transfer", ("z", "A2"))])
assert [x["vars"]["result"] for x in s] == ["true", "true", "false", "true", "false", "false"]
assert s[-1]["vars"]["totals"] == "A1=3"
fill(CH, F, block(c, ["call"], s), "@@TRACE2@@")
