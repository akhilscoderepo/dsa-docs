from common import *
CH='03-strings'; F='03-parsing-state.md'
def run(s):
    state="START"; st=[{"at":{"i":-1},"vars":{"state":"START"},"note":"Start: the parser has read nothing, so the state is START."}]
    ok=True
    for i,c in enumerate(s):
        letter=c.isascii() and (c.isalpha() or c=='_'); digit=c in '0123456789'
        if state=="START" and letter: ns="BODY"; n=f"Index {i} holds '{c}', a legal first character, so the state becomes BODY."
        elif state=="BODY" and (letter or digit): ns="BODY"; n=f"Index {i} holds '{c}', which is legal in BODY, so the state stays BODY."
        else:
            st.append({"at":{"i":i},"vars":{"state":"REJECT"},"note":f"Index {i} holds '{c}', which no transition allows in {state}, so the method returns false."}); ok=False; break
        state=ns; st.append({"at":{"i":i},"vars":{"state":state},"note":n})
    if ok:
        st.append({"at":{"i":len(s)},"vars":{"state":state},"note":f"The index equals the length and the state is {state}, which is accepting, so the answer is true."})
    return st,ok
for ph,s,exp in (("@@TRACE1@@","x_1",True),("@@TRACE2@@","ab-c",False)):
    st,ok=run(s); assert ok==exp
    import re; assert ok==bool(re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',s))
    fill(CH,F,block(list(s),["i"],st),ph)
