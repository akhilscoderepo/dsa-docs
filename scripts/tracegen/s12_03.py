from common import *
CH='12-monotonic-stacks'; FILE='03-stock-span.md'
def fmt(l): return "["+", ".join(map(str,l))+"]"
V=[30,25,20,22,22,28,40,10]; st=[]; steps=[]; out=[]
for i,v in enumerate(V):
    while st and V[st[-1]]<=v:
        t=st.pop()
        steps.append({"at":{"i":i},"vars":{"stack":fmt(st),"span":"-"},"note":f"Price {v} is at least prices[{t}] = {V[t]}, so index {t} leaves the stack."})
    b=st[-1] if st else -1; sp=i-b; out.append(sp); st.append(i)
    steps.append({"at":{"i":i},"vars":{"stack":fmt(st),"span":sp},"note":f"The boundary is {b}, so the span is {i} - ({b}) = {sp}, and index {i} goes on the stack."})
assert out==[1,1,1,2,3,5,7,1]; fill(CH,FILE,block(V,["i"],steps),"@@TRACE1@@")
V=[8,6,5,6,6,9,3]; st=[]; steps=[]; out=[]
pf=lambda s:"["+", ".join(f"{p}/{c}" for p,c in s)+"]"
for i,v in enumerate(V):
    sp=1
    while st and st[-1][0]<=v:
        p,c=st.pop(); sp+=c
        steps.append({"at":{"i":i},"vars":{"pairs":pf(st),"span":sp},"note":f"Price {v} is at least {p}, so the pair {p}/{c} leaves and its {c} day{'s' if c>1 else ''} join the span."})
    st.append((v,sp)); out.append(sp)
    steps.append({"at":{"i":i},"vars":{"pairs":pf(st),"span":sp},"note":f"The span of price {v} is {sp}, and the pair {v}/{sp} goes on the stack."})
assert out==[1,1,1,3,4,6,1]; fill(CH,FILE,block(V,["i"],steps),"@@TRACE2@@")
