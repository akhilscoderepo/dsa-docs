from common import *
CH='20-greedy'
F='06-greedy-and-ordering.md'
s="xyxzzwvwvu"
last={c:i for i,c in enumerate(s)}
start=0; end=0; st=[]; sizes=[]
for i,c in enumerate(s):
    old=end; end=max(end,last[c])
    if i==end:
        sizes.append(i-start+1)
        note=f"Letter '{c}' has its last occurrence at {last[c]}, and the index has reached the section end {end}, so the section {start} to {i} closes with {i-start+1} character{'s' if i-start+1!=1 else ''}."
        start=i+1
    elif end>old:
        note=f"Letter '{c}' last appears at {last[c]}, which pushes the section end from {old} to {end}."
    else:
        note=f"Letter '{c}' last appears at {last[c]}, inside the current reach {end}, so the section end stays."
    st.append({"at":{"i":i},"vars":{"start":start,"end":end,"sizes":"-".join(map(str,sizes)) or "none"},"note":note})
assert sizes==[3,2,4,1] and st[-1]["at"]["i"]==len(s)-1
fill(CH,F,block(list(s),["i"],st),"@@TRACE1@@")
greed=[7,2,5]; gl=[5,1,3,9]
kids=sorted(range(3),key=lambda i:(greed[i],i)); order=sorted(range(4),key=lambda i:(gl[i],i))
assert [gl[i] for i in order]==[1,3,5,9]
k=0; st=[]; owner=[-1]*4
for pos,c in enumerate(order):
    if k<len(kids) and gl[c]>=greed[kids[k]]:
        owner[c]=kids[k]
        note=f"The glove of size {gl[c]} fits the helper who needs {greed[kids[k]]}, who is next in size order, so it is given to them."
        k+=1
    else:
        note=f"The glove of size {gl[c]} is smaller than the {greed[kids[k]]} that the next helper needs, so it fits nobody and stays unused."
    st.append({"at":{"i":pos},"vars":{"served":k,"nextNeed":(greed[kids[k]] if k<len(kids) else "none")},"note":note})
assert owner==[2,-1,1,0]
fill(CH,F,block([str(gl[c]) for c in order],["i"],st),"@@TRACE2@@")
