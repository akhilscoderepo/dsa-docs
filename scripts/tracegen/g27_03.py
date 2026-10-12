from common import *
CH='27-dynamic-programming-capacity-and-partition-patterns'
F='03-zero-one-knapsack.md'
def run(w,v,C,up=False):
    dp=[0]*(C+1)
    steps=[{"at":{"c":-1},"vars":{"item":-1,"skip":0,"take":0,"dp":0},"note":"The table starts at 0 for every capacity, because the empty selection is legal."}]
    for i in range(len(w)):
        rng=range(w[i],C+1) if up else range(C,w[i]-1,-1)
        for c in rng:
            skip=dp[c]; take=dp[c-w[i]]+v[i]
            dp[c]=max(skip,take)
            why="taking wins" if take>skip else "skipping keeps the entry"
            src="the entry that file %d already rewrote"%i if (up and c-w[i]>=w[i]) else "an entry that still holds the earlier files"
            steps.append({"at":{"c":c},"vars":{"item":i,"skip":skip,"take":take,"dp":dp[c]},
              "note":f"File {i}, capacity {c}. Skipping holds {skip}. Taking reads capacity {c-w[i]} for {take}, from {src}, so {why} at {dp[c]}."})
    return steps,dp
def brute(w,v,C):
    n=len(w); b=0
    for m in range(1<<n):
        if sum(w[i] for i in range(n) if m>>i&1)<=C: b=max(b,sum(v[i] for i in range(n) if m>>i&1))
    return b
w,v,C=[4,3,3],[5,3,3],6
s,d=run(w,v,C); assert d[C]==brute(w,v,C)==6
fill(CH,F,block(list(range(C+1)),["c"],s),"@@TRACE1@@")
s,d=run([3],[4],6,True); assert d[6]==8 and brute([3],[4],6)==4
fill(CH,F,block(list(range(7)),["c"],s),"@@TRACE2@@")
# example checks
assert brute([1,3,4,5],[1,4,5,7],7)==9 and brute([6,7],[3,4],5)==0
def row(w,v,C):
    dp=[0]*(C+1)
    for i in range(len(w)):
        for c in range(C,w[i]-1,-1): dp[c]=max(dp[c],dp[c-w[i]]+v[i])
    return dp
assert row([2,3],[3,4],5)==[0,0,3,4,4,7] and row([4],[9],3)==[0,0,0,0]
def ex(nums):
    t=sum(nums)
    if t%2: return False
    r={0}
    for x in nums: r|={s+x for s in r}
    return t//2 in r
assert ex([3,3,6,2,4]) and not ex([2,2,3,5])
print("ok")
