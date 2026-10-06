from common import *
from collections import deque
CH='11-stacks-and-queues'; FILE='04-bfs-queue-state.md'
TOP=20
def dfs_first(s,t):
    seen=[False]*(TOP+1); st=[(s,0)]; seen[s]=True
    while st:
        x,k=st.pop()
        if x==t: return k
        if x+3<=TOP and not seen[x+3]: seen[x+3]=True; st.append((x+3,k+1))
        if x-2>=0 and not seen[x-2]: seen[x-2]=True; st.append((x-2,k+1))
    return -1
def run(s,t,ph):
    dist={s:0}; q=deque([s]); steps=[]; skipped=0
    fq=lambda: "["+", ".join(f"{x}:{dist[x]}" for x in q)+"]"
    while q:
        cur=q.popleft(); new=[]
        if cur==t:
            steps.append({"at":{"cur":cur},"vars":{"queue":fq(),"count":dist[cur]},"note":f"Floor {cur} leaves the queue and is the target. The answer is {dist[cur]}."})
            fill(CH,FILE,block(list(range(TOP+1)),["cur"],steps),ph)
            return dist[cur],skipped
        for d in (3,-2):
            n=cur+d
            if n<0 or n>TOP: continue
            if n in dist: skipped+=1; continue
            dist[n]=dist[cur]+1; q.append(n); new.append(f"{n}:{dist[n]}")
        steps.append({"at":{"cur":cur},"vars":{"queue":fq(),"new":", ".join(new) if new else "none"},"note":f"Floor {cur} leaves the queue with count {dist[cur]}. It adds {len(new)} new floor(s)."})
    return -1,skipped
assert dfs_first(1,10)==8
r,sk=run(1,10,"@@TRACE1@@"); assert r==3
r,sk=run(18,13,"@@TRACE2@@"); assert sk>0,sk
print(r,sk)
