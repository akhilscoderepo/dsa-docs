from common import *
CH='22-bfs-variations'; F='03-bidirectional-frontiers.md'
EDGES=[(0,1),(0,2),(1,3),(2,3),(3,4),(4,5),(4,6),(5,7),(6,7)]
N=8
adj=[[] for _ in range(N)]
for a,b in EDGES: adj[a].append(b); adj[b].append(a)
def show(m): return ",".join(str(m.get(v,-1)) for v in range(N))
def run(s,t):
    dS={s:0}; dT={t:0}; fS=[s]; fT=[t]; st=[]
    while fS and fT:
        fromS=len(fS)<=len(fT)
        f,own,oth=(fS,dS,dT) if fromS else (fT,dT,dS)
        side="start side" if fromS else "target side"
        nf=[]
        for c in f:
            found=None; added=[]
            for x in adj[c]:
                if x in oth: found=x; break
                if x in own: continue
                own[x]=own[c]+1; nf.append(x); added.append(x)
            vars_={"distStart":show(dS),"distTarget":show(dT)}
            if found is not None:
                total=own[c]+1+oth[found]
                st.append({"at":{"cur":c},"vars":vars_,"note":f"The {side} expands {c}. Its neighbor {found} is already in the opposite map at distance {oth[found]}, so the answer is {own[c]} + 1 + {oth[found]} = {total}."})
                return st,total
            txt=("adds "+" and ".join(map(str,added))) if added else "adds nothing new"
            st.append({"at":{"cur":c},"vars":vars_,"note":f"The {side} expands {c} and {txt}."})
        if fromS: fS=nf
        else: fT=nf
    return st,-1
st,r=run(0,7); assert r==5 and len(st)==6
fill(CH,F,block(list(range(N)),["cur"],st),"@@TRACE1@@")
st,r=run(0,5); assert r==4 and len(st)==5
fill(CH,F,block(list(range(N)),["cur"],st),"@@TRACE2@@")
