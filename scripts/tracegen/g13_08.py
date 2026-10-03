from common import *
CH='13-deques-and-monotonic-queues'
F='08-shortest-subarray-deque-state.md'
fmt=lambda l:"["+",".join(map(str,l))+"]"
def run(nums,k):
    P=[0]
    for x in nums: P.append(P[-1]+x)
    d=[];best=None;steps=[]
    for b,v in enumerate(P):
        used=[];dom=[]
        while d and v-P[d[0]]>=k:
            s=d.pop(0);used.append(s)
            L=b-s
            best=L if best is None or L<best else best
        while d and P[d[-1]]>=v: dom.append(d.pop())
        d.append(b)
        p=[f"Cut point {b} has balance {v}."]
        if used: p.append("The front passes the target test and is removed for start"+("s " if len(used)>1 else " ")+", ".join(map(str,used))+", giving the best length "+str(best)+".")
        else: p.append("The front does not reach the target.")
        if dom: p.append("The back removes cut point"+("s " if len(dom)>1 else " ")+", ".join(map(str,dom))+" because "+str(v)+" is not larger.")
        p.append(f"Cut point {b} is appended.")
        steps.append({"at":{"b":b},"vars":{"balances":fmt(P[:b+1]),"deque":fmt(d),"best":best if best is not None else -1},"note":" ".join(p)})
    return P,steps,(best if best is not None else -1)
n1=[3,-2,4,-1,5]
P,s1,b1=run(n1,6); assert b1==3 and s1[5]["vars"]["deque"]=="[4,5]"
fill(CH,F,block(P,["b"],s1),"@@TRACE1@@")
n2=[4,-5,6,-1,7]
P2,s2,b2=run(n2,12); assert b2==3
fill(CH,F,block(P2,["b"],s2),"@@TRACE2@@")
