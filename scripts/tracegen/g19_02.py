from common import *
CH='19-recursion-and-backtracking'; F='02-choose-explore-unchoose.md'
cells=["flag 0","flag 1"]
def run(undo):
    st=[]; path=[]; out=[]
    def show(): return ",".join(map(str,path)) or "empty"
    def rec(d,limit):
        if d==2:
            out.append(list(path))
            st.append({"at":{"d":d},"vars":{"path":show(),"stored":len(out)},"note":f"The depth equals 2, so the leaf stores the snapshot [{show()}]."}); return
        for v in (0,1):
            if not undo and len(st)>=8: return
            path.append(v)
            st.append({"at":{"d":d},"vars":{"path":show(),"stored":len(out)},"note":f"The call at depth {d} adds {v}, so the working path is [{show()}]."})
            rec(d+1,limit)
            if undo:
                path.pop()
                st.append({"at":{"d":d},"vars":{"path":show(),"stored":len(out)},"note":f"The undo step removes the {v} from depth {d}, so the working path is [{show()}]."})
    rec(0,0); return st,out
st,out=run(True)
assert out==[[0,0],[0,1],[1,0],[1,1]] and len(st)==16
fill(CH,F,block(cells,["d"],st),"@@TRACE1@@")
# no undo: hand simulation of the first 5 steps
path=[];st=[];out=[]
def add(d,v,note):
    path.append(v); st.append({"at":{"d":d},"vars":{"path":",".join(map(str,path)),"stored":len(out)},"note":note})
add(0,0,"The call at depth 0 adds 0, so the working path is [0].")
add(1,0,"The call at depth 1 adds 0, so the working path is [0,0].")
out.append(list(path)); st.append({"at":{"d":2},"vars":{"path":"0,0","stored":1},"note":"The depth equals 2, so the leaf stores the snapshot [0,0]. No undo step follows."})
add(1,1,"The loop at depth 1 adds 1 to a path that still holds two entries, so the path is [0,0,1], longer than the two decisions.")
out.append(list(path)); st.append({"at":{"d":2},"vars":{"path":"0,0,1","stored":2},"note":"The leaf stores the snapshot [0,0,1], a third entry for two flags. The output is already wrong."})
assert len(path)==3
fill(CH,F,block(cells,["d"],st),"@@TRACE2@@")
