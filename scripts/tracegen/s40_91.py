from common import *
CH='40-composite-indexes-and-allocation'; F='91-map-ordered-index.md'
def run(init,calls):
    T={}; cells=[]; st=[]
    def view():
        g=sorted(T.items(),key=lambda kv:(-kv[1][1],-kv[0]))
        gl=" ".join(str(i) for i,_ in g) or "empty"
        us={}
        for i,_ in g: us.setdefault(T[i][0],[]).append(i)
        return gl," ".join(f"u{u}:[{','.join(map(str,l))}]" for u,l in sorted(us.items())) or "empty"
    allc=[("add",a) for a in init]+calls
    for o,a in allc: cells.append(f"{o}({','.join(map(str,a))})")
    for n,(o,a) in enumerate(allc):
        r="null"
        if o=="add":
            u,i,p=a; T[i]=(u,p); note=f"Call {n}: task {i} enters the record, the global index and the list of user {u}."
        elif o=="edit":
            i,p=a; u,_=T[i]; T[i]=(u,p); note=f"Call {n}: the helper removes the old entry of task {i} everywhere, then inserts it with priority {p}."
        elif o=="execUser":
            u=a[0]; mine=sorted(((i,p) for i,(uu,p) in T.items() if uu==u),key=lambda x:(-x[1],-x[0]))
            if mine: i=mine[0][0]; del T[i]; r=str(i); note=f"Call {n}: the best task of user {u} is {i}. The helper removes it from all three structures."
            else: r="-1"; note=f"Call {n}: user {u} has no task, so the call returns -1."
        else:
            g=sorted(T.items(),key=lambda kv:(-kv[1][1],-kv[0]))
            if g: i=g[0][0]; del T[i]; r=str(i); note=f"Call {n}: the best task overall is {i}. The helper removes it from all three structures."
            else: r="-1"; note=f"Call {n}: no task exists, so the call returns -1."
        gl,ul=view()
        st.append({"at":{"call":n},"vars":{"global":gl,"users":ul,"result":r},"note":note})
    return cells,st
c,s=run([(1,101,5),(1,102,7),(2,103,7)],[("execUser",(1,)),("execGlobal",()),("execGlobal",())])
assert [x["vars"]["result"] for x in s[3:]]==["102","103","101"]
fill(CH,F,block(c,["call"],s),"@@TRACE1@@")
c,s=run([(4,301,2),(4,302,9),(5,303,4)],[("edit",(301,10)),("execGlobal",()),("execUser",(4,)),("execGlobal",())])
assert [x["vars"]["result"] for x in s[4:]]==["301","302","303"]
fill(CH,F,block(c,["call"],s),"@@TRACE2@@")
