from common import *
import heapq
CH='24-shortest-paths-and-graph-state-modeling'
F='03-node-state-search.md'
def pairs(n,edges,src,dst):
    out=[[] for _ in range(n)]
    for u,v,w in edges: out[u].append((v,w))
    INF=10**18
    fare=[INF]*(2*n); fare[src*2]=0
    pq=[(0,src*2)]; order=[]; steps=[]; stale=0
    while pq:
        c,ix=heapq.heappop(pq)
        if c>fare[ix]: stale+=1; continue
        order.append(ix); u,sp=divmod(ix,2)
        for v,w in out[u]:
            if c+w<fare[v*2+sp]: fare[v*2+sp]=c+w; heapq.heappush(pq,(c+w,v*2+sp))
            if sp==0 and c<fare[v*2+1]: fare[v*2+1]=c; heapq.heappush(pq,(c,v*2+1))
        steps.append((ix,c,stale,len(pq)))
    return fare,order,steps
g=[[0,1,4],[0,2,9],[1,2,3],[1,3,12],[2,3,6],[2,4,20],[3,4,7]]
fare,order,steps=pairs(5,g,0,4)
assert min(fare[8],fare[9])==7 and fare[9]==7 and fare[8]==20
lab=lambda ix:f"{ix//2}/{'spent' if ix%2 else 'open'}"
cells=[lab(ix) for ix in order]
st=[]
for i,(ix,c,s,w) in enumerate(steps):
    st.append({"at":{"cur":i},"vars":{"fare":c,"stale":s,"waiting":w},"note":f"Pair {lab(ix)} is settled at fare {c}; {w} entr"+("y" if w==1 else "ies")+" now wait."+(" The lighthouse is settled here with the coupon spent." if ix==9 and c==7 else "")})
fill(CH,F,block(cells,["cur"],st),"@@TRACE1@@")
# trace 2: node-only
h=[[0,1,3],[1,2,10],[2,3,4],[0,4,6],[4,2,9]]
out=[[] for _ in range(5)]
for u,v,w in h: out[u].append((v,w))
pq=[(0,0,0)]; done=set(); seq=[]
while pq:
    c,f,u=heapq.heappop(pq)
    if u in done: continue
    done.add(u); seq.append((u,c,f))
    for v,w in out[u]:
        heapq.heappush(pq,(c+w,f,v))
        if f==0: heapq.heappush(pq,(c,1,v))
fl,_,_=pairs(5,h,0,3)
assert min(fl[6],fl[7])==7 and dict((u,c) for u,c,f in seq)[3]==13
st=[]
for i,(u,c,f) in enumerate(seq):
    st.append({"at":{"cur":i},"vars":{"fare":c,"spent":f},"note":f"Stop {u} is settled once at fare {c} with the coupon "+("spent" if f else "in hand")+"; no other arrival there is kept."+(" The answer is wrong here: the pair search gets 7." if u==3 else "")})
fill(CH,F,block([u for u,c,f in seq],["cur"],st),"@@TRACE2@@")
print(cells,seq)
