from common import *
CH='39-dynamic-query-structures'; F='06-dynamic-graph-queries.md'
INF=10**15
def run(n, edges, ops):
    d=[[INF]*n for _ in range(n)]
    for i in range(n): d[i][i]=0
    for a,b,w in edges: d[a][b]=min(d[a][b],w)
    for k in range(n):
        for i in range(n):
            for j in range(n): d[i][j]=min(d[i][j],d[i][k]+d[k][j])
    def row(): return ",".join("INF" if x>=INF else str(x) for x in d[0])
    st=[]; res=[]
    for o in ops:
        if o[0]=='q':
            _,a,b=o; r=-1 if d[a][b]>=INF else d[a][b]; res.append(r)
            note=f"query({a}, {b}) reads dist[{a}][{b}] and returns {r}."
            vars_={"row0":row(),"result":str(r)}
        else:
            _,a,b,w=o; ch=0
            nd=[[min(d[i][j],d[i][a]+w+d[b][j]) for j in range(n)] for i in range(n)]
            ch=sum(nd[i][j]<d[i][j] for i in range(n) for j in range(n)); d=nd
            res.append(ch>0)
            note=(f"addEdge({a}, {b}, {w}) repairs every pair and lowers {ch} cells." if ch else
                  f"addEdge({a}, {b}, {w}) offers no cheaper route, so the repair changes no cell.")
            vars_={"row0":row(),"changed":str(ch)}
        st.append({"at":{"a":o[1],"b":o[2]},"vars":vars_,"note":note})
    return st,res
st,res=run(4,[(0,1,5),(1,2,4),(2,3,1)],[('q',0,3),('a',0,2,6),('q',0,3),('a',0,3,9),('q',0,3)])
assert res==[10,True,7,False,7]
fill(CH,F,block([str(i) for i in range(4)],["a","b"],st),"@@TRACE1@@")
st,res=run(3,[(0,1,3)],[('q',0,2),('a',1,2,2),('q',0,2),('a',1,2,7),('a',0,2,5),('a',0,2,4),('q',0,2)])
assert res==[-1,True,5,False,False,True,4]
fill(CH,F,block([str(i) for i in range(3)],["a","b"],st),"@@TRACE2@@")
