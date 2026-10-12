from common import *
CH='27-dynamic-programming-capacity-and-partition-patterns'
F='02-unbounded-knapsack.md'
def run(w,v,C):
    dp=[0]*(C+1)
    steps=[{"at":{"c":-1},"vars":{"item":-1,"skip":0,"take":0,"dp":0},"note":"The table starts at 0 for every capacity, because the empty selection is legal."}]
    for i in range(len(w)):
        for c in range(w[i],C+1):
            skip=dp[c]; take=dp[c-w[i]]+v[i]
            dp[c]=max(skip,take)
            why="taking wins" if take>skip else "skipping keeps the entry"
            steps.append({"at":{"c":c},"vars":{"item":i,"skip":skip,"take":take,"dp":dp[c]},
              "note":f"Item {i}, capacity {c}. Skipping holds {skip} and taking reads capacity {c-w[i]} for {take}, so {why} at {dp[c]}."})
    return steps,dp
def brute(w,v,C):
    best=0
    def rec(i,left,val):
        nonlocal best
        if i==len(w): best=max(best,val); return
        k=0
        while k*w[i]<=left: rec(i+1,left-k*w[i],val+k*v[i]); k+=1
    rec(0,C,0); return best
for w,v,C,k in (([4,3],[5,3],6,1),([3,5],[4,7],9,2)):
    s,d=run(w,v,C); assert d[C]==brute(w,v,C)
    fill(CH,F,block(list(range(C+1)),["c"],s),"@@TRACE%d@@"%k)
print("ok")
