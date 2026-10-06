from common import *
CH='14-linked-lists'; F='04-merge.md'
def run(A,B,ph):
    cells=A+B; na=len(A)
    a=0 if A else -1; b=na if B else -1
    nxtA=lambda i: i+1 if i+1<na else -1
    nxtB=lambda i: i+1 if i+1<len(cells) else -1
    out=[]; st=[]; tail=-1
    def snap(note): st.append({"at":{"a":a,"b":b,"tail":tail},"vars":{"merged":",".join(map(str,out)) or "empty"},"note":note})
    snap("Start: both lists have unplaced nodes, and the finalized prefix is empty.")
    first=True
    while a!=-1 and b!=-1:
        if cells[b]<cells[a]:
            v=cells[b]; out.append(v); tail=b; b=nxtB(b); src="second"
        else:
            v=cells[a]; out.append(v); tail=a; a=nxtA(a); src="first"
        cmp=f"Compare {cells[tail] if False else ''}".strip()
        snap(f"The smaller head is the node {v} of the {src} list, so it joins the finalized prefix and that list advances.")
    rest=[]
    while a!=-1: rest.append(cells[a]); tail_=a; a=nxtA(a)
    while b!=-1: rest.append(cells[b]); b=nxtB(b)
    out.extend(rest); 
    snap(f"One list is empty. One write attaches the remainder {','.join(map(str,rest))}, and no comparison is made with it.")
    return st,out
A,B=[1,4,6],[2,3,7]
s,o=run(A,B,1); assert o==sorted(A+B)
fill(CH,F,block(A+B,["a","b","tail"],s),"@@TRACE1@@")
A,B=[1,2],[5,6,7]
s,o=run(A,B,2); assert o==sorted(A+B)
fill(CH,F,block(A+B,["a","b","tail"],s),"@@TRACE2@@")
