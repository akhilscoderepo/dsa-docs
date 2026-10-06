from common import *
CH='18-tries'; F='91-look-up-prefixes-in-a-dictionary.md'
def mk(words):
    root={}
    for w in words:
        c=root
        for ch in w: c=c.setdefault(ch,{})
        c['$']=True
    return root
def tr(roots,w):
    root=mk(roots); c=root; st=[]
    for i,ch in enumerate(w):
        if ch not in c:
            st.append({"at":{"i":i},"vars":{"node":w[:i]},"note":f"The node {w[:i]} has no edge for {ch}, so the candidate set is empty. The word stays unchanged."}); return st,w
        c=c[ch]; note=f"The letter {ch} has an edge, so the walk moves to the node {w[:i+1]}."
        if '$' in c:
            note+=f" The node has a true flag, so the walk stops and returns the root {w[:i+1]}."
            st.append({"at":{"i":i},"vars":{"node":w[:i+1]},"note":note}); return st,w[:i+1]
        st.append({"at":{"i":i},"vars":{"node":w[:i+1]},"note":note+" The flag is false."})
    return st,w
st,r=tr(["cat","bat","rat"],"cattle"); assert r=="cat" and len(st)==3
fill(CH,F,block(list("cattle"),["i"],st),"@@TRACE1@@")
st,r=tr(["cat","cart"],"carb"); assert r=="carb" and len(st)==4
fill(CH,F,block(list("carb"),["i"],st),"@@TRACE2@@")
