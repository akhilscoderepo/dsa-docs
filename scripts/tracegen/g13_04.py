from common import *
CH='13-deques-and-monotonic-queues'
F='04-expired-front-eviction.md'
fmt=lambda l:"["+",".join(map(str,l))+"]"
def run(a,k):
    d=[];steps=[]
    for r,v in enumerate(a):
        exp=[]
        while d and d[0]<=r-k: exp.append(d.pop(0))
        dom=[]
        while d and a[d[-1]]<v: dom.append(d.pop())
        d.append(r)
        parts=[f"Right edge {r} brings the value {v}."]
        parts.append(f"The age test removes index {', '.join(map(str,exp))} from the front, since {r} - {k} = {r-k} and the index is at most that." if exp else f"The age test finds nothing stale, since the front is above {r-k}." if d[:-1] else "The deque is empty, so nothing can be stale.")
        parts.append(f"The value {v} removes index {', '.join(map(str,dom))} from the back." if dom else "Nothing is removed from the back.")
        parts.append(f"Index {r} is appended.")
        steps.append({"at":{"right":r},"vars":{"deque":fmt(d),"expired":len(exp),"dominated":len(dom)},"note":" ".join(parts)})
    return steps,d
a=[4,2,12,3,8,1]
s1,d=run(a,3); assert d==[4,5] and s1[5]["vars"]["expired"]==1 and s1[2]["vars"]["deque"]=="[2]" and s1[4]["vars"]["deque"]=="[2,4]"
fill(CH,F,block(a,["right"],s1),"@@TRACE1@@")
def jump(left):
    d=[];steps=[]
    for r in range(len(left)):
        d.append(r); exp=[]
        while d and d[0]<left[r]: exp.append(d.pop(0))
        note=(f"Right edge {r} appends index {r}. The legal left bound is {left[r]}, so index "+", ".join(map(str,exp))+" expire from the front." if exp else f"Right edge {r} appends index {r}. The legal left bound is {left[r]}, and the front is already legal.")
        steps.append({"at":{"right":r},"vars":{"deque":fmt(d),"bound":left[r],"expired":len(exp)},"note":note})
    return steps,d
left=[0,0,1,3,3,5]
s2,d=jump(left); assert [s["vars"]["expired"] for s in s2]==[0,0,1,2,0,2]
fill(CH,F,block(list(range(6)),["right"],s2),"@@TRACE2@@")
