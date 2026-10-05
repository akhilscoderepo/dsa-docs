from common import *
CH='10-intervals'; FILE='03-merge-insert.md'
S=lambda l:" ".join(f"[{a},{b}]" for a,b in l) if l else "none"
w=[[8,10],[1,3],[2,6],[6,7],[15,18]]
s=sorted(w,key=lambda p:(p[0],p[1]))
res=[]; st=[{"at":{"i":-1},"vars":{"result":"none"},"note":"The windows are sorted by start. The result is empty."}]
for i,(a,b) in enumerate(s):
    if not res or res[-1][1]<a:
        res.append([a,b]); note=f"The start {a} is after the active end, or the result is empty, so [{a},{b}] opens a new active interval."
        if i==0: note=f"The result is empty, so [{a},{b}] becomes the active interval."
    else:
        old=res[-1][1]; res[-1][1]=max(old,b); note=f"The start {a} is at most the active end {old}, so the window joins and the active end becomes {res[-1][1]}."
    st.append({"at":{"i":i},"vars":{"window":f"[{a},{b}]","result":S(res)},"note":note})
assert res==[[1,7],[8,10],[15,18]]
fill(CH,FILE,block([x[0] for x in s],["i"],st),"@@TRACE1@@")
lst=[[1,2],[3,5],[6,7],[8,10],[12,16]]; add=[4,9]
start,end=add; out=[]; i=0
st=[{"at":{"i":-1},"vars":{"new":"[4,9]","part":"start"},"note":"The list is sorted and has no overlaps. The new interval is [4,9]."}]
while i<len(lst) and lst[i][1]<start:
    out.append(lst[i]); st.append({"at":{"i":i},"vars":{"part":"copy before","output":S(out)},"note":f"The entry [{lst[i][0]},{lst[i][1]}] ends before {start}, so it is copied."}); i+=1
while i<len(lst) and lst[i][0]<=end:
    start=min(start,lst[i][0]); end=max(end,lst[i][1])
    st.append({"at":{"i":i},"vars":{"part":"absorb","merged":f"[{start},{end}]"},"note":f"The entry [{lst[i][0]},{lst[i][1]}] starts at or before the merged end, so the merged interval becomes [{start},{end}]."}); i+=1
out.append([start,end])
st.append({"at":{"i":i},"vars":{"part":"write merged","output":S(out)},"note":f"The entry [{lst[i][0]},{lst[i][1]}] starts after the merged end {end}, so the block ends. The merged interval [{start},{end}] is written."})
while i<len(lst):
    out.append(lst[i]); i+=1
st.append({"at":{"i":len(lst)},"vars":{"part":"copy after","output":S(out)},"note":"The remaining entries are copied unchanged. The pass is complete."})
assert out==[[1,2],[3,10],[12,16]]
fill(CH,FILE,block([x[0] for x in lst],["i"],st),"@@TRACE2@@")
