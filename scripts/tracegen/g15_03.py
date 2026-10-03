from common import *
from tr import *
CH='15-trees-dfs'
F='03-iterative-dfs.md'
arr=[4,2,7,1,3]
L,R=parse(arr)
pend=[0];out=[];st=[]
while pend:
    i=pend.pop()
    out.append(arr[i])
    pushed=[]
    if R[i] is not None: pend.append(R[i]); pushed.append(f"right {arr[R[i]]}")
    if L[i] is not None: pend.append(L[i]); pushed.append(f"left {arr[L[i]]}")
    note=f"The room {arr[i]} came off the top of the pile and is written down. " + (("It leaves " + " then ".join(pushed) + " on the pile.") if pushed else "It has no sub-rooms, so nothing is added to the pile.")
    st.append({"at":{"node":i},"vars":{"pile":" ".join(str(arr[p]) for p in pend) or "empty","sheet":" ".join(map(str,out))},"note":note})
assert out==[4,2,1,3,7]
fill(CH,F,block(cells(arr),["node"],st),"@@TRACE1@@")
arr=[6,2,9,1,4]
L,R=parse(arr)
pend=[];out=[];st=[];cur=0
while cur is not None or pend:
    while cur is not None:
        pend.append(cur)
        st.append({"at":{"node":cur},"vars":{"pile":" ".join(str(arr[p]) for p in pend),"sheet":" ".join(map(str,out))},"note":f"The cursor reaches the room {arr[cur]}, which is put on the pile before the cursor goes to its left."})
        cur=L[cur]
    cur=pend.pop()
    out.append(arr[cur])
    st.append({"at":{"node":cur},"vars":{"pile":" ".join(str(arr[p]) for p in pend) or "empty","sheet":" ".join(map(str,out))},"note":f"The left side is finished, so the room {arr[cur]} is taken off the pile and written down, and the cursor moves to its right."})
    cur=R[cur]
assert out==[1,2,4,6,9]
fill(CH,F,block(cells(arr),["node"],st),"@@TRACE2@@")
