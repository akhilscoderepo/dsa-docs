from common import *
CH='19-recursion-and-backtracking'; F='03-subsets.md'
a=[1,2,3]; st=[]; path=[]; out=[]
def go(start):
    out.append(list(path))
    s=",".join(map(str,path)) or "empty"
    note=f"The call with start {start} stores the subset [{s}]." if path else f"The root call with start {start} stores the empty subset."
    st.append({"at":{"start":start},"vars":{"path":s,"stored":len(out)},"note":note})
    for i in range(start,len(a)):
        path.append(a[i]); go(i+1); path.pop()
go(0)
assert len(out)==8 and out[-1]==[3]
fill(CH,F,block([str(x) for x in a],["start"],st),"@@TRACE1@@")
b=[1,2]; st=[]; calls=[]
def g2(used,path):
    calls.append(list(path))
    for i in range(2):
        if i not in used: g2(used|{i},path+[b[i]])
g2(set(),[])
assert len(calls)==5
seen=set(); st=[]
for k,p in enumerate(calls):
    key=tuple(sorted(p)); dup=key in seen; seen.add(key)
    s=",".join(map(str,p)) or "empty"
    st.append({"at":{"i":len(p)},"vars":{"path":s,"set size":len(seen)},"note":f"Call {k+1} holds the path [{s}], and its sorted form "+("is already in the hash set, so the call was wasted." if dup else "is new, so the hash set grows.")})
assert len(seen)==4
fill(CH,F,block(["1","2"],["i"],st),"@@TRACE2@@")
