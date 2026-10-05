from common import *
CH='10-intervals'; FILE='04-intersect-lists.md'
def run(A,B,ph):
    i=j=0; out=[]; st=[{"at":{"i":0,"j":0},"vars":{"found":"none"},"note":"Both cursors start at position 0."}]
    F=lambda l:" ".join(f"[{a},{b}]" for a,b in l) or "none"
    while i<len(A) and j<len(B):
        lo=max(A[i][0],B[j][0]); hi=min(A[i][1],B[j][1])
        if lo<=hi: out.append([lo,hi]); note=f"The pair [{A[i][0]},{A[i][1]}] and [{B[j][0]},{B[j][1]}] shares [{lo},{hi}], which is recorded."
        else: note=f"The pair [{A[i][0]},{A[i][1]}] and [{B[j][0]},{B[j][1]}] shares nothing."
        adv='i' if A[i][1]<B[j][1] else 'j'
        note+=f" The window of {'A' if adv=='i' else 'B'} ends first, so cursor {adv} advances."
        st.append({"at":{"i":i,"j":j},"vars":{"lo":lo,"hi":hi,"found":F(out)},"note":note})
        if adv=='i': i+=1
        else: j+=1
    st.append({"at":{"i":i,"j":j},"vars":{"found":F(out)},"note":"A cursor has left its list, so the pass ends."})
    n=max(len(A),len(B)); fill(CH,FILE,block(list(range(n)),["i","j"],st),ph); return out
A=[[1,4],[6,9],[12,15],[18,20]];B=[[3,7],[8,13],[14,19]]
assert run(A,B,"@@TRACE1@@")==[[3,4],[6,7],[8,9],[12,13],[14,15],[18,19]]
assert run([[1,3],[5,7]],[[3,5],[7,9]],"@@TRACE2@@")==[[3,3],[5,5],[7,7]]
