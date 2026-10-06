from common import *
CH='18-tries'; F='03-wildcard-branching.md'
def mk(words):
    root={}
    for w in words:
        c=root
        for ch in w: c=c.setdefault(ch,{})
        c['$']=True
    return root
def trace(words,pat):
    root=mk(words); st=[]; calls=[0]
    def go(node,pre,i):
        calls[0]+=1
        if i==len(pat):
            ok='$' in node
            return ok
        ch=pat[i]
        kids=[k for k in sorted(node) if k!='$']
        if ch!='.':
            if ch in node:
                st.append({"at":{"i":i},"vars":{"node":pre+ch,"calls":calls[0]},"note":f"The letter {ch} has an edge, so the search moves to the node {pre+ch}."})
                return go(node[ch],pre+ch,i+1)
            st.append({"at":{"i":i},"vars":{"node":pre,"calls":calls[0]},"note":f"The node {pre} has no edge for {ch}, so this branch returns false."})
            return False
        if not kids:
            st.append({"at":{"i":i},"vars":{"node":pre,"calls":calls[0]},"note":f"The dot needs a child, but the node {pre} has none, so the search returns false."}); return False
        for k in kids:
            st.append({"at":{"i":i},"vars":{"node":pre+k,"calls":calls[0]},"note":f"The dot tries the child {k}, which leads to the node {pre+k}."})
            if go(node[k],pre+k,i+1): return True
        return False
    r=go(root,"",0)
    return r,st
r,st=trace(["cap","cot"],"c.t"); assert r
# make the final success step explicit
st[-1]["note"]+=" The pattern ends on a node with a true flag, so the search returns true."
fill(CH,F,block(list("c.t"),["i"],st),"@@TRACE1@@")
r,st=trace(["cat"],"ca.."); assert not r
fill(CH,F,block(list("ca.."),["i"],st),"@@TRACE2@@")
print(len(st))
