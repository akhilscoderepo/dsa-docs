from common import *
CH='10-intervals'
F='06-event-sweep-ties.md'
IV=[[1,4],[2,5],[4,7],[5,8]]
def run(closed):
    ev=[]
    for s,e in IV: ev+= [(s,1),(e,-1)]
    ev.sort(key=lambda x:(x[0],-x[1]) if closed else (x[0],x[1]))
    cells=[f"{c}{'+' if d>0 else '-'}" for c,d in ev]
    act=0; peak=0; st=[]
    for i,(c,d) in enumerate(ev):
        act+=d; peak=max(peak,act)
        kind='start' if d>0 else 'end'
        st.append({"at":{"e":i},"vars":{"active":act,"peak":peak},"note":f"The {kind} entry at coordinate {c} moves the counter to {act}, and the peak so far is {peak}."})
    return cells,st,peak
c1,s1,p1=run(False); assert p1==2
assert c1[2]=="4-" and c1[3]=="4+" and s1[2]["vars"]["active"]==1 and s1[3]["vars"]["active"]==2
s1[2]["note"]="The end entry at coordinate 4 comes first and moves the counter down to 1, and the peak so far is 2."
fill(CH,F,block(c1,["e"],s1),"@@TRACE1@@")
c2,s2,p2=run(True); assert p2==3
assert c2[2]=="4+" and c2[3]=="4-" and s2[2]["vars"]["active"]==3
fill(CH,F,block(c2,["e"],s2),"@@TRACE2@@")
