from common import *
CH='03-strings'; F='02-safe-construction.md'
def run(a):
    out=""; st=[{"at":{"i":-1},"vars":{"out":""},"note":"Start: the builder is empty."}]
    for i,v in enumerate(a):
        sep = i>0
        out += ("," if sep else "")+str(v)
        n=(f"Index {i} writes a comma and then {v}." if sep else f"Index {i} writes {v} and no comma, because it is the first element.")
        st.append({"at":{"i":i},"vars":{"out":out},"note":n+f" The builder holds {out}."})
    st.append({"at":{"i":len(a)},"vars":{"out":out},"note":f"The index equals the length, so the loop ends with {out} and no trailing comma."})
    return st,out
for ph,a,exp in (("@@TRACE1@@",[3,1,4],"3,1,4"),("@@TRACE2@@",[9,15],"9,15")):
    st,o=run(a); assert o==exp==",".join(map(str,a))
    fill(CH,F,block([str(x) for x in a],["i"],st),ph)
