from common import *
from collections import deque
CH='21-graph-traversal-models-dfs-and-ordinary-bfs'
F='05-grid-graphs.md'
DR=[-1,1,0,0]; DC=[0,0,-1,1]
# trace 1: spill from index 0, flat 3x3
rows,cols=3,3
floor=[1,1,0, 0,1,0, 1,0,1]
tone=floor[0]; seen=[False]*9; seen[0]=True; q=deque([0]); steps=[]; done=0
while q:
    code=q.popleft(); r,c=divmod(code,cols); done+=1
    added=[]
    for d in range(4):
        nr,nc=r+DR[d],c+DC[d]
        if nr<0 or nr>=rows or nc<0 or nc>=cols: continue
        if floor[nr*cols+nc]!=tone: continue
        if seen[nr*cols+nc]: continue
        seen[nr*cols+nc]=True; q.append(nr*cols+nc); added.append(nr*cols+nc)
    steps.append({"at":{"cur":code},"vars":{"recoloured":done,"queue":",".join(map(str,q)) or "empty"},
      "note":f"Tile {code} at row {r}, column {c} is recoloured, and "+(f"it queues {len(added)} new neighbor tile"+("s" if len(added)!=1 else "")+f" ({','.join(map(str,added))})." if added else "it queues nothing, since every neighbor is out of bounds, another colour or already seen.")})
assert [i for i in range(9) if seen[i]]==[0,1,4] and done==3 and not seen[6] and not seen[8]
fill(CH,F,block(floor,["cur"],steps),"@@TRACE1@@")
# trace 2: islands on flat 3x4
rows,cols=3,4
g="110000100011"
g=[ "1100","0010","0011"]
flat=[ch for row in g for ch in row]
seen=[False]*12; islands=0; last=0; steps=[]
def flood(s):
    seen[s]=True; q=deque([s]); n=0
    while q:
        code=q.popleft(); n+=1; r,c=divmod(code,cols)
        for d in range(4):
            nr,nc=r+DR[d],c+DC[d]
            if 0<=nr<rows and 0<=nc<cols and flat[nr*cols+nc]=='1' and not seen[nr*cols+nc]:
                seen[nr*cols+nc]=True; q.append(nr*cols+nc)
    return n
for s in range(12):
    if flat[s]=='1' and not seen[s]:
        last=flood(s); islands+=1
        note=f"Index {s} is unseen land, so island {islands} starts and its traversal claims {last} tile"+("s" if last!=1 else "")+"."
    elif flat[s]=='1':
        note=f"Index {s} is land but already seen, so no new traversal starts."
    else:
        continue
    steps.append({"at":{"scan":s},"vars":{"islands":islands,"last_size":last},"note":note})
steps.append({"at":{"scan":12},"vars":{"islands":islands,"last_size":last},"note":f"The scan has passed all twelve cells and the answer is {islands} islands."})
assert islands==3 and all(seen[i]==(flat[i]=='1') for i in range(12))
fill(CH,F,block(flat,["scan"],steps),"@@TRACE2@@")
