from common import *
CH='36-stateful-containers-and-histories'; F='05-cursor-histories.md'

class Hist:
    """Array plus cursor plus live length; records a trace step after each call."""
    def __init__(s, home, cap):
        s.items=[home]+[None]*(cap-1); s.cursor=0; s.live=1; s.steps=[]
        s.rec("The history starts with the homepage in slot 0, so the cursor is 0 and the live length is 1.")
    def rec(s, note):
        shown=",".join(x if x else "-" for x in s.items)
        s.steps.append({"at":{"cursor":s.cursor,"live":s.live},"vars":{"slots":shown},"note":note})
    def visit(s, u):
        s.cursor+=1; s.items[s.cursor]=u; s.live=s.cursor+1
        s.rec(f"visit({u}): the cursor moves to slot {s.cursor}, the page is written there, and the live length becomes {s.live}.")
    def back(s, k):
        old=s.cursor; s.cursor=max(0,s.cursor-k)
        s.rec(f"back({k}): the target {old - k} is {'below 0, so the clamp stops the cursor at 0' if old-k<0 else 'inside the live range'}. The cursor moves from {old} to {s.cursor}; no slot changes.")
        return s.items[s.cursor]
    def forward(s, k):
        old=s.cursor; s.cursor=min(s.live-1,s.cursor+k)
        s.rec(f"forward({k}): the target {old + k} is {'past the last live slot, so the clamp stops the cursor at '+str(s.live-1) if old+k>s.live-1 else 'inside the live range'}. The cursor moves from {old} to {s.cursor}; the live length stays {s.live}.")
        return s.items[s.cursor]

# Oracle: list with real truncation.
class Ref:
    def __init__(s,h): s.l=[h]; s.i=0
    def visit(s,u): del s.l[s.i+1:]; s.l.append(u); s.i+=1
    def back(s,k): s.i=max(0,s.i-k); return s.l[s.i]
    def forward(s,k): s.i=min(len(s.l)-1,s.i+k); return s.l[s.i]

h=Hist("H",6); r=Ref("H")
for op,a in [("visit","A"),("visit","B"),("visit","C"),("back",2),("visit","D")]:
    got=getattr(h,op)(a); exp=getattr(r,op)(a); assert got==exp
assert h.items[:4]==["H","A","D","C"] and h.live==3 and h.cursor==2
h.steps[-1]["note"]+=" Slot 3 still holds C, but the live length 3 hides it."
t1=block([str(i) for i in range(6)],["cursor","live"],h.steps)
fill(CH,F,t1,"@@TRACE1@@")

# Trace 2 continues from the final state of trace 1.
h.steps=[]; h.rec("The state after the first trace: cursor 2, live length 3, and the old page C still sits in slot 3.")
for op,a in [("forward",5),("back",9),("forward",1),("visit","E")]:
    got=getattr(h,op)(a); exp=getattr(r,op)(a); assert got==exp
assert h.items[:4]==["H","A","E","C"] and h.live==3 and h.cursor==2
h.steps[-1]["note"]+=" The write replaced D in slot 2; slot 3 is still unreachable."
fill(CH,F,block([str(i) for i in range(6)],["cursor","live"],h.steps),"@@TRACE2@@")

# Examples for the exercises (recomputed here).
def run(cls,ops):
    out=[]
    for o,a in ops: out.append(getattr(cls,o)(*a))
    return out
class U:
    def __init__(s): s.s=[""]; s.i=0
    def append(s,c): s.s=s.s[:s.i+1]; s.s.append(s.s[s.i]+c); s.i+=1
    def undo(s,k): m=min(k,s.i); s.i-=m; return m
    def redo(s,k): m=min(k,len(s.s)-1-s.i); s.i+=m; return m
    def text(s): return s.s[s.i]
print("U1",run(U(),[("append","h"),("append","i"),("append","!"),("undo",2),("text",()),("append","o"),("text",()),("undo",1),("redo",1),("text",())] ) if False else "")
u=U(); 
for c in "hi!": u.append(c)
u.undo(2); a=u.text(); u.append("o"); b=u.text(); u.undo(1); u.redo(1); print("B1",a,b,u.text())
u=U()
for c in "abcd": u.append(c)
u.undo(3); u.redo(2); a=u.text(); u.append("e"); b=u.text(); u.undo(4); print("B2",a,b,repr(u.text()))
u=U(); u.append("a"); u.append("b"); print("O1",u.undo(2**31-1),repr(u.text()),u.redo(2**31-1),u.text(),u.undo(1),end=" "); u.append("c"); print(u.redo(5),u.text())
u=U(); print("O2",u.undo(5)); u.append("z"); print(u.redo(2**31-1),u.text(),u.undo(0))
r=Ref("start.com"); o=[]
for op,a in [("visit","a.com"),("visit","b.com"),("visit","c.com"),("back",1),("back",1),("visit","d.com"),("forward",2),("back",3),("forward",1)]:
    o.append(getattr(r,op)(a))
print("V1",o)
r=Ref("x"); o=[]
for op,a in [("visit","y"),("visit","z"),("back",5),("forward",1),("visit","w"),("forward",1),("back",1),("forward",9)]:
    o.append(getattr(r,op)(a))
print("V2",o)
class Ed:
    def __init__(s): s.t=""; s.p=0
    def add(s,x): s.t=s.t[:s.p]+x+s.t[s.p:]; s.p+=len(x)
    def dele(s,k): m=min(k,s.p); s.t=s.t[:s.p-m]+s.t[s.p:]; s.p-=m; return m
    def left(s,k): s.p-=min(k,s.p); return s.t[max(0,s.p-10):s.p]
    def right(s,k): s.p+=min(k,len(s.t)-s.p); return s.t[max(0,s.p-10):s.p]
e=Ed(); o=[]
for op,a in [("add","hello"),("add","world"),("left",3),("dele",4),("add","xyz"),("right",20),("left",2),("dele",50),("left",5)]:
    o.append(getattr(e,op)(a))
print("E1",o,repr(e.t),e.p)
e=Ed(); o=[]
for op,a in [("add","abcdefghijklmn"),("left",1),("left",12),("right",100),("dele",3),("left",2)]:
    o.append(getattr(e,op)(a))
print("E2",o)
