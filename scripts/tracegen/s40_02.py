from common import *
CH='40-composite-indexes-and-allocation'; F='02-dynamic-rankings.md'
def run(calls):
    sc={}; cells=[f"{o}({','.join(map(str,a))})" for o,a in calls]; st=[]; out=[]
    for n,(o,a) in enumerate(calls):
        r="null"
        if o=="add":
            i,p=a; old=sc.get(i)
            sc[i]=(old or 0)+p
            note=(f"Call {n}: player {i} is new, so the board gains {sc[i]}:{i}." if old is None else f"Call {n}: the board removes {old}:{i} and inserts {sc[i]}:{i}.")
        elif o=="reset":
            i=a[0]; old=sc[i]; sc[i]=0
            note=f"Call {n}: the board removes {old}:{i} and inserts 0:{i}."
        else:
            k=a[0]; rows=sorted(((-s,i) for i,s in sc.items())); r=str(sum(-s for s,_ in rows[:k]))
            note=f"Call {n}: top({k}) adds the first {k} rows of the board and returns {r}."
        rows=sorted(((-s,i) for i,s in sc.items()))
        st.append({"at":{"call":n},"vars":{"board":" ".join(f"{-s}:{i}" for s,i in rows),"result":r},"note":note}); out.append(r)
    return cells,st,out
c,s,o=run([("add",(1,30)),("add",(2,30)),("add",(1,15)),("add",(3,40)),("top",(2,)),("reset",(1,)),("top",(2,))])
assert o[4]=="85" and o[6]=="70"
fill(CH,F,block(c,["call"],s),"@@TRACE1@@")
c,s,o=run([("add",(9,10)),("add",(4,10)),("add",(7,10)),("top",(3,)),("add",(7,5)),("top",(1,))])
assert o[3]=="30" and o[5]=="15"
fill(CH,F,block(c,["call"],s),"@@TRACE2@@")
