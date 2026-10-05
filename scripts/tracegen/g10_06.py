from common import *
CH='10-intervals'; FILE='06-event-sweep.md'
def sweep(iv,closed,ph):
    ev=[]
    for a,b in iv: ev+=[(a,1),(b,-1)]
    ev.sort(key=lambda e:(e[0],-e[1] if closed else e[1]))
    act=best=0; st=[{"at":{"e":-1},"vars":{"active":0,"best":0},"note":"The events are sorted. The running count starts at 0."}]
    for i,(c,d) in enumerate(ev):
        act+=d; best=max(best,act)
        kind="start" if d>0 else "end"
        st.append({"at":{"e":i},"vars":{"change":f"{d:+d}","active":act,"best":best},"note":f"The {kind} event at coordinate {c} changes the count by {d:+d}, so the count becomes {act}."})
    fill(CH,FILE,block([c for c,d in ev],["e"],st),ph); return best
assert sweep([[1,4],[4,6],[2,5],[5,7]],False,"@@TRACE1@@")==2
assert sweep([[1,4],[4,6],[2,5],[5,7]],True,"@@TRACE2@@")==3
