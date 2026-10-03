from common import *
CH='05-sorting-and-java-comparators'
a=[9,4,7,1,8,2]; lo,hi=1,5
sl=a[lo:hi]; res=a[:lo]+sorted(sl)+a[hi:]
assert res==[9,1,4,7,8,2]
st=[{"at":{"from":lo,"to":hi},"vars":{"slice":",".join(map(str,sl)),"length":hi-lo},"note":f"The call covers positions {lo} up to but not including {hi}, so the slice is {', '.join(map(str,sl))} and its length is {hi-lo}. Positions 0 and {hi} are outside it."},
{"at":{"from":lo,"to":hi},"vars":{"sortedSlice":",".join(map(str,sorted(sl)))},"note":f"Only the slice is put in order, giving {', '.join(map(str,sorted(sl)))}."},
{"at":{"from":lo,"to":hi},"vars":{"array":",".join(map(str,res)),"position0":res[0],"position5":res[5]},"note":f"The array after the call is {', '.join(map(str,res))}. The values 9 and 2 at the ends did not move."}]
import pathlib
if "@@TRACE1@@" in (ROOT/CH/'02-arrays-sort.md').read_text(): fill(CH,'02-arrays-sort.md',block(a,["from","to"],st),"@@TRACE1@@")
orig=[8,3,6,1,6,9]; s=sorted(orig); st=[]; found=None
for i in range(1,len(s)):
    if s[i]==s[i-1]:
        st.append({"at":{"i":i},"vars":{"previous":s[i-1],"current":s[i],"verdict":"repeat"},"note":f"Position {i} holds {s[i]} and position {i-1} holds {s[i-1]}. They are equal, so a repeat exists and the scan returns true here."}); found=True; break
    st.append({"at":{"i":i},"vars":{"previous":s[i-1],"current":s[i]},"note":f"Position {i} holds {s[i]} and position {i-1} holds {s[i-1]}. They differ, so keep scanning."})
assert found and s==[1,3,6,6,8,9]
fill(CH,'02-arrays-sort.md',block(s,["i"],st),"@@TRACE2@@")
