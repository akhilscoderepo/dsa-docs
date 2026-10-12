from common import *
CH='27-dynamic-programming-capacity-and-partition-patterns'
F='07-permutation-counts.md'
def run(nums,T):
    w=[0]*(T+1); w[0]=1
    steps=[{"at":{"t":0},"vars":{"value":0,"add":0,"ways":1},"note":"The seed is the empty sequence, so the count for total 0 is 1."}]
    for t in range(1,T+1):
        for v in nums:
            if v<=t and w[t-v]:
                add=w[t-v]; w[t]+=add
                steps.append({"at":{"t":t},"vars":{"value":v,"add":add,"ways":w[t]},
                  "note":f"Total {t} with the last element {v} gains {add} from total {t-v}, so its count becomes {w[t]}."})
    return steps,w
def brute(nums,T):
    def rec(left): 
        return 1 if left==0 else sum(rec(left-v) for v in nums if v<=left)
    return rec(T)
for nums,T,k in (([1,2],4,1),([2,3],7,2)):
    s,w=run(nums,T); assert w[T]==brute(nums,T)
    fill(CH,F,block(list(range(T+1)),["t"],s),"@@TRACE%d@@"%k)
print("ok")
