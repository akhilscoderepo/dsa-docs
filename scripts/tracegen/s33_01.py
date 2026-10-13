from common import *
CH='33-design-data-structure-problems'; F='01-api-contracts.md'
def fmt(c): return "{"+", ".join(f"{k}:{v}" for k,v in c.items())+"}"
def counter(calls):
    c={}; total=0
    st=[{"at":{"call":-1},"vars":{"counts":"{}","total":0,"distinct":0,"result":"none"},"note":"Start: the counter is empty, so total and distinct are both 0."}]
    for i,(op,k) in enumerate(calls):
        if op=="add":
            c[k]=c.get(k,0)+1; total+=1; res=f"count {c[k]}"; note=f"add({k}) raises {k} to {c[k]}. total is {total} and distinct is {len(c)}."
        elif k in c:
            c[k]-=1; total-=1; res="ok"
            if c[k]==0: del c[k]; note=f"remove({k}) lowers {k} to 0, so the key is deleted. total is {total} and distinct is {len(c)}."
            else: note=f"remove({k}) lowers {k} to {c[k]}. total is {total} and distinct is {len(c)}."
        else:
            res="throws"; note=f"remove({k}) finds no key and throws NoSuchElementException. counts, total and distinct are unchanged."
        st.append({"at":{"call":i},"vars":{"counts":fmt(c),"total":total,"distinct":len(c),"result":res},"note":note})
    return st,c,total
calls=[("add","bob"),("add","bob"),("add","amy"),("remove","bob"),("remove","amy"),("remove","amy")]
st,c,total=counter(calls); assert c=={"bob":1} and total==1 and st[-1]["vars"]["result"]=="throws"
fill(CH,F,block([f"{o}({k})" for o,k in calls],["call"],st),"@@TRACE1@@")
def stack(calls):
    s=[]
    st=[{"at":{"call":-1},"vars":{"stack":"[]","size":0,"result":"none"},"note":"Start: the stack is empty."}]
    for i,(op,v) in enumerate(calls):
        if op=="push": s.append(v); res="ok"; note=f"push({v}) appends {v}. The stack is {s}."
        elif not s: res="throws"; note=f"{op}() on an empty stack throws NoSuchElementException. The stack is still empty."
        elif op=="top": res=str(s[-1]); note=f"top() returns {s[-1]} and removes nothing. The stack is {s}."
        else: res=str(s.pop()); note=f"pop() removes and returns {res}. The stack is {s}."
        st.append({"at":{"call":i},"vars":{"stack":str(s).replace(" ",""),"size":len(s),"result":res},"note":note})
    return st,s
calls=[("push",4),("push",9),("top",0),("pop",0),("pop",0),("pop",0),("push",7),("top",0)]
st,s=stack(calls); assert s==[7] and st[-1]["vars"]["result"]=="7" and st[6]["vars"]["result"]=="throws"
fill(CH,F,block([f"push({v})" if o=="push" else f"{o}()" for o,v in calls],["call"],st),"@@TRACE2@@")
