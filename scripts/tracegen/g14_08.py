from common import *
CH='14-linked-lists'
F='08-middle-nodes.md'
def run(vals):
    n=len(vals);slow=0;fast=0;st=[{"at":{"slow":0,"fast":0},"vars":{"rounds":0},"note":f"Both pointers start on the first lantern, holding {vals[0]}."}]
    r=0
    def nxt(i): return i+1 if i+1<n else -1
    while fast!=-1 and nxt(fast)!=-1:
        slow=nxt(slow);fast=nxt(nxt(fast));r+=1
        fv="past the end" if fast==-1 else f"on the lantern holding {vals[fast]}"
        note=f"Round {r}: slow steps once to the lantern holding {vals[slow]}, and fast steps twice and is {fv}."
        st.append({"at":{"slow":slow,"fast":fast},"vars":{"rounds":r},"note":note})
    return st,slow
v1=[4,8,6,3,2]
st,slow=run(v1)
st[-1]["note"]+=" The loop stops because fast has no successor."
assert slow==2
fill(CH,F,block(v1,["slow","fast"],st),"@@TRACE1@@")
v2=[3,5,2,8,1,6]
st,slow=run(v2)
st[-1]["note"]+=" The loop stops because fast is null. Slow holds the second of the two middle lanterns."
assert slow==3
fill(CH,F,block(v2,["slow","fast"],st),"@@TRACE2@@")
