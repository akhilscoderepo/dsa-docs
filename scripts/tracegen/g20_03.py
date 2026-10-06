from common import *
CH='20-greedy'; F='03-farthest-frontier.md'
def run(p,ph):
    st=[]; far=0; res=None
    for i in range(len(p)):
        if i>far:
            st.append({"at":{"i":i},"vars":{"farthest":far},"note":f"Index {i} is beyond farthest = {far}, so no scanned station forwards that far. The answer is false."}); res=False; break
        far=max(far,i+p[i])
        note=f"Station {i} has power {p[i]}, so it forwards to index {i+p[i]}, and farthest becomes {far}."
        if far>=len(p)-1: note+=" This is the last index, so the answer is true."; res=True
        st.append({"at":{"i":i},"vars":{"farthest":far},"note":note})
        if res: break
    fill(CH,F,block(p,["i"],st),ph); return res
assert run([2,1,1,2,4],"@@TRACE1@@")==True
assert run([3,2,1,0,4],"@@TRACE2@@")==False
