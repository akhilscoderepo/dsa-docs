from common import *
CH='26-dynamic-programming-foundations'
F='05-rolling-state.md'
N=7
def run(n,wrong):
    p2,p1=1,2
    cells=[f"dp{i}" for i in range(n+1)]
    steps=[{"at":{"i":1},"vars":{"prev2":p2,"prev1":p1,"cur":p1},"note":"The window starts from the base entries: prev2 holds dp0 = 1 and prev1 holds dp1 = 2."}]
    vals=[1,2]
    for i in range(2,n+1):
        cur=p1+p2
        a,b=p2,p1
        if wrong:
            p1=cur; p2=p1
        else:
            p2=p1; p1=cur
        vals.append(cur)
        if wrong:
            note=f"The sum of {a} and {b} gives cur = {cur}. The wrong shift sets prev1 to {cur} first, so prev2 also becomes {p2}."
        else:
            note=f"The sum of {a} and {b} gives cur = {cur}. The shift moves {b} into prev2 and {cur} into prev1."
        steps.append({"at":{"i":i},"vars":{"prev2":p2,"prev1":p1,"cur":cur},"note":note})
    return cells,steps,p1,vals
cells,steps,res,vals=run(N,False)
fib=[1,2]
for _ in range(N-1): fib.append(fib[-1]+fib[-2])
assert res==fib[N]==34 and vals==fib[:N+1]
fill(CH,F,block(cells,["i"],steps),"@@TRACE1@@")
cells,steps,res,vals=run(N,True)
assert res==96 and vals==[1,2,3,6,12,24,48,96]
fill(CH,F,block(cells,["i"],steps),"@@TRACE2@@")
print("ok")
