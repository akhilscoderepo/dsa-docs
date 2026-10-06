from common import *
from tr import *
CH='15-trees-dfs'; F='01-tree-representation.md'
def run(arr):
    L,R=parse(arr); n=len(arr); steps=[]
    def go(i,label):
        if i is None:
            steps.append({"at":{"node":n},"vars":{"result":0},"note":f"The call receives null, which is an empty subtree, and returns 0."})
            return 0
        steps.append({"at":{"node":i},"vars":{"result":"?"},"note":f"The call receives the node {arr[i]} and asks the {label}."} if False else {"at":{"node":i},"vars":{"result":"?"},"note":f"The call receives the node {arr[i]} and counts its left side first."})
        a=go(L[i],"left"); b=go(R[i],"right")
        r=1+a+b
        steps.append({"at":{"node":i},"vars":{"result":r},"note":f"Both sides of the node {arr[i]} are counted as {a} and {b}, so the call returns 1 + {a} + {b} = {r}."})
        return r
    t=go(0,"root"); return steps,t
arr=[2,1,3]; s,t=run(arr); assert t==3
fill(CH,F,block(cells(arr),["node"],s),"@@TRACE1@@")
# second tree: missing left child, chain on the right; null cell at index 1
arr=[7,None,8,None,9]
L,R=parse(arr); assert L[0] is None and R[0]==2 and R[2]==4
steps=[]
def go2(i,side):
    if i is None:
        pos={"rootleft":1,"l2":3}.get(side,len(arr))
        steps.append({"at":{"node":pos},"vars":{"result":0},"note":"The call receives null, so it returns 0 without reading any field."})
        return 0
    steps.append({"at":{"node":i},"vars":{"result":"?"},"note":f"The call receives the node {arr[i]} and counts its left side first."})
    a=go2(L[i],"rootleft" if i==0 else ("l2" if i==2 else "x")); b=go2(R[i],"x")
    r=1+a+b
    steps.append({"at":{"node":i},"vars":{"result":r},"note":f"The sides of the node {arr[i]} return {a} and {b}, so the call returns {r}."})
    return r
assert go2(0,"root")==3
fill(CH,F,block(cells(arr),["node"],steps),"@@TRACE2@@")
