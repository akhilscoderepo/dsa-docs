from common import *
CH='16-trees-bfs-and-bsts'; F='05-kth-and-range-queries.md'
cells=[50,30,70,20,40,60,80]; kids={0:(1,2),1:(3,4),2:(5,6),3:(None,None),4:(None,None),5:(None,None),6:(None,None)}
# Trace 1: iterative inorder, k=3
st=[]; stack=[]; node=0; visits=0; k=3; ans=None
def snap(i,note): st.append({"at":{"node":i},"vars":{"stack":str([cells[j] for j in stack]),"visits":visits},"note":note})
while node is not None or stack:
    while node is not None:
        stack.append(node); snap(node,f"The loop pushes {cells[node]} onto the stack and moves to its left child."); node=kids[node][0]
    node=stack.pop(); visits+=1
    if visits==k:
        snap(node,f"The loop pops {cells[node]} as visit {visits}. The count equals k, so {cells[node]} is the answer."); ans=cells[node]; break
    snap(node,f"The loop pops {cells[node]} as visit {visits} and then moves to its right child.")
    node=kids[node][1]
assert ans==40
fill(CH,F,block(cells,["node"],st),"@@TRACE1@@")
# Trace 2: range sum 35..65
low,high=35,65; st=[]; total=0
def walk(i):
    global total
    if i is None: return
    v=cells[i]
    if v<low:
        st.append({"at":{"node":i},"vars":{"sum":total},"note":f"{v} is below {low}, so it and its left subtree are skipped and the walk goes right."}); walk(kids[i][1])
    elif v>high:
        st.append({"at":{"node":i},"vars":{"sum":total},"note":f"{v} is above {high}, so it and its right subtree are skipped and the walk goes left."}); walk(kids[i][0])
    else:
        total+=v
        st.append({"at":{"node":i},"vars":{"sum":total},"note":f"{v} lies in the range, so it joins the sum and the walk continues on both sides."}); walk(kids[i][0]); walk(kids[i][1])
walk(0)
assert total==150 and 3 not in [s["at"]["node"] for s in st] and 6 not in [s["at"]["node"] for s in st]
fill(CH,F,block(cells,["node"],st),"@@TRACE2@@")
