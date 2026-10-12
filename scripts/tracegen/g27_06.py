from common import *
CH='27-dynamic-programming-capacity-and-partition-patterns'
F='06-combination-counts.md'
def run(coins,A,coins_outer):
    w=[0]*(A+1); w[0]=1
    steps=[{"at":{"a":0},"vars":{"coin":0,"add":0,"ways":1},"note":"The seed is the empty combination, so the count for amount 0 is 1."}]
    if coins_outer:
        for c in coins:
            for a in range(c,A+1):
                add=w[a-c]; w[a]+=add
                if add: steps.append({"at":{"a":a},"vars":{"coin":c,"add":add,"ways":w[a]},
                  "note":f"Adding the coin {c}, amount {a} gains {add} from amount {a-c}, so its count becomes {w[a]}."})
    else:
        for a in range(1,A+1):
            for c in coins:
                if c<=a:
                    add=w[a-c]; w[a]+=add
                    if add: steps.append({"at":{"a":a},"vars":{"coin":c,"add":add,"ways":w[a]},
                      "note":f"With the last coin {c}, amount {a} gains {add} from amount {a-c}, so its count becomes {w[a]}."})
    return steps,w
def comb(coins,A): return run(coins,A,True)[1][A]
def seqs(coins,A): return run(coins,A,False)[1][A]
def brute(coins,A):
    n=len(coins)
    def rec(i,left):
        if i==n: return 1 if left==0 else 0
        return sum(rec(i+1,left-k*coins[i]) for k in range(left//coins[i]+1))
    return rec(0,A)
s,w=run([1,2,5],5,True); assert w[5]==brute([1,2,5],5)==4 and w==[1,1,2,2,3,4]
fill(CH,F,block(list(range(6)),["a"],s),"@@TRACE1@@")
s,w=run([1,2,5],5,False); assert w[5]==9 and w[3]==3
fill(CH,F,block(list(range(6)),["a"],s),"@@TRACE2@@")
assert comb([2,3,7],12)==brute([2,3,7],12)==4 and comb([1,2],4)==3 and seqs([1,2],4)==5 and comb([3,4],7)==1 and seqs([3,4],7)==2
print(w, "ok")
