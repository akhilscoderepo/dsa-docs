from common import *
CH='13-deques-and-monotonic-queues'
F='07-index-expiry.md'
fmt=lambda l:"["+",".join(map(str,l))+"]"
a=[5,3,6,2,4,1,7];k=3
d=[];out=[];s1=[]
for i,v in enumerate(a):
    exp=[]
    while d and d[0]<i-k: exp.append(d.pop(0))
    ans=a[d[0]] if d else -1
    out.append(ans)
    dom=[]
    while d and a[d[-1]]<v: dom.append(d.pop())
    d.append(i)
    p=[f"Position {i} holds {v}."]
    if exp: p.append(f"The age test removes position {exp[0]} from the front.")
    p.append("No earlier position is eligible, so the answer is none." if ans==-1 else f"The front gives the answer {ans}.")
    if dom: p.append("Then the value "+str(v)+" removes position "+", ".join(map(str,dom))+" from the back.")
    p.append("Then position "+str(i)+" is appended.")
    s1.append({"at":{"i":i},"vars":{"deque":fmt(d),"answers":fmt(out)},"note":" ".join(p)})
assert out==[-1,5,5,6,6,6,4] and s1[6]["vars"]["deque"]=="[6]"
fill(CH,F,block(a,["i"],s1),"@@TRACE1@@")
nums=[3,-2,4,-1,2,-5,6]
sc=[0]*7;d=[0];sc[0]=3;s2=[{"at":{"i":0},"vars":{"scores":"[3]","deque":"[0]"},"note":"The start is worth 3 and position 0 is stored."}]
for i in range(1,7):
    exp=[]
    while d[0]<i-k: exp.append(d.pop(0))
    sc[i]=nums[i]+sc[d[0]]
    dom=[]
    while d and sc[d[-1]]<=sc[i]: dom.append(d.pop())
    d.append(i)
    p=[f"Position {i} holds {nums[i]}."]
    if exp: p.append(f"The age test removes position {exp[0]} from the front.")
    p.append(f"The front is position {(dom or [None])[0] if False else ''}".replace(" is position ","") if False else "")
    s2.append((i,exp,dom))
# rebuild notes properly
s2=[s2[0]]
sc=[0]*7;sc[0]=3;d=[0]
for i in range(1,7):
    exp=[]
    while d[0]<i-k: exp.append(d.pop(0))
    f=d[0]
    sc[i]=nums[i]+sc[f]
    dom=[]
    while d and sc[d[-1]]<=sc[i]: dom.append(d.pop())
    d.append(i)
    p=[f"Position {i} holds {nums[i]}."]
    if exp: p.append(f"The age test removes position {exp[0]} from the front.")
    p.append(f"The front is position {f} with score {sc[f]}, so the score here is {sc[i]}.")
    if dom: p.append("The new score removes position "+", ".join(map(str,dom))+" from the back.")
    s2.append({"at":{"i":i},"vars":{"scores":fmt(sc[:i+1]),"deque":fmt(d)},"note":" ".join(p)})
assert sc[6]==15
fill(CH,F,block(nums,["i"],s2),"@@TRACE2@@")
