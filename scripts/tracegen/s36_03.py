from common import *
CH='36-stateful-containers-and-histories'; F='03-circular-buffers.md'
def show(slots, live):
    return ",".join(str(slots[i]) if i in live else "_" for i in range(len(slots)))
# Simulates a bounded deque on cap slots and records one step per call.
class D:
    def __init__(s,cap): s.cap=cap; s.slots=[None]*cap; s.head=0; s.size=0
    def live(s): return {(s.head+i)%s.cap for i in range(s.size)}
    def nxt(s): return (s.head+s.size)%s.cap
    def step(s,note): return {"at":{"head":s.head,"next":s.nxt()},"vars":{"slots":show(s.slots,s.live()),"size":s.size},"note":note}
# Trace 1: FIFO of capacity 4.
q=D(4); st=[q.step("The buffer is empty: size is 0, head is 0, and the write position next is (0 + 0) % 4 = 0.")]
def offer(v):
    if q.size==q.cap:
        st.append(q.step(f"offer({v}) is rejected because size equals the capacity 4. head, size and every slot stay as they were; here next equals head, so only size shows that the buffer is full.")); return False
    pos=q.nxt(); q.slots[pos]=v; q.size+=1
    extra=" The position wrapped past the end of the array to slot 0." if pos==0 and q.size>1 else ""
    st.append(q.step(f"offer({v}) writes slot {pos}, the position (head + size) % 4 computed before the add, and size becomes {q.size}.{extra}")); return True
def poll():
    v=q.slots[q.head]; old=q.head; q.head=(q.head+1)%q.cap; q.size-=1
    st.append(q.step(f"poll() returns {v} from slot {old}, moves head to (head + 1) % 4 = {q.head} and lowers size to {q.size}. No item is copied.")); return v
for v in (10,20,30,40): assert offer(v)
assert not offer(50)
assert poll()==10
assert offer(50)
assert poll()==20 and poll()==30
assert q.head==3 and q.size==2 and q.slots==[50,20,30,40]
fill(CH,F,block(["0","1","2","3"],["head","next"],st),"@@TRACE1@@")
# Trace 2: deque of capacity 3.
q=D(3); st=[q.step("The deque is empty: size is 0, head is 0 and next is 0.")]
def ins_last(v):
    pos=q.nxt(); q.slots[pos]=v; q.size+=1
    st.append(q.step(f"insertLast({v}) writes slot (head + size) % 3 = {pos} and size becomes {q.size}."))
def ins_front(v):
    old=q.head; q.head=(q.head-1+q.cap)%q.cap; q.slots[q.head]=v; q.size+=1
    st.append(q.step(f"insertFront({v}) moves head from {old} to (head - 1 + 3) % 3 = {q.head}, writes slot {q.head} and size becomes {q.size}."))
def order(): return [q.slots[(q.head+i)%q.cap] for i in range(q.size)]
ins_last(1); ins_front(2); ins_last(3)
assert order()==[2,1,3] and q.slots==[1,3,2]
assert q.nxt()==q.head
old=q.head; v=q.slots[q.head]; q.head=(q.head+1)%3; q.size-=1
st.append(q.step(f"deleteFront() returns {v} from slot {old}, moves head to {q.head} and lowers size to {q.size}."))
r=(q.head+q.size-1)%3
st.append(q.step(f"getRear() reads slot (head + size - 1) % 3 = {r}, which holds {q.slots[r]}. No field changes."))
assert order()==[1,3] and q.slots[r]==3
fill(CH,F,block(["0","1","2"],["head","next"],st),"@@TRACE2@@")
