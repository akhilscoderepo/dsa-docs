from common import *
CH='11-stacks-and-queues'; FILE='05-matching-delimiters.md'
PAIR={')':'(',']':'[','}':'{'}
def run(text,ph):
    st=[]; stack=[]; n=len(text); ok=True
    fmt=lambda d: "["+", ".join(d)+"]"
    for i,c in enumerate(text):
        if c in "([{":
            stack.append(c)
            st.append({"at":{"i":i},"vars":{"stack":fmt(stack),"char":c},"note":f"{c} is an opening, so the scan pushes it."})
        else:
            if not stack:
                ok=False; st.append({"at":{"i":i},"vars":{"stack":"[]","char":c},"note":"The stack is empty, so the scan stops with false."}); break
            o=stack.pop()
            if o!=PAIR[c]:
                ok=False; st.append({"at":{"i":i},"vars":{"stack":fmt(stack),"char":c,"popped":o},"note":f"{c} pops {o}, and the partner of {c} is {PAIR[c]}. This is a mismatch, so the scan stops with false."}); break
            st.append({"at":{"i":i},"vars":{"stack":fmt(stack),"char":c,"popped":o},"note":f"{c} pops {o}, which is its partner."})
    else:
        ok=not stack
        st.append({"at":{"i":n},"vars":{"stack":fmt(stack),"result":str(ok).lower()},"note":"The text ends with an empty stack, so the result is true."})
    fill(CH,FILE,block(list(text),["i"],st),ph); return ok
assert run("([]{})","@@TRACE1@@") is True
assert run("([)]","@@TRACE2@@") is False
# recompute exercise examples
def red(s):
    while True:
        t=s.replace("()","").replace("[]","").replace("{}","")
        if t==s: return s
        s=t
assert red("(()())")=="" and red(")(")!="" and (")(").count("(")==(")(").count(")")
assert red("{[()]}[]")=="" and red("{[}]")!=""
def first_err(s):
    st=[]
    for i,c in enumerate(s):
        if c in "([{": st.append(i)
        else:
            if not st or s[st.pop()]!=PAIR[c]: return i
    return st[-1] if st else -1
assert first_err("())(")==2 and first_err("[(()")==1 and first_err("([)]")==2
def outer(s):
    d=0;o=""
    for c in s:
        if c=="(":
            if d>0:o+=c
            d+=1
        else:
            d-=1
            if d>0:o+=c
    return o
assert outer("((()))()(())")=="(())()" and outer("()()")==""
k=50000
rounds=0;s="("*k+")"*k;tot=0
assert k*(k+1)==2500050000
