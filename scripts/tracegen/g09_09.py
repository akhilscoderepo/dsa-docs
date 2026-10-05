from common import *
from collections import Counter
CH='09-sliding-window'; F='09-shrink-fully-or-once.md'
def t1():
    s="AAABCD"; k=1; cnt={}; l=0; H=0; st=[]
    for r,c in enumerate(s):
        cnt[c]=cnt.get(c,0)+1; H=max(H,cnt[c]); n=f"The letter '{c}' enters, so peak is {H}."
        if r-l+1-H>k: n+=f" The length {r-l+1} minus peak {H} is {r-l+1-H}, above {k}, so the letter '{s[l]}' leaves and the window slides."; cnt[s[l]]-=1; l+=1
        else: n+=" The cost is within the budget, so the window grows."
        w=s[l:r+1]; real=len(w)-max(Counter(w).values()); ok=real<=k
        st.append({"at":{"left":l,"right":r},"vars":{"window":w,"peak":str(H),"valid":"yes" if ok else "no"},"note":n+(f" The window '{w}' is valid." if ok else f" The window '{w}' is invalid, with exact cost {real}.")})
    assert len(s)-l==4
    return block(list(s),["left","right"],st)
def t2():
    s="abcdbea"; cnt={}; l=0; best=0; st=[]
    for r,c in enumerate(s):
        cnt[c]=cnt.get(c,0)+1; n=f"The character '{c}' enters."
        if cnt[c]>1: n+=f" The count of '{c}' is {cnt[c]}, so one character leaves: '{s[l]}'."; cnt[s[l]]-=1; l+=1
        w=s[l:r+1]; dup=len(set(w))<len(w); best=max(best,r-l+1)
        n+=f" The window '{w}' has {'a repeated character' if dup else 'no repeat'}, and best is {best}."
        st.append({"at":{"left":l,"right":r},"vars":{"window":w,"repeat":"yes" if dup else "no","best":str(best)},"note":n})
    assert best==6
    return block(list(s),["left","right"],st)
fill(CH,F,t1(),"@@TRACE1@@"); fill(CH,F,t2(),"@@TRACE2@@")
