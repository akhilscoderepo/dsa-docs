from common import *
CH='19-recursion-and-backtracking'; F='07-duplicate-control.md'
a=[1,2,2]
def run(check_zero):
    st=[]; path=[]; out=[]
    def go(start):
        out.append(list(path)); s=",".join(map(str,path))
        st.append({"at":{"start":start},"vars":{"path":s or "empty","stored":len(out)},"note":(f"The call with start {start} stores [{s}]." if path else "The root call with start 0 stores the empty list.")})
        for i in range(start,3):
            lim=0 if check_zero else start
            if i>lim and a[i]==a[i-1]:
                st.append({"at":{"start":start},"vars":{"path":s or "empty","stored":len(out)},"note":f"The loop reaches index {i}, where {a[i]} equals its left neighbour and i is above {'0' if check_zero else 'start'}, so it skips the choice."})
                continue
            path.append(a[i]); go(i+1); path.pop()
    go(0); return st,out
st,out=run(False); assert len(out)==6; print(len(st))
fill(CH,F,block(["1","2","2"],["start"],st),"@@TRACE1@@")
st,out=run(True); assert [1,2,2] not in out and len(out)==4; print(len(st))
fill(CH,F,block(["1","2","2"],["start"],st),"@@TRACE2@@")
