from common import *
from tr import *
CH='15-trees-dfs'; F='02-recursive-traversal-orders.md'
def walk(arr, mode):
    L,R=parse(arr); out=[]; steps=[]
    def vs(): return " ".join(map(str,out)) or "empty"
    def act(i,why):
        out.append(arr[i])
        steps.append({"at":{"node":i},"vars":{"out":vs()},"note":why})
    def go(i):
        if i is None: return
        if mode=="pre":
            act(i,f"The call on the node {arr[i]} starts and writes the value at once, before it calls either child.")
        else:
            steps.append({"at":{"node":i},"vars":{"out":vs()},"note":f"The call on the node {arr[i]} starts and calls its left child first."})
        go(L[i])
        if mode=="in": act(i,f"The left subtree of the node {arr[i]} is done, so the call writes the value {arr[i]} and then calls the right child.")
        go(R[i])
    go(0); return steps,out
arr=[1,2,3,4,5]; s,o=walk(arr,"in"); assert o==[4,2,5,1,3]
fill(CH,F,block(cells(arr),["node"],s),"@@TRACE1@@")
arr=[3,None,5,4]; s,o=walk(arr,"pre"); assert o==[3,5,4]
fill(CH,F,block(cells(arr),["node"],s),"@@TRACE2@@")
