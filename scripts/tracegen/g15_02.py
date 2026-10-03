from common import *
from tr import *
CH='15-trees-dfs'
F='02-recursive-traversal-orders.md'
arr=[4,2,7,1,3]
L,R=parse(arr)
pre=[];ino=[];post=[];st=[]
def snap(i,note):
    st.append({"at":{"node":i},"vars":{"pre":" ".join(map(str,pre)),"in":" ".join(map(str,ino)),"post":" ".join(map(str,post))},"note":note})
def go(i):
    if i is None: return
    pre.append(arr[i]); snap(i,f"The call on the shelf {arr[i]} has just started, so preorder writes {arr[i]}.")
    go(L[i])
    ino.append(arr[i]); snap(i,f"The left call of the shelf {arr[i]} has returned, so inorder writes {arr[i]}.")
    go(R[i])
    post.append(arr[i]); snap(i,f"Both calls of the shelf {arr[i]} have returned, so postorder writes {arr[i]}.")
go(0)
assert pre==[4,2,1,3,7] and ino==[1,2,3,4,7] and post==[1,3,2,7,4]
fill(CH,F,block(cells(arr),["node"],st),"@@TRACE1@@")
arr=[6,2,None,None,4]
L,R=parse(arr)
out=[];st=[]
def snap2(i,note):
    st.append({"at":{"node":i},"vars":{"sheet":" ".join(map(str,out))},"note":note})
def go2(i,parent,side):
    if i is None:
        snap2(parent,f"The {side} sub-shelf of {arr[parent]} is empty, so that call returns at once and writes nothing.")
        return
    go2(L[i],i,"left")
    out.append(arr[i]); snap2(i,f"The left call of the shelf {arr[i]} is done, so the label {arr[i]} joins the sheet.")
    go2(R[i],i,"right")
go2(0,None,None)
assert out==[2,4,6]
fill(CH,F,block(cells(arr),["node"],st),"@@TRACE2@@")
