from common import *
CH='39-dynamic-query-structures'; F='02-interval-unions.md'
def fmt(m): return " ".join(f"[{s},{e})" for s,e in sorted(m.items())) or "empty"
def add(m,l,r):
    parts=[]
    left=max((s for s in m if s<=l),default=None)
    nl,nr=l,r
    if left is not None and m[left]>=l:
        parts.append(f"The floor entry [{left},{m[left]}) reaches {l}, so it merges and the start becomes {left}.")
        nl=left; nr=max(nr,m[left]); del m[left]
    else:
        parts.append(f"The floor entry does not reach {l}, so the start stays {l}.")
    ab=[s for s in sorted(m) if nl<=s<=nr]
    for s in ab:
        parts.append(f"The entry [{s},{m[s]}) starts at {s}, which is at most {nr}, so it merges.")
        nr=max(nr,m[s]); del m[s]
    if not ab: parts.append("No later entry starts inside the new range.")
    m[nl]=nr
    parts.append(f"The map stores [{nl},{nr}).")
    return " ".join(parts)
def remove(m,l,r):
    parts=[]
    for s in sorted(m):
        e=m[s]
        if s<r and e>l:
            del m[s]
            pieces=[]
            if s<l: m[s]=l; pieces.append(f"[{s},{l})")
            if e>r: m[r]=e; pieces.append(f"[{r},{e})")
            parts.append(f"The entry [{s},{e}) overlaps, so it is cut"+(" and keeps "+" and ".join(pieces) if pieces else " away completely")+".")
    if not parts: parts.append("No entry overlaps the range.")
    return " ".join(parts)
def query(m,l,r):
    f=max((s for s in m if s<=l),default=None)
    ok=f is not None and m[f]>=r
    note=(f"The floor entry [{f},{m[f]}) "+("covers" if ok else "does not reach")+f" up to {r}, so the answer is {str(ok).lower()}.") if f is not None else f"No entry starts at or before {l}, so the answer is false."
    return ok,note
def run(n,ops,point=False):
    m={}; st=[]; res=[]
    for o,l,r in ops:
        if point: l,r=l,l+1
        ok=None
        if o=='a': note=add(m,l,r); lab=f"add [{l},{r}). "
        elif o=='r': note=remove(m,l,r); lab=f"remove [{l},{r}). "
        else: ok,note=query(m,l,r); lab=f"query [{l},{r}). "
        res.append(ok)
        v={"stored":fmt(m)}
        if ok is not None: v["result"]=str(ok).lower()
        st.append({"at":{"l":l,"r":r},"vars":v,"note":lab+note})
    return st,res,m
st,res,m=run(10,[('a',v,0) for v in [1,3,2,7,6,5,4]],point=True)
assert m=={1:8}
fill(CH,F,block([str(i) for i in range(10)],["l","r"],st),"@@TRACE1@@")
st,res,m=run(12,[('a',2,6),('a',8,11),('a',6,8),('r',4,7),('q',3,5),('q',7,10),('q',2,4)])
assert m=={2:4,7:11} and res[-3:]==[False,True,True]
fill(CH,F,block([str(i) for i in range(12)],["l","r"],st),"@@TRACE2@@")
