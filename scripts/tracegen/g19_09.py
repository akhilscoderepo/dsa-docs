from common import *
CH='19-recursion-and-backtracking'; F='09-partition-generation.md'
s="aba"; st=[]; path=[]; out=[]
def pal(l,h):
    while l<h:
        if s[l]!=s[h]: return False
        l+=1;h-=1
    return True
def go(start):
    if start==len(s):
        out.append(list(path)); return
    for end in range(start+1,len(s)+1):
        f=s[start:end]; p=",".join(path) or "empty"
        if not pal(start,end-1):
            st.append({"at":{"start":start,"end":end},"vars":{"path":p,"stored":len(out)},"note":f"The field {f} does not read the same in both directions, so the call skips this piece end."}); continue
        path.append(f)
        will=(end==len(s))
        note=f"The call at start {start} tests the piece end {end}. The field {f} passes, so the path becomes [{','.join(path)}]."
        if will: note+=" The new start position equals the length, which is the empty suffix, so the search stores a copy."
        st.append({"at":{"start":start,"end":end},"vars":{"path":",".join(path),"stored":len(out)+(1 if will else 0)},"note":note})
        go(end); path.pop()
go(0)
assert out==[["a","b","a"],["aba"]]
fill(CH,F,block(list(s),["start","end"],st),"@@TRACE1@@"); print(len(st))
st=[{"at":{"i":0},"vars":{"kept":"a","covered":1},"note":"The subset search includes a, so the path holds the letter a."},
    {"at":{"i":1},"vars":{"kept":"a","covered":1},"note":"The search excludes b, so no field covers the letter at position 1."},
    {"at":{"i":2},"vars":{"kept":"ac","covered":2},"note":"The search includes c and stores the list a, c. Only 2 of 3 positions are covered, so it is not a cut."}]
fill(CH,F,block(["a","b","c"],["i"],st),"@@TRACE2@@")
