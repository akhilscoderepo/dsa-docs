from common import *
from collections import deque
CH='11-stacks-and-queues'
F='08-queue-based-level-processing.md'
ch=[[1,2],[3,4],[5],[],[6],[],[]]
cells=list(range(7))
def qs(q): return str(list(q)).replace(' ','')
q=deque([0]); st=[]; rnd=0
while q:
    size=len(q); batch=list(q)
    for k in range(size):
        x=q.popleft(); add=ch[x]
        for c in add: q.append(c)
        note=f"Round {rnd + 1} has captured size {size}. Person {x} speaks" + (f" and adds {add}, who wait behind the current group." if add else " and adds nobody.")
        st.append({"at":{"item":x},"vars":{"round":rnd,"size":size,"queue":qs(q)},"note":note})
    rnd+=1
assert rnd==4
assert st[1]["vars"]["size"]==2 and st[1]["vars"]["queue"]=="[2,3,4]"
fill(CH,F,block(cells,["item"],st),"@@TRACE1@@")
# faulty loop: i < queue.size() live
q=deque([0]); st=[]
i=0; batch=[]
while i<len(q):
    x=q.popleft(); batch.append(x)
    for c in ch[x]: q.append(c)
    st.append({"at":{"item":x},"vars":{"i":i,"liveSize":len(q),"batch":str(batch).replace(' ','')},"note":f"Step {i}: person {x} is removed and adds {ch[x] if ch[x] else 'nobody'}, so the live size is now {len(q)} and the counter moves to {i+1}."})
    i+=1
assert batch==[0,1,2], batch
st[-1]["note"]+=" The counter now equals the live size, so the loop stops with the first batch holding 0, 1 and 2."
fill(CH,F,block(cells,["item"],st),"@@TRACE2@@")
