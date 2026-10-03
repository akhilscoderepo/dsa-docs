from common import *
from collections import defaultdict
CH='07-prefix-sums-and-difference-arrays'
F='07-prefix-xor.md'
a=[6,2,7,4]; px=[0]; st=[]
for i,x in enumerate(a):
    px.append(px[-1]^x)
    st.append({"at":{"i":i},"vars":{"card":x,"prefixXor":px[-1]},"note":f"XOR the card {x} into the running value, which becomes {px[-1]}, and store it in slot {i+1}."})
assert px==[0,6,4,3,7]
st.append({"at":{"i":3},"vars":{"slotHigh":px[4],"slotLow":px[1],"answer":px[4]^px[1]},"note":f"The query covers positions 1 to 3, so read slot 4, which holds {px[4]}, and slot 1, which holds {px[1]}. Their XOR is {px[4]^px[1]}."})
assert px[4]^px[1]==1==(2^7^4)
fill(CH,F,block([str(x) for x in a],["i"],st),"@@TRACE1@@")
a=[4,2,2,6,4]; k=6; seen=defaultdict(int); seen[0]=1; cur=0; cnt=0; st=[]
for i,x in enumerate(a):
    cur^=x; need=cur^k; hit=seen[need]; cnt+=hit; seen[cur]+=1
    st.append({"at":{"i":i},"vars":{"prefix":cur,"need":need,"found":hit,"count":cnt},"note":f"The prefix is {cur} and the complement {cur} XOR {k} is {need}. It occurred {hit} times before, so the count is {cnt}."})
assert cnt==4 and st[3]["vars"]["prefix"]==2 and st[3]["vars"]["need"]==4 and st[3]["vars"]["found"]==2
fill(CH,F,block([str(x) for x in a],["i"],st),"@@TRACE2@@")
