from common import *
CH='19-recursion-and-backtracking'; F='02-choose-explore-unchoose.md'
# trace 1: options ab, c, de with one shared path
options=["ab","c","de"]; path=[]; res=[]; steps=[]
def rec(d):
    if d==len(options):
        res.append("".join(path))
        steps.append({"at":{"depth":d},"vars":{"path":"".join(path),"stored":len(res)},"note":f"Every course is decided, so a copy of the path is stored as menu {len(res)}, reading {''.join(path)}."})
        return
    for ch in options[d]:
        path.append(ch)
        steps.append({"at":{"depth":d},"vars":{"path":"".join(path),"stored":len(res)},"note":f"The course at depth {d} puts {ch} on the path, which now reads {''.join(path)}."})
        rec(d+1)
        path.pop()
        steps.append({"at":{"depth":d},"vars":{"path":"".join(path) or "empty","stored":len(res)},"note":f"Everything below {ch} is finished, so {ch} is lifted and the path reads {''.join(path) or 'nothing'} again."})
rec(0)
assert res==["acd","ace","bcd","bce"]
fill(CH,F,block(options,["depth"],steps),"@@TRACE1@@")
# trace 2: climbing 3 stairs, stored by reference (aliasing bug)
cells=["1","2"]; path=[]; res=[]; steps=[]
def snap(): return str([list(r) for r in res])
def climb(left):
    if left==0:
        res.append(path)  # aliasing on purpose
        steps.append({"at":{"pick":-1},"vars":{"path":str(path),"stored":snap()},"note":"The stairs are used up, and the working list itself is stored, with no copy, as result "+str(len(res))+"."})
        return
    for k,s in enumerate((1,2)):
        if s>left: continue
        path.append(s)
        steps.append({"at":{"pick":k},"vars":{"path":str(path),"stored":snap()},"note":f"A step of {s} goes on the path, leaving {left-s} stairs."})
        climb(left-s)
        path.pop()
        steps.append({"at":{"pick":k},"vars":{"path":str(path),"stored":snap()},"note":f"The step of {s} is lifted, and every stored result that is this same list changes with it."})
climb(3)
assert all(r==[] for r in res) and len(res)==3
steps.append({"at":{"pick":-1},"vars":{"path":str(path),"stored":snap()},"note":"The search is over and the path is empty, so all three stored results are the same empty list."})
fill(CH,F,block(cells,["pick"],steps),"@@TRACE2@@")
