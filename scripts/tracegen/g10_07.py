from common import *
CH='10-intervals'
F='07-sorting-and-intervals.md'
R=[[8,10],[1,4],[2,6],[5,7],[15,18],[16,17]]
S=sorted(R)
assert S==[[1,4],[2,6],[5,7],[8,10],[15,18],[16,17]]
cells=[f"{a}-{b}" for a,b in S]
st=[]; blk=-1; end=None; n=0
for i,(a,b) in enumerate(S):
    if end is None or a>end:
        blk=i; end=b; n+=1
        note=f"The session {a} to {b} starts after the carried end, so a new block opens here and the carried end becomes {b}." if n>1 else f"The session {a} to {b} is the first one, so the first block opens and the carried end becomes {b}."
    else:
        if b>end:
            end=b; note=f"The session {a} to {b} starts at or before the carried end and reaches further, so the carried end grows to {b}."
        else:
            note=f"The session {a} to {b} starts at or before the carried end and ends inside it, so nothing changes."
    st.append({"at":{"i":i,"block":blk},"vars":{"carriedEnd":end,"blocks":n},"note":note})
assert n==3 and end==18 and "starts after the carried end" in st[3]["note"] and "ends inside it" in st[5]["note"]
fill(CH,F,block(cells,["i","block"],st),"@@TRACE1@@")
P=[[3,9],[0,6],[5,10],[11,13],[12,15]]
T=sorted(P,key=lambda r:r[1])
assert T==[[0,6],[3,9],[5,10],[11,13],[12,15]]
cells=[f"{a}-{b}" for a,b in T]
st=[]; shot=None; owner=-1; shots=[]
for i,(a,b) in enumerate(T):
    if shot is None or a>shot:
        shot=b; owner=i; shots.append(b)
        note=f"The session {a} to {b} has not heard an announcement, so one is made at its end, {b}." 
    else:
        note=f"The session {a} to {b} starts at {a}, which is not after the announcement at {shot}, so it already heard it."
    st.append({"at":{"i":i,"shot":owner},"vars":{"lastShot":shot,"announcements":len(shots)},"note":note})
assert shots==[6,13]
fill(CH,F,block(cells,["i","shot"],st),"@@TRACE2@@")
