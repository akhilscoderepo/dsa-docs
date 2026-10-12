from common import *
CH='27-dynamic-programming-capacity-and-partition-patterns'
F='04-partition-state.md'
def run(nums):
    total=sum(nums); assert total%2==0; T=total//2
    reach=[False]*(T+1); reach[0]=True
    steps=[{"at":{"s":0},"vars":{"x":0,"count":1,"reach":1},"note":"Only sum 0 is reachable at the start, because the empty subset sums to 0."}]
    cnt=1
    for x in nums:
        for s in range(T,x-1,-1):
            if reach[s-x] and not reach[s]:
                reach[s]=True; cnt+=1
                steps.append({"at":{"s":s},"vars":{"x":x,"count":cnt,"reach":1},
                  "note":f"Adding the element {x}, sum {s} becomes reachable because sum {s-x} was reachable before it, so the count of reachable sums is {cnt}."})
    steps.append({"at":{"s":T},"vars":{"x":0,"count":cnt,"reach":int(reach[T])},
      "note":"The target is "+str(T)+" and the final flag is "+("true, so an equal split exists." if reach[T] else "false, so no subset reaches the target and no equal split exists.")})
    return steps,reach,T
def brute(nums,T):
    return any(sum(nums[i] for i in range(len(nums)) if m>>i&1)==T for m in range(1<<len(nums)))
for nums,k in (([3,3,2,2,2],1),([7,3,3,9],2)):
    s,r,T=run(nums); assert r[T]==brute(nums,T)
    if k==1: assert [i for i in range(T+1) if r[i]]==[0,2,3,4,5,6]
    else: assert [i for i in range(T+1) if r[i]]==[0,3,6,7,9,10]
    fill(CH,F,block(list(range(T+1)),["s"],s),"@@TRACE%d@@"%k)
# example checks
def mn(nums):
    tot=sum(nums)
    if tot%2: return -1
    h=tot//2; best=None
    for m in range(1<<len(nums)):
        if sum(nums[i] for i in range(len(nums)) if m>>i&1)==h:
            c=bin(m).count('1'); best=c if best is None else min(best,c)
    return -1 if best is None else best
assert mn([4,6,5,3,2])==2 and mn([3,5,9,2])==-1
def sums(nums): 
    r={0}
    for x in nums: r|={a+x for a in r}
    return len(r)
assert sums([1,2,2])==6 and sums([5,5])==3 and sums([])==1
def stone(st):
    seen={}
    def f(t):
        t=tuple(sorted(t))
        if t in seen: return seen[t]
        if len(t)<=1: r=t[0] if t else 0
        else:
            r=10**9
            for i in range(len(t)):
                for j in range(i+1,len(t)):
                    rest=list(t[:i]+t[i+1:j]+t[j+1:])
                    d=t[j]-t[i]
                    if d: rest.append(d)
                    r=min(r,f(rest))
        seen[t]=r; return r
    return f(st)
assert stone([10,4,3,1])==2 and stone([6,11,4,9])==0
print("ok")
