from common import *
from tr import *
CH='15-trees-dfs'; F='05-diameter-and-subtree-returns.md'
def run(arr,expect):
    L,R=parse(arr); steps=[]; best_all=[0]
    def go(i):
        if i is None: return (0,0)
        lh,lb=go(L[i]); rh,rb=go(R[i])
        through=lh+rh; best=max(through,lb,rb); h=1+max(lh,rh)
        why=("The complete path here is better than both sides, so best is "+str(best)+".") if best==through and through>max(lb,rb) else ("A leaf has no edges below it, so best stays 0." if (lh==0 and rh==0) else "A path below is at least as long, so best stays "+str(best)+".")
        steps.append({"at":{"node":i},"vars":{"height":h,"through":through,"best":best},"note":f"The call on the node {arr[i]} finishes. The children report heights {lh} and {rh}, so through is {through} and the height is {h}. {why}"})
        return (h,best)
    h,b=go(0); assert b==expect,(b,expect); return steps
a=[1,2,3,4,5]; fill(CH,F,block(cells(a),["node"],run(a,3)),"@@TRACE1@@")
a=[1,2,None,3,4,5,None,None,6]; fill(CH,F,block(cells(a),["node"],run(a,4)),"@@TRACE2@@")
