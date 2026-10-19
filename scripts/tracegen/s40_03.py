from common import *
CH='40-composite-indexes-and-allocation'; F='03-resource-allocation.md'
def t1():
    n=4; free=set(range(1,n+1)); taken=set(); calls=[("reserve",()),("reserve",()),("release",(1,)),("reserve",()),("reserve",())]
    cells=[f"{o}({','.join(map(str,a))})" for o,a in calls]; st=[]; out=[]
    for k,(o,a) in enumerate(calls):
        if o=="reserve":
            s=min(free); free.remove(s); taken.add(s); r=str(s); note=f"Call {k}: the first free seat is {s}. It leaves the free set and enters the taken seats."
        else:
            s=a[0]; assert s in taken; taken.remove(s); free.add(s); r="true"; note=f"Call {k}: seat {s} is taken, so it leaves the taken seats and enters the free set."
        st.append({"at":{"call":k},"vars":{"free":"{"+",".join(map(str,sorted(free)))+"}","taken":"{"+",".join(map(str,sorted(taken)))+"}","result":r},"note":note}); out.append(r)
    assert out==["1","2","true","1","3"]
    return cells,st
def t2():
    n=10; occ=[]; cells=[]; st=[]; out=[]
    calls=["seat"]*4+["leave 4","seat"]
    cells=calls
    for k,c in enumerate(calls):
        if c=="seat":
            if not occ: p=0; why="The room is empty, so the first student sits at seat 0."
            else:
                best=(occ[0],0,"left end"); cand=[]
                if occ[0]>0: cand.append((occ[0],0))
                for a,b in zip(occ,occ[1:]):
                    m=a+(b-a)//2
                    if m!=a: cand.append((m-a,m))
                if occ[-1]<n-1: cand.append((n-1-occ[-1],n-1))
                d,p=max(cand,key=lambda x:(x[0],-x[1]))
                why=f"The best candidate sits at seat {p}, at distance {d} from its nearest occupied seat."
            occ.append(p); occ.sort(); r=str(p); note=f"Call {k}: {why}"
        else:
            p=int(c.split()[1]); occ.remove(p); r="null"; note=f"Call {k}: seat {p} leaves the occupied set, so its two neighboring gaps merge."
        st.append({"at":{"call":k},"vars":{"occupied":"{"+",".join(map(str,occ))+"}","result":r},"note":note}); out.append(r)
    assert out==["0","9","4","2","null","5"]
    return cells,st
c,s=t1(); fill(CH,F,block(c,["call"],s),"@@TRACE1@@")
c,s=t2(); fill(CH,F,block(c,["call"],s),"@@TRACE2@@")
