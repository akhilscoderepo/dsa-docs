from common import *
import itertools, random
import os
FILL=os.environ.get("FILL")=="1"
CH='29-dynamic-programming-intervals-and-advanced-states'
F='01-interval-dp.md'
def table(a):
    n=len(a); p=[0]
    for x in a: p.append(p[-1]+x)
    dp=[[0]*n for _ in range(n)]
    steps=[{"at":{"cell":-1},"vars":{"l":0,"r":0,"sum":0,"k":0,"dp":0},"note":"Every interval with one piece starts at 0, because a single piece needs no merge. The cells for these intervals stay 0 throughout."}]
    for ln in range(2,n+1):
        for l in range(0,n-ln+1):
            r=l+ln-1; s=p[r+1]-p[l]
            cands=[(dp[l][k]+dp[k+1][r],k) for k in range(l,r)]
            bv,bk=min(cands)
            dp[l][r]=bv+s
            lst="; ".join("split after %d gives %d"%(k,v) for v,k in cands)
            steps.append({"at":{"cell":l*n+r},"vars":{"l":l,"r":r,"sum":s,"k":bk,"dp":dp[l][r]},"note":"Interval %d to %d has sum %d. The candidates are: %s. The cheapest is the split after %d with %d, so the entry is %d plus %d, which is %d."%(l,r,s,lst,bk,bv,bv,s,dp[l][r])})
    return steps,dp
def brute(a):
    # tries every merge plan by recursion without a table
    if len(a)<2: return 0
    best=10**9
    for k in range(1,len(a)):
        best=min(best,brute(a[:k])+brute(a[k:])+sum(a))
    return best
def greedy(a):
    a=list(a); c=0
    while len(a)>1:
        s=[a[i]+a[i+1] for i in range(len(a)-1)]
        i=s.index(min(s)); c+=s[i]; a[i:i+2]=[s[i]]
    return c
def dpcost(a): 
    n=len(a)
    if n<2: return 0
    return table(a)[1][0][n-1]
A=[9,7,8,8]
s,d=table(A); assert d[0][3]==brute(A)==64 and greedy(A)==70
print(d)
FILL and fill(CH,F,block(list(range(16)),["cell"],s),"@@TRACE1@@")
B=[1,3,4,2,5]
s,d=table(B); assert d[0][4]==brute(B); print(d,brute(B),greedy(B))
FILL and fill(CH,F,block(list(range(25)),["cell"],s),"@@TRACE2@@")
# bottleneck counts
calls=[0]
def count(n):
    calls[0]+=1
    if n==1: return
    for k in range(1,n): count(k); count(n-k)
count(10); assert calls[0]==3**9==19683
from math import comb
assert comb(18,9)//10==4862 and 10*11//2==55
# exercise examples
assert dpcost([7,8,8])==38 and dpcost([4,1,3,5][0:3])==12
for t in range(300):
    x=[random.randint(0,9) for _ in range(random.randint(0,7))]
    assert dpcost(x)==brute(x)
print(dpcost([3,1,2]),dpcost([5,5]),dpcost([0,0,0]))
def chain(p):
    n=len(p)-1
    if n<2: return 0
    import functools
    @functools.lru_cache(None)
    def f(l,r):
        if l==r: return 0
        return min(f(l,k)+f(k+1,r)+p[l]*p[k+1]*p[r+1] for k in range(l,r))
    return f(0,n-1)
print(chain([10,30,5,60]),chain([3,8,2,9,4]),chain([7,2]),chain([6]))
def burst(v):
    import functools
    @functools.lru_cache(None)
    def f(t):
        if not t: return 0
        return max(f(t[:i]+t[i+1:])+(t[i-1] if i else 1)*t[i]*(t[i+1] if i+1<len(t) else 1) for i in range(len(t)))
    return f(tuple(v))
print(burst([3,1,5,8]),burst([2,4,3]),burst([5,1,6,2]),burst([]),burst([9]))
