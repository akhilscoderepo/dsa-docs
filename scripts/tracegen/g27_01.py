from common import *
CH='27-dynamic-programming-capacity-and-partition-patterns'
F='01-unbounded-coin-change.md'
def run(coins, amount, pre):
    M=amount+1; dp=[M]*(amount+1); dp[0]=0; ch=[0]*(amount+1)
    steps=[{"at":{"a":-1},"vars":{"dp":0,"coin":0},"note":pre}]
    for a in range(1,amount+1):
        for c in coins:
            if c<=a and dp[a-c]+1<dp[a]: dp[a]=dp[a-c]+1; ch[a]=c
        if dp[a]==M:
            note=f"Amount {a} has no denomination that leaves a reachable amount, so the entry keeps the marker {M}."
        else:
            note=f"Amount {a} takes the last coin {ch[a]}, which leaves amount {a-ch[a]} with {dp[a-ch[a]]} tokens, so the entry becomes {dp[a]}."
        steps.append({"at":{"a":a},"vars":{"dp":dp[a],"coin":ch[a]},"note":note})
    return steps,dp
def brute(coins,amount):
    best=[None]*(amount+1); best[0]=0
    for a in range(1,amount+1):
        for c in coins:
            if c<=a and best[a-c] is not None and (best[a] is None or best[a-c]+1<best[a]): best[a]=best[a-c]+1
    return best[amount]
s,d=run([1,3,4],6,"The base entry for amount 0 is 0, because paying nothing needs no tokens.")
assert d[6]==2==brute([1,3,4],6)
fill(CH,F,block(list(range(7)),["a"],s),"@@TRACE1@@")
s,d=run([5,7],14,"The base entry for amount 0 is 0, and the marker 15 stands for unreachable amounts.")
assert d[14]==2==brute([5,7],14) and [i for i in range(15) if d[i]==15]==[1,2,3,4,6,8,9,11,13]
fill(CH,F,block(list(range(15)),["a"],s),"@@TRACE2@@")
print("ok")
