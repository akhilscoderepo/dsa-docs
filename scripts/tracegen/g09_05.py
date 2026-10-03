from common import *
CH='09-sliding-window'
F='05-at-most-k-distinct-windows.md'

def run(a,k):
    tally={}; left=0; best=0; steps=[]
    for r,v in enumerate(a):
        tally[v]=tally.get(v,0)+1
        note=f"Position {r} holds {v}, so its count becomes {tally[v]}."
        gone=[]
        while len(tally)>k:
            x=a[left]; tally[x]-=1
            if tally[x]==0: del tally[x]
            gone.append(x); left+=1
        if gone:
            note+=f" The tally would be over the limit of {k}, so the left edge drops {len(gone)} position{'s' if len(gone)>1 else ''} ({', '.join(map(str,gone))}) until a key disappears, and left becomes {left}."
        else:
            note+=f" The tally holds {len(tally)} value{'s' if len(tally)!=1 else ''}, within the limit of {k}."
        best=max(best,r-left+1)
        note+=f" Window length {r-left+1}, best so far {best}."
        shown=" ".join(f"{key}x{c}" for key,c in tally.items())
        steps.append({"at":{"left":left,"right":r},"vars":{"tally":shown,"best":best},"note":note})
    return steps,best

def brute(a,k):
    b=0
    for s in range(len(a)):
        for e in range(s,len(a)):
            if len(set(a[s:e+1]))<=k: b=max(b,e-s+1)
    return b

a1=[1,2,1,3,3,2,1]
s,b=run(a1,2); assert b==brute(a1,2)==3 and s[3]["at"]["left"]==2 and "drops 2 positions (1, 2)" in s[3]["note"]
fill(CH,F,block(a1,["left","right"],s),"@@TRACE1@@")
a2=list("xyxzzwxy")
s,b=run(a2,3); assert b==brute(a2,3)==5 and s[5]["at"]["left"]==2 and s[7]["at"]["left"]==5
fill(CH,F,block(a2,["left","right"],s),"@@TRACE2@@")
