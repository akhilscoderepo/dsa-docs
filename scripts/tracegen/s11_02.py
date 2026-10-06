from common import *
from collections import deque
CH='11-stacks-and-queues'; FILE='02-fifo-simulation.md'
fmt=lambda d: "["+", ".join(map(str,d))+"]"
def rr(work):
    w=list(work); q=deque(range(len(w))); fin=[]; st=[]
    while q:
        t=q.popleft(); w[t]-=1
        if w[t]>0:
            q.append(t); note=f"Task {t} loses one unit, has {w[t]} left and returns to the back."
        else:
            fin.append(t); note=f"Task {t} loses its last unit and finishes."
        st.append({"at":{"task":t},"vars":{"queue":fmt(q),"finished":fmt(fin)},"note":note})
    fill(CH,FILE,block(list(work),["task"],st),"@@TRACE1@@"); return fin
assert rr([2,1,3])==[1,0,2]
def lunch(stu,sw):
    q=deque(stu); top=0; miss=0; st=[]
    while q and miss<len(q):
        s=q.popleft()
        if s==sw[top]:
            top+=1; miss=0; note=f"A student who wants {s} takes sandwich {s}, and misses resets to 0."
        else:
            q.append(s); miss+=1; note=f"A student who wants {s} does not match sandwich {sw[top]} and moves to the back, so misses is {miss}."
        st.append({"at":{"top":top},"vars":{"queue":fmt(q),"misses":miss},"note":note})
    st.append({"at":{"top":top},"vars":{"queue":fmt(q),"misses":miss},"note":f"The queue size equals misses, so the loop stops with {len(q)} students left."})
    fill(CH,FILE,block(list(sw),["top"],st),"@@TRACE2@@"); return len(q)
assert lunch([1,0,0,1,1],[0,0,1,0,1])==2
