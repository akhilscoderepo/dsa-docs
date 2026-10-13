from common import *
CH='33-design-data-structure-problems'; F='04-iterators.md'

# Trace 1: lookahead wrapper over [4,7,9]; pointer pos = number of source advances.
class Peek:
    def __init__(s, data): s.d=data; s.pos=0; s.slot=None; s.filled=False
    def has_next(s): return s.filled or s.pos < len(s.d)
    def peek(s):
        if not s.filled:
            assert s.pos < len(s.d)
            s.slot=s.d[s.pos]; s.pos+=1; s.filled=True
        return s.slot
    def next(s):
        v=s.peek(); s.filled=False; return v
data=[4,7,9]; w=Peek(data)
st=[{"at":{"pos":0},"vars":{"slot":"empty","call":"start"},"note":"Start: nothing is pulled, the slot is empty and pos is 0."}]
script=[("peek",4),("peek",4),("next",4),("hasNext",True),("next",7),("peek",9),("next",9),("hasNext",False)]
for op,exp in script:
    r={"peek":w.peek,"next":w.next,"hasNext":w.has_next}[op]()
    assert r==exp,(op,r,exp)
    slot=str(w.slot) if w.filled else "empty"
    if op=="peek": note=f"peek() returns {r}; pos is {w.pos} and the slot holds {slot}."
    elif op=="next": note=f"next() returns {r}; the slot is now empty and pos is {w.pos}."
    else: note=f"hasNext() answers {str(r).lower()} without pulling; pos stays {w.pos}."
    st.append({"at":{"pos":w.pos},"vars":{"slot":slot,"call":f"{op}() = {str(r).lower() if isinstance(r,bool) else r}"},"note":note})
assert w.pos==3
fill(CH,F,block(data,["pos"],st),"@@TRACE1@@")

# Trace 2: stack of iterators on [[1,[2]],[],3]; cells are the integers in output order.
def L(*x): return list(x)
nested=L(L(1,L(2)),L(),3)
stack=[iter(nested)]; pending=[None]; out=[]
def scan():
    acts=[]
    while pending[0] is None and stack:
        top=stack[-1]
        try: item=next(top)
        except StopIteration:
            stack.pop(); acts.append("pops a finished list"); continue
        if isinstance(item,int):
            pending[0]=item; acts.append(f"finds {item}")
        else:
            stack.append(iter(item)); acts.append("enters a list" if item else "enters an empty list")
    return acts
st=[{"at":{"out":0},"vars":{"frames":len(stack),"value":"none"},"note":"Start: only the top-level list is on the stack, so frames is 1."}]
for k in range(3):
    acts=scan(); v=pending[0]; pending[0]=None; out.append(v)
    st.append({"at":{"out":len(out)},"vars":{"frames":len(stack),"value":v},"note":f"next() {', '.join(acts)} and returns {v}; frames is {len(stack)}."})
acts=scan(); assert pending[0] is None and not stack
st.append({"at":{"out":3},"vars":{"frames":0,"value":"none"},"note":f"hasNext() {', '.join(acts)} and answers false; frames is 0."})
assert out==[1,2,3]
assert [s["vars"]["frames"] for s in st]==[1,2,3,1,0]
fill(CH,F,block(out,["out"],st),"@@TRACE2@@")
