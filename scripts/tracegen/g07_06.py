from common import *
CH='07-prefix-sums-and-difference-arrays'
F='06-remainder-classes.md'
a=[4,5,0,-2,-3,1]; k=5; seen=[0]*k; seen[0]=1; tot=0; cnt=0; st=[]
for i,x in enumerate(a):
    tot+=x; c=tot%k if tot>=0 else tot%k  # python mod is already normalized
    add=seen[c]; cnt+=add; seen[c]+=1
    st.append({"at":{"i":i},"vars":{"total":tot,"class":c,"added":add,"count":cnt},"note":f"The total is {tot}, in class {c}. Class {c} occurred {add} times before, so {add} stretches end here and the count is {cnt}."})
assert cnt==7 and st[2]["vars"]["added"]==2 and st[2]["vars"]["count"]==3
fill(CH,F,block([str(x) for x in a],["i"],st),"@@TRACE1@@")
a=[-3,1,2,-4]; k=3; tot=0; seen=[0]*k; seen[0]=1; cnt=0; st=[]
def jrem(t): return int(abs(t)%k)*(1 if t>=0 else -1)
for i,x in enumerate(a):
    tot+=x; c=tot%k; add=seen[c]; cnt+=add; seen[c]+=1
    st.append({"at":{"i":i},"vars":{"total":tot,"javaRemainder":jrem(tot),"class":c,"count":cnt},"note":f"The total is {tot}. Java's % gives {jrem(tot)} and the normalized class is {c}, which occurred {add} times before, so the count is {cnt}."})
assert cnt==3 and st[1]["vars"]["javaRemainder"]==-2 and st[1]["vars"]["class"]==1
fill(CH,F,block([str(x) for x in a],["i"],st),"@@TRACE2@@")
