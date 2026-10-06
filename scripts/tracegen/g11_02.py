from common import *
from collections import deque
CH='11-stacks-and-queues'
F='02-fifo-simulation.md'
pages=[3,1,2]
left=pages[:]; q=deque(range(3)); st=[]; order=[]
def qs(): return "["+",".join(f"{j}:{left[j]}" for j in q)+"]"
while q:
    j=q.popleft(); left[j]-=1
    if left[j]==0:
        order.append(j); note=f"The job at position {j} prints its last page, so it finishes and leaves the line for good."
    else:
        q.append(j); note=f"The job at position {j} prints one page and goes to the back of the line with {left[j]} left."
    st.append({"at":{"front":j},"vars":{"line":qs(),"finished":str(order).replace(' ','')},"note":note})
assert order==[1,2,0]
fill(CH,F,block(pages,["front"],st),"@@TRACE1@@")
students=[1,1,1,0]; sand=[0,0,1,1]
line=deque(students); sandwichAt=0; spins=0; st=[]
def ls(): return "["+",".join(map(str,line))+"]"
while line and sandwichAt<len(sand) and spins<len(line):
    w=line.popleft(); at=sandwichAt
    if w==sand[sandwichAt]:
        note=f"The front student wants type {w}, which matches the sandwichAt sandwich, so the student eats and the next sandwich is offered."
        sandwichAt+=1; spins=0
    else:
        line.append(w); spins+=1
        note=f"The front student wants type {w}, but the sandwichAt sandwich is type {sand[at]}, so the student goes to the back and the rejection count is {spins}."
    st.append({"at":{"sandwichAt":min(sandwichAt,len(sand)-1) if w!=sand[at] else at},"vars":{"queue":ls(),"spins":spins},"note":note})
assert len(line)==3 and spins==3
st[-1]["note"]+=" That equals the number of students waiting, so a full rotation made no progress and the line is stuck."
fill(CH,F,block(sand,["sandwichAt"],st),"@@TRACE2@@")
