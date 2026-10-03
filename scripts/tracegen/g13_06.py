from common import *
CH='13-deques-and-monotonic-queues'
F='06-sliding-minimum.md'
fmt=lambda l:"["+",".join(map(str,l))+"]"
def run(a,k):
    d=[];out=[];steps=[]
    for r,v in enumerate(a):
        exp=[]
        while d and d[0]<=r-k: exp.append(d.pop(0))
        dom=[]
        while d and a[d[-1]]>v: dom.append(d.pop())
        d.append(r)
        parts=[f"Right edge {r} brings {v}."]
        if exp: parts.append(f"Index {exp[0]} is expired and leaves the front.")
        if dom: parts.append("The value "+str(v)+" removes index "+", ".join(map(str,dom))+" from the back because it is smaller.")
        if not exp and not dom: parts.append("Nothing is removed.")
        if r>=k-1: out.append(a[d[0]]); parts.append(f"The front is index {d[0]}, so the frame reads {a[d[0]]}.")
        else: parts.append("The first frame is not complete yet.")
        steps.append({"at":{"right":r},"vars":{"deque":fmt(d),"output":fmt(out)},"note":" ".join(parts)})
    return steps,out
a=[7,4,5,2,9,4,6]
s1,out=run(a,3); assert out==[4,2,2,2,4] and s1[6]["vars"]["deque"]=="[5,6]" and s1[3]["vars"]["deque"]=="[3]"
fill(CH,F,block(a,["right"],s1),"@@TRACE1@@")
def lim(a,limit):
    hi=[];lo=[];left=0;best=0;steps=[]
    for r,v in enumerate(a):
        while hi and a[hi[-1]]<v: hi.pop()
        while lo and a[lo[-1]]>v: lo.pop()
        hi.append(r); lo.append(r)
        moved=0
        while a[hi[0]]-a[lo[0]]>limit:
            left+=1; moved+=1
            if hi[0]<left: hi.pop(0)
            if lo[0]<left: lo.pop(0)
        best=max(best,r-left+1)
        rng=a[hi[0]]-a[lo[0]]
        note=f"Index {r} (value {v}) joins both deques. "+(f"The range was above {limit}, so the left pointer moves forward {moved} step(s) to {left}, expiring fronts that fall behind it. " if moved else "The range is within the limit, so the left pointer stays. ")+f"The window covers indices {left} to {r} with range {rng}, and the best length is {best}."
        steps.append({"at":{"left":left,"right":r},"vars":{"max_deque":fmt(hi),"min_deque":fmt(lo),"range":rng,"best":best},"note":note})
    return steps,best
b=[5,8,6,7,2,9,4]
s2,best=lim(b,3); assert best==4
fill(CH,F,block(b,["left","right"],s2),"@@TRACE2@@")
