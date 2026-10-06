from common import *
from collections import deque
CH='11-stacks-and-queues'; FILE='01-arraydeque-contracts.md'
VALS=[4,7,9]
def run(removal,ph):
    dq=deque(); out=[]; st=[]
    fmt=lambda d: "["+", ".join(map(str,d))+"]"
    for i,v in enumerate(VALS):
        dq.append(v)
        st.append({"at":{"in":i},"vars":{"deque":fmt(dq),"out":fmt(out)},"note":f"addLast({v}) puts {v} at the last end."})
    for _ in VALS:
        x=dq.pop() if removal=="last" else dq.popleft()
        out.append(x)
        call="removeLast" if removal=="last" else "removeFirst"
        st.append({"at":{"in":len(VALS)},"vars":{"deque":fmt(dq),"out":fmt(out)},"note":f"{call}() returns {x}."})
    assert not dq
    fill(CH,FILE,block(VALS,["in"],st),ph); return out
assert run("last","@@TRACE1@@")==[9,7,4]
assert run("first","@@TRACE2@@")==[4,7,9]
