from common import *
import itertools
CH='27-dynamic-programming-capacity-and-partition-patterns'
F='05-target-sum.md'
def run(nums,target):
    total=sum(nums); goal=(total+target)//2
    ways=[0]*(goal+1); ways[0]=1
    steps=[{"at":{"s":0},"vars":{"x":0,"add":0,"ways":1},"note":"Only the empty subset exists at the start, so the count for sum 0 is 1."}]
    for x in nums:
        for s in range(goal,x-1,-1):
            add=ways[s-x]
            if add:
                ways[s]+=add
                steps.append({"at":{"s":s},"vars":{"x":x,"add":add,"ways":ways[s]},
                  "note":f"Adding the element {x}, sum {s} gains {add} from sum {s-x}, so its count becomes {ways[s]}."})
    return steps,ways,goal
def cnt(nums,t): return sum(1 for sg in itertools.product((1,-1),repeat=len(nums)) if sum(a*b for a,b in zip(sg,nums))==t)
for nums,t,k in (([1,2,3,4],2,1),([0,0,1],1,2)):
    s,w,g=run(nums,t); assert w[g]==cnt(nums,t)
    fill(CH,F,block(list(range(g+1)),["s"],s),"@@TRACE%d@@"%k)
assert cnt([2,3,5,1],1)==2
print("ok")
