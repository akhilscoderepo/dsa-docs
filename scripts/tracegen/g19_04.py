from common import *
CH='19-recursion-and-backtracking'; F='04-permutations.md'
a=[1,2,3]; used=[False]*3; path=[]; st=[]; out=[]
def U(): return "".join("T" if u else "F" for u in used)
def go():
    if len(path)==3: out.append(list(path)); return
    for i in range(3):
        if used[i]: continue
        used[i]=True; path.append(a[i])
        d=len(path)-1
        note=f"The call at depth {d} chooses index {i}, so the path becomes [{','.join(map(str,path))}]."
        if len(path)==3: note+=" The path is full, so the leaf stores a copy."
        st.append({"at":{"i":i},"vars":{"path":",".join(map(str,path)),"used":U()},"note":note})
        go(); path.pop(); used[i]=False
go()
assert len(out)==6 and len(st)==15 and out[-1]==[3,2,1]
fill(CH,F,block(["1","2","3"],["i"],st),"@@TRACE1@@")
b=[1,2]; used=[False]*2; path=[]; st=[]; out=[]
def go2():
    if len(path)==2: out.append(list(path)); return
    for i in range(2):
        if used[i]: continue
        used[i]=True; path.append(b[i])
        st.append({"at":{"i":i},"vars":{"path":",".join(map(str,path)),"used":U()},"note":f"The call at depth {len(path)-1} chooses index {i}, so the path becomes [{','.join(map(str,path))}]."+(" The path is full, so the leaf stores a copy." if len(path)==2 else "")})
        go2(); path.pop()           # the mark is NOT cleared
        st.append({"at":{"i":i},"vars":{"path":",".join(map(str,path)) or "empty","used":U()},"note":f"The undo step removes the value of index {i} from the path but leaves its mark true."})
go2()
assert out==[[1,2]]
fill(CH,F,block(["1","2"],["i"],st),"@@TRACE2@@")
