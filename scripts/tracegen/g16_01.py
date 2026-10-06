from common import *
CH='16-trees-bfs-and-bsts'; F='01-levels-zigzag-and-views.md'
from collections import deque
# Trace 1: tree 3 -> (9, 20 -> (15, 7)); cells in discovery order
T={3:(9,20),9:(None,None),20:(15,7),15:(None,None),7:(None,None)}
cells=[3,9,20,15,7]; idx={v:i for i,v in enumerate(cells)}
q=deque([3]); front=0; res=[]; st=[]
while q:
    size=len(q); stop=front+size; lvl=[]
    st.append({"at":{"front":front,"stop":stop},"vars":{"size":size,"level":str(lvl)},"note":f"The level starts. The queue holds {size} node(s), so size is stored as {size} and the boundary stop is {stop}."} if False else None)
    st.pop()
    for _ in range(size):
        n=q.popleft(); lvl.append(n); front+=1
        for c in T[n]:
            if c is not None: q.append(c)
    res.append(lvl)
    st.append({"at":{"front":front,"stop":stop},"vars":{"size":size,"result":str(res)},"note":f"Level {len(res)-1} ends. The loop stored size {size}, removed exactly {size} node(s) and collected {lvl}."})
assert res==[[3],[9,20],[15,7]]
fill(CH,F,block(cells,["front","stop"],st),"@@TRACE1@@")
# Trace 2: buggy size read; tree 1 -> (2 -> (4), 3)
T={1:(2,3),2:(4,None),3:(None,None),4:(None,None)}
cells=[1,2,3,4]; q=deque([1]); front=0; lvl=[]; i=0
st=[{"at":{"front":0,"stop":1},"vars":{"i":0,"queue size":1,"level":"[]"},"note":"Start: the queue holds the node 1, and the first test reads the queue size 1."}]
while i<len(q):
    n=q.popleft(); lvl.append(n); front+=1
    for c in T[n]:
        if c is not None: q.append(c)
    i+=1
    st.append({"at":{"front":front,"stop":front+len(q)},"vars":{"i":i,"queue size":len(q),"level":str(lvl)},"note":f"The node {n} leaves and its children join, so the test now reads {len(q)} and compares it with i = {i}."+(" The test passes, so the loop removes another node of depth 1 in this level." if i<len(q) else " The test fails and the loop stops.")})
assert lvl==[1,2]
fill(CH,F,block(cells,["front","stop"],st),"@@TRACE2@@")
