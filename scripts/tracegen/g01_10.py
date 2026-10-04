from common import *
CH='01-arrays-core-operations'
def kad(arr):
    st=[]; e=b=arr[0]
    st.append({"at":{"i":0},"vars":{"bestEndingHere":e,"bestOverall":b},"note":f"Index 0 holds {arr[0]}. Both variables start at {arr[0]}, because the subarray must be non-empty."})
    for i in range(1,len(arr)):
        x=arr[i]; ext=e+x
        if x>ext: act=f"Starting fresh gives {x}, which beats extending to {ext}."
        elif ext>x: act=f"Extending gives {ext}, which beats starting fresh at {x}."
        else: act=f"Extending and starting both give {x}."
        e=max(x,ext); nb=max(b,e)
        tail=f" bestOverall rises to {nb}." if nb>b else f" bestOverall stays {nb}."
        b=nb
        st.append({"at":{"i":i},"vars":{"bestEndingHere":e,"bestOverall":b},"note":f"Index {i} holds {x}. {act} bestEndingHere is {e}."+tail})
    return st,b
a=[-2,1,-3,4,-1,2,1,-5,4]; s,b=kad(a); assert b==6
fill(CH,'10-kadane-state.md',block(a,["i"],s),"@@TRACE1@@")
a=[-8,-3,-6]; s,b=kad(a); assert b==-3
fill(CH,'10-kadane-state.md',block(a,["i"],s),"@@TRACE2@@")
