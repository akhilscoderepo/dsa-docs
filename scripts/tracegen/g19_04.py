from common import *
CH='19-recursion-and-backtracking'; F='04-permutations.md'
g=[1,2,3]
def ms(used): return "".join("T" if u else "F" for u in used)
# trace 1: used marks, stop after third arrangement
path=[]; used=[False]*3; res=[]; steps=[]
class Stop(Exception): pass
def rec(d):
    if d==3:
        res.append(list(path))
        steps.append({"at":{"depth":d,"i":-1},"vars":{"path":str(path),"used":ms(used)},"note":f"All three chairs are filled, so a copy of {path} is recorded as arrangement {len(res)}."})
        if len(res)==3: raise Stop()
        return
    for i in range(3):
        if used[i]: continue
        used[i]=True; path.append(g[i])
        steps.append({"at":{"depth":d,"i":i},"vars":{"path":str(path),"used":ms(used)},"note":f"Guest {g[i]} is offered for chair {d}, so index {i} is marked and the path is {path}."})
        rec(d+1)
        path.pop(); used[i]=False
        steps.append({"at":{"depth":d,"i":i},"vars":{"path":str(path),"used":ms(used)},"note":f"Guest {g[i]} leaves chair {d}, so index {i} is cleared and the path is {path or 'empty'}."})
try: rec(0)
except Stop: pass
assert res==[[1,2,3],[1,3,2],[2,1,3]]
fill(CH,F,block([str(x) for x in g],["depth","i"],steps),"@@TRACE1@@")
# trace 2: swapping, stop after third arrangement
a=[1,2,3]; res=[]; steps=[]
def sw(pos):
    if pos==3:
        res.append(list(a))
        steps.append({"at":{"pos":pos,"j":-1},"vars":{"array":str(a)},"note":f"Every chair is filled, so a copy of {a} is recorded as arrangement {len(res)}."})
        if len(res)==3: raise Stop()
        return
    for j in range(pos,3):
        a[pos],a[j]=a[j],a[pos]
        steps.append({"at":{"pos":pos,"j":j},"vars":{"array":str(a)},"note":f"Position {pos} swaps with position {j}, so the seated front of the array is now {a[:pos+1]}."})
        sw(pos+1)
        a[pos],a[j]=a[j],a[pos]
        steps.append({"at":{"pos":pos,"j":j},"vars":{"array":str(a)},"note":f"The swap of positions {pos} and {j} is reversed, so the array reads {a} again."})
try: sw(0)
except Stop: pass
assert res==[[1,2,3],[1,3,2],[2,1,3]]
fill(CH,F,block([str(x) for x in g],["pos","j"],steps),"@@TRACE2@@")
