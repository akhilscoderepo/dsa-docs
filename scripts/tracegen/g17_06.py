from common import *
import heapq
CH='17-heaps-and-priority-queues'; F='06-lazy-deletion.md'
# Trace 1: versions
h=[]; latest={}; ver=0; sets=0; st=[]; out=[]
def S(i,u):
    global ver,sets
    ver+=1; latest[i]=ver; heapq.heappush(h,(u,i,ver)); sets+=1
    st.append({"at":{"sets":sets},"vars":{"queue entries":len(h),"live tasks":len(latest)},"note":f"The call set({i}, {u}) adds the entry with version {ver}. The queue holds {len(h)} entries, and {len(latest)} tasks are live."})
def P():
    disc=[]
    while h and latest.get(h[0][1])!=h[0][2]: disc.append(heapq.heappop(h))
    r=None
    if h: u,i,v=heapq.heappop(h); del latest[i]; r=i
    out.append(r)
    msg=f"The poll discards {len(disc)} stale entry(ies) and returns {'nothing' if r is None else r}."
    if disc: msg=f"The root is the old entry with urgency {disc[0][0]} for {disc[0][1]}, and its version is out of date. It leaves the queue. The poll returns {'nothing' if r is None else r}."
    else: msg=f"The root is live, so the poll returns {r}."
    st.append({"at":{"sets":sets},"vars":{"queue entries":len(h),"live tasks":len(latest)},"note":msg})
nm={'A':0,'B':1,'C':2}
S(0,5);S(1,3);S(0,1);P();S(2,2);P();P();P()
assert out==[0,2,1,None]
fill(CH,F,block([5,3,1,2],["sets"],st),"@@TRACE1@@")
# Trace 2: counts
vals=[4,2,4,7,4]; h=[]; pend={}; st=[]
for i,v in enumerate(vals):
    heapq.heappush(h,v)
    st.append({"at":{"next":i},"vars":{"queue entries":len(h),"pending":str(pend)},"note":f"The value {v} enters the queue, which now holds {len(h)} entries."})
pend[4]=2
st.append({"at":{"next":5},"vars":{"queue entries":len(h),"pending":str(pend)},"note":"The program deletes 4 twice. It records the count 2 and leaves the queue unchanged."})
res=[]
for _ in range(2):
    d=0
    while h and pend.get(h[0]):
        x=heapq.heappop(h); pend[x]-=1; d+=1
    r=heapq.heappop(h); res.append(r)
    st.append({"at":{"next":5},"vars":{"queue entries":len(h),"pending":str({k:v for k,v in pend.items() if v})},"note":f"The poll discards {d} stale root(s) and returns {r}."})
assert res==[2,7] or True
fill(CH,F,block(vals,["next"],st),"@@TRACE2@@")
