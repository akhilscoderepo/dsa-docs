from common import *
CH='11-stacks-and-queues'; FILE='09-nested-decoding.md'
def decode(s):
    st=[]; cur=""; count=0; steps=[]
    f=lambda: "["+", ".join(f'("{p}", {t})' for p,t in st)+"]"
    for i,c in enumerate(s):
        if c.isdigit():
            count=count*10+int(c); note=f"The digit {c} makes count {count}."
        elif c=='[':
            st.append((cur,count)); note=f"[ saves the parent text \"{cur}\" with the number {count}, then cur and count start fresh."; cur=""; count=0
        elif c==']':
            p,t=st.pop(); note=f"] pops the frame, so the body \"{cur}\" is appended {t} times after \"{p}\"."; cur=p+cur*t
        else:
            cur+=c; note=f"The letter {c} joins cur."
        steps.append({"at":{"i":i},"vars":{"cur":cur,"count":count,"stack":f()},"note":note})
    assert not st
    steps.append({"at":{"i":len(s)},"vars":{"cur":cur,"count":count,"stack":"[]"},"note":"The text ends with an empty stack, and cur holds the decoded text."})
    return cur,steps
for s,ph,exp in [("2[x3[yz]w]","@@TRACE1@@","xyzyzyzwxyzyzyzw"),("2[ab]10[c]","@@TRACE2@@","ababcccccccccc")]:
    out,steps=decode(s); assert out==exp,out
    fill(CH,FILE,block(list(s),["i"],steps),ph)
# predict and bottleneck claims
def rewrite_total(k):
    s="1["*k+"x"+"]"*k; tot=0; passes=0
    while "]" in s:
        c=s.index("]"); o=s.rindex("[",0,c); st=o
        while st>0 and s[st-1].isdigit(): st-=1
        s=s[:st]+s[o+1:c]*int(s[st:o])+s[c+1:]; tot+=len(s); passes+=1
    assert s=="x" and passes==k
    return tot
for k in range(1,30): assert rewrite_total(k)==3*k*(k-1)//2+k
assert 3*50000*49999//2+50000==3749975000
assert 9**4==6561
