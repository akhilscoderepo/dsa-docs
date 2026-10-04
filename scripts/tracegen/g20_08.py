from common import *
CH='20-greedy'
F='08-greedy-and-monotonic-stack.md'
num="52913"; k=2; st=[]; stack=[]
for i,c in enumerate(num):
    pops=[]
    while k>0 and stack and stack[-1]>c:
        pops.append(stack.pop()); k-=1
    stack.append(c)
    if pops: note=f"The digit {c} is smaller than {', then '.join(pops)}, so "+("that digit is" if len(pops)==1 else "those digits are")+f" popped, spending removals, and {c} is pushed."
    elif i==0: note=f"The digit {c} starts the stack."
    else: note=f"The digit {c} is larger than the top, so nothing is popped and it is pushed."
    st.append({"at":{"i":i},"vars":{"stack":"".join(stack),"budget":k},"note":note})
assert "".join(stack)=="213" and k==0 and st[-1]["at"]["i"]==4
fill(CH,F,block(list(num),["i"],st),"@@TRACE1@@")
s="dcbadbcd"
last={c:i for i,c in enumerate(s)}
stack=[]; ins=set(); st=[]
for i,c in enumerate(s):
    if c in ins:
        note=f"The letter {c} is already on the stack, so it is skipped."
    else:
        pops=[]
        while stack and stack[-1]>c and last[stack[-1]]>i:
            t=stack.pop(); ins.discard(t); pops.append(t)
        stack.append(c); ins.add(c)
        if pops: note=f"The letter {c} is smaller than the top, and the popped "+(f"letter {pops[0]}" if len(pops)==1 else "letters "+", ".join(pops))+f" appear again later, so the pop is permitted and {c} is pushed."
        elif i==0: note=f"The letter {c} starts the stack."
        else: note=f"The letter {c} is larger than the top, so it is pushed without popping."
    st.append({"at":{"i":i},"vars":{"stack":"".join(stack)},"note":note})
assert "".join(stack)=="abcd"
fill(CH,F,block(list(s),["i"],st),"@@TRACE2@@")
