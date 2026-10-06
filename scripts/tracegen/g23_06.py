from common import *
CH='23-directed-graphs-and-union-find'; N='06-dynamic-connectivity.md'
class DS:
    def __init__(s,n): s.p=list(range(n)); s.sz=[1]*n; s.c=n
    def find(s,x):
        while s.p[x]!=x:
            s.p[x]=s.p[s.p[x]]; x=s.p[x]
        return x
    def union(s,a,b):
        x,y=s.find(a),s.find(b)
        if x==y: return x,y,False
        if s.sz[x]<s.sz[y]: x,y=y,x
        s.p[y]=x; s.sz[x]+=s.sz[y]; s.c-=1
        return x,y,True
    def ps(s): return " ".join(map(str,s.p))
# trace 1
n=6; ds=DS(6); st=[]; answers=[]
for t,a,b in [(0,0,1),(0,2,3),(1,0,3),(0,1,2),(1,0,3),(0,3,0),(1,4,5)]:
    if t==0:
        x,y,m=ds.union(a,b)
        note=(f"The link {a},{b} finds the representatives {x} and {y}, which differ, so it merges the two groups and the count drops to {ds.c}." if m
              else f"The link {a},{b} finds the same representative {x} twice, so the groups and the count stay as they are.")
        ans=""
    else:
        x,y=ds.find(a),ds.find(b); ans=str(x==y).lower()
        answers.append(x==y)
        note=f"The question {a},{b} finds the representatives {x} and {y}, so the answer is {ans}."
    st.append({"at":{"ra":x,"rb":y},"vars":{"event":("link " if t==0 else "ask ")+f"{a},{b}","parent":ds.ps(),"components":ds.c,"answer":ans or "none"},"note":note})
assert answers==[False,True,False] and ds.c==3
fill(CH,N,block(list(range(n)),["ra","rb"],st),"@@TRACE1@@")
# trace 2
accts=[["a","b"],["c","d"],["b","e"],["f"],["d","g"]]
ds=DS(5); owner={}; st=[]
for i,ems in enumerate(accts):
    other=-1; shared=[]
    for e in ems:
        if e in owner:
            x,y,m=ds.union(i,owner[e]); shared.append(e); other=owner[e]
        else: owner[e]=i
    if shared:
        note=f"Account {i} lists the email {shared[0]}, which account {other} listed first, so the two accounts merge."
    else:
        note=f"Account {i} lists only new emails, so it stores itself as the owner of each and merges with nothing."
    st.append({"at":{"acct":i,"other":other},"vars":{"emails":" ".join(ems),"parent":ds.ps(),"components":ds.c},"note":note})
groups={}
for i in range(5): groups.setdefault(ds.find(i),[]).append(i)
assert sorted(groups.values())==[[0,2],[1,4],[3]],groups
st.append({"at":{"acct":-1,"other":-1},"vars":{"emails":"none","parent":ds.ps(),"components":ds.c},"note":"The final pass groups the accounts by representative and finds the groups 0 and 2, 1 and 4, and 3 alone."})
fill(CH,N,block(list(range(5)),["acct","other"],st),"@@TRACE2@@")
