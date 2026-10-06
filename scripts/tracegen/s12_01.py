from common import *
CH='12-monotonic-stacks'; FILE='01-next-greater-or-smaller.md'
def fmt(l): return "["+", ".join(map(str,l))+"]"
def run(vals):
    st=[]; ans=[None]*len(vals); steps=[]
    show=lambda: "["+", ".join("." if a is None else str(a) for a in ans)+"]"
    for i,v in enumerate(vals):
        while st and vals[st[-1]]<v:
            t=st.pop(); ans[t]=v
            steps.append({"at":{"i":i},"vars":{"stack":fmt(st),"ans":show()},"note":f"{v} is greater than nums[{t}] = {vals[t]}, so ans[{t}] becomes {v} and index {t} leaves the stack."})
        why = "The stack is empty or its top value is not smaller, so no pop happens" if True else ""
        st.append(i)
        steps.append({"at":{"i":i},"vars":{"stack":fmt(st),"ans":show()},"note":f"Index {i} with value {v} goes on top of the stack."})
    steps.append({"at":{"i":len(vals)},"vars":{"stack":fmt(st),"ans":show()},"note":f"The scan ends. Indices {fmt(st)} stay on the stack and keep -1."})
    return [-1 if a is None else a for a in ans],steps
V1=[6,2,4,3,9,5,7]; a,s=run(V1); assert a==[9,4,9,9,-1,7,-1]; fill(CH,FILE,block(V1,["i"],s),"@@TRACE1@@")
V2=[4,4,2,4,5]; a,s=run(V2); assert a==[5,5,4,5,-1]; fill(CH,FILE,block(V2,["i"],s),"@@TRACE2@@")
