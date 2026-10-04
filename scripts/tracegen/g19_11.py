from common import *
CH='19-recursion-and-backtracking'; F='11-trie-and-backtracking.md'
class N:
    def __init__(s): s.k={}; s.w=None
def build(ws):
    r=N()
    for w in ws:
        n=r
        for ch in w: n=n.k.setdefault(ch,N())
        n.w=w
    return r
def hunt(row, words):
    root=build(words); marked=[False]*len(row); found=[]; steps=[]
    def st(c,prefix,note):
        steps.append({"at":{"cell":c},"vars":{"prefix":prefix or "root","found":",".join(found) if found else "none"},"note":note})
    def dfs(c,par,prefix):
        if c<0 or c>=len(row): return
        if marked[c]:
            st(c,prefix,f"The tile {c} holding {row[c]} is already on the route, so the walk may not return to it.")
            return
        n=par.k.get(row[c])
        if n is None:
            st(c,prefix,f"The cursor at {prefix or 'the root'} has no child for the letter {row[c]}, so no listed word continues this way and the tile is not entered.")
            return
        p=prefix+row[c]
        note=f"The tile {c} is entered, and the cursor moves to the node for {p}."
        if n.w is not None:
            found.append(n.w)
            note+=f" That node stores the word {n.w}, so it is emitted and cleared from the node."
            n.w=None
        marked[c]=True
        st(c,p,note)
        dfs(c-1,n,p); dfs(c+1,n,p)
        marked[c]=False
        st(c,p,f"Both neighbours of tile {c} have been tried, so its marker is lifted and the cursor goes back to {prefix or 'the root'}.")
    for c in range(len(row)): dfs(c,root,"")
    return sorted(found),steps
res,steps=hunt("oath",["oat","oath","hat"])
assert res==["oat","oath"]
fill(CH,F,block(list("oath"),["cell"],steps),"@@TRACE1@@")
res,steps=hunt("aaa",["aa"])
assert res==["aa"]
fill(CH,F,block(list("aaa"),["cell"],steps),"@@TRACE2@@")
print(len(steps))
