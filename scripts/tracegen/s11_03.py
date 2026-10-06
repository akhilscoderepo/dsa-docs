from common import *
CH='11-stacks-and-queues'; FILE='03-two-stack-queue.md'
fmt=lambda d: "["+", ".join(map(str,d))+"]"
def run(vals, ops, ph):
    ins=[]; outs=[]; got=[]; moves=0; nxt=0; st=[]
    for op in ops:
        if op=="E":
            v=vals[nxt]; nxt+=1; ins.append(v); note=f"enqueue({v}) pushes {v} onto in."
        else:
            note=""
            if not outs:
                n=len(ins)
                while ins: outs.append(ins.pop()); moves+=1
                note=f"out is empty, so {n} value(s) move from in to out. "
            x=outs.pop(); got.append(x); note+=f"dequeue() pops {x} from out."
        st.append({"at":{"next":nxt},"vars":{"in":fmt(ins),"out":fmt(outs)},"note":note})
    assert moves<=len(vals)
    fill(CH,FILE,block(vals,["next"],st),ph); return got
assert run([4,7,9],"EEEDDD","@@TRACE1@@")==[4,7,9]
assert run([4,7,9,2],"EEEDEDDD","@@TRACE2@@")==[4,7,9,2]
