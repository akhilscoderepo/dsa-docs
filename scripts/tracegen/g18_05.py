from common import *
CH='18-tries'; F='05-binary-tries.md'
W=5
def bits(v): return [(v>>b)&1 for b in range(W-1,-1,-1)]
def mk(vals):
    root={}
    for v in vals:
        c=root
        for bit in bits(v): c=c.setdefault(bit,{})
    return root
root=mk([10]); st=[]; c=root; created=0; v=8
for i,bit in enumerate(bits(v)):
    b=W-1-i
    if bit in c: note=f"The bit {bit} at position {b} already has a child, so the insert reuses it."
    else: c[bit]={}; created+=1; note=f"The bit {bit} at position {b} has no child, so the insert creates one."
    c=c[bit]
    st.append({"at":{"i":i},"vars":{"created":created},"note":note})
assert created==2
fill(CH,F,block(bits(v),["i"],st),"@@TRACE1@@")
vals=[3,10,5,25,2,8]; root=mk(vals); x=5; c=root; res=0; st=[]; pre=""
for i,bit in enumerate(bits(x)):
    b=W-1-i; opp=1-bit
    if opp in c:
        res|=1<<b; c=c[opp]; pre+=str(opp)
        note=f"The bit of x at position {b} is {bit}, and a child {opp} exists, so the walk takes it. The result gains {1<<b}."
    else:
        c=c[bit]; pre+=str(bit)
        note=f"The bit of x at position {b} is {bit}, and no child {opp} exists, so the walk takes the child {bit}. The result gains 0."
    st.append({"at":{"i":i},"vars":{"result":res,"partner":pre},"note":note})
assert res==28 and max(x^y for y in vals)==28
fill(CH,F,block(bits(x),["i"],st),"@@TRACE2@@")
