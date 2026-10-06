from common import *
CH='19-recursion-and-backtracking'; F='91-search-a-board-with-a-prefix-tree.md'
row="aba"; words=["ab","aba"]
# trie as dict
root={}
for w in words:
    c=root
    for ch in w: c=c.setdefault(ch,{})
    c['$']=w
st=[]; on=[False]*3; found=[]; emitted=set()
def go(i,node,prefix,once,pre):
    if i<0 or i>=3 or on[i]: return
    ch=row[i]
    if ch not in node:
        st.append({"at":{"cell":i},"vars":{"node":prefix or "root","found":len(found)},"note":f"The letter {ch} has no edge below the node {prefix or 'root'}, so no word begins with {prefix+ch}. The call returns before it marks the cell."}); return
    nn=node[ch]; p=prefix+ch
    note=f"The call at cell {i} moves the node to {p}."
    if '$' in nn:
        w=nn['$']
        if once and w in emitted: note+=f" The slot of {w} is empty after its first report, so nothing is reported."
        else: found.append(w); emitted.add(w); note+=f" The node stores {w}, so the search reports it."
    st.append({"at":{"cell":i},"vars":{"node":p,"found":len(found)},"note":note})
    on[i]=True; go(i-1,nn,p,once,pre); go(i+1,nn,p,once,pre); on[i]=False
for s in range(3): go(s,root,"",False,None)
assert found==["ab","aba","ab","aba"]; print(len(st))
fill(CH,F,block(list(row),["cell"],st),"@@TRACE1@@")
st=[]; found=["ab","aba"]; emitted={"ab","aba"}; on=[False]*3
go(2,root,"",True,None)
print(len(st)); assert len(found)==2
fill(CH,F,block(list(row),["cell"],st),"@@TRACE2@@")
