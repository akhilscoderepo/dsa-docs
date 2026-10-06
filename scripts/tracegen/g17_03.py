from common import *
import heapq
CH='17-heaps-and-priority-queues'; F='03-top-k.md'
def run(s,k):
    h=[]; st=[]
    for i,v in enumerate(s):
        if len(h)<k: heapq.heappush(h,v); act=f"The queue holds fewer than {k} values, so {v} enters."
        elif v>h[0]:
            old=heapq.heapreplace(h,v); act=f"The candidate {v} beats the root {old}. The value {old} leaves and {v} enters."
        else: act=f"The candidate {v} does not beat the root {h[0]}, so the program discards it."
        st.append({"at":{"next":i},"vars":{"kept":str(sorted(h)),"root":h[0]},"note":act+f" The kept values are {sorted(h)}."})
    return h,st
h,st=run([4,9,2,7,5,8,3],3); assert sorted(h)==[7,8,9]
fill(CH,F,block([4,9,2,7,5,8,3],["next"],st),"@@TRACE1@@")
h,st=run([5,5,5,1],2); assert sorted(h)==[5,5]
fill(CH,F,block([5,5,5,1],["next"],st),"@@TRACE2@@")
