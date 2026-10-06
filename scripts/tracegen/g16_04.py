from common import *
CH='16-trees-bfs-and-bsts'; F='04-successor-and-predecessor.md'
cells=[5,3,8,2,4,6,9,7]
kids={0:(1,2),1:(3,4),2:(5,6),3:(None,None),4:(None,None),5:(None,7),6:(None,None),7:(None,None)}
def run(key,ph):
    i=0; best=-1; st=[]
    while i is not None:
        v=cells[i]
        if v>key:
            best=i; nxt=kids[i][0]
            note=f"{v} is larger than {key}, so it becomes the candidate and the search goes left."
        else:
            nxt=kids[i][1]
            note=f"{v} is not larger than {key}, so it and its left side are skipped and the search goes right."
        st.append({"at":{"node":i,"best":best},"vars":{"key":key},"note":note})
        i=nxt
    st.append({"at":{"node":-1,"best":best},"vars":{"key":key},"note":f"The search reaches an empty slot, so the answer is the last candidate, {cells[best]}."})
    fill(CH,F,block(cells,["node","best"],st),ph)
    return cells[best]
assert run(7,"@@TRACE1@@")==8
assert run(5,"@@TRACE2@@")==6
