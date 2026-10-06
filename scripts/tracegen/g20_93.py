from common import *
CH='20-greedy'; F='93-drop-earlier-items-with-a-stack.md'
num="1432219"; k=3; stack=[]; st=[]
for i,d in enumerate(num):
    note=f"The digit {d} is read."
    popped=[]
    while k>0 and stack and stack[-1]>d:
        popped.append(stack.pop()); k-=1
    if popped: note+=f" The top {popped[-1]} is larger, so the loop pops it and spends a deletion."
    else: note+=" No larger top is available or the budget is spent, so nothing is popped."
    stack.append(d)
    st.append({"at":{"i":i},"vars":{"stack":"".join(stack),"k":k},"note":note})
res="".join(stack[:len(stack)-k] if k else stack); assert k==0 and res=="1219"
fill(CH,F,block(list(num),["i"],st),"@@TRACE1@@")
s="cbacdcbc"; last={c:i for i,c in enumerate(s)}; stack=[]; st=[]
for i,c in enumerate(s):
    if c in stack:
        note=f"The letter {c} is already on the stack, so the loop skips it."
    else:
        note=f"The letter {c} is new."
        while stack and stack[-1]>c and last[stack[-1]]>i:
            t=stack.pop(); note+=f" The top {t} is larger and appears later, so the loop pops it."
        stack.append(c)
    st.append({"at":{"i":i},"vars":{"stack":"".join(stack)},"note":note})
assert "".join(stack)=="acdb"
fill(CH,F,block(list(s),["i"],st),"@@TRACE2@@")
