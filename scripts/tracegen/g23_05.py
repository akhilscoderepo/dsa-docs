from common import *
CH='23-directed-graphs-and-union-find'
F='05-union-by-size.md'
def root(p,x):
    while p[x]!=x: x=p[x]
    return x
def depth(p,x):
    d=0
    while p[x]!=x: x=p[x]; d+=1
    return d
# trace 1
n=9
reqs=[(0,1),(2,3),(1,3),(4,5),(6,4),(3,5),(2,0),(7,8)]
p=list(range(n)); s=[1]*n; comps=n; steps=[]
for i,(a,b) in enumerate(reqs):
    ra,rb=root(p,a),root(p,b)
    if ra==rb:
        steps.append({"at":{"i":i},"vars":{"ra":ra,"rb":rb,"keeper":ra,"rootSize":s[ra],"clubs":comps},
          "note":f"Students {a} and {b} both lead to holder {ra}, so they already share a club and nothing is written."})
        continue
    big=ra if s[ra]>=s[rb] else rb
    small=rb if big==ra else ra
    p[small]=big; s[big]+=s[small]; comps-=1
    steps.append({"at":{"i":i},"vars":{"ra":ra,"rb":rb,"keeper":big,"rootSize":s[big],"clubs":comps},
      "note":f"Holders {ra} and {rb} are found first. Holder {small} gives up its banner and answers to {big}, whose size becomes {s[big]}."})
assert comps==2 and s[root(p,0)]==7 and s[root(p,7)]==2
assert steps[4]["vars"]["keeper"]==4 and steps[4]["vars"]["rootSize"]==3
assert steps[5]["vars"]["keeper"]==0 and steps[5]["vars"]["rootSize"]==7
assert "already share" in steps[6]["note"]
assert max(depth(p,v) for v in range(n))<=3
fill(CH,F,block([f"{a}-{b}" for a,b in reqs],["i"],steps),"@@TRACE1@@")
# trace 2
n=7
reqs=[(0,k) for k in range(1,7)]
pn=list(range(n)); p=list(range(n)); s=[1]*n; steps=[]
for i,(a,b) in enumerate(reqs):
    pn[root(pn,a)]=root(pn,b)
    ra,rb=root(p,a),root(p,b)
    big=ra if s[ra]>=s[rb] else rb
    small=rb if big==ra else ra
    p[small]=big; s[big]+=s[small]
    nd=depth(pn,0); sd=max(depth(p,v) for v in range(n))
    assert nd==i+1 and sd==1
    steps.append({"at":{"i":i},"vars":{"naiveDepth":nd,"sizeDepth":sd},
      "note":f"After merging 0 with {b}, student 0 needs {nd} hop"+("s" if nd!=1 else "")+f" under the naive rule, while the longest chain under the size rule is {sd}."})
fill(CH,F,block([f"{a}-{b}" for a,b in reqs],["i"],steps),"@@TRACE2@@")
print("ok")
