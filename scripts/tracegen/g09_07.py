from common import *
CH='09-sliding-window'; F='07-replacement-budget-window.md'
def run(s,k):
    cnt={}; l=0; best=0; st=[]
    for r,c in enumerate(s):
        cnt[c]=cnt.get(c,0)+1; n=f"The letter '{c}' enters."
        while r-l+1-max(cnt.values())>k:
            n+=f" The window '{s[l:r+1]}' has length {r-l+1} and dominant count {max(cnt.values())}, so the cost is {r-l+1-max(cnt.values())}, above {k}. The letter '{s[l]}' leaves."
            cnt[s[l]]-=1; l+=1
        d=max(cnt.values()); best=max(best,r-l+1)
        st.append({"at":{"left":l,"right":r},"vars":{"window":s[l:r+1],"dominant":str(d),"cost":str(r-l+1-d),"best":str(best)},"note":n+f" The window '{s[l:r+1]}' has dominant count {d} and cost {r-l+1-d}, so best is {best}."})
    return st,best
s="aababba"; st,b=run(s,1); assert b==4
fill(CH,F,block(list(s),["left","right"],st),"@@TRACE1@@")
s="abbbcxyz"; st,b=run(s,1); assert b==4
fill(CH,F,block(list(s),["left","right"],st),"@@TRACE2@@")
