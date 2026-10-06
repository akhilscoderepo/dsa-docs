from common import *
from collections import deque
CH='21-graph-traversal-models-dfs-and-ordinary-bfs'; F='91-walk-a-grid-as-a-graph.md'
D8=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
def count8(grid,ph):
    R,C=len(grid),len(grid[0]); cells=[v for row in grid for v in row]; N=R*C
    vis=[False]*N; st=[]; count=0
    for s in range(N):
        if cells[s]!=1: continue
        if vis[s]:
            st.append({"at":{"scan":s,"cur":-1},"vars":{"count":str(count),"frontier":"[]"},
              "note":f"The scan reaches cell {s}. It holds land, but visited already marks it, so no new search starts."})
            continue
        count+=1; vis[s]=True; q=deque([s])
        st.append({"at":{"scan":s,"cur":-1},"vars":{"count":str(count),"frontier":str(list(q))},
          "note":f"Cell {s} is land and no search has reached it. It begins region {count} and enters the frontier."})
        k=0
        while q:
            cur=q.popleft(); r,c=divmod(cur,C); join=[]; diag=[]
            for j,(dr,dc) in enumerate(D8):
                nr,nc=r+dr,c+dc
                if 0<=nr<R and 0<=nc<C and grid[nr][nc]==1 and not vis[nr*C+nc]:
                    vis[nr*C+nc]=True; q.append(nr*C+nc); join.append(nr*C+nc)
                    if j>=4: diag.append(nr*C+nc)
            if join:
                body=f"cells {', '.join(map(str,join))} join the frontier"
                if diag: body+=f", and the corner contact brings in {', '.join(map(str,diag))}"
            else: body="no new cell qualifies"
            lead=[f"Cell {cur} leaves the frontier.",f"The search expands cell {cur}.",f"Next the search takes cell {cur}."][k%3]; k+=1
            st.append({"at":{"scan":s,"cur":cur},"vars":{"count":str(count),"frontier":str(list(q))},"note":f"{lead} Of its eight candidates, {body}."})
    st.append({"at":{"scan":N,"cur":-1},"vars":{"count":str(count),"frontier":"[]"},"note":f"The scan passes the last cell. The map holds {count} regions."})
    fill(CH,F,block(cells,["scan","cur"],st),ph); return count
assert count8([[1,0,0,1],[0,1,0,0],[0,0,1,1]],"@@TRACE1@@")==2
D4=[(1,0),(-1,0),(0,1),(0,-1)]
def clone(grid,ph):
    R,C=len(grid),len(grid[0]); cells=[v for row in grid for v in row]; N=R*C
    order=[(-1,0),(0,-1),(0,1),(1,0)]
    first=cells.index(1); copies={first:[]}; q=deque([first]); st=[]
    st.append({"at":{"cur":-1},"vars":{"copies":"1","frontier":str(list(q))},"note":f"The first land cell is {first}. Its copy is created at once and the cell enters the frontier."})
    k=0
    while q:
        cur=q.popleft(); r,c=divmod(cur,C); new=[]; old=[]
        for dr,dc in order:
            nr,nc=r+dr,c+dc
            if 0<=nr<R and 0<=nc<C and grid[nr][nc]==1:
                n=nr*C+nc
                if n in copies: old.append(n)
                else: copies[n]=[]; q.append(n); new.append(n)
                copies[cur].append(n)
        parts=[]
        if new: parts.append(f"cells {', '.join(map(str,new))} get new copies and enter the frontier")
        if old: parts.append(f"the copies of cells {', '.join(map(str,old))} exist already, so the walk only links to them")
        body="; ".join(parts) if parts else "the cell has no land neighbors"
        lead=[f"Cell {cur} leaves the frontier.",f"The walk expands cell {cur}."][k%2]; k+=1
        st.append({"at":{"cur":cur},"vars":{"copies":str(len(copies)),"frontier":str(list(q))},"note":f"{lead} Its copy now lists {copies[cur]}; {body}."})
    fill(CH,F,block(cells,["cur"],st),ph); return copies
r=clone([[1,1,0],[0,1,0],[1,0,1]],"@@TRACE2@@")
assert r=={0:[1],1:[0,4],4:[1]}
