from common import *
CH='10-intervals'; FILE='91-sort-then-scan.md'
w=[[5,7],[1,4],[3,6],[9,9]]
s=sorted(w); assert s==[[1,4],[3,6],[5,7],[9,9]]
st=[{"at":{"i":-1},"vars":{"active":"none","covered":0},"note":"The windows are sorted by start. Nothing has been read yet."}]
fr,to=s[0]; cov=0
st.append({"at":{"i":0},"vars":{"active":f"[{fr},{to}]","covered":cov},"note":f"The first window [{fr},{to}] becomes the active interval."})
for i in range(1,len(s)):
    a,b=s[i]
    if a<=to:
        to=max(to,b); note=f"The start {a} is at most the active end, so the window joins and the active end becomes {to}."
    else:
        cov+=to-fr+1; note=f"The start {a} is after the active end {to}, so [{fr},{to}] is finished and adds {to-fr+1} hours. The window [{a},{b}] becomes active."; fr,to=a,b
    st.append({"at":{"i":i},"vars":{"active":f"[{fr},{to}]","covered":cov},"note":note})
cov+=to-fr+1
st.append({"at":{"i":len(s)},"vars":{"active":"none","covered":cov},"note":f"The last active interval adds {to-fr+1} hour. The total is {cov} hours."})
assert cov==8
fill(CH,FILE,block([x[0] for x in s],["i"],st),"@@TRACE1@@")
b=[[10,16],[2,8],[1,6],[7,12]]
s=sorted(b,key=lambda p:p[1]); assert s==[[1,6],[2,8],[7,12],[10,16]]
arrows=[s[0][1]]; st=[{"at":{"i":-1},"vars":{"arrows":"none"},"note":"The balloons are sorted by end."},{"at":{"i":0},"vars":{"arrows":str(arrows)},"note":"The first arrow goes to the smallest end, 6."}]
for i in range(1,len(s)):
    a,e=s[i]
    if a>arrows[-1]:
        arrows.append(e); note=f"The start {a} is after the arrow at {arrows[-2]}, so the arrow misses [{a},{e}]. A new arrow goes to {e}."
    else: note=f"The start {a} is at most the arrow at {arrows[-1]}, so the arrow bursts [{a},{e}]."
    st.append({"at":{"i":i},"vars":{"arrows":str(arrows)},"note":note})
assert arrows==[6,12]
fill(CH,FILE,block([x[1] for x in s],["i"],st),"@@TRACE2@@")
