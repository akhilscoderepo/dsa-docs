from common import *
CH='07-prefix-sums-and-difference-arrays'
F='08-difference-arrays.md'
n=6; jobs=[(1,3,5),(2,5,2),(4,5,4)]; diff=[0]*(n+1); st=[]
for k,(l,r,v) in enumerate(jobs):
    diff[l]+=v; diff[r+1]-=v
    st.append({"at":{"start":l,"cancel":r+1},"vars":{"amount":v,"slotStart":diff[l],"slotCancel":diff[r+1]},"note":f"Job {k+1} adds {v} to plots {l} to {r}. Add {v} to slot {l}, which becomes {diff[l]}, and subtract {v} from slot {r+1}, which becomes {diff[r+1]}."})
assert diff==[0,5,2,0,-1,0,-6] and jobs[2][1]+1==6
fill(CH,F,block([str(x) for x in diff],["start","cancel"],st),"@@TRACE1@@")
st=[]; run=0; out=[]
for p in range(n):
    run+=diff[p]; out.append(run)
    st.append({"at":{"p":p},"vars":{"delta":diff[p],"total":run},"note":f"Add the delta {diff[p]} to the running sum, which becomes {run}, so plot {p} receives {run} liters."})
assert out==[0,5,7,7,6,6] and st[3]["vars"]["delta"]==0 and st[3]["vars"]["total"]==7
fill(CH,F,block([str(x) for x in diff],["p"],st),"@@TRACE2@@")
