from common import *
CH='14-linked-lists'; F='91-copy-a-list-with-random-links.md'
def run(vals,rnd,ph):
    n=len(vals); steps=[]
    mp=0
    def links(done):
        out=[]
        for i in range(done):
            nx = i+1 if i+1<n else None
            out.append(f"{i}:next={nx if nx is not None else 'null'},random={rnd[i] if rnd[i] is not None else 'null'}")
        return " ".join(out) if out else "none"
    steps.append({"at":{"curr":0},"vars":{"map":0,"links":"none"},"note":"Start: the map is empty, and curr is the first original node."})
    for i in range(n):
        mp+=1
        nxt=i+1 if i+1<n else -1
        steps.append({"at":{"curr":nxt},"vars":{"map":mp,"links":"none"},"note":f"First pass: a new node for the original node {vals[i]} is stored in the map. The map holds {mp} entries."})
    for i in range(n):
        nxt=i+1 if i+1<n else -1
        r = "null" if rnd[i] is None else f"the copy of the node {vals[rnd[i]]}"
        steps.append({"at":{"curr":i},"vars":{"map":mp,"links":links(i+1)},"note":f"Second pass at the node {vals[i]}: next becomes "+("the copy of the node "+str(vals[i+1]) if i+1<n else "null")+f", and random becomes {r}. Every lookup finds an entry."})
    return steps
v=[5,8,2]; r=[2,None,0]
fill(CH,F,block(v,["curr"],run(v,r,1)),"@@TRACE1@@")
v=[4,6,9]; r=[0,2,2]
s=run(v,r,2)
s[-1]["note"]+=" The node 9 is the target of two random links and still has one copy."
fill(CH,F,block(v,["curr"],s),"@@TRACE2@@")
