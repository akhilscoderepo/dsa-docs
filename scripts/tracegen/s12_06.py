from common import *
CH='12-monotonic-stacks'; FILE='06-contribution-counting.md'
V=[2,5,3,5,1]; n=len(V)
def bounds(a,mx):
    L=[];R=[]
    for i in range(n):
        j=i-1
        while j>=0 and ((a[j]<=a[i]) if mx else (a[j]>=a[i])): j-=1
        L.append(j);k=i+1
        while k<n and ((a[k]<a[i]) if mx else (a[k]>a[i])): k+=1
        R.append(k)
    return L,R
def make(mx,ph,expect):
    L,R=bounds(V,mx); tot=0; steps=[]
    for i in range(n):
        s=i-L[i]; e=R[i]-i; c=V[i]*s*e; tot+=c
        steps.append({"at":{"i":i},"vars":{"left":L[i],"right":R[i],"starts":s,"ends":e,"total":tot},"note":f"Index {i} holds {V[i]} with {s} start choices and {e} end choices, so it owns {s*e} windows and adds {c}."})
    steps.append({"at":{"i":n},"vars":{"total":tot},"note":f"All {n} indices are added, and the total is {tot}."})
    assert tot==expect
    fill(CH,FILE,block(V,["i"],steps),ph)
make(False,"@@TRACE1@@",35); make(True,"@@TRACE2@@",66)
