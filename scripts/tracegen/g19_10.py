from common import *
CH='19-recursion-and-backtracking'; F='10-board-constraints.md'
def bstr(b): return "/".join("".join(r) for r in b)
def run(rows, w, leak):
    R,C=len(rows),len(rows[0]); b=[list(r) for r in rows]; steps=[]
    def st(r,c,exp,matched,note):
        hashes=sum(ch=='#' for row in b for ch in row)
        steps.append({"at":{"cell":r*C+c},"vars":{"matched":matched,"board":bstr(b),"clean":"yes" if hashes==exp else "no"},"note":note})
    def rec(r,c,k):
        if b[r][c]!=w[k]:
            st(r,c,k,k,f"The stone at row {r}, column {c} holds {b[r][c]}, but letter {k+1} of the word is {w[k]}, so this route fails here.")
            return False
        if k==len(w)-1:
            st(r,c,k,k+1,f"The stone at row {r}, column {c} holds {w[k]}, the last letter, so the word is traced.")
            return True
        saved=b[r][c]; b[r][c]='#'
        st(r,c,k+1,k+1,f"The stone at row {r}, column {c} matches {w[k]} and is marked with a hash, so {k+1} letters are matched.")
        found=False
        for dr,dc in((1,0),(-1,0),(0,1),(0,-1)):
            nr,nc=r+dr,c+dc
            if 0<=nr<R and 0<=nc<C and rec(nr,nc,k+1):
                found=True
                break
        if found and leak:
            st(r,c,k,k+1,f"The route succeeded, and the careless code returns now without restoring the stone at row {r}, column {c}, so the hash stays on the board.")
            return True
        b[r][c]=saved
        st(r,c,k,k,f"Every neighbour of the stone at row {r}, column {c} has been tried or the route has succeeded, so its letter {saved} is put back and the board reads {bstr(b)}.")
        return found
    return rec,steps,b
# trace 1
rec,steps,b=run(["aaa","baa"],"aaba",False)
found=None
for r in range(2):
    for c in range(3):
        if rec(r,c,0): found=(r,c); break
    if found: break
assert found is not None and bstr(b)=="aaa/baa" and all(s["vars"]["clean"]=="yes" for s in steps)
fill(CH,F,block(list("aaabaa"),["cell"],steps),"@@TRACE1@@")
# trace 2: leaking version, scan all starts
rec,steps,b=run(["aaa","bba"],"bba",True)
starts=[]
for r in range(2):
    for c in range(3):
        if rec(r,c,0): starts.append([r,c])
assert starts==[[1,0]], starts
assert any(s["vars"]["clean"]=="no" for s in steps)
fill(CH,F,block(list("aaabba"),["cell"],steps),"@@TRACE2@@")
