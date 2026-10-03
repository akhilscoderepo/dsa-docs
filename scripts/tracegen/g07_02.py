from common import *
CH='07-prefix-sums-and-difference-arrays'
F='02-range-queries.md'
a=[3,1,4,1,5,9,2,6]; pre=[0]
for x in a: pre.append(pre[-1]+x)
assert pre==[0,3,4,8,9,14,23,25,31]
l,r=2,5
st=[{"at":{"lo":l,"hi":r+1},"vars":{"left":l,"right":r},"note":f"The question covers days {l} to {r}. The slot after the last day is {r+1} and the slot before the first day is {l}."},
{"at":{"lo":l,"hi":r+1},"vars":{"slotHigh":pre[r+1],"slotLow":pre[l]},"note":f"Read slot {r+1}, which holds {pre[r+1]}, and slot {l}, which holds {pre[l]}."},
{"at":{"lo":l,"hi":r+1},"vars":{"answer":pre[r+1]-pre[l]},"note":f"Subtract: {pre[r+1]} - {pre[l]} = {pre[r+1]-pre[l]}, the sum of {a[2]}, {a[3]}, {a[4]} and {a[5]}."}]
assert pre[r+1]-pre[l]==19==sum(a[l:r+1])
fill(CH,F,block([str(x) for x in pre],["lo","hi"],st),"@@TRACE1@@")
qs=[(4,4),(0,7),(3,3)]; st=[]
for l,r in qs:
    ans=pre[r+1]-pre[l]; assert ans==sum(a[l:r+1])
    kind="a single day" if l==r else "the whole ledger"
    extra=" The left slot is the sentinel at position 0, which holds 0, so no special case is needed." if l==0 else ""
    st.append({"at":{"lo":l,"hi":r+1},"vars":{"left":l,"right":r,"answer":ans},"note":f"The question is {kind}, days {l} to {r}: slot {r+1} minus slot {l} is {pre[r+1]} - {pre[l]} = {ans}."+extra})
assert "sentinel" in st[1]["note"]
fill(CH,F,block([str(x) for x in pre],["lo","hi"],st),"@@TRACE2@@")
