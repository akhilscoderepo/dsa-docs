from common import *
CH='12-monotonic-stacks'; FILE='02-circular-next-greater.md'
def fmt(l): return "["+", ".join(map(str,l))+"]"
def run(vals):
    n=len(vals); st=[]; ans=[None]*n; steps=[]
    show=lambda: "["+", ".join("." if a is None else str(a) for a in ans)+"]"
    for p in range(2*n):
        i=p%n; v=vals[i]
        while st and vals[st[-1]]<v:
            t=st.pop(); ans[t]=v
            steps.append({"at":{"i":i},"vars":{"p":p,"stack":fmt(st),"ans":show()},"note":f"Position {p} reads {v}, which is greater than nums[{t}] = {vals[t]}. Index {t} gets the answer {v} and leaves the stack."})
        if p<n:
            st.append(i); note=f"Position {p} pushes index {i} with value {v}."
        else:
            note=f"Position {p} reads {v} and pushes nothing."
        steps.append({"at":{"i":i},"vars":{"p":p,"stack":fmt(st),"ans":show()},"note":note})
    steps.append({"at":{"i":n},"vars":{"p":2*n,"stack":fmt(st),"ans":show()},"note":f"Both passes end. Indices {fmt(st)} keep -1."})
    return [-1 if a is None else a for a in ans],steps
V=[3,8,4,1,2]; a,s=run(V); assert a==[8,-1,8,2,3]; fill(CH,FILE,block(V,["i"],s),"@@TRACE1@@")
V=[1,2,3,2,1]; a,s=run(V); assert a==[2,3,-1,3,2]; fill(CH,FILE,block(V,["i"],s),"@@TRACE2@@")
