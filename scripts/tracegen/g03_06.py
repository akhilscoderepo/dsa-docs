from common import *
CH='03-strings'
def enc_trace(s):
    cells=list(s); st=[]; out=""; cur=s[0]; ln=1
    st.append({"at":{"i":0},"vars":{"cur":cur,"len":1,"output":out or "empty"},"note":f"Read {cur!r}. It starts the pending run with length 1."})
    for i in range(1,len(s)):
        c=s[i]
        if c==cur:
            ln+=1
            st.append({"at":{"i":i},"vars":{"cur":cur,"len":ln,"output":out or "empty"},"note":f"{c!r} matches the pending character, so the length rises to {ln}."})
        else:
            out+=f"{ln}{cur}"
            st.append({"at":{"i":i},"vars":{"cur":c,"len":1,"output":out},"note":f"{c!r} differs from {cur!r}. Flush {ln}{cur} to the output and start a new pending run of {c!r}."})
            cur=c; ln=1
    out+=f"{ln}{cur}"
    st.append({"at":{"i":len(s)},"vars":{"cur":cur,"len":ln,"output":out},"note":f"The input has ended. Flush the final run {ln}{cur}. The output is {out}."})
    return st,out
st,out=enc_trace("ppqrrr"); assert out=="2p1q3r"
fill(CH,'06-run-construction.md',block(list("ppqrrr"),["i"],st),"@@TRACE1@@")
# in-place compress
s="zzzzyyx"; chars=list(s); w=0; cur=chars[0]; ln=1; st=[]
st.append({"at":{"i":0},"vars":{"cur":cur,"len":1,"write":0},"note":"Read 'z'. The pending run starts with length 1 and nothing has been written."})
for i in range(1,len(chars)+1):
    if i<len(chars) and chars[i]==cur:
        ln+=1
        st.append({"at":{"i":i},"vars":{"cur":cur,"len":ln,"write":w},"note":f"{chars[i]!r} matches, so the length rises to {ln}."}); continue
    wrote=cur
    chars[w]=cur; w+=1
    if ln>1:
        for d in str(ln): chars[w]=d; w+=1; wrote+=d
    if i<len(chars):
        nxt=chars[i]
        st.append({"at":{"i":i},"vars":{"cur":nxt,"len":1,"write":w},"note":f"{nxt!r} differs. Write {wrote} at the write position, which is now {w}, and start a new pending run."}); cur=nxt; ln=1
    else:
        st.append({"at":{"i":i},"vars":{"cur":cur,"len":ln,"write":w},"note":f"The input has ended. Write the final run {wrote}. The compressed length is {w}."})
assert w==5 and "".join(chars[:5])=="z4y2x"
fill(CH,'06-run-construction.md',block(list(s),["i"],st),"@@TRACE2@@")
