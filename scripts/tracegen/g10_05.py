from common import *
CH='10-intervals'; FILE='05-keep-most.md'
S=lambda l:" ".join(f"[{a},{b})" for a,b in l) or "none"
iv=[[1,10],[2,3],[4,5],[6,7],[5,9]]
s=sorted(iv,key=lambda p:p[1]); assert s==[[2,3],[4,5],[6,7],[5,9],[1,10]]
last=None; kept=[]; st=[{"at":{"i":-1},"vars":{"lastEnd":"none","kept":0},"note":"The requests are sorted by end. Nothing is kept yet."}]
for i,(a,b) in enumerate(s):
    if last is None or a>=last:
        kept.append([a,b]); last=b; note=f"The start {a} is at least lastEnd, or nothing is kept yet, so [{a},{b}) is kept and lastEnd becomes {b}."
    else: note=f"The start {a} is before lastEnd {last}, so [{a},{b}) clashes and is skipped."
    st.append({"at":{"i":i},"vars":{"lastEnd":last,"kept":len(kept)},"note":note})
assert len(kept)==3
fill(CH,FILE,block([x[1] for x in s],["i"],st),"@@TRACE1@@")
iv=[[1,4],[3,6],[2,8],[1,2],[8,9]]
s=sorted(iv,key=lambda p:(p[0],-p[1])); assert s==[[1,4],[1,2],[2,8],[3,6],[8,9]]
mx=None; cnt=0; st=[{"at":{"i":-1},"vars":{"maxEnd":"none","notCovered":0},"note":"The requests are sorted by start, with ties by larger end first."}]
for i,(a,b) in enumerate(s):
    if mx is None or b>mx:
        cnt+=1; mx=b; note=f"The end {b} is larger than every earlier end, so [{a},{b}) is not covered and maxEnd becomes {b}."
    else: note=f"The end {b} is at most maxEnd {mx}, so an earlier request covers [{a},{b})."
    st.append({"at":{"i":i},"vars":{"maxEnd":mx,"notCovered":cnt},"note":note})
assert cnt==3
fill(CH,FILE,block([x[0] for x in s],["i"],st),"@@TRACE2@@")
