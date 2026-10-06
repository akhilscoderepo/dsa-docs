from common import *
import itertools
CH='20-greedy'; F='04-exchange-reasoning.md'
def ov(a,b): return a[0]<b[1] and b[0]<a[1]
# trace 1: exchange on schedule
iv=[(1,3),(2,5),(4,7),(6,9)]; opt=[(2,5),(6,9)]
assert all(not ov(a,b) for a,b in itertools.combinations(opt,2))
best=max(len(c) for r in range(5) for c in itertools.combinations(iv,r) if all(not ov(a,b) for a,b in itertools.combinations(c,2)))
assert best==2
chosen=min(iv,key=lambda x:x[1]); assert chosen==(1,3)
changed=[chosen]+opt[1:]; assert all(not ov(a,b) for a,b in itertools.combinations(changed,2)) and len(changed)==2
lab=lambda x:f"{x[0]}-{x[1]}"
st=[{"at":{"k":0},"vars":{"answer":"2-5, 6-9","size":2},"note":"The best answer begins with [2,5), which is not the choice of the rule. The rule picks [1,3), the interval with the earliest end."},
{"at":{"k":0},"vars":{"answer":"1-3, 6-9","size":2},"note":"The exchange step replaces [2,5) with [1,3). The new interval ends at 3, before 5, so it ends no later than the interval it replaces."},
{"at":{"k":1},"vars":{"answer":"1-3, 6-9","size":2},"note":"The interval [6,9) starts at 6, after 3, so it does not overlap the choice. The changed answer is valid, has size 2 and begins with the choice."}]
fill(CH,F,block([lab(x) for x in opt],["k"],st),"@@TRACE1@@")
# trace 2: shortest first
iv=[(0,4),(3,5),(4,8)]
order=sorted(iv,key=lambda x:(x[1]-x[0],x[0])); kept=[]; st=[]
for i,m in enumerate(order):
    if any(ov(m,k) for k in kept):
        note=f"The interval [{m[0]},{m[1]}) overlaps the accepted interval, so the rule rejects it."
    else:
        kept.append(m); note=f"The interval [{m[0]},{m[1]}) has length {m[1]-m[0]} and overlaps no accepted interval, so the rule accepts it."
    st.append({"at":{"i":i},"vars":{"accepted":len(kept)},"note":note})
assert len(kept)==1 and not ov((0,4),(4,8))
fill(CH,F,block([lab(x) for x in order],["i"],st),"@@TRACE2@@")
