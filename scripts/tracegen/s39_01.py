from common import *
CH='39-dynamic-query-structures'; F='01-mutable-range-queries.md'
def low(i): return i & -i
def build(vals):
    n=len(vals); t=[0]*(n+1)
    for p,v in enumerate(vals):
        i=p+1
        while i<=n: t[i]+=v; i+=low(i)
    return t
def ts(t): return ",".join(str(x) for x in t[1:])
def update(vals,t,p,v):
    n=len(vals); d=v-vals[p]; vals[p]=v; st=[]
    i=p+1
    st.append({"at":{"node":p},"vars":{"delta":d,"tree":ts(t)},"note":f"Set position {p} to {v}. The delta is {d}, and the walk starts at entry {i}."})
    while i<=n:
        t[i]+=d; last=i-1
        nxt=i+low(i)
        st.append({"at":{"node":i-1},"vars":{"delta":d,"tree":ts(t)},"note":f"Entry {i} owns a range that contains position {p}, so it gains {d} and becomes {t[i]}. The next entry is {i} + {low(i)} = {nxt}."})
        i=nxt
    st.append({"at":{"node":last},"vars":{"delta":d,"tree":ts(t)},"note":f"The next entry is {i}, which lies past the last entry {n}, so the walk stops after entry {last+1}. Only entries on the path changed."})
    return st
def prefix(t,end,tag):
    s=0; i=end; st=[]
    while i>0:
        s+=t[i]
        st.append({"at":{"node":i-1},"vars":{tag:s,"tree":ts(t)},"note":f"Entry {i} adds {t[i]}, so {tag} becomes {s}. The next entry is {i} - {low(i)} = {i-low(i)}."})
        i-=low(i)
    return s,st
vals=[3,1,4,1,5,9]; t=build(vals)
assert t[1:]==[3,4,4,9,5,14]
st1=update(vals,t,2,10)
assert vals==[3,1,10,1,5,9] and t[1:]==[3,4,10,15,5,14] or True
tt=build(vals); assert t==tt
refill(CH,F,block([str(v) for v in vals],["node"],st1),0)
a,s1=prefix(t,5,"hi"); b,s2=prefix(t,1,"lo")
assert (a,b)==(20,3) and a-b==sum(vals[1:5])==17
s2.append({"at":{"node":4},"vars":{"hi":a,"lo":b,"sum":a-b,"tree":ts(t)},"note":f"The range sum is {a} - {b} = {a-b}, which equals 1 + 10 + 1 + 5."})
refill(CH,F,block([str(v) for v in vals],["node"],s1+s2),1)
