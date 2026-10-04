from common import *
CH='19-recursion-and-backtracking'; F='01-call-state.md'
# trace 1: power(2,10) by halving
def pw(rate, e, depth, log):
    if e == 0:
        log.append((depth, 'base', e, 1)); return 1
    log.append((depth, 'down', e, None))
    half = pw(rate, e//2, depth+1, log)
    r = half*half*(rate if e % 2 else 1)
    log.append((depth, 'up', e, r)); return r
log=[]; assert pw(2,10,0,log)==1024==2**10
exps=[10,5,2,1,0]; steps=[]
for d,kind,e,r in log:
    if kind=='down': note=f"The call for exponent {e} is not a base case, so it asks the same question for exponent {e//2} and waits."
    elif kind=='base': note="The exponent is zero, which is the base case, so the call answers 1 without asking anything."
    else: note=f"The half result is back, so the call for exponent {e} squares it" + (" and multiplies by the rate once more" if e%2 else "") + f", answering {r}."
    steps.append({"at":{"depth":d},"vars":{"exponent":e,"answer":"waiting" if kind=='down' else r},"note":note})
fill(CH,F,block([str(x) for x in exps],["depth"],steps),"@@TRACE1@@")
# trace 2: prefix total of [3,1,4,1] k=4
a=[3,1,4,1]; steps=[]
def tot(k):
    if k==0:
        steps.append({"at":{"k":0},"vars":{"returned":0},"note":"The count is zero, which is the base case, so the call returns 0 without reading the array."}); return 0
    steps.append({"at":{"k":k},"vars":{"returned":"waiting"},"note":f"The call for k = {k} must add a[{k-1}] = {a[k-1]} to the total of the first {k-1} figures, so it asks for that total."})
    r=tot(k-1)+a[k-1]
    steps.append({"at":{"k":k},"vars":{"returned":r},"note":f"The smaller total is back, so the call for k = {k} returns {r - a[k-1]} + {a[k-1]} = {r}."}); return r
assert tot(4)==9
fill(CH,F,block([str(x) for x in a],["k"],steps),"@@TRACE2@@")
