from common import *
CH='16-trees-bfs-and-bsts'; F='03-validate-search-and-insert.md'
cells=[20,10,30,5,15,25,35]; kids={0:(1,2),1:(3,4),2:(5,6),3:(None,None),4:(None,None),5:(None,None),6:(None,None)}
key=25; i=0; st=[]
while True:
    v=cells[i]
    if v==key:
        st.append({"at":{"node":i},"vars":{"key":key},"note":f"The key {key} equals the node key {v}, so the search stops with a match."}); break
    d=0 if key<v else 1
    st.append({"at":{"node":i},"vars":{"key":key},"note":f"The key {key} is {'smaller' if d==0 else 'larger'} than {v}, so the search goes {'left' if d==0 else 'right'} and drops the other subtree."})
    i=kids[i][d]
assert i==5 and len(st)==3
fill(CH,F,block(cells,["node"],st),"@@TRACE1@@")
cells=[20,10,30,5,15,25,35,12]; key=12; i=0; st=[]
while True:
    v=cells[i]; d=0 if key<v else 1
    nxt=kids[i][d]
    if nxt is None:
        st.append({"at":{"node":i},"vars":{"key":key},"note":f"The key {key} is {'smaller' if d==0 else 'larger'} than {v}, and the {'left' if d==0 else 'right'} slot is empty, so this slot is the insertion point."}); break
    st.append({"at":{"node":i},"vars":{"key":key},"note":f"The key {key} is {'smaller' if d==0 else 'larger'} than {v}, so the walk goes {'left' if d==0 else 'right'}."})
    i=nxt
assert i==4
st.append({"at":{"node":7},"vars":{"key":key},"note":"The method writes the new node 12 into the empty left slot of the node 15."})
fill(CH,F,block(cells,["node"],st),"@@TRACE2@@")
