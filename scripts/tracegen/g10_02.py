from common import *
CH='10-intervals'
F='02-touching-boundary-semantics.md'
pairs=[([1,3],[3,5]),([1,3],[4,5]),([1,4],[3,6]),([3,3],[1,5])]
st=[]
for i,(a,b) in enumerate(pairs):
    s=max(a[0],b[0]); e=min(a[1],b[1]); c=s<=e; h=s<e
    st.append({"at":{"i":i},"vars":{"largerStart":s,"smallerEnd":e,"closed":"yes" if c else "no","halfOpen":"yes" if h else "no"},"note":f"The pair {a[0]} to {a[1]} and {b[0]} to {b[1]} has larger start {s} and smaller end {e}, so closed says {'yes' if c else 'no'} and half-open says {'yes' if h else 'no'}."})
assert st[0]["vars"]["closed"]=="yes" and st[0]["vars"]["halfOpen"]=="no"
fill(CH,F,block([f"{a[0]}-{a[1]} vs {b[0]}-{b[1]}" for a,b in pairs],["i"],st),"@@TRACE1@@")
iv=[[1,3],[3,5],[7,8]]; reach=3; blocks=1; st=[{"at":{"i":0},"vars":{"reach":3,"blocks":1},"note":"The first range 1 to 3 opens a block, so the reach is 3 and there is 1 block."}]
s,e=iv[1]; blocks+=1; reach=e
st.append({"at":{"i":1},"vars":{"reach":reach,"blocks":blocks},"note":f"The start {s} equals the reach 3. Half-open needs a start strictly below the reach, so a new block opens and the count is {blocks}."})
s,e=iv[2]; blocks+=1; reach=e
st.append({"at":{"i":2},"vars":{"reach":reach,"blocks":blocks},"note":f"The start {s} is past the reach 5, so another block opens and the count is {blocks}."})
assert blocks==3
fill(CH,F,block([f"{a}-{b}" for a,b in iv],["i"],st),"@@TRACE2@@")
