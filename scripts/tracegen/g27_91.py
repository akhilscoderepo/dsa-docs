from common import *
CH='27-dynamic-programming-capacity-and-partition-patterns'
F='91-dp-and-capacity.md'
def once(items,T):
    w=[0]*(T+1); w[0]=1
    st=[{"at":{"t":0},"vars":{"v":0,"add":0,"ways":1},"note":"The seed is the empty choice, so the count for total 0 is 1."}]
    for v in items:
        for t in range(T,v-1,-1):
            add=w[t-v]
            if add:
                w[t]+=add
                st.append({"at":{"t":t},"vars":{"v":v,"add":add,"ways":w[t]},
                  "note":f"Pack {v} at total {t} gains {add} from total {t-v}, which was read before pack {v} changed it, so the count becomes {w[t]}."})
    return st,w
def ordered(items,T):
    w=[0]*(T+1); w[0]=1
    st=[{"at":{"t":0},"vars":{"v":0,"add":0,"ways":1},"note":"The seed is the empty sequence, so the count for total 0 is 1."}]
    for t in range(1,T+1):
        for v in items:
            if v<=t and w[t-v]:
                add=w[t-v]; w[t]+=add
                st.append({"at":{"t":t},"vars":{"v":v,"add":add,"ways":w[t]},
                  "note":f"Total {t} with the last element {v} gains {add} from total {t-v}, so its count becomes {w[t]}."})
    return st,w
import itertools
sub=lambda it,T: sum(1 for m in range(1<<len(it)) if sum(it[i] for i in range(len(it)) if m>>i&1)==T)
s,w=once([1,2,3],4); assert w[4]==sub([1,2,3],4)==1
fill(CH,F,block(list(range(5)),["t"],s),"@@TRACE1@@")
s,w=ordered([1,2,3],4); assert w==[1,1,2,4,7]
fill(CH,F,block(list(range(5)),["t"],s),"@@TRACE2@@")
print("ok")
