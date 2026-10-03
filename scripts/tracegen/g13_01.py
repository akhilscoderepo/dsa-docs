from common import *
CH='13-deques-and-monotonic-queues'
F='01-arraydeque-mechanics.md'
CAP=6
class Ring:
    def __init__(s): s.a=["-"]*CAP; s.h=0; s.t=0
    def size(s): return (s.t-s.h)%CAP
    def line(s): return [s.a[(s.h+i)%CAP] for i in range(s.size())]
    def addLast(s,x): assert s.size()<CAP-1; s.a[s.t]=str(x); s.t=(s.t+1)%CAP
    def addFirst(s,x): assert s.size()<CAP-1; s.h=(s.h-1)%CAP; s.a[s.h]=str(x)
    def removeFirst(s): v=s.a[s.h]; s.a[s.h]="-"; s.h=(s.h+1)%CAP; return v
    def removeLast(s): s.t=(s.t-1)%CAP; v=s.a[s.t]; s.a[s.t]="-"; return v
def snap(r,note):
    return {"at":{"head":r.h,"tail":r.t},"vars":{"slots":"["+",".join(r.a)+"]","front_to_back":"["+",".join(r.line())+"]","size":r.size()},"note":note}
def run(ops):
    r=Ring(); steps=[snap(r,"The ring is empty, so head and tail are the same slot, 0.")]
    for op,x in ops:
        if op=="addLast":
            slot=r.t; r.addLast(x); steps.append(snap(r,f"addLast({x}) writes {x} in slot {slot} and moves the tail to slot {r.t}."))
        elif op=="addFirst":
            old=r.h; r.addFirst(x); wrap=" The head wrapped from slot 0 to the last slot, and no item moved." if old==0 else ""
            steps.append(snap(r,f"addFirst({x}) moves the head back from slot {old} to slot {r.h} and writes {x} there."+wrap))
        elif op=="removeFirst":
            slot=r.h; v=r.removeFirst(); steps.append(snap(r,f"removeFirst() takes {v} from slot {slot} and moves the head forward to slot {r.h}."))
        elif op=="removeLast":
            v=r.removeLast(); steps.append(snap(r,f"removeLast() moves the tail back to slot {r.t} and takes {v} from it."))
    return steps,r
ops1=[("addLast",4),("addLast",7),("addFirst",2),("removeLast",None)]
s1,r=run(ops1); assert r.line()==["2","4"] and r.h==5 and r.t==1
cells=["-"]*CAP
fill(CH,F,block(cells,["head","tail"],s1),"@@TRACE1@@")
# bounded history capacity 3
def hist(stream,cap):
    r=Ring(); steps=[snap(r,"The history is empty.")]
    for x in stream:
        slot=r.t; r.addLast(x)
        steps.append(snap(r,f"Append {x} at slot {slot}. The history holds {r.size()} items."))
        if r.size()>cap:
            ev=r.removeFirst()
            steps.append(snap(r,f"The size {r.size()+1} is above the capacity {cap}, so the oldest item {ev} is removed from the front."))
    return steps,r
s2,r=hist([5,6,7,8],3); assert r.line()==["6","7","8"]
fill(CH,F,block(cells,["head","tail"],s2),"@@TRACE2@@")
