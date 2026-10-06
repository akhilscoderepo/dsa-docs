from common import *
from collections import deque
CH='22-bfs-variations'; F='04-state-space-bfs.md'

def succ(c):
    out=[]
    for i,ch in enumerate(c):
        d=int(ch)
        out.append(c[:i]+str((d+1)%10)+c[i+1:]); out.append(c[:i]+str((d+9)%10)+c[i+1:])
    return out

# Trace 1: two-wheel lock, deadends 10 and 01, target 12.
dead={"10","90"}; start="00"; target="11"
seen=set(dead)|{start}; q=deque([start]); order=[]; steps=[]; turns=0; ans=-1; found=False
layers=[]
while q and not found:
    layer=list(q); q.clear(); layers.append(layer)
    for cur in layer:
        order.append(cur)
        if cur==target: ans=turns; found=True; break
        for n in succ(cur):
            if n not in seen: seen.add(n); q.append(n)
    if not found: turns+=1
assert ans==2, ans
# replay to build steps with indexes into order
seen=set(dead)|{start}; q=deque([(start,0)]); idx=0; steps=[]
while q:
    cur,t=q.popleft()
    i=order.index(cur)
    if cur==target:
        steps.append({"at":{"cur":i},"vars":{"turns":t,"queued":len(q)},"note":f"The search takes {cur} from the queue after {t} turns. It equals the target, so the method returns {t}."})
        break
    new=[]
    for n in succ(cur):
        if n not in seen: seen.add(n); q.append((n,t+1)); new.append(n)
    steps.append({"at":{"cur":i},"vars":{"turns":t,"queued":len(q)},"note":("The search takes "+cur+" from the queue and generates "+(", ".join(new) if new else "no new code")+(f"; each of them is {t+1} turn{'s' if t+1!=1 else ''} from the start." if new else ".")) })
print(order, len(steps)); 
for s in steps: print(s)
fill(CH,F,block(order,["cur"],steps),"@@TRACE1@@")

# Trace 2: key grid, complete state (row, col, key).
grid=["S.DT","#K##"]
def bfs(full):
    seen=set(); q=deque(); order=[]; steps=[]
    s=(0,0,0); seen.add(s if full else (0,0)); q.append((s,0))
    while q:
        (r,c,k),d=q.popleft(); order.append((r,c,k,d))
        if grid[r][c]=='T': return d,order
        for dr,dc in ((0,1),(1,0),(0,-1),(-1,0)):
            x,y=r+dr,c+dc
            if not(0<=x<2 and 0<=y<4) or grid[x][y]=='#': continue
            if grid[x][y]=='D' and not k: continue
            nk=1 if (k or grid[x][y]=='K') else 0
            key=(x,y,nk) if full else (x,y)
            if key in seen: continue
            seen.add(key); q.append(((x,y,nk),d+1))
    return -1,order
wrong,_=bfs(False); right,order=bfs(True)
assert wrong==-1 and right==5
cells=[f"({r},{c},{k})" for r,c,k,d in order]
steps=[]
seen={(0,0,0)}; q=deque([((0,0,0),0)])
while q:
    (r,c,k),d=q.popleft(); i=cells.index(f"({r},{c},{k})")
    if grid[r][c]=='T':
        steps.append({"at":{"cur":i},"vars":{"moves":d,"queued":len(q)},"note":f"The search takes ({r},{c},{k}), the target cell, after {d} moves, so it returns {d}."}); break
    new=[]
    for dr,dc in ((0,1),(1,0),(0,-1),(-1,0)):
        x,y=r+dr,c+dc
        if not(0<=x<2 and 0<=y<4) or grid[x][y]=='#': continue
        if grid[x][y]=='D' and not k: continue
        nk=1 if (k or grid[x][y]=='K') else 0
        if (x,y,nk) in seen: continue
        seen.add((x,y,nk)); q.append(((x,y,nk),d+1)); new.append(f"({x},{y},{nk})")
    steps.append({"at":{"cur":i},"vars":{"moves":d,"queued":len(q)},"note":f"The search takes ({r},{c},{k}) and generates "+(", ".join(new) if new else "no new state")+"."})
print(cells)
for s in steps: print(s)
fill(CH,F,block(cells,["cur"],steps),"@@TRACE2@@")
