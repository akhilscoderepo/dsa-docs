from common import *
CH='20-greedy'
F='09-greedy-and-two-pointers.md'
w=sorted([7,2,5,3,4]); limit=9
lo=0; hi=len(w)-1; boats=0; st=[]
while lo<=hi:
    if lo<hi and w[lo]+w[hi]<=limit:
        note=f"The lightest {w[lo]} and the heaviest {w[hi]} weigh {w[lo]+w[hi]} together, within the limit {limit}, so they share boat number {boats+1}."
        st.append({"at":{"lo":lo,"hi":hi},"vars":{"boats":boats+1},"note":note}); lo+=1
    elif lo<hi:
        note=f"The lightest {w[lo]} and the heaviest {w[hi]} weigh {w[lo]+w[hi]}, over the limit, so the heaviest rides alone in boat number {boats+1}."
        st.append({"at":{"lo":lo,"hi":hi},"vars":{"boats":boats+1},"note":note})
    else:
        note=f"Both pointers stand on the weight {w[lo]}, the last person, who rides alone in boat number {boats+1}."
        st.append({"at":{"lo":lo,"hi":hi},"vars":{"boats":boats+1},"note":note})
    hi-=1; boats+=1
assert boats==3
fill(CH,F,block([str(x) for x in w],["lo","hi"],st),"@@TRACE1@@")
t=sorted([60,20,90,30,10]); power=45
lo=0; hi=len(t)-1; score=0; best=0; st=[]
while lo<=hi:
    if power>=t[lo]:
        note=f"The cheapest token {t[lo]} is affordable with energy {power}, so it is played face up for a point."
        st.append({"at":{"lo":lo,"hi":hi},"vars":{"power":power-t[lo],"score":score+1},"note":note})
        power-=t[lo]; lo+=1; score+=1; best=max(best,score)
    elif score>0:
        note=f"The cheapest token {t[lo]} costs more than the energy {power}, so the dearest token {t[hi]} is sold face down for energy."
        st.append({"at":{"lo":lo,"hi":hi},"vars":{"power":power+t[hi],"score":score-1},"note":note})
        power+=t[hi]; hi-=1; score-=1
    else: break
assert best==3
fill(CH,F,block([str(x) for x in t],["lo","hi"],st),"@@TRACE2@@")
