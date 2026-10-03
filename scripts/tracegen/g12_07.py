from common import *
CH='12-monotonic-stacks'
F='07-histogram-rectangles.md'
fmt=lambda l:"["+",".join(map(str,l))+"]"

def sim(h):
    n=len(h);st=[];best=0;steps=[]
    for j in range(n+1):
        v=0 if j==n else h[j]; parts=[]
        while st and h[st[-1]]>v:
            t=st.pop(); l=st[-1] if st else -1; w=j-l-1; a=h[t]*w; best=max(best,a)
            parts.append(f"Index {t} (height {h[t]}) is removed with left wall {l} and right wall {j}, so the width is {w} and the area is {a}.")
        if j<n: st.append(j)
        head=(f"The height {v} arrives." if j<n else "The closing zero arrives.")
        if not parts: parts=["Nothing is removed."]
        steps.append({"at":{"j":j},"vars":{"stack":fmt(st),"best":best},"note":head+" "+" ".join(parts)+f" The best area is {best}."})
    return steps,best
a=[3,6,2,5,4,5,1]
s1,b=sim(a); assert b==12 and len(s1)==8 and s1[6]["vars"]["best"]==12 and s1[2]["vars"]["best"]==6
fill(CH,F,block(a,["j"],s1),"@@TRACE1@@")
c=[5,5,2,5]
s2,b=sim(c); assert b==10 and s2[2]["vars"]["best"]==10
fill(CH,F,block(c,["j"],s2),"@@TRACE2@@")
