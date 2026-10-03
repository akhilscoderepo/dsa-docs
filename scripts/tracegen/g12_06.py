from common import *
CH='12-monotonic-stacks'
F='06-contribution-counting.md'
fmt=lambda l:"["+",".join(map(str,l))+"]"

def sim(a):
    n=len(a);st=[];tot=0;steps=[]
    for j in range(n+1):
        v=None if j==n else a[j]
        parts=[]
        while st and (v is None or a[st[-1]]>=v):
            t=st.pop(); l=st[-1] if st else -1
            c=a[t]*(t-l)*(j-t); tot+=c
            parts.append(f"Index {t} leaves with left wall {l} and right wall {j}, so it owns {t-l} times {j-t} stretches and contributes {a[t]} times {(t-l)*(j-t)}, which is {c}.")
        if j<n: st.append(j)
        head=(f"The value {v} arrives." if j<n else "The flush step arrives, lower than every value.")
        if not parts: parts=["Nothing leaves the stack."]
        steps.append({"at":{"j":j},"vars":{"stack":fmt(st),"total":tot},"note":head+" "+" ".join(parts)+f" The total is {tot}."})
    return steps,tot
a=[3,1,2,4]
s1,t=sim(a); assert t==17 and len(s1)==5 and s1[4]["vars"]["total"]==17 and s1[1]["vars"]["total"]==3
fill(CH,F,block(a,["j"],s1),"@@TRACE1@@")
b=[2,9,3,3]
s2,t=sim(b); assert t==32 and s2[2]["vars"]["total"]==9 and s2[3]["vars"]["total"]==15
fill(CH,F,block(b,["j"],s2),"@@TRACE2@@")
