from common import *
CH='15-trees-dfs'
F='07-traversal-reconstruction.md'
def run(pre,ino,ph):
    where={v:i for i,v in enumerate(ino)}
    nxt=[0];st=[]
    def build(lo,hi):
        if lo>hi: return
        i=nxt[0]; nxt[0]+=1
        r=pre[i]; m=where[r]
        st.append({"at":{"pre":i},"vars":{"lo":lo,"hi":hi,"rootPos":m},"note":f"The next walking label is {r}, found at position {m} of the other sheet, so the stretch {lo} to {hi} splits into the left stretch {lo} to {m-1} and the right stretch {m+1} to {hi}."})
        build(lo,m-1); build(m+1,hi)
    build(0,len(ino)-1)
    assert nxt[0]==len(pre)
    fill(CH,F,block([str(x) for x in pre],["pre"],st),ph)
run([3,9,20,15,7],[9,3,15,20,7],"@@TRACE1@@")
run([4,3,2,1],[1,2,3,4],"@@TRACE2@@")
