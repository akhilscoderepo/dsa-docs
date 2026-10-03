from common import *
CH='09-sliding-window'
F='06-exactly-k-by-subtraction.md'

def at_most(a,k):
    odd=0; left=0; tot=0; steps=[]
    for r,v in enumerate(a):
        odd+=v&1
        shrunk=0
        while odd>k:
            odd-=a[left]&1; left+=1; shrunk+=1
        add=r-left+1; tot+=add
        kind="odd" if v&1 else "even"
        note=f"Position {r} holds {v}, which is {kind}, so the window holds {odd} odd value{'s' if odd!=1 else ''} after trimming"
        note+=f" (the left edge moved {shrunk} step{'s' if shrunk!=1 else ''}, to {left}). " if shrunk else ". "
        note+=f"Every start from {left} to {r} gives a valid subarray ending here, which is {add}, so the running total is {tot}."
        steps.append({"at":{"left":left,"right":r},"vars":{"odd":odd,"added":add,"total":tot},"note":note})
    return steps,tot

def exact_brute(a,k):
    return sum(1 for s in range(len(a)) for e in range(s,len(a)) if sum(x&1 for x in a[s:e+1])==k)

a1=[2,1,4,3,2,5]
s,t=at_most(a1,2); assert t==19 and s[5]["at"]["left"]==2
assert t-at_most(a1,1)[1]==exact_brute(a1,2)
fill(CH,F,block(a1,["left","right"],s),"@@TRACE1@@")
a2=[1,2,1,2,2,1]
s,t=at_most(a2,0); t1=at_most(a2,1)[1]
assert t==4 and t1==15 and t1-t==exact_brute(a2,1)==11 and s[2]["at"]["left"]==3
s[-1]["note"]+=f" With atMost(1) equal to {t1} and atMost(0) equal to {t}, the exactly-one count is {t1-t}."
fill(CH,F,block(a2,["left","right"],s),"@@TRACE2@@")
