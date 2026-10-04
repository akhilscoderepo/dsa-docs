from common import *
CH='01-arrays-core-operations'; F='03-running-extremum-and-best-gain.md'
def run(nums):
    low=nums[0]; best=0
    st=[{"at":{"i":0},"vars":{"lowestSoFar":low,"bestGain":best},"note":f"Start: lowestSoFar is {low}, bestGain is 0, and the loop begins at index 1."}]
    for i in range(1,len(nums)):
        x=nums[i]; gain=x-low; best=max(best,gain); low=min(low,x)
        st.append({"at":{"i":i},"vars":{"lowestSoFar":low,"bestGain":best},"note":f"i = {i}: selling at {x} against the old minimum gives {gain}. bestGain is {best}, lowestSoFar is {low}."})
    st.append({"at":{"i":len(nums)},"vars":{"lowestSoFar":low,"bestGain":best},"note":f"The loop ends. The answer is {best}."})
    return st,best
a=[9,4,6,3,8,5]; st,b=run(a); assert b==5
fill(CH,F,block(a,["i"],st),"@@TRACE1@@")
a=[8,6,5,2]; st,b=run(a); assert b==0
fill(CH,F,block(a,["i"],st),"@@TRACE2@@")
