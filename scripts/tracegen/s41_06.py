from common import *
CH='41-algorithmic-services-and-simulations'; F='06-prefix-services.md'

def pre(d):
    return " ".join(f"{k}:{v}" for k,v in sorted(d.items(), key=lambda kv:(len(kv[0]),kv[0])) if v) or "empty"

def mapsum():
    val={}; node={}; calls=[("insert","apple",3),("insert","app",2),("sum","ap",None),("insert","apple",5),("insert","app",2),("sum","ap",None)]
    cells=[f"{o}({k},{v})" if v is not None else f"{o}({k})" for o,k,v in calls]; st=[]
    for n,(o,k,v) in enumerate(calls):
        if o=="insert":
            old=val.get(k,0); delta=v-old; val[k]=v
            for i in range(1,len(k)+1): node[k[:i]]=node.get(k[:i],0)+delta
            if old==0: note=f"Call {n}: the word is new, so the delta is {delta} and every node on the path to {k} gains {delta}."
            elif delta: note=f"Call {n}: the old value is {old}, so the delta is {delta} and every node on the path to {k} changes by {delta}."
            else: note=f"Call {n}: the old value is {old} and the new value is the same, so the delta is 0 and no node changes."
            vars_={"sums":pre(node),"delta":str(delta),"result":str(old if old else -1)}
        else:
            r=node.get(k,0); vars_={"sums":pre(node),"delta":"-","result":str(r)}
            note=f"Call {n}: the walk reads the node for {k} and returns {r}."
        st.append({"at":{"call":n},"vars":vars_,"note":note})
    assert node["ap"]==7 and node["apple"]==5 and node["app"]==7
    return cells,st

def counts():
    words={}; calls=[("insert","app"),("insert","apple"),("insert","app"),("erase","app"),("erase","ap"),("countPrefix","app"),("erase","apple"),("erase","app"),("countPrefix","a")]
    cells=[f"{o}({w})" for o,w in calls]; st=[]
    def view():
        p={};e={}
        for w,c in words.items():
            if c==0: continue
            for i in range(1,len(w)+1): p[w[:i]]=p.get(w[:i],0)+c
            e[w]=c
        return " ".join(f"{k}={v}/{e.get(k,0)}" for k,v in sorted(p.items(), key=lambda kv:(len(kv[0]),kv[0]))) or "empty"
    for n,(o,w) in enumerate(calls):
        if o=="insert":
            words[w]=words.get(w,0)+1; r="-"; note=f"Call {n}: the pass count rises by 1 on every node of the path to {w}, and the end count rises on the last node."
        elif o=="erase":
            if words.get(w,0)>0:
                words[w]-=1; r="true"; note=f"Call {n}: a copy of {w} exists, so every node on its path loses 1 from the pass count and the last node loses 1 from the end count."
            else:
                r="false"; note=f"Call {n}: no copy of {w} is stored, so the call returns false before it changes any node."
        else:
            r=str(sum(c for x,c in words.items() if x.startswith(w))); note=f"Call {n}: the walk reads the pass count of {w}, which is {r}."
        st.append({"at":{"call":n},"vars":{"nodes":view(),"result":r},"note":note})
    assert view()=="empty"
    return cells,st

c,s=mapsum(); fill(CH,F,block(c,["call"],s),"@@TRACE1@@")
c,s=counts(); fill(CH,F,block(c,["call"],s),"@@TRACE2@@")
