from common import *
CH='12-monotonic-stacks'
F='91-count-subarrays-from-stack-boundaries.md'
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
            body=" ".join(f"Index {t} leaves with left boundary {left[t]} and right boundary {right[t]}, so it owns {owned[t]}." for t in popped)
        else: body="Nothing leaves the stack."
        steps.append({"at":{"j":j},"vars":{"stack":fmt(st),"owned":fmt(owned)},"note":head+" "+body})
    return steps,owned
a=[3,5,3,4]
def brute(a,mx):
    n=len(a);o=[0]*n
    for i in range(n):
        for j in range(i,n):
            w=a[i:j+1];e=max(w) if mx else min(w)
            o[max(k for k in range(i,j+1) if a[k]==e)]+=1
    return o
s1,o=role(a,False); assert o==brute(a,False)==[2,1,6,1] and sum(x*y for x,y in zip(a,o))==33
fill(CH,F,block(a,["j"],s1),"@@TRACE1@@")
s2,o2=role(a,True); assert o2==brute(a,True)==[1,6,1,2] and sum(x*y for x,y in zip(a,o2))==44
fill(CH,F,block(a,["j"],s2),"@@TRACE2@@")
