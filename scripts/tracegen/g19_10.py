from common import *
CH='19-recursion-and-backtracking'; F='10-board-constraints.md'
b=["aa","ab"]; w="aaa"; R=C=2
def idx(r,c): return r*C+c
def run(unmark):
    st=[]; on=[[False]*C for _ in range(C)]; mk=[0]
    def log(cell,note): st.append({"at":{"cell":cell},"vars":{"marks":mk[0],"letter":None},"note":note})
    def go(r,c,k):
        if not(0<=r<R and 0<=c<C): return False
        if on[r][c]: return False
        if b[r][c]!=w[k]: return False
        if k==len(w)-1:
            st.append({"at":{"cell":idx(r,c)},"vars":{"marks":mk[0],"k":k+1},"note":f"The cell {idx(r,c)} holds {b[r][c]}, which is the last letter of the word, so the search succeeds."}); return True
        on[r][c]=True; mk[0]+=1
        st.append({"at":{"cell":idx(r,c)},"vars":{"marks":mk[0],"k":k+1},"note":f"The search enters cell {idx(r,c)}, which holds {b[r][c]}, and sets its mark."})
        found=False
        for dr,dc in((-1,0),(1,0),(0,-1),(0,1)):
            if go(r+dr,c+dc,k+1): found=True; break
        if unmark or found:
            on[r][c]=False; mk[0]-=1
            if not found: st.append({"at":{"cell":idx(r,c)},"vars":{"marks":mk[0],"k":k},"note":f"No neighbour of cell {idx(r,c)} completes the word, so the unmark step clears its mark."})
        return found
    res=False
    for r in range(R):
        for c in range(C):
            if on[r][c]:
                if not unmark and not res: st.append({"at":{"cell":idx(r,c)},"vars":{"marks":mk[0],"k":0},"note":f"The start at cell {idx(r,c)} finds its own mark still set, so it stops at once."})
                continue
            if go(r,c,0): res=True; break
        if res: break
    return st,res
st,res=run(True); assert res; print(len(st))
for s in st: s["vars"].pop("letter",None)
fill(CH,F,block(list("aaab"),["cell"],st),"@@TRACE1@@")
st,res=run(False); print(len(st),res)
for s in st: s["vars"].pop("letter",None)
fill(CH,F,block(list("aaab"),["cell"],st),"@@TRACE2@@")
