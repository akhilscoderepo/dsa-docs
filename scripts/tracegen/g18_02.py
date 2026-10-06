from common import *
CH='18-tries'; F='02-insert-and-search.md'
def ins(root,w):
    c=root
    for ch in w:
        c=c.setdefault(ch,{})
    c['$']=True
root={}; ins(root,"app")
w="apple"; c=root; created=0; st=[]
for i,ch in enumerate(w):
    pre=w[:i+1]; s=ord(ch)-97
    if ch in c: note=f"The slot {s} for {ch} holds a node, so the insert moves into the node for {pre}."
    else: c[ch]={}; created+=1; note=f"The slot {s} for {ch} is empty, so the insert creates the node for {pre}."
    c=c[ch]
    if i==len(w)-1: c['$']=True; note+=" The word ends here, so the terminal flag becomes true."
    st.append({"at":{"i":i},"vars":{"slot":s,"created":created},"note":note})
assert created==2
fill(CH,F,block(list(w),["i"],st),"@@TRACE1@@")
root={}; ins(root,"app"); ins(root,"apple")
w="apx"; c=root; st=[]
for i,ch in enumerate(w):
    s=ord(ch)-97
    if ch in c:
        c=c[ch]; note=f"The slot {s} for {ch} holds a node, so the search moves into the node for {w[:i+1]}."
        st.append({"at":{"i":i},"vars":{"slot":s,"found":"yes"},"note":note})
    else:
        st.append({"at":{"i":i},"vars":{"slot":s,"found":"no"},"note":f"The slot {s} for {ch} is empty, so no stored word starts with {w[:i+1]}. The search returns false and reads no more characters."}); break
assert len(st)==3
fill(CH,F,block(list(w),["i"],st),"@@TRACE2@@")
