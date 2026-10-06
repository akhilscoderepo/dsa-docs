from common import *
CH='16-trees-bfs-and-bsts'; F='06-general-and-bst-lca.md'
cells=[10,4,15,2,7,12,20,6,9]
kids={0:(1,2),1:(3,4),2:(5,6),3:(None,None),4:(7,8),5:(None,None),6:(None,None),7:(None,None),8:(None,None)}
P,Q=7,8  # indices of 6 and 9
st=[]
def post(i):
    if i is None: return None
    if i in (P,Q):
        st.append({"at":{"node":i},"vars":{"returns":cells[i]},"note":f"{cells[i]} is a target, so the call returns it at once."}); return i
    l=post(kids[i][0]); r=post(kids[i][1])
    if l is not None and r is not None:
        st.append({"at":{"node":i},"vars":{"returns":cells[i]},"note":f"Both children reported a target, so {cells[i]} is the lowest common ancestor and the call returns it."}); return i
    res=l if l is not None else r
    st.append({"at":{"node":i},"vars":{"returns":"null" if res is None else cells[res]},"note":f"{'Only one child reported, so the call passes that report up.' if res is not None else 'No child reported a target, so the call returns null.'}"}); return res
ans=post(0); assert cells[ans]==7
fill(CH,F,block(cells,["node"],st),"@@TRACE1@@")
lo,hi=6,9; i=0; st=[]
while True:
    v=cells[i]
    if hi<v: st.append({"at":{"node":i},"vars":{"lo":lo,"hi":hi},"note":f"Both keys are smaller than {v}, so the walk goes left."}); i=kids[i][0]
    elif lo>v: st.append({"at":{"node":i},"vars":{"lo":lo,"hi":hi},"note":f"Both keys are larger than {v}, so the walk goes right."}); i=kids[i][1]
    else:
        st.append({"at":{"node":i},"vars":{"lo":lo,"hi":hi},"note":f"The keys {lo} and {hi} lie on different sides of {v}, so {v} is the split point and the answer."}); break
assert cells[i]==7
fill(CH,F,block(cells,["node"],st),"@@TRACE2@@")
