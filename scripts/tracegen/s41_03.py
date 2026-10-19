from common import *
CH='41-algorithmic-services-and-simulations'; F='03-dependency-state.md'
class Sheet:
    def __init__(s): s.f={}; s.dep={}; s.v={}
    def get(s,c): return s.v.get(c,0)
    def detach(s,c):
        for r in s.f.pop(c,[]): s.dep[r].discard(c)
    def reaches(s,frm,t):
        st=list(frm); seen=set()
        while st:
            c=st.pop()
            if c==t: return True
            if c not in seen: seen.add(c); st+=s.f.get(c,[])
        return False
    def refresh(s,start):
        post=[]; seen=set()
        def col(c):
            if c in seen: return
            seen.add(c)
            for d in sorted(s.dep.get(c,())): col(d)
            post.append(c)
        col(start); post.reverse(); done=[]
        for c in post:
            if c in s.f: s.v[c]=sum(s.get(r) for r in s.f[c]); done.append(c)
        return done
    def lit(s,c,x): s.detach(c); s.v[c]=x; return s.refresh(c)
    def setf(s,c,refs):
        if s.reaches(refs,c): return None
        s.detach(c); s.f[c]=list(refs)
        for r in refs: s.dep.setdefault(r,set()).add(c)
        return s.refresh(c)
def vals(s): return " ".join(f"{k}={s.v[k]}" for k in sorted(s.v))
def deps(s,c): return "{"+",".join(sorted(s.dep.get(c,())))+"}"
def t1():
    s=Sheet(); cells=["a=3","b=4","c=a+b","d=c+a","a=10","b=1"]; st=[]
    ops=[("l","a",3),("l","b",4),("f","c",["a","b"]),("f","d",["c","a"]),("l","a",10),("l","b",1)]
    for k,(o,c,x) in enumerate(ops):
        done=s.lit(c,x) if o=="l" else s.setf(c,x)
        rc=",".join(done) or "none"
        what=f"stores {x} in {c}" if o=="l" else f"gives {c} the formula {'+'.join(x)}"
        st.append({"at":{"call":k},"vars":{"values":vals(s),"recomputed":rc},"note":f"Call {k}: the sheet {what}, and it recomputes {rc if done else 'no formula cells'}."})
    assert s.v=={"a":10,"b":1,"c":11,"d":21}
    return cells,st
def t2():
    s=Sheet(); cells=["a=2","b=5","e=a+a","a=e","e=b","a=9","b=6"]; st=[]
    ops=[("l","a",2),("l","b",5),("f","e",["a","a"]),("f","a",["e"]),("f","e",["b"]),("l","a",9),("l","b",6)]
    for k,(o,c,x) in enumerate(ops):
        done=s.lit(c,x) if o=="l" else s.setf(c,x)
        if done is None:
            r="false"; note=f"Call {k}: e already reads a, so the cycle check rejects the formula and nothing changes."
        else:
            rc=",".join(done) or "none"; r="true"
            if o=="l": note=f"Call {k}: the literal {x} goes into {c}, and the sheet recomputes {rc if done else 'no formula cells'}."
            else: note=f"Call {k}: {c} gets the formula {'+'.join(x)}, and the sheet recomputes {rc}."
        st.append({"at":{"call":k},"vars":{"values":vals(s),"dependents of a":deps(s,"a"),"result":r},"note":note})
    assert s.v=={"a":9,"b":6,"e":6}
    return cells,st
c,x=t1(); fill(CH,F,block(c,["call"],x),"@@TRACE1@@")
c,x=t2(); fill(CH,F,block(c,["call"],x),"@@TRACE2@@")
