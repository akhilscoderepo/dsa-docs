from common import *
import heapq
CH='17-heaps-and-priority-queues'; F='04-k-way-merge.md'
def run(src):
    h=[(s[0],i,0) for i,s in enumerate(src) if s]; heapq.heapify(h); out=[]; st=[]
    fmt=lambda h:"["+", ".join(f"{v} from {i}" for v,i,_ in sorted(h))+"]"
    st.append({"at":{"out":-1},"vars":{"frontier":fmt(h)},"note":f"The frontier starts with the first value of each non-empty file: {fmt(h)}."})
    while h:
        v,i,p=heapq.heappop(h); out.append(v)
        n=p+1; ex=""
        if n<len(src[i]): heapq.heappush(h,(src[i][n],i,n)); ex=f" File {i} offers its successor {src[i][n]}."
        else: ex=f" File {i} has no successor, so the frontier shrinks."
        st.append({"at":{"out":len(out)-1},"vars":{"frontier":fmt(h)},"note":f"The poll returns {v} from file {i}."+ex})
    return out,st
src=[[1,4,7],[2,5],[3,6,9]]; out,st=run(src); assert out==sorted(sum(src,[]))
fill(CH,F,block(out,["out"],st),"@@TRACE1@@")
src=[[2,2],[],[2,3]]; out,st=run(src); assert out==[2,2,2,3]
fill(CH,F,block(out,["out"],st),"@@TRACE2@@")
