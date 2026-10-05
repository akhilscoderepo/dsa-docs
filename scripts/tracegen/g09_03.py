from common import *
CH='09-sliding-window'; F='03-longest-valid-window.md'
def t1():
    a=[1,1,0,1,0,1,1]; l=0; z=0; best=0; st=[]
    for r in range(len(a)):
        n=f"The value {a[r]} enters."
        if a[r]==0: z+=1; n+=f" It is an outage, so outages is {z}."
        while z>1:
            if a[l]==0: z-=1; n+=f" The outage at index {l} leaves, so outages is {z}."
            else: n+=f" The value at index {l} leaves."
            l+=1
        best=max(best,r-l+1); n+=f" The window length {r-l+1} is valid, and best is {best}."
        st.append({"at":{"left":l,"right":r},"vars":{"outages":str(z),"best":str(best)},"note":n})
    assert best==4
    return block(a,["left","right"],st)
def t2():
    s="abcdbea"; l=0; cnt={}; best=0; st=[]
    for r,c in enumerate(s):
        cnt[c]=cnt.get(c,0)+1; n=f"The character '{c}' enters."; rem=0
        while cnt[c]>1:
            o=s[l]; cnt[o]-=1; l+=1; rem+=1; n+=f" The character '{o}' leaves."
        if rem>1: n+=f" The loop ran {rem} times for this index."
        best=max(best,r-l+1)
        st.append({"at":{"left":l,"right":r},"vars":{"window":s[l:r+1],"best":str(best)},"note":n+f" The window '{s[l:r+1]}' has no repeat, and best is {best}."})
    assert best==5
    return block(list(s),["left","right"],st)
fill(CH,F,t1(),"@@TRACE1@@"); fill(CH,F,t2(),"@@TRACE2@@")
