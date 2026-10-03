from common import *
CH='05-sorting-and-java-comparators'
F='08-sort-then-scan.md'
a=sorted([2,2,3,1,5,5],reverse=True); st=[]; place=0; ans=None
for i,x in enumerate(a):
    if i==0: place=1; note=f"{x} is the first value, so it begins the first place."
    elif x!=a[i-1]: place+=1; note=f"The value falls from {a[i-1]} to {x}, so place {place} begins."
    else: note=f"{x} equals the previous value, so it shares place {place}."
    if place==3:
        ans=x; note+=f" Place three has been reached, so the answer is {x}."
    st.append({"at":{"i":i},"vars":{"value":x,"place":place},"note":note})
    if ans is not None: break
assert ans==2 and len(st)==4
fill(CH,F,block(a,["i"],st),"@@TRACE1@@")
b=sorted([3,0,1,4]); st=[]
for i,x in enumerate(b):
    if x==i: st.append({"at":{"i":i},"vars":{"expected":i,"value":x},"note":f"Position {i} holds {x}, which equals its index, so nothing is missing so far."})
    else:
        st.append({"at":{"i":i},"vars":{"expected":i,"value":x,"answer":i},"note":f"Position {i} holds {x} but should hold {i}. The number {i} is missing, so the scan returns {i}."}); break
assert st[-1]["vars"]["answer"]==2 and len(st)==3
fill(CH,F,block(b,["i"],st),"@@TRACE2@@")
