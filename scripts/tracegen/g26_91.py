from common import *
CH='26-dynamic-programming-foundations'
F='91-recursion-and-memoization.md'
# trace 1: house values with a hit counter
nums=[4,1,2,9,3]; n=len(nums)
memo=[None]*n; hits=0; steps=[]
M=lambda: " ".join("." if v is None else str(v) for v in memo)
steps.append({"at":{"i":-1},"vars":{"memo":M(),"hits":0},"note":"No call has finished. All five slots are empty."})
def best(i):
    global hits
    if i>=n: return 0
    if memo[i] is not None:
        hits+=1
        steps.append({"at":{"i":i},"vars":{"memo":M(),"hits":hits},"note":f"best({i}) finds the stored value {memo[i]} and returns without recursing. This is hit {hits}."})
        return memo[i]
    a=best(i+1); b=nums[i]+best(i+2)
    memo[i]=max(a,b)
    steps.append({"at":{"i":i},"vars":{"memo":M(),"hits":hits},"note":f"best({i}) skips for {a} or takes for {b}, and it stores {memo[i]}."})
    return memo[i]
assert best(0)==13 and hits==3 and sum(1 for s in steps if 'stores' in s['note'])==5
fill(CH,F,block(nums,["i"],steps),"@@TRACE1@@")
# trace 2: routes on a 3 by 3 board
R=C=3
cells=[f"{r},{c}" for r in range(R) for c in range(C)]
memo2=[None]*9; hits=0; calls=0
M2=lambda: " ".join("." if v is None else str(v) for v in memo2)
steps=[{"at":{"tile":-1},"vars":{"memo":M2(),"hits":0},"note":"No call has finished. All nine slots are empty."}]
def routes(r,c):
    global hits,calls
    calls+=1; k=r*C+c
    if memo2[k] is not None:
        hits+=1
        steps.append({"at":{"tile":k},"vars":{"memo":M2(),"hits":hits},"note":f"Tile {r},{c} is already stored as {memo2[k]}, so the call returns it. This is the hit."})
        return memo2[k]
    if r==R-1 or c==C-1: res=1; why="It lies in the last row or column, so it has one route."
    else:
        res=routes(r+1,c)+routes(r,c+1); why=f"It adds the counts of tiles {r+1},{c} and {r},{c+1}."
    memo2[k]=res
    steps.append({"at":{"tile":k},"vars":{"memo":M2(),"hits":hits},"note":f"Tile {r},{c} stores {res}. {why}"})
    return res
assert routes(0,0)==6 and hits==1 and calls==9 and sum(v is not None for v in memo2)==8 and memo2[8] is None
fill(CH,F,block(cells,["tile"],steps),"@@TRACE2@@")
