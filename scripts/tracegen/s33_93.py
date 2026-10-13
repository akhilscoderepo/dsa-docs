from common import *
CH='33-design-data-structure-problems'; F='93-iterator-api-state.md'

# Trace 1: spine stack on the tree 6(2(1,4(3,-)),9(8,-)).
T={6:(2,9),2:(1,4),4:(3,None),9:(8,None),1:(None,None),3:(None,None),8:(None,None)}
def spine(n,st):
    while n is not None:
        st.append(n); n=T[n][0]
cells=[1,2,3,4,6,8,9]
st=[]; spine(6,st)
steps=[{"at":{"next":0},"vars":{"stack":str(st),"depth":len(st)},"note":f"The constructor pushes the left spine. The stack holds {st} and the top, {st[-1]}, is the next value."}]
out=[]
for k in range(len(cells)):
    top=st.pop(); out.append(top); spine(T[top][1],st)
    nxt=k+1
    note=f"next() pops {top} and pushes the left spine of its right child. Returned so far: {out}."
    steps.append({"at":{"next":nxt},"vars":{"returned":top,"stack":str(st),"depth":len(st)},"note":note})
assert out==cells and st==[] and steps[-1]["vars"]["depth"]==0
fill(CH,F,block(cells,["next"],steps),"@@TRACE1@@")

# Trace 2: cached head over a source holding 4, 7, 9.
src=[4,7,9]; pulled=0; head=None; calls=0
steps=[{"at":{"pulled":0},"vars":{"head":"empty","calls":0},"note":"Start: the slot is empty and the source has not been called."}]
def snap(op,note,res):
    steps.append({"at":{"pulled":pulled},"vars":{"op":op,"result":res,"head":"empty" if head is None else head,"calls":calls},"note":note})
def peek():
    global pulled,head,calls
    if head is None:
        head=src[pulled]; pulled+=1; calls+=1; return head,f"peek() finds the slot empty and pulls {head}. The source call count is {calls}."
    return head,f"peek() finds the slot full and returns {head} with no source call. The count stays {calls}."
def nxt():
    global pulled,head,calls
    if head is not None:
        v=head; head=None; return v,f"next() returns the cached {v} and empties the slot. The count stays {calls}."
    v=src[pulled]; pulled+=1; calls+=1; return v,f"next() finds the slot empty and pulls {v} directly. The count is {calls}."
def hn():
    r=head is not None or pulled<len(src)
    return r,f"hasNext() answers {str(r).lower()} from the slot and the source, with no pull. The count stays {calls}."
res=[]
for op in ["peek","peek","next","hasNext","next","peek","next","hasNext"]:
    f={"peek":peek,"next":nxt,"hasNext":hn}[op]
    r,note=f(); res.append(r); snap(op+"()",note,str(r).lower() if isinstance(r,bool) else r)
assert res==[4,4,4,True,7,9,9,False] and calls==3
fill(CH,F,block(src,["pulled"],steps),"@@TRACE2@@")
