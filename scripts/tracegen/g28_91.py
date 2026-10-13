import itertools, random, os, sys
from common import *
CH='28-dynamic-programming-state-machines-and-sequences'
F='91-dp-state-machines.md'
NEG=-10**9

def best_trade(p):
    md=0; bp=0; bs=-1; bb=-1
    for j in range(1,len(p)):
        if p[j]<p[md] and False: pass
        if p[j]-p[md]>bp: bp=p[j]-p[md]; bs=j; bb=md
        if p[j]<p[md]: md=j
    return (bb,bs) if bs>=0 else (-1,-1)
def brute_trade(p):
    best=None
    for s in range(len(p)):
        for b in range(s):
            g=p[s]-p[b]
            if g>0 and (best is None or (g,-s,-b)>best[0]): best=((g,-s,-b),(b,s))
    return best[1] if best else (-1,-1)

def cool(p):
    n=len(p); K=1000
    free=0; hold=NEG*K; rest=NEG*K
    for d,x in enumerate(p):
        nf=max(free,rest); nh=max(hold,free-x*K); nr=hold+x*K-(1 if d<n-1 else 0)
        free,hold,rest=nf,nh,nr
    key=max(free,rest); pr=-((-key)//K); return pr, pr*K-key
def brute_cool(p):
    n=len(p); best=[None]
    def rec(d,holding,blocked,pr,cd):
        if d==n:
            if not holding:
                c=(pr,-cd)
                if best[0] is None or c>best[0]: best[0]=c
            return
        rec(d+1,holding,False,pr,cd)
        if holding: rec(d+1,False,True,pr+p[d],cd+(1 if d<n-1 else 0))
        elif not blocked: rec(d+1,True,False,pr-p[d],cd)
    rec(0,False,False,0,0); return best[0][0],-best[0][1]

def fee_min(p,fee,mn):
    free=0; hold=NEG
    for x in p:
        nh=max(hold,free-x-fee); nf=max(free,hold+x)
        hold,free=nh,nf
    return free if free>=mn else 0
def brute_fee(p,fee,mn):
    n=len(p); best=[0]
    def rec(d,holding,pr):
        if d==n:
            if not holding: best[0]=max(best[0],pr)
            return
        rec(d+1,holding,pr)
        if holding: rec(d+1,False,pr+p[d])
        else: rec(d+1,True,pr-p[d]-fee)
    rec(0,False,0); return best[0] if best[0]>=mn else 0

def ktr(p,k):
    K=1000
    free=[0]+[NEG*K]*k; hold=[NEG*K]*(k+1)
    for x in p:
        nf=free[:]; nh=hold[:]
        for c in range(k+1):
            nf[c]=max(free[c],hold[c]+x*K)
            if c>0: nh[c]=max(hold[c],free[c-1]-x*K-1)
        free,hold=nf,nh
    key=max(free); pr=-((-key)//K); return pr, pr*K-key
def brute_k(p,k):
    n=len(p); best=[None]
    def rec(d,holding,used,pr):
        if d==n:
            if not holding:
                c=(pr,-used)
                if best[0] is None or c>best[0]: best[0]=c
            return
        rec(d+1,holding,used,pr)
        if holding: rec(d+1,False,used,pr+p[d])
        elif used<k: rec(d+1,True,used+1,pr-p[d])
    rec(0,False,0,0); return best[0][0],-best[0][1]

rnd=random.Random(2891)
for _ in range(3000):
    p=[rnd.randint(1,9) for _ in range(rnd.randint(0,9))]
    assert best_trade(p)==brute_trade(p),p
    assert cool(p)==brute_cool(p),p
    fe=rnd.randint(0,4); mn=rnd.randint(0,6)
    assert fee_min(p,fe,mn)==brute_fee(p,fe,mn),p
    k=rnd.randint(0,4)
    assert ktr(p,k)==brute_k(p,k),(p,k)

if __name__=='__main__' and len(sys.argv)>1 and sys.argv[1]=='ex':
    print(best_trade([6,2,8,2,8,1]),best_trade([7,5,4]),best_trade([4,9,4,9]))
    print(cool([1,4,2,5]),cool([3,2,6,5,0,3]),cool([5]),cool([2,9,1,9,1,9]))
    print(fee_min([2,8,4,9],2,5),fee_min([2,8,4,9],2,9),fee_min([1,3],0,0),fee_min([],1,0),fee_min([3,3,3],0,1))
    print(ktr([3,8,1,6,2,9],2),ktr([3,8,1,6,2,9],1),ktr([5,4,3],3),ktr([1,5,2,6],0), ktr([1,5,2,6,1,5],2))
    sys.exit()

def U(x): return -99 if x<=NEG//2 else x
def machine(p,K,cd):
    free=[0]+[NEG]*K; hold=[NEG]*(K+1); rest=[NEG]*(K+1); out=[]
    for d,x in enumerate(p):
        nf=[0]*(K+1); nh=[0]*(K+1); nr=[0]*(K+1)
        for c in range(K+1):
            nf[c]=max(free[c],rest[c])
            if not cd: nf[c]=max(nf[c],hold[c]+x)
            nh[c]=max(hold[c],free[c-1]-x if c>0 else NEG)
            nr[c]=hold[c]+x if cd else NEG
        free,hold,rest=nf,nh,nr; out.append((d,x,free[:],hold[:],rest[:]))
    return out,max(max(free),max(rest))
P1=[3,2,6,5,0,3]
o,ans=machine(P1,3,True); assert ans==7==cool(P1)[0]
st=[]
for d,x,f,h,r in o:
    a,b,c=U(max(f)),U(max(h)),U(max(r))
    st.append({"at":{"d":d},"vars":{"price":x,"free":a,"hold":b,"rest":c},
      "note":f"After day {d} at price {x}, the best cash is {a} when free, {b} when holding and {c} when resting."})
fill(CH,F,block(P1,["d"],st),"@@TRACE1@@")
P2=[3,8,1,6,2,9]
o,ans=machine(P2,2,False); assert ans==13==ktr(P2,2)[0]
st=[]
for d,x,f,h,r in o:
    v=dict(price=x,f1=U(f[1]),f2=U(f[2]),h1=U(h[1]),h2=U(h[2]))
    st.append({"at":{"d":d},"vars":v,
      "note":f"After day {d} at price {x}, free with one purchase holds {v['f1']}, free with two holds {v['f2']}, holding after one holds {v['h1']} and holding after two holds {v['h2']}."})
fill(CH,F,block(P2,["d"],st),"@@TRACE2@@")
print("ok")
