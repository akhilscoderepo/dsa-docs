from common import *
CH='19-recursion-and-backtracking'; F='06-reusable-candidates.md'
coins=[2,3]; price=6; path=[]; res=[]; steps=[]
def pay(start,left):
    if left==0:
        res.append(list(path))
        steps.append({"at":{"i":start},"vars":{"path":str(path),"left":0},"note":f"The amount left is zero, so a copy of {path} is recorded as handful {len(res)}."})
        return
    for i in range(start,len(coins)):
        c=coins[i]
        if c>left:
            steps.append({"at":{"i":i},"vars":{"path":str(path) if path else "empty","left":left},"note":f"The coin {c} is larger than the {left} still owed, so it is skipped."})
            continue
        path.append(c)
        steps.append({"at":{"i":i},"vars":{"path":str(path),"left":left-c},"note":f"The coin {c} is paid, so {left-c} is left, and the next call may use positions from {i} onward, which keeps {c} available."})
        pay(i,left-c)
        path.pop()
        steps.append({"at":{"i":i},"vars":{"path":str(path) if path else "empty","left":left},"note":f"The coin {c} is taken back, so the path is {path if path else 'empty'} and {left} is owed again."})
pay(0,price)
assert res==[[2,2,2],[3,3]]
# the final step must not point past the cells; i<=len(cells) is fine
fill(CH,F,block([str(c) for c in coins],["i"],steps),"@@TRACE1@@")
# trace 2: restart at zero, coins [1,2] price 3
coins=[1,2]; price=3; path=[]; seen=set(); steps=[]
def pay2(left):
    if left==0:
        key=tuple(sorted(path)); rep=key in seen; seen.add(key)
        steps.append({"at":{"i":coins.index(path[-1])},"vars":{"path":str(path),"again":"yes" if rep else "no"},"note":f"The amount left is zero, so {path} is complete as the handful {list(key)}, " + ("which was found before, so it is a repeat." if rep else "which is new.")})
        return
    for i,c in enumerate(coins):
        if c>left: continue
        path.append(c)
        steps.append({"at":{"i":i},"vars":{"path":str(path),"again":"no"},"note":f"The coin {c} is paid from the whole list, because the loop restarts at the first coin, so the path is {path}."})
        pay2(left-c)
        path.pop()
        steps.append({"at":{"i":i},"vars":{"path":str(path) if path else "empty","again":"no"},"note":f"The coin {c} is taken back, so the path is {path if path else 'empty'}."})
pay2(price)
assert sum(1 for s in steps if s["vars"]["again"]=="yes")==1 and len(seen)==2
fill(CH,F,block([str(c) for c in coins],["i"],steps),"@@TRACE2@@")
