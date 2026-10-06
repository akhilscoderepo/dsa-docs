from common import *
CH='16-trees-bfs-and-bsts'; F='02-bst-invariant-and-bounds.md'
INF=None
def fmt(x,neg):
    return "no limit" if x is None else str(x)
def run(cells,kids,order_check):
    pass
# Trace 1: 5 (1, 6 (3,7)); indices 0..4; children: 0->(1,2), 2->(3,4)
cells=[5,1,6,3,7]; kids={0:(1,2),1:(None,None),2:(3,4),3:(None,None),4:(None,None)}
st=[]; ok=True
def walk(i,low,high,why):
    global ok
    if i is None or not ok: return
    v=cells[i]; bad=(low is not None and v<=low) or (high is not None and v>=high)
    lo,hi=fmt(low,0),fmt(high,1)
    if bad:
        st.append({"at":{"node":i},"vars":{"low":lo,"high":hi},"note":f"{why} The key {v} must lie between {lo} and {hi}, and it does not, so the result is false."}); ok=False; return
    st.append({"at":{"node":i},"vars":{"low":lo,"high":hi},"note":f"{why} The key {v} lies inside the interval, so the walk continues."})
    l,r=kids[i]; walk(l,low,v,f"Left of {v}: the upper limit becomes {v}."); walk(r,v,high,f"Right of {v}: the lower limit becomes {v}.")
walk(0,None,None,"The root starts with no limit.")
assert not ok and st[-1]["at"]["node"]==3
fill(CH,F,block(cells,["node"],st),"@@TRACE1@@")
# Trace 2: 8 (4 (2,6), 12 (10,14)); path 8 -> 4 -> 6
cells=[8,4,12,2,6,10,14]
path=[(0,None,None,"The root starts with no limit."),(1,None,8,"Left turn at 8: the upper limit becomes 8."),(4,4,8,"Right turn at 4: the lower limit becomes 4.")]
st=[]
for i,lo,hi,why in path:
    v=cells[i]; assert (lo is None or v>lo) and (hi is None or v<hi)
    st.append({"at":{"node":i},"vars":{"low":fmt(lo,0),"high":fmt(hi,1)},"note":f"{why} The key {v} lies inside the interval."})
fill(CH,F,block(cells,["node"],st),"@@TRACE2@@")
