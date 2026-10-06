from common import *
CH='16-trees-bfs-and-bsts'; F='09-balanced-tree-concepts.md'
cells=[1,2,3,4,5,6,7]
# chain search for 7: keys 1..7 in order; compact path 4,6,7
comp=[4,6,7]
st=[]
for s in range(1,8):
    c=s-1
    b=cells.index(comp[s-1]) if s<=3 else -1
    nb=f"The compact tree compares 7 with {comp[s-1]}." if s<=3 else "The compact tree is finished."
    if s==3: nb="The compact tree compares 7 with 7 and stops with a match."
    st.append({"at":{"chain":c,"compact":b},"vars":{"step":s},"note":f"The chain compares 7 with {s}"+(" and stops with a match. " if s==7 else " and goes right. ")+nb})
fill(CH,F,block(cells,["chain","compact"],st),"@@TRACE1@@")
cells=[1,2,3]
st=[{"at":{"top":2},"vars":{"height":3},"note":"Start: the tree is the left chain 3, 2, 1. The top key is 3 and the height is 3."},
{"at":{"top":2},"vars":{"height":3},"note":"The method takes y = 2, the left child of 3. The right subtree of 2 is empty, so it becomes the new left subtree of 3."},
{"at":{"top":1},"vars":{"height":2},"note":"The method makes 3 the right child of 2 and returns 2 as the new top. The height is 2, and the sorted order is still 1, 2, 3."}]
fill(CH,F,block(cells,["top"],st),"@@TRACE2@@")
