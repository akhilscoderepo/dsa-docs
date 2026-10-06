from common import *
from tr import *
CH='15-trees-dfs'; F='06-balance-sentinels.md'
def run(arr,expect):
    L,R=parse(arr); steps=[]
    def go(i):
        if i is None: return 0
        l=go(L[i])
        if l==-1:
            steps.append({"at":{"node":i},"vars":{"result":-1},"note":f"The left call of the node {arr[i]} returned -1, so the call returns -1 at once. The right side is not visited."}); return -1
        r=go(R[i])
        if r==-1:
            steps.append({"at":{"node":i},"vars":{"result":-1},"note":f"The right call of the node {arr[i]} returned -1, so the call returns -1."}); return -1
        if abs(l-r)>1:
            steps.append({"at":{"node":i},"vars":{"result":-1},"note":f"The node {arr[i]} has sides of height {l} and {r}. The difference {abs(l-r)} is more than 1, so the call returns -1."}); return -1
        h=1+max(l,r)
        steps.append({"at":{"node":i},"vars":{"result":h},"note":f"The node {arr[i]} has sides of height {l} and {r}. The difference {abs(l-r)} is allowed, so the call returns {h}."}); return h
    assert go(0)==expect
    return steps
a=[5,3,8,1,None,7,9]; fill(CH,F,block(cells(a),["node"],run(a,3)),"@@TRACE1@@")
a=[6,4,8,2,None,None,None,1]; s=run(a,-1); assert all(x["at"]["node"]!=2 for x in s); fill(CH,F,block(cells(a),["node"],s),"@@TRACE2@@")
