from common import *
CH='09-sliding-window'; F='91-track-counts-inside-a-window.md'
def t1():
    s="eidbaooo"; p="ab"; k=2; need={}; 
    for c in p: need[c]=need.get(c,0)+1
    cnt={}; bad=len(need); st=[]; ans=-1
    def ok(c): return cnt.get(c,0)==need.get(c,0)
    for r,c in enumerate(s):
        was=ok(c); cnt[c]=cnt.get(c,0)+1; now=ok(c); n=f"The letter '{c}' enters."
        if was and not now: bad+=1; n+=f" Its count stops matching, so bad is {bad}."
        elif not was and now: bad-=1; n+=f" Its count now matches, so bad is {bad}."
        else: n+=f" Its status does not change, so bad stays {bad}."
        if r>=k:
            o=s[r-k]; was=ok(o); cnt[o]-=1; now=ok(o); n+=f" The letter '{o}' leaves."
            if was and not now: bad+=1; n+=f" Its count stops matching, so bad is {bad}."
            elif not was and now: bad-=1; n+=f" Its count now matches, so bad is {bad}."
            else: n+=f" Its status does not change, so bad stays {bad}."
        l=max(0,r-k+1)
        if r>=k-1 and bad==0: ans=r-k+1; n+=f" The counter is 0, so the scan returns the start {ans}."
        st.append({"at":{"left":l,"right":r},"vars":{"bad":str(bad)},"note":n})
        if ans>=0: break
    assert ans==3
    return block(list(s),["left","right"],st)
def t2():
    s="abcabc"; t="abc"; need={c:1 for c in t}; cnt={}; bad=3; l=0; best=None; ways=0; st=[]
    for r,c in enumerate(s):
        if cnt.get(c,0)<need.get(c,0): bad-=1
        cnt[c]=cnt.get(c,0)+1; n=f"The letter '{c}' enters, so bad is {bad}."
        while bad==0:
            L=r-l+1
            if best is None or L<best: best=L; ways=1; n+=f" The window '{s[l:r+1]}' covers the requirement and is the shortest so far, so best is {L} and ways is 1."
            elif L==best: ways+=1; n+=f" The window '{s[l:r+1]}' covers the requirement with the shortest length, so ways is {ways}."
            else: n+=f" The window '{s[l:r+1]}' covers the requirement but is longer than best."
            d=s[l]; cnt[d]-=1
            if cnt[d]<need.get(d,0): bad+=1; n+=f" The letter '{d}' leaves, so bad is {bad}."
            l+=1
        st.append({"at":{"left":l,"right":r},"vars":{"bad":str(bad),"best":str(best) if best else "none","ways":str(ways)},"note":n})
    assert (best,ways)==(3,4)
    return block(list(s),["left","right"],st)
fill(CH,F,t1(),"@@TRACE1@@"); fill(CH,F,t2(),"@@TRACE2@@")
