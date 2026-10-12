from common import *
CH='26-dynamic-programming-foundations'
F='01-state-definition.md'
def brute(n,sizes=(2,3)):
    if n==0: return 1
    return sum(brute(n-s,sizes) for s in sizes if n-s>=0)
# trace 1: dp over chunk sizes 2 and 3, n = 10
n=10
dp=[0]*(n+1); dp[0]=1
cells=[str(i) for i in range(n+1)]
steps=[{"at":{"i":0},"vars":{"fromTwo":0,"fromThree":0},"note":"Index 0 is the base entry. The empty sequence adds up to 0 bytes, so dp[0] is 1."}]
for i in range(1,n+1):
    a=dp[i-2] if i>=2 else 0
    b=dp[i-3] if i>=3 else 0
    dp[i]=a+b
    if i==1:
        note="Index 1 has no valid last chunk, since both sizes are larger than 1, so dp[1] stays 0."
    else:
        note=f"Index {i} adds {a} from dp[{i-2}]"+(f" and {b} from dp[{i-3}]" if i>=3 else " and has no index for a 3-chunk")+f", so dp[{i}] is {dp[i]}."
    steps.append({"at":{"i":i},"vars":{"fromTwo":a,"fromThree":b},"note":note})
assert dp[n]==brute(n)==7 and dp[5]==2
assert dp==[1,0,1,1,1,2,2,3,4,5,7]
fill(CH,F,block(cells,["i"],steps),"@@TRACE1@@")
# trace 2: at most one 3-chunk, n = 7
n=7
zero=[0]*(n+1); one=[0]*(n+1); zero[0]=1
cells=[str(i) for i in range(n+1)]
steps=[{"at":{"i":0},"vars":{"zero":1,"one":0},"note":"Index 0 holds the empty sequence, which has no 3-chunk, so zero is 1 and one is 0."}]
for i in range(1,n+1):
    zero[i]=zero[i-2] if i>=2 else 0
    one[i]=(one[i-2] if i>=2 else 0)+(zero[i-3] if i>=3 else 0)
    steps.append({"at":{"i":i},"vars":{"zero":zero[i],"one":one[i]},"note":f"Index {i} gives zero = {zero[i]} and one = {one[i]}, so the total for {i} bytes is {zero[i]+one[i]}."})
def brute2(n):
    def go(r,t):
        if r==0: return 1
        x=0
        if r>=2: x+=go(r-2,t)
        if r>=3 and t<1: x+=go(r-3,t+1)
        return x
    return go(n,0)
assert zero[n]+one[n]==brute2(n)==3 and one[n]==3 and zero[n]==0
fill(CH,F,block(cells,["i"],steps),"@@TRACE2@@")
print("ok")
