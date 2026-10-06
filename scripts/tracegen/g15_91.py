from common import *
from tr import *
CH='15-trees-dfs'; F='91-return-results-from-subtrees.md'
def run(arr):
    L,R=parse(arr); steps=[]
    def go(i):
        if i is None: return (0,0,0)
        l=go(L[i]); r=go(R[i])
        lg=abs(l[0]-r[0]); lp=l[0]+r[0]
        rec=(1+max(l[0],r[0]), max(lg,l[1],r[1]), max(lp,l[2],r[2]))
        steps.append({"at":{"node":i},"vars":{"height":rec[0],"gap":rec[1],"path":rec[2]},"note":f"The call on the node {arr[i]} finishes. The children report heights {l[0]} and {r[0]}, so the local gap is {lg} and the local path is {lp} edge{"" if lp==1 else "s"}. The record is height {rec[0]}, gap {rec[1]}, path {rec[2]}."})
        return rec
    rec=go(0); return steps,rec
a=[5,3,8,1,4,None,9,0]; s,rec=run(a); assert rec==(4,1,5) or print(rec)
fill(CH,F,block(cells(a),["node"],s),"@@TRACE1@@")
a=[1,2,None,3,None,4]; s,rec=run(a); assert rec==(4,3,3),rec
fill(CH,F,block(cells(a),["node"],s),"@@TRACE2@@")
