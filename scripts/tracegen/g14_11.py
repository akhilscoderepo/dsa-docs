from common import *
CH='14-linked-lists'
F='11-linked-list-map.md'
vals=[5,9,2,6];rnd=[2,0,-1,3]
n=4
steps=[]
for i in range(n):
    steps.append({"at":{"orig":i,"target":-1},"vars":{"pass":"first","map_size":i+1},"note":f"First pass: a new clone holding {vals[i]} is created for original node {i}, and the identity map now records {i+1} original-to-clone pair(s). No links are set yet."})
wired=[]
for i in range(n):
    t=rnd[i]
    nx=f"its next is the clone of node {i+1}" if i+1<n else "its next is null"
    rn=f"its random is the clone of node {t}" if t>=0 else "its random stays null"
    if t==i: rn+=", which is the clone itself"
    wired.append(f"{i}:{t}")
    steps.append({"at":{"orig":i,"target":t},"vars":{"pass":"second","random_so_far":"["+",".join(w.split(':')[1] for w in wired)+"]"},"note":f"Second pass: for original node {i} holding {vals[i]}, {nx}, and {rn}. Each target is found with one map lookup."})
fill(CH,F,block(vals,["orig","target"],steps),"@@TRACE1@@")
v2=[7,7,3,7];r2=[3,2,1,0]
st=[]
for i in range(4):
    st.append({"at":{"orig":i,"target":-1},"vars":{"pass":"first","identity_map":i+1,"value_map":len(set(v2[:i+1]))},"note":f"First pass: a clone is made for original node {i} holding {v2[i]}. The identity map holds {i+1} pairs. A map keyed by value would hold only {len(set(v2[:i+1]))}, since equal values collapse into one key."})
for i in range(4):
    t=r2[i]
    st.append({"at":{"orig":i,"target":t},"vars":{"pass":"second","target_node":t},"note":f"Second pass: original node {i} points at node {t}, holding {v2[t]}. The identity map returns the clone of node {t} exactly. A value-keyed map would return the clone of the last node holding {v2[t]}, which is correct only when that last node is node {t}."})
fill(CH,F,block(v2,["orig","target"],st),"@@TRACE2@@")
