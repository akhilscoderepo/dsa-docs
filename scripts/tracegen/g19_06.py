from common import *
CH='19-recursion-and-backtracking'; F='06-reusable-candidates.md'
c=[2,3,7]; st=[]; path=[]; out=[]
def go(start,rem):
    if rem==0: out.append(list(path)); return
    for i in range(start,len(c)):
        path.append(c[i]); nr=rem-c[i]; p=",".join(map(str,path))
        if nr<0: note=f"The call with start {start} chooses {c[i]}, and the remaining target becomes {nr}. The path overshoots, so the child returns at once."
        elif nr==0: note=f"The call with start {start} chooses {c[i]}, and the remaining target becomes 0. The child stores [{p}]."
        else: note=f"The call with start {start} chooses {c[i]}, and the remaining target becomes {nr}."
        st.append({"at":{"start":start},"vars":{"remain":nr,"stored":len(out)+(1 if nr==0 else 0)},"note":note})
        if nr>0: go(i,nr)
        elif nr==0: out.append(list(path))
        path.pop()
go(0,7)
assert out==[[2,2,3],[7]]; print(len(st))
fill(CH,F,block([str(x) for x in c],["start"],st),"@@TRACE1@@")
c2=[1,2]; st=[]; path=[]; out=[]
def g2(rem):
    if rem==0: out.append(list(path)); return
    for i in range(2):
        if c2[i]>rem: continue
        path.append(c2[i]); nr=rem-c2[i]
        st.append({"at":{"start":0},"vars":{"remain":nr,"stored":len(out)+(1 if nr==0 else 0)},"note":f"The loop restarts at coin 1, and it chooses {c2[i]}, so the path becomes [{','.join(map(str,path))}] with the remaining target {nr}."+(f" The path adds up to 3, so the search stores [{','.join(map(str,path))}]." if nr==0 else "")})
        g2(nr); path.pop()
g2(3)
assert out==[[1,1,1],[1,2],[2,1]]; print(len(st))
fill(CH,F,block(["1","2"],["start"],st),"@@TRACE2@@")
