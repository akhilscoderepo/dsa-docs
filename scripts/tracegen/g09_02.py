from common import *
CH='09-sliding-window'
F='02-fixed-frequency-windows.md'

def run(text,card,letters):
    m=len(card)
    need={c:card.count(c) for c in letters}
    have={c:0 for c in letters}
    st=[]; found=[]
    for right,ch in enumerate(text):
        have[ch]+=1
        if right>=m: have[text[right-m]]-=1
        if right>=m-1:
            left=right-m+1
            ok=(have==need)
            if ok: found.append(left)
            vars_={c:have[c] for c in letters}
            vars_["match"]="yes" if ok else "no"
            stretch=text[left:right+1]
            if right==m-1:
                note=f"The first {m} beads are in the tally, so the stretch is {stretch}."
            else:
                note=f"{text[right-m]} leaves and {ch} enters, so the stretch is {stretch}."
            note+=(f" The tally matches the card, so the start {left} joins the answers." if ok else " The tally differs from the card, so nothing is recorded.")
            st.append({"at":{"left":left,"right":right},"vars":vars_,"note":note})
    return st,found

t1="abcbacab"
s1,f1=run(t1,"abc","abc")
assert f1==[0,2,3,5] and s1[2]["vars"]["match"]=="yes" and "cba" in s1[2]["note"] and len(s1)==6
fill(CH,F,block(list(t1),["left","right"],s1),"@@TRACE1@@")
t2="zzabzaab"
s2,f2=run(t2,"aab","abz")
assert f2==[5] and s2[2]["vars"]["match"]=="no" and "abz" in s2[2]["note"] and s2[-1]["vars"]["match"]=="yes"
fill(CH,F,block(list(t2),["left","right"],s2),"@@TRACE2@@")
