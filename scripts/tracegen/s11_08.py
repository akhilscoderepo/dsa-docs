from common import *
from collections import deque
CH='11-stacks-and-queues'; FILE='08-queue-based-level-processing.md'
def fmt(l): return "["+", ".join(map(str,l))+"]"
def run(start,ch,ph,live):
    n=len(ch); q=deque(start); steps=[]; levels=[]
    while q:
        size=len(q); lv=[]
        v={"queue":fmt(q),"levelSize":size}
        if live: v["queue.size()"]=len(q)
        steps.append({"at":{"id":n},"vars":v,"note":f"A level begins. The captured size is {size}."})
        for _ in range(size):
            x=q.popleft(); lv.append(x); q.extend(ch[x])
            v={"queue":fmt(q),"levelSize":size,"batch":fmt(lv)}
            if live: v["queue.size()"]=len(q)
            steps.append({"at":{"id":x},"vars":v,"note":f"Poll {x}"+(f" and append {fmt(ch[x])}." if ch[x] else " and append nothing.")})
        levels.append(lv)
    fill(CH,FILE,block(list(range(n)),["id"],steps),ph); return levels
assert run([0],[[1,2],[3,4],[5],[],[6],[],[]],"@@TRACE1@@",False)==[[0],[1,2],[3,4,5],[6]]
assert run([0],[[1,2,3],[4],[],[5,6],[],[],[]],"@@TRACE2@@",True)==[[0],[1,2,3],[4,5,6]]
