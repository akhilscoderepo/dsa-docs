from common import *
CH='03-strings'; F='01-indexed-scans.md'
def run(s):
    w=0; st=[{"at":{"i":-1},"vars":{"words":0},"note":"Start: no character has been read, so words is 0."}]
    for i,c in enumerate(s):
        starts = c!=' ' and (i==0 or s[i-1]==' ')
        if starts: w+=1
        shown = '␣' if c==' ' else c
        if c==' ': n=f"Position {i} holds a space, so no word starts."
        elif starts: n=f"Position {i} holds '{c}' and "+("it is the first position" if i==0 else "the character before it is a space")+f", so a word starts."
        else: n=f"Position {i} holds '{c}' and the character before it is a letter, so no word starts."
        st.append({"at":{"i":i},"vars":{"startsWord":starts,"words":w},"note":n+f" The count is {w}."})
    st.append({"at":{"i":len(s)},"vars":{"words":w},"note":f"The index equals the length, so the loop ends with {w} words."})
    return st,w
for ph,s,exp in (("@@TRACE1@@","to  be",2),("@@TRACE2@@"," x y ",2)):
    st,w=run(s); assert w==exp==len(s.split())
    fill(CH,F,block(['␣' if c==' ' else c for c in s],["i"],st),ph)
