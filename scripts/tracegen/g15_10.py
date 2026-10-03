from common import *
from tr import *
CH='15-trees-dfs'
F='10-tree-dfs-returns.md'
arr=[1,2,3,4,None,None,5]
L,R=parse(arr)
best=[0];gap=[0];st=[]
def go(i):
    if i is None: return 0
    a=go(L[i]); b=go(R[i])
    best[0]=max(best[0],a+b); gap[0]=max(gap[0],abs(a-b))
    h=1+max(a,b)
    st.append({"at":{"node":i},"vars":{"height":h,"chain":best[0],"gap":gap[0]},"note":f"The household {arr[i]} receives the branch heights {a} and {b}, so its local chain is {a + b} steps and its imbalance is {abs(a-b)}, and it reports the height {h}."})
    return h
go(0)
assert best[0]==4 and gap[0]==1
fill(CH,F,block(cells(arr),["node"],st),"@@TRACE1@@")
arr=[2,-1,3,None,4]
L,R=parse(arr)
best=[-10**9];st=[]
def go2(i):
    if i is None: return 0
    a=max(0,go2(L[i])); b=max(0,go2(R[i]))
    through=arr[i]+a+b
    best[0]=max(best[0],through)
    gain=arr[i]+max(a,b)
    st.append({"at":{"node":i},"vars":{"gain":gain,"through":through,"best":best[0]},"note":f"The household {arr[i]} gets the usable branch gains {a} and {b}, so the chain through it is worth {through}, while the gain it reports upward is {gain}."})
    return gain
go2(0)
assert best[0]==8
fill(CH,F,block(cells(arr),["node"],st),"@@TRACE2@@")
