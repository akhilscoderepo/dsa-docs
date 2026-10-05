from common import *
CH='09-sliding-window'; F='04-shortest-covering-window.md'
def run(s,t):
    need={};have={}
    for c in t: need[c]=need.get(c,0)+1
    miss=len(t); l=0; best=None; st=[]
    for r,c in enumerate(s):
        n=f"The character '{c}' enters."
        if have.get(c,0)<need.get(c,0): miss-=1; n+=" It fills a required copy."
        else: n+=" It is a surplus."
        have[c]=have.get(c,0)+1
        while miss==0:
            L=r-l+1
            if best is None or L<best: best=L; n+=f" The block '{s[l:r+1]}' covers the requirement and is the shortest so far, with length {L}."
            else: n+=f" The block '{s[l:r+1]}' covers the requirement, with length {L}."
            d=s[l]; have[d]-=1
            if have[d]<need.get(d,0): miss+=1; n+=f" The character '{d}' leaves and breaks the cover."
            else: n+=f" The surplus '{d}' leaves, and the cover holds."
            l+=1
        st.append({"at":{"left":l,"right":r},"vars":{"missing":str(miss),"best":str(best) if best else "none"},"note":n})
    return st,best
def brute(s,t):
    b=None
    for i in range(len(s)):
        for j in range(i,len(s)):
            w=s[i:j+1]
            if all(w.count(c)>=t.count(c) for c in set(t)) and (b is None or len(w)<b): b=len(w)
    return b
s1="bccbbacc"; st,b=run(s1,"ab"); assert b==brute(s1,"ab")==2
fill(CH,F,block(list(s1),["left","right"],st),"@@TRACE1@@")
s2="abcabca"; st,b=run(s2,"aab"); assert b==brute(s2,"aab")==4
fill(CH,F,block(list(s2),["left","right"],st),"@@TRACE2@@")
