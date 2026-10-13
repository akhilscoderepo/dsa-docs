from common import *
CH='36-stateful-containers-and-histories'; F='02-direct-stores.md'
# Trace 1: boolean direct set with domain 8.
D=8; present=[False]*D; st=[]
def shown(): return ",".join(str(k) for k in range(D) if present[k]) or "none"
ops=[("add",3),("add",5),("add",3),("remove",5),("contains",5),("contains",3)]
for op,k in ops:
    if op=="add":
        if present[k]: msg=f"add {k}: slot {k} is already true, so nothing changes and the call reports that the key was present."
        else: present[k]=True; msg=f"add {k}: slot {k} was false, so the call writes true there and reports a new key."
    elif op=="remove":
        assert present[k]; present[k]=False; msg=f"remove {k}: slot {k} was true, so the call writes false there and no other slot changes."
    else:
        msg=f"contains {k}: the call reads slot {k} and finds {'true' if present[k] else 'false'}."
    st.append({"at":{"key":k},"vars":{"stored":shown()},"note":msg})
assert shown()=="3"
fill(CH,F,block([str(i) for i in range(D)],["key"],st),"@@TRACE1@@")
# Trace 2: four chains, new nodes link at the chain head.
B=4; ch=[[] for _ in range(B)]; st=[]
def shown2(): return " | ".join(f"{b}:"+(",".join(map(str,ch[b])) or "-") for b in range(B))
ops=[("add",6),("add",10),("add",3),("add",10),("remove",6),("contains",10)]
for op,k in ops:
    b=k%B; c=ch[b]
    if op=="add":
        if k in c: msg=f"add {k}: bucket {b} holds {k} already, so the walk compares and stops without a new node."
        else:
            c.insert(0,k)
            msg=f"add {k}: {k} % {B} = {b}. The chain of bucket {b} has no equal key, so a new node becomes its head."
    elif op=="remove":
        c.remove(k); msg=f"remove {k}: {k} % {B} = {b}. The walk finds the node and unlinks it, and the other buckets stay untouched."
    else:
        assert k in c; msg=f"contains {k}: {k} % {B} = {b}. The walk of bucket {b} reaches key {k} and answers true."
    st.append({"at":{"b":b},"vars":{"chains":shown2()},"note":msg})
assert shown2()=="0:- | 1:- | 2:10 | 3:3"
fill(CH,F,block([str(i) for i in range(B)],["b"],st),"@@TRACE2@@")
