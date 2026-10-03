from common import *
CH='13-deques-and-monotonic-queues'
F='03-dominated-back-eviction.md'
fmt=lambda l:"["+",".join(map(str,l))+"]"
def run(a,mx):
    d=[];steps=[]
    for i,v in enumerate(a):
        rem=[]
        while d and ((a[d[-1]]<v) if mx else (a[d[-1]]>v)): rem.append(d.pop())
        d.append(i)
        word="beaten" if mx else "dominated"
        if rem: note=f"Index {i} (value {v}) removes index "+", ".join(map(str,rem))+f" from the back, since each has a value that {i} outlasts and beats. Then index {i} is appended."
        else: note=f"Index {i} (value {v}) beats nothing at the back, so it is appended and nothing is removed."
        steps.append({"at":{"i":i},"vars":{"deque":fmt(d),"front_value":a[d[0]],"removed":len(rem)},"note":note})
    return steps,d
a=[5,3,4,4,2,6]
s1,d=run(a,True); assert d==[5] and s1[5]["vars"]["removed"]==4 and s1[2]["vars"]["deque"]=="[0,2]"
fill(CH,F,block(a,["i"],s1),"@@TRACE1@@")
b=[4,6,2,5,5,1]
s2,d=run(b,False); assert d==[5] and s2[2]["vars"]["deque"]=="[2]" and s2[5]["vars"]["removed"]==3
fill(CH,F,block(b,["i"],s2),"@@TRACE2@@")
