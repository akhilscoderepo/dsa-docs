from common import *
import bisect, itertools, random
CH='28-dynamic-programming-state-machines-and-sequences'
F='03-increasing-subsequences.md'
def brute(a):
    n=len(a); b=0
    for m in range(1<<n):
        s=[a[i] for i in range(n) if m>>i&1]
        if all(s[k]<s[k+1] for k in range(len(s)-1)): b=max(b,len(s))
    return b
def quad(a):
    e=[1]*len(a)
    steps=[{"at":{"i":-1,"j":-1},"vars":{"best":0,"len":0},"note":"Every index starts with length 1, because the element alone is a subsequence."}]
    for i in range(len(a)):
        for j in range(i):
            if a[j]<a[i]:
                old=e[i]; e[i]=max(e[i],e[j]+1)
                note=f"Index {i} holds {a[i]} and index {j} holds {a[j]}. The smaller earlier value extends length {e[j]}, so the length at index {i} is {e[i]}."
                if e[i]==old: note=f"Index {i} holds {a[i]} and index {j} holds {a[j]}. The extension gives {e[j]+1}, which does not beat {old}, so the length stays {old}."
            else:
                note=f"Index {i} holds {a[i]} and index {j} holds {a[j]}. The earlier value is not smaller, so it cannot extend and the length stays {e[i]}."
            steps.append({"at":{"i":i,"j":j},"vars":{"best":e[i],"len":e[j]},"note":note})
        steps.append({"at":{"i":i,"j":i},"vars":{"best":e[i],"len":e[i]},"note":f"Index {i} is finished with length {e[i]}, the longest strictly increasing subsequence that ends at value {a[i]}."})
    return steps,e
def tails(a,right=False):
    t=[]; steps=[{"at":{"i":-1},"vars":{"x":0,"pos":0,"size":0},"note":"The tails list starts empty, so the length is 0."}]
    for i,x in enumerate(a):
        p=bisect.bisect_right(t,x) if right else bisect.bisect_left(t,x)
        if p==len(t):
            t.append(x); what=f"No tail is at least {x}, so it goes at position {p} and the length grows to {len(t)}."
        else:
            old=t[p]; t[p]=x
            what=f"The first tail that is at least {x} is {old} at position {p}, so {x} replaces it and the length stays {len(t)}."
        steps.append({"at":{"i":i},"vars":{"x":x,"pos":p,"size":len(t)},"note":f"Value {x}. {what} Tails are now {t}."})
    return steps,t
a=[5,1,6,2,7,3,8]
s,e=quad(a); assert max(e)==brute(a)==4
fill(CH,F,block(a,["i","j"],s),"@@TRACE1@@")
b=[4,8,4,9,2,3,5,5,6]
s,t=tails(b); assert len(t)==brute(b)
fill(CH,F,block(b,["i"],s),"@@TRACE2@@")
def ends(a):
    e=[1]*len(a)
    for i in range(len(a)):
        for j in range(i):
            if a[j]<a[i]: e[i]=max(e[i],e[j]+1)
    return e
def pre(a):
    t=[];r=[]
    for x in a:
        p=bisect.bisect_left(t,x)
        if p==len(t): t.append(x)
        else: t[p]=x
        r.append(len(t))
    return r
assert ends([3,1,4,1,5,9,2,6])==[1,1,2,1,3,4,2,4] and ends([4,4,4])==[1,1,1]
assert brute([0,8,4,12,2,10,6,14])==4 and brute([7,7,7,7])==1
assert brute([2,2,3,3,1,3])==2 and brute([5,4,3])==1
assert [brute([3,1,2,1,5,4,6][:k]) for k in range(1,8)]==pre([3,1,2,1,5,4,6])==[1,1,2,2,3,3,4]
assert pre([5,4,3,2])==[1,1,1,1]
def nd(a):
    t=[]
    for x in a:
        p=bisect.bisect_right(t,x)
        if p==len(t): t.append(x)
        else: t[p]=x
    return len(t)
assert nd([2,2,3,3,1,3])==5 and nd([5,4,3])==1
# prose claims: contiguous run of the opening example is 2, tails differ from the real subsequence
def run(a):
    b=r=1
    for i in range(1,len(a)):
        r=r+1 if a[i]>a[i-1] else 1; b=max(b,r)
    return b
assert run([5,1,6,2,7,3,8])==2
assert t==[2,3,5,6] and b[-1]==6
print("ok")
