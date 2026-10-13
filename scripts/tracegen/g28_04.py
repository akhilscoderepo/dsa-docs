from common import *
CH='28-dynamic-programming-state-machines-and-sequences'
F='04-common-subsequences.md'
def run(a,b):
    m,n=len(a),len(b)
    dp=[[0]*(n+1) for _ in range(m+1)]
    steps=[{"at":{"cell":-1},"vars":{"i":0,"j":0,"diag":0,"up":0,"left":0,"dp":0},
            "note":"Row 0 and column 0 start at 0, because an empty prefix shares nothing with any other text."}]
    for i in range(1,m+1):
        for j in range(1,n+1):
            diag,up,left=dp[i-1][j-1],dp[i-1][j],dp[i][j-1]
            if a[i-1]==b[j-1]:
                dp[i][j]=diag+1
                note=f"Prefix lengths {i} and {j} end in '{a[i-1]}' on both sides. The characters are equal, so the entry is the diagonal value {diag} plus 1, which is {dp[i][j]}."
            else:
                dp[i][j]=max(up,left)
                note=f"Prefix lengths {i} and {j} end in '{a[i-1]}' and '{b[j-1]}'. The characters differ, so the entry is the larger of up {up} and left {left}, which is {dp[i][j]}."
            steps.append({"at":{"cell":i*(n+1)+j},"vars":{"i":i,"j":j,"diag":diag,"up":up,"left":left,"dp":dp[i][j]},"note":note})
    return steps,dp
def brute(a,b):
    best=0
    for mask in range(1<<len(a)):
        s=[a[i] for i in range(len(a)) if mask>>i&1]
        k=0
        for ch in b:
            if k<len(s) and s[k]==ch: k+=1
        if k==len(s): best=max(best,len(s))
    return best
def greedy(a,b):
    p=0;c=0
    for ch in a:
        q=b.find(ch,p)
        if q>=0: c+=1;p=q+1
    return c
for a,b in [("bacd","acdb"),("cab","abc")]:
    s,d=run(a,b); assert d[-1][-1]==brute(a,b)
    fill(CH,F,block(list(range((len(a)+1)*(len(b)+1))),["cell"],s),"@@TRACE1@@" if a=="bacd" else "@@TRACE2@@")
assert greedy("bacd","acdb")==1 and brute("bacd","acdb")==3
assert run("bacd","acdb")[1][3][4]==2 and run("bacd","acdb")[1][1][2]==0
assert brute("abcd","xaybzc")==3 and brute("programming","gaming")==6
def zeros(a,b): return sum(x==0 for r in run(a,b)[1] for x in r)
assert zeros("","abc")==4 and zeros("ab","ba")==6
def dele(a,b): return len(a)+len(b)-2*brute(a,b)
assert dele("bacd","acdb")==2 and dele("kitten","sitting")==5
print("ok")
