import heapq
from common import *
CH='41-algorithmic-services-and-simulations'; F='07-lifecycle-routing.md'

def tree_trace():
    calls=[("add",1,5),("add",2,9),("add",3,9),("cancel",2),("next",),("complete",3),("cancel",3),("next",)]
    cells=[c[0]+"("+",".join(map(str,c[1:]))+")" for c in calls]
    state={}; prio={}; steps=[]; outs=[]
    def ready(): return sorted((i for i in state if state[i]=="PENDING"),key=lambda i:(-prio[i],i))
    for k,c in enumerate(calls):
        op=c[0]
        if op=="add":
            assert c[1] not in state; state[c[1]]="PENDING"; prio[c[1]]=c[2]; r="true"; note=f"Call {k}: job {c[1]} with priority {c[2]} enters the status table and the ready set."
        elif op in("cancel","complete"):
            i=c[1]; new="CANCELLED" if op=="cancel" else "DONE"
            if state.get(i)=="PENDING":
                state[i]=new; r="true"; note=f"Call {k}: job {i} is PENDING, so the table records {new} and the job leaves the ready set."
            else:
                r="false"; note=f"Call {k}: job {i} is {state.get(i)}, which cannot become {new}, so the call returns false and writes nothing."
        else:
            rd=ready(); r=str(rd[0] if rd else -1); outs.append(int(r))
            note=f"Call {k}: the first job in the ready set is job {r}, and the call writes nothing."
        rd=ready()
        view=" ".join(f"{i}p{prio[i]}" for i in rd) or "empty"
        steps.append({"at":{"call":k},"vars":{"ready":view,"result":r},"note":note})
    assert outs==[3,1], outs
    return cells,steps

def heap_trace():
    calls=[("add",1,5),("add",2,9),("setPriority",2,1),("cancel",1),("add",3,4),("take",),("take",)]
    cells=[c[0]+"("+",".join(map(str,c[1:]))+")" for c in calls]
    table={}; h=[]; steps=[]; outs=[]
    def key(e): return (-e[0],e[1])
    def show(): return " ".join(f"{e[1]}@{e[0]} v{e[2]}" for e in sorted(h,key=key)) or "empty"
    def pend(): return sum(1 for j in table.values() if j["s"]=="PENDING")
    for k,c in enumerate(calls):
        op=c[0]
        if op=="add":
            table[c[1]]={"p":c[2],"v":0,"s":"PENDING"}; h.append((c[2],c[1],0)); r="true"
            note=f"Call {k}: job {c[1]} enters the table and the heap gets the entry {c[1]}@{c[2]} v0."
        elif op=="setPriority":
            j=table[c[1]]; assert j["s"]=="PENDING"; j["p"]=c[2]; j["v"]+=1; h.append((c[2],c[1],j["v"])); r="true"
            note=f"Call {k}: the table records priority {c[2]} and version {j['v']} for job {c[1]}, and the heap gets a second entry while the old one stays."
        elif op=="cancel":
            table[c[1]]["s"]="CANCELLED"; r="true"
            note=f"Call {k}: the table records CANCELLED for job {c[1]}, and its heap entry stays in place."
        else:
            skipped=[]; res=-1
            while True:
                if not h: break
                e=min(h,key=key); j=table[e[1]]
                if j["s"]=="PENDING" and j["v"]==e[2]:
                    res=e[1]; h.remove(e); j["s"]="DONE"; break
                h.remove(e); skipped.append(f"{e[1]}@{e[0]} v{e[2]}")
            outs.append(res); r=str(res)
            sk=("It discards the stale entries "+", ".join(skipped)+" and ") if skipped else "It finds the top entry matching the table and "
            note=f"Call {k}: {sk}returns job {res}." if res!=-1 else f"Call {k}: the heap is empty, so the call returns -1."
        steps.append({"at":{"call":k},"vars":{"heap":show(),"pending":str(pend()),"result":r},"note":note})
    assert outs==[3,2], outs
    return cells,steps

c,s=tree_trace(); fill(CH,F,block(c,["call"],s),"@@TRACE1@@")
c,s=heap_trace(); fill(CH,F,block(c,["call"],s),"@@TRACE2@@")
