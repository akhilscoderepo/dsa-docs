from common import *
from tr import *
CH='15-trees-dfs'; F='04-depth-and-path-state.md'
arr=[8,3,10,1,6]; L,R=parse(arr); T=12
assert L[0]==1 and R[0]==2 and L[1]==3 and R[1]==4
def run(backtrack):
    route=[]; steps=[]; found=[]
    def vs(): return " ".join(map(str,route)) or "empty"
    def go(i):
        if i is None: return
        route.append(arr[i]); rem=T-sum(route); leaf=L[i] is None and R[i] is None
        if leaf:
            if backtrack: ok=rem==0
            else: ok=rem==0
            note=f"The call on the leaf {arr[i]} adds its value. The remaining amount is {rem}"+(", so this route matches." if rem==0 else ", so this route does not match.")
        else:
            note=f"The call on the node {arr[i]} adds its value to the list. The remaining amount is {rem}, and the call continues to its children."
        if not backtrack and leaf and arr[i]==6:
            note=f"The call on the leaf 6 adds its value to a list that still holds 1. The remaining amount shows {rem}, but the route to this node is 8, 3, 6 with remaining {T-17}."
        steps.append({"at":{"node":i},"vars":{"route":vs(),"remaining":rem},"note":note})
        go(L[i]); go(R[i])
        if backtrack:
            route.pop()
            steps.append({"at":{"node":i},"vars":{"route":vs(),"remaining":T-sum(route)},"note":f"Both children of the node {arr[i]} are done, so the call removes its value from the list."})
    go(0); return steps
fill(CH,F,block(cells(arr),["node"],run(True)),"@@TRACE1@@")
fill(CH,F,block(cells(arr),["node"],run(False)),"@@TRACE2@@")
