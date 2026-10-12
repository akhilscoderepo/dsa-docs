from common import *
CH='26-dynamic-programming-foundations'
F='03-linear-recurrence.md'
# trace 1: sequence counts up to 8
N=8
ways=[0]*(N+2); ways[0]=ways[1]=1
cells=[f"ways[{i}]" for i in range(N+1)]
steps=[{"at":{"i":0},"vars":{"left":0,"right":0},"note":"The base case ways[0] is 1, because the empty sequence adds up to 0 blocks."},
       {"at":{"i":1},"vars":{"left":0,"right":1},"note":"The base case ways[1] is 1, because only the request of size 1 fits."}]
for i in range(2,N+1):
    ways[i]=ways[i-1]+ways[i-2]
    steps.append({"at":{"i":i},"vars":{"left":ways[i-2],"right":ways[i-1]},"note":f"The entry ways[{i}] is {ways[i-2]} + {ways[i-1]}, which equals {ways[i]}."})
def brute(n):
    return 1 if n<=1 else brute(n-1)+brute(n-2)
assert ways[:N+1]==[1,1,2,3,5,8,13,21,34]==[brute(i) for i in range(N+1)]
fill(CH,F,block(cells,["i"],steps),"@@TRACE1@@")
# trace 2: min cost climbing
cost=[10,15,20,5,10,25,5]; n=len(cost)
dp=[0]*(n+1)
cells=[f"dp[{i}]" for i in range(n+1)]
steps=[{"at":{"i":0},"vars":{"viaOne":0,"viaTwo":0},"note":"Position 0 is a free start, so dp[0] is 0."},
       {"at":{"i":1},"vars":{"viaOne":0,"viaTwo":0},"note":"Position 1 is also a free start, so dp[1] is 0."}]
for i in range(2,n+1):
    a=dp[i-1]+cost[i-1]; b=dp[i-2]+cost[i-2]
    dp[i]=min(a,b)
    steps.append({"at":{"i":i},"vars":{"viaOne":a,"viaTwo":b},"note":f"The two sums are {a} and {b}, so dp[{i}] is {dp[i]}."})
def brute2(i):
    if i<=1: return 0
    return min(brute2(i-1)+cost[i-1],brute2(i-2)+cost[i-2])
assert dp[n]==brute2(n)
print(dp)
fill(CH,F,block(cells,["i"],steps),"@@TRACE2@@")
print("ok",dp[n])
