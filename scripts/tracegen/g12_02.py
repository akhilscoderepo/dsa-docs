from common import *
CH='12-monotonic-stacks'
F='02-circular-next-greater.md'

def sim(a):
    n=len(a); st=[]; ans=[-1]*n; steps=[]
    for j in range(2*n):
        p=j%n; v=a[p]; popped=[]
        while st and v>a[st[-1]]:
            t=st.pop(); ans[t]=v; popped.append(t)
        pushed=False
        if j<n:
            st.append(p); pushed=True
        lap=1 if j<n else 2
        parts=[f"Virtual index {j} reads position {p} with value {v} on lap {lap}."]
        if popped:
            parts.append("It is greater than the waiting value at position "+", ".join(map(str,popped))+f", so each receives {v}.")
        else:
            parts.append("It does not exceed the waiting top, so nothing is resolved." if st and (not pushed or len(st)>1) else "Nothing is waiting to be resolved.")
        parts.append(f"Position {p} is pushed." if pushed else "Lap two pushes nothing.")
        steps.append({"at":{"i":p},"vars":{"j":j,"stack":"["+",".join(map(str,st))+"]","answer":"["+",".join(map(str,ans))+"]"},"note":" ".join(parts)})
    return steps,ans

a=[3,8,4,1,2]
s1,r=sim(a); assert r==[8,-1,8,2,3] and len(s1)==10
assert s1[4]["vars"]["stack"]=="[1,2,4]" and s1[5]["vars"]["answer"]=="[8,-1,-1,2,3]"
fill(CH,F,block(a,["i"],s1),"@@TRACE1@@")
b=[5,1,5,3]
s2,r=sim(b); assert r==[-1,5,-1,5] and len(s2)==8
assert s2[3]["vars"]["stack"]=="[0,2,3]"
fill(CH,F,block(b,["i"],s2),"@@TRACE2@@")
