from common import *
CH='18-tries'; F='04-word-break-trie-search.md'
def mk(words):
    root={}
    for w in words:
        c=root
        for ch in w: c=c.setdefault(ch,{})
        c['$']=True
    return root
# trace 1
D=["cat","cats","and","sand","dog"]; root=mk(D); s="catsand"; st=[]; c=root; cuts=[]
for i in range(0,len(s)):
    ch=s[i]
    if ch not in c:
        st.append({"at":{"i":i},"vars":{"cuts":str(cuts)},"note":f"The node for {s[:i]} has no edge for {ch}, so the walk reaches a dead end and stops."}); break
    c=c[ch]; note=f"The letter {ch} has an edge, so the walk moves to the node for {s[:i+1]}."
    if '$' in c: cuts.append(i+1); note+=f" The node is terminal, so the walk records the cut point {i+1}."
    st.append({"at":{"i":i},"vars":{"cuts":str(cuts)},"note":note})
assert cuts==[3,4] and len(st)==5
fill(CH,F,block(list(s),["i"],st),"@@TRACE1@@")
# trace 2
D=["a","aa"]; root=mk(D); s="aaab"; st=[]; visits={}
def cuts_of(s,f):
    c=root; out=[]
    for i in range(f,len(s)):
        if s[i] not in c: break
        c=c[s[i]]
        if '$' in c: out.append(i+1)
    return out
def go(f):
    visits[f]=visits.get(f,0)+1
    cs=cuts_of(s,f)
    note=f"The call at index {f} finds the cut points {cs}." if cs else f"The call at index {f} finds no cut point, so it fails."
    if visits[f]>1: note+=f" This index was visited before, so the search repeats its work."
    st.append({"at":{"from":f},"vars":{"visits":visits[f]},"note":note})
    for e in cs: go(e)
go(0)
assert len(st)==7 and visits=={0:1,1:1,2:2,3:3}
fill(CH,F,block(list(s),["from"],st),"@@TRACE2@@")
