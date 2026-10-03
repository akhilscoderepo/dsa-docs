from common import *
CH='10-intervals'
F='05-overlap-and-coverage.md'
# trace 1: select by end, half-open
R=[[0,6],[1,3],[2,4],[3,5],[5,7],[6,8]]
S=sorted(R,key=lambda r:r[1])
assert S==[[1,3],[2,4],[3,5],[0,6],[5,7],[6,8]]
cells=[f"{a}-{b}" for a,b in S]
kept=-1; last=None; cnt=0; st=[]
for i,(a,b) in enumerate(S):
    if last is None or a>=last:
        kept=i; last=b; cnt+=1
        note=f"The request {a} to {b} starts at {a}, which is at or after the last end {'(none yet)' if cnt==1 else ''}".replace(" (none yet)"," of nothing kept yet") if cnt==1 else f"The request {a} to {b} starts at {a}, at or after the last end, so it is kept and the last end becomes {b}."
        if cnt==1: note=f"The request {a} to {b} is the first one, so it is kept and the last end becomes {b}."
    else:
        note=f"The request {a} to {b} starts at {a}, before the last end {last}, so it is rejected and the kept pointer stays put."
    st.append({"at":{"i":i,"kept":kept},"vars":{"lastEnd":last,"kept":cnt},"note":note})
assert cnt==3 and len(R)-cnt==3
assert st[1]["note"].startswith("The request 2 to 4 starts at 2, before the last end 3")
fill(CH,F,block(cells,["i","kept"],st),"@@TRACE1@@")
# trace 2: coverage
Q=[[1,4],[3,6],[2,8],[2,5],[8,9],[7,8]]
T=sorted(Q,key=lambda r:(r[0],-r[1]))
assert T==[[1,4],[2,8],[2,5],[3,6],[7,8],[8,9]]
cells=[f"{a}-{b}" for a,b in T]
reach=None; owner=-1; vis=0; st=[]
for i,(a,b) in enumerate(T):
    if reach is None or b>reach:
        vis+=1; owner=i; prev=reach; reach=b
        note=f"The request {a} to {b} ends past the reach, so it is visible and now sets the reach to {b}." if prev is not None else f"The request {a} to {b} is the first one, so it is visible and sets the reach to {b}."
    else:
        note=f"The request {a} to {b} ends at {b}, which does not pass the reach {reach}, so it is covered and hidden."
    st.append({"at":{"i":i,"owner":owner},"vars":{"reach":reach,"visible":vis},"note":note})
assert vis==3
assert "2 to 5" in st[2]["note"] and "covered" in st[2]["note"]
fill(CH,F,block(cells,["i","owner"],st),"@@TRACE2@@")
