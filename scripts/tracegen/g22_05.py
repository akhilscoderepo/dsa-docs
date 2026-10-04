from common import *
from collections import deque
CH='22-bfs-variations'
F='05-resource-dominance.md'
DR=[-1,1,0,0]; DC=[0,0,-1,1]

def run(fell, tokens):
    """simulate the lesson's best-table layered BFS; return steps list and answer"""
    rows,cols=len(fell),len(fell[0]); width=tokens+1
    best=[-1]*(rows*cols); best[0]=tokens
    frontier=deque([0*width+tokens]); log=[]; steps=0; ans=-1
    while frontier:
        for _ in range(len(frontier)):
            state=frontier.popleft(); cell,left=divmod(state,width)
            r,c=divmod(cell,cols); pushed=[]; refused=[]
            if cell==rows*cols-1:
                log.append((cell,left,steps,pushed,refused,len(frontier))); return log,steps
            for d in range(4):
                nr,nc=r+DR[d],c+DC[d]
                if nr<0 or nr>=rows or nc<0 or nc>=cols: continue
                nl=left-(1 if fell[nr][nc]=='#' else 0)
                if nl<0: continue
                nxt=nr*cols+nc
                if nl<=best[nxt]: refused.append((nxt,nl)); continue
                best[nxt]=nl; frontier.append(nxt*width+nl); pushed.append((nxt,nl))
            log.append((cell,left,steps,pushed,refused,len(frontier)))
        steps+=1
    return log,-1

def mk(fell, tokens, pick=None):
    log,ans=run(fell,tokens)
    cells=[ch for row in fell for ch in row]
    out=[]
    for cell,left,dist,pushed,refused,qn in log:
        if pick is not None and cell not in pick: continue
        r,c=divmod(cell,len(fell[0]))
        p=", ".join(f"cell {a} with {b} left" for a,b in pushed) or "nothing"
        note=f"Take cell {cell} (row {r}, column {c}) at step {dist} holding {left} token"+("s" if left!=1 else "")+f"; it queues {p}"
        if refused: note+="; refused as not richer than the table: "+", ".join(f"cell {a} with {b} left" for a,b in refused)
        note+="."
        out.append({"at":{"cur":cell},"vars":{"step":dist,"left":left,"queued":qn},"note":note})
    return cells,out,ans

# trace 1: small fell
f1=['.#.','##.','...']
cells,steps,ans=mk(f1,1)
assert ans==4, ans
assert len(steps)>=3
fill(CH,F,block(cells,["cur"],steps),"@@TRACE1@@")

# trace 2: the grid where a Boolean by cell fails
f2=['.#...','...##','..##.']
log,ans=run(f2,1)
assert ans==8
# the key moment: cell 2 (row 0, col 2) is taken at step 2 with 0 left and again at step 4 with 1 left
hits=[(c,l,d) for c,l,d,_,_,_ in log if c==2]
assert hits==[(2,0,2),(2,1,4)], hits
cells,steps,ans=mk(f2,1)
print(len(steps))
fill(CH,F,block(cells,["cur"],steps),"@@TRACE2@@")
