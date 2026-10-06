from common import *
CH='12-monotonic-stacks'; FILE='04-boundary-discovery.md'
def fmt(l): return "["+", ".join(map(str,l))+"]"
V=[4,2,5,5,3,6]; n=len(V)
st=[]; left=[None]*n; steps=[]
sh=lambda a:"["+", ".join("." if x is None else str(x) for x in a)+"]"
for i,v in enumerate(V):
    while st and V[st[-1]]>=v:
        t=st.pop()
        steps.append({"at":{"i":i},"vars":{"stack":fmt(st),"left":sh(left)},"note":f"nums[{t}] = {V[t]} is at least {v}, so index {t} leaves the stack."})
    left[i]=st[-1] if st else -1; st.append(i)
    steps.append({"at":{"i":i},"vars":{"stack":fmt(st),"left":sh(left)},"note":f"The surviving top gives left[{i}] = {left[i]}, and index {i} goes on the stack."})
assert left==[-1,-1,1,1,1,4]; fill(CH,FILE,block(V,["i"],steps),"@@TRACE1@@")
st=[]; right=[None]*n; steps=[]
for i,v in enumerate(V):
    while st and V[st[-1]]>v:
        t=st.pop(); right[t]=i
        steps.append({"at":{"i":i},"vars":{"stack":fmt(st),"right":sh(right)},"note":f"{v} is smaller than nums[{t}] = {V[t]}, so right[{t}] = {i} and index {t} leaves the stack."})
    st.append(i)
    steps.append({"at":{"i":i},"vars":{"stack":fmt(st),"right":sh(right)},"note":f"Index {i} with value {v} goes on the stack."})
for t in st: right[t]=n
steps.append({"at":{"i":n},"vars":{"stack":fmt(st),"right":sh(right)},"note":f"The scan ends, and the indices {fmt(st)} receive the sentinel {n}."})
assert right==[1,6,4,4,6,6]; fill(CH,FILE,block(V,["i"],steps),"@@TRACE2@@")
