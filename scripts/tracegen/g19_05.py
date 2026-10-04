from common import *
CH='19-recursion-and-backtracking'; F='05-increasing-start-combinations.md'
n,k=4,2; vals=[1,2,3,4]
path=[]; res=[]; steps=[]
def pick(start):
    need=k-len(path)
    if need==0:
        res.append(list(path))
        steps.append({"at":{"start":start-1,"i":-1},"vars":{"path":str(path),"need":0,"recorded":len(res)},"note":f"The path {path} has k members, so a copy is recorded as panel {len(res)}."})
        return
    hi=n-need+1
    for i in range(start,hi+1):
        path.append(i)
        steps.append({"at":{"start":start-1,"i":i-1},"vars":{"path":str(path),"need":need-1,"recorded":len(res)},"note":f"Member {i} is picked, so the path is {path} and the next call starts at member {i+1}; this loop may run up to member {hi}."})
        pick(i+1)
        path.pop()
        steps.append({"at":{"start":start-1,"i":i-1},"vars":{"path":str(path) if path else "empty","need":need,"recorded":len(res)},"note":f"Member {i} is removed again, so the path is {path if path else 'empty'} and the loop tries the next member."})
pick(1)
assert res==[[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
fill(CH,F,block([str(v) for v in vals],["start","i"],steps),"@@TRACE1@@")
# trace 2: used marks, n=3 k=2, stop after 4 draws
n,k=3,2; vals=[1,2,3]; path=[]; used=[False]*4; seen=set(); steps=[]; draws=[0]
class Stop(Exception): pass
def draw():
    if len(path)==k:
        draws[0]+=1
        key=tuple(sorted(path)); rep=key in seen; seen.add(key)
        steps.append({"at":{"i":path[-1]-1},"vars":{"path":str(path),"repeat":"yes" if rep else "no"},"note":f"The draw {path} is complete as the panel {list(key)}, " + ("which was already recorded, so it is a repeat." if rep else "which is new, so it is kept.")})
        if draws[0]==4: raise Stop()
        return
    for m in range(1,n+1):
        if used[m]: continue
        used[m]=True; path.append(m)
        steps.append({"at":{"i":m-1},"vars":{"path":str(path),"repeat":"no"},"note":f"Member {m} is picked from anywhere in the row that is not marked, so the path is {path}."})
        draw()
        path.pop(); used[m]=False
        steps.append({"at":{"i":m-1},"vars":{"path":str(path) if path else "empty","repeat":"no"},"note":f"Member {m} is removed and unmarked, so the path is {path if path else 'empty'}."})
try: draw()
except Stop: pass
assert sum(1 for s in steps if s["vars"]["repeat"]=="yes")==1
fill(CH,F,block([str(v) for v in vals],["i"],steps),"@@TRACE2@@")
