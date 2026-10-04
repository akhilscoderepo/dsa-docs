from common import *
import heapq
CH='20-greedy'
F='05-task-selection.md'
types=[(3,7),(5,2),(2,9),(4,4)]
S=sorted(types,key=lambda t:-t[1])
assert S==[(2,9),(3,7),(4,4),(5,2)]
truck=8; units=0; st=[]
for i,(n,u) in enumerate(S):
    take=min(n,truck)
    if take>0:
        units+=take*u; truck-=take
        note=(f"All {n} boxes at {u} units fit, so they are loaded whole and {truck} places remain." if take==n
              else f"Only {take} of the {n} boxes at {u} units fit, so the truck becomes full.")
    else:
        note=f"The truck is already full, so the {n} boxes at {u} units stay on the dock."
    st.append({"at":{"i":i},"vars":{"placesLeft":truck,"units":units},"note":note})
assert units==51 and truck==0
fill(CH,F,block([f"{n}x{u}" for n,u in S],["i"],st),"@@TRACE1@@")
jobs=[(3,4),(5,9),(4,10),(2,11),(6,12)]
assert jobs==sorted(jobs,key=lambda j:j[1])
heap=[]; t=0; st=[]
for i,(h,dl) in enumerate(jobs):
    heapq.heappush(heap,-h); t+=h
    if t>dl:
        longest=-heapq.heappop(heap); t-=longest
        if longest==h: note=f"The task of {h} hours due at {dl} would end at hour {t+h}, too late. It is the longest in the set, so it ejects itself and the total returns to {t}."
        else: note=f"The task of {h} hours due at {dl} would end at hour {t+longest}, too late. The longest kept task of {longest} hours is ejected, so the total drops to {t}."
    else:
        note=f"The task of {h} hours due at {dl} ends at hour {t}, in time, so it joins the set."
    st.append({"at":{"i":i},"vars":{"total":t,"kept":len(heap),"longest":-heap[0]},"note":note})
assert len(heap)==3 and t==9
fill(CH,F,block([f"{h}h-{d}" for h,d in jobs],["i"],st),"@@TRACE2@@")
