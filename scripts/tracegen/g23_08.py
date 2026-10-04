from common import *
CH='23-directed-graphs-and-union-find'
F='08-graph-and-union-find.md'
def run(n,edges):
    parent=list(range(n)); size=[1]*n
    def find(x):
        while parent[x]!=x: x=parent[x]
        return x
    comps=n; pointless=0; first=-1; rows=[]
    for i,(a,b) in enumerate(edges):
        ra,rb=find(a),find(b)
        if ra==rb:
            pointless+=1
            if first<0: first=i
            kind="pointless"
        else:
            big=ra if size[ra]>=size[rb] else rb
            small=rb if big==ra else ra
            parent[small]=big; size[big]+=size[small]; comps-=1; kind="merge"
        rows.append((i,ra,rb,kind,comps,pointless,first,list(parent),list(size)))
    return rows
# trace 1
e1=[[0,1],[2,3],[1,3],[3,0],[4,5],[6,6]]
rows=run(7,e1)
steps=[]
for i,ra,rb,kind,c,p,f,par,sz in rows:
    if kind=="merge": note=f"Representatives {ra} and {rb} differ, so the two networks merge and {c} remain."
    else: note=f"Both endpoints lead to representative {ra}, so the line is pointless; it is counted and nothing is written."+(f" It is the first one, at index {f}." if p==1 else "")
    steps.append({"at":{"i":i},"vars":{"ra":ra,"rb":rb,"networks":c,"pointless":p,"first":f},"note":note})
assert rows[-1][4]==3 and rows[-1][5]==2 and rows[-1][6]==3
assert [r[3] for r in rows]==["merge","merge","merge","pointless","merge","pointless"]
fill(CH,F,block(["0-1","2-3","1-3","3-0","4-5","6-6"],["i"],steps),"@@TRACE1@@")
# trace 2
e2=[[4,5],[3,4],[0,1],[1,2],[2,0],[2,5]]
rows=run(6,e2)
steps=[]
for i,ra,rb,kind,c,p,f,par,sz in rows:
    a,b=e2[i]
    note=(f"Representatives {ra} and {rb} differ, so one slot of parent and one slot of size change together." if kind=="merge"
          else f"Representatives are both {ra}, so neither array is written.")
    steps.append({"at":{"i":i},"vars":{"parent":"".join(map(str,par)),"size":"".join(map(str,sz)),"networks":c},"note":note})
print(rows[-1])
assert rows[-1][4]==1 and rows[-1][5]==1
fill(CH,F,block([f"{a}-{b}" for a,b in e2],["i"],steps),"@@TRACE2@@")
