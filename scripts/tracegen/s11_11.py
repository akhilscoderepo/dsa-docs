from common import *
CH='11-stacks-and-queues'; FILE='11-infix-and-postfix-evaluation.md'
def tdiv(a,b):
    q=abs(a)//abs(b); return q if (a<0)==(b<0) else -q
OPS={'+':lambda a,b:a+b,'-':lambda a,b:a-b,'*':lambda a,b:a*b,'/':tdiv}
fmt=lambda d:"["+", ".join(map(str,d))+"]"
def eval_run(toks):
    vals=[]; steps=[]
    for i,t in enumerate(toks):
        if t in OPS:
            r=vals.pop(); l=vals.pop(); v=OPS[t](l,r); vals.append(v)
            note=f"{t} pops the right operand {r}, then the left operand {l}, and pushes {l} {t} {r} = {v}."
        else:
            vals.append(int(t)); note=f"The number {t} goes on the stack."
        steps.append({"at":{"i":i},"vars":{"values":fmt(vals)},"note":note})
    assert len(vals)==1
    return vals[0],steps
PR={'+':1,'-':1,'*':2,'/':2}
def conv_run(toks):
    out=[]; ops=[]; steps=[]
    for i,t in enumerate(toks):
        if t in PR:
            popped=[]
            while ops and PR[ops[-1]]>=PR[t]: popped.append(ops.pop()); out.append(popped[-1])
            ops.append(t)
            if popped: note=f"{t} pops {' and '.join(popped)} to the output, because they bind at least as tightly, and then waits."
            elif len(ops)==1: note=f"{t} finds no waiting operator, so it waits."
            else: note=f"{t} binds tighter than the waiting {ops[-2]}, so it pops nothing and waits above it."
        else:
            out.append(t); note=f"The number {t} goes straight to the output."
        steps.append({"at":{"i":i},"vars":{"output":" ".join(out),"ops":fmt(ops)},"note":note})
    left=[]
    while ops: left.append(ops.pop()); out.append(left[-1])
    steps.append({"at":{"i":len(toks)},"vars":{"output":" ".join(out),"ops":"[]"},"note":f"The end of the text pops the waiting {' and '.join(left)} to the output."})
    return out,steps
v,st=eval_run("20 4 - 3 2 / *".split()); assert v==16
fill(CH,FILE,block("20 4 - 3 2 / *".split(),["i"],st),"@@TRACE1@@")
out,st=conv_run("8 - 3 * 2 + 1".split()); assert " ".join(out)=="8 3 2 * - 1 +"
assert eval_run(out)[0]==8-3*2+1==3
fill(CH,FILE,block("8 - 3 * 2 + 1".split(),["i"],st),"@@TRACE2@@")
# prose and example claims
assert 8-3==5 and 3-8==-5 and 6//2==3 and 2//6==0 and tdiv(-7,2)==-3
assert eval_run(["6","-4","/","5","+"])[0]==4 and tdiv(6,-4)==-1
assert eval_run("9 3 4 - * 2 /".split())[0]==-4
assert eval_run(["-7","2","/","-3","*"])[0]==9 and tdiv(-7,2)==-3
assert eval_run(conv_run("9 / 2 * 4 - 7".split())[0])[0]==9 and tdiv(9,2)==4
assert eval_run(conv_run("6 - 2 - 3".split())[0])[0]==1
assert 20-4==16 and tdiv(3,2)==1
n=1000; moves=0; L=2*n-1
for _ in range(n-1): moves+=(L-2)+(L-3); L-=2   # remove(1) twice shifts L-2 then L-3 elements
assert 1_900_000<moves<2_100_000,moves
