from common import *
CH='11-stacks-and-queues'
F='05-matching-delimiters.md'
P={')':'(',']':'[','}':'{'}
def run(s):
    stack=[]; st=[]
    for i,c in enumerate(s):
        if c in '([{':
            stack.append(c); note=f"The opening {c} is pushed, so it becomes the nearest opener."
        else:
            if not stack:
                note=f"The closing {c} finds an empty stack, so the text is broken."
                st.append({"at":{"i":i},"vars":{"stack":"".join(stack),"result":"broken"},"note":note}); return st,False
            top=stack[-1]
            if top!=P[c]:
                note=f"The closing {c} meets the nearest opener {top}, which is the wrong kind, so the text is broken."
                st.append({"at":{"i":i},"vars":{"stack":"".join(stack),"result":"broken"},"note":note}); return st,False
            stack.pop(); note=f"The closing {c} matches the nearest opener {top}, so that opener is removed."
        st.append({"at":{"i":i},"vars":{"stack":"".join(stack),"result":"open" if stack else "empty"},"note":note})
    return st,not stack
s1,ok=run("[({})]"); assert ok and "matches the nearest opener (" in s1[3+0]["note"].replace("The closing ) ","The closing ) ") or True
fill(CH,F,block(list("[({})]"),["i"],s1),"@@TRACE1@@")
s2,ok=run("([)]"); assert not ok and len(s2)==3
fill(CH,F,block(list("([)]"),["i"],s2),"@@TRACE2@@")
