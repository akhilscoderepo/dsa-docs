from common import *
CH='20-greedy'; F='02-interval-scheduling.md'
def run(iv,ph):
    iv=sorted(iv,key=lambda x:x[1]); st=[]; last=-10**9; acc=0
    for i,(s,e) in enumerate(iv):
        if s>=last: acc+=1; last=e; note=f"The request [{s},{e}) starts at {s}, which is not below lastEnd, so the scan accepts it and sets lastEnd to {e}."
        else: note=f"The request [{s},{e}) starts at {s}, which is below lastEnd = {last}, so the scan rejects it."
        st.append({"at":{"i":i},"vars":{"lastEnd":last if acc else "none","accepted":acc},"note":note})
    fill(CH,F,block([f"{s}-{e}" for s,e in iv],["i"],st),ph); return acc
assert run([[1,3],[2,4],[3,6],[5,7],[6,8]],"@@TRACE1@@")==3
assert run([[0,10],[1,2],[3,4],[5,6]],"@@TRACE2@@")==3
