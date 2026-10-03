from common import *
CH='12-monotonic-stacks'
F='04-boundary-discovery.md'
fmt=lambda l:"["+",".join(map(str,l))+"]"

def left(a):
    st=[];out=[];steps=[]
    for j,v in enumerate(a):
        popped=[]
        while st and a[st[-1]]>=v: popped.append(st.pop())
        w=st[-1] if st else -1
        out.append(w); st.append(j)
        if popped: note=f"The height {v} removes index "+", ".join(map(str,popped))+" because those planks are not shorter. "
        else: note="Nothing is removed. "
        note+=("The stack is empty, so the left wall is the sentinel -1." if w==-1 else f"The surviving top is index {w}, which is shorter, so it is the left wall.")
        steps.append({"at":{"j":j},"vars":{"left":w,"stack":fmt(st)},"note":note})
    return steps,out
def right(a):
    n=len(a);st=[];out=[n]*n;steps=[]
    for j,v in enumerate(a):
        popped=[]
        while st and v<a[st[-1]]:
            t=st.pop(); out[t]=j; popped.append(t)
        st.append(j)
        if popped: note=f"The height {v} is strictly shorter than the waiting plank(s) at index "+", ".join(map(str,popped))+f", so their right wall is {j}. Index {j} is pushed."
        else: note=f"The height {v} is not shorter than the top, or the stack is empty, so nothing is resolved and index {j} is pushed."
        steps.append({"at":{"j":j},"vars":{"right":fmt(out),"stack":fmt(st)},"note":note})
    return steps,out

a=[3,5,4,6,2,7]
s1,r=left(a); assert r==[-1,0,0,2,-1,4] and len(s1)==6 and s1[4]["vars"]["stack"]=="[4]"
fill(CH,F,block(a,["j"],s1),"@@TRACE1@@")
b=[2,5,5,3,1]
s2,r=right(b); assert r==[4,3,3,4,5] and s2[2]["vars"]["stack"]=="[0,1,2]"
fill(CH,F,block(b,["j"],s2),"@@TRACE2@@")
