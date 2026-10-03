from common import *
CH='12-monotonic-stacks'
F='05-duplicate-attribution-policy.md'
fmt=lambda l:"["+",".join(map(str,l))+"]"

def walls(a):
    n=len(a);L=[];R=[]
    for i in range(n):
        k=i-1
        while k>=0 and not a[k]<a[i]: k-=1
        L.append(k)
        k=i+1
        while k<n and not a[k]<=a[i]: k+=1
        R.append(k)
    return L,R
def table(a):
    L,R=walls(a); steps=[]; tot=0
    for i in range(len(a)):
        c=(i-L[i])*(R[i]-i); tot+=c
        lw="the sentinel -1" if L[i]==-1 else f"index {L[i]}"
        rw="the sentinel "+str(R[i]) if R[i]==len(a) else f"index {R[i]}"
        eq=""
        if R[i]<len(a) and a[R[i]]==a[i]: eq=" The right wall has an equal value and still stops the walk."
        steps.append({"at":{"i":i},"vars":{"left":L[i],"right":R[i],"owned":c,"total":tot},
          "note":f"Index {i} has left wall {lw} and right wall {rw}, so it has {i-L[i]} left ends and {R[i]-i} right ends and owns {c} subarrays.{eq}"})
    return steps,tot
def scan(a):
    n=len(a);st=[];right=[n]*n;steps=[]
    for j,v in enumerate(a):
        popped=[]
        while st and a[st[-1]]>=v:
            t=st.pop(); right[t]=j; popped.append(t)
        lw=st[-1] if st else -1
        st.append(j)
        note=(f"The value {v} removes index "+", ".join(map(str,popped))+f", because it is smaller or equal, so each gets right wall {j}. " if popped else f"Nothing is removed. ")
        note+=(f"The survivor is index {lw}, the strict left wall of index {j}." if lw!=-1 else f"The stack is empty, so the left wall of index {j} is -1.")
        steps.append({"at":{"j":j},"vars":{"stack":fmt(st),"right":fmt(right)},"note":note})
    return steps,right

a=[3,1,3,1]
s1,tot=table(a); assert tot==10 and [s["vars"]["owned"] for s in s1]==[1,4,1,4]
fill(CH,F,block(a,["i"],s1),"@@TRACE1@@")
b=[2,2,2]
s2,r=scan(b); assert r==[1,2,3] and s2[2]["vars"]["stack"]=="[2]"
fill(CH,F,block(b,["j"],s2),"@@TRACE2@@")
