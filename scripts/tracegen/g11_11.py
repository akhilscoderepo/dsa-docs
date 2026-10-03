from common import *
CH='11-stacks-and-queues'
F='11-infix-and-postfix-evaluation.md'
tok=["2","3","4","*","-","5","+"]
vals=[]; st=[]
for i,t in enumerate(tok):
    if t in "+-*/" and len(t)==1:
        r=vals.pop(); l=vals.pop()
        v={'+':l+r,'-':l-r,'*':l*r}[t]
        vals.append(v)
        note=f"The key {t} pops {r} first as the right operand and {l} second as the left operand, then pushes {l} {t} {r} = {v}."
    else:
        vals.append(int(t)); note=f"The number {t} is pushed onto the value stack."
    st.append({"at":{"t":i},"vars":{"values":str(vals).replace(' ','')},"note":note})
assert vals==[-5]
fill(CH,F,block(tok,["t"],st),"@@TRACE1@@")
cells=["3","+","2","*","4","-","6","/","2"]
prec=lambda o:2 if o in "*/" else 1
out=[];ops=[];st=[]
for i,c in enumerate(cells):
    if c.isdigit():
        out.append(c); note=f"The number {c} goes straight to the output."
    else:
        rel=[]
        while ops and prec(ops[-1])>=prec(c): rel.append(ops.pop())
        out.extend(rel); ops.append(c)
        note=(f"The operator {c} first releases {''.join(rel)} to the output because it binds at least as tightly, and then waits on the operator stack." if rel else f"The operator {c} binds tighter than the waiting operator or finds none, so it waits on the operator stack.")
    st.append({"at":{"t":i},"vars":{"output":" ".join(out),"waiting":"".join(ops)},"note":note})
out.extend(reversed(ops)); ops=[]
assert out==["3","2","4","*","+","6","2","/","-"]
st[-1]["note"]+=" At the end the waiting operators leave in reverse order, so the output is 3 2 4 * + 6 2 / -."
fill(CH,F,block(cells,["t"],st),"@@TRACE2@@")
