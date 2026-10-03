from common import *
from tr import *
CH='15-trees-dfs'
F='01-tree-representation.md'
arr=[4,2,7,1,3]
L,R=parse(arr)
st=[]
def go(i):
    if i is None: return 0
    a=go(L[i]); b=go(R[i]); c=1+a+b
    la=arr[L[i]] if L[i] is not None else None
    note=(f"The node {arr[i]} has " + (f"the left subtree of size {a}" if L[i] is not None else "an empty left subtree") + " and " + (f"the right subtree of size {b}" if R[i] is not None else "an empty right subtree") + f", so its count is 1 + {a} + {b} = {c}.")
    st.append({"at":{"node":i},"vars":{"count":c},"note":note})
    return c
assert go(0)==5
fill(CH,F,block(cells(arr),["node"],st),"@@TRACE1@@")
ch=[[1,2,3],[4],[],[5],[],[]]
st=[]
def depth(i):
    d=0
    for c in ch[i]: d=max(d,depth(c))
    d+=1
    note=(f"The node {i} is a leaf with an empty child list, so its depth is 1." if not ch[i] else f"The node {i} takes the largest child depth {d-1} and adds one, so its depth is {d}.")
    st.append({"at":{"node":i},"vars":{"depth":d},"note":note})
    return d
assert depth(0)==3
fill(CH,F,block([str(i) for i in range(6)],["node"],st),"@@TRACE2@@")
