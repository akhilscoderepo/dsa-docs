from common import *
CH='41-algorithmic-services-and-simulations'; F='04-feed-aggregation.md'
import heapq
def merge():
    streams=[[9,6,2],[8,7],[5]]; k=5
    heap=[(-s[0],i,0) for i,s in enumerate(streams)]; heapq.heapify(heap)
    out=[]; cells=[f"pop {j+1}" for j in range(k)]; st=[]
    for j in range(k):
        front=" ".join(f"{-t}@{i}" for t,i,p in sorted(heap)) or "empty"
        t,i,p=heapq.heappop(heap); out.append(-t)
        if p+1<len(streams[i]): heapq.heappush(heap,(-streams[i][p+1],i,p+1))
        nf=" ".join(f"{-a}@{b}" for a,b,c in sorted(heap)) or "empty"
        st.append({"at":{"pop":j},"vars":{"frontier":nf,"output":",".join(map(str,out))},
          "note":f"Pop {j+1}: the heap held {front}, so the entry {-t}@{i} leaves and the output gains {-t}."+(f" Account {i} pushes its next post {streams[i][p+1]}." if p+1<len(streams[i]) else f" Account {i} has no older post, so it adds no entry.")})
    assert out==[9,8,7,6,5]
    return cells,st
def net():
    posts={}; fol={}; dead=set(); clock=[0]
    def feed(u,k):
        if u in dead: return []
        src={u}|{b for b in fol.get(u,set()) if b not in dead}
        al=sorted([(t,i) for a in src for (t,i) in posts.get(a,[])],reverse=True)
        return [i for t,i in al[:k]]
    calls=[("post",2,20),("post",1,10),("follow",1,2),("follow",1,1),("feed",1,5),("delete",2,None),("feed",1,5),("unfollow",1,2)]
    cells=[]; st=[]
    for k,(o,a,b) in enumerate(calls):
        if o=="post":
            posts.setdefault(a,[]).append((clock[0],b)); clock[0]+=1; r="true"; cells.append(f"post({a},{b})"); note=f"Call {k}: account {a} is live, so the post is stored."
        elif o=="follow":
            cells.append(f"follow({a},{b})")
            if a==b: r="false"; note=f"Call {k}: the ids are equal, so the call returns false and the follow set does not change."
            else: fol.setdefault(a,set()).add(b); r="true"; note=f"Call {k}: both accounts are live and the edge is new, so account {a} follows account {b}."
        elif o=="feed":
            cells.append(f"feed({a},{b})"); r=",".join(map(str,feed(a,b))); note=f"Call {k}: the visibility check admits "+(" and ".join(f"account {x}" for x in sorted({a}|{y for y in fol.get(a,set()) if y not in dead})))+f", so the merge returns {r}."
        elif o=="delete":
            dead.add(a); r="true"; cells.append(f"deleteUser({a})"); note=f"Call {k}: account {a} joins the deleted set, and no follow set changes."
        else:
            fol[a].remove(b); r="true"; cells.append(f"unfollow({a},{b})"); note=f"Call {k}: the stale edge to the deleted account {b} is removed from the follow set."
        fs="{"+",".join(map(str,sorted(fol.get(1,set()))))+"}"
        st.append({"at":{"call":k},"vars":{"follows":fs,"result":r},"note":note})
    return cells,st
c,s=merge(); fill(CH,F,block(c,["pop"],s),"@@TRACE1@@")
c,s=net(); fill(CH,F,block(c,["call"],s),"@@TRACE2@@")
