from common import *
CH='14-linked-lists'
F='09-fixed-gap-kth-from-end.md'
vals=[4,8,6,3,2];n=5;k=2
lead=0;trail=0
st=[{"at":{"lead":0,"trail":0},"vars":{"gap":0},"note":"Both pointers start on the first camel, holding 4. The lead pointer will run ahead by exactly 2 camels."}]
for i in range(k):
    lead+=1
    st.append({"at":{"lead":lead,"trail":0},"vars":{"gap":lead},"note":f"The lead pointer takes step {i+1} of {k} alone and stands on the camel holding {vals[lead]}. The trailing pointer has not moved."})
while lead<n:
    lead+=1
    trail+=1
    ln=f"on the camel holding {vals[lead]}" if lead<n else "past the last camel"
    st.append({"at":{"lead":lead,"trail":trail},"vars":{"gap":lead-trail},"note":f"Both pointers move one camel. The lead is {ln} and the trailing pointer is on the camel holding {vals[trail]}. The gap is still {k}."})
assert trail==3 and lead==5
st[-1]["note"]+=" The lead is past the end, so the trailing pointer stands on the second camel from the end."
fill(CH,F,block(vals,["lead","trail"],st),"@@TRACE1@@")
# trace 2: remove kth=5 from length-5 list using dummy (-1)
k=5
lead=-1;trail=-1
s2=[{"at":{"lead":-1,"trail":-1},"vars":{"list":"4>8>6>3>2"},"note":"Both pointers start on the dummy that stands before the first camel."}]
for i in range(k):
    lead+=1
    s2.append({"at":{"lead":lead,"trail":-1},"vars":{"steps_taken":i+1},"note":f"The lead pointer takes step {i+1} of {k} and stands on the camel holding {vals[lead]}."})
last=lead==n-1
s2.append({"at":{"lead":lead,"trail":-1},"vars":{"list":"4>8>6>3>2"},"note":"The lead is on the last camel, which has no successor, so the trailing pointer never moves. It stays on the dummy, and the camel after the dummy is the one to remove."})
s2.append({"at":{"lead":lead,"trail":-1},"vars":{"list":"8>6>3>2"},"note":"The dummy is pointed past the camel holding 4. The list now reads 8, 6, 3, 2, and the original first camel was removed by the same bypass used anywhere else."})
fill(CH,F,block(vals,["lead","trail"],s2),"@@TRACE2@@")
