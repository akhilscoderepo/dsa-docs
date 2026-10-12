from common import *
CH='26-dynamic-programming-foundations'
F='02-memo-and-table.md'
# trace 1: memoized fib(6), event recorded when a call finishes
n=6
memo=[-1]*(n+1)
events=[]
cnt={'calls':0}
def go(k,depth):
    cnt['calls']+=1
    if k<2:
        events.append((k,depth,'base'))
        return k
    if memo[k]!=-1:
        events.append((k,depth,'hit'))
        return memo[k]
    memo[k]=go(k-1,depth+1)+go(k-2,depth+1)
    events.append((k,depth,'store'))
    return memo[k]
go(n,1)
assert memo[n]==8 and cnt['calls']==11 and len(events)==11
assert sum(1 for e in events if e[2]=='hit')==3 and sum(1 for e in events if e[2]=='base')==3
cells=[str(i) for i in range(n+1)]
steps=[]
filled=set(); fin=0
for k,depth,kind in events:
    fin+=1
    if kind=='hit':
        note=f"The call for {k} finds its answer in the cache and returns at once."
    elif kind=='base':
        note=f"The call for {k} is a base case and returns {k} without touching the cache."
    else:
        filled.add(k); note=f"The call for {k} adds its two smaller answers and stores {memo[k]}."
    steps.append({"at":{"call":k},"vars":{"depth":depth,"filled":len(filled),"calls":fin},"note":note})
assert len(filled)==5
fill(CH,F,block(cells,["call"],steps),"@@TRACE1@@")
# trace 2: tabulation for n = 8
n=8
t=[0]*(n+1); t[1]=1
cells=[str(i) for i in range(n+1)]
steps=[{"at":{"i":1},"vars":{"left":0,"right":0},"note":"Before the loop, the base entries are set: entry 0 is 0 and entry 1 is 1."}]
for i in range(2,n+1):
    l,r=t[i-2],t[i-1]
    t[i]=l+r
    steps.append({"at":{"i":i},"vars":{"left":l,"right":r},"note":f"Entry {i} adds {l} and {r}, and stores {t[i]}."})
assert t==[0,1,1,2,3,5,8,13,21]
fill(CH,F,block(cells,["i"],steps),"@@TRACE2@@")
print("ok")
