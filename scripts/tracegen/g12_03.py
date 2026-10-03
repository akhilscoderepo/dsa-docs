from common import *
CH='12-monotonic-stacks'
F='03-stock-span.md'

def fmt(st): return "["+", ".join(f"({p},{s})" for p,s in st)+"]"
def sim(a):
    st=[]; out=[]; steps=[]
    for i,p in enumerate(a):
        span=1; popped=[]
        while st and st[-1][0]<=p:
            q=st.pop(); span+=q[1]; popped.append(q)
        st.append((p,span)); out.append(span)
        if popped:
            names=", ".join(f"({q[0]},{q[1]})" for q in popped)
            eq=any(q[0]==p for q in popped)
            note=f"The price {p} removes {names}, so the span is 1 plus their spans, which is {span}."+(" An equal price is removed as well, because equal days are inside the run." if eq else "")
        else:
            note=f"The price {p} is lower than the top, or the stack is empty, so nothing is removed and the span is 1."
        steps.append({"at":{"i":i},"vars":{"span":span,"pairs":fmt(st)},"note":note})
    return steps,out

a=[40,30,20,35,25,38,50]
s1,r=sim(a); assert r==[1,1,1,3,1,5,7] and len(s1)==7
assert s1[3]["vars"]["pairs"]=="[(40,1), (35,3)]"
fill(CH,F,block(a,["i"],s1),"@@TRACE1@@")
b=[5,5,3,5]
s2,r=sim(b); assert r==[1,2,1,4]
assert s2[1]["vars"]["pairs"]=="[(5,2)]"
fill(CH,F,block(b,["i"],s2),"@@TRACE2@@")
