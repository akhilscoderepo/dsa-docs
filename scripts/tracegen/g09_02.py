from common import *
CH='09-sliding-window'; F='02-fixed-frequency-window.md'
def run(s,p,show):
    k=len(p); need={}; have={}
    for c in p: need[c]=need.get(c,0)+1
    st=[]; hits=[]
    for r,c in enumerate(s):
        have[c]=have.get(c,0)+1; note=f"The character '{c}' enters."
        if r>=k:
            o=s[r-k]; have[o]-=1; note+=f" The character '{o}' leaves."
        v={}
        if r>=k-1:
            eq=all(have.get(x,0)==need.get(x,0) for x in set(have)|set(need)); l=r-k+1
            v={"window":s[l:r+1],"equal":"yes" if eq else "no"}
            if eq: hits.append(l); note+=f" The counts match, so the start {l} is recorded."
            else:
                bad=[x for x in sorted(set(have)|set(need)) if have.get(x,0)!=need.get(x,0)][0]
                note+=f" The counts differ at '{bad}': the window holds {have.get(bad,0)} and the pattern needs {need.get(bad,0)}."
        else:
            l=0; note+=" The window is not full yet, so no test is made."
        st.append({"at":{"left":l,"right":r},"vars":v,"note":note})
    return st,hits
s1="bacdcab"; st,h=run(s1,"abc",0); assert h==[i for i in range(len(s1)-2) if sorted(s1[i:i+3])==sorted("abc")]==[0,4]
fill(CH,F,block(list(s1),["left","right"],st),"@@TRACE1@@")
s2="cabxaab"; st,h=run(s2,"aab",0); assert h==[4]
fill(CH,F,block(list(s2),["left","right"],st),"@@TRACE2@@")
