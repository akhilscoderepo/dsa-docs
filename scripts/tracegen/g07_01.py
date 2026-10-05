from common import *
CH='07-prefix-sums-and-difference-arrays'
def build(a,ph):
    pre=[0]; st=[{"at":{"i":-1},"vars":{"prefix":"[0]"},"note":"Start with the sentinel entry prefix[0] = 0, the sum of zero values."}]
    for i,v in enumerate(a):
        pre.append(pre[-1]+v)
        st.append({"at":{"i":i},"vars":{"nums[i]":str(v),"prefix":str(pre)},"note":f"Add {v} to {pre[i]} and store {pre[i+1]} as prefix[{i+1}]."})
    fill(CH,'01-prefix-construction.md',block(a,["i"],st),ph); return pre
assert build([3,1,4,1,5],"@@TRACE1@@")==[0,3,4,8,9,14]
def pivot(a,ph):
    pre=[0]
    for v in a: pre.append(pre[-1]+v)
    tot=pre[-1]; st=[]; res=-1
    for i,v in enumerate(a):
        l=pre[i]; r=tot-pre[i+1]
        if l==r:
            st.append({"at":{"i":i},"vars":{"left":str(l),"right":str(r)},"note":f"Left side {l} equals right side {r}, so index {i} is the pivot."}); res=i; break
        st.append({"at":{"i":i},"vars":{"left":str(l),"right":str(r)},"note":f"Left side {l} differs from right side {r}, so the loop moves on."})
    fill(CH,'01-prefix-construction.md',block(a,["i"],st),ph); return res
assert pivot([1,7,3,6,5,6],"@@TRACE2@@")==3
