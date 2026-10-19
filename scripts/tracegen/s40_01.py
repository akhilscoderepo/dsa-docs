from common import *
CH='40-composite-indexes-and-allocation'; F='01-multi-index-records.md'
def show(at,idx):
    a=",".join(f"{k}:{v}" for k,v in sorted(at.items())) or "empty"
    b=" ".join(f"{k}:{{{','.join(map(str,sorted(s)))}}}" for k,s in sorted(idx.items())) or "empty"
    return a,b
def run(calls):
    at={}; idx={}; cells=[]; st=[]; res=[]
    for n,(op,args) in enumerate(calls):
        cells.append(f"{op}({','.join(map(str,args))})")
    for n,(op,args) in enumerate(calls):
        if op=="change":
            i,x=args; old=at.get(i)
            if old==x: note=f"Call {n}: index {i} already holds {x}, so the call changes neither map."
            else:
                at[i]=x
                if old is not None:
                    idx[old].discard(i)
                    if not idx[old]: del idx[old]
                idx.setdefault(x,set()).add(i)
                note=(f"Call {n}: index {i} holds {x} now. The old number {old} loses index {i}." if old is not None else f"Call {n}: index {i} is new, so there is no old entry to remove, and number {x} gains index {i}.")
                if old is not None and old not in idx: note+=f" The set for {old} is empty, so its key disappears."
            r="null"
        else:
            x=args[0]; r=str(min(idx[x]) if x in idx else -1)
            note=f"Call {n}: find({x}) reads the set for {x} and returns {r}."
        a,b=show(at,idx)
        st.append({"at":{"call":n},"vars":{"numberAt":a,"indexesOf":b,"result":r},"note":note}); res.append(r)
    return cells,st,res
c,s,r=run([("change",(2,10)),("change",(1,10)),("change",(1,20)),("find",(10,)),("find",(20,))])
assert r[3]=="2" and r[4]=="1"
fill(CH,F,block(c,["call"],s),"@@TRACE1@@")
c,s,r=run([("change",(3,5)),("change",(3,5)),("change",(3,7)),("find",(5,))])
assert r[3]=="-1"
fill(CH,F,block(c,["call"],s),"@@TRACE2@@")
