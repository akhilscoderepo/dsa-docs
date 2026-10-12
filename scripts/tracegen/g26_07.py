from common import *
CH='26-dynamic-programming-foundations'
F='07-grid-dp.md'
def routes3(blocked):
    R,C=len(blocked),len(blocked[0]); dp=[[0]*C for _ in range(R)]; steps=[]
    for r in range(R):
        for c in range(C):
            if blocked[r][c]: w=0; why="is a shelf, so it stores 0"
            elif r==c==0: w=1; dp[r][c]=1; why="is the start, so it stores 1"
            else:
                parts=[]
                if r>0: parts.append(dp[r-1][c])
                if c>0: parts.append(dp[r][c-1])
                if r>0 and c>0: parts.append(dp[r-1][c-1])
                w=sum(parts); why="adds %d predecessor entr%s %s and stores %d"%(len(parts),"y" if len(parts)==1 else "ies","+".join(map(str,parts)),w)
            dp[r][c]=w
            steps.append({"at":{"cell":r*C+c},"vars":{"row":r,"col":c,"ways":w},"note":"Cell (%d, %d) %s."%(r,c,why)})
    return dp,steps
def brute3(blocked,r,c):
    if r<0 or c<0 or blocked[r][c]: return 0
    if r==c==0: return 1
    return brute3(blocked,r-1,c)+brute3(blocked,r,c-1)+brute3(blocked,r-1,c-1)
b1=[[False]*4,[False,True,False,False],[False]*4]
dp,steps=routes3(b1)
assert dp[2][3]==brute3(b1,2,3)==dp[-1][-1]
steps[-1]['note']+=" The answer is %d."%dp[2][3]
cells=["(%d,%d)"%(r,c) for r in range(3) for c in range(4)]
fill(CH,F,block(cells,["cell"],steps),"@@TRACE1@@")
print(dp)
g=[[2,-1,3,0],[1,4,-2,2],[-3,2,5,-1]]
R,C=3,4; best=[[0]*C for _ in range(R)]; st=[]
for r in range(R):
    for c in range(C):
        if r==c==0: v=g[0][0]; why="is the start, so it stores its own gain %d"%v
        else:
            pr=[]
            if r>0: pr.append(best[r-1][c])
            if c>0: pr.append(best[r][c-1])
            m=max(pr); v=m+g[r][c]; why="takes the larger predecessor %d and adds its own gain %d, storing %d"%(m,g[r][c],v)
        best[r][c]=v
        st.append({"at":{"cell":r*C+c},"vars":{"row":r,"col":c,"gain":v},"note":"Cell (%d, %d) %s."%(r,c,why)})
def bf(r,c): 
    if r==c==0: return g[0][0]
    return g[r][c]+max(bf(r-1,c) if r>0 else -10**9, bf(r,c-1) if c>0 else -10**9)
assert best[-1][-1]==bf(R-1,C-1)
st[-1]['note']+=" The best total is %d."%best[-1][-1]
fill(CH,F,block(cells,["cell"],st),"@@TRACE2@@")
# exercise examples
print(routes3([[False]*3]*2)[0], routes3([[False]*3,[False,True,False],[False]*3])[0][-1][-1])
def mg(g):
    R,C=len(g),len(g[0]);b=[[0]*C for _ in range(R)]
    for r in range(R):
        for c in range(C):
            pr=[]
            if r:pr.append(b[r-1][c])
            if c:pr.append(b[r][c-1])
            b[r][c]=g[r][c]+(max(pr) if pr else 0)
    return b[-1][-1]
print(mg([[2,-1,3],[1,4,-2],[-3,2,5]]),mg([[-5,-2],[-7,-9]]))
