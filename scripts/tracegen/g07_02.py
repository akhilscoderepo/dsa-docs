from common import *
CH='07-prefix-sums-and-difference-arrays'
def q(a,l,r,ph):
    pre=[0]
    for v in a: pre.append(pre[-1]+v)
    st=[{"at":{"left":-1,"end":-1},"vars":{"query":f"[{l}, {r}]"},"note":f"The prefix array is ready. The query is [{l}, {r}], so the two reads are prefix[{r+1}] and prefix[{l}]."},
        {"at":{"left":-1,"end":r+1},"vars":{"prefix[end]":str(pre[r+1])},"note":f"Read prefix[{r+1}] = {pre[r+1]}, the sum of the first {r+1} values."},
        {"at":{"left":l,"end":r+1},"vars":{"prefix[end]":str(pre[r+1]),"prefix[left]":str(pre[l])},"note":f"Read prefix[{l}] = {pre[l]}, the sum of the first {l} values."},
        {"at":{"left":l,"end":r+1},"vars":{"answer":f"{pre[r+1]} - {pre[l]} = {pre[r+1]-pre[l]}"},"note":f"The shared first {l} values cancel, so the answer is {pre[r+1]-pre[l]}."}]
    fill(CH,'02-range-queries.md',block(pre,["left","end"],st),ph); return pre[r+1]-pre[l]
a=[2,4,1,5,3,6]
assert q(a,1,3,"@@TRACE1@@")==10
assert q(a,0,5,"@@TRACE2@@")==21
