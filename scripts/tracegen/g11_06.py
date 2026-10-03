from common import *
CH='11-stacks-and-queues'
F='06-nested-structure.md'
s="(()(()))"
frames=[]; top=0; st=[]
for i,c in enumerate(s):
    if c=='(':
        frames.append(top); top=0
        note="An opening bracket saves the current total and starts a new level with zero."
    else:
        child=top; val=max(2*child,1); top=frames.pop()+val
        note=f"A closing bracket finishes a group with inner total {child}, which is worth {val}, and the parent total becomes {top}."
    st.append({"at":{"i":i},"vars":{"saved":str(frames).replace(' ',''),"current":top},"note":note})
assert top==6
fill(CH,F,block(list(s),["i"],st),"@@TRACE1@@")
s="1(2(3))4"
frames=[]; acc=0; st=[]
for i,c in enumerate(s):
    if c=='(':
        frames.append(acc); acc=0
        note=f"An opening bracket saves the total so far and starts a new level with zero."
    elif c==')':
        child=acc; acc=frames.pop()+2*child
        note=f"A closing bracket finishes a group worth {child}, so the saved total receives twice that and the current total becomes {acc}."
    else:
        acc+=int(c); note=f"The part {c} is added to the innermost open level, so the current total becomes {acc}."
    st.append({"at":{"i":i},"vars":{"saved":str(frames).replace(' ',''),"current":acc},"note":note})
assert acc==21
fill(CH,F,block(list(s),["i"],st),"@@TRACE2@@")
