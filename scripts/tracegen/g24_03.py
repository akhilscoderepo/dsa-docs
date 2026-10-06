from common import *
import heapq
CH='24-shortest-paths-and-graph-state-modeling'
F='03-node-state-search.md'
INF=10**18

def fmt(dist,n):
    return " ".join("%d:%s/%s"%(v,"-" if dist[2*v]>=INF else dist[2*v],"-" if dist[2*v+1]>=INF else dist[2*v+1]) for v in range(n))

def coupon(n,edges,src,dst):
    out=[[] for _ in range(n)]
    for u,v,w in edges: out[u].append((v,w))
    dist=[INF]*(2*n); dist[2*src]=0
    pq=[(0,2*src)]; steps=[]
    while pq:
        c,ix=heapq.heappop(pq)
        if c>dist[ix]: continue
        u,used=divmod(ix,2)
        for v,w in out[u]:
            if c+w<dist[2*v+used]: dist[2*v+used]=c+w; heapq.heappush(pq,(c+w,2*v+used))
            if used==0 and c+w//2<dist[2*v+1]: dist[2*v+1]=c+w//2; heapq.heappush(pq,(c+w//2,2*v+1))
        steps.append({"at":{"cur":u},"vars":{"pop":"node %d, coupon %s, cost %d"%(u,"used" if used else "unused",c),"dist":fmt(dist,n)},
            "note":"The search removes the entry of node %d with the coupon %s at cost %d and relaxes its edges."%(u,"used" if used else "unused",c)})
    return min(dist[2*dst],dist[2*dst+1]),steps

def alt(n,red,blue):
    adj=[[[] for _ in range(n)] for _ in range(2)]
    for a,b in red: adj[0][a].append(b)
    for a,b in blue: adj[1][a].append(b)
    names=["red","blue","start"]
    dist=[[-1]*3 for _ in range(n)]; dist[0][2]=0
    q=[(0,2)]; steps=[]; h=0
    def show():
        return " ".join("%d:%s"%(v,"/".join("-" if x<0 else str(x) for x in dist[v])) for v in range(n))
    while h<len(q):
        u,last=q[h]; h+=1
        new=[]
        for c in range(2):
            if c==last: continue
            for v in adj[c][u]:
                if dist[v][c]<0:
                    dist[v][c]=dist[u][last]+1; q.append((v,c)); new.append("(%d,%s)"%(v,names[c]))
        steps.append({"at":{"cur":u},"vars":{"pop":"node %d, last %s, distance %d"%(u,names[last],dist[u][last]),"dist":show()},
            "note":"The search removes the position of node %d with last color %s and adds %s."%(u,names[last],", ".join(new) if new else "no new position")})
    ans=[]
    for v in range(n):
        xs=[x for x in dist[v] if x>=0]; ans.append(min(xs) if xs else -1)
    return ans,steps

g=[(0,1,8),(1,2,2),(2,3,100),(0,2,30)]
best,st=coupon(4,g,0,3); assert best==60,best
fill(CH,F,block([0,1,2,3],["cur"],st),"@@TRACE1@@")
ans,st2=alt(4,[(0,1),(0,2),(2,3)],[(1,2),(1,0)],) ; assert ans==[0,1,1,3],ans
fill(CH,F,block([0,1,2,3],["cur"],st2),"@@TRACE2@@")
if __name__=="__main__":
    for s in st+st2: print(s["vars"],s["note"])
