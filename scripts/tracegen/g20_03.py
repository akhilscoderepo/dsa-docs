from common import *
CH='20-greedy'
F='03-farthest-frontier.md'
def scan(a):
    far=0; st=[]; ok=True
    for i,v in enumerate(a):
        if i>far:
            st.append({"at":{"i":i},"vars":{"far":far,"verdict":"cut off"},"note":f"Tower {i} lies beyond the frontier {far}, so no reachable tower can pass a message this far and the scan stops with a no."})
            ok=False; break
        old=far; far=max(far,i+v)
        if v==0: note=f"Tower {i} is dead with strength 0, and the frontier {far} already lies beyond it, so nothing changes." if far>i else f"Tower {i} is dead with strength 0 and sits exactly on the frontier {far}, so the frontier cannot grow."
        elif far>old: note=f"Tower {i} with strength {v} reaches {i+v}, so the frontier grows from {old} to {far}."
        else: note=f"Tower {i} with strength {v} reaches only {i+v}, which does not beat the frontier {old}, so it stays."
        if i==len(a)-1: note=f"Tower {i} is the summit and lies inside the frontier {far}, so the message arrives."
        st.append({"at":{"i":i},"vars":{"far":far},"note":note})
    return st,ok
a=[3,1,0,2,0,5]
st,ok=scan(a); assert ok and st[-1]["at"]["i"]==5
fill(CH,F,block([str(x) for x in a],["i"],st),"@@TRACE1@@")
b=[2,1,0,0,3]
st,ok=scan(b); assert not ok and st[-1]["at"]["i"]==3 and st[-1]["vars"]["far"]==2
fill(CH,F,block([str(x) for x in b],["i"],st),"@@TRACE2@@")
c=[4,1,1,3,1,1,1]
n=len(c); jumps=0; cur=0; far=0; st=[]
for i in range(n-1):
    far=max(far,i+c[i])
    if i==cur:
        jumps+=1; cur=far
        note=f"Tower {i} ends the layer. The record is {far}, so relay number {jumps} is counted and the next layer ends at {cur}."
        if i==0: note=f"Tower 0 is the first layer on its own, with record {far}, so relay number 1 is counted and the next layer ends at {cur}."
        st.append({"at":{"i":i},"vars":{"far":far,"curEnd":cur,"jumps":jumps},"note":note})
        if cur>=n-1: break
    else:
        st.append({"at":{"i":i},"vars":{"far":far,"curEnd":cur,"jumps":jumps},"note":f"Tower {i} has strength {c[i]} and reaches {i+c[i]}, so the record is {far}. The layer continues."})
assert jumps==2 and st[-1]["at"]["i"]==4
fill(CH,F,block([str(x) for x in c],["i"],st),"@@TRACE3@@")
