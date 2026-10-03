from common import *
CH='11-stacks-and-queues'
F='12-stack-and-parsing-state.md'
parts=["a",".","b","..","c"]
names=[]; st=[]
for i,p in enumerate(parts):
    if p==".": note="The single dot is the current directory, so nothing changes."
    elif p=="..":
        if names: r=names.pop(); note=f"The double dot removes {r}, the newest open directory, from the end of the stack."
        else: note="The double dot finds the stack empty, so it is ignored."
    else:
        names.append(p); note=f"The name {p} is entered, so it is added to the end of the stack."
    st.append({"at":{"p":i},"vars":{"open":"/"+"/".join(names)},"note":note})
assert names==["a","c"]
fill(CH,F,block(parts,["p"],st),"@@TRACE1@@")
s="3[ab2[c]]d"; cap=10**18
frames=[]; cur=0; count=0; st=[]
for i,c in enumerate(s):
    if c.isdigit():
        count=count*10+int(c); note=f"The digit {c} is read, so the count in progress is {count}."
    elif c=='[':
        frames.append((cur,count)); note=f"An opening bracket parks the length {cur} and the count {count}, then starts a new level at length 0."
        cur=0; count=0
    elif c==']':
        pl,pc=frames.pop(); inner=cur; cur=pl+pc*inner
        note=f"A closing bracket repeats the inner length {inner} by {pc}, and the parent length {pl} plus {pc*inner} gives {cur}."
    else:
        cur+=1; note=f"The letter {c} adds one to the current length, which is now {cur}."
    st.append({"at":{"i":i},"vars":{"length":cur,"parked":str(frames).replace(' ','')},"note":note})
assert cur==13
fill(CH,F,block(list(s),["i"],st),"@@TRACE2@@")
