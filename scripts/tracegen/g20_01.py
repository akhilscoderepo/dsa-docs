from common import *
CH='20-greedy'
F='01-local-choice.md'
need=[1,3,4]; beds=[1,1,2,3,5]
g=0; st=[]; disc=0
for r,cap in enumerate(beds):
    if g<len(need) and cap>=need[g]:
        note=f"The room with {cap} bed{'s' if cap!=1 else ''} fits the waiting party of {need[g]}, so the key goes out and the party cursor advances."
        g+=1
    else:
        disc+=1
        note=f"The room with {cap} bed{'s' if cap!=1 else ''} is too small for the waiting party of {need[g]}, so it is discarded and nobody is housed."
    st.append({"at":{"r":r},"vars":{"housed":g,"discarded":disc,"waiting":(need[g] if g<len(need) else "none")},"note":note})
assert g==3 and disc==2 and st[-1]["at"]["r"]==len(beds)-1
fill(CH,F,block([str(b) for b in beds],["r"],st),"@@TRACE1@@")
bills=[5,5,10,5,20,10,5,20]
f=t=0; st=[]
for i,b in enumerate(bills):
    if b==5:
        f+=1; note="A five is paid for a five-dollar drink, so no change is owed and the fives counter grows."
    elif b==10:
        assert f>0; f-=1; t+=1; note="A ten is paid, so one five goes back as change and the tens counter grows."
    elif t>0 and f>0:
        t-=1; f-=1; note="A twenty is paid. Fifteen is given as a ten plus a five, which keeps the remaining fives for later customers."
    else:
        assert f>=3; f-=3; note="A twenty is paid with no ten available, so three fives are given."
    st.append({"at":{"i":i},"vars":{"fives":f,"tens":t},"note":note})
assert f==0 and t==0
fill(CH,F,block([str(b) for b in bills],["i"],st),"@@TRACE2@@")
