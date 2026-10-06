from common import *
import heapq
CH='17-heaps-and-priority-queues'; F='05-heap-scheduling.md'
def run(tasks):
    n=len(tasks); rel=sorted(range(n),key=lambda i:tasks[i][0]); h=[]; nxt=0; t=0; order=[]; st=[]
    cells=[tasks[i][1] for i in rel]
    for _ in range(n):
        note=""
        if not h and t<tasks[rel[nxt]][0]:
            note=f"The queue is empty, so the clock jumps from {t} to {tasks[rel[nxt]][0]}. "; t=tasks[rel[nxt]][0]
        added=[]
        while nxt<n and tasks[rel[nxt]][0]<=t:
            i=rel[nxt]; heapq.heappush(h,(tasks[i][1],i)); added.append(i); nxt+=1
        if added: note+=f"The requests {added} have arrived and join the queue. "
        d,i=heapq.heappop(h); order.append(i); start=t; t+=d
        st.append({"at":{"next":nxt},"vars":{"start":start,"clock":t,"queue":str(sorted(j for _,j in h)),"order":str(order)},"note":note+f"The request {i} has the smallest duration {d} among the arrived requests. It starts at {start} and ends at {t}."})
    return cells,order,st
cells,order,st=run([[5,3],[0,4],[2,2],[2,2]]); assert order==[1,2,3,0]
fill(CH,F,block(cells,["next"],st),"@@TRACE1@@")
cells,order,st=run([[4,2],[4,1],[0,1]]); assert order==[2,1,0]
fill(CH,F,block(cells,["next"],st),"@@TRACE2@@")
