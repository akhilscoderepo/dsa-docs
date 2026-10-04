from common import *
CH='19-recursion-and-backtracking'; F='07-duplicate-control.md'
vals=[1,2,2]; path=[]; res=[]; steps=[]
def walk(start):
    res.append(list(path))
    steps.append({"at":{"start":start,"i":-1},"vars":{"path":str(path),"recorded":len(res)},"note":f"The call arrives with start {start} and records a copy of {path} as selection {len(res)}."})
    for i in range(start,len(vals)):
        if i>start and vals[i]==vals[i-1]:
            steps.append({"at":{"start":start,"i":i},"vars":{"path":str(path),"recorded":len(res)},"note":f"Position {i} holds {vals[i]}, the same as position {i-1} in this same loop, so it is an equal sibling and is skipped."})
            continue
        path.append(vals[i])
        note=f"Position {i} holds {vals[i]} and is taken, so the path is {path}."
        if i==start and i>0 and vals[i]==vals[i-1]:
            note=f"Position {i} holds {vals[i]}, equal to the value just taken above, but it is the first position of this loop, so it is a second copy and is taken: the path is {path}."
        steps.append({"at":{"start":start,"i":i},"vars":{"path":str(path),"recorded":len(res)},"note":note})
        walk(i+1)
        path.pop()
        steps.append({"at":{"start":start,"i":i},"vars":{"path":str(path) if path else "empty","recorded":len(res)},"note":f"The value {vals[i]} is removed, so the path is {path if path else 'empty'}."})
walk(0)
assert res==[[],[1],[1,2],[1,2,2],[2],[2,2]]
fill(CH,F,block([str(v) for v in vals],["start","i"],steps),"@@TRACE1@@")
# trace 2: wrong skip test i>0 on [2,2]
vals=[2,2]; path=[]; res=[]; steps=[]
def walk2(start):
    res.append(list(path))
    steps.append({"at":{"start":start,"i":-1},"vars":{"path":str(path),"lost":"no"},"note":f"The call arrives with start {start} and records a copy of {path}."})
    for i in range(start,len(vals)):
        if i>0 and vals[i]==vals[i-1]:
            lost = i==start
            steps.append({"at":{"start":start,"i":i},"vars":{"path":str(path),"lost":"yes" if lost else "no"},"note":(f"Position {i} equals position {i-1}, and the test i > 0 skips it, although this is the first position of the loop, so the valid pair {path+[vals[i]]} is cut off." if lost else f"Position {i} equals position {i-1} in this loop, so skipping it is right.")})
            continue
        path.append(vals[i])
        steps.append({"at":{"start":start,"i":i},"vars":{"path":str(path),"lost":"no"},"note":f"Position {i} is taken, so the path is {path}."})
        walk2(i+1)
        path.pop()
        steps.append({"at":{"start":start,"i":i},"vars":{"path":str(path) if path else "empty","lost":"no"},"note":f"The value is removed, so the path is {path if path else 'empty'}."})
walk2(0)
assert res==[[],[2]]
fill(CH,F,block([str(v) for v in vals],["start","i"],steps),"@@TRACE2@@")
