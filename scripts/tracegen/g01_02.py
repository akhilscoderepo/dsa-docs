from common import *
CH='01-arrays-core-operations'; F='02-aggregation.md'
nums=[-6,-2,-9,-2,-4]; mx=nums[0]; st=[{"at":{"i":0},"vars":{"max":mx},"note":f"max starts as the first element, {mx}. The loop begins at index 1."}]
for i in range(1,len(nums)):
    x=nums[i]
    if x>mx:
        mx=x; st.append({"at":{"i":i},"vars":{"max":mx},"note":f"i = {i}: {x} is larger than the old max, so max becomes {mx}."})
    else:
        st.append({"at":{"i":i},"vars":{"max":mx},"note":f"i = {i}: {x} is not larger than {mx}, so max stays {mx}."})
st.append({"at":{"i":len(nums)},"vars":{"max":mx},"note":f"The loop ends. max is {mx}."})
assert mx==-2==max(nums)
fill(CH,F,block(nums,["i"],st),"@@TRACE1@@")
bits=[1,1,0,1,1,1]; cur=best=0; st=[]
for i,b in enumerate(bits):
    if b==1:
        cur+=1; note=f"i = {i}: the value is 1, so current grows to {cur}."
    else:
        cur=0; note=f"i = {i}: the value is 0, so current resets to 0 and best keeps its value."
    best=max(best,cur)
    st.append({"at":{"i":i},"vars":{"current":cur,"best":best},"note":note+f" best is {best}."})
st.append({"at":{"i":len(bits)},"vars":{"current":cur,"best":best},"note":f"The array ends inside a run. No zero follows, and best already holds {best}."})
assert best==3
fill(CH,F,block(bits,["i"],st),"@@TRACE2@@")
