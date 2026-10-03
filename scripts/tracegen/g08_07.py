from common import *
CH='08-two-pointers'
F='07-array-cycle-state.md'

def run(nums):
    steps=[]
    slow=fast=0
    r=0
    while True:
        slow=nums[slow]; fast=nums[nums[fast]]; r+=1
        if slow==fast:
            note=f"Round {r}: slow reads index {slow}, fast reads two cells and also lands on index {fast}. They are equal, so phase one ends inside the ring."
        else:
            note=f"Round {r}: slow moves to index {slow} and fast moves two steps to index {fast}. They differ, so another round follows."
        steps.append({"at":{"slow":slow,"fast":fast,"finder":-1},"vars":{"phase":1,"round":r},"note":note})
        if slow==fast: break
    meet=slow
    steps.append({"at":{"slow":slow,"fast":-1,"finder":0},"vars":{"phase":2,"round":0},"note":f"Phase two starts. slow stays on index {meet}, and a new walker called finder starts at index 0. Both will now move one step per round."})
    finder=0; k=0
    while finder!=slow:
        finder=nums[finder]; slow=nums[slow]; k+=1
        if finder==slow:
            note=f"Round {k}: finder and slow both land on index {finder}. That index is the duplicate."
        else:
            note=f"Round {k}: finder moves to index {finder} and slow moves to index {slow}. They differ."
        steps.append({"at":{"slow":slow,"fast":-1,"finder":finder},"vars":{"phase":2,"round":k},"note":note})
    return steps,meet,slow

def dup(nums):
    for v in set(nums):
        if nums.count(v)>1: return v

a=[4,6,2,1,2,5,3]
s,meet,d=run(a); assert d==dup(a)==2 and meet==2 and len(s)>=3
fill(CH,F,block(a,["slow","fast","finder"],s),"@@TRACE1@@")
b=[5,8,3,1,7,2,3,6,4]
s,meet,d=run(b); assert d==dup(b)==3 and meet==4 and len(s)>=3
fill(CH,F,block(b,["slow","fast","finder"],s),"@@TRACE2@@")
