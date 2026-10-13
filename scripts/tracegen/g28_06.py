from common import *
CH='28-dynamic-programming-state-machines-and-sequences'
F='06-palindromic-sequences.md'
def lps_brute(s):
    n=len(s); b=0
    for m in range(1<<n):
        t=[s[i] for i in range(n) if m>>i&1]
        if t==t[::-1]: b=max(b,len(t))
    return b
def run(s):
    n=len(s); dp=[[0]*n for _ in range(n)]
    steps=[]
    for L in range(1,n+1):
        for l in range(0,n-L+1):
            r=l+L-1
            if L==1:
                dp[l][r]=1; inner=0; skip=0
                note=f"Length 1, interval {l}..{r}. A single character is a palindrome, so the entry is 1."
            elif s[l]==s[r]:
                inner=dp[l+1][r-1] if L>2 else 0; skip=max(dp[l+1][r],dp[l][r-1])
                dp[l][r]=inner+2
                note=f"Length {L}, interval {l}..{r}. The endpoints {s[l]} and {s[r]} match, the inner value is {inner}, so the entry is {inner}+2={dp[l][r]}."
            else:
                inner=dp[l+1][r-1] if L>2 else 0
                a,b=dp[l+1][r],dp[l][r-1]; skip=max(a,b); dp[l][r]=skip
                note=f"Length {L}, interval {l}..{r}. The endpoints {s[l]} and {s[r]} differ. Skipping the left end gives {a}, skipping the right end gives {b}, so the entry is {skip}."
            steps.append({"at":{"left":l,"right":r},"vars":{"length":L,"inner":inner,"skip":skip,"dp":dp[l][r]},"note":note})
    return steps,dp
import sys
for s,ph in (("bbbab","@@TRACE1@@"),("abcda","@@TRACE2@@")):
    st,dp=run(s); assert dp[0][-1]==lps_brute(s)
    fill(CH,F,block(list(s),["left","right"],st),ph)
assert lps_brute("bbbab")==4 and lps_brute("abcda")==3 and lps_brute("cbbd")==2
assert run("bbbab")[1][1][3]==2
# lesson-prose claims
def pos(n,l,r):
    L=r-l+1; return sum(n-k+1 for k in range(1,L))+l
order=[(l,l+L-1) for L in range(1,6) for l in range(0,5-L+1)]
assert order.index((1,2))==pos(5,1,2)==6 and order.index((0,4))==pos(5,0,4)==14
assert 5-lps_brute("mbadm")==2 and 5-lps_brute("zzazz")==0
print("ok")
