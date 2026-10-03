from common import *
CH='11-stacks-and-queues'
F='07-min-stack.md'
ops=["push 5","push 3","push 7","min","pop","pop","min"]
stk=[]; st=[]; ans=[]
for i,o in enumerate(ops):
    if o.startswith("push"):
        v=int(o.split()[1]); m=min(v,stk[-1][1]) if stk else v; stk.append((v,m))
        note=f"The reading {v} is pushed with the coldest value {m}, which is the smaller of {v} and the pair below."
    elif o=="min":
        ans.append(stk[-1][1]); note=f"The question reads the top pair and answers {stk[-1][1]} without scanning."
    else:
        v,m=stk.pop(); note=f"The top pair with reading {v} is crossed out, and the pair below now carries the coldest value of what remains."
    st.append({"at":{"op":i},"vars":{"pairs":str(stk).replace(' ',''),"answers":str(ans).replace(' ','')},"note":note})
assert ans==[3,5]
fill(CH,F,block(ops,["op"],st),"@@TRACE1@@")
ops=["push 4","push 4","push 2","pop","pop","min"]
vals=[];mins=[];st=[]
for i,o in enumerate(ops):
    if o.startswith("push"):
        v=int(o.split()[1]); vals.append(v)
        if not mins or v<=mins[-1]:
            mins.append(v); note=f"The reading {v} is at most the current minimum, so it is recorded on the minimum stack as well."
        else: note=f"The reading {v} is larger than the current minimum, so it is not recorded."
    elif o=="pop":
        v=vals.pop()
        if v==mins[-1]:
            mins.pop(); note=f"The reading {v} equals the top of the minimum stack, so its record is removed too."
        else: note=f"The reading {v} is not the recorded minimum, so the minimum stack is untouched."
    else:
        note=f"The question reads the top of the minimum stack and answers {mins[-1]}."
    st.append({"at":{"op":i},"vars":{"values":str(vals).replace(' ',''),"mins":str(mins).replace(' ','')},"note":note})
assert mins==[4]
st[3]["note"]="The reading 2 equals the top of the minimum stack, so its record is removed too."
st[4]["note"]="The reading 4 is crossed out and its record is removed, but the other copy of 4 is still standing and still recorded, so the minimum stack keeps one entry."
st[4]["vars"]["mins"]="[4]"
fill(CH,F,block(ops,["op"],st),"@@TRACE2@@")
