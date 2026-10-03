from common import *
CH='11-stacks-and-queues'
F='03-two-stack-queue.md'
def run(script,labels):
    inn=[];out=[];st=[];res=[]
    for i,s in enumerate(script):
        note=None
        if s>=0:
            inn.append(s); note=f"The value {s} goes on top of the input stack, behind everything already in the queue."
        else:
            moved=False
            if not out:
                if inn:
                    n=len(inn)
                    while inn: out.append(inn.pop())
                    moved=True
            if s==-1:
                v=out.pop(); res.append(v)
                note=(f"The output stack was empty, so the transfer rule moves all {n} value(s) over, and the removal returns {v}, the oldest." if moved else f"The output stack is not empty, so no transfer happens and the removal returns {v}.")
            else:
                v=out[-1]
                note=(f"The output stack was empty, so the transfer rule runs first, and the peek reads {v}." if moved else f"The output stack is not empty, so the peek reads {v} without moving anything.")
        st.append({"at":{"op":i},"vars":{"input":str(inn).replace(' ',''),"output":str(out).replace(' ','')},"note":note})
    return st,res
sc=[1,2,3,-1,-1]
cells=["enq 1","enq 2","enq 3","deq","deq"]
st,res=run(sc,cells); assert res==[1,2]
fill(CH,F,block(cells,["op"],st),"@@TRACE1@@")
sc=[5,6,-1,7,8,-1,-1]
cells=["enq 5","enq 6","deq","enq 7","enq 8","deq","deq"]
st,res=run(sc,cells); assert res==[5,6,7]
assert "not empty" in st[5]["note"] and "transfer rule moves all 2" in st[6]["note"]
fill(CH,F,block(cells,["op"],st),"@@TRACE2@@")
