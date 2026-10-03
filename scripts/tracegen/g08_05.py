from common import *
from itertools import combinations
CH='08-two-pointers'
F='05-duplicate-skipping.md'
def run(a):
    n=len(a); st=[]; res=[]
    for i in range(n-2):
        if i>0 and a[i]==a[i-1]:
            st.append((i,-1,-1,None,len(res),f"Position {i} holds {a[i]}, the same as position {i-1}, whose hunt already finished. Skip it without scanning."))
            continue
        lo,hi=i+1,n-1
        while lo<hi:
            s=a[i]+a[lo]+a[hi]
            if s<0:
                st.append((i,lo,hi,s,len(res),f"{a[i]} + {a[lo]} + {a[hi]} = {s}, too small, so lo becomes {lo+1}.")); lo+=1
            elif s>0:
                st.append((i,lo,hi,s,len(res),f"{a[i]} + {a[lo]} + {a[hi]} = {s}, too large, so hi becomes {hi-1}.")); hi-=1
            else:
                res.append((a[i],a[lo],a[hi])); gl,gr=a[lo],a[hi]
                lo0,hi0=lo,hi
                while lo<hi and a[lo]==gl: lo+=1
                while lo<hi and a[hi]==gr: hi-=1
                st.append((i,lo0,hi0,s,len(res),f"{a[i]} + {a[lo0]} + {a[hi0]} = 0. Record the trio first, then move past the twins: lo becomes {lo} and hi becomes {hi}."))
    exp=sorted(set(tuple(sorted(c)) for c in combinations(a,3) if sum(c)==0))
    assert res==exp,(res,exp)
    return [{"at":{"i":i,"lo":l,"hi":h},"vars":({"sum":s,"found":f} if s is not None else {"found":f}),"note":n} for i,l,h,s,f,n in st],res
a1=[-1,-1,0,1,2,2]; s,r=run(a1); assert r==[(-1,-1,2),(-1,0,1)]; print(len(s))
fill(CH,F,block(a1,["i","lo","hi"],s),"@@TRACE1@@")
a2=[-2,-2,0,0,0,2,2,2]; s,r=run(a2); assert r==[(-2,0,2),(0,0,0)]; print(len(s))
fill(CH,F,block(a2,["i","lo","hi"],s),"@@TRACE2@@")
