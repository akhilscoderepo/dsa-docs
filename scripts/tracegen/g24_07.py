from common import *
import heapq
CH='24-shortest-paths-and-graph-state-modeling'
F='07-graph-and-heap.md'
# trace 1: last-to-light, first flare on pad 2
times=[[2,1,2],[2,3,1],[3,4,3],[1,4,1],[4,5,2]]; n=5; k=2
out={i:[] for i in range(1,n+1)}
for u,v,w in times: out[u].append((v,w))
INF=10**9
best={i:INF for i in out}; best[k]=0
heap=[(0,k)]; steps=[]; skipped=0; popped=[]
while heap:
    d,u=heapq.heappop(heap)
    if d>best[u]:
        skipped+=1
        steps.append({"at":{"u":u-1},"vars":{"time":d,"best":best[u],"skipped":skipped,"waiting":len(heap)},
          "note":f"The entry ({d}, pad {u}) is older than the recorded time {best[u]}, so stale rejection drops it and pad {u} is not expanded again."})
        continue
    added=[]
    for v,w in out[u]:
        if d+w<best[v]:
            best[v]=d+w; heapq.heappush(heap,(d+w,v)); added.append(f"pad {v} at {d+w}")
    steps.append({"at":{"u":u-1},"vars":{"time":d,"best":best[u],"skipped":skipped,"waiting":len(heap)},
      "note":f"Pad {u} is final at time {d}"+("; it pushes "+", ".join(added)+"." if added else " and offers nothing better.")})
assert best=={1:2,2:0,3:1,4:3,5:5}, best
assert skipped==1 and len(steps)==6
worst=max(best.values()); who=min(v for v in best if best[v]==worst)
assert (worst,who)==(5,5)
steps[-1]["note"]+=f" The largest time is {worst}, held by pad {who}."
fill(CH,F,block([str(i) for i in range(1,n+1)],["u"],steps),"@@TRACE1@@")
# trace 2: flights with state key (strip, used), cap = stops+1 = 2
fl=[[0,1,1],[1,2,1],[2,3,1],[0,2,5]]; src,dst,stops=0,3,1; cap=stops+1
bst={(0,0):0}; heap=[(0,0,0)]; steps=[]; order=[]; ans=None
while heap:
    c,e,u=heapq.heappop(heap)
    if c>bst.get((u,e),10**9): continue
    order.append(f"{u}/{e}")
    if u==dst:
        ans=(c,e)
        steps.append({"at":{"pop":len(order)-1},"vars":{"cost":c,"flights":e,"waiting":len(heap)},"note":f"Strip {u} is the destination, released with cost {c} and {e} flights, so the answer is {c} with {e} flights."})
        break
    if e==cap:
        steps.append({"at":{"pop":len(order)-1},"vars":{"cost":c,"flights":e,"waiting":len(heap)},"note":f"State {u}/{e} is current but all {cap} flights are used, so nothing is expanded."})
        continue
    added=[]
    for a,b,w in fl:
        if a==u and c+w<bst.get((b,e+1),10**9):
            bst[(b,e+1)]=c+w; heapq.heappush(heap,(c+w,e+1,b)); added.append(f"{b}/{e+1} at {c+w}")
    steps.append({"at":{"pop":len(order)-1},"vars":{"cost":c,"flights":e,"waiting":len(heap)},
      "note":f"State {u}/{e} costs {c}"+("; it pushes "+", ".join(added)+"." if added else " and pushes nothing.")})
assert ans==(6,2) and order==["0/0","1/1","2/2","2/1","3/2"], (ans,order)
fill(CH,F,block(order,["pop"],steps),"@@TRACE2@@")
print(order,ans)
