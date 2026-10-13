from common import *
CH='28-dynamic-programming-state-machines-and-sequences'
F='01-stock-states.md'
NEG=-(2**31)//2
def run(prices,one):
    hold,cash=NEG,0
    steps=[{"at":{"i":-1},"vars":{"hold":hold,"cash":cash},"note":"Before day 0, cash is 0 because doing nothing is legal, and hold is impossible."}]
    for i,p in enumerate(prices):
        bv=-p if one else cash-p
        nh=max(hold,bv); nc=max(cash,hold+p)
        hn=("Buying gives %d, so hold becomes %d"%(bv,nh)) if nh!=hold else ("Buying gives %d, which does not beat %d, so hold stays"%(bv,hold) if hold>NEG else "hold stays impossible")
        cn=("Selling gives %d, so cash becomes %d"%(hold+p,nc)) if nc!=cash else "Selling does not improve cash, which stays %d"%cash
        if hold==NEG and nc==cash: cn="No share exists to sell, so cash stays %d"%cash
        hold,cash=nh,nc
        steps.append({"at":{"i":i},"vars":{"hold":hold,"cash":cash},"note":"Day %d, price %d. %s. %s."%(i,p,hn,cn)})
    return steps,cash
def brute(prices,one):
    n=len(prices); best=0
    def go(d,own,prof,tr):
        nonlocal best
        if d==n:
            if not own: best=max(best,prof)
            return
        go(d+1,own,prof,tr)
        if own: go(d+1,False,prof+prices[d],tr)
        elif not one or tr==0: go(d+1,True,prof-prices[d],tr+1)
    go(0,False,0,0); return best
a=[3,1,4,1,5]; s,c=run(a,False); assert c==brute(a,False)==7
fill(CH,F,block(a,["i"],s),"@@TRACE1@@")
b=[7,1,5,3,6,4]; s,c=run(b,True); assert c==brute(b,True)==5
fill(CH,F,block(b,["i"],s),"@@TRACE2@@")
# opening and example checks
assert brute([6,9,1,3],False)==5 and brute([6,9,1,3],True)==3
calls=[0]
def ex(prices,d,own):
    calls[0]+=1
    if d==len(prices): return -10**6 if own else 0
    r=ex(prices,d+1,own)
    return max(r,prices[d]+ex(prices,d+1,False)) if own else max(r,-prices[d]+ex(prices,d+1,True))
assert ex([1,2,3],0,False)==2 and calls[0]==15
def best_days(pr):
    return [max([0]+[pr[j]-pr[k] for j in range(i+1) for k in range(j)]) for i in range(len(pr))]
assert best_days([7,1,5,3,6,4])==[0,0,4,4,5,5] and best_days([5,4,3])==[0,0,0]
import itertools
def seqs(pr):
    out=[];n=len(pr)
    for acts in itertools.product("BSR",repeat=n):
        own=False;prof=0;ok=True;tr=0
        for a,p in zip(acts,pr):
            if a=="B":
                if own: ok=False;break
                own=True;prof-=p;tr+=1
            elif a=="S":
                if not own: ok=False;break
                own=False;prof+=p
        if ok and not own: out.append((prof,tr))
    return out
def ways(pr):
    o=seqs(pr);m=max(x[0] for x in o);return [m,sum(1 for x in o if x[0]==m)]
def mt(pr):
    o=seqs(pr);m=max(x[0] for x in o);return [m,min(x[1] for x in o if x[0]==m)]
assert mt([3,1,4,1,5])==[7,2] and mt([2,2,2])==[0,0]
assert ways([1,2,3])==[2,1] and ways([2,2,2])==[0,4]
def one_or_neg(pr):
    b=max(0,max([pr[j]-pr[i] for i in range(len(pr)) for j in range(i+1,len(pr))],default=0)); return b if b>0 else -1
assert one_or_neg([9])==-1 and one_or_neg([4,4,2,1,4])==3
print("ok")
