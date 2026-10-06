from common import *
import heapq
CH='20-greedy'; F='92-undo-the-worst-choice-with-a-heap.md'
lv=[4,5,13,14]; allow=2; passes=1; h=[]; st=[]
for i in range(1,len(lv)):
    rise=lv[i]-lv[i-1]; heapq.heappush(h,rise); note=f"The rise at index {i} is {rise}, so the runner pushes it into the heap."
    if len(h)>passes:
        out=heapq.heappop(h); allow-=out; note+=f" The heap holds more than {passes} rise, so the runner pops the smallest, {out}, and pays it from the allowance."
    else: note+=" The heap still fits the passes, so nothing is paid."
    assert allow>=0
    st.append({"at":{"i":i},"vars":{"heap":len(h),"allowance":allow},"note":note})
assert i==3
fill(CH,F,block(lv,["i"],st),"@@TRACE1@@")
# trace 2: refuel
start=10; stops=[(5,2),(11,10),(20,5)]; target=25
pts=stops+[(target,0)]; fuel=start; h=[]; n=0; st=[]; pos=0
for i,(p,f) in enumerate(pts):
    note=f"The next stop is at {p} and needs fuel {p} in total."
    while fuel<p and h:
        g=-heapq.heappop(h); fuel+=g; n+=1; note+=f" The fuel {fuel-g} is short, so the vehicle takes the largest passed station, {g}, and the fuel becomes {fuel}."
    assert fuel>=p
    if i<len(stops): heapq.heappush(h,-f); note+=f" The vehicle reaches it and adds its fuel {f} to the heap."
    else: note+=" The vehicle reaches the target."
    st.append({"at":{"i":i},"vars":{"fuel":fuel,"stops":n},"note":note})
assert n==3
fill(CH,F,block([f"{p}:{f}" if f else f"{p}:end" for p,f in pts],["i"],st),"@@TRACE2@@")
