from common import *
CH='26-dynamic-programming-foundations'
F='04-take-or-skip.md'
def run(v, pre):
    n=len(v); best=[0]*(n+1)
    steps=[{"at":{"i":-1},"vars":{"skip":0,"take":0,"best":0},"note":pre}]
    notes=[]
    for i in range(1,n+1):
        skip=best[i-1]; take=v[i-1]+(best[i-2] if i>=2 else 0)
        best[i]=max(skip,take)
        why="taking wins" if take>skip else ("skipping wins" if skip>take else "both cases tie")
        steps.append({"at":{"i":i-1},"vars":{"skip":skip,"take":take,"best":best[i]},
          "note":f"Hour {i-1} has value {v[i-1]}. Skipping keeps {skip}, taking gives {take}, so {why} and best becomes {best[i]}."})
    return steps,best
def brute(v):
    n=len(v); b=0
    for m in range(1<<n):
        if m&(m>>1): continue
        b=max(b,sum(v[i] for i in range(n) if m>>i&1))
    return b
v1=[5,8,5,3,9,4]
s,b=run(v1,"The empty prefix has the best score 0, so nothing is chosen yet.")
assert b[-1]==brute(v1)==19 and b==[0,5,8,10,11,19,19]
fill(CH,F,block(v1,["i"],s),"@@TRACE1@@")
v2=[2,10,3,3,12,2,9]
s,b=run(v2,"The empty prefix has the best score 0, so nothing is chosen yet.")
assert b[-1]==brute(v2)==31, b
print(b)
fill(CH,F,block(v2,["i"],s),"@@TRACE2@@")
print("ok")
