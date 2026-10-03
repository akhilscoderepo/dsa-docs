from common import *
from collections import deque
CH='11-stacks-and-queues'
F='04-bfs-queue-state.md'
nxt=[[1,2],[3],[3,4],[5],[5,6],[],[]]
nxt=[[1,2],[3],[3,4],[5],[5,6],[],[]]
cells=list(range(7))
def qs(q): return "["+",".join(map(str,q))+"]"
def run(mark_at_insert):
    dist=[-1]*7; q=deque([0]); dist[0]=0; seen={0}; st=[]; processed=set()
    while q:
        b=q.popleft()
        if not mark_at_insert and b in processed:
            st.append({"at":{"at":b},"vars":{"queue":qs(q)},"note":f"Beacon {b} is removed again, but it was already processed, so the duplicate is skipped."}); continue
        processed.add(b)
        added=[]; skipped=[]
        for nb in nxt[b]:
            if mark_at_insert:
                if nb in seen: skipped.append(nb)
                else: seen.add(nb); q.append(nb); added.append(nb)
            else:
                if nb in processed: skipped.append(nb)
                else: q.append(nb); added.append(nb)
        if b==5:
            note="Beacon 5 is the target, so the search stops with the shortest distance."
        else:
            note=f"Beacon {b} is removed."
            note+=(f" It adds {added}." if added else " It adds nothing.")
            if skipped: note+=f" The beacon(s) {skipped} are already marked, so they are not added again."
        st.append({"at":{"at":b},"vars":{"queue":qs(q)},"note":note})
        if b==5: break
    return st
s1=run(True)
assert any("already marked" in s["note"] for s in s1)
fill(CH,F,block(cells,["at"],s1),"@@TRACE1@@")
s2=run(False)
assert any("skipped" in s["note"] for s in s2)
# make duplicate visible: check the queue after beacon 2 holds 3 twice
assert any(s["vars"]["queue"].count("3")==2 for s in s2), [s["vars"] for s in s2]
fill(CH,F,block(cells,["at"],s2),"@@TRACE2@@")
