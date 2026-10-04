from common import *
from collections import deque
CH='22-bfs-variations'
F='04-state-space-bfs.md'
def nb(s):
    o=[]
    for i,ch in enumerate(s):
        d=int(ch)
        for n in ((d+9)%10,(d+1)%10): o.append(s[:i]+str(n)+s[i+1:])
    return o
# trace 1: strings
start,code,worn='00','21',{'10','11'}
clicks={start:0}; q=deque([start]); order=[]; info=[]; found=None
while q and found is None:
    cur=q.popleft(); order.append(cur); added=[]
    for n in nb(cur):
        if n in worn or n in clicks: continue
        clicks[n]=clicks[cur]+1; q.append(n); added.append(n)
        if n==code: found=n
    info.append((cur,clicks[cur],len(q),added))
assert found==code and clicks[code]==5, clicks[code]
assert info[0][3]==['90','09','01']
steps=[]
for i,(cur,k,ql,added) in enumerate(info):
    note=f"State {cur} is expanded at {k} click"+("s" if k!=1 else "")+"; "+(f"it adds {', '.join(added)}." if added else "every neighbor is worn or already reached.")
    if code in added: note+=f" The code {code} is generated here, so the answer is {clicks[code]} clicks."
    steps.append({"at":{"cur":i},"vars":{"clicks":k,"waiting":ql,"added":len(added)},"note":note})
fill(CH,F,block(order,["cur"],steps),"@@TRACE1@@")
# trace 2: flat 3x3
g=[0,0,0, 0,1,0, 0,0,0]; n=3
dist={0:1}; ways={0:1}; q=deque([0]); steps=[]
while q:
    c=q.popleft(); r,cc=divmod(c,n)
    for dr in(-1,0,1):
        for dc in(-1,0,1):
            if dr==dc==0: continue
            nr,nc=r+dr,cc+dc
            if not(0<=nr<n and 0<=nc<n) or g[nr*n+nc]: continue
            m=nr*n+nc
            if m not in dist: dist[m]=dist[c]+1; ways[m]=0; q.append(m)
            if dist[m]==dist[c]+1: ways[m]+=ways[c]
    # at expansion time ways[c] is final
    steps.append({"at":{"cur":c},"vars":{"length":dist[c],"paths":ways[c],"waiting":len(q)},
      "note":f"Cell {c} is expanded with shortest length {dist[c]} and {ways[c]} shortest path"+("s" if ways[c]!=1 else "")+f" into it; {len(q)} cell"+("s" if len(q)!=1 else "")+" now wait."})
assert dist[8]==4 and ways[8]==2
fill(CH,F,block(g,["cur"],steps),"@@TRACE2@@")
print(order, clicks[code])
