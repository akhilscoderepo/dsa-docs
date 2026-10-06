from common import *
CH='18-tries'; F='01-prefix-nodes.md'
def build(words):
    root={}; n=0
    for w in words:
        c=root
        for ch in w:
            if ch not in c: c[ch]={}; n+=1
            c=c[ch]
        c['$']=True
    return root,n
# trace 1: insert "cat" into a tree holding "car"
root,n=build(["car"]); st=[]; c=root; w="cat"
for i,ch in enumerate(w):
    pre=w[:i+1]
    if ch in c: note=f"The node for {pre} already exists, so the insert reuses it and creates nothing."
    else: c[ch]={}; n+=1; note=f"The node for {pre} is missing, so the insert creates it."
    c=c[ch]
    if i==len(w)-1: c['$']=True; note+=" The word ends here, so the terminal flag becomes true."
    st.append({"at":{"i":i},"vars":{"prefix":pre,"nodes":n},"note":note})
assert n==4
pass
# trace 2: query "ca" in {car,cat}
root,n=build(["card","care"]); st=[]; c=root; w="car"
for i,ch in enumerate(w):
    pre=w[:i+1]; c=c[ch]
    note=f"The edge {ch} exists, so the walk reaches the node for {pre}."
    if i==len(w)-1:
        term='$' in c; assert not term
        note+=" The node exists, so startsWith returns true. The terminal flag is false, so search returns false."
    st.append({"at":{"i":i},"vars":{"prefix":pre,"flag":"true" if '$' in c else "false"},"note":note})
fill(CH,F,block(list(w),["i"],st),"@@TRACE2@@")
