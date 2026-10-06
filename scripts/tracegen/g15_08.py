from common import *
from tr import *
CH='15-trees-dfs'; F='08-morris-traversal.md'
def run(arr,expect):
    L,R=parse(arr); n=len(arr)
    # mutable right links: R copy
    right=dict(R); left=dict(L); steps=[]; out=[]
    def thr():
        t=[f"{arr[a]} to {arr[b]}" for a,b in right.items() if b is not None and R[a]!=b]
        return ", ".join(t) or "none"
    def o(): return " ".join(map(str,out)) or "empty"
    cur=0
    while cur is not None:
        if left[cur] is None:
            out.append(arr[cur])
            nxt=right[cur]
            how="a thread back to an ancestor" if (nxt is not None and R[cur]!=nxt) else "its right child"
            steps.append({"at":{"cur":cur,"pred":-1},"vars":{"out":o(),"threads":thr()},"note":f"The node {arr[cur]} has no left child, so the walk writes it and moves right, along {how}." if nxt is not None else f"The node {arr[cur]} has no left child and no right link, so the walk writes it and ends."})
            cur=nxt
        else:
            p=left[cur]
            while right[p] is not None and right[p]!=cur: p=right[p]
            if right[p] is None:
                right[p]=cur
                steps.append({"at":{"cur":cur,"pred":p},"vars":{"out":o(),"threads":thr()},"note":f"The predecessor of the node {arr[cur]} is the node {arr[p]}, and its right reference is empty. The walk stores a thread to {arr[cur]} and moves to the left child."})
                cur=left[cur]
            else:
                right[p]=R[p]
                out.append(arr[cur])
                steps.append({"at":{"cur":cur,"pred":p},"vars":{"out":o(),"threads":thr()},"note":f"The predecessor {arr[p]} already links to the node {arr[cur]}, so this is the second arrival. The walk removes the thread, writes {arr[cur]} and moves right."})
                cur=right[cur]
    assert out==expect,(out,expect)
    assert all(right[k]==R[k] for k in R)
    return steps
a=[4,2,6,1,3]; fill(CH,F,block(cells(a),["cur","pred"],run(a,[1,2,3,4,6])),"@@TRACE1@@")
a=[3,1,None,None,2]; fill(CH,F,block(cells(a),["cur","pred"],run(a,[1,2,3])),"@@TRACE2@@")
