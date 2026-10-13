from common import *
import random
CH='28-dynamic-programming-state-machines-and-sequences'
F='05-edit-distance.md'
def run(s,t):
    m,n=len(s),len(t); W=n+1
    d=[[0]*W for _ in range(m+1)]
    for i in range(m+1): d[i][0]=i
    for j in range(W): d[0][j]=j
    steps=[{"at":{"cell":-1},"vars":{"i":0,"j":0,"diag":0,"up":0,"left":0,"dp":0},"note":"The first row and first column already hold plain lengths, because an empty prefix needs one edit per character."}]
    for i in range(1,m+1):
        for j in range(1,W):
            dg,up,lf=d[i-1][j-1],d[i-1][j],d[i][j-1]
            if s[i-1]==t[j-1]:
                d[i][j]=dg; why="The characters match, so the cell copies the diagonal value "+str(dg)+"."
            else:
                d[i][j]=1+min(dg,up,lf)
                why="The characters differ, so the cell adds one to the smallest read, which is %d."%min(dg,up,lf)
            steps.append({"at":{"cell":i*W+j},"vars":{"i":i,"j":j,"diag":dg,"up":up,"left":lf,"dp":d[i][j]},
              "note":f"Compare {s[i-1]} with {t[j-1]} for prefix lengths {i} and {j}. {why}"})
    return steps,d
def ref(s,t):
    from functools import lru_cache
    @lru_cache(None)
    def f(a,b):
        if not a: return len(b)
        if not b: return len(a)
        if a[0]==b[0]: return f(a[1:],b[1:])
        return 1+min(f(a[1:],b),f(a,b[1:]),f(a[1:],b[1:]))
    return f(s,t)
for s,t,tag in [("spin","pine","@@TRACE1@@"),("act","cat","@@TRACE2@@")]:
    st,d=run(s,t); assert d[-1][-1]==ref(s,t)==2
    fill(CH,F,block(list(range((len(s)+1)*(len(t)+1))),["cell"],st),tag)
random.seed(5)
for _ in range(300):
    a=''.join(random.choice('abc') for _ in range(random.randint(0,6)));b=''.join(random.choice('abc') for _ in range(random.randint(0,6)))
    assert run(a,b)[1][-1][-1]==ref(a,b)
for a,b,e in [("kitten","sitting",3),("monday","mundane",3),("sea","eat",2),("abc","xyz",3),("","abc",3),("abcd","",4)]:
    assert ref(a,b)==e
def ind(a,b):
    m,n=len(a),len(b);d=[[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1):d[i][0]=i
    for j in range(n+1):d[0][j]=j
    for i in range(1,m+1):
        for j in range(1,n+1):
            d[i][j]=d[i-1][j-1] if a[i-1]==b[j-1] else 1+min(d[i-1][j],d[i][j-1])
    return d[m][n]
assert ind("sea","eat")==2 and ind("abc","xyz")==6
print("ok")
