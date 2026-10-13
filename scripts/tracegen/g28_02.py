from common import *
import itertools, functools
CH='28-dynamic-programming-state-machines-and-sequences'
F='02-transaction-variants.md'
def brute_cd(p):
    @functools.lru_cache(None)
    def go(i,holding,cool):
        if i==len(p): return 0
        best=go(i+1,holding,False)
        if holding: best=max(best,p[i]+go(i+1,False,True))
        elif not cool: best=max(best,-p[i]+go(i+1,True,False))
        return best
    return go(0,False,False)
def cooldown(p,bug=False):
    hold,sold,rest=-p[0],0,0
    steps=[{"at":{"i":0},"vars":{"hold":hold,"sold":sold,"rest":rest},
      "note":"Day 0 at price %d. The only possible action is a purchase, so hold is %d, and sold and rest stay at 0."%(p[0],hold)}]
    for i in range(1,len(p)):
        x=p[i]
        if not bug:
            nh=max(hold,rest-x); ns=hold+x; nr=max(rest,sold)
            why="Hold keeps %d or buys from rest for %d. Sold is the old hold plus the price. Rest takes the larger of the old rest %d and the old sold %d, so a sale made today cannot fund a purchase tomorrow."%(hold,rest-x,rest,sold)
            hold,sold,rest=nh,ns,nr
        else:
            ns=hold+x; nr=max(rest,ns); nh=max(hold,nr-x)
            why="Sold is the old hold plus the price, %d. The faulty rest reads that new sold at once and becomes %d, so it carries every sale up to today. Hold buys from that rest, so a purchase can directly follow a sale."%(ns,nr)
            hold,sold,rest=nh,ns,nr
        steps.append({"at":{"i":i},"vars":{"hold":hold,"sold":sold,"rest":rest},
          "note":"Day %d at price %d. %s The values become hold %d, sold %d and rest %d."%(i,x,why,hold,sold,rest)})
    return steps,max(sold,rest)
p1=[2,3,4,1,3]
s,r=cooldown(p1); assert r==brute_cd(tuple(p1))==3
fill(CH,F,block(p1,["i"],s),"@@TRACE1@@")
p2=[2,5,1,4]
s,r=cooldown(p2,True); assert r==6 and brute_cd(tuple(p2))==3
fill(CH,F,block(p2,["i"],s),"@@TRACE2@@")
def plain(p):
    h,c=-p[0],0
    for x in p[1:]: h,c=max(h,c-x),max(c,h+x)
    return c
assert plain(p1)==4
def brute_fee(p,fee):
    @functools.lru_cache(None)
    def go(i,holding):
        if i==len(p): return 0
        b=go(i+1,holding)
        if holding: b=max(b,p[i]-fee+go(i+1,False))
        else: b=max(b,-p[i]+go(i+1,True))
        return b
    return go(0,False)
def brute2(p):
    n=len(p); best=0
    for c in itertools.combinations(range(n),4): best=max(best,p[c[1]]-p[c[0]]+p[c[3]]-p[c[2]])
    for c in itertools.combinations(range(n),2): best=max(best,p[c[1]]-p[c[0]])
    return best
for q in ([6,1,3,2,4,7],[5,4,3]): print('cd',q,brute_cd(tuple(q)))
for q,f in (([3,8,5,10,4,9],2),([4,5,6],5)): print('fee',q,f,brute_fee(tuple(q),f))
for q in ([4,2,6,1,5,3,8],[9,7,5]): print('two',q,brute2(q))
def first_diff(p):
    h,so,r=-p[0],0,0; h2,s2,r2=h,0,0
    for i in range(1,len(p)):
        x=p[i]; h,so,r=max(h,r-x),h+x,max(r,so)
        s2=h2+x; r2=max(r2,s2); h2=max(h2,r2-x)
        if max(so,r)!=max(s2,r2): return i
    return -1
for q in ([2,5,1,4],[3,3,3],[7]): print('alias',q,first_diff(q))
print("ok")
assert brute_cd((6,1,3,2,4,7))==6 and brute_cd((5,4,3))==0
assert brute_fee((3,8,5,10,4,9),2)==9 and brute_fee((4,5,6),5)==0
assert brute2([4,2,6,1,5,3,8])==11 and brute2([9,7,5])==0
assert first_diff([2,5,1,4])==3 and first_diff([3,3,3])==-1 and first_diff([7])==-1
