from common import *
CH='11-stacks-and-queues'; FILE='07-min-stack.md'
def fmt(l): return "["+", ".join(map(str,l))+"]"
# Trace 1: value-min pairs
VALS=[5,3,7,3]
st=[];steps=[]
pf=lambda s:"["+", ".join(f"{v}/{m}" for v,m in s)+"]"
for i,v in enumerate(VALS):
    lo=v if not st else min(v,st[-1][1])
    st.append((v,lo))
    steps.append({"at":{"in":i},"vars":{"pairs":pf(st),"min":lo},"note":f"push({v}) stores the pair {v} with minimum {lo}."})
for _ in VALS:
    v,_m=st.pop()
    steps.append({"at":{"in":len(VALS)},"vars":{"pairs":pf(st),"min":st[-1][1] if st else "none"},"note":f"pop() returns {v}"+(f" and the minimum reads {st[-1][1]} from the pair below." if st else " and the stack is empty.")})
assert not st and steps[3]["vars"]["min"]==3 and steps[6]["vars"]["min"]==5
fill(CH,FILE,block(VALS,["in"],steps),"@@TRACE1@@")
# Trace 2: helper stack, duplicates
VALS=[4,2,2,6]
main=[];mins=[];steps=[]
for i,v in enumerate(VALS):
    main.append(v)
    kept = not mins or v<=mins[-1]
    if kept: mins.append(v)
    steps.append({"at":{"in":i},"vars":{"main":fmt(main),"helper":fmt(mins),"min":mins[-1]},"note":f"push({v}) "+("also enters the helper stack." if kept else "stays out of the helper stack.")})
for _ in VALS:
    v=main.pop()
    dropped = v==mins[-1]
    if dropped: mins.pop()
    steps.append({"at":{"in":len(VALS)},"vars":{"main":fmt(main),"helper":fmt(mins),"min":mins[-1] if mins else "none"},"note":f"pop() returns {v}"+(" and removes one helper entry." if dropped else " and leaves the helper stack unchanged.")})
assert not main and not mins and steps[6]["vars"]["min"]==4 and steps[5]["vars"]["min"]==2
fill(CH,FILE,block(VALS,["in"],steps),"@@TRACE2@@")
