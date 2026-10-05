from common import *
CH='09-sliding-window'; F='05-at-most-k-distinct.md'
def run(a,k):
    cnt={}; l=0; best=0; st=[]
    for r,v in enumerate(a):
        cnt[v]=cnt.get(v,0)+1; n=f"The id {v} enters, so the distinct count is {len(cnt)}."
        while len(cnt)>k:
            g=a[l]; cnt[g]-=1
            if cnt[g]==0: del cnt[g]; n+=f" The id {g} leaves and its key is removed, so the distinct count is {len(cnt)}."
            else: n+=f" The id {g} leaves, but it still occurs inside, so the distinct count stays {len(cnt)}."
            l+=1
        best=max(best,r-l+1); n+=f" The window length is {r-l+1}, and best is {best}."
        st.append({"at":{"left":l,"right":r},"vars":{"distinct":str(len(cnt)),"best":str(best)},"note":n})
    return st,best
def brute(a,k):
    b=0
    for i in range(len(a)):
        for j in range(i,len(a)):
            if len(set(a[i:j+1]))<=k: b=max(b,j-i+1)
    return b
a=[1,2,1,3,3,2,2]; st,b=run(a,2); assert b==brute(a,2)==4
fill(CH,F,block(a,["left","right"],st),"@@TRACE1@@")
a=[4,4]; st,b=run(a,0); assert b==brute(a,0)==0
fill(CH,F,block(a,["left","right"],st),"@@TRACE2@@")
for a,k,e in (([5,5,2,2,2,7],1,3),([9],1,1),([4,4,4],2,3),([1,2,2],1,2)): assert brute(a,k)==e
assert brute(list("eceba"),2)==3 and brute(list("aaabbb"),1)==3
