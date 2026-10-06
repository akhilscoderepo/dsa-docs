from common import *
import heapq
CH='20-greedy'; F='05-task-selection.md'
def run(c,ph):
    order=sorted(c,key=lambda x:x[1]); h=[]; total=0; st=[]
    for i,(d,l) in enumerate(order):
        heapq.heappush(h,-d); total+=d
        note=f"The job {d} due {l} joins the set, so the total becomes {total}."
        if total>l:
            out=-heapq.heappop(h); total-=out
            note+=f" The total passes {l}, so the scan drops the longest duration {out}, and the total becomes {total}."
        else: note+=f" The total fits inside {l}, so the job stays."
        st.append({"at":{"i":i},"vars":{"total":total,"kept":len(h)},"note":note})
    fill(CH,F,block([f"{d}/{l}" for d,l in order],["i"],st),ph); return len(h)
assert run([[4,4],[3,9],[2,10],[9,11]],"@@TRACE1@@")==3
assert run([[5,5],[2,6],[2,6]],"@@TRACE2@@")==2
