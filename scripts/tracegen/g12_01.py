from common import *
CH='12-monotonic-stacks'
F='01-next-greater-or-smaller.md'

def sim(a):
    st=[]; ans=[-1]*len(a); steps=[]
    for j,v in enumerate(a):
        popped=[]
        while st and v>a[st[-1]]:
            t=st.pop(); ans[t]=v; popped.append(t)
        st.append(j)
        if popped:
            note=f"The value {v} is greater than the waiting value(s) at index "+", ".join(map(str,popped))+f", so each gets the answer {v} and leaves. Index {j} is then pushed."
        elif len(st)==1:
            note=f"The stack is empty, so index {j} (value {v}) is pushed with nothing to resolve."
        else:
            below=a[st[-2]]
            note=f"The value {v} is not greater than {below} on top, so nothing is resolved and index {j} is pushed."
        steps.append({"at":{"j":j},"vars":{"stack":"["+",".join(map(str,st))+"]","answer":"["+",".join(map(str,ans))+"]"},"note":note})
    return steps,ans

a=[5,3,4,1,6]
s1,r=sim(a); assert r==[6,4,6,6,-1] and len(s1)==5
assert s1[4]["vars"]["stack"]=="[4]"
fill(CH,F,block(a,["j"],s1),"@@TRACE1@@")
b=[3,3,2,5]
s2,r=sim(b); assert r==[5,5,5,-1]
assert s2[1]["vars"]["stack"]=="[0,1]"
fill(CH,F,block(b,["j"],s2),"@@TRACE2@@")
