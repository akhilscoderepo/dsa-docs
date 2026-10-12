from common import *
CH='25-advanced-graph-optimization'
F='06-strong-components.md'
def build(n,E):
    out=[[] for _ in range(n)]; back=[[] for _ in range(n)]
    for a,b in E: out[a].append(b); back[b].append(a)
    return out,back
def finish(n,out):
    seen=[False]*n; cur=[0]*n; order=[]
    for s in range(n):
        if seen[s]: continue
        st=[s]; seen[s]=True
        while st:
            u=st[-1]
            if cur[u]<len(out[u]):
                v=out[u][cur[u]]; cur[u]+=1
                if not seen[v]: seen[v]=True; st.append(v)
            else: st.pop(); order.append(u)
    return order
def closure(n,E):
    r=[[i==j for j in range(n)] for i in range(n)]
    for a,b in E: r[a][b]=True
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if r[i][k] and r[k][j]: r[i][j]=True
    return r
def sweep(n,order,g,truthsize):
    label=[-1]*n; nxt=0; cells=[]; steps=[]; labeled=0
    for i,s in enumerate(reversed(order)):
        cells.append(str(s))
        if label[s]!=-1:
            note=f"Vertex {s} already has label {label[s]}, so no search starts."
            found=0; lab=label[s]
        else:
            label[s]=nxt; st=[s]; got=[s]
            while st:
                u=st.pop()
                for v in g[u]:
                    if label[v]==-1: label[v]=nxt; st.append(v); got.append(v)
            found=len(got); lab=nxt; labeled+=found
            note=f"Vertex {s} opens label {nxt} and the search collects {found} vertices: "+", ".join(map(str,sorted(got)))+"."
            nxt+=1
        steps.append({"at":{"i":i},"vars":{"label":lab,"found":found,"labeled":labeled,**({"truth":truthsize[s]} if truthsize else {})},"note":note})
    return cells,steps,label
# trace 1
n1=8; e1=[(0,3),(3,6),(6,0),(6,1),(1,4),(4,1),(4,2),(2,5),(5,2),(5,7),(3,7)]
out,back=build(n1,e1); order=finish(n1,out)
assert order==[7,5,2,4,1,6,3,0],order
cells,steps,label=sweep(n1,order,back,None)
assert cells==['0','3','6','1','4','2','5','7']
assert label==[0,1,2,0,1,2,0,3]
r=closure(n1,e1)
assert all((r[u][v] and r[v][u])==(label[u]==label[v]) for u in range(n1) for v in range(n1))
assert steps[0]['vars']['found']==3 and steps[0]['note'].endswith("0, 3, 6.")
fill(CH,F,block(cells,["i"],steps),"@@TRACE1@@")
# trace 2: forward lists in pass two
n2=5; e2=[(0,1),(1,0),(1,2),(2,3),(3,2),(3,4)]
out,back=build(n2,e2); order=finish(n2,out)
assert order==[4,3,2,1,0],order
r=closure(n2,e2)
size=[sum(1 for v in range(n2) if r[u][v] and r[v][u]) for u in range(n2)]
assert size==[2,2,2,2,1]
cells,steps,label=sweep(n2,order,out,size)
assert label==[0]*5 and steps[0]['vars']['found']==5 and steps[0]['vars']['truth']==2
fill(CH,F,block(cells,["i"],steps),"@@TRACE2@@")
print(cells)
