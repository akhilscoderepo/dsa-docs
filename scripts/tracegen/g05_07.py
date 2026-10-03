from common import *
CH='05-sorting-and-java-comparators'
F='07-sort-and-deduplicate.md'
a=sorted([4,1,4,2,1,4]); st=[]; run=0; emitted=[]
for i,x in enumerate(a):
    if i==0 or x!=a[i-1]:
        note=("The first position begins a run." if i==0 else f"The value changes from {a[i-1]} to {x}, so the run of {a[i-1]} ends with length {run} and a new run begins.")
        run=1; emitted.append(x)
    else:
        run+=1; note=f"{x} equals the previous value, so the current run has length {run}."
    st.append({"at":{"i":i},"vars":{"value":x,"runLength":run,"representatives":",".join(map(str,emitted))},"note":note+f" Representatives so far: {', '.join(map(str,emitted))}."})
assert emitted==[1,2,4] and "ends with length 2" in st[2]["note"]
fill(CH,F,block(a,["i"],st),"@@TRACE1@@")
both=sorted(sorted(set([4,9,5,9]))+sorted(set([9,4,9,8,4]))); st=[]; out=[]
for i in range(1,len(both)):
    if both[i]==both[i-1]:
        out.append(both[i]); note=f"Position {i} holds {both[i]} and position {i-1} holds {both[i-1]}. The value came from both arrays, so report {both[i]}."
    else: note=f"Position {i} holds {both[i]} and position {i-1} holds {both[i-1]}. They differ, so nothing is reported."
    st.append({"at":{"i":i},"vars":{"previous":both[i-1],"current":both[i],"common":",".join(map(str,out))},"note":note})
assert both==[4,4,5,8,9,9] and out==[4,9]
fill(CH,F,block(both,["i"],st),"@@TRACE2@@")
