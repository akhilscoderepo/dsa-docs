from common import *
CH='16-trees-bfs-and-bsts'; F='92-search-and-validate-a-search-tree.md'
cells=[20,10,30,5,25]; kids={0:(1,2),1:(3,4),2:(None,None),3:(None,None),4:(None,None)}
key=25; i=0; st=[]
while i is not None:
    v=cells[i]; d=0 if key<v else 1
    st.append({"at":{"node":i},"vars":{"key":key},"note":f"The key {key} is {'smaller' if d==0 else 'larger'} than {v}, so the lookup goes {'left' if d==0 else 'right'}."})
    i=kids[i][d]
st.append({"at":{"node":-1},"vars":{"key":key},"note":"The lookup reaches an empty slot without meeting a node that holds 25, so the node 25 is not where its key belongs."})
assert len(st)==3
fill(CH,F,block(cells,["node"],st),"@@TRACE1@@")
st=[]; ok=True
def f(i,low,high,why):
    global ok
    if i is None or not ok: return
    v=cells[i]; lo="none" if low is None else low; hi="none" if high is None else high
    bad=(low is not None and v<=low) or (high is not None and v>=high)
    if bad:
        st.append({"at":{"node":i},"vars":{"low":lo,"high":hi},"note":f"{why} The key {v} is not between {lo} and {hi}, so the pass reports the fault."}); ok=False; return
    st.append({"at":{"node":i},"vars":{"low":lo,"high":hi},"note":f"{why} The key {v} lies between {lo} and {hi}."})
    l,r=kids[i]; f(l,low,v,f"Left of {v}: the upper bound becomes {v}."); f(r,v,high,f"Right of {v}: the lower bound becomes {v}.")
f(0,None,None,"The root starts with no limit.")
assert not ok and len(st)==4 and st[-1]["at"]["node"]==4
fill(CH,F,block(cells,["node"],st),"@@TRACE2@@")
