from common import *
CH='39-dynamic-query-structures'; F='91-ordered-interval-state.md'
def fmt(runs): return " ".join(f"[{s},{e})" for s,e in runs) or "empty"

# ---- trace 1: sorted run array with explicit predecessor search ----
def first_start_above(runs,x):
    lo,hi=0,len(runs)
    while lo<hi:
        mid=(lo+hi)//2
        if runs[mid][0]>x: hi=mid
        else: lo=mid+1
    return lo
def run_add(runs,l,r):
    j=first_start_above(runs,r); i=j
    while i>0 and runs[i-1][1]>=l: i-=1
    s,e=l,r
    if i<j: s=min(s,runs[i][0]); e=max(e,runs[j-1][1])
    absorbed=runs[i:j]
    runs[i:j]=[(s,e)]
    if not absorbed: note=f"The search returns index {j}, and no run on its left reaches {l}, so no stored run is touched. The new range becomes its own run."
    else: note=f"The search returns index {j}, and the walk to the left stops at index {i}. The {len(absorbed)} run(s) {fmt(absorbed)} touch or overlap the range, so they fuse with it into [{s},{e})."
    return note
def run_remove(runs,l,r):
    j=first_start_above(runs,r-1); i=j
    while i>0 and runs[i-1][1]>l: i-=1
    if i==j: return f"The search returns index {j}, and no run reaches past {l}, so nothing is cut."
    old=runs[i:j]; keep=[]
    if old[0][0]<l: keep.append((old[0][0],l))
    if old[-1][1]>r: keep.append((r,old[-1][1]))
    runs[i:j]=keep
    return f"The search returns index {j}, and the walk to the left stops at index {i}. The run(s) {fmt(old)} overlap the cut, so the array keeps "+(fmt(keep) if keep else "no piece")+"."
def trace1(ops):
    runs=[]; st=[]
    for o,l,r in ops:
        note=run_add(runs,l,r) if o=='a' else run_remove(runs,l,r)
        cov=sum(e-s for s,e in runs)
        st.append({"at":{"l":l,"r":r},"vars":{"call":("add" if o=='a' else "remove")+f"({l},{r})","runs":fmt(runs),"covered":cov},"note":("add" if o=='a' else "remove")+f" [{l},{r}). "+note})
    return st,runs
st,runs=trace1([('a',2,6),('a',9,12),('a',6,9),('r',4,10),('a',14,16),('r',3,15)])
assert runs==[(2,3),(15,16)], runs
fill(CH,F,block([str(i) for i in range(16)],["l","r"],st),"@@TRACE1@@")

# ---- trace 2: dynamic segment tree, nodes created only on touched paths ----
class N:
    def __init__(s): s.l=s.r=None; s.c=0
def live(n): return 0 if n is None else 1+live(n.l)+live(n.r)
def tadd(n,lo,hi,l,r,ev):
    size=hi-lo
    if n.c==size: ev.append(f"[{lo},{hi}) is already full, so the call stops there.") ; return
    if l<=lo and hi<=r:
        dropped=live(n.l)+live(n.r)
        n.c=size; n.l=n.r=None
        ev.append(f"[{lo},{hi}) lies inside the range, so it becomes full"+(f" and drops {dropped} node(s) below it." if dropped else "."))
        return
    mid=lo+(hi-lo)//2
    if n.l is None: n.l=N(); n.r=N()
    if l<mid: tadd(n.l,lo,mid,l,r,ev)
    if r>mid: tadd(n.r,mid,hi,l,r,ev)
    n.c=n.l.c+n.r.c
def trace2(ops,lim):
    root=N(); st=[]
    for l,r in ops:
        ev=[]; tadd(root,0,lim,l,r,ev)
        st.append({"at":{"l":l,"r":r},"vars":{"call":f"add({l},{r})","covered":root.c,"nodes":live(root)},"note":f"add [{l},{r}). "+" ".join(ev)+f" The tree now holds {live(root)} node(s) and the covered count is {root.c}."})
    return st,root
st,root=trace2([(1,3),(4,8),(2,6),(8,12),(0,16)],16)
assert root.c==16 and live(root)==1
fill(CH,F,block([str(i) for i in range(16)],["l","r"],st),"@@TRACE2@@")
