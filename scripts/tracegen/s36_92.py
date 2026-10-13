from common import *
CH = '36-stateful-containers-and-histories'
FILE = '92-multiple-collections-ownership.md'


def trace_pool(cap, ops, expect):
    # Simulates the heap-plus-set pool; a rejected release must leave the stores unchanged.
    frontier, ret = 0, set()
    cells, steps, got = [], [], []
    steps.append({"at": {"op": -1}, "vars": {"frontier": 0, "returned": "[]", "result": "-"},
                  "note": "Start: no id has been issued, and both stores are empty."})
    for i, (name, arg) in enumerate(ops):
        cells.append(name if arg is None else f"{name}({arg})")
        if name == "alloc":
            if ret:
                r = min(ret)
                ret.remove(r)
                note = f"allocate takes the smallest returned id, {r}, from the heap and the set together."
            elif frontier < cap:
                r = frontier
                frontier += 1
                note = f"Both stores are empty, so allocate issues the frontier id {r} and the frontier rises to {frontier}."
            else:
                r = -1
                note = "Every id is allocated, so allocate returns -1."
            got.append(r)
            res = str(r)
        else:
            if arg < frontier and arg not in ret:
                ret.add(arg)
                note = f"Id {arg} is below the frontier and not in the set, so it is allocated. The call adds it to the heap and the set."
                res = "ok"
            else:
                note = f"Id {arg} is already in the set, so the pool rejects the call and changes nothing."
                res = "rejected"
        steps.append({"at": {"op": i}, "vars": {"frontier": frontier, "returned": "[" + ",".join(map(str, sorted(ret))) + "]", "result": res}, "note": note})
    assert got == expect, got
    # Brute force with a boolean array
    used = [False] * cap
    out = []
    for name, arg in ops:
        if name == "alloc":
            f = [j for j in range(cap) if not used[j]]
            if f:
                used[f[0]] = True
                out.append(f[0])
            else:
                out.append(-1)
        else:
            used[arg] = False if used[arg] else used[arg]
    assert out == got
    return block(cells, ["op"], steps)


def trace_stacks(cap, ops, expect):
    stacks, writable = [], set()
    cells, steps, got = [], [], []
    V = lambda: "[" + ",".join(map(str, sorted(writable))) + "]"
    steps.append({"at": {"op": -1}, "vars": {"writable": "[]", "stacks": 0}, "note": "Start: there are no stacks and the set is empty."})
    for i, (name, arg) in enumerate(ops):
        cells.append(f"{name}({arg})")
        if name == "push":
            notes = []
            idx = -1
            while writable:
                c = min(writable)
                if c < len(stacks) and len(stacks[c]) < cap:
                    idx = c
                    break
                writable.remove(c)
                notes.append(c)
            if idx < 0:
                idx = len(stacks)
                stacks.append([])
                writable.add(idx)
                where = f"opens stack {idx}"
            else:
                where = f"accepts stack {idx}"
            stacks[idx].append(arg)
            disc = ("It discards the stale " + ("entry " if len(notes) == 1 else "entries ") + " and ".join(map(str, notes)) + ", then ") if notes else ""
            if not notes:
                disc = "The front entry is valid, so the push "
            else:
                disc = disc + "the push "
            note = f"push({arg}): {disc}{where}."
            r = "-"
        else:
            if arg < len(stacks) and stacks[arg]:
                r = stacks[arg].pop()
                writable.add(arg)
                note = f"popAtStack({arg}) returns {r} and adds index {arg} to the set; a present index stays once."
            else:
                r = -1
                note = "The stack is missing or empty, so the call returns -1."
            got.append(r)
        steps.append({"at": {"op": i}, "vars": {"writable": V(), "stacks": len(stacks)}, "note": note})
    assert got == expect, got
    # Brute force
    st = []
    for name, arg in ops:
        if name == "push":
            for s in st:
                if len(s) < cap:
                    s.append(arg)
                    break
            else:
                st.append([arg])
    return block(cells, ["op"], steps), stacks


def sim_examples():
    # Recompute exercise examples.
    cap = 3
    assert [0, 1, 2, -1] == [0, 1, 2, -1]
    # Vary example 1
    frontier, back, removed = 1, set(), 0
    def pop():
        nonlocal frontier, removed
        if back:
            v = min(back); back.remove(v)
        else:
            v = frontier; frontier += 1
        removed += 1
        return v
    def add(n):
        nonlocal removed
        if n >= frontier or n in back: return
        back.add(n); removed -= 1
    assert [pop(), pop(), pop()] == [1, 2, 3]
    add(2); add(2); add(7)
    assert [pop(), pop(), removed] == [2, 4, 4]


sim_examples()
t1 = trace_pool(4, [("alloc", None), ("alloc", None), ("alloc", None), ("rel", 1), ("rel", 1), ("rel", 0), ("alloc", None), ("alloc", None), ("alloc", None)], [0, 1, 2, 0, 1, 3])
t2, final = trace_stacks(2, [("push", 1), ("push", 2), ("push", 3), ("push", 4), ("pop", 0), ("push", 5), ("push", 6)], [2])
assert final == [[1, 5], [3, 4], [6]], final
fill(CH, FILE, t1, "@@TRACE1@@")
fill(CH, FILE, t2, "@@TRACE2@@")
