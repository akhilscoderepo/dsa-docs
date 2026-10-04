from common import *
CH='21-graph-traversal-models-dfs-and-ordinary-bfs'
F='06-path-enumeration.md'
trails=[[1,2],[3],[3,4],[],[]]; TO=3
def fmt(p): return ">".join(map(str,p)) or "empty"
# trace 1: correct walk, steps on enter and on return
path=[0]; found=[]; steps=[]
def snap(): return " | ".join(fmt(p) for p in found) or "none"
def walk(h):
    if h==TO:
        found.append(list(path))
        steps.append({"at":{"hut":h},"vars":{"path":fmt(path),"found":len(found),"cards":snap()},
          "note":f"Hut {h} is the target, so a copy of the working path {fmt(path)} is stored as card {len(found)}."})
        return
    if not trails[h]:
        steps.append({"at":{"hut":h},"vars":{"path":fmt(path),"found":len(found),"cards":snap()},
          "note":f"Hut {h} has no trails and is not the target, so the call returns with nothing stored."})
        return
    for nx in trails[h]:
        path.append(nx)
        if nx!=TO and trails[nx] or nx==TO or True:
            pass
        walk(nx)
        path.pop()
        steps.append({"at":{"hut":h},"vars":{"path":fmt(path),"found":len(found),"cards":snap()},
          "note":f"Back at hut {h}, the undo step removes hut {nx}, leaving the working path {fmt(path)}."})
steps.append({"at":{"hut":0},"vars":{"path":"0","found":0,"cards":"none"},"note":"The walk starts at hut 0 with the working path holding only that hut."})
walk(0)
assert sorted(found)==[[0,1,3],[0,2,3]] and path==[0]
fill(CH,F,block([0,1,2,3,4],["hut"],steps),"@@TRACE1@@")
# trace 2: global visited false friend
used=set(); path=[0]; found=[]; steps=[]
def walk2(h):
    used.add(h)
    if h==TO:
        found.append(list(path))
        steps.append({"at":{"hut":h},"vars":{"path":fmt(path),"found":len(found),"used":",".join(map(str,sorted(used)))},
          "note":f"Hut {h} is the target and is marked used, and card {len(found)} is stored as {fmt(path)}."})
        return
    steps.append({"at":{"hut":h},"vars":{"path":fmt(path),"found":len(found),"used":",".join(map(str,sorted(used)))},
      "note":f"Hut {h} is entered and marked used."})
    for nx in trails[h]:
        if nx in used:
            steps.append({"at":{"hut":h},"vars":{"path":fmt(path),"found":len(found),"used":",".join(map(str,sorted(used)))},
              "note":f"At hut {h}, the trail to hut {nx} is skipped because hut {nx} is already marked used, so a valid route is lost."})
            continue
        path.append(nx); walk2(nx); path.pop()
walk2(0)
steps.append({"at":{"hut":-1},"vars":{"path":"0","found":len(found),"used":",".join(map(str,sorted(used)))},
  "note":f"The walk ends with {len(found)} card, while the correct answer from the first trace is 2."})
assert len(found)==1 and found==[[0,1,3]]
fill(CH,F,block([0,1,2,3,4],["hut"],steps),"@@TRACE2@@")
