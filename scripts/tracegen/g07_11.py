from common import *
from collections import defaultdict
CH='07-prefix-sums-and-difference-arrays'
F='11-prefix-state-and-maps.md'
a=[1000000000,1000000000,-1000000000]; k=1000000000
seen=defaultdict(int); seen[0]=1; p=0; cnt=0; st=[]
for i,x in enumerate(a):
    p+=x; need=p-k; hit=seen[need]; cnt+=hit; seen[p]+=1
    st.append({"at":{"i":i},"vars":{"total":p,"pairKey":need,"found":hit,"count":cnt},"note":f"The running total is {p} and the paired key is {need}. The table holds it {hit} times, so the count is {cnt}."})
assert cnt==3 and st[2]["vars"]["total"]==1000000000 and st[2]["vars"]["pairKey"]==0 and st[2]["vars"]["found"]==1
fill(CH,F,block([str(x) for x in a],["i"],st),"@@TRACE1@@")
a=[23,2,4,6,7]; k=6; first={0:-1}; tot=0; st=[]
for i,x in enumerate(a):
    tot+=x; cls=tot%k; e=first.get(cls)
    if e is None:
        first[cls]=i
        st.append({"at":{"i":i},"vars":{"total":tot,"key":cls},"note":f"The total is {tot} and the key is {cls}, which is new, so record index {i} as its first position."})
    elif i-e>=2:
        st.append({"at":{"i":i},"vars":{"total":tot,"key":cls,"firstIndex":e,"start":e+1,"end":i},"note":f"The key {cls} was first seen at index {e}, the gap is {i-e}, so the stretch from {e+1} to {i} qualifies and the scan stops."}); break
    else:
        st.append({"at":{"i":i},"vars":{"total":tot,"key":cls,"firstIndex":e},"note":f"The key {cls} was first seen at index {e}, but the gap is only {i-e}, so keep scanning."})
assert len(st)==3 and st[2]["vars"]["start"]==1 and st[2]["vars"]["end"]==2 and st[2]["vars"]["key"]==5
fill(CH,F,block([str(x) for x in a],["i"],st),"@@TRACE2@@")
