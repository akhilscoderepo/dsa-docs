from common import *
CH='41-algorithmic-services-and-simulations'; F='91-rank-words-by-prefix.md'
K=3
def run(calls):
    cnt={}; cells=[]; st=[]
    def rank(w): return (-cnt[w],w)
    def lst(p):
        ws=sorted((w for w in cnt if w.startswith(p)),key=rank)[:K]
        return "["+",".join(ws)+"]" if ws else "empty"
    def counts():
        return " ".join(f"{w}:{c}" for w,c in sorted(cnt.items()))
    for o,a in calls: cells.append(f"{o}({a})")
    for n,(o,a) in enumerate(calls):
        res="null"
        if o=="record":
            cnt[a]=cnt.get(a,0)+1
            note=f"Call {n}: the count of {a} becomes {cnt[a]}, and the call repairs the list of every prefix node on the path of {a}."
        else:
            res=lst(a)
            note=f"Call {n}: the query walks to the node for '{a}'." + (" The node exists, so the call copies its list." if res!="empty" else " The walk ends at a missing child, so the answer is empty.")
        st.append({"at":{"call":n},"vars":{"counts":counts(),"list(t)":lst(CP),"list(te)":lst(CP2),"result":res} if CP else {},"note":note})
    return cells,st
CP,CP2="t","te"
c,s=run([("record","tea"),("record","ten"),("record","tea"),("record","team"),("record","tent"),("query","te")])
assert s[-1]["vars"]["result"]=="[tea,team,ten]"
fill(CH,F,block(c,["call"],s),"@@TRACE1@@")
# second trace: different variables
def run2(calls):
    cnt={}; cells=[]; st=[]
    def lst(p):
        ws=sorted((w for w in cnt if w.startswith(p)),key=lambda w:(-cnt[w],w))[:K]
        return "["+",".join(ws)+"]" if ws else "empty"
    for o,a in calls: cells.append(f"{o}({a})")
    for n,(o,a) in enumerate(calls):
        res="null"
        if o=="record":
            cnt[a]=cnt.get(a,0)+1
            note=f"Call {n}: the count of {a} becomes {cnt[a]}, and the call repairs the root and the nodes on the path of {a}."
        else:
            res=lst(a)
            note=f"Call {n}: the query for '{a}' " + ("reads the list of the node it reaches." if a=="" or res!="empty" else "ends at a missing child and returns an empty list.")
        st.append({"at":{"call":n},"vars":{"counts":" ".join(f"{w}:{c}" for w,c in sorted(cnt.items())),"list(root)":lst(""),"list(b)":lst("b"),"result":res},"note":note})
    return cells,st
c,s=run2([("record","ba"),("record","bb"),("record","bc"),("record","bd"),("record","bd"),("query","b"),("query","be"),("query","")])
assert s[3]["vars"]["list(b)"]=="[ba,bb,bc]" and s[4]["vars"]["list(b)"]=="[bd,ba,bb]"
assert s[-3]["vars"]["result"]=="[bd,ba,bb]" and s[-2]["vars"]["result"]=="empty"
fill(CH,F,block(c,["call"],s),"@@TRACE2@@")
