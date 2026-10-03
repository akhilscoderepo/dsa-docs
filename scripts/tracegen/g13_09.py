from common import *
CH='13-deques-and-monotonic-queues'
F='09-deque-and-sliding-window.md'
fmt=lambda l:"["+",".join(map(str,l))+"]"
def fixed(a,k):
    d=[];out=[];steps=[]
    for r,v in enumerate(a):
        exp=[];dom=[]
        while d and d[0]<=r-k: exp.append(d.pop(0))
        while d and a[d[-1]]<v: dom.append(d.pop())
        d.append(r)
        p=[f"Edge {r} brings {v}."]
        p.append(("The expiry pass removes index "+", ".join(map(str,exp))+" from the front.") if exp else "The expiry pass removes nothing.")
        p.append(("The domination pass removes index "+", ".join(map(str,dom))+" from the back.") if dom else "The domination pass removes nothing.")
        if r>=k-1: out.append(a[d[0]]); p.append(f"The front is index {d[0]}, so the window reads {a[d[0]]}.")
        else: p.append("The first window is not complete.")
        steps.append({"at":{"right":r},"vars":{"deque":fmt(d),"output":fmt(out)},"note":" ".join(p)})
    return steps,out
a=[6,1,4,4,2,9,3];k=3
s1,out=fixed(a,k); assert out==[6,4,4,9,9]
fill(CH,F,block(a,["right"],s1),"@@TRACE1@@")
def calm(a,limit):
    hi=[];lo=[];left=0;total=0;steps=[]
    for r,v in enumerate(a):
        while hi and a[hi[-1]]<v: hi.pop()
        while lo and a[lo[-1]]>v: lo.pop()
        hi.append(r);lo.append(r)
        moved=0
        while a[hi[0]]-a[lo[0]]>limit:
            left+=1;moved+=1
            if hi[0]<left: hi.pop(0)
            if lo[0]<left: lo.pop(0)
        total+=r-left+1
        note=f"Edge {r} brings {v}. "+(f"The range exceeds {limit}, so the left pointer moves {moved} step(s) to {left}. " if moved else "The range is within the limit. ")+f"The window {left} to {r} adds {r-left+1} calm subarrays ending here, for a total of {total}."
        steps.append({"at":{"left":left,"right":r},"vars":{"max_deque":fmt(hi),"min_deque":fmt(lo),"total":total},"note":note})
    return steps,total
b=[2,4,3,7,5]
s2,t=calm(b,2); assert t==9
fill(CH,F,block(b,["left","right"],s2),"@@TRACE2@@")
