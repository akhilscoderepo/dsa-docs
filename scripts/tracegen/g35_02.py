import sys
sys.path.insert(0,'/tmp/s35') if False else None
from common import *
import heapq
CH='35-advanced-search-sampling-and-geometric-state'; N='02-a-star-search.md'
D=[(-1,0),(1,0),(0,-1),(0,1)]
def run(cost,s,g,expect,ph,stale_needed):
    R,C=len(cost),len(cost[0]); INF=10**9
    best=[[INF]*C for _ in range(R)]; h=lambda r,c:abs(r-g[0])+abs(c-g[1])
    best[s[0]][s[1]]=0; pq=[(h(*s),s[0],s[1],0)]
    cells=[str(x) for row in cost for x in row]
    st=[{"at":{"cur":-1},"vars":{"queue":1,"best":"start 0"},"note":f"Start: the start cell has g 0 and f {h(*s)}, the Manhattan distance."}]
    exp=0; stale=0
    while pq:
        f,r,c,gv=heapq.heappop(pq); idx=r*C+c
        if gv>best[r][c]:
            stale+=1
            st.append({"at":{"cur":idx},"vars":{"g":gv,"best":best[r][c],"f":f,"queue":len(pq)},"note":f"The entry for row {r}, column {c} has g {gv}, but best is {best[r][c]}. The entry is stale, so the planner skips it."}); continue
        exp+=1
        if (r,c)==g:
            st.append({"at":{"cur":idx},"vars":{"g":gv,"f":f,"queue":len(pq)},"note":f"The goal pops with g {gv}. The first goal pop is optimal, so the search returns {gv} after {exp} expansions."}); assert gv==expect; break
        pushed=0
        for dr,dc in D:
            nr,nc=r+dr,c+dc
            if 0<=nr<R and 0<=nc<C and cost[nr][nc]>0 and gv+cost[nr][nc]<best[nr][nc]:
                best[nr][nc]=gv+cost[nr][nc]; pushed+=1
                heapq.heappush(pq,(best[nr][nc]+h(nr,nc),nr,nc,best[nr][nc]))
        st.append({"at":{"cur":idx},"vars":{"g":gv,"f":f,"pushed":pushed,"queue":len(pq)},"note":f"Pop row {r}, column {c} with g {gv} and f {f}. Push {pushed} neighbour entries."})
    assert (stale>=1)==stale_needed
    fill(CH,N,block(cells,["cur"],st),ph)
run([[1,1,1,2],[0,1,0,1],[0,1,1,1]],(0,0),(2,3),5,"@@TRACE1@@",False)
run([[1,4,1,1],[1,1,3,3]],(0,0),(1,3),8,"@@TRACE2@@",True)
