from common import *
CH='10-intervals'; FILE='01-sort-order.md'
def wrap(x): return (x + 2**31) % 2**32 - 2**31
iv=[[5,8],[1,4],[1,2],[3,6]]
s=sorted(iv,key=lambda p:(p[0],p[1]))
assert s==[[1,2],[1,4],[3,6],[5,8]]
st=[{"at":{"i":-1},"vars":{"sorted":"[1,2] [1,4] [3,6] [5,8]"},"note":"The sorted order by start and then end is ready. The pointer is before the first pair."}]
for i in range(1,len(s)):
    a,b=s[i-1],s[i]
    if a[0]==b[0]:
        note=f"The starts tie at {a[0]}, so the ends {a[1]} and {b[1]} decide. The interval with end {a[1]} goes first."
        v={"prev":f"[{a[0]},{a[1]}]","cur":f"[{b[0]},{b[1]}]","deciding key":"end"}
    else:
        note=f"The starts differ, {a[0]} before {b[0]}, so the start alone decides."
        v={"prev":f"[{a[0]},{a[1]}]","cur":f"[{b[0]},{b[1]}]","deciding key":"start"}
    st.append({"at":{"i":i},"vars":v,"note":note})
fill(CH,FILE,block([x[0] for x in s],["i"],st),"@@TRACE1@@")
a,b=2000000000,-2000000000   # a = sorted[1], b = sorted[0]
true=a-b; w=wrap(true)
assert true==4000000000 and w==-294967296 and w<0
st=[{"at":{"i":0},"vars":{"sorted[0].start":"-2000000000"},"note":"The first start is -2,000,000,000, the smaller of the two."},
{"at":{"i":1},"vars":{"true difference":str(true),"wrapped difference":str(w)},"note":"The true difference a minus b is 4,000,000,000, which exceeds the int maximum of 2,147,483,647, so the stored result wraps to -294,967,296."},
{"at":{"i":1},"vars":{"subtraction says":"a first","Integer.compare says":"b first"},"note":"The negative wrapped value tells the sort that the larger start goes first. Integer.compare returns 1 for the same pair and keeps the smaller start first."}]
fill(CH,FILE,block([b,a],["i"],st),"@@TRACE2@@")
