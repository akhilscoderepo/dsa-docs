from common import *
from collections import deque
CH='16-trees-bfs-and-bsts'; F='91-group-nodes-by-depth-with-a-queue.md'
cells=[1,2,3,4,5,6,7]; kids={0:[1,2,3],1:[],2:[4,5],3:[6],4:[],5:[],6:[]}
q=deque([0]); front=0; st=[]; res=[]
while q:
    size=len(q); stop=front+size; row=0
    for _ in range(size):
        n=q.popleft(); front+=1; row+=cells[n]
        for c in kids[n]: q.append(c)
    res.append(row)
    st.append({"at":{"front":front,"stop":stop},"vars":{"size":size,"row sum":row},"note":f"Row {len(res)-1} ends. The loop stored size {size}, removed that many nodes and found the sum {row}."})
assert res==[1,9,18]
pass
cells=[1,2,3,4,5,6]; kids={0:[1,2],1:[3],2:[4],3:[5],4:[],5:[]}
q=deque([0]); front=0; depth=0; k=3; st=[]; view=[]
while q and depth<k:
    size=len(q); stop=front+size; last=None
    for _ in range(size):
        n=q.popleft(); front+=1; last=n
        for c in kids[n]: q.append(c)
    view.append(cells[last]); depth+=1
    st.append({"at":{"front":front,"stop":stop},"vars":{"depth":depth,"view":str(view)},"note":f"Row {depth-1} ends. The last node removed was {cells[last]}, so it joins the view. The pass counter is now {depth}."+(" The counter equals k, so the loop stops." if depth==k else "")})
assert view==[1,3,5]
fill(CH,F,block(cells,["front","stop"],st),"@@TRACE2@@")
