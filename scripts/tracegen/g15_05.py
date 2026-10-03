from common import *
from tr import *
CH='15-trees-dfs'
F='05-diameter-and-subtree-returns.md'
arr=[1,2,3,4,5]
L,R=parse(arr)
best=[0];st=[]
def go(i):
    if i is None: return 0
    a=go(L[i]); b=go(R[i])
    best[0]=max(best[0],a+b)
    h=1+max(a,b)
    note=(f"The station {arr[i]} has branches {a} and {b} below it, so a journey turning here has {a + b} segments, and it reports a branch of {h} upward.")
    st.append({"at":{"node":i},"vars":{"reports":h,"best":best[0]},"note":note})
    return h
go(0)
assert best[0]==3
fill(CH,F,block(cells(arr),["node"],st),"@@TRACE1@@")
arr=[-10,9,20,None,None,15,7]
L,R=parse(arr)
best=[-10**9];st=[]
def go2(i):
    if i is None: return 0
    a=max(0,go2(L[i])); b=max(0,go2(R[i]))
    turn=arr[i]+a+b
    best[0]=max(best[0],turn)
    up=arr[i]+max(a,b)
    note=f"The station {arr[i]} adds its label to the branches {a} and {b}, giving {turn} for a journey turning here, and it reports {max(0,up)} upward."
    st.append({"at":{"node":i},"vars":{"reports":max(0,up),"best":best[0]},"note":note})
    return up
go2(0)
assert best[0]==42
fill(CH,F,block(cells(arr),["node"],st),"@@TRACE2@@")
