from common import *
CH='12-monotonic-stacks'
F='08-stack-and-contribution-counting.md'
fmt=lambda l:"["+",".join(map(str,l))+"]"

def role(a,mx):
    n=len(a);st=[];right=[n]*n;left=[0]*n;steps=[];owned=[0]*n
    done=[False]*n
    for j in range(n+1):
        popped=[]
        while st and (j==n or ((a[st[-1]]<=a[j]) if mx else (a[st[-1]]>=a[j]))):
            t=st.pop(); right[t]=j; popped.append(t)
            l=st[-1] if st else -1
            left[t]=l; owned[t]=(t-l)*(j-t)
        if j<n:
            st.append(j)
        head=(f"The reading {a[j]} arrives." if j<n else "The closing step arrives.")
        if popped:
            body=" ".join(f"Index {t} leaves with left wall {left[t]} and right wall {right[t]}, so it owns {owned[t]}." for t in popped)
        else: body="Nothing leaves the stack."
        steps.append({"at":{"j":j},"vars":{"stack":fmt(st),"owned":fmt(owned)},"note":head+" "+body})
    return steps,owned
a=[2,5,3,5]
s1,o=role(a,False); assert o==[4,1,4,1] and sum(o)==10
fill(CH,F,block(a,["j"],s1),"@@TRACE1@@")
s2,o=role(a,True); assert o==[1,4,1,4] and sum(o)==10
assert sum(x*y for x,y in zip(a,o))-sum(x*y for x,y in zip(a,[4,1,4,1]))==15
fill(CH,F,block(a,["j"],s2),"@@TRACE2@@")
