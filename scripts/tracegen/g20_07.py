from common import *
import heapq
CH='20-greedy'
F='07-greedy-and-heap.md'
h=[3,9,4,6,2,12,8]; timber=4; wins=1
heap=[]; st=[]; ans=len(h)-1
for i in range(len(h)-1):
    climb=h[i+1]-h[i]
    if climb<=0:
        note=f"Moving from height {h[i]} to {h[i+1]} is level or downhill, so it costs nothing."
    else:
        heapq.heappush(heap,climb)
        if len(heap)>wins:
            r=heapq.heappop(heap); timber-=r
            note=f"The climb of {climb} is added and the winches are overcommitted, so the smallest climb on a winch, {r}, is paid in timber, leaving {timber}."
            if timber<0:
                note=f"The climb of {climb} is added and the smallest climb on a winch, {r}, must be paid in timber, but the timber would fall to {timber}, so the walk stops here."
        else:
            note=f"The climb of {climb} takes a winch provisionally, and no timber is spent."
    st.append({"at":{"i":i},"vars":{"timber":timber,"onWinches":"-".join(map(str,sorted(heap))) or "none"},"note":note})
    if timber<0:
        ans=i; break
assert ans==4 and st[-1]["at"]["i"]==4
fill(CH,F,block([str(x) for x in h],["i"],st),"@@TRACE1@@")
target=60; fuel=10; depots=[(10,30),(20,10),(30,25),(50,20)]
pool=[]; stops=0; st=[]
cells=[f"{p}:{o}" for p,o in depots]+[f"{target}:end"]
for i in range(len(depots)+1):
    pos=depots[i][0] if i<len(depots) else target
    notes=[]
    while fuel<pos:
        o=-heapq.heappop(pool); fuel+=o; stops+=1
        notes.append(f"The reach {fuel-o} is short of {pos}, so the largest oil in the pool, {o}, is drawn as stop number {stops} and the reach becomes {fuel}.")
    if i<len(depots):
        heapq.heappush(pool,-depots[i][1])
        notes.append(f"The depot at {pos} is within reach, so its {depots[i][1]} units of oil enter the pool.")
    else:
        notes.append(f"The target at {pos} is within the reach {fuel}.")
    st.append({"at":{"i":i},"vars":{"reach":fuel,"stops":stops,"pool":"-".join(str(-x) for x in sorted(pool)) or "none"},"note":" ".join(notes)})
assert stops==2 and st[-1]["at"]["i"]==len(depots)
fill(CH,F,block(cells,["i"],st),"@@TRACE2@@")
