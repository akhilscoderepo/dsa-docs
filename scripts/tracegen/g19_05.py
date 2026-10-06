from common import *
CH='19-recursion-and-backtracking'; F='05-increasing-start-combinations.md'
a=[1,2,3,4]
def run(k,bounded):
    st=[]; path=[]; out=[]
    def go(start):
        if len(path)==k:
            out.append(list(path)); return
        last=len(a)-(k-len(path)) if bounded else len(a)-1
        for i in range(start,last+1):
            path.append(a[i])
            note=f"The call with start {start} chooses {a[i]}, so the path becomes [{','.join(map(str,path))}]."
            if len(path)==k: note+=" The path has the target size, so the call stores a copy."
            elif i==len(a)-1: note+=" The next start is 4, so the child has no index left and stores nothing."
            elif bounded and False: pass
            st.append({"at":{"start":start},"vars":{"path":",".join(map(str,path)),"stored":len(out)+(1 if len(path)==k else 0)},"note":note})
            go(i+1); path.pop()
    go(0); return st,out
st,out=run(2,False); assert len(st)==10 and len(out)==6
fill(CH,F,block(["1","2","3","4"],["start"],st),"@@TRACE1@@")
st,out=run(3,True); print(len(st),len(out)); assert len(out)==4
fill(CH,F,block(["1","2","3","4"],["start"],st),"@@TRACE2@@")
