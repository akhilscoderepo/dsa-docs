from common import *
CH='03-strings'; F='04-normalization.md'
def run(s):
    out=""; st=[{"at":{"i":-1},"vars":{"out":""},"note":"Start: the builder is empty."}]
    for i,c in enumerate(s):
        shown='the space' if c==' ' else f"'{c}'"
        if 'A'<=c<='Z': out+=c.lower(); n=f"Index {i} holds the capital {c}, so the loop appends {c.lower()}."
        elif 'a'<=c<='z' or '0'<=c<='9': out+=c; n=f"Index {i} holds {shown}, so the loop appends it unchanged."
        else: n=f"Index {i} holds {shown}, which is noise, so the builder stays unchanged."
        st.append({"at":{"i":i},"vars":{"out":out},"note":n+(f" The builder holds {out}." if out else " The builder is empty.")})
    st.append({"at":{"i":len(s)},"vars":{"out":out},"note":"The index equals the length, so the canonical form is "+(out if out else "the empty string")+"."})
    return st,out
import re
for ph,s,exp in (("@@TRACE1@@","A-b 1","ab1"),("@@TRACE2@@","?!","")):
    st,o=run(s); assert o==exp==re.sub(r'[^a-z0-9]','',s.lower())
    fill(CH,F,block(['␣' if c==' ' else c for c in s],["i"],st),ph)
