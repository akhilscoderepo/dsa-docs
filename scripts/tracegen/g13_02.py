from common import *
CH='13-deques-and-monotonic-queues'
F='02-front-and-back-invariants.md'
fmt=lambda l:"["+",".join(map(str,l))+"]"
def run(a,mx):
    d=[];steps=[]
    for i,v in enumerate(a):
        rem=[]
        while d and ((d[-1]<v) if mx else (d[-1]>v)):
            rem.append(d.pop())
        d.append(v)
        kind="smaller" if mx else "larger"
        if rem: note=f"The value {v} removes {', '.join(map(str,rem))} from the back, because "+("they are" )+f" strictly {kind}. Then {v} is appended."
        else: note=f"The back is not strictly {kind} than {v}, or the deque is empty, so nothing is removed and {v} is appended."
        steps.append({"at":{"i":i},"vars":{"deque":fmt(d),"front":d[0]},"note":note})
    return steps,d
a=[4,2,7,3,3,1,6]
s1,d=run(a,True); assert d==[7,6] and s1[2]["vars"]["deque"]=="[7]"
fill(CH,F,block(a,["i"],s1),"@@TRACE1@@")
b=[5,3,8,2,2,7]
s2,d=run(b,False); assert d==[2,2,7] and s2[3]["vars"]["deque"]=="[2]"
fill(CH,F,block(b,["i"],s2),"@@TRACE2@@")
