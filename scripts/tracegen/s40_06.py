from common import *
CH='40-composite-indexes-and-allocation'; F='06-transaction-lifecycles.md'
V=[20,50,100,200,500]
def atm():
    notes=[0]*5; cells=["deposit","withdraw(600)","withdraw(125)","withdraw(300)"]; st=[]
    def show(): return ",".join(map(str,notes))
    notes[:]=[0,10,0,3,1]
    st.append({"at":{"call":0},"vars":{"stock":show(),"plan":"-"},"note":"Call 0: the deposit adds the counts 0, 10, 0, 3 and 1 to the stock."})
    for k,amt in ((1,600),(2,125),(3,300)):
        plan=[0]*5; left=amt
        for i in range(4,-1,-1):
            plan[i]=min(notes[i],left//V[i]); left-=plan[i]*V[i]
        if left:
            note=f"Call {k}: the plan {','.join(map(str,plan))} leaves {left} unpaid, so the call returns -1 and the stock does not change."; ps="fails"
        else:
            for i in range(5): notes[i]-=plan[i]
            note=f"Call {k}: the plan {','.join(map(str,plan))} pays {amt} exactly, so the commit subtracts it from the stock."; ps=",".join(map(str,plan))
        st.append({"at":{"call":k},"vars":{"stock":show(),"plan":ps},"note":note})
    assert notes==[0,6,0,2,0]
    return cells,st
def orders():
    S=["CREATED","PAID","SHIPPED","DELIVERED","CANCELLED"]; st_of={}
    calls=[("create",1),("create",2),("pay",1),("ship",1),("cancel",1),("cancel",2)]
    cells=[f"{o}({i})" for o,i in calls]; st=[]
    nxt={"pay":("CREATED","PAID"),"ship":("PAID","SHIPPED")}
    for k,(o,i) in enumerate(calls):
        if o=="create": st_of[i]="CREATED"; r="true"; note=f"Call {k}: order {i} enters the CREATED index."
        elif o in nxt:
            a,b=nxt[o]; assert st_of[i]==a; st_of[i]=b; r="true"; note=f"Call {k}: order {i} is {a}, so it leaves that index and enters {b}."
        else:
            if st_of[i] in("CREATED","PAID"): old=st_of[i]; st_of[i]="CANCELLED"; r="true"; note=f"Call {k}: order {i} is {old}, so it leaves that index and enters CANCELLED."
            else: r="false"; note=f"Call {k}: order {i} is {st_of[i]}, which cannot be cancelled, so the call returns false and no index changes."
        view=" ".join(f"{s[:3]}:{{{','.join(str(x) for x in sorted(j for j,v in st_of.items() if v==s))}}}" for s in S if any(v==s for v in st_of.values())) or "empty"
        st.append({"at":{"call":k},"vars":{"indexes":view,"result":r},"note":note})
    return cells,st
c,s=atm(); fill(CH,F,block(c,["call"],s),"@@TRACE1@@")
c,s=orders(); fill(CH,F,block(c,["call"],s),"@@TRACE2@@")
