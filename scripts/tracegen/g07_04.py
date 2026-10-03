from common import *
from collections import defaultdict
CH='07-prefix-sums-and-difference-arrays'
F='04-prefix-counts.md'
def run(a,k,third_note=None):
    seen=defaultdict(int); seen[0]=1; p=0; ans=0; st=[]
    for i,x in enumerate(a):
        p+=x; need=p-k; hit=seen[need]; ans+=hit; seen[p]+=1
        st.append({"at":{"i":i},"vars":{"balance":p,"need":need,"found":hit,"answer":ans},"note":f"The balance is {p}, so the complement is {need}. The table holds it {hit} times, so the answer is {ans}. Then record the balance {p}."})
    return st,ans
a=[3,4,7,2,-3,1,4,2]
st,ans=run(a,7); assert ans==4 and st[2]["vars"]["balance"]==14 and st[2]["vars"]["need"]==7 and st[2]["vars"]["found"]==1
fill(CH,F,block([str(x) for x in a],["i"],st),"@@TRACE1@@")
a=[0,0,0]
st,ans=run(a,0); assert ans==6 and st[2]["vars"]["found"]==3
fill(CH,F,block([str(x) for x in a],["i"],st),"@@TRACE2@@")
