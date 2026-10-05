from common import *
CH='09-sliding-window'; F='01-fixed-size-window.md'
def t1():
    a=[4,2,7,1,3,5]; k=3; s=0; st=[]
    for r in range(k):
        s+=a[r]
        n=f"The value {a[r]} enters, so the sum is {s}."
        if r==k-1: n+=f" The window is full and the first total is {s}."
        st.append({"at":{"left":0,"right":r},"vars":{"sum":str(s)},"note":n})
    out=[s]
    for r in range(k,len(a)):
        s+=a[r]-a[r-k]; out.append(s)
        st.append({"at":{"left":r-k+1,"right":r},"vars":{"sum":str(s)},"note":f"The value {a[r]} enters and the value {a[r-k]} leaves, so the sum becomes {s}."})
    assert out==[sum(a[i:i+k]) for i in range(len(a)-k+1)]==[13,10,11,9]
    return block(a,["left","right"],st)
def t2():
    a=[-9,-1,-6,-2,-3]; k=2; s=a[0]+a[1]; best=s; st=[{"at":{"left":0,"right":1},"vars":{"sum":str(s),"best":str(best)},"note":f"The first window gives {s}, and best starts at {s}, not at 0."}]
    for r in range(k,len(a)):
        s+=a[r]-a[r-k]; old=best; best=max(best,s)
        n=f"The value {a[r]} enters and the value {a[r-k]} leaves, so the sum is {s}. "
        n+=f"The sum beats {old}, so best becomes {best}." if best!=old else f"The sum does not beat {best}, so best stays."
        st.append({"at":{"left":r-k+1,"right":r},"vars":{"sum":str(s),"best":str(best)},"note":n})
    assert best==max(a[i]+a[i+1] for i in range(4))==-5
    return block(a,["left","right"],st)
fill(CH,F,t1(),"@@TRACE1@@"); fill(CH,F,t2(),"@@TRACE2@@")
