from common import *
CH='41-algorithmic-services-and-simulations'; F='05-transaction-ledgers.md'
def bank():
    bal={1:10,2:100,3:20}
    calls=[("transfer",2,3,40),("transfer",1,4,5),("withdraw",3,50),("deposit",1,15),("transfer",1,2,30),("transfer",2,1,60)]
    cells=[f"{c[0]}({','.join(map(str,c[1:]))})" for c in calls]; st=[]
    for k,c in enumerate(calls):
        op=c[0]
        if op=="transfer":
            _,a,b,m=c
            if a not in bal or b not in bal: ok=False; why=f"names account {b if a in bal else a}, which does not exist"
            elif bal[a]<m: ok=False; why=f"asks for {m} from an account that holds {bal[a]}"
            else: ok=True; bal[a]-=m; bal[b]+=m
            note=(f"Call {k}: the transfer of {m} from account {a} to account {b} passes both tests, so the commit writes both balances." if ok
                  else f"Call {k}: the call {why}, so the first block refuses it and no balance changes.")
        elif op=="withdraw":
            _,a,m=c; assert bal[a]>=m; bal[a]-=m; ok=True
            note=f"Call {k}: account {a} holds enough for {m}, so the commit lowers its balance."
        else:
            _,a,m=c; bal[a]+=m; ok=True
            note=f"Call {k}: account {a} exists, so the commit adds {m}."
        st.append({"at":{"call":k},"vars":{"balances":",".join(str(bal[i]) for i in (1,2,3)),"result":"true" if ok else "false"},"note":note})
    assert [bal[i] for i in (1,2,3)]==[85,0,10] and sum(bal.values())==95
    return cells,st
def metro():
    active={}; stats={}
    calls=[("in",1,"a",3),("in",1,"b",5),("in",2,"a",4),("out",1,"b",10),("out",1,"b",11),("out",2,"b",12)]
    cells=[f"check{'In' if c[0]=='in' else 'Out'}({c[1]},{c[2]},{c[3]})" for c in calls]; st=[]
    for k,(op,i,s,t) in enumerate(calls):
        if op=="in":
            if i in active: ok=False; note=f"Call {k}: rider {i} already has an open trip, so the first block refuses the call and nothing changes."
            else: active[i]=(s,t); ok=True; note=f"Call {k}: rider {i} has no open trip, so the commit stores station {s} and time {t}."
        else:
            if i not in active: ok=False; note=f"Call {k}: rider {i} has no open trip, so the first block refuses the call and the active map and stats stay as they were."
            else:
                s0,t0=active.pop(i); assert t>=t0; d=t-t0; r=f"{s0}>{s}"
                tot,cnt=stats.get(r,(0,0)); stats[r]=(tot+d,cnt+1); ok=True
                note=f"Call {k}: the commit closes the trip of rider {i} and adds {d} to route {r}."
        a=",".join(f"{i}@{s}" for i,(s,_) in sorted(active.items())) or "-"
        sv=" ".join(f"{r}:{x}/{y}" for r,(x,y) in sorted(stats.items())) or "-"
        st.append({"at":{"call":k},"vars":{"active":a,"stats":sv,"result":"true" if ok else "false"},"note":note})
    assert stats=={"a>b":(15,2)} and not active
    return cells,st
c,s=bank(); fill(CH,F,block(c,["call"],s),"@@TRACE1@@")
c,s=metro(); fill(CH,F,block(c,["call"],s),"@@TRACE2@@")
