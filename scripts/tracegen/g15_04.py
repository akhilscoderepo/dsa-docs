from common import *
from tr import *
CH='15-trees-dfs'
F='04-depth-and-path-state.md'
arr=[5,4,8,11,None,13,4]
L,R=parse(arr)
st=[];found=[]
def go(i,rem,seen):
    if i is None: return
    rem2=rem-arr[i]
    leaf=L[i] is None and R[i] is None
    if leaf:
        ok=rem2==0
        note=f"The signpost {arr[i]} is a dead end and the remaining amount is {rem2}, " + ("so this route matches the target." if ok else "which is not zero, so this route does not match.")
        if ok: found.append(i)
    else:
        note=f"The signpost {arr[i]} is entered with {rem} still needed, so its children are given {rem2}."
    st.append({"at":{"node":i},"vars":{"remaining":rem2},"note":note})
    go(L[i],rem2,seen); go(R[i],rem2,seen)
go(0,20,[])
assert found==[3]
fill(CH,F,block(cells(arr),["node"],st),"@@TRACE1@@")
arr=[1,2,3,4,5]
L,R=parse(arr)
st=[];path=[];tot=[0]
def go2(i):
    if i is None: return
    path.append(arr[i]); s=sum(path)
    leaf=L[i] is None and R[i] is None
    if leaf:
        note=f"The signpost {arr[i]} is chalked and is a dead end with sum {s}, " + ("which equals 7, so the route is copied out." if s==7 else "which is not 7, so nothing is reported.")
    else:
        note=f"The signpost {arr[i]} is chalked, and the board now holds the route to it with sum {s}."
    st.append({"at":{"node":i},"vars":{"board":" ".join(map(str,path)),"sum":s},"note":note})
    go2(L[i]); go2(R[i])
    path.pop()
    st.append({"at":{"node":i},"vars":{"board":" ".join(map(str,path)) or "empty","sum":sum(path)},"note":f"Both trails below the signpost {arr[i]} are done, so its chalk mark is wiped and the board returns to its earlier state."})
go2(0)
fill(CH,F,block(cells(arr),["node"],st),"@@TRACE2@@")
