from common import *
from tr import *
CH='15-trees-dfs'
F='08-morris-traversal.md'
def run(arr,ph):
    L,R=parse(arr); R=dict(R)
    cur=0; sheet=[]; ropes={}; st=[]
    def snap(i,note):
        st.append({"at":{"cur":i},"vars":{"sheet":" ".join(map(str,sheet)),"ropes":len(ropes)},"note":note})
    while cur is not None:
        if L[cur] is None:
            sheet.append(arr[cur])
            nxt=R[cur]
            snap(cur,f"The bench {arr[cur]} has no left path, so it is recorded at once and the keeper moves right.")
            cur=nxt; continue
        pred=L[cur]
        while R[pred] is not None and R[pred]!=cur: pred=R[pred]
        if R[pred] is None:
            R[pred]=cur; ropes[pred]=cur
            snap(cur,f"The bench {arr[cur]} has a left path whose last bench {arr[pred]} has a free right link, so a rope is tied from {arr[pred]} to {arr[cur]} and the keeper goes left.")
            cur=L[cur]
        else:
            R[pred]=None; del ropes[pred]
            sheet.append(arr[cur])
            snap(cur,f"The keeper returned to {arr[cur]} along its rope from {arr[pred]}, so the rope is cut, the bench is recorded, and he moves right.")
            cur=R[cur]
    assert not ropes
    fill(CH,F,block(cells(arr),["cur"],st),ph)
    return sheet
assert run([4,2,7,1,3],"@@TRACE1@@")==[1,2,3,4,7]
assert run([3,2,None,1],"@@TRACE2@@")==[1,2,3]
