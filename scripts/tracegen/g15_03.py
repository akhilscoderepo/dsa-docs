from common import *
from tr import *
CH='15-trees-dfs'; F='03-iterative-dfs.md'
def sv(st,arr): return " ".join(str(arr[i]) for i in reversed(st)) or "empty"
# trace 1: iterative preorder on [7,3,9,1,5]
arr=[7,3,9,1,5]; L,R=parse(arr); st=[0]; out=[]; steps=[]
while st:
    i=st.pop(); out.append(arr[i])
    if R[i] is not None: st.append(R[i])
    if L[i] is not None: st.append(L[i])
    pushed=[arr[c] for c in (R[i],L[i]) if c is not None]
    nt=("Its children go in as "+" then ".join(map(str,pushed))+", so the left child ends on top.") if pushed else "It has no children, so nothing is pushed."
    steps.append({"at":{"node":i},"vars":{"stack":sv(st,arr),"out":" ".join(map(str,out))},"note":f"The loop pops the node {arr[i]} and writes it. {nt}"})
assert out==[7,3,1,5,9]
fill(CH,F,block(cells(arr),["node"],steps),"@@TRACE1@@")
# trace 2: iterative postorder with last visited on [4,2,None,1,3]
arr=[4,2,None,1,3]; L,R=parse(arr); assert L[0]==1 and R[0] is None and L[1]==3 and R[1]==4
st=[];out=[];steps=[];cur=0;last=None
def vs(): return " ".join(map(str,out)) or "empty"
while cur is not None or st:
    while cur is not None:
        st.append(cur)
        steps.append({"at":{"node":cur},"vars":{"stack":sv(st,arr),"out":vs()},"note":f"The loop pushes the node {arr[cur]} and moves to its left child."})
        cur=L[cur]
    top=st[-1]
    if R[top] is not None and R[top]!=last:
        cur=R[top]
        steps.append({"at":{"node":top},"vars":{"stack":sv(st,arr),"out":vs()},"note":f"The node {arr[top]} is on top and its right child {arr[R[top]]} is not the last node written, so the loop enters the right side."})
    else:
        out.append(arr[top]); last=st.pop()
        why="it has no right child" if R[top] is None else f"its right child {arr[R[top]]} was just written"
        steps.append({"at":{"node":top},"vars":{"stack":sv(st,arr),"out":vs()},"note":f"The node {arr[top]} is on top and {why}, so the loop writes and pops it."})
assert out==[1,3,2,4]
fill(CH,F,block(cells(arr),["node"],steps),"@@TRACE2@@")
