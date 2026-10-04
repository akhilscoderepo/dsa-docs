from common import *
CH='19-recursion-and-backtracking'; F='03-subsets.md'
# trace 1: increasing-start loop on [1,2,3]
nums=[1,2,3]; path=[]; card=[]; steps=[]
def rec(start):
    card.append(list(path))
    steps.append({"at":{"start":start,"i":-1},"vars":{"path":str(path),"recorded":len(card)},"note":f"The call arrives with start {start} and records a copy of the path {path} as bundle {len(card)}."})
    for i in range(start,len(nums)):
        path.append(nums[i])
        steps.append({"at":{"start":start,"i":i},"vars":{"path":str(path),"recorded":len(card)},"note":f"The loop takes jar {nums[i]}, so the path is {path}, and the next call may only use jars from index {i+1}."})
        rec(i+1)
        path.pop()
        steps.append({"at":{"start":start,"i":i},"vars":{"path":str(path),"recorded":len(card)},"note":f"Jar {nums[i]} is left again, so the path is {path} and the loop moves to the next jar."})
rec(0)
assert card==[[],[1],[1,2],[1,2,3],[1,3],[2],[2,3],[3]]
fill(CH,F,block([str(x) for x in nums],["start","i"],steps),"@@TRACE1@@")
# trace 2: include/leave on [4,7], leave first
nums=[4,7]; path=[]; card=[]; steps=[]
def rec2(idx):
    if idx==len(nums):
        card.append(list(path))
        steps.append({"at":{"index":idx},"vars":{"path":str(path),"recorded":len(card)},"note":f"Both jars are settled, so a copy of the path {path} is recorded as bundle {len(card)}."})
        return
    steps.append({"at":{"index":idx},"vars":{"path":str(path),"recorded":len(card)},"note":f"Jar {nums[idx]} is left out first, so the path stays {path}."})
    rec2(idx+1)
    path.append(nums[idx])
    steps.append({"at":{"index":idx},"vars":{"path":str(path),"recorded":len(card)},"note":f"Jar {nums[idx]} is now taken, so the path is {path}."})
    rec2(idx+1)
    path.pop()
    steps.append({"at":{"index":idx},"vars":{"path":str(path),"recorded":len(card)},"note":f"Both choices for jar {nums[idx]} are done, so it is removed and the path reads {path}."})
rec2(0)
assert card==[[],[7],[4],[4,7]]
fill(CH,F,block([str(x) for x in nums],["index"],steps),"@@TRACE2@@")
