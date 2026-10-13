from common import *
import heapq
CH='35-advanced-search-sampling-and-geometric-state'; N='92-a-star-heuristics.md'
def graph():
    n=7; pos=[(0,0),(4,1),(3,3),(2,2),(1,3),(0,1),(4,0)]
    E=[(2,4,3),(0,5,2),(0,3,6),(3,5,4),(2,6,5),(5,6,7),(3,4,4),(5,4,3),(4,2,2),(6,1,1),(3,6,4)]
    goal=6; adj=[[] for _ in range(n)]
    for u,v,w in E: adj[u].append((v,w))
    h=[abs(p[0]-pos[goal][0])+abs(p[1]-pos[goal][1]) for p in pos]
    best=[10**9]*n; best[0]=0; pq=[(h[0],0,0)]
    st=[{"at":{"cur":-1},"vars":{"queue":f"vertex 0 (f {h[0]})"},"note":f"Start: vertex 0 has cost 0 and guess {h[0]}, so its priority is {h[0]}."}]
    pops=0
    while pq:
        f,u,g=heapq.heappop(pq)
        if g>best[u]: continue
        pops+=1
        if u==goal:
            st.append({"at":{"cur":u},"vars":{"g":g,"f":f,"pops":pops},"note":f"The goal pops with cost {g} after {pops} finalized vertices. The first goal pop is optimal."}); break
        for v,w in adj[u]:
            if g+w<best[v]: best[v]=g+w; heapq.heappush(pq,(best[v]+h[v],v,best[v]))
        q=", ".join(f"{b} (f {a})" for a,b,_ in sorted(pq))
        st.append({"at":{"cur":u},"vars":{"g":g,"h":h[u],"f":f,"queue":q},"note":f"Vertex {u} pops with cost {g}, guess {h[u]} and priority {f}. Its edges push or improve the entries in the queue."})
    assert pops==3 and best[6]==9
    fill(CH,N,block([str(i) for i in range(n)],["cur"],st),"@@TRACE1@@")
def grid():
    cost=[[2,2,9,1],[1,1,2,1]]; H=[[0,1,2,0],[3,0,1,0]]; R,C=2,4; g=(1,3)
    D=[(-1,0),(1,0),(0,-1),(0,1)]; best=[[10**9]*C for _ in range(R)]; best[0][0]=0; closed=set(); pq=[(0,0,0,0)]
    cells=[str(x) for row in cost for x in row]
    st=[{"at":{"cur":-1},"vars":{"queue":"cell 0 (f 0)"},"note":"Start: the top left cell has cost 0 and guess 0."}]; reop=0
    while pq:
        f,r,c,gv=heapq.heappop(pq)
        if gv>best[r][c]: continue
        again=(r,c) in closed; reop+=again; closed.add((r,c))
        if (r,c)==g:
            st.append({"at":{"cur":r*C+c},"vars":{"g":gv,"f":f,"reopened":reop},"note":f"The goal pops with cost {gv}. The search expanded {reop} cell a second time."}); break
        for dr,dc in D:
            nr,nc=r+dr,c+dc
            if 0<=nr<R and 0<=nc<C and gv+cost[nr][nc]<best[nr][nc]:
                best[nr][nc]=gv+cost[nr][nc]; heapq.heappush(pq,(best[nr][nc]+H[nr][nc],nr,nc,best[nr][nc]))
        note=f"Pop row {r}, column {c} with cost {gv} and priority {f}."
        if again: note+=" The cell was expanded before, and this entry has a smaller cost, so the search reopens it."
        st.append({"at":{"cur":r*C+c},"vars":{"g":gv,"f":f,"reopened":reop},"note":note})
    assert reop==1 and gv==5
    fill(CH,N,block(cells,["cur"],st),"@@TRACE2@@")
graph(); grid()
