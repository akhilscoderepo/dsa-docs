from common import *
CH='20-greedy'
F='02-interval-scheduling.md'
R=[(2,5),(1,3),(4,6),(3,8),(6,9),(8,10),(9,12)]
S=sorted(R,key=lambda r:r[1])
assert S==[(1,3),(2,5),(4,6),(3,8),(6,9),(8,10),(9,12)]
free=None; kept=0; st=[]
for i,(a,b) in enumerate(S):
    if free is None:
        free=b; kept+=1; note=f"The span {a} to {b} is first in end order and nothing is held, so it is accepted and the free boundary becomes {b}."
    elif a>=free:
        extra=" It begins exactly at the boundary, which half-open spans allow." if a==free else ""
        free=b; kept+=1; note=f"The span {a} to {b} begins at {a}, not before the boundary, so it is accepted and the boundary moves to {b}.{extra}"
    else:
        note=f"The span {a} to {b} begins at {a}, before the boundary {free}, so it is rejected and the boundary stays."
    st.append({"at":{"i":i},"vars":{"freeAt":free,"kept":kept,"rejected":i+1-kept},"note":note})
assert kept==4 and len(R)-kept==3
fill(CH,F,block([f"{a}-{b}" for a,b in S],["i"],st),"@@TRACE1@@")
B=[(10,16),(2,8),(1,6),(7,12),(14,18),(5,6)]
T=sorted(B,key=lambda r:r[0])
assert T==[(1,6),(2,8),(5,6),(7,12),(10,16),(14,18)]
shots=0; g=None; st=[]
for i,(a,b) in enumerate(T):
    if g is None or a>g:
        shots+=1
        if g is None: note=f"The balloon {a} to {b} opens the first group, so arrow number 1 is owed and the group end is {b}."
        else: note=f"The balloon {a} to {b} starts at {a}, past the group end {g}, so the earlier group is closed at {g} and arrow number {shots} is owed with group end {b}."
        g=b
    else:
        old=g; g=min(g,b)
        note=f"The balloon {a} to {b} starts at {a}, within reach of the group end {old}, so it joins and the group end becomes {g}."
    st.append({"at":{"i":i},"vars":{"groupEnd":g,"arrows":shots},"note":note})
assert shots==3
fill(CH,F,block([f"{a}-{b}" for a,b in T],["i"],st),"@@TRACE2@@")
