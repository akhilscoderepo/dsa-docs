from common import *
CH='20-greedy'
F='04-exchange-reasoning.md'
d=[5,2,8,1]
def total(o):
    c=t=0
    for x in o: c+=x; t+=c
    return t
o=d[:]; st=[]
assert total(o)==43
for i in range(len(o)):
    k=min(range(i,len(o)),key=lambda j:(o[j],j))
    before=total(o)
    if k!=i:
        o[i],o[k]=o[k],o[i]
        note=f"The shortest job in the unresolved part is {o[i]}, found at position {k}. Swapping it with the job at position {i} moves the total from {before} to {total(o)}."
    else:
        note=f"The job at position {i} is already a shortest one in the unresolved part, so no swap is needed and the total stays {before}."
    st.append({"at":{"i":i},"vars":{"order":"-".join(map(str,o)),"total":total(o)},"note":note})
assert o==[1,2,5,8] and total(o)==28 and [s["vars"]["total"] for s in st]==[31,31,28,28]
fill(CH,F,block([str(x) for x in d],["i"],st),"@@TRACE1@@")
iv=[(0,3),(2,4),(3,7)]
cells=[f"{a}-{b}" for a,b in iv]
def clash(a,b): return a[0]<b[1] and b[0]<a[1]
st=[]; taken=[]
for i in sorted(range(3),key=lambda i:iv[i][1]-iv[i][0]):
    a=iv[i]; c=[x for x in taken if clash(a,x)]
    if not c:
        taken.append(a); note=f"Shortest-first examines {a[0]}-{a[1]}, the shortest span left with length {a[1]-a[0]}, and takes it."
    else:
        note=f"The span {a[0]}-{a[1]} starts at {a[0]} and ends at {a[1]}, so it overlaps the taken {c[0][0]}-{c[0][1]} and is skipped."
    st.append({"at":{"i":i},"vars":{"rule":"shortest first","taken":len(taken)},"note":note})
assert len(taken)==1
taken=[]; free=None
for i in sorted(range(3),key=lambda i:iv[i][1]):
    a=iv[i]
    if free is None:
        taken.append(a); free=a[1]; note=f"Earliest-finish sorts by end and takes {a[0]}-{a[1]} first, since it ends at {a[1]}."
    elif a[0]>=free:
        taken.append(a); note=f"The span {a[0]}-{a[1]} starts at {a[0]}, not before the boundary {free}, so it is taken. Two spans beat the one that shortest-first found."; free=a[1]
    else:
        note=f"The span {a[0]}-{a[1]} starts at {a[0]}, before the boundary {free}, so it is rejected."
    st.append({"at":{"i":i},"vars":{"rule":"earliest finish","taken":len(taken)},"note":note})
assert len(taken)==2
fill(CH,F,block(cells,["i"],st),"@@TRACE2@@")
