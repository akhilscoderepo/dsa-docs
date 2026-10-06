from common import *
from collections import deque
CH='16-trees-bfs-and-bsts'; F='91-group-nodes-by-depth-with-a-queue.md'
def run(cells,kids,k,mode,ph):
    q=deque([0]); removed=-1; queued=0; depth=0; st=[{"at":{"removed":-1,"queued":0},"vars":{"depth":0},"note":"Start: the queue holds only the root."}]; res=[]
    while q and depth<k:
        size=len(q); last=None; row=0
        for _ in range(size):
            n=q.popleft(); removed=n; last=n; row+=cells[n]
            for c in kids[n]: q.append(c); queued=c
        depth+=1
        if mode=="sum":
            res.append(row); st.append({"at":{"removed":removed,"queued":queued},"vars":{"size":size,"row sum":row},"note":f"Row {depth-1} ends. The loop stored size {size}, removed that many nodes and found the sum {row}."})
        else:
            res.append(cells[last]); st.append({"at":{"removed":removed,"queued":queued},"vars":{"depth":depth,"view":str(res)},"note":f"Row {depth-1} ends. The last node removed was {cells[last]}, so it joins the view. The pass counter is now {depth}."+(" The counter equals k, so the loop stops." if depth==k else "")})
    fill(CH,F,block(cells,["removed","queued"],st),ph); return res
assert run([1,2,3,4,5,6,7],{0:[1,2,3],1:[],2:[4,5],3:[6],4:[],5:[],6:[]},99,"sum","@@TRACE1@@")==[1,9,18]
assert run([1,2,3,4,5,6],{0:[1,2],1:[3],2:[4],3:[5],4:[],5:[]},3,"view","@@TRACE2@@")==[1,3,5]
