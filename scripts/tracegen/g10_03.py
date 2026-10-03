from common import *
CH='10-intervals'
F='03-merge-and-insert.md'
rep=[[8,10],[1,3],[15,18],[2,6]]
srt=sorted(rep); out=[]; st=[]
idx={tuple(r):i for i,r in enumerate(rep)}
for r in srt:
    if not out or r[0]>out[-1][1]:
        out.append(list(r)); note=f"The report {r[0]} to {r[1]} starts past the active end, so it opens a new active stretch. The output now has {len(out)} stretches."
    else:
        old=out[-1][1]; out[-1][1]=max(out[-1][1],r[1]); note=f"The report {r[0]} to {r[1]} starts inside the active stretch, so its end becomes {out[-1][1]} and nothing is added to the output."
    st.append({"at":{"i":idx[tuple(r)]},"vars":{"activeStart":out[-1][0],"activeEnd":out[-1][1],"stretches":len(out)},"note":note})
assert out==[[1,6],[8,10],[15,18]] and "end becomes 6" in st[1]["note"]
fill(CH,F,block([f"{a}-{b}" for a,b in rep],["i"],st),"@@TRACE1@@")
board=[[1,2],[3,5],[6,7],[8,10],[12,16]]; lo,hi=4,8; st=[]; out=[]
for i,(s,e) in enumerate(board):
    if e<lo:
        out.append([s,e]); note=f"The stretch {s} to {e} ends before the new report starts at {lo}, so it is copied unchanged."
    elif s<=hi:
        lo=min(lo,s); hi=max(hi,e); note=f"The stretch {s} to {e} reaches the new report, so it is absorbed and the new report becomes {lo} to {hi}."
    else:
        if not any(o==[lo,hi] for o in out): out.append([lo,hi])
        out.append([s,e]); note=f"The stretch {s} to {e} starts after the new report ends, so the grown report {lo} to {hi} is written first and this stretch is copied."
    st.append({"at":{"i":i},"vars":{"newStart":lo,"newEnd":hi,"written":len(out)},"note":note})
assert out==[[1,2],[3,10],[12,16]] and "becomes 3 to 10" in st[3]["note"]
fill(CH,F,block([f"{a}-{b}" for a,b in board],["i"],st),"@@TRACE2@@")
