from common import *
CH = '23-directed-graphs-and-union-find'; F = '04-find-compression.md'

def run(parent, queries):
    parent = list(parent); steps = []
    ps = lambda: "-".join(map(str, parent))
    for x in queries:
        root = x; walked = 0
        steps.append({"at": {"cur": x}, "vars": {"parents": ps(), "phase": "walk", "root": "unknown"}, "note": f"The call find({x}) starts its first pass at machine {x}."})
        while parent[root] != root:
            nxt = parent[root]
            walked += 1
            steps.append({"at": {"cur": nxt}, "vars": {"parents": ps(), "phase": "walk", "root": "unknown"}, "note": f"Machine {root} links to machine {nxt}, so the walk moves there. Links followed so far: {walked}."})
            root = nxt
        steps[-1]["vars"]["root"] = root
        steps[-1]["note"] += f" Machine {root} links to itself, so it is the root."
        cur = x
        while parent[cur] != root:
            nxt = parent[cur]
            parent[cur] = root
            steps.append({"at": {"cur": cur}, "vars": {"parents": ps(), "phase": "rewrite", "root": root}, "note": f"The second pass sets the link of machine {cur} to root {root} and then moves to machine {nxt}."})
            cur = nxt
        steps.append({"at": {"cur": cur}, "vars": {"parents": ps(), "phase": "rewrite", "root": root}, "note": f"Machine {cur} already links to root {root}, so the second pass stops. The call returns {root} after {walked} links."})
    return parent, steps

p1, s1 = run([0,0,1,2,3], [4])
assert p1 == [0,0,0,0,0]
fill(CH, F, block(list(range(5)), ["cur"], s1), "@@TRACE1@@")
p2, s2 = run([0,0,1,2,3,3,4], [6, 5])
assert p2 == [0,0,0,0,0,0,0] or True
assert p2 == [0,0,0,0,0,0,0]
fill(CH, F, block(list(range(7)), ["cur"], s2), "@@TRACE2@@")
