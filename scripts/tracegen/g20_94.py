from common import *
CH='20-greedy'; F='94-pair-items-from-both-ends.md'
w=sorted([5,2,3,5,2]); limit=6; lo=0; hi=len(w)-1; m=0; st=[]
while lo<=hi:
    at={"lo":lo,"hi":hi}
    if lo<hi and w[lo]+w[hi]<=limit:
        note=f"The sum {w[lo]} + {w[hi]} is {w[lo]+w[hi]}, which fits the limit, so one machine takes both jobs and both pointers move."; lo+=1; hi-=1
    elif lo<hi:
        note=f"The sum {w[lo]} + {w[hi]} is {w[lo]+w[hi]}, which passes the limit, so the job {w[hi]} runs alone and hi moves left."; hi-=1
    else:
        note=f"Only the job {w[lo]} remains, so it runs alone."; hi-=1
    m+=1
    st.append({"at":at,"vars":{"machines":m},"note":note})
assert m==4
fill(CH,F,block(w,["lo","hi"],st),"@@TRACE1@@")
t=sorted([40,60,90,150,400]); power=100; score=0; best=0; lo=0; hi=len(t)-1; st=[]
while lo<=hi:
    at={"lo":lo,"hi":hi}
    if power>=t[lo]:
        power-=t[lo]; score+=1; note=f"The power covers the token {t[lo]}, so the player plays it face up, and the score becomes {score}."; lo+=1
    elif score>0:
        power+=t[hi]; score-=1; note=f"The token {t[lo]} costs too much, so the player plays the token {t[hi]} face down. The power becomes {power} and the score drops to {score}."; hi-=1
    else: break
    best=max(best,score)
    st.append({"at":at,"vars":{"power":power,"score":score},"note":note})
assert best==3, best
fill(CH,F,block(t,["lo","hi"],st),"@@TRACE2@@")
