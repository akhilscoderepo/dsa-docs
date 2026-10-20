from common import *
CH='41-algorithmic-services-and-simulations'; F='02-hierarchical-namespaces.md'
def tree_view(d):
    return " ".join(f"{p}={v}" for p,v in sorted(d.items())) or "empty"
def t1():
    calls=[("create","/a",1),("create","/a/b",2),("create","/c/d",3),("create","/a",5),("get","/a/b",None),("get","/a/x",None)]
    d={}; cells=[]; st=[]
    for k,(op,p,v) in enumerate(calls):
        if op=="create":
            cells.append(f"create({p},{v})")
            parent=p.rsplit("/",1)[0]
            if parent!="" and parent not in d:
                r="false"; note=f"Call {k}: the walk stops because {parent} is missing, so the call returns false and writes nothing."
            elif p in d:
                r="false"; note=f"Call {k}: the path {p} exists already, so the call returns false and keeps the old value {d[p]}."
            else:
                d[p]=v; r="true"; note=f"Call {k}: the parent exists and {p} is new, so the walk adds the node with value {v}."
        else:
            cells.append(f"get({p})")
            r=str(d.get(p,-1)); note=f"Call {k}: the walk {'reaches' if p in d else 'cannot reach'} {p}, so the call returns {r}."
        st.append({"at":{"call":k},"vars":{"tree":tree_view(d),"result":r},"note":note})
    assert d=={"/a":1,"/a/b":2}
    return cells,st
def norm(s):
    if not s.startswith("/"): return None,"the string has no leading separator"
    parts=[x for x in s.split("/") if x]
    for x in parts:
        if x in (".",".."): return None,f"the name {x} is illegal"
    return parts,""
def t2():
    raw=["/a/b","//a///b/","/","a/b","/a/./b","/a/b."]; cells=raw; st=[]; seen={}
    for k,s in enumerate(raw):
        parts,why=norm(s)
        if parts is None:
            vs="rejected"; note=f"Call {k}: the string is rejected because {why}."
        else:
            key="/"+"/".join(parts); vs=",".join(parts) if parts else "(none)"
            if key in seen: note=f"Call {k}: the components {vs} name the same location as call {seen[key]}."
            else:
                seen[key]=k
                note=f"Call {k}: the components {vs} name "+("the root." if not parts else "a new location.")
        st.append({"at":{"call":k},"vars":{"components":vs},"note":note})
    assert norm("//a///b/")[0]==["a","b"] and norm("/")[0]==[]
    return cells,st
c,s=t1(); refill(CH,F,block(c,["call"],s),0)
c,s=t2(); refill(CH,F,block(c,["call"],s),1)
