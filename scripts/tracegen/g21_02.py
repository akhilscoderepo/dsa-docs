from common import *
CH='21-graph-traversal-models-dfs-and-ordinary-bfs'
NAME='02-graph-cloning.md'
adj={0:[1,2],1:[0,2],2:[0,1,3],3:[2]}
twin={}; st=[]
def visit(c,frm):
    if c in twin:
        st.append({"at":{"i":c},"vars":{"from":frm,"copies":len(twin),"result":"found"},"note":f"Call for card {c} from {frm}. It is already in the map, so the existing copy is returned at once."})
        return
    twin[c]=True
    st.append({"at":{"i":c},"vars":{"from":frm,"copies":len(twin),"result":"made"},"note":f"Call for card {c} from {frm}. No copy yet, so a blank copy is made and recorded before its threads are followed."})
    for nb in adj[c]: visit(nb,c)
visit(0,"start")
assert len(twin)==4 and len(st)==9
fill(CH,NAME,block(["0","1","2","3"],["i"],st),"@@TRACE1@@")
labels=[7,7,5]; names="abc"; seen=set(); st=[]
for i,l in enumerate(labels):
    seen.add(l)
    st.append({"at":{"i":i},"vars":{"label":l,"by_label":len(seen),"by_object":i+1},"note":f"Card {names[i]} with label {l} is discovered. The label map holds {len(seen)} entries and the identity map holds {i+1}."+(" The label was already a key, so the label map lost this card." if len(seen)<i+1 and labels.index(l)==i-1 or (len(seen)<i+1 and i==1) else "")})
fill(CH,NAME,block(list(names),["i"],st),"@@TRACE2@@")
