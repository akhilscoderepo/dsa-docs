from common import *
CH='12-monotonic-stacks'; FILE='05-duplicate-attribution-policy.md'
def fmt(l): return "["+", ".join(map(str,l))+"]"
sh=lambda a:"["+", ".join("." if x is None else str(x) for x in a)+"]"
V=[3,2,2,4,2,5]; n=len(V); st=[]; L=[None]*n; R=[None]*n; steps=[]
for i,v in enumerate(V):
    while st and V[st[-1]]>=v:
        t=st.pop(); R[t]=i
        steps.append({"at":{"i":i},"vars":{"stack":fmt(st),"left":sh(L),"right":sh(R)},"note":f"nums[{t}] = {V[t]} is at least {v}, so right[{t}] = {i} and index {t} leaves the stack."})
    L[i]=st[-1] if st else -1; st.append(i)
    steps.append({"at":{"i":i},"vars":{"stack":fmt(st),"left":sh(L),"right":sh(R)},"note":f"The surviving top gives left[{i}] = {L[i]}, and index {i} goes on the stack."})
for t in st: R[t]=n
own=[(i-L[i])*(R[i]-i) for i in range(n)]
steps.append({"at":{"i":n},"vars":{"stack":fmt(st),"left":sh(L),"right":sh(R),"owned":fmt(own)},"note":f"The scan ends. The remaining indices get right = {n}, and owned[i] = (i - left) * (right - i) gives {fmt(own)}."})
assert own==[1,2,6,1,10,1] and sum(own)==21; fill(CH,FILE,block(V,["i"],steps),"@@TRACE1@@")
V=[2,2,2]; n=3; steps=[]; c=[0]*n
for l in range(n):
    for r in range(l,n):
        c[r]+=1  # all ties: rightmost minimum is r
        steps.append({"at":{"l":l,"r":r},"vars":{"owner":r,"credits":fmt(c)},"note":f"The window from {l} to {r} holds only 2s, so its rightmost minimum is index {r}, and index {r} gets one credit."})
assert c==[1,2,3] and sum(c)==6; fill(CH,FILE,block(V,["l","r"],steps),"@@TRACE2@@")
