from common import *
CH='13-deques-and-monotonic-queues'
F='05-sliding-maximum.md'
fmt=lambda l:"["+",".join(map(str,l))+"]"
def run(a,k):
    d=[];out=[];steps=[]
    for r,v in enumerate(a):
        exp=[]
        while d and d[0]<=r-k: exp.append(d.pop(0))
        dom=[]
        while d and a[d[-1]]<v: dom.append(d.pop())
        d.append(r)
        parts=[f"Right edge {r} brings {v}."]
        if exp: parts.append(f"Index {exp[0]} is expired and leaves the front.")
        if dom: parts.append("The value "+str(v)+" removes index "+", ".join(map(str,dom))+" from the back.")
        if not exp and not dom: parts.append("Nothing is removed.")
        if r>=k-1:
            out.append(a[d[0]]); parts.append(f"The front is index {d[0]}, so the frame ending here reads {a[d[0]]}.")
        else: parts.append("The first frame is not complete yet, so nothing is read.")
        steps.append({"at":{"right":r},"vars":{"deque":fmt(d),"output":fmt(out)},"note":" ".join(parts)})
    return steps,out
a=[8,3,5,9,2,7,7,1]
s1,out=run(a,3); assert out==[8,9,9,9,7,7] and s1[6]["vars"]["deque"]=="[5,6]" and s1[3]["vars"]["deque"]=="[3]"
fill(CH,F,block(a,["right"],s1),"@@TRACE1@@")
b=[6,5,4,3,2,1]
s2,out=run(b,3); assert out==[6,5,4,3]
fill(CH,F,block(b,["right"],s2),"@@TRACE2@@")
