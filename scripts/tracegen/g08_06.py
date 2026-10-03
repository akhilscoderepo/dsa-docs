from common import *
from itertools import combinations
CH='08-two-pointers'
F='06-k-sum-reduction.md'
def exact(a,target):
    n=len(a); st=[]; found=False
    for i in range(n-2):
        rem=target-a[i]; lo,hi=i+1,n-1
        while lo<hi:
            p=a[lo]+a[hi]
            if p==rem:
                st.append((i,lo,hi,rem,p,f"Pick {a[i]}, remaining target {rem}. Pair {a[lo]} + {a[hi]} = {p}, which equals it, so three weights reach {target}.")); found=True; break
            if p<rem:
                st.append((i,lo,hi,rem,p,f"Pick {a[i]}, remaining target {rem}. Pair {a[lo]} + {a[hi]} = {p}, too light, so lo becomes {lo+1}.")); lo+=1
            else:
                st.append((i,lo,hi,rem,p,f"Pick {a[i]}, remaining target {rem}. Pair {a[lo]} + {a[hi]} = {p}, too heavy, so hi becomes {hi-1}.")); hi-=1
        if found: break
    assert found==any(sum(c)==target for c in combinations(a,3))
    return [{"at":{"i":i,"lo":l,"hi":h},"vars":{"remaining":r,"pair":p},"note":nt} for i,l,h,r,p,nt in st]
a1=[2,5,7,8,11,14,20]
s=exact(a1,26); print(len(s))
assert s[-1]["at"]=={"i":1,"lo":2,"hi":5} and sum(1 for x in s if x["at"]["i"]==0)==5
fill(CH,F,block(a1,["i","lo","hi"],s),"@@TRACE1@@")
def near(a,target):
    n=len(a); best=a[0]+a[1]+a[2]; st=[]
    for i in range(n-2):
        lo,hi=i+1,n-1
        while lo<hi:
            t=a[i]+a[lo]+a[hi]; old=best
            if abs(t-target)<abs(best-target): best=t
            if best!=old: act=f"New best {best}, replacing {old}."
            else: act=f"Best stays {best}."
            if t==target: st.append((i,lo,hi,t,best,f"Total {t} equals the target. Stop.")); return st,best
            if t<target: st.append((i,lo,hi,t,best,f"{a[i]} + {a[lo]} + {a[hi]} = {t}, below the target {target}. {act} lo becomes {lo+1}.")); lo+=1
            else: st.append((i,lo,hi,t,best,f"{a[i]} + {a[lo]} + {a[hi]} = {t}, above the target {target}. {act} hi becomes {hi-1}.")); hi-=1
    return st,best
a2=[-9,-4,0,3,8,12]
st,best=near(a2,1)
alls=[sum(c) for c in combinations(a2,3)]
assert abs(best-1)==min(abs(x-1) for x in alls); print(len(st),best)
for x in st: print(x)
s=[{"at":{"i":i,"lo":l,"hi":h},"vars":{"total":t,"best":b},"note":nt} for i,l,h,t,b,nt in st]
fill(CH,F,block(a2,["i","lo","hi"],s),"@@TRACE2@@")
